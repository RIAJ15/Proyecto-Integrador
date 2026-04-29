import flet as ft
from datetime import datetime
import asyncio

from connector import get_connection
from corte_manager import obtener_info_corte, resumen_por_corte, cerrar_corte

# ------------------------------------------------------------
# Compatibilidad Flet 0.80 / 0.81+
# ------------------------------------------------------------
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons

if not hasattr(ft, "animation"):
    ft.animation = ft

# Compatibilidad alignment
ALIGN_CENTER = getattr(getattr(ft, "alignment", None), "center", None) or getattr(ft.Alignment, "CENTER", None)


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


ICON_MENU = _icon("MENU")
ICON_HOME = _icon("HOME", "HOME_OUTLINED")
ICON_BOX = _icon("INVENTORY_2", "INVENTORY", "STORE")
ICON_SWAP = _icon("SWAP_HORIZ", "COMPARE_ARROWS", "SYNC_ALT")
ICON_WALLET = _icon("ACCOUNT_BALANCE_WALLET", "WALLET", "PAYMENTS")
ICON_REPORT = _icon("ASSESSMENT", "ANALYTICS", "BAR_CHART")
ICON_MORE = _icon("MORE_HORIZ", "MORE_VERT")
ICON_LOGOUT = _icon("LOGOUT", "EXIT_TO_APP")


