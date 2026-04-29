import flet as ft

# Compatibilidad íconos (Flet nuevo)
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons

from login import LoginView


def main(page: ft.Page):
    page.title = "Corallie Bubble - Punto de Venta"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F9F6FB"
    page.padding = 0

    # --- FUNCION BACK (flecha de regresar en AppBar, si la usas) ---
    def view_pop(view):
        # Solo hacemos pop si hay más de una vista
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = view_pop

    # --- CARGAR LOGIN COMO PRIMERA VISTA ---
    page.views.clear()
    page.views.append(LoginView(page))   # LoginView devuelve un ft.View("/") :contentReference[oaicite:1]{index=1}
    page.update()


ft.app(target=main)
