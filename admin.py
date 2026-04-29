# admin.py
import flet as ft
from sidebar_admin import build_admin_sidebar

# Compatibilidad íconos (Flet nuevo)
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons



def admin_view(page: ft.Page, nombre: str = "Administrador") -> ft.View:
    # -----------------------------
    # Navegación
    # -----------------------------
    def ir_control_empleados(e):
        from admin_empleados import admin_empleados_view
        page.views.append(admin_empleados_view(page, nombre))
        page.go("/admin_empleados")
        page.update()

    def ir_control_usuarios(e):
        from admin_usuarios import admin_usuarios_view
        page.views.append(admin_usuarios_view(page, nombre))
        page.go("/admin_usuarios")
        page.update()

    def ir_reportes(e):
        # OJO: tu generar_reportes_view retorna ruta "/reportes"
        from generar_reportes import generar_reportes_view
        page.views.append(generar_reportes_view(page, nombre))
        page.go("/reportes")
        page.update()

    def cerrar_sesion(e):
        from login import LoginView
        page.views.clear()
        page.views.append(LoginView(page))
        page.go("/")
        page.update()

    # -----------------------------
    # UI helpers
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

    def crear_tarjeta(titulo: str, descripcion: str, on_click):
        card = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=24,
            padding=20,
            col={"xs": 12, "sm": 6, "md": 6, "lg": 4},
            content=ft.Column(
                [
                    ft.Text(titulo, size=18, weight="bold", color="#333333"),
                    ft.Text(descripcion, size=13, color="#666666"),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Ingresar",
                        bgcolor="#C86DD7",
                        color="white",
                        on_click=on_click,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            padding=20,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10,
            ),
            animate_scale=ft.Animation(300, "easeOut"),
            animate_opacity=300,
        )

        def on_hover(ev):
            card.scale = 1.03 if ev.data == "true" else 1.0
            card.opacity = 1.0 if ev.data == "true" else 0.95
            card.update()

        card.on_hover = on_hover
        return card

    # -----------------------------
    # Sidebar
    # -----------------------------
    sidebar = build_admin_sidebar(
        page=page,
        nombre=nombre,
        ir_inicio=lambda e: None,
        ir_control_empleados=ir_control_empleados,
        ir_control_usuarios=ir_control_usuarios,
        ir_reportes=ir_reportes,
        cerrar_sesion_real=cerrar_sesion,
    )
    # -----------------------------
    # Contenido principal
    # -----------------------------
    tarjetas = ft.ResponsiveRow(
        [
            crear_tarjeta(
                "Control de empleados",
                "Administra empleados: altas, bajas, edición, consultas.",
                ir_control_empleados,
            ),
            crear_tarjeta(
                "Control de usuarios (Clientes)",
                "Administra clientes/usuarios: edición, búsqueda y control.",
                ir_control_usuarios,
            ),
            crear_tarjeta(
                "Generar reportes",
                "Accede a la interfaz de reportes ya existente.",
                ir_reportes,
            ),
        ],
        run_spacing=20,
        spacing=20,
    )

    main_content = ft.Container(
        expand=True,
        bgcolor="#F9F6FB",
        padding=20,
        content=ft.Column(
            [
                ft.Text(f"Bienvenido, {nombre}", size=18, weight="bold", color="#C86DD7"),
                ft.Text("Selecciona un apartado para continuar.", size=13, color="#666666"),
                ft.Container(height=10),
                tarjetas,
            ],
            spacing=10,
        ),
    )

    layout = ft.Row([sidebar, main_content], expand=True)

    appbar = ft.AppBar(
        title=ft.Text("Corallie Bubble - Admin"),
        bgcolor="#C86DD7",
        color="white",
    )

    return ft.View(route="/admin", controls=[layout], appbar=appbar)