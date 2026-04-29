import flet as ft
from datetime import datetime

from connector import get_connection
from sidebar import build_sidebar

# ------------------------------------------------------------
# Compatibilidad Flet 0.80 / 0.81+
# ------------------------------------------------------------
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons


# ------------------------------------------------------------
# Helpers UI
# ------------------------------------------------------------
def _open_dialog(page: ft.Page, dlg: ft.AlertDialog):
    try:
        if hasattr(page, "open"):
            page.open(dlg)
        else:
            page.dialog = dlg
            dlg.open = True
            page.update()
    except Exception:
        page.dialog = dlg
        dlg.open = True
        page.update()


def _show_snack(page: ft.Page, texto: str, ok: bool = True):
    sb = ft.SnackBar(
        content=ft.Text(texto, color="white"),
        bgcolor="#2E7D32" if ok else "#C62828",
    )
    try:
        if hasattr(page, "open"):
            page.open(sb)
        else:
            page.snack_bar = sb
            sb.open = True
            page.update()
    except Exception:
        page.snack_bar = sb
        sb.open = True
        page.update()


def caja_chica_view(page: ft.Page, nombre: str = "", rol: str = "") -> ft.View:
    # ------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------
    def ir_inicio(e=None):
        if len(page.views) > 1:
            page.views.pop()
        page.go("/pos")
        page.update()

    def ir_inventario(e):
        from inventario import inventario_view
        page.views.append(inventario_view(page, nombre))
        page.go("/inventario")
        page.update()

    def ir_movimientos(e):
        from movimientos import movimientos_view
        page.views.append(movimientos_view(page, nombre))
        page.go("/movimientos")
        page.update()

    def ir_caja_chica(e=None):
        page.go("/caja_chica")
        page.update()

    def cerrar_sesion(e=None):
        from login import LoginView
        page.views.clear()
        page.views.append(LoginView(page))
        page.go("/")
        page.update()

    # ------------------------------------------------------------
    # Base de datos
    # ------------------------------------------------------------
    def db_resumen():
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    COALESCE(SUM(CASE WHEN LOWER(TipoMovimiento)='ingreso' THEN Monto ELSE 0 END), 0) AS ingresos,
                    COALESCE(SUM(CASE WHEN LOWER(TipoMovimiento)='egreso'  THEN Monto ELSE 0 END), 0) AS egresos,
                    COUNT(*) AS movimientos
                FROM ingresos_egresos
                """
            )
            row = cur.fetchone() or {}
            ingresos = float(row.get("ingresos") or 0)
            egresos = float(row.get("egresos") or 0)
            movimientos = int(row.get("movimientos") or 0)
            balance = ingresos - egresos
            return ingresos, egresos, balance, movimientos
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except Exception:
                pass

    def db_listar_movimientos(limit: int = 100):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                f"""
                SELECT
                    idMovimiento,
                    TipoMovimiento,
                    Monto,
                    Descripcion,
                    Fecha,
                    Hora
                FROM ingresos_egresos
                ORDER BY Fecha DESC, Hora DESC, idMovimiento DESC
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
            except Exception:
                pass

    def db_insertar_movimiento(tipo: str, monto: float, descripcion: str):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            ahora = datetime.now()
            cur.execute(
                """
                INSERT INTO ingresos_egresos (TipoMovimiento, Monto, Descripcion, Fecha, Hora)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (tipo, float(monto), descripcion, ahora.date(), ahora.strftime("%H:%M:%S")),
            )
            conn.commit()
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except Exception:
                pass

    # ------------------------------------------------------------
    # Controles
    # ------------------------------------------------------------
    dd_tipo = ft.Dropdown(
        label="Tipo de movimiento",
        options=[ft.dropdown.Option("Ingreso"), ft.dropdown.Option("Egreso")],
        value="Ingreso",
        border_radius=12,
        width=220,
    )

    txt_monto = ft.TextField(
        label="Monto",
        border_radius=12,
        width=220,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    txt_desc = ft.TextField(
        label="Descripción",
        border_radius=12,
        width=460,
        multiline=True,
        min_lines=2,
        max_lines=3,
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Monto")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Hora")),
        ],
        rows=[],
        border_radius=12,
        heading_row_color="#F3E9F7",
        data_row_min_height=52,
        data_row_max_height=88,
        column_spacing=22,
    )

    card_ingresos = ft.Container()
    card_egresos = ft.Container()
    card_balance = ft.Container()
    lbl_estado = ft.Text("", size=12, color="#6B7280")

    def money(v):
        try:
            return f"$ {float(v):,.2f}"
        except Exception:
            return "$ 0.00"

    def crear_kpi(titulo: str, valor: str):
        return ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=16,
            col={"xs": 12, "sm": 6, "md": 4},
            content=ft.Column(
                [
                    ft.Text(titulo, size=13, color="#666666"),
                    ft.Text(valor, size=22, weight="bold", color="#C86DD7"),
                ],
                spacing=6,
            ),
        )

    def recargar_resumen():
        ingresos, egresos, balance, movimientos = db_resumen()
        card_ingresos.content = crear_kpi("Ingresos", money(ingresos)).content
        card_egresos.content = crear_kpi("Egresos", money(egresos)).content
        card_balance.content = crear_kpi("Balance", money(balance)).content
        lbl_estado.value = f"Movimientos registrados: {movimientos}"

    def recargar_tabla():
        rows = db_listar_movimientos(limit=150)
        tabla.rows = []
        for r in rows:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.get("idMovimiento", "")))),
                        ft.DataCell(ft.Text(str(r.get("TipoMovimiento", "")))),
                        ft.DataCell(ft.Text(money(r.get("Monto", 0)))),
                        ft.DataCell(ft.Text(str(r.get("Descripcion", "")), max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)),
                        ft.DataCell(ft.Text(str(r.get("Fecha", "")))),
                        ft.DataCell(ft.Text(str(r.get("Hora", "")))),
                    ]
                )
            )

    def validar_formulario():
        ok = True
        dd_tipo.error_text = None
        txt_monto.error_text = None
        txt_desc.error_text = None

        if not dd_tipo.value:
            dd_tipo.error_text = "Selecciona el tipo"
            ok = False

        monto_raw = (txt_monto.value or "").strip().replace(",", "")
        try:
            monto_value = float(monto_raw)
        except Exception:
            monto_value = -1

        if monto_value <= 0:
            txt_monto.error_text = "Ingresa un monto válido (> 0)"
            ok = False

        descripcion = (txt_desc.value or "").strip()
        if not descripcion:
            txt_desc.error_text = "Escribe una descripción"
            ok = False
        elif len(descripcion) > 500:
            txt_desc.error_text = "La descripción es demasiado larga"
            ok = False

        page.update()
        return ok, monto_value, descripcion

    def guardar_movimiento(e):
        ok, monto_value, descripcion = validar_formulario()
        if not ok:
            return
        try:
            db_insertar_movimiento(dd_tipo.value, monto_value, descripcion)
            txt_monto.value = ""
            txt_desc.value = ""
            recargar_resumen()
            recargar_tabla()
            page.update()
            _show_snack(page, "Movimiento registrado correctamente")
        except Exception as ex:
            _open_dialog(
                page,
                ft.AlertDialog(
                    title=ft.Text("No se pudo registrar"),
                    content=ft.Text(str(ex)),
                ),
            )

    # ------------------------------------------------------------
    # Sidebar reutilizable
    # ------------------------------------------------------------
    sidebar = build_sidebar(
        page=page,
        nombre=nombre or "Empleado",
        ir_inicio=ir_inicio,
        ir_inventario=ir_inventario,
        ir_movimientos=ir_movimientos,
        ir_caja_chica=ir_caja_chica,
        cerrar_sesion_real=cerrar_sesion,
    )

    # ------------------------------------------------------------
    # Layout principal
    # ------------------------------------------------------------
    header = ft.Row(
        [
            ft.Text("Caja chica", size=22, weight="bold", color="#C86DD7"),
            ft.Container(expand=True),
        ]
    )

    resumen_row = ft.ResponsiveRow(
        [
            card_ingresos,
            card_egresos,
            card_balance,
        ],
        spacing=16,
        run_spacing=16,
    )

    formulario = ft.Container(
        bgcolor="white",
        border_radius=18,
        padding=16,
        content=ft.Column(
            [
                ft.Text("Registrar movimiento", size=16, weight="bold"),
                ft.Row([dd_tipo, txt_monto], spacing=12),
                txt_desc,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Guardar",
                            bgcolor="#C86DD7",
                            color="white",
                            on_click=guardar_movimiento,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=20),
                                padding=18,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=12,
        ),
    )

    tabla_wrap = ft.Container(
        expand=True,
        bgcolor="white",
        border_radius=18,
        padding=12,
        content=ft.ListView(
            expand=True,
            controls=[
                ft.Row(
                    [ft.Container(content=tabla, padding=6)],
                    scroll=ft.ScrollMode.AUTO,
                )
            ],
        ),
    )

    main_content = ft.Container(
        expand=True,
        bgcolor="#F9F6FB",
        padding=20,
        content=ft.Column(
            [
                header,
                lbl_estado,
                resumen_row,
                formulario,
                tabla_wrap,
            ],
            spacing=16,
            expand=True,
        ),
    )

    recargar_resumen()
    recargar_tabla()

    layout = ft.Row([sidebar, main_content], expand=True)

    appbar = ft.AppBar(
        title=ft.Text("Caja chica"),
        bgcolor="#C86DD7",
        color="white",
    )

    return ft.View(route="/caja_chica", controls=[layout], appbar=appbar)