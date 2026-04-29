import flet as ft
from connector import get_connection
from sidebar_admin import build_admin_sidebar

# Compatibilidad íconos
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons


def admin_usuarios_view(page: ft.Page, nombre_admin: str = "Administrador") -> ft.View:
    # ------------------------------------------------------------
    # Helpers UI
    # ------------------------------------------------------------
    def open_dialog(dlg: ft.AlertDialog):
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

    def close_dialog(dlg: ft.AlertDialog):
        try:
            dlg.open = False
            page.update()
        except Exception:
            pass

    def show_snack(texto: str, ok: bool = True):
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

    def ir_inicio(e=None):
        if len(page.views) > 1:
            page.views.pop()
        page.go("/admin")
        page.update()

    def ir_control_empleados(e=None):
        from admin_empleados import admin_empleados_view
        page.views.append(admin_empleados_view(page, nombre_admin))
        page.go("/admin_empleados")
        page.update()

    def ir_control_usuarios(e=None):
        pass

    def ir_reportes(e=None):
        from generar_reportes import generar_reportes_view
        page.views.append(generar_reportes_view(page, nombre_admin))
        page.go("/reportes")
        page.update()

    # ------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------
    def volver_admin(e=None):
        if len(page.views) > 1:
            page.views.pop()
        page.go("/admin")
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
    def db_listar_clientes():
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    c.IdCliente,
                    c.Nombre,
                    c.Apellido,
                    c.Telefono,
                    c.Correo,
                    c.Usuario_IdUsuario,
                    u.NombreUsuario
                FROM cliente c
                LEFT JOIN usuario u ON u.IdUsuario = c.Usuario_IdUsuario
                ORDER BY c.IdCliente DESC
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

    def db_existe_usuario(nombre_usuario: str, exclude_id_usuario=None) -> bool:
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            if exclude_id_usuario is None:
                cur.execute(
                    "SELECT COUNT(*) FROM usuario WHERE NombreUsuario=%s",
                    (nombre_usuario,),
                )
            else:
                cur.execute(
                    "SELECT COUNT(*) FROM usuario WHERE NombreUsuario=%s AND IdUsuario<>%s",
                    (nombre_usuario, int(exclude_id_usuario)),
                )
            row = cur.fetchone()
            return (row[0] or 0) > 0
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except Exception:
                pass

    def db_crear_cliente(nombre, apellido, telefono, correo, usuario, password):
        conn = None
        cur = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO usuario (NombreUsuario, Contraseña) VALUES (%s, %s)",
                (usuario, password),
            )
            id_usuario = cur.lastrowid

            cur.execute(
                """
                INSERT INTO cliente (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (nombre, apellido, telefono, correo, id_usuario),
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

    def db_editar_cliente(id_cliente, nombre, apellido, telefono, correo, nombre_usuario, password=None):
        conn = None
        cur = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cur = conn.cursor(dictionary=True)

            cur.execute(
                "SELECT Usuario_IdUsuario FROM cliente WHERE IdCliente=%s",
                (int(id_cliente),),
            )
            row = cur.fetchone()
            if not row:
                raise Exception("Cliente no encontrado")

            id_usuario = int(row["Usuario_IdUsuario"])

            if password:
                cur.execute(
                    """
                    UPDATE usuario
                    SET NombreUsuario=%s, Contraseña=%s
                    WHERE IdUsuario=%s
                    """,
                    (nombre_usuario, password, id_usuario),
                )
            else:
                cur.execute(
                    """
                    UPDATE usuario
                    SET NombreUsuario=%s
                    WHERE IdUsuario=%s
                    """,
                    (nombre_usuario, id_usuario),
                )

            cur.execute(
                """
                UPDATE cliente
                SET Nombre=%s, Apellido=%s, Telefono=%s, Correo=%s
                WHERE IdCliente=%s
                """,
                (nombre, apellido, telefono, correo, int(id_cliente)),
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

    def db_eliminar_cliente(id_cliente):
        conn = None
        cur = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            cur.execute(
                "SELECT Usuario_IdUsuario FROM cliente WHERE IdCliente=%s",
                (int(id_cliente),),
            )
            row = cur.fetchone()
            if not row:
                conn.rollback()
                return

            id_usuario = int(row[0])

            cur.execute("DELETE FROM cliente WHERE IdCliente=%s", (int(id_cliente),))
            cur.execute("DELETE FROM usuario WHERE IdUsuario=%s", (id_usuario,))

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
    # UI
    # ------------------------------------------------------------
    txt_buscar = ft.TextField(label="Buscar usuario/cliente", border_radius=12, width=320)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Cliente")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        border_radius=12,
        heading_row_color="#F3E9F7",
        data_row_min_height=52,
        data_row_max_height=90,
        column_spacing=18,
    )

    cache = []

    def validar_texto(valor: str):
        return (valor or "").strip()

    def recargar():
        nonlocal cache
        try:
            cache = db_listar_clientes()
        except Exception as ex:
            cache = []
            show_snack(f"Error al cargar clientes: {ex}", ok=False)
        aplicar_filtro()

    def aplicar_filtro(e=None):
        q = (txt_buscar.value or "").strip().lower()
        lista = cache

        if q:
            lista = [
                x for x in lista
                if q in str(x.get("IdCliente", "")).lower()
                or q in str(x.get("Nombre", "")).lower()
                or q in str(x.get("Apellido", "")).lower()
                or q in str(x.get("Telefono", "")).lower()
                or q in str(x.get("Correo", "")).lower()
                or q in str(x.get("NombreUsuario", "")).lower()
            ]

        pintar_tabla(lista)

    txt_buscar.on_change = aplicar_filtro

    def pintar_tabla(lista):
        tabla.rows = []

        for cli in lista:
            cli_id = int(cli["IdCliente"])

            def editar_click(e, cliente=cli):
                abrir_dialogo_editar(cliente)

            def eliminar_click(e, id_cli=cli_id):
                confirmar_eliminar(id_cli)

            acciones = ft.Row(
                [
                    ft.TextButton("Editar", on_click=editar_click),
                    ft.TextButton("Eliminar", on_click=eliminar_click),
                ],
                spacing=4,
            )

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(cli.get("IdCliente", "")))),
                        ft.DataCell(ft.Text(str(cli.get("Nombre", "")))),
                        ft.DataCell(ft.Text(str(cli.get("Apellido", "")))),
                        ft.DataCell(ft.Text(str(cli.get("Telefono", "")))),
                        ft.DataCell(ft.Text(str(cli.get("Correo", "")))),
                        ft.DataCell(ft.Text(str(cli.get("NombreUsuario", "")))),
                        ft.DataCell(acciones),
                    ]
                )
            )

        page.update()

    def abrir_dialogo_nuevo(e=None):
        txt_nombre = ft.TextField(label="Nombre", border_radius=12)
        txt_apellido = ft.TextField(label="Apellido", border_radius=12)
        txt_telefono = ft.TextField(label="Teléfono", border_radius=12, keyboard_type=ft.KeyboardType.NUMBER)
        txt_correo = ft.TextField(label="Correo", border_radius=12)
        txt_usuario = ft.TextField(label="Nombre de usuario", border_radius=12)
        txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_radius=12)

        dlg = ft.AlertDialog(title=ft.Text("Nuevo cliente"))

        def guardar(ev):
            nombre = validar_texto(txt_nombre.value)
            apellido = validar_texto(txt_apellido.value)
            telefono = validar_texto(txt_telefono.value)
            correo = validar_texto(txt_correo.value)
            usuario = validar_texto(txt_usuario.value)
            password = validar_texto(txt_pass.value)

            for f in [txt_nombre, txt_apellido, txt_telefono, txt_correo, txt_usuario, txt_pass]:
                f.error_text = None

            ok = True

            if not nombre:
                txt_nombre.error_text = "Requerido"
                ok = False
            if not apellido:
                txt_apellido.error_text = "Requerido"
                ok = False
            if not telefono or not telefono.isdigit():
                txt_telefono.error_text = "Solo números"
                ok = False
            if not correo or "@" not in correo or "." not in correo:
                txt_correo.error_text = "Correo inválido"
                ok = False
            if not usuario:
                txt_usuario.error_text = "Requerido"
                ok = False
            elif db_existe_usuario(usuario):
                txt_usuario.error_text = "Ese usuario ya existe"
                ok = False
            if not password or len(password) < 4:
                txt_pass.error_text = "Mínimo 4 caracteres"
                ok = False

            page.update()

            if not ok:
                return

            try:
                db_crear_cliente(nombre, apellido, telefono, correo, usuario, password)
                close_dialog(dlg)
                recargar()
                show_snack("Cliente registrado correctamente")
            except Exception as ex:
                show_snack(f"No se pudo registrar: {ex}", ok=False)

        dlg.content = ft.Container(
            width=500,
            content=ft.Column(
                [
                    txt_nombre,
                    txt_apellido,
                    txt_telefono,
                    txt_correo,
                    ft.Divider(),
                    txt_usuario,
                    txt_pass,
                ],
                tight=True,
            ),
        )
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda ev: close_dialog(dlg)),
            ft.ElevatedButton("Guardar", bgcolor="#C86DD7", color="white", on_click=guardar),
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    def abrir_dialogo_editar(cliente: dict):
        txt_nombre = ft.TextField(label="Nombre", border_radius=12, value=str(cliente.get("Nombre", "")))
        txt_apellido = ft.TextField(label="Apellido", border_radius=12, value=str(cliente.get("Apellido", "")))
        txt_telefono = ft.TextField(
            label="Teléfono",
            border_radius=12,
            value=str(cliente.get("Telefono", "")),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        txt_correo = ft.TextField(label="Correo", border_radius=12, value=str(cliente.get("Correo", "")))
        txt_usuario = ft.TextField(label="Nombre de usuario", border_radius=12, value=str(cliente.get("NombreUsuario", "")))
        txt_pass = ft.TextField(
            label="Nueva contraseña (opcional)",
            password=True,
            can_reveal_password=True,
            border_radius=12,
        )

        dlg = ft.AlertDialog(title=ft.Text(f"Editar cliente #{cliente.get('IdCliente')}"))

        def guardar(ev):
            nombre = validar_texto(txt_nombre.value)
            apellido = validar_texto(txt_apellido.value)
            telefono = validar_texto(txt_telefono.value)
            correo = validar_texto(txt_correo.value)
            usuario = validar_texto(txt_usuario.value)
            password = validar_texto(txt_pass.value)

            for f in [txt_nombre, txt_apellido, txt_telefono, txt_correo, txt_usuario, txt_pass]:
                f.error_text = None

            ok = True

            if not nombre:
                txt_nombre.error_text = "Requerido"
                ok = False
            if not apellido:
                txt_apellido.error_text = "Requerido"
                ok = False
            if not telefono or not telefono.isdigit():
                txt_telefono.error_text = "Solo números"
                ok = False
            if not correo or "@" not in correo or "." not in correo:
                txt_correo.error_text = "Correo inválido"
                ok = False

            usuario_id = cliente.get("Usuario_IdUsuario")
            if not usuario:
                txt_usuario.error_text = "Requerido"
                ok = False
            elif db_existe_usuario(usuario, exclude_id_usuario=usuario_id):
                txt_usuario.error_text = "Ese usuario ya existe"
                ok = False

            if password and len(password) < 4:
                txt_pass.error_text = "Mínimo 4 caracteres"
                ok = False

            page.update()

            if not ok:
                return

            try:
                db_editar_cliente(
                    id_cliente=cliente["IdCliente"],
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    correo=correo,
                    nombre_usuario=usuario,
                    password=password if password else None,
                )
                close_dialog(dlg)
                recargar()
                show_snack("Cliente actualizado correctamente")
            except Exception as ex:
                show_snack(f"No se pudo actualizar: {ex}", ok=False)

        dlg.content = ft.Container(
            width=500,
            content=ft.Column(
                [
                    txt_nombre,
                    txt_apellido,
                    txt_telefono,
                    txt_correo,
                    ft.Divider(),
                    txt_usuario,
                    txt_pass,
                ],
                tight=True,
            ),
        )
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda ev: close_dialog(dlg)),
            ft.ElevatedButton("Guardar cambios", bgcolor="#C86DD7", color="white", on_click=guardar),
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    def confirmar_eliminar(id_cliente: int):
        dlg = ft.AlertDialog(title=ft.Text("Eliminar cliente"))

        def eliminar(ev):
            try:
                db_eliminar_cliente(id_cliente)
                close_dialog(dlg)
                recargar()
                show_snack("Cliente eliminado correctamente")
            except Exception as ex:
                show_snack(f"No se pudo eliminar: {ex}", ok=False)

        dlg.content = ft.Text("¿Deseas eliminar este cliente y su usuario?")
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda ev: close_dialog(dlg)),
            ft.ElevatedButton("Eliminar", bgcolor="#C62828", color="white", on_click=eliminar),
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    recargar()

    header = ft.Row(
        [
            ft.Text("Control de usuarios (Clientes)", size=22, weight="bold", color="#C86DD7"),
            ft.Container(expand=True),
            txt_buscar,
            ft.ElevatedButton(
                "+ Nuevo cliente",
                bgcolor="#C86DD7",
                color="white",
                on_click=abrir_dialogo_nuevo,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), padding=18),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    content = ft.Container(
        expand=True,
        bgcolor="#F9F6FB",
        padding=20,
        content=ft.Column(
            [
                header,
                ft.Container(height=10),
                ft.Container(
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
                ),
                ft.Row(
                    [
                        ft.Text(f"Admin: {nombre_admin}", size=12, color="#888888"),
                        ft.Container(expand=True),
                        ft.TextButton("Volver", on_click=volver_admin),
                        ft.TextButton("Cerrar sesión", on_click=cerrar_sesion),
                    ]
                )
            ],
            expand=True,
        ),
    )

    appbar = ft.AppBar(
        title=ft.Text("Corallie Bubble - Admin"),
        bgcolor="#C86DD7",
        color="white",
    )

    sidebar = build_admin_sidebar(
        page=page,
        nombre=nombre_admin,
        ir_inicio=ir_inicio,
        ir_control_empleados=ir_control_empleados,
        ir_control_usuarios=ir_control_usuarios,
        ir_reportes=ir_reportes,
        cerrar_sesion_real=cerrar_sesion,
    )

    layout = ft.Row(
        [
            sidebar,
            content,
        ],
        expand=True,
    )

    return ft.View(route="/admin_usuarios", controls=[layout], appbar=appbar)