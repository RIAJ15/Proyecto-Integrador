import flet as ft

# Compatibilidad íconos (Flet nuevo)
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons

from connector import get_connection

# -------------------------------------------------------------------
# VISTA DE REGISTRO (CLIENTE / EMPLEADO)
# -------------------------------------------------------------------
def RegistroView(page: ft.Page, tipo: str):
    """
    tipo: "Cliente" o "Empleado"
    """

    titulo = f"Registro de {tipo}"

    txt_nombre = ft.TextField(label="Nombre", autofocus=True)
    txt_apellido = ft.TextField(label="Apellido")
    txt_correo = ft.TextField(label="Correo electrónico")
    txt_tel = ft.TextField(label="Teléfono")
    txt_usuario = ft.TextField(label="Nombre de usuario")
    txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    txt_pass2 = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True)

    lbl_msg = ft.Text("")

    # -------------------------------------------------------------
    # VALIDACIONES POR CAMPO
    # -------------------------------------------------------------
    def validar_campos():
        valido = True

        # limpiar errores
        for campo in [txt_nombre, txt_apellido, txt_correo, txt_tel,
                      txt_usuario, txt_pass, txt_pass2]:
            campo.error_text = None

        if not (txt_nombre.value or "").strip():
            txt_nombre.error_text = "Ingresa tu nombre"
            valido = False

        if not (txt_apellido.value or "").strip():
            txt_apellido.error_text = "Ingresa tu apellido"
            valido = False

        correo = (txt_correo.value or "").strip()
        if not correo:
            txt_correo.error_text = "Ingresa tu correo"
            valido = False
        elif "@" not in correo or "." not in correo:
            txt_correo.error_text = "Correo no válido"
            valido = False

        tel = (txt_tel.value or "").strip()
        if not tel:
            txt_tel.error_text = "Ingresa tu teléfono"
            valido = False
        elif not tel.isdigit():
            txt_tel.error_text = "El teléfono solo debe contener números"
            valido = False

        usuario = (txt_usuario.value or "").strip()
        if not usuario:
            txt_usuario.error_text = "Ingresa un nombre de usuario"
            valido = False

        password = (txt_pass.value or "").strip()
        password2 = (txt_pass2.value or "").strip()
        if not password:
            txt_pass.error_text = "Ingresa una contraseña"
            valido = False
        elif len(password) < 4:
            txt_pass.error_text = "La contraseña debe tener al menos 4 caracteres"
            valido = False

        if not password2:
            txt_pass2.error_text = "Confirma tu contraseña"
            valido = False
        elif password and password2 and password != password2:
            txt_pass2.error_text = "Las contraseñas no coinciden"
            valido = False

        page.update()
        return valido

    # -------------------------------------------------------------
    # IR AL LOGIN (REUTILIZABLE)
    # -------------------------------------------------------------
    def ir_login():
        from login import LoginView   # import aquí para evitar ciclo
        page.views.clear()
        page.views.append(LoginView(page))
        page.go("/")
        page.update()

    # -------------------------------------------------------------
    # REGISTRAR EN LA BD
    # -------------------------------------------------------------
    def registrar(e):
        if not validar_campos():
            return

        nombre = txt_nombre.value.strip()
        apellido = txt_apellido.value.strip()
        correo = txt_correo.value.strip()
        tel = txt_tel.value.strip()
        usuario = txt_usuario.value.strip()
        password = txt_pass.value.strip()

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Revisar si el usuario ya existe
            cursor.execute(
                "SELECT IdUsuario FROM usuario WHERE NombreUsuario=%s",
                (usuario,),
            )
            if cursor.fetchone():
                txt_usuario.error_text = "Ese nombre de usuario ya existe"
                page.update()
                return

            # Insertar en usuario
            cursor.execute(
                "INSERT INTO usuario (NombreUsuario, Contraseña) VALUES (%s, %s)",
                (usuario, password),
            )
            id_usuario = cursor.lastrowid

            # Insertar en cliente o empleado
            tabla = "cliente" if tipo == "Cliente" else "empleado"
            cursor.execute(
                f"INSERT INTO {tabla} (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario) "
                "VALUES (%s, %s, %s, %s, %s)",
                (nombre, apellido, tel, correo, id_usuario),
            )

            conn.commit()

            # Aviso + regresar al login
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{tipo} registrado correctamente. Ahora puedes iniciar sesión.")
            )
            page.snack_bar.open = True
            page.update()

            ir_login()

        except Exception as ex:
            lbl_msg.value = f"Error al registrar: {ex}"
            lbl_msg.color = "red"
            page.update()
        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass

    # Botón manual por si quiere cancelar
    def volver_login(e):
        ir_login()

    # -------------------------------------------------------------
    # LAYOUT
    # -------------------------------------------------------------
    contenido = ft.Container(
        expand=True,
        bgcolor="#F9F6FB",
        alignment=ft.Alignment.center,
        content=ft.Column(
            [
                ft.Text("Corallie Bubble", size=26, weight="bold", color="#C86DD7"),
                ft.Text(titulo, size=20),
                txt_nombre,
                txt_apellido,
                txt_correo,
                txt_tel,
                txt_usuario,
                txt_pass,
                txt_pass2,
                ft.ElevatedButton(
                    "Registrarme",
                    bgcolor="#C86DD7",
                    color="white",
                    on_click=registrar,
                ),
                ft.TextButton("Volver al login", on_click=volver_login),
                lbl_msg,
            ],
            spacing=15,
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            width=400,
        ),
    )

    return ft.View(route="/registro", controls=[contenido])
