"""Ayudas de dibujo propias del curso Akuvox, lecciones 15 a 28 (relés por HTTP y porteros de calle).
No modifica ilus.py ni _akv.py: solo suma piezas. Todo genérico, sin logos ni copia de productos reales."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e  # noqa

OUT = "/home/claude/ies-training/ilustraciones/akuvox/"
GRAY_ = "#9AAFC3"


def save(c, name):
    c.items.insert(0, "<style>text{font-variant-ligatures:none;font-feature-settings:'liga' 0,'calt' 0}</style>")
    return c.save(OUT + name)


KC = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
      "gray": (WHITE, INK3), "cyan": (WHITE, CYAN), "soft": (SOFT, BLUE), "dark": (DEEP, CYAN)}


def panel(x, y, w, h, title=None, kind="info", sub=None, title_size=18):
    """Tarjeta con borde de color y título arriba a la izquierda."""
    bg, fg = KC[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{fg if kind not in ("info",) else LINE2}" stroke-width="2"/>']
    if title:
        tc = WHITE if kind == "dark" else (fg if kind not in ("info", "soft", "gray") else INK)
        out.append(text(x + 20, y + 32, title, title_size, 600, tc, FD))
    if sub:
        out.append(text(x + 20, y + 56, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def pill(x, y, s, fg=BLUE, bg=WHITE, size=15, mono=True, anchor="middle", bold=600):
    w = len(s) * (size * (0.6 if mono else 0.52)) + 24
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{x0:.1f}" y="{y - size - 5:.1f}" width="{w:.1f}" height="{size + 13}" rx="{(size + 13) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, bold, fg, FM if mono else FB, anchor="middle"))


def chipw(s, mono=True):
    return len(s) * (9.2 if mono else 8.4) + 26


def code(x, y, w, s, size=15, color="#D9E9F8", h=40):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03213C"/>' + text(x + 16, y + h / 2 + size * 0.35, s, size, 500, color, FM)


def code_parts(x, y, parts, size=16, h=44, pad=16):
    k = size * 0.6
    w = sum(len(p) for p, _ in parts) * k + 2 * pad
    out = [f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="10" fill="#03213C"/>']
    cx, spans = x + pad, []
    for p, col in parts:
        out.append(text(cx, y + h / 2 + size * 0.35, p, size, 500, col, FM))
        spans.append((cx, cx + len(p) * k))
        cx += len(p) * k
    return "".join(out), spans


def terminal(x, y, label, color=BLUE, below=True, size=14):
    ly = y + 25 if below else y - 15
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="{SOFT}" stroke="{color}" stroke-width="2"/>'
            f'<path d="M{x - 5} {y + 5}L{x + 5} {y - 5}" stroke="{color}" stroke-width="1.6"/>'
            + text(x, ly, label, size, 600, INK2, FM, anchor="middle"))


def wire(points, kind="data", arrow=False, dash=None, dots=True):
    col, sw, d0 = Cable.STY[kind]
    dash = dash or d0
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(col, "a-blue")
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + (f' marker-end="url(#{mk})"' if arrow else "") + "/>"
    if kind in ("data", "power+", "power-", "relay") and not arrow and dots:
        (x1, y1), (x2, y2) = points[0], points[-1]
        s += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="4.5" fill="{col}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="4.5" fill="{col}"/>'
    return s


def icon(x, y, name, color=BLUE, scale=1.2, sw=1.8):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'


def check(x, y, ok=True, r=13):
    """Tilde o cruz chica en círculo (para grillas)."""
    col, bg = (OK, OK_BG) if ok else (ALERT, ALERT_BG)
    p = "M-5 0.5l3.5 3.5L5.5-4.5" if ok else "M-4.5-4.5l9 9M4.5-4.5l-9 9"
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{bg}" stroke="{col}" stroke-width="1.8"/><path transform="translate({x} {y})" d="{p}" fill="none" stroke="{col}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'


def dash_mark(x, y):
    return f'<path d="M{x - 9} {y}H{x + 9}" stroke="{GRAY_}" stroke-width="3" stroke-linecap="round"/>'


def bullet_list(x, y, items, w, size=16, gap=10, color=INK2):
    out, yy = [], y
    for it in items:
        s, kd = (it, "info") if isinstance(it, str) else it
        col = {"info": CYAN, "ok": OK, "alert": ALERT, "warn": WARN}[kd]
        out.append(f'<circle cx="{x + 5}" cy="{yy - size * 0.33:.1f}" r="4.5" fill="{col}"/>')
        svg, hh = wrap(x + 20, yy, s, w - 20, size, 400, color)
        out.append(svg)
        yy += hh + gap
    return "".join(out), yy


# ------------------------------------------------------------------ portero genérico
def portero(x, y, kind="boton", s=1.0, title=None, sub=None, hl=None, title_size=18, n_botones=3, cams=1):
    """Frente de portero genérico, 150x260 a escala s. kind:
    boton | botones | teclado | pantalla | pantalla_teclado | pantalla_grande.
    Devuelve svg. Centro horizontal = x + 75*s. Título debajo."""
    W, H = 150 * s, 260 * s
    cx = x + W / 2
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{W:.1f}" height="{H:.1f}" rx="{18 * s:.1f}" fill="#26323F" stroke="{hl or DEEP}" stroke-width="{3 if hl else 2}"/>',
           ]
    for dx in ([0] if cams == 1 else [-18, 18]):
        out.append(f'<circle cx="{cx + dx * s:.1f}" cy="{y + 30 * s:.1f}" r="{12 * s:.1f}" fill="#0B1A28" stroke="#5B6F84" stroke-width="2"/><circle cx="{cx + dx * s:.1f}" cy="{y + 30 * s:.1f}" r="{4.5 * s:.1f}" fill="{CYAN}"/>')
    def R(rx, ry, rw, rh, fill="#3A4A5C", rr=6, stroke=None):
        st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
        return f'<rect x="{x + rx * s:.1f}" y="{y + ry * s:.1f}" width="{rw * s:.1f}" height="{rh * s:.1f}" rx="{rr * s:.1f}" fill="{fill}"{st}/>'
    if kind == "boton":
        out.append(R(30, 62, 90, 54, rr=8))
        out.append(f'<path d="M{x + 44 * s:.1f} {y + 84 * s:.1f}H{x + 106 * s:.1f}M{x + 44 * s:.1f} {y + 96 * s:.1f}H{x + 90 * s:.1f}" stroke="#7D90A4" stroke-width="{2.5 * s:.1f}" stroke-linecap="round"/>')
        out.append(R(46, 138, 58, 36, fill="#1E2A36", rr=6, stroke="#5B6F84"))
        out.append(f'<circle cx="{cx:.1f}" cy="{y + 214 * s:.1f}" r="{24 * s:.1f}" fill="#3A4A5C" stroke="{CYAN}" stroke-width="2.5"/>')
    elif kind == "botones":
        n = n_botones
        for i in range(n):
            yy = 62 + i * 44
            out.append(R(24, yy, 70, 32, rr=6))
            out.append(f'<path d="M{x + 34 * s:.1f} {y + (yy + 16) * s:.1f}H{x + 80 * s:.1f}" stroke="#7D90A4" stroke-width="{2.4 * s:.1f}" stroke-linecap="round"/>')
            out.append(f'<circle cx="{x + 114 * s:.1f}" cy="{y + (yy + 16) * s:.1f}" r="{13 * s:.1f}" fill="#3A4A5C" stroke="{CYAN}" stroke-width="2"/>')
        out.append(R(46, 62 + n * 44 + 8, 58, 30, fill="#1E2A36", rr=6, stroke="#5B6F84"))
    elif kind == "teclado":
        for r in range(4):
            for k in range(3):
                out.append(R(36 + k * 28, 60 + r * 26, 22, 19, rr=4))
        out.append(R(46, 176, 58, 30, fill="#1E2A36", rr=6, stroke="#5B6F84"))
        out.append(f'<circle cx="{cx:.1f}" cy="{y + 230 * s:.1f}" r="{15 * s:.1f}" fill="#3A4A5C" stroke="{CYAN}" stroke-width="2"/>')
    elif kind == "pantalla":
        out.append(R(20, 56, 110, 120, fill="#0B1A28", rr=8, stroke="#5B6F84"))
        out.append(R(46, 196, 58, 34, fill="#1E2A36", rr=6, stroke="#5B6F84"))
    elif kind == "pantalla_grande":
        out.append(R(14, 52, 122, 176, fill="#0B1A28", rr=8, stroke="#5B6F84"))
    elif kind == "pantalla_teclado":
        out.append(R(26, 54, 98, 58, fill="#0B1A28", rr=6, stroke="#5B6F84"))
        for r in range(4):
            for k in range(3):
                out.append(R(40 + k * 26, 122 + r * 24, 20, 17, rr=4))
        out.append(R(52, 222, 46, 24, fill="#1E2A36", rr=5, stroke="#5B6F84"))
    if title:
        out.append(text(cx, y + H + 26, title, title_size, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(cx, y + H + 26 + title_size + 4, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def monitor(x, y, w=240, h=160, title=None, sub=None, hl=None, screen_txt=None, keys=()):
    """Monitor interior genérico. keys = lista de etiquetas de teclas en pantalla (abajo)."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#F1F4F7" stroke="{hl or LINE2}" stroke-width="{3 if hl else 2}"/>',
           f'<rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 42}" rx="8" fill="#0B1A28"/>',
           f'<circle cx="{x + w / 2}" cy="{y + h - 14}" r="5" fill="{INK3}"/>']
    if screen_txt:
        out.append(text(x + w / 2, y + 44, screen_txt, 15, 500, "#9FC3E3", FM, anchor="middle"))
    if keys:
        kw = (w - 28 - 10 * (len(keys) + 1)) / len(keys)
        for i, (k, on) in enumerate(keys):
            kx = x + 24 + i * (kw + 10)
            out.append(f'<rect x="{kx:.1f}" y="{y + h - 72}" width="{kw:.1f}" height="34" rx="8" fill="{CYAN if on else "#24384C"}"/>')
            out.append(text(kx + kw / 2, y + h - 50, k, 15, 600, WHITE, FB, anchor="middle"))
    if title:
        out.append(text(x + w / 2, y + h + 26, title, 18, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(x + w / 2, y + h + 48, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def box(x, y, w, h, title, sub=None, kind="info", icon_name=None, title_size=18, center=False):
    """Caja simple con ícono opcional."""
    bg, fg = KC[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{bg}" stroke="{fg if kind not in ("info",) else LINE2}" stroke-width="2"/>']
    tx = x + (56 if icon_name else 18)
    if icon_name:
        out.append(icon(x + 16, y + h / 2 - 15, icon_name, CYAN if kind == "dark" else BLUE, 1.25))
    tc = WHITE if kind == "dark" else INK
    if center:
        ty = y + h / 2 + (-3 if sub else 6)
        out.append(text(x + w / 2, ty, title, title_size, 600, tc, FB, anchor="middle"))
        if sub:
            out.append(text(x + w / 2, ty + 22, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM, anchor="middle"))
    else:
        ty = y + h / 2 + (-4 if sub else 6)
        out.append(text(tx, ty, title, title_size, 600, tc, FB))
        if sub:
            out.append(text(tx, ty + 22, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def grid(x, y, models, rows, first_w=230, col_w=150, row_h=40, head_h=46, hl_cols=(), head_sub=None):
    """Grilla de características. models = [nombres]; rows = [(característica, [valor por modelo])].
    valor: True (tilde), False (cruz), None (guion = sin dato), str (texto), (str, kind) con kind ok/warn/alert."""
    W = first_w + col_w * len(models)
    H = head_h + row_h * len(rows)
    out = [f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>',
           f'<path d="M{x} {y + 14}a14 14 0 0 1 14 -14h{W - 28}a14 14 0 0 1 14 14v{head_h - 14}h-{W}z" fill="{SOFT}"/>']
    for i, m in enumerate(models):
        cx = x + first_w + col_w * i + col_w / 2
        if i in hl_cols:
            out.append(f'<rect x="{x + first_w + col_w * i + 4}" y="{y + 4}" width="{col_w - 8}" height="{H - 8}" rx="10" fill="none" stroke="{CYAN}" stroke-width="2"/>')
        out.append(text(cx, y + (head_h / 2 + 6 if not head_sub else 24), m, 17, 700, INK, FB, anchor="middle"))
        if head_sub:
            out.append(text(cx, y + 42, head_sub[i], 14, 400, INK3, FM, anchor="middle"))
    for r, (feat, vals) in enumerate(rows):
        ry = y + head_h + row_h * r
        if r:
            out.append(f'<path d="M{x + 12} {ry}H{x + W - 12}" stroke="{LINE}" stroke-width="1"/>')
        out.append(text(x + 16, ry + row_h / 2 + 6, feat, 16, 600, INK2, FB))
        for i, v in enumerate(vals):
            cx = x + first_w + col_w * i + col_w / 2
            cy = ry + row_h / 2
            if v is True:
                out.append(check(cx, cy, True))
            elif v is False:
                out.append(check(cx, cy, False))
            elif v is None:
                out.append(dash_mark(cx, cy))
            else:
                s, kd = (v, None) if isinstance(v, str) else v
                col = {None: INK, "ok": OK, "warn": WARN, "alert": ALERT, "blue": BLUE}[kd]
                out.append(text(cx, cy + 6, s, 15, 600 if kd else 500, col, FM, anchor="middle"))
    return "".join(out), W, H


def house(x, y, w=170, h=130, color=BLUE, label=None):
    """Casa genérica (contorno)."""
    out = [f'<path d="M{x} {y + h * 0.42}L{x + w / 2} {y}L{x + w} {y + h * 0.42}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>',
           f'<rect x="{x + w * 0.12}" y="{y + h * 0.38}" width="{w * 0.76}" height="{h * 0.62}" fill="{WHITE}" stroke="{color}" stroke-width="3"/>',
           f'<rect x="{x + w * 0.42}" y="{y + h * 0.62}" width="{w * 0.16}" height="{h * 0.38}" fill="{SOFT}" stroke="{color}" stroke-width="2"/>']
    if label:
        out.append(text(x + w / 2, y + h + 26, label, 17, 600, INK, FB, anchor="middle"))
    return "".join(out)


def building(x, y, w=150, h=170, floors=5, color=BLUE, label=None, tall=False):
    """Edificio genérico (contorno con ventanas)."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WHITE}" stroke="{color}" stroke-width="3"/>']
    fh = (h - 40) / floors
    for f in range(floors):
        for k in range(3):
            out.append(f'<rect x="{x + 18 + k * (w - 36) / 3 + 4:.1f}" y="{y + 12 + f * fh:.1f}" width="{(w - 36) / 3 - 8:.1f}" height="{fh - 10:.1f}" rx="2" fill="{SOFT}"/>')
    out.append(f'<rect x="{x + w / 2 - 16}" y="{y + h - 34}" width="32" height="34" fill="{SOFT}" stroke="{color}" stroke-width="2"/>')
    if label:
        out.append(text(x + w / 2, y + h + 26, label, 17, 600, INK, FB, anchor="middle"))
    return "".join(out)


def gate(x, y, w=180, h=110, color=BLUE, label=None):
    """Portón vehicular genérico (barras)."""
    out = [f'<rect x="{x}" y="{y}" width="14" height="{h}" fill="{color}"/><rect x="{x + w - 14}" y="{y}" width="14" height="{h}" fill="{color}"/>',
           f'<path d="M{x + 14} {y + 18}H{x + w - 14}M{x + 14} {y + h - 14}H{x + w - 14}" stroke="{color}" stroke-width="3"/>']
    for i in range(1, 8):
        bx = x + 14 + i * (w - 28) / 8
        out.append(f'<path d="M{bx:.1f} {y + 18}V{y + h - 14}" stroke="{color}" stroke-width="2.5"/>')
    if label:
        out.append(text(x + w / 2, y + h + 26, label, 17, 600, INK, FB, anchor="middle"))
    return "".join(out)


def tester(x, y, reading, ok=None, label=None):
    """Tester genérico (multímetro) con lectura en pantalla. Ancho 130, alto 190."""
    col = {None: INK, True: OK, False: ALERT}[ok]
    out = [f'<rect x="{x}" y="{y}" width="130" height="190" rx="16" fill="#F2C94C" stroke="{INK}" stroke-width="2"/>',
           f'<rect x="{x + 14}" y="{y + 14}" width="102" height="52" rx="6" fill="#E9F1E4" stroke="{INK}" stroke-width="1.5"/>',
           text(x + 65, y + 50, reading, 22, 700, col, FM, anchor="middle"),
           f'<circle cx="{x + 65}" cy="{y + 112}" r="26" fill="#2B2B2B"/><path d="M{x + 65} {y + 112}L{x + 65} {y + 90}" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>',
           f'<circle cx="{x + 38}" cy="{y + 164}" r="8" fill="{RED}"/><circle cx="{x + 92}" cy="{y + 164}" r="8" fill="{BLACK}"/>',
           text(x + 65, y + 150, "V DC", 14, 600, INK, FM, anchor="middle")]
    if label:
        out.append(text(x + 65, y + 216, label, 16, 600, INK, FB, anchor="middle"))
    return "".join(out)


def doc(x, y, w, h, title, lines, kind="info", stamp=None):
    """Hoja de documento (ficha o guía) con líneas de texto."""
    bg, fg = KC[kind]
    out = [f'<path d="M{x} {y}H{x + w - 26}L{x + w} {y + 26}V{y + h}H{x}z" fill="{WHITE}" stroke="{fg if kind != "info" else LINE2}" stroke-width="2"/>',
           f'<path d="M{x + w - 26} {y}V{y + 26}H{x + w}" fill="{SOFT}" stroke="{fg if kind != "info" else LINE2}" stroke-width="2"/>',
           text(x + 18, y + 34, title, 17, 600, INK, FB)]
    yy = y + 66
    for ln in lines:
        s, kd = (ln, None) if isinstance(ln, str) else ln
        col = {None: INK2, "ok": OK, "warn": WARN, "alert": ALERT, "blue": BLUE}[kd]
        out.append(text(x + 18, yy, s, 16, 600 if kd else 400, col, FM if kd else FB))
        yy += 28
    if stamp:
        out.append(pill(x + w / 2, y + h - 18, stamp, fg, bg if kind != "info" else SOFT, 15, False))
    return "".join(out)


def arrow(a, b, kind="flow", label=None, **kw):
    return Cable(a, b, kind=kind, label=label, arrow=True, **kw).svg()


def step_dot(x, y, n, color=CYAN):
    return Step(x, y, n, color).svg()


def screen_flow(x, y, steps, w=240, h=150, gap=48):
    """Secuencia de pantallas del equipo. steps = [(lo que marcás, lo que ves)]. Devuelve svg."""
    out = []
    for i, (key, shown) in enumerate(steps):
        sx = x + i * (w + gap)
        out.append(f'<rect x="{sx}" y="{y}" width="{w}" height="{h}" rx="16" fill="#26323F" stroke="{DEEP}" stroke-width="2"/>')
        out.append(f'<rect x="{sx + 14}" y="{y + 14}" width="{w - 28}" height="{h - 28}" rx="8" fill="#0B1A28"/>')
        out.append(text(sx + w / 2, y + h / 2 + 8, shown, 18, 600, "#9FE3F7", FM, anchor="middle"))
        out.append(pill(sx + w / 2, y + h + 40, key, BLUE, WHITE, 16, True))
        if i < len(steps) - 1:
            out.append(Cable((sx + w + 6, y + h / 2), (sx + w + gap - 6, y + h / 2), kind="flow", arrow=True, bend="straight").svg())
    return "".join(out)


def switch(x, y, ports=("1", "2", "3", "4"), name="Switch PoE", sub="", hl=None, w=None):
    return Router(x, y, name, sub, ports=list(ports), hl=hl or {}).svg()
