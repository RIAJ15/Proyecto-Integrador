import flet as ft

# Compatibilidad íconos (Flet nuevo)
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons

from connector import get_connection

# -------------------------------------------------------------------
# CONTROL DE USUARIOS (ADMIN)
# - Gestiona tabla usuario + datos en empleado/cliente ligados por Usuario_IdUsuario
# -------------------------------------------------------------------
def control_usuario_view(page: ft.Page, nombre_admin: str = "Administrador") -> ft.View:
    # -----------------------------
    # Helpers UI compatibles
    # -----------------------------
    def open_dialog(dlg: ft.AlertDialog):
        if hasattr(page, "open"):
            page.open(dlg)
        else:
            page.dialog = dlg
            dlg.open = True
            page.update()

    def close_dialog(dlg: ft.AlertDialog):
        try:
            if hasattr(page, "close"):
                page.close(dlg)
            else:
                dlg.open = False
                page.update()
        except:
            dlg.open = False
            page.update()

    def show_snack(texto: str):
        sb = ft.SnackBar(content=ft.Text(texto))
        if hasattr(page, "open"):
            page.open(sb)
        else:
            page.snack_bar = sb
            sb.open = True
            page.update()

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

    # -----------------------------
    # Sidebar (mismo estilo)
    # -----------------------------
    def crear_boton_sidebar(texto: str, on_click):
        btn = ft.Container(
            padding=ft.padding.symmetric(vertical=10, horizontal=16),
            border_radius=20,
            content=ft.Text(texto, color="white", size=14, weight="w600"),
            ink=True,
            on_click=on_click,
        )

        def on_hover(ev):
            btn.bgcolor = "rgba(255,255,255,0.18)" if ev.data == "true" else None
            btn.update()

        btn.on_hover = on_hover
        return btn

    sidebar = ft.Container(
        width=220,
        bgcolor="#C86DD7",
        padding=20,
        content=ft.Column(
            [
                ft.Text("Corallie Bubble", size=20, weight="bold", color="white"),
                ft.Text("Administrador", size=12, color="white70"),
                ft.Container(height=20),
                crear_boton_sidebar("Inicio", volver_pos),
                crear_boton_sidebar("Control de usuarios", lambda e: None),
                ft.Container(expand=True),
                crear_boton_sidebar("Cerrar sesión", cerrar_sesion),
            ],
            spacing=6,
        ),
    )

    # -----------------------------
    # BD
    # -----------------------------
    def db_listar_usuarios():
        """
        Devuelve usuarios con datos ligados de empleado/cliente.
        Si existe en ambos (raro), prioriza empleado.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    u.IdUsuario,
                    u.NombreUsuario,

                    e.Nombre   AS EmpNombre,
                    e.Apellido AS EmpApellido,
                    e.Telefono AS EmpTelefono,
                    e.Correo   AS EmpCorreo,

                    c.Nombre   AS CliNombre,
                    c.Apellido AS CliApellido,
                    c.Telefono AS CliTelefono,
                    c.Correo   AS CliCorreo
                FROM usuario u
                LEFT JOIN empleado e ON e.Usuario_IdUsuario = u.IdUsuario
                LEFT JOIN cliente  c ON c.Usuario_IdUsuario = u.IdUsuario
                ORDER BY u.IdUsuario DESC
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

    def db_usuario_existe(nombre_usuario: str, exclude_id: int | None = None) -> bool:
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            if exclude_id is None:
                cur.execute("SELECT COUNT(*) FROM usuario WHERE NombreUsuario=%s", (nombre_usuario,))
            else:
                cur.execute("SELECT COUNT(*) FROM usuario WHERE NombreUsuario=%s AND IdUsuario<>%s", (nombre_usuario, exclude_id))
            return (cur.fetchone()[0] or 0) > 0
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except:
                pass

    def db_crear_usuario_con_perfil(tipo: str, nombre_usuario: str, password: str, nombre: str, apellido: str, tel: str, correo: str):
        """
        tipo: 'Empleado' o 'Cliente'
        Inserta en usuario y luego en la tabla correspondiente.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO usuario (NombreUsuario, Contraseña) VALUES (%s, %s)",
                (nombre_usuario, password),
            )
            id_usuario = cur.lastrowid

            tabla = "empleado" if tipo == "Empleado" else "cliente"
            cur.execute(
                f"""
                INSERT INTO {tabla} (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (nombre, apellido, tel, correo, id_usuario),
            )

            conn.commit()
            return int(id_usuario)
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

    def db_editar_usuario_y_perfil(id_usuario: int, nombre_usuario: str, password: str | None,
                                  tipo: str, nombre: str, apellido: str, tel: str, correo: str):
        """
        Actualiza:
        - usuario.NombreUsuario
        - usuario.Contraseña si password no es None y no viene vacío
        - perfil en tabla empleado/cliente (si no existe, lo crea)
        - si cambia tipo, mueve el perfil (elimina de la otra tabla y crea en la seleccionada)
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cur = conn.cursor()

            # 1) actualizar usuario
            if password:
                cur.execute(
                    "UPDATE usuario SET NombreUsuario=%s, Contraseña=%s WHERE IdUsuario=%s",
                    (nombre_usuario, password, id_usuario),
                )
            else:
                cur.execute(
                    "UPDATE usuario SET NombreUsuario=%s WHERE IdUsuario=%s",
                    (nombre_usuario, id_usuario),
                )

            # 2) detectar si existe en empleado/cliente
            cur.execute("SELECT COUNT(*) FROM empleado WHERE Usuario_IdUsuario=%s", (id_usuario,))
            es_emp = (cur.fetchone()[0] or 0) > 0

            cur.execute("SELECT COUNT(*) FROM cliente WHERE Usuario_IdUsuario=%s", (id_usuario,))
            es_cli = (cur.fetchone()[0] or 0) > 0

            # 3) si cambia tipo, quitar de la otra
            if tipo == "Empleado" and es_cli:
                cur.execute("DELETE FROM cliente WHERE Usuario_IdUsuario=%s", (id_usuario,))
                es_cli = False
            if tipo == "Cliente" and es_emp:
                cur.execute("DELETE FROM empleado WHERE Usuario_IdUsuario=%s", (id_usuario,))
                es_emp = False

            # 4) upsert del perfil
            if tipo == "Empleado":
                if es_emp:
                    cur.execute(
                        """
                        UPDATE empleado
                        SET Nombre=%s, Apellido=%s, Telefono=%s, Correo=%s
                        WHERE Usuario_IdUsuario=%s
                        """,
                        (nombre, apellido, tel, correo, id_usuario),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO empleado (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (nombre, apellido, tel, correo, id_usuario),
                    )
            else:
                if es_cli:
                    cur.execute(
                        """
                        UPDATE cliente
                        SET Nombre=%s, Apellido=%s, Telefono=%s, Correo=%s
                        WHERE Usuario_IdUsuario=%s
                        """,
                        (nombre, apellido, tel, correo, id_usuario),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO cliente (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (nombre, apellido, tel, correo, id_usuario),
                    )

            conn.commit()
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

    def db_eliminar_usuario(id_usuario: int):
        """
        Elimina primero perfiles, luego usuario.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            conn.start_transaction()
            cur = conn.cursor()
            cur.execute("DELETE FROM empleado WHERE Usuario_IdUsuario=%s", (id_usuario,))
            cur.execute("DELETE FROM cliente  WHERE Usuario_IdUsuario=%s", (id_usuario,))
            cur.execute("DELETE FROM usuario  WHERE IdUsuario=%s", (id_usuario,))
            conn.commit()
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
    # UI Estado / filtros
    # -----------------------------
    txt_buscar = ft.TextField(label="Buscar (usuario, nombre, correo)", border_radius=12, width=340)
    dd_tipo_filtro = ft.Dropdown(
        label="Filtrar por tipo",
        options=[ft.dropdown.Option("Todos"), ft.dropdown.Option("Empleado"), ft.dropdown.Option("Cliente")],
        value="Todos",
        border_radius=12,
        width=220,
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        border_radius=12,
        heading_row_color="#F3E9F7",
        data_row_min_height=52,
        data_row_max_height=90,
    )
    lbl_error = ft.Text("", color=ft.Colors.RED, size=12)
    lbl_empty = ft.Text("No hay usuarios para mostrar.", color="#777777", visible=False)

    cache = []

    def map_row(r: dict):
        # Determinar tipo y datos
        if r.get("EmpNombre") or r.get("EmpCorreo") or r.get("EmpTelefono"):
            tipo = "Empleado"
            nombre = f'{r.get("EmpNombre","")} {r.get("EmpApellido","")}'.strip()
            correo = r.get("EmpCorreo") or ""
            tel = r.get("EmpTelefono") or ""
        elif r.get("CliNombre") or r.get("CliCorreo") or r.get("CliTelefono"):
            tipo = "Cliente"
            nombre = f'{r.get("CliNombre","")} {r.get("CliApellido","")}'.strip()
            correo = r.get("CliCorreo") or ""
            tel = r.get("CliTelefono") or ""
        else:
            tipo = "Sin perfil"
            nombre = "—"
            correo = "—"
            tel = "—"

        return {
            "IdUsuario": int(r["IdUsuario"]),
            "Tipo": tipo,
            "NombreUsuario": str(r.get("NombreUsuario") or ""),
            "Nombre": nombre,
            "Correo": str(correo),
            "Telefono": str(tel),
            "raw": r,
        }

    def recargar():
        nonlocal cache
        lbl_error.value = ""
        try:
            rows = db_listar_usuarios()
            cache = [map_row(r) for r in rows]
        except Exception as ex:
            cache = []
            lbl_error.value = f"Error al cargar usuarios: {ex}"
        aplicar_filtro()

    def aplicar_filtro(e=None):
        q = (txt_buscar.value or "").strip().lower()
        t = dd_tipo_filtro.value or "Todos"

        lista = cache

        if t != "Todos":
            lista = [x for x in lista if x["Tipo"] == t]

        if q:
            def in_any(x):
                return (
                    q in x["NombreUsuario"].lower()
                    or q in (x["Nombre"] or "").lower()
                    or q in (x["Correo"] or "").lower()
                    or q in (x["Telefono"] or "").lower()
                    or q in str(x["IdUsuario"])
                )
            lista = [x for x in lista if in_any(x)]

        pintar_tabla(lista)

    txt_buscar.on_change = aplicar_filtro
    dd_tipo_filtro.on_change = aplicar_filtro

    def pintar_tabla(lista):
        lbl_empty.visible = (len(lista) == 0)
        tabla.rows = []

        def link(texto, callback):
            return ft.GestureDetector(
                content=ft.Text(texto, color=ft.Colors.BLUE, weight="w600"),
                on_tap=callback,
                mouse_cursor=ft.MouseCursor.CLICK,
            )

        def cell(ctrl, w=None):
            return ft.Container(
                width=w,
                padding=ft.padding.symmetric(horizontal=8, vertical=8),
                border_radius=10,
                content=ctrl,
            )

        for u in lista:
            uid = u["IdUsuario"]

            def _editar(e, user=u):
                abrir_dialogo_editar(user)

            def _eliminar(e, user_id=uid):
                confirmar_eliminar(user_id)

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(cell(ft.Text(str(uid)), w=70)),
                        ft.DataCell(cell(ft.Text(u["Tipo"]), w=110)),
                        ft.DataCell(cell(ft.Text(u["NombreUsuario"]), w=160)),
                        ft.DataCell(cell(ft.Text(u["Nombre"]), w=200)),
                        ft.DataCell(cell(ft.Text(u["Correo"]), w=230)),
                        ft.DataCell(cell(ft.Text(u["Telefono"]), w=140)),
                        ft.DataCell(
                            cell(
                                ft.Row(
                                    [
                                        link("Editar", _editar),
                                        link("Eliminar", _eliminar),
                                    ],
                                    spacing=18,
                                ),
                                w=150,
                            )
                        ),
                    ]
                )
            )

        page.update()

    # -----------------------------
    # Diálogos CRUD
    # -----------------------------
    def validar_basico(txt):
        return (txt or "").strip()

    def abrir_dialogo_nuevo(e=None):
        dd_tipo = ft.Dropdown(
            label="Tipo",
            options=[ft.dropdown.Option("Empleado"), ft.dropdown.Option("Cliente")],
            value="Cliente",
            border_radius=12,
        )
        u_user = ft.TextField(label="Nombre de usuario", border_radius=12)
        u_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, border_radius=12)

        u_nombre = ft.TextField(label="Nombre", border_radius=12)
        u_apellido = ft.TextField(label="Apellido", border_radius=12)
        u_tel = ft.TextField(label="Teléfono", border_radius=12, keyboard_type=ft.KeyboardType.NUMBER)
        u_correo = ft.TextField(label="Correo", border_radius=12)

        dlg = ft.AlertDialog(title=ft.Text("Nuevo usuario"))

        def validar():
            ok = True
            for f in [u_user, u_pass, u_nombre, u_apellido, u_tel, u_correo]:
                f.error_text = None

            user = validar_basico(u_user.value)
            pwd = validar_basico(u_pass.value)
            nom = validar_basico(u_nombre.value)
            ape = validar_basico(u_apellido.value)
            tel = validar_basico(u_tel.value)
            cor = validar_basico(u_correo.value)

            if not user:
                u_user.error_text = "Requerido"
                ok = False
            else:
                if db_usuario_existe(user):
                    u_user.error_text = "Ese usuario ya existe"
                    ok = False

            if not pwd or len(pwd) < 4:
                u_pass.error_text = "Contraseña mínima 4 caracteres"
                ok = False

            if not nom:
                u_nombre.error_text = "Requerido"
                ok = False
            if not ape:
                u_apellido.error_text = "Requerido"
                ok = False
            if not tel or not tel.isdigit():
                u_tel.error_text = "Teléfono inválido (solo números)"
                ok = False
            if not cor or ("@" not in cor or "." not in cor):
                u_correo.error_text = "Correo no válido"
                ok = False

            page.update()
            return ok, dd_tipo.value, user, pwd, nom, ape, tel, cor

        def guardar(ev):
            ok, tipo, user, pwd, nom, ape, tel, cor = validar()
            if not ok:
                return
            try:
                new_id = db_crear_usuario_con_perfil(tipo, user, pwd, nom, ape, tel, cor)
                close_dialog(dlg)
                recargar()
                show_snack(f"Usuario creado (ID {new_id}) ✅")
            except Exception as ex:
                show_snack(f"No se pudo crear: {ex}")

        dlg.content = ft.Column(
            [
                dd_tipo,
                u_user, u_pass,
                ft.Divider(),
                u_nombre, u_apellido, u_tel, u_correo,
            ],
            tight=True,
            width=520,
        )
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda ev: close_dialog(dlg)),
            ft.ElevatedButton("Guardar", bgcolor="#C86DD7", color="white", on_click=guardar),
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    def abrir_dialogo_editar(user: dict):
        raw = user.get("raw") or {}
        uid = int(user["IdUsuario"])

        # tipo actual estimado
        tipo_actual = "Cliente"
        if raw.get("EmpNombre") or raw.get("EmpCorreo") or raw.get("EmpTelefono"):
            tipo_actual = "Empleado"
        elif raw.get("CliNombre") or raw.get("CliCorreo") or raw.get("CliTelefono"):
            tipo_actual = "Cliente"

        dd_tipo = ft.Dropdown(
            label="Tipo",
            options=[ft.dropdown.Option("Empleado"), ft.dropdown.Option("Cliente")],
            value=tipo_actual if tipo_actual in ("Empleado", "Cliente") else "Cliente",
            border_radius=12,
        )

        u_user = ft.TextField(label="Nombre de usuario", border_radius=12, value=user.get("NombreUsuario", ""))
        u_pass = ft.TextField(
            label="Nueva contraseña (opcional)",
            password=True,
            can_reveal_password=True,
            border_radius=12,
            hint_text="Deja vacío para no cambiarla",
        )

        # valores actuales (según tipo)
        if tipo_actual == "Empleado":
            nom = raw.get("EmpNombre") or ""
            ape = raw.get("EmpApellido") or ""
            tel = raw.get("EmpTelefono") or ""
            cor = raw.get("EmpCorreo") or ""
        else:
            nom = raw.get("CliNombre") or ""
            ape = raw.get("CliApellido") or ""
            tel = raw.get("CliTelefono") or ""
            cor = raw.get("CliCorreo") or ""

        u_nombre = ft.TextField(label="Nombre", border_radius=12, value=str(nom))
        u_apellido = ft.TextField(label="Apellido", border_radius=12, value=str(ape))
        u_tel = ft.TextField(label="Teléfono", border_radius=12, value=str(tel), keyboard_type=ft.KeyboardType.NUMBER)
        u_correo = ft.TextField(label="Correo", border_radius=12, value=str(cor))

        dlg = ft.AlertDialog(title=ft.Text(f"Editar usuario #{uid}"))

        def validar():
            ok = True
            for f in [u_user, u_pass, u_nombre, u_apellido, u_tel, u_correo]:
                f.error_text = None

            usern = validar_basico(u_user.value)
            pwd = (u_pass.value or "").strip()  # opcional
            nomv = validar_basico(u_nombre.value)
            apev = validar_basico(u_apellido.value)
            telv = validar_basico(u_tel.value)
            corv = validar_basico(u_correo.value)

            if not usern:
                u_user.error_text = "Requerido"
                ok = False
            else:
                if db_usuario_existe(usern, exclude_id=uid):
                    u_user.error_text = "Ese usuario ya existe"
                    ok = False

            if pwd and len(pwd) < 4:
                u_pass.error_text = "Contraseña mínima 4 caracteres"
                ok = False

            if not nomv:
                u_nombre.error_text = "Requerido"
                ok = False
            if not apev:
                u_apellido.error_text = "Requerido"
                ok = False
            if not telv or not telv.isdigit():
                u_tel.error_text = "Teléfono inválido (solo números)"
                ok = False
            if not corv or ("@" not in corv or "." not in corv):
                u_correo.error_text = "Correo no válido"
                ok = False

            page.update()
            return ok, dd_tipo.value, usern, (pwd if pwd else None), nomv, apev, telv, corv

        def guardar(ev):
            ok, tipo, usern, pwd, nomv, apev, telv, corv = validar()
            if not ok:
                return
            try:
                db_editar_usuario_y_perfil(uid, usern, pwd, tipo, nomv, apev, telv, corv)
                close_dialog(dlg)
                recargar()
                show_snack("Usuario actualizado ✅")
            except Exception as ex:
                show_snack(f"No se pudo actualizar: {ex}")

        dlg.content = ft.Column(
            [
                dd_tipo,
                u_user,
                u_pass,
                ft.Divider(),
                u_nombre, u_apellido, u_tel, u_correo,
            ],
            tight=True,
            width=520,
        )
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda ev: close_dialog(dlg)),
            ft.ElevatedButton("Guardar cambios", bgcolor="#C86DD7", color="white", on_click=guardar),
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    def confirmar_eliminar(id_usuario: int):
        dlg = ft.AlertDialog(title=ft.Text("Eliminar usuario"))

        def eliminar(ev):
            try:
                db_eliminar_usuario(id_usuario)
                close_dialog(dlg)
                recargar()
                show_snack("Usuario eliminado 🗑️")
            except Exception as ex:
                show_snack(f"No se pudo eliminar: {ex}")

        dlg.content = ft.Text(f"¿Seguro que deseas eliminar el usuario ID {id_usuario}?\nEsto eliminará su perfil (empleado/cliente) también.")
        dlg.actions = [
            ft.TextButton("Cancelar", on_click=lambda ev: close_dialog(dlg)),
            ft.ElevatedButton("Eliminar", bgcolor="#E53935", color="white", on_click=eliminar),
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    # -----------------------------
    # Layout principal
    # -----------------------------
    header = ft.Row(
        [
            ft.Text("Control de usuarios", size=22, weight="bold", color="#C86DD7"),
            ft.Container(expand=True),
            dd_tipo_filtro,
            txt_buscar,
            ft.ElevatedButton(
                "+ Nuevo usuario",
                bgcolor="#C86DD7",
                color="white",
                on_click=abrir_dialogo_nuevo,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), padding=18),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
    )

    tabla_responsiva = ft.Row(
        controls=[ft.Container(padding=6, content=tabla)],
        scroll=ft.ScrollMode.AUTO,  # horizontal
    )

    main_content = ft.Container(
        expand=True,
        bgcolor="#F9F6FB",
        padding=20,
        content=ft.Column(
            [
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Regresar", on_click=volver_pos),
                        ft.Text(f"Admin: {nombre_admin}", size=12, color="#777777"),
                    ]
                ),
                header,
                lbl_error,
                lbl_empty,
                ft.Container(height=10),
                ft.Container(
                    expand=True,
                    bgcolor="white",
                    border_radius=18,
                    padding=12,
                    content=tabla_responsiva,  # directo, más estable en desktop
                ),
            ],
            expand=True,
        ),
    )

    layout = ft.Row([sidebar, main_content], expand=True)

    appbar = ft.AppBar(
        title=ft.Text("Corallie Bubble - Administrador"),
        bgcolor="#C86DD7",
        color="white",
    )

# Cuando main_content se monta en pantalla, cargamos datos
    def _on_mount(e):
        recargar()

    # main_content ya existe arriba, solo asigna el evento:
    main_content.on_mount = _on_mount

    view = ft.View(route="/control_usuarios", controls=[layout], appbar=appbar)
    return view