import flet as ft
from datetime import datetime
from connector import get_connection
import asyncio
import inspect

# ------------------------------------------------------------
# COMPATIBILIDAD FLET 0.81+ (sin cambiar tu lógica)
# ------------------------------------------------------------
# Icons: en algunas versiones es ft.icons, en otras ft.Icons
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons

# animation: en versiones antiguas existía ft.animation
if not hasattr(ft, "animation"):
    ft.animation = ft

# Alignment: evita usar ft.Alignment.CENTER (no existe en 0.81)
ALIGN_CENTER = getattr(getattr(ft, "alignment", None), "center", None) or getattr(ft.Alignment, "CENTER", None)
ALIGN_TOP_CENTER = getattr(getattr(ft, "alignment", None), "top_center", None) or getattr(ft.Alignment, "TOP_CENTER", None)


def _icon(name: str, fallback: str):
    """Obtiene un icono de forma compatible entre versiones (ft.icons.* o string)."""
    try:
        return getattr(ft.icons, name)
    except Exception:
        return fallback

def _icon_data(name: str):
    """Devuelve IconData si existe en ft.icons/ft.Icons; si no, None."""
    try:
        return getattr(ft.icons, name)
    except Exception:
        return None


def _iconbtn(icon_name: str, emoji: str, **kwargs):
    """Botón de ícono compatible.
    - Si existe IconData: usa IconButton normal.
    - Si NO existe IconData: usa Container clickeable con emoji (fallback universal).
    """
    icon_data = _icon_data(icon_name)
    if icon_data is not None:
        return ft.IconButton(icon=icon_data, **kwargs)

    on_click = kwargs.pop("on_click", None)
    # Algunos builds no soportan tooltip/ink en Container; lo ignoramos para evitar crash.
    kwargs.pop("tooltip", None)
    icon_color = kwargs.pop("icon_color", None) or kwargs.pop("color", None)

    return ft.Container(
        width=40,
        height=40,
        border_radius=12,
        alignment=ALIGN_CENTER,
        on_click=on_click,
        content=ft.Text(emoji, size=18, color=icon_color),
    )

def _iconctrl(icon_name: str, emoji: str, size: int = 18, color=None):
    """Icono compatible para usar dentro de rows/containers."""
    icon_data = _icon_data(icon_name)
    if icon_data is not None:
        return ft.Icon(icon_data, size=size, color=color)
    return ft.Text(emoji, size=size)

