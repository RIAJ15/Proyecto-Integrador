import flet as ft

# ------------------------------------------------------------
# Compatibilidad Flet 0.80 / 0.81+
# ------------------------------------------------------------
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons


def _icon(*names):
    """Obtiene un icono compatible entre versiones de Flet."""
    for name in names:
        try:
            value = getattr(getattr(ft, "icons", None), name, None)
            if value is not None:
                return value
        except Exception:
            pass
        try:
            value = getattr(getattr(ft, "Icons", None), name, None)
            if value is not None:
                return value
        except Exception:
            pass
    return None


ICON_HOME = _icon("HOME", "HOME_OUTLINED")
ICON_EMPLOYEES = _icon("GROUP", "PEOPLE", "SUPERVISOR_ACCOUNT")
ICON_USERS = _icon("PERSON", "MANAGE_ACCOUNTS", "ACCOUNT_CIRCLE")
ICON_REPORT = _icon("ASSESSMENT", "ANALYTICS", "BAR_CHART")
ICON_LOGOUT = _icon("LOGOUT", "EXIT_TO_APP")


def build_admin_sidebar(
    page: ft.Page,
    nombre: str,
    ir_inicio,
    ir_control_empleados,
    ir_control_usuarios,
    cerrar_sesion_real,
    ir_reportes=None,
):
    """
    Sidebar para el módulo administrador.
    - Inicio
    - Control de empleados
    - Control de usuarios
    - Generar reportes (opcional)
    - Cerrar sesión
    """

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

    def nav_item(icono, texto, on_click):
        icon_control = ft.Icon(icono, color="white", size=20) if icono else ft.Container(width=20)

        item = ft.Container(
            border_radius=16,
            padding=ft.padding.symmetric(horizontal=14, vertical=12),
            ink=True,
            on_click=on_click,
            content=ft.Row(
                spacing=10,
                controls=[
                    icon_control,
                    ft.Text(texto, color="white", size=14, weight="bold"),
                ],
            ),
        )

        def on_hover(e):
            item.bgcolor = "rgba(255,255,255,0.18)" if e.data == "true" else None
            item.update()

        item.on_hover = on_hover
        return item

    def confirmar_cierre(e=None):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cerrar sesión"),
            content=ft.Text("¿Deseas salir del módulo administrador?"),
        )

        def cancelar(_e=None):
            dlg.open = False
            page.update()

        def salir(_e=None):
            dlg.open = False
            page.update()
            cerrar_sesion_real(None)

        dlg.actions = [
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.ElevatedButton(
                "Cerrar sesión",
                bgcolor="#C86DD7",
                color="white",
                on_click=salir,
            ),
        ]
        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    nav_controls = [
        nav_item(ICON_HOME, "Inicio", ir_inicio),
        nav_item(ICON_EMPLOYEES, "Control de empleados", ir_control_empleados),
        nav_item(ICON_USERS, "Control de usuarios", ir_control_usuarios),
    ]

    if ir_reportes is not None:
        nav_controls.append(nav_item(ICON_REPORT, "Generar reportes", ir_reportes))

    sidebar = ft.Container(
        width=250,
        bgcolor="#C86DD7",
        padding=20,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Container(height=12),
                ft.Text("Corallie Bubble", size=18, weight="bold", color="white"),
                ft.Text("Administrador", size=12, color="#F7E8FF"),
                ft.Container(height=10),
                ft.Text(f"Bienvenido, {nombre}", size=12, color="white70"),
                ft.Container(height=26),
                ft.Column(nav_controls, spacing=6),
                ft.Container(expand=True),
                nav_item(ICON_LOGOUT, "Cerrar sesión", confirmar_cierre),
            ],
        ),
    )

    return sidebar