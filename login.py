import flet as ft
import hashlib
from connector import get_connection
from registro import RegistroView
from corte_manager import abrir_corte
from admin import admin_view

# -------------------------------------------------------------------
# COMPATIBILIDAD FLET (evita: module 'flet' has no attribute 'icons')
# -------------------------------------------------------------------
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons

if not hasattr(ft, "animation"):
    ft.animation = ft

_original_container = ft.Container

def SafeContainer(*args, **kwargs):
    kwargs.pop("elevation", None)
    return _original_container(*args, **kwargs)

ft.Container = SafeContainer

# -------------------------------------------------------------------
# LOGIN PRINCIPAL
# -------------------------------------------------------------------
def LoginView(page: ft.Page):

    txt_user = ft.TextField(label="Correo o Usuario", border_radius=12)
    txt_pass = ft.TextField(label="Contraseña", password=True, border_radius=12)
    lbl_msg = ft.Text("")

    # -------------------------------------------------------------
    # ALMACENAMIENTO COMPATIBLE (Flet nuevo: shared_preferences es async)
    # -------------------------------------------------------------
    async def storage_set(key, value):
        # Guarda SIEMPRE en memoria de la sesión (sync) para poder leerlo sin await en otros módulos.
        if not hasattr(page, "_mem_store") or not isinstance(getattr(page, "_mem_store", None), dict):
            page._mem_store = {}
        page._mem_store[key] = value

        # Flet nuevo: shared_preferences (async, típicamente strings)
        if hasattr(page, "shared_preferences"):
            try:
                await page.shared_preferences.set(key, str(value))
                return
            except Exception:
                # si falla, ya quedó en memoria
                return

        # Flet viejo: client_storage
        if hasattr(page, "client_storage"):
            try:
                page.client_storage.set(key, value)
            except Exception:
                pass

    # -------------------------------------------------------------
    # INICIAR SESIÓN
    # -------------------------------------------------------------
    async def login(e):
        # Importamos aquí para evitar import circular
        from menu import menu_interactivo_view
        from punto_venta import punto_venta_view

        user = (txt_user.value or "").strip()
        password = (txt_pass.value or "").strip()

        if not user or not password:
            lbl_msg.value = "Ingresa usuario y contraseña"
            lbl_msg.color = "red"
            page.update()
            return

        # Soporta contraseñas guardadas en texto plano o SHA-256 (porque tu BD tiene ambas)
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # 1) Validar credenciales en tabla REAL: `usuario`
            cursor.execute(
                """
                SELECT IdUsuario, NombreUsuario
                FROM usuario
                WHERE NombreUsuario=%s AND (Contraseña=%s OR Contraseña=%s)
                """,
                (user, password, password_hash),
            )
            user_row = cursor.fetchone()

            if not user_row:
                lbl_msg.value = "Usuario o contraseña incorrectos"
                lbl_msg.color = "red"
                page.update()
                return

            id_usuario = user_row["IdUsuario"]

            # 2) ¿Es admin?
            # (Regla simple: si el NombreUsuario es "admin")
            if str(user_row.get("NombreUsuario", "")).strip().lower() == "admin":
                page.views.append(admin_view(page, "Administrador"))
                page.go("/admin")
                page.update()
                return

            # 2) ¿Es empleado?
            cursor.execute(
                "SELECT IdEmpleado, Nombre FROM empleado WHERE Usuario_IdUsuario=%s",
                (id_usuario,),
            )
            emp = cursor.fetchone()
            if emp:
                id_empleado = int(emp["IdEmpleado"])
                nombre_empleado = emp.get("Nombre") or user_row.get("NombreUsuario")

                # ✅ abrir corte usando el ID (número)
                corte_id = abrir_corte(id_empleado)
                await storage_set("corte_id", int(corte_id))
                await storage_set("empleado", nombre_empleado)

                page.views.append(punto_venta_view(page, nombre_empleado))
                page.go("/pos")
                page.update()
                return



            # 3) ¿Es cliente?
            cursor.execute(
                "SELECT Nombre FROM cliente WHERE Usuario_IdUsuario=%s",
                (id_usuario,),
            )
            cli = cursor.fetchone()
            if cli:
                nombre = cli.get("Nombre") or user_row.get("NombreUsuario")
                page.views.append(menu_interactivo_view(page, nombre))
                page.go("/menu")
                page.update()
                return

            # Existe en usuario pero no está ligado
            lbl_msg.value = "Tu usuario no está ligado a cliente ni empleado"
            lbl_msg.color = "red"
            page.update()

        except Exception as ex:
            lbl_msg.value = f"Error al conectar con la base de datos: {ex}"
            lbl_msg.color = "red"
            page.update()
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass

    # -------------------------------------------------------------
    # IR A REGISTRO (cliente)
    # -------------------------------------------------------------
    def ir_registro(e):
        page.views.append(RegistroView(page, "Cliente"))
        page.go("/registro")
        page.update()

    def olvidar(e):
        lbl_msg.value = "Función próximamente disponible"
        lbl_msg.color = "blue"
        page.update()

    contenido = ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            [
                ft.Text("Corallie Bubble", size=36, weight="bold", color="#C86DD7"),
                ft.Text("Iniciar Sesión", size=22),
                txt_user,
                txt_pass,
                ft.ElevatedButton("Iniciar sesión", bgcolor="#C86DD7", color="white", on_click=login),
                lbl_msg,
                ft.TextButton("Registrarse", on_click=ir_registro),
                ft.TextButton("Olvidé mi contraseña", on_click=olvidar),
            ],
            spacing=20,
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    return ft.View(route="/", controls=[contenido])