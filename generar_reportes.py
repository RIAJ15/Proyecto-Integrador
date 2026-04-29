import os
import flet as ft
from datetime import datetime
from io import BytesIO

from connector import get_connection
from sidebar_admin import build_admin_sidebar
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

# ------------------------------------------------------------
# Compatibilidad Flet
# ------------------------------------------------------------
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons


def generar_reportes_view(page: ft.Page, nombre: str = "Empleado") -> ft.View:
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

    def money(v):
        try:
            return f"$ {float(v):,.2f}"
        except Exception:
            return "$ 0.00"

    def validar_fecha(valor: str):
        raw = (valor or "").strip()
        if not raw:
            return False, "Ingresa la fecha", None
        try:
            dt = datetime.strptime(raw, "%Y-%m-%d")
            return True, None, dt.date()
        except Exception:
            return False, "Usa formato YYYY-MM-DD", None

    # ------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------
    def ir_inicio(e=None):
        if len(page.views) > 1:
            page.views.pop()
        page.go("/pos")
        page.update()
    def ir_inicio(e=None):
        if len(page.views) > 1:
            page.views.pop()
        page.go("/admin")
        page.update()

    def ir_control_empleados(e=None):
        from admin_empleados import admin_empleados_view
        page.views.append(admin_empleados_view(page, nombre))
        page.go("/admin_empleados")
        page.update()

    def ir_control_usuarios(e=None):
        from admin_usuarios import admin_usuarios_view
        page.views.append(admin_usuarios_view(page, nombre))
        page.go("/admin_usuarios")
        page.update()

    def ir_reportes(e=None):
        page.go("/reportes")
        page.update()

    def cerrar_sesion(e=None):
        from login import LoginView
        page.views.clear()
        page.views.append(LoginView(page))
        page.go("/")
        page.update()

    # ------------------------------------------------------------
    # Estado del reporte
    # ------------------------------------------------------------
    ultimo_reporte = {
        "data": [],
        "total": 0.0,
        "inicio": "",
        "fin": "",
    }

    # ------------------------------------------------------------
    # Base de datos
    # ------------------------------------------------------------
    def obtener_ventas(inicio: str, fin: str):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT IdVentas, FechaVenta, Hora, DetalleVenta, Subtotal, Impuesto, Total
                FROM ventas
                WHERE FechaVenta BETWEEN %s AND %s
                ORDER BY FechaVenta DESC, Hora DESC, IdVentas DESC
                """,
                (inicio, fin),
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

    # ------------------------------------------------------------
    # PDF
    # ------------------------------------------------------------
    def crear_pdf_bytes(data: list, total: float, inicio: str, fin: str) -> bytes:
        styles = getSampleStyleSheet()
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter)

        elements = []
        elements.append(Paragraph("Corallie Bubble - Reporte de Ventas", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Generado por: {nombre}", styles["Normal"]))
        elements.append(Paragraph(f"Rango: {inicio} a {fin}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        headers = ["ID", "Fecha", "Hora", "Detalle", "Subtotal", "Impuesto", "Total"]
        table_data = [headers]

        for r in data:
            table_data.append(
                [
                    str(r.get("IdVentas", "")),
                    str(r.get("FechaVenta", "")),
                    str(r.get("Hora", "")),
                    str(r.get("DetalleVenta", "")),
                    f"{float(r.get('Subtotal', 0) or 0):.2f}",
                    f"{float(r.get('Impuesto', 0) or 0):.2f}",
                    f"{float(r.get('Total', 0) or 0):.2f}",
                ]
            )

        table_data.append(["", "", "", "TOTAL GENERAL", "", "", f"{float(total):.2f}"])

        tabla_pdf = Table(table_data, repeatRows=1)
        tabla_pdf.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9D5F3")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (4, 1), (-1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        elements.append(tabla_pdf)
        doc.build(elements)
        return buf.getvalue()

    def guardar_pdf_en_proyecto(pdf_bytes: bytes, nombre_archivo: str) -> str:
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        with open(ruta, "wb") as f:
            f.write(pdf_bytes)
        return ruta

    # ------------------------------------------------------------
    # Controles
    # ------------------------------------------------------------
    fecha_inicio = ft.TextField(
        label="Fecha inicio (YYYY-MM-DD)",
        border_radius=12,
        width=240,
    )

    fecha_fin = ft.TextField(
        label="Fecha fin (YYYY-MM-DD)",
        border_radius=12,
        width=240,
    )

    txt_total = ft.Text(
        "Total general: $ 0.00",
        size=18,
        weight="bold",
        color="#C86DD7",
    )

    lbl_estado = ft.Text("", size=12, color="#6B7280")

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Detalle")),
            ft.DataColumn(ft.Text("Subtotal")),
            ft.DataColumn(ft.Text("Impuesto")),
            ft.DataColumn(ft.Text("Total")),
        ],
        rows=[],
        border_radius=12,
        heading_row_color="#F3E9F7",
        data_row_min_height=52,
        data_row_max_height=90,
        column_spacing=18,
    )

    # ------------------------------------------------------------
    # Lógica de pantalla
    # ------------------------------------------------------------
    def pintar_tabla(data: list):
        tabla.rows = []

        for r in data:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(r.get("IdVentas", "")))),
                        ft.DataCell(ft.Text(str(r.get("FechaVenta", "")))),
                        ft.DataCell(ft.Text(str(r.get("Hora", "")))),
                        ft.DataCell(
                            ft.Text(
                                str(r.get("DetalleVenta", "")),
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            )
                        ),
                        ft.DataCell(ft.Text(money(r.get("Subtotal", 0)))),
                        ft.DataCell(ft.Text(money(r.get("Impuesto", 0)))),
                        ft.DataCell(ft.Text(money(r.get("Total", 0)))),
                    ]
                )
            )

    def generar_reporte(e=None):
        fecha_inicio.error_text = None
        fecha_fin.error_text = None

        ok1, err1, f1 = validar_fecha(fecha_inicio.value)
        ok2, err2, f2 = validar_fecha(fecha_fin.value)

        if not ok1:
            fecha_inicio.error_text = err1
        if not ok2:
            fecha_fin.error_text = err2

        if not ok1 or not ok2:
            page.update()
            show_snack("Corrige las fechas del reporte", ok=False)
            return

        if f1 > f2:
            fecha_inicio.error_text = "La fecha inicio no puede ser mayor"
            fecha_fin.error_text = "La fecha fin debe ser posterior"
            page.update()
            show_snack("El rango de fechas no es válido", ok=False)
            return

        try:
            data = obtener_ventas(fecha_inicio.value.strip(), fecha_fin.value.strip())
            total = sum(float(r.get("Total", 0) or 0) for r in data)

            ultimo_reporte["data"] = data
            ultimo_reporte["total"] = total
            ultimo_reporte["inicio"] = fecha_inicio.value.strip()
            ultimo_reporte["fin"] = fecha_fin.value.strip()

            pintar_tabla(data)
            txt_total.value = f"Total general: {money(total)}"
            lbl_estado.value = f"Ventas encontradas: {len(data)}"
            page.update()

            show_snack("Reporte generado correctamente")
        except Exception as ex:
            show_snack(f"Error al generar reporte: {ex}", ok=False)

    def descargar_pdf(e=None):
        if not ultimo_reporte["data"]:
            show_snack("Primero genera un reporte", ok=False)
            return

        try:
            pdf_bytes = crear_pdf_bytes(
                ultimo_reporte["data"],
                ultimo_reporte["total"],
                ultimo_reporte["inicio"],
                ultimo_reporte["fin"],
            )

            nombre_archivo = (
                f"reporte_{ultimo_reporte['inicio']}_a_{ultimo_reporte['fin']}.pdf"
                .replace(":", "-")
                .replace("/", "-")
            )

            ruta = guardar_pdf_en_proyecto(pdf_bytes, nombre_archivo)
            show_snack(f"PDF guardado en: {ruta}")

        except Exception as ex:
            open_dialog(
                ft.AlertDialog(
                    title=ft.Text("No se pudo guardar el PDF"),
                    content=ft.Text(str(ex)),
                )
            )

    # ------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------
    sidebar = build_admin_sidebar(
        page=page,
        nombre=nombre or "Administrador",
        ir_inicio=ir_inicio,
        ir_control_empleados=ir_control_empleados,
        ir_control_usuarios=ir_control_usuarios,
        ir_reportes=ir_reportes,
        cerrar_sesion_real=cerrar_sesion,
    )
    # ------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------
    header = ft.Row(
        [
            ft.Text("Generar reportes", size=22, weight="bold", color="#C86DD7"),
            ft.Container(expand=True),
        ]
    )

    filtros = ft.Container(
        bgcolor="white",
        border_radius=18,
        padding=16,
        content=ft.Column(
            [
                ft.Text("Consulta de ventas", size=16, weight="bold"),
                ft.Row(
                    [
                        fecha_inicio,
                        fecha_fin,
                    ],
                    spacing=12,
                    wrap=True,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Generar reporte",
                            bgcolor="#C86DD7",
                            color="white",
                            on_click=generar_reporte,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=20),
                                padding=18,
                            ),
                        ),
                        ft.OutlinedButton(
                            "Descargar PDF",
                            on_click=descargar_pdf,
                        ),
                    ],
                    spacing=12,
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
                filtros,
                txt_total,
                tabla_wrap,
            ],
            spacing=16,
            expand=True,
        ),
    )

    layout = ft.Row(
        [
            sidebar,
            main_content,
        ],
        expand=True,
    )

    appbar = ft.AppBar(
        title=ft.Text("Reportes"),
        bgcolor="#C86DD7",
        color="white",
    )

    return ft.View(route="/reportes", controls=[layout], appbar=appbar)