def build_sidebar(
    page: ft.Page,
    nombre: str,
    ir_inicio,
    ir_inventario,
    ir_movimientos,
    ir_caja_chica,
    ir_reportes,
    cerrar_sesion_real,
):
    """Sidebar compatible con Flet reciente para el módulo POS."""

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

    def _store_get(key, default=None):
        try:
            store = getattr(page, "_mem_store", None)
            if isinstance(store, dict) and key in store:
                return store.get(key, default)
        except Exception:
            pass
        try:
            if hasattr(page, "client_storage"):
                value = page.client_storage.get(key)
                return default if value is None else value
        except Exception:
            pass
        return default

    def _store_remove(key):
        try:
            store = getattr(page, "_mem_store", None)
            if isinstance(store, dict):
                store.pop(key, None)
        except Exception:
            pass
        try:
            if hasattr(page, "client_storage"):
                page.client_storage.remove(key)
        except Exception:
            pass

    def money(v):
        try:
            return f"$ {float(v):,.2f}"
        except Exception:
            return "$ 0.00"

    # ------------------------------------------------------------
    # Datos de corte
    # ------------------------------------------------------------
    corte_id = _store_get("corte_id")
    try:
        corte_id_int = int(corte_id) if corte_id else None
    except Exception:
        corte_id_int = None

    info = obtener_info_corte(corte_id_int) if corte_id_int else None
    if corte_id_int:
        ing, egr, bal, movs, platillos = resumen_por_corte(corte_id_int)
    else:
        ing, egr, bal, movs, platillos = 0.0, 0.0, 0.0, 0, 0

    def db_movimientos_corte(corte_id_param, limit=6):
        if not corte_id_param:
            return []
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                f"""
                SELECT 'Entrada' AS Tipo, Fecha AS FechaMov, Cantidad AS Cant, Descripcion AS Texto
                FROM entradasproductos
                WHERE CorteCaja_idCorteCaja = %s
                UNION ALL
                SELECT 'Salida' AS Tipo, FechaSalida AS FechaMov, Cantidad AS Cant, Detalle AS Texto
                FROM salidasproductos
                WHERE CorteCaja_idCorteCaja = %s
                ORDER BY FechaMov DESC
                LIMIT {int(limit)}
                """,
                (int(corte_id_param), int(corte_id_param)),
            )
            return cur.fetchall() or []
        except Exception:
            return []
        finally:
            try:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
            except Exception:
                pass

    movs_list = db_movimientos_corte(corte_id_int, limit=6)

    # ------------------------------------------------------------
    # Acciones del menú
    # ------------------------------------------------------------
    def confirmar_cierre(e=None):
        resumen = []
        if corte_id_int:
            resumen.append(f"Corte activo: #{corte_id_int}")
            resumen.append(f"Ingresos: {money(ing)} | Egresos: {money(egr)}")
            resumen.append(f"Balance: {money(bal)} | Movimientos: {movs}")
        else:
            resumen.append("No hay corte activo detectado.")

        dlg = ft.AlertDialog(modal=True, title=ft.Text("Cerrar sesión"))

        def cancelar(_e=None):
            dlg.open = False
            page.update()

        def solo_salir(_e=None):
            dlg.open = False
            page.update()
            cerrar_sesion_real(None)

        def cerrar_corte_y_salir(_e=None):
            try:
                if corte_id_int:
                    cerrar_corte(int(corte_id_int))
            except Exception:
                pass
            _store_remove("corte_id")
            _store_remove("empleado")
            dlg.open = False
            page.update()
            cerrar_sesion_real(None)

        dlg.content = ft.Column(
            tight=True,
            controls=[
                ft.Text("¿Deseas cerrar sesión?", weight="bold"),
                ft.Container(height=6),
                ft.Text("\n".join(resumen), size=12),
            ],
        )
        dlg.actions = [ft.TextButton("Cancelar", on_click=cancelar)]

        if corte_id_int:
            dlg.actions.extend(
                [
                    ft.OutlinedButton("Solo cerrar sesión", on_click=solo_salir),
                    ft.ElevatedButton(
                        "Cerrar corte y salir",
                        bgcolor="#C86DD7",
                        color="white",
                        on_click=cerrar_corte_y_salir,
                    ),
                ]
            )
        else:
            dlg.actions.append(
                ft.ElevatedButton(
                    "Sí, cerrar sesión",
                    bgcolor="#C86DD7",
                    color="white",
                    on_click=solo_salir,
                )
            )

        dlg.actions_alignment = ft.MainAxisAlignment.END
        open_dialog(dlg)

    def ver_perfil(e=None):
        mov_txt = "Sin movimientos recientes."
        if movs_list:
            mov_txt = "\n".join(
                [
                    f"• {m.get('Tipo')} | {m.get('FechaMov')} | Cant: {m.get('Cant')}"
                    for m in movs_list[:8]
                ]
            )

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Perfil"),
            content=ft.Container(
                width=480,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Row(
                            [
                                ft.Container(
                                    width=56,
                                    height=56,
                                    border_radius=18,
                                    bgcolor="#FFE0F0",
                                    alignment=ALIGN_CENTER,
                                    content=ft.Text(
                                        (nombre[:1] or "U").upper(),
                                        size=22,
                                        weight="bold",
                                    ),
                                ),
                                ft.Column(
                                    [
                                        ft.Text(nombre, size=16, weight="bold"),
                                        ft.Text("Rol: Empleado", size=12, color="#6B7280"),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            spacing=12,
                        ),
                        ft.Divider(),
                        ft.Text(
                            f"Corte actual: #{corte_id_int}" if corte_id_int else "Corte actual: —",
                            weight="bold",
                        ),
                        ft.Text(f"Ingresos: {money(ing)}", size=12),
                        ft.Text(f"Egresos: {money(egr)}", size=12),
                        ft.Text(
                            f"Balance: {money(bal)} | Movimientos: {movs} | Platillos: {platillos}",
                            size=12,
                        ),
                        ft.Divider(height=10),
                        ft.Text("Movimientos recientes", weight="bold", size=12),
                        ft.Text(mov_txt, size=11, color="#4B5563"),
                    ],
                ),
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=lambda _e: setattr(dlg, "open", False) or page.update(),
                )
            ],
        )
        open_dialog(dlg)

    # ------------------------------------------------------------
    # Fecha / hora
    # ------------------------------------------------------------
    lbl_datetime = ft.Text("", size=11, color="white70")

    def paint_datetime():
        try:
            lbl_datetime.value = datetime.now().strftime("%Y-%m-%d  %H:%M")
            if getattr(lbl_datetime, "page", None):
                lbl_datetime.update()
        except Exception:
            try:
                page.update()
            except Exception:
                pass

    async def _datetime_loop():
        while True:
            try:
                paint_datetime()
                await asyncio.sleep(1)
            except Exception:
                await asyncio.sleep(1)

    if hasattr(page, "run_task") and not getattr(page, "_sidebar_datetime_started", False):
        page._sidebar_datetime_started = True
        page.run_task(_datetime_loop)

    paint_datetime()

    # ------------------------------------------------------------
    # Construcción UI
    # ------------------------------------------------------------
    sidebar_state = {"collapsed": False}
    nav_text_refs = []

    avatar_txt = ft.Text((nombre[:1] or "U").upper(), weight="bold", color="#6C2BD9")

    avatar = ft.Container(
        width=44,
        height=44,
        border_radius=16,
        bgcolor="#FFE0F0",
        alignment=ALIGN_CENTER,
        content=avatar_txt,
    )

    user_info = ft.Column(
        [
            ft.Text(
                nombre,
                size=13,
                weight="bold",
                color="white",
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            ft.Text("Empleado", size=11, color="white70"),
        ],
        spacing=1,
        expand=True,
    )

    user_menu = ft.PopupMenuButton(
        icon=ICON_MORE,
        icon_color="white",
        items=[
            ft.PopupMenuItem(content=ft.Text("Ver perfil"), on_click=ver_perfil),
            ft.PopupMenuItem(),
            ft.PopupMenuItem(content=ft.Text("Cerrar sesión"), on_click=confirmar_cierre),
        ],
    )

    user_row = ft.Row(
        [avatar, user_info, user_menu],
        spacing=10,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    user_header_expanded = ft.Container(
        padding=ft.padding.symmetric(horizontal=10, vertical=10),
        border_radius=18,
        bgcolor="rgba(255,255,255,0.12)",
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=user_row,
    )

    user_header_collapsed = ft.Container(
        padding=6,
        border_radius=18,
        bgcolor="rgba(255,255,255,0.12)",
        alignment=ALIGN_CENTER,
        content=avatar,
    )

    user_header_switch = ft.AnimatedSwitcher(
        content=user_header_expanded,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=200,
        reverse_duration=160,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
    )

    def nav_item(icon, text, on_click):
        text_ctrl = ft.Text(text, color="white", size=13, visible=True)
        nav_text_refs.append(text_ctrl)

        content_controls = []
        if icon is not None:
            content_controls.append(ft.Icon(icon, color="white", size=22))
        content_controls.append(text_ctrl)

        item = ft.Container(
            height=44,
            padding=ft.padding.symmetric(horizontal=10),
            border_radius=16,
            ink=True,
            on_click=on_click,
            animate=ft.animation.Animation(180, ft.AnimationCurve.EASE_OUT),
            content=ft.Row(content_controls, spacing=10),
        )

        def on_hover(e):
            item.bgcolor = "rgba(255,255,255,0.18)" if e.data == "true" else None
            try:
                item.update()
            except Exception:
                pass

        item.on_hover = on_hover
        return item

    def toggle_sidebar(e=None):
        sidebar_state["collapsed"] = not sidebar_state["collapsed"]
        collapsed = sidebar_state["collapsed"]

        sidebar.width = 76 if collapsed else 240
        sidebar.padding = 12 if collapsed else 16

        user_info.visible = not collapsed
        user_menu.visible = not collapsed
        user_row.alignment = (
            ft.MainAxisAlignment.CENTER if collapsed else ft.MainAxisAlignment.SPACE_BETWEEN
        )
        user_row.spacing = 0 if collapsed else 10

        user_header_switch.content = user_header_collapsed if collapsed else user_header_expanded

        avatar.width = 40 if collapsed else 44
        avatar.height = 40 if collapsed else 44
        avatar.border_radius = 14 if collapsed else 16

        lbl_datetime.visible = not collapsed

        for t in nav_text_refs:
            t.visible = not collapsed

        page.update()

    nav_column = ft.Column(
        [
            nav_item(ICON_HOME, "Inicio", ir_inicio),
            nav_item(ICON_BOX, "Ver inventario", ir_inventario),
            nav_item(ICON_SWAP, "Entradas y salidas", ir_movimientos),
            nav_item(ICON_WALLET, "Caja chica", ir_caja_chica),
            nav_item(ICON_REPORT, "Reportes", ir_reportes),
        ],
        spacing=6,
    )

    header_row = ft.Row(
        [
            ft.IconButton(icon=ICON_MENU, icon_color="white", on_click=toggle_sidebar),
            ft.Container(expand=True),
        ]
    )

    sidebar = ft.Container(
        width=240,
        bgcolor="#C86DD7",
        padding=16,
        animate=ft.animation.Animation(220, ft.AnimationCurve.EASE_OUT),
        content=ft.Column(
            [
                header_row,
                ft.Container(height=10),
                user_header_switch,
                ft.Container(height=8),
                ft.Container(padding=ft.padding.only(left=6), content=lbl_datetime),
                ft.Container(height=10),
                nav_column,
                ft.Container(expand=True),
                nav_item(ICON_LOGOUT, "Cerrar sesión", confirmar_cierre),
            ],
            spacing=6,
        ),
    )

    return sidebar