# ------------------------------------------------------------
# MENU INTERACTIVO (CLIENTE) - MÓVIL + CARRITO + HISTORIAL + ESTATUS
# ------------------------------------------------------------
def menu_interactivo_view(page: ft.Page, nombre: str, cliente_id: int | None = None):
    # ---- Estilo general / tipografía (mejora de fuentes) ----
    page.bgcolor = "#FFF3E8"
    page.padding = 0

    # Tipografía coherente (sin depender de fuentes externas)
    page.theme = ft.Theme(font_family="Roboto")
    page.theme_mode = ft.ThemeMode.LIGHT

    # Jerarquía tipográfica
    TITLE = 16
    SUB = 12
    BODY = 13
    SMALL = 11

    cliente_id = cliente_id or 1
    MESA_FIJA = 1  # tu BD requiere NumeroMesa

    # ------------------------------------------------------------
    # MENÚ FIJO (no BD)
    # ------------------------------------------------------------
    bebidas = [
        {"id": 1, "nombre": "Té Boba Fresa", "precio": 59.0, "descripcion": "Té con leche + tapioca sabor fresa.", "categoria": "Boba Tea"},
        {"id": 2, "nombre": "Té Boba Mango", "precio": 59.0, "descripcion": "Tropical, dulce y refrescante.", "categoria": "Boba Tea"},
        {"id": 3, "nombre": "Taro Milk Tea", "precio": 65.0, "descripcion": "Cremoso y clásico sabor taro.", "categoria": "Boba Tea"},
        {"id": 4, "nombre": "Matcha Latte", "precio": 69.0, "descripcion": "Matcha suave con leche.", "categoria": "Especialidad"},
        {"id": 5, "nombre": "Chocolate Boba", "precio": 67.0, "descripcion": "Chocolate intenso con tapioca.", "categoria": "Clásicos"},
        {"id": 6, "nombre": "Smoothie Frutos Rojos", "precio": 72.0, "descripcion": "Fresa, zarzamora y arándano.", "categoria": "Smoothies"},
        {"id": 7, "nombre": "Smoothie Mango", "precio": 72.0, "descripcion": "Mango natural bien frío.", "categoria": "Smoothies"},
        {"id": 8, "nombre": "Frappé Vainilla", "precio": 74.0, "descripcion": "Cremoso con toque de vainilla.", "categoria": "Frappés"},
        {"id": 9, "nombre": "Frappé Mocha", "precio": 76.0, "descripcion": "Café + chocolate, energía total.", "categoria": "Frappés"},
        {"id": 10, "nombre": "Soda Italiana Limón", "precio": 49.0, "descripcion": "Burbujeante y súper fresca.", "categoria": "Refrescos"},
    ]

    # ------------------------------------------------------------
    # ESTADO
    # ------------------------------------------------------------
    cart: dict[str, dict] = {}  # key -> {"nombre","precio","qty","prep"}
    last_pedido_id: int | None = None

    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------
    def money(x: float) -> str:
        try:
            return f"${float(x):,.2f}"
        except Exception:
            return "$0.00"

    def safe_text(s: str, max_len=70):
        s = (s or "").strip()
        return s if len(s) <= max_len else s[: max_len - 1] + "…"

    def snack(msg, ok=True):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg, size=BODY, color="white"),
            bgcolor=("#2ecc71" if ok else "#e74c3c"),
        )
        page.snack_bar.open = True
        page.update()

    def prep_to_text(prep: dict) -> str:
        parts = []
        if prep.get("tamano"): parts.append(f"Tamaño: {prep['tamano']}")
        if prep.get("azucar") is not None: parts.append(f"Azúcar: {prep['azucar']}%")
        if prep.get("hielo") is not None: parts.append(f"Hielo: {prep['hielo']}%")
        if prep.get("leche"): parts.append(f"Leche: {prep['leche']}")
        tops = prep.get("toppings") or []
        if tops: parts.append("Extras: " + ", ".join(tops))
        notas = (prep.get("notas") or "").strip()
        if notas: parts.append(f"Notas: {safe_text(notas, 60)}")
        return " | ".join(parts) if parts else "Preparación estándar"

    def make_cart_key(nombre_bebida: str, prep: dict) -> str:
        tops = tuple(sorted(prep.get("toppings") or []))
        key = (
            nombre_bebida.strip().lower(),
            prep.get("tamano", ""),
            prep.get("azucar", ""),
            prep.get("hielo", ""),
            prep.get("leche", ""),
            tops,
            (prep.get("notas") or "").strip().lower(),
        )
        return str(key)

    def calc_total():
        return sum(float(it["precio"]) * int(it["qty"]) for it in cart.values())

    # ------------------------------------------------------------
    # BD
    # ------------------------------------------------------------
    def insert_pedido(producto_texto: str, total: float) -> int:
        conn = get_connection()
        cur = conn.cursor()

        fecha = datetime.now().date()
        hora = datetime.now().time().replace(microsecond=0)

        estatus_id = 3
        estatus_txt = "Pedido Realizado"

        cur.execute("""
            INSERT INTO generarpedido
            (HoraPedido, FechaPedido, Producto, Total, NumeroMesa, Estatus, EstatusPedido_IdEstatusPedido, Clientes_Idcliente)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (hora, fecha, producto_texto, total, MESA_FIJA, estatus_txt, estatus_id, cliente_id))

        pedido_id = cur.lastrowid

        # recibo (si tu tabla existe)
        try:
            cur.execute("""
                INSERT INTO recibospedidos (Producto, Total, Fecha, Hora, Usuario)
                VALUES (%s,%s,%s,%s,%s)
            """, (producto_texto, total, fecha, hora, nombre))
        except Exception:
            pass

        conn.commit()
        cur.close()
        conn.close()
        return int(pedido_id)

    def db_get_pedido(pedido_id: int):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT IdGenerarPedido, HoraPedido, FechaPedido, Producto, Total, Estatus
                FROM generarpedido
                WHERE IdGenerarPedido=%s AND Clientes_Idcliente=%s
            """, (pedido_id, cliente_id))
            row = cur.fetchone()
            cur.close()
            conn.close()
            return row
        except Exception:
            return None

    def db_historial(limit=25):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT IdGenerarPedido, HoraPedido, FechaPedido, Producto, Total, Estatus
                FROM generarpedido
                WHERE Clientes_Idcliente=%s
                ORDER BY IdGenerarPedido DESC
                LIMIT %s
            """, (cliente_id, limit))
            rows = cur.fetchall() or []
            cur.close()
            conn.close()
            return rows
        except Exception:
            return []

    # ------------------------------------------------------------
    # DIALOG HELPERS
    # ------------------------------------------------------------
    def close_dialog(dlg: ft.AlertDialog):
        dlg.open = False
        page.update()

    def open_dialog(dlg: ft.AlertDialog):
        if hasattr(page, "open"):
            page.open(dlg)
        else:
            page.dialog = dlg
            dlg.open = True
            page.update()

    def fancy_chip(text: str, bgcolor: str):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
            border_radius=999,
            bgcolor=bgcolor,
            content=ft.Text(text, size=SMALL, weight=ft.FontWeight.BOLD, color="#2C2C2C"),
        )

    # ------------------------------------------------------------
    # UI - HEADER
    # ------------------------------------------------------------
    header = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
        bgcolor="#FFF0FA",
        border=ft.border.only(bottom=ft.border.BorderSide(1, "#F0E3FF")),
        content=ft.Row(
            [
                ft.Container(
                    width=44,
                    height=44,
                    border_radius=16,
                    bgcolor="#C86DD7",
                    alignment=ALIGN_CENTER,
                    content=ft.Text("CB", color="white", weight=ft.FontWeight.BOLD, size=14),
                ),
                ft.Column(
                    [
                        ft.Text("Corallie Bubble", size=TITLE, weight=ft.FontWeight.BOLD, color="#2C2C2C"),
                        ft.Text(f"Hola, {nombre}", size=SUB, color="#666"),
                    ],
                    spacing=1,
                    expand=True,
                ),
                _iconbtn("SHOPPING_CART", "🛒", icon_color="#6C2BD9", tooltip="Carrito", on_click=lambda e: set_tab("carrito")),
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    # ------------------------------------------------------------
    # BUSCADOR
    # ------------------------------------------------------------
    txt_search = ft.TextField(
        hint_text="Buscar bebida…",
        prefix=_iconctrl("SEARCH", "🔎", size=18, color="#6C2BD9"),
        border_radius=18,
        height=46,
        bgcolor="white",
        filled=True,
        text_size=14,
    )

    # Tabs containers
    tab_menu_btn = ft.Container()
    tab_carrito_btn = ft.Container()
    tab_hist_btn = ft.Container()
    tab_estado_btn = ft.Container()

    # Views containers
    menu_list = ft.Column(spacing=12, expand=True, scroll=ft.ScrollMode.AUTO)
    carrito_list = ft.Column(spacing=12, expand=True, scroll=ft.ScrollMode.AUTO)
    historial_list = ft.Column(spacing=12, expand=True, scroll=ft.ScrollMode.AUTO)
    estado_panel = ft.Column(spacing=12, expand=True, scroll=ft.ScrollMode.AUTO)

    main_switcher = ft.AnimatedSwitcher(
        content=menu_list,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=220,
        reverse_duration=180,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
        expand=True,
    )

    lbl_total = ft.Text("Total: $0.00", size=14, weight=ft.FontWeight.BOLD, color="#2C2C2C")

    def refresh_total_ui():
        lbl_total.value = f"Total: {money(calc_total())}"
        page.update()

    # ------------------------------------------------------------
    # CARRITO
    # ------------------------------------------------------------
    def change_qty(key: str, delta: int):
        if key not in cart:
            return
        cart[key]["qty"] += delta
        if cart[key]["qty"] <= 0:
            cart.pop(key)
        build_carrito()
        refresh_total_ui()

    def remove_item(key: str):
        if key in cart:
            cart.pop(key)
        build_carrito()
        refresh_total_ui()

    def build_carrito():
        carrito_list.controls.clear()

        if not cart:
            carrito_list.controls.append(
                ft.Container(
                    padding=16,
                    border_radius=18,
                    bgcolor="white",
                    border=ft.border.all(1, "#F0E3FF"),
                    content=ft.Row(
                        [ft.Text("🛒", size=18), ft.Text("Tu carrito está vacío.", size=BODY, color="#444")],
                        spacing=10,
                    ),
                )
            )
            return

        for key, it in cart.items():
            carrito_list.controls.append(
                ft.Container(
                    bgcolor="white",
                    border_radius=18,
                    border=ft.border.all(1, "#F0E3FF"),
                    padding=14,
                    animate=ft.animation.Animation(220, ft.AnimationCurve.EASE_OUT),
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(it["nombre"], weight=ft.FontWeight.BOLD, size=BODY, expand=True, color="#2C2C2C"),
                                    ft.Text(money(it["precio"]), size=SUB, color="#6C2BD9", weight=ft.FontWeight.BOLD),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(safe_text(prep_to_text(it.get("prep") or {}), 120), size=SMALL, color="#666"),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            _iconbtn("REMOVE", "➖", icon_size=18, on_click=lambda e, k=key: change_qty(k, -1)),
                                            ft.Text(str(it["qty"]), width=24, text_align=ft.TextAlign.CENTER, size=BODY),
                                            _iconbtn("ADD", "➕", icon_size=18, on_click=lambda e, k=key: change_qty(k, +1)),
                                        ],
                                        spacing=0,
                                    ),
                                    _iconbtn("DELETE_OUTLINE", "🗑️", on_click=lambda e, k=key: remove_item(k)),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=8,
                    ),
                )
            )

    # ------------------------------------------------------------
    # PERSONALIZACIÓN (DIALOG)
    # ------------------------------------------------------------
    def open_prepare(item: dict):
        nombre_prod = item["nombre"]
        precio_base = float(item["precio"])
        desc = item.get("descripcion", "")

        dd_tamano = ft.Dropdown(
            label="Tamaño",
            value="Mediano",
            options=[ft.dropdown.Option("Chico"), ft.dropdown.Option("Mediano"), ft.dropdown.Option("Grande")],
        )

        s_azucar = ft.Slider(min=0, max=100, divisions=10, value=70, label="{value}%")
        s_hielo = ft.Slider(min=0, max=100, divisions=10, value=70, label="{value}%")

        dd_leche = ft.Dropdown(
            label="Tipo de leche",
            value="Entera",
            options=[
                ft.dropdown.Option("Entera"),
                ft.dropdown.Option("Deslactosada"),
                ft.dropdown.Option("Almendra"),
                ft.dropdown.Option("Avena"),
                ft.dropdown.Option("Soya"),
                ft.dropdown.Option("Sin leche"),
            ],
        )

        extras = [("Boba extra", 6), ("Jelly", 6), ("Popping boba", 8), ("Crema", 5), ("Chispas", 5)]
        cb = {t: ft.Checkbox(label=f"{t}  (+{p})", value=False) for t, p in extras}

        txt_notas = ft.TextField(
            label="Indicaciones",
            hint_text="Ej. sin hielo, más dulce, extra boba…",
            multiline=True,
            min_lines=2,
            max_lines=3,
        )

        lbl_precio = ft.Text(money(precio_base), weight=ft.FontWeight.BOLD, color="#6C2BD9", size=BODY)

        def calc_delta():
            delta = 0.0
            if dd_tamano.value == "Grande":
                delta += 10
            elif dd_tamano.value == "Chico":
                delta -= 5
            for t, p in extras:
                if cb[t].value:
                    delta += float(p)
            return delta

        def refresh_price(_=None):
            final = max(0.0, precio_base + calc_delta())
            lbl_precio.value = money(final)
            page.update()

        dd_tamano.on_change = refresh_price
        dd_leche.on_change = refresh_price
        for t, _p in extras:
            cb[t].on_change = refresh_price

        def add_confirm(_e):
            prep = {
                "tamano": dd_tamano.value,
                "azucar": int(s_azucar.value),
                "hielo": int(s_hielo.value),
                "leche": dd_leche.value,
                "toppings": [t for t, _p in extras if cb[t].value],
                "notas": txt_notas.value or "",
            }

            precio_final = max(0.0, precio_base + calc_delta())
            key = make_cart_key(nombre_prod, prep)

            if key not in cart:
                cart[key] = {"nombre": nombre_prod, "precio": float(precio_final), "qty": 1, "prep": prep}
            else:
                cart[key]["qty"] += 1

            build_carrito()
            refresh_total_ui()
            close_dialog(prepare_dlg)
            snack(f"Agregado: {nombre_prod}")

        anim_wrap = ft.AnimatedSwitcher(
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=220,
            switch_in_curve=ft.AnimationCurve.EASE_OUT_BACK,
            switch_out_curve=ft.AnimationCurve.EASE_IN,
            content=ft.Container(
                padding=14,
                border_radius=18,
                bgcolor="#FFF7FF",
                border=ft.border.all(1, "#F0E3FF"),
                content=ft.Column(
                    [
                        ft.Row([dd_tamano, dd_leche], spacing=10),
                        ft.Text("Azúcar", weight=ft.FontWeight.BOLD, size=SUB),
                        s_azucar,
                        ft.Text("Hielo", weight=ft.FontWeight.BOLD, size=SUB),
                        s_hielo,
                        ft.Divider(height=10),
                        ft.Text("Extras", weight=ft.FontWeight.BOLD, size=SUB),
                        ft.Column([cb[t] for t, _p in extras], spacing=2),
                        txt_notas,
                    ],
                    spacing=10,
                    tight=True,
                ),
            ),
        )

        prepare_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Container(
                        width=42,
                        height=42,
                        border_radius=16,
                        bgcolor="#FFE0F0",
                        alignment=ALIGN_CENTER,
                        content=ft.Text("🧋", size=20),
                    ),
                    ft.Column(
                        [
                            ft.Text(nombre_prod, weight=ft.FontWeight.BOLD, size=BODY),
                            ft.Text(safe_text(desc, 90), size=SUB, color="#666"),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                        border_radius=999,
                        bgcolor="#F7F2FF",
                        content=lbl_precio,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(width=520, content=anim_wrap),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog(prepare_dlg)),
                ft.ElevatedButton(
                    "Agregar",
                    icon=_icon("ADD_SHOPPING_CART_OUTLINED", "add_shopping_cart"),
                    bgcolor="#C86DD7",
                    color="white",
                    on_click=add_confirm,
                ),
            ],
        )

        refresh_price()
        open_dialog(prepare_dlg)

    # ------------------------------------------------------------
    # CARD DEL MENÚ
    # ------------------------------------------------------------
    def menu_card(item):
        nombre_prod = item["nombre"]
        precio = float(item["precio"])
        desc = item.get("descripcion", "")

        return ft.Container(
            bgcolor="white",
            border_radius=18,
            border=ft.border.all(1, "#F0E3FF"),
            padding=14,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                width=54,
                                height=54,
                                border_radius=16,
                                bgcolor="#FFE0F0",
                                alignment=ALIGN_CENTER,
                                content=ft.Text("🧋", size=22),
                            ),
                            ft.Column(
                                [
                                    ft.Text(nombre_prod, size=15, weight=ft.FontWeight.BOLD, color="#2C2C2C"),
                                    ft.Text(
                                        safe_text(desc, 80),
                                        size=SUB,
                                        color="#444",
                                        max_lines=2,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                border_radius=999,
                                bgcolor="#F7F2FF",
                                padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                content=ft.Text(money(precio), weight=ft.FontWeight.BOLD, color="#6C2BD9", size=BODY),
                            ),
                            ft.ElevatedButton(
                                "Personalizar",
                                icon=_icon("TUNE", "tune"),
                                bgcolor="#C86DD7",
                                color="white",
                                on_click=lambda e, it=item: open_prepare(it),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=10,
            ),
        )

    # ------------------------------------------------------------
    # RENDER MENÚ
    # ------------------------------------------------------------
    def render_menu():
        q = (txt_search.value or "").strip().lower()
        menu_list.controls.clear()

        filtered = [b for b in bebidas if (not q) or (q in b["nombre"].lower()) or (q in (b.get("descripcion", "").lower()))]

        if not filtered:
            menu_list.controls.append(
                ft.Container(
                    padding=16,
                    border_radius=16,
                    bgcolor="white",
                    border=ft.border.all(1, "#F0E3FF"),
                    content=ft.Row(
                        [ft.Text("🔎", size=16), ft.Text("No encontramos bebidas.", size=BODY, color="#444")],
                        spacing=10,
                    ),
                )
            )
        else:
            for item in filtered:
                menu_list.controls.append(menu_card(item))

        page.update()

    txt_search.on_change = lambda e: render_menu()

    # ------------------------------------------------------------
    # ESTADO + HISTORIAL
    # ------------------------------------------------------------
    def build_estado():
        estado_panel.controls.clear()

        if not last_pedido_id:
            estado_panel.controls.append(
                ft.Container(
                    padding=16,
                    border_radius=18,
                    bgcolor="white",
                    border=ft.border.all(1, "#F0E3FF"),
                    content=ft.Row(
                        [ft.Text("🧾", size=18), ft.Text("Aún no has realizado pedidos.", size=BODY, color="#444")],
                        spacing=10,
                    ),
                )
            )
            return

        row = db_get_pedido(last_pedido_id)
        if not row:
            estado_panel.controls.append(
                ft.Container(
                    padding=16,
                    border_radius=18,
                    bgcolor="white",
                    border=ft.border.all(1, "#F0E3FF"),
                    content=ft.Row(
                        [ft.Text("⚠️", size=18), ft.Text("No se pudo cargar el estatus.", size=BODY, color="#444")],
                        spacing=10,
                    ),
                )
            )
            return

        est = (row.get("Estatus") or "Pedido").strip()
        chip_bg = "#F7F2FF"
        if "pag" in est.lower():
            chip_bg = "#D7FFE8"
        elif "realiz" in est.lower():
            chip_bg = "#FFE7D6"

        estado_panel.controls.append(
            ft.Container(
                padding=16,
                border_radius=18,
                bgcolor="white",
                border=ft.border.all(1, "#F0E3FF"),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(f"Pedido #{row['IdGenerarPedido']}", weight=ft.FontWeight.BOLD, size=15, expand=True),
                                fancy_chip(est, chip_bg),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(f"Fecha: {row.get('FechaPedido')}  Hora: {row.get('HoraPedido')}", size=SUB, color="#666"),
                        ft.Text(f"Total: {money(row.get('Total') or 0)}", size=BODY, weight=ft.FontWeight.BOLD, color="#6C2BD9"),
                        ft.Divider(height=10),
                        ft.Text("Detalle:", size=SUB, weight=ft.FontWeight.BOLD),
                        ft.Text(safe_text(row.get("Producto") or "", 260), size=SUB, color="#444"),
                        ft.Row(
                            [
                                ft.OutlinedButton("Actualizar", icon=_icon("REFRESH", "refresh"), on_click=lambda e: (build_estado(), page.update())),
                                ft.ElevatedButton("Ver historial", icon=_icon("HISTORY", "history"), bgcolor="#C86DD7", color="white",
                                                  on_click=lambda e: set_tab("historial")),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                    spacing=8,
                ),
            )
        )

    def open_detalle_pedido(row: dict):
        est = (row.get("Estatus") or "").strip()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Text(f"Pedido #{row.get('IdGenerarPedido')}", weight=ft.FontWeight.BOLD, size=BODY),
                    fancy_chip(est or "—", "#F7F2FF"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(
                width=520,
                content=ft.Column(
                    [
                        ft.Text(f"Fecha: {row.get('FechaPedido')}  Hora: {row.get('HoraPedido')}", size=SUB, color="#666"),
                        ft.Text(f"Total: {money(row.get('Total') or 0)}", size=BODY, weight=ft.FontWeight.BOLD, color="#6C2BD9"),
                        ft.Divider(height=10),
                        ft.Text(row.get("Producto") or "", size=SUB),
                    ],
                    spacing=10,
                    tight=True,
                ),
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: close_dialog(dlg))],
        )
        open_dialog(dlg)

    def build_historial():
        historial_list.controls.clear()
        rows = db_historial(limit=30)

        if not rows:
            historial_list.controls.append(
                ft.Container(
                    padding=16,
                    border_radius=18,
                    bgcolor="white",
                    border=ft.border.all(1, "#F0E3FF"),
                    content=ft.Row(
                        [ft.Text("📭", size=18), ft.Text("Sin historial por ahora.", size=BODY, color="#444")],
                        spacing=10,
                    ),
                )
            )
            return

        for r in rows:
            est = (r.get("Estatus") or "Pedido").strip()
            chip_bg = "#F7F2FF"
            if "pag" in est.lower():
                chip_bg = "#D7FFE8"
            elif "realiz" in est.lower():
                chip_bg = "#FFE7D6"

            historial_list.controls.append(
                ft.Container(
                    padding=14,
                    border_radius=18,
                    bgcolor="white",
                    border=ft.border.all(1, "#F0E3FF"),
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"Pedido #{r.get('IdGenerarPedido')}", weight=ft.FontWeight.BOLD, size=BODY, expand=True),
                                    fancy_chip(est, chip_bg),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(f"{r.get('FechaPedido')}  {r.get('HoraPedido')}", size=SUB, color="#666"),
                            ft.Row(
                                [
                                    ft.Text(money(r.get("Total") or 0), weight=ft.FontWeight.BOLD, color="#6C2BD9", size=BODY),
                                    ft.TextButton("Ver detalle", on_click=lambda e, row=r: open_detalle_pedido(row)),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=6,
                    ),
                )
            )

    # ------------------------------------------------------------
    # CHECKOUT
    # ------------------------------------------------------------
    def checkout():
        nonlocal last_pedido_id
        if not cart:
            snack("Tu pedido está vacío.", ok=False)
            return

        lineas = [f"{it['nombre']} (x{it['qty']}) [{prep_to_text(it.get('prep') or {})}]" for it in cart.values()]
        producto_texto = " / ".join(lineas)
        total = calc_total()

        try:
            pedido_id = insert_pedido(producto_texto, total)
        except Exception as ex:
            snack(f"Error al guardar pedido: {ex}", ok=False)
            return

        last_pedido_id = pedido_id
        cart.clear()
        build_carrito()
        refresh_total_ui()
        snack(f"Pedido enviado ✅ (ID {pedido_id})")
        set_tab("estado")

    # ------------------------------------------------------------
    # TABS
    # ------------------------------------------------------------
    current_tab = {"value": "menu"}

    def tab_button(title: str, icon_name: str, emoji: str, tab_key: str):
        def on_click(_e):
            set_tab(tab_key)

        return ft.Container(
            border_radius=16,
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            animate=ft.animation.Animation(180, ft.AnimationCurve.EASE_OUT),
            on_click=on_click,
            content=ft.Row(
                [ _iconctrl(icon_name, emoji, size=18, color="#6C2BD9"), ft.Text(title, size=SUB, weight=ft.FontWeight.BOLD)],
                spacing=6,
                tight=True,
            ),
        )

    tab_menu_btn.content = tab_button("Menú", "MENU_BOOK", "📋", "menu")
    tab_carrito_btn.content = tab_button("Carrito", "SHOPPING_CART", "🛒", "carrito")
    tab_hist_btn.content = tab_button("Historial", "HISTORY", "🕘", "historial")
    tab_estado_btn.content = tab_button("Estado", "RECEIPT_LONG", "🧾", "estado")

    def paint_tabs():
        def style(btn_container: ft.Container, active: bool):
            b = btn_container.content
            b.bgcolor = "#C86DD7" if active else "white"
            b.border = ft.border.all(1, "#C86DD7" if active else "#F0E3FF")
            row = b.content
            row.controls[0].color = "white" if active else "#6C2BD9"
            row.controls[1].color = "white" if active else "#2C2C2C"

        style(tab_menu_btn, current_tab["value"] == "menu")
        style(tab_carrito_btn, current_tab["value"] == "carrito")
        style(tab_hist_btn, current_tab["value"] == "historial")
        style(tab_estado_btn, current_tab["value"] == "estado")

    def set_tab(tab_key: str):
        current_tab["value"] = tab_key

        if tab_key == "menu":
            main_switcher.content = menu_list
        elif tab_key == "carrito":
            build_carrito()
            main_switcher.content = carrito_list
        elif tab_key == "historial":
            build_historial()
            main_switcher.content = historial_list
        elif tab_key == "estado":
            build_estado()
            main_switcher.content = estado_panel

        paint_tabs()
        page.update()

    # ------------------------------------------------------------
    # AUTO-REFRESH ESTADO (cada 3s)
    # ------------------------------------------------------------
    async def _estado_poller():
        while True:
            await asyncio.sleep(3)
            if current_tab["value"] == "estado" and last_pedido_id:
                try:
                    build_estado()
                    page.update()
                except Exception:
                    pass

    def start_poller():
        if not hasattr(page, "run_task"):
            return
        try:
            if inspect.iscoroutinefunction(_estado_poller):
                try:
                    page.run_task(_estado_poller)
                except TypeError:
                    page.run_task(_estado_poller())
            else:
                page.run_task(_estado_poller())
        except Exception:
            pass

    start_poller()

    # ------------------------------------------------------------
    # BARRA INFERIOR
    # ------------------------------------------------------------
    bottom_bar = ft.Container(
        padding=ft.padding.symmetric(horizontal=14, vertical=12),
        bgcolor="#FFF0FA",
        border=ft.border.only(top=ft.border.BorderSide(1, "#F0E3FF")),
        content=ft.Row(
            [
                ft.Column([ft.Text("Tu pedido", size=SUB, color="#666"), lbl_total], spacing=2, expand=True),
                ft.ElevatedButton(
                    "Enviar",
                    bgcolor="#C86DD7",
                    color="white",
                    on_click=lambda e: checkout(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    # ------------------------------------------------------------
    # LAYOUT (marco móvil)
    # ------------------------------------------------------------
    tabs_row = ft.Row(
        [tab_menu_btn, tab_carrito_btn, tab_hist_btn, tab_estado_btn],
        spacing=10,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    mobile_frame = ft.Container(
        alignment=ALIGN_TOP_CENTER,
        expand=True,
        content=ft.Container(
            width=520,
            expand=True,
            padding=ft.padding.symmetric(horizontal=14, vertical=14),
            content=ft.Column(
                [
                    tabs_row,
                    ft.Container(height=8),
                    txt_search,
                    ft.Container(height=6),
                    ft.Container(expand=True, content=main_switcher),
                ],
                expand=True,
                spacing=10,
            ),
        ),
    )

    root = ft.Column([header, mobile_frame, bottom_bar], spacing=0, expand=True)

    # Inicial
    render_menu()
    build_carrito()
    refresh_total_ui()
    set_tab("menu")

    return ft.View(route="/menu", controls=[root])