import flet as ft
from sidebar import build_sidebar
from datetime import date
from connector import get_connection
# Compatibilidad íconos (Flet nuevo)
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons


def movimientos_view(page: ft.Page, nombre: str) -> ft.View:
    # -----------------------------
    # Navegación
    # -----------------------------
    def volver_pos(e=None):
        if len(page.views) > 1:
            page.views.pop()
        page.update()

    def cerrar_sesion(e):
        from login import LoginView
        page.views.clear()
        page.views.append(LoginView(page))
        page.go("/")
        page.update()

    def ir_inicio(e=None):
        volver_pos()

    def ir_inventario(e=None):
        from inventario import inventario_view
        page.views.append(inventario_view(page, nombre))
        page.update()

    def ir_movimientos(e=None):
        pass

    def ir_caja_chica(e=None):
        from caja_chica import caja_chica_view
        page.views.append(caja_chica_view(page, nombre))
        page.update()

    # -----------------------------
    # Helpers UI compatibles
    # -----------------------------
    def open_overlay(ctrl):
        if hasattr(page, "open"):
            page.open(ctrl)
        else:
            page.dialog = ctrl
            ctrl.open = True
            page.update()

    def show_snack(texto: str):
        sb = ft.SnackBar(content=ft.Text(texto))
        if hasattr(page, "open"):
            page.open(sb)
        else:
            page.snack_bar = sb
            sb.open = True
            page.update()

    sidebar = build_sidebar(
    page=page,
    nombre=nombre,
    ir_inicio=ir_inicio,
    ir_inventario=ir_inventario,
    ir_movimientos=ir_movimientos,
    ir_caja_chica=ir_caja_chica,
    cerrar_sesion_real=cerrar_sesion,
)

    # -----------------------------
    # BD
    # -----------------------------
    def db_listar_productosstock():
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    p.IdProductos,
                    p.Nombre,
                    p.Descripcion,
                    p.CorteCaja_idCorteCaja,
                    COALESCE(ps.IdProductosStock, 0) AS IdProductosStock,
                    COALESCE(ps.Cantidad, 0) AS Cantidad
                FROM productos p
                LEFT JOIN productosstock ps
                    ON TRIM(LOWER(ps.Nombre)) = TRIM(LOWER(p.Nombre))
                ORDER BY p.Nombre ASC
                """
            )
            return cur.fetchall() or []
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except:
                pass

    def db_listar_movimientos(limit=100):
        """
        Une entradas + salidas y las devuelve ordenadas.
        Guardamos producto dentro de Descripcion/Detalle como: ID|NOMBRE|DESC
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                f"""
                SELECT
                    'Entrada' AS Tipo,
                    Fecha AS FechaMov,
                    Cantidad AS Cant,
                    Descripcion AS Texto
                FROM entradasproductos
                UNION ALL
                SELECT
                    'Salida' AS Tipo,
                    FechaSalida AS FechaMov,
                    CAST(Cantidad AS DECIMAL(10,2)) AS Cant,
                    Detalle AS Texto
                FROM salidasproductos
                ORDER BY FechaMov DESC
                LIMIT {int(limit)}
                """
            )
            return cur.fetchall() or []
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except:
                pass

    def db_registrar_movimiento(tipo: str, id_prod: int, nombre_prod: str, cantidad: float, descripcion: str):
        """
        Regla clave:
        - Entrada: suma stock y registra en entradasproductos
        - Salida: valida stock suficiente, resta stock y registra en salidasproductos
        - Si el producto existe en productos pero no en productosstock y la operación es Entrada,
          se crea automáticamente su registro de stock.
        Todo en una transacción (commit/rollback).
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT IdProductosStock, Cantidad, CorteCaja_idCorteCaja
                FROM productosstock
                WHERE TRIM(LOWER(Nombre)) = TRIM(LOWER(%s))
                FOR UPDATE
                """,
                (nombre_prod,),
            )
            row = cur.fetchone()

            if row:
                id_stock = int(row["IdProductosStock"])
                stock_actual = float(row["Cantidad"] or 0)
                corte_id = int(row.get("CorteCaja_idCorteCaja") or 1)
            else:
                id_stock = None
                stock_actual = 0.0
                corte_id = 1

            if tipo == "Salida" and cantidad > stock_actual:
                raise Exception(f"No puedes sacar {cantidad} porque solo hay {stock_actual} en stock.")

            if not row and tipo == "Entrada":
                nuevo_stock = float(cantidad)
                cur.execute(
                    """
                    INSERT INTO productosstock (Nombre, Descripcion, Cantidad, CorteCaja_idCorteCaja)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (nombre_prod, (descripcion or "")[:35], nuevo_stock, corte_id),
                )
            elif row:
                if tipo == "Entrada":
                    nuevo_stock = stock_actual + cantidad
                else:
                    nuevo_stock = stock_actual - cantidad

                cur.execute(
                    """
                    UPDATE productosstock
                    SET Cantidad=%s,
                        Descripcion=%s
                    WHERE IdProductosStock=%s
                    """,
                    (nuevo_stock, (descripcion or "")[:35], id_stock),
                )
            else:
                raise Exception("Ese producto aún no tiene stock registrado. Primero realiza una entrada.")

            texto = f"{id_prod}|{nombre_prod}|{descripcion}".strip()

            if tipo == "Entrada":
                cur.execute(
                    """
                    INSERT INTO entradasproductos (Cantidad, Fecha, Descripcion, CorteCaja_idCorteCaja)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (int(cantidad), date.today(), texto, corte_id),
                )
            else:
                cur.execute(
                    """
                    INSERT INTO salidasproductos (FechaSalida, Detalle, Cantidad, CorteCaja_idCorteCaja)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (date.today(), texto, str(float(cantidad)), corte_id),
                )

            conn.commit()
            return nuevo_stock

        except:
            try:
                if conn:
                    conn.rollback()
            except:
                pass
            raise
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except:
                pass

    # -----------------------------
    # UI Formulario
    # -----------------------------
    productos = db_listar_productosstock()
    opciones = [
        ft.dropdown.Option(
            key=str(p["IdProductos"]),
            text=f'{p["Nombre"]} (Stock: {p["Cantidad"]})',
        )
        for p in productos
    ]

    dd_producto = ft.Dropdown(
        label="Producto",
        options=opciones,
        border_radius=12,
        width=420,
    )

    dd_tipo = ft.Dropdown(
        label="Tipo de movimiento",
        options=[ft.dropdown.Option("Entrada"), ft.dropdown.Option("Salida")],
        value="Entrada",
        border_radius=12,
        width=220,
    )

    txt_cantidad = ft.TextField(
        label="Cantidad",
        border_radius=12,
        width=220,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    txt_desc = ft.TextField(
        label="Descripción (motivo)",
        border_radius=12,
        width=420,
        multiline=True,
        min_lines=2,
        max_lines=3,
    )

    # -----------------------------
    # Tabla movimientos
    # -----------------------------
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Descripción")),
        ],
        rows=[],
        border_radius=12,
        heading_row_color="#F3E9F7",
        data_row_min_height=52,
        data_row_max_height=80,
    )

    def parse_texto(texto: str):
        # Espera: ID|NOMBRE|DESC
        try:
            parts = (texto or "").split("|", 2)
            if len(parts) == 3:
                return parts[0].strip(), parts[1].strip(), parts[2].strip()
        except:
            pass
        return "", "Desconocido", (texto or "")

    def recargar_tabla():
        movimientos = db_listar_movimientos(limit=150)
        tabla.rows = []
        for m in movimientos:
            pid, pnom, desc = parse_texto(m.get("Texto"))
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(m.get("FechaMov")))),
                        ft.DataCell(ft.Text(str(m.get("Tipo")))),
                        ft.DataCell(ft.Text(f"{pnom}")),
                        ft.DataCell(ft.Text(str(m.get("Cant")))),
                        ft.DataCell(ft.Text(desc)),
                    ]
                )
            )
        page.update()

    def recargar_dropdown_productos():
        nonlocal productos
        productos = db_listar_productosstock()
        dd_producto.options = [
            ft.dropdown.Option(
                key=str(p["IdProductos"]),
                text=f'{p["Nombre"]} (Stock: {p["Cantidad"]})',
            )
            for p in productos
        ]
        dd_producto.value = None
        page.update()

    def validar_form():
        ok = True
        dd_producto.error_text = None
        txt_cantidad.error_text = None
        txt_desc.error_text = None

        if not dd_producto.value:
            dd_producto.error_text = "Selecciona un producto"
            ok = False

        c_raw = (txt_cantidad.value or "").strip()
        try:
            c = float(c_raw)
        except:
            c = -1

        if c <= 0:
            txt_cantidad.error_text = "Ingresa una cantidad válida (> 0)"
            ok = False

        d = (txt_desc.value or "").strip()
        if not d:
            txt_desc.error_text = "Escribe una descripción"
            ok = False

        page.update()
        return ok, c, d

    def guardar_movimiento(e):
        ok, c, d = validar_form()
        if not ok:
            return

        tipo = dd_tipo.value
        id_prod = int(dd_producto.value)

        # tomar nombre del producto del dropdown (más seguro: buscar en lista)
        nombre_prod = None
        for p in productos:
            if int(p["IdProductos"]) == id_prod:
                nombre_prod = str(p["Nombre"])
                break
        if not nombre_prod:
            show_snack("Producto no encontrado. Recarga e intenta de nuevo.")
            return

        try:
            nuevo_stock = db_registrar_movimiento(tipo, id_prod, nombre_prod, c, d)
            # limpiar
            txt_cantidad.value = ""
            txt_desc.value = ""
            page.update()

            recargar_dropdown_productos()
            recargar_tabla()
            show_snack(f"{tipo} registrada ✅ Nuevo stock: {nuevo_stock}")
        except Exception as ex:
            open_overlay(ft.AlertDialog(title=ft.Text("No se pudo registrar"), content=ft.Text(str(ex))))

    recargar_tabla()

    # -----------------------------
    # Layout principal
    # -----------------------------
    header = ft.Row(
        [
            ft.Text("Entradas y Salidas", size=22, weight="bold", color="#C86DD7"),
            ft.Container(expand=True),
        ]
    )

    formulario = ft.Container(
        bgcolor="white",
        border_radius=18,
        padding=15,
        content=ft.Column(
            [
                ft.Text("Registrar movimiento", size=16, weight="bold"),
                ft.Row([dd_tipo, txt_cantidad], spacing=12),
                dd_producto,
                txt_desc,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Guardar",
                            bgcolor="#C86DD7",
                            color="white",
                            on_click=guardar_movimiento,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), padding=18),
                        ),
                        ft.TextButton("Recargar tabla", on_click=lambda e: recargar_tabla()),
                    ],
                    spacing=12,
                ),
            ],
            spacing=10,
        ),
    )

    listado = ft.Container(
        expand=True,
        bgcolor="white",
        border_radius=18,
        padding=15,
        content=ft.Column(
            [
                ft.Text("Historial de movimientos", size=16, weight="bold"),
                ft.Container(expand=True, content=ft.ListView(expand=True, controls=[tabla])),
            ],
            expand=True,
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor="#F9F6FB",
        padding=20,
        content=ft.Column(
            [
                header,
                ft.Container(height=10),
                formulario,
                ft.Container(height=10),
                listado,
            ],
            expand=True,
        ),
    )

    layout = ft.Row([sidebar, main_content], expand=True)

    appbar = ft.AppBar(
        title=ft.Text("Corallie Bubble - Punto de Venta"),
        bgcolor="#C86DD7",
        color="white",
    )

    return ft.View(route="/movimientos", controls=[layout], appbar=appbar)
