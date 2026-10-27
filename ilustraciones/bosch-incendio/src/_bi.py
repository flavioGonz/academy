"""Ayudas de dibujo propias del curso Bosch Incendio (copiadas del esquema de HikCentral). No modifica ilus.py: solo suma piezas.

Kicker sin número de lección ("Bosch Incendio" o "Bosch Incendio · Paso N") para que las imágenes
sigan siendo correctas si el curso se reordena por módulos.
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, wrap, e, Node  # noqa

OUT = "/home/claude/ies-training/ilustraciones/bosch-incendio/"


def K(paso=None):
    return "Bosch Incendio" + (f" · Paso {paso}" if paso else "")


def save(c, name):
    return c.save(OUT + name)


KC = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
      "gray": (WHITE, INK3), "cyan": (WHITE, CYAN), "soft": (SOFT, BLUE), "dark": (DEEP, CYAN)}


def panel(x, y, w, h, title=None, kind="info", sub=None, title_size=18):
    """Tarjeta con borde de color y título arriba a la izquierda."""
    bg, fg = KC[kind]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{fg if kind not in ("info",) else LINE2}" stroke-width="2"/>']
    if title:
        col = WHITE if kind == "dark" else (fg if kind not in ("info", "soft", "gray", "cyan") else INK)
        out.append(text(x + 20, y + 32, title, title_size, 600, col, FD))
    if sub:
        out.append(text(x + 20, y + 56, sub, 15, 400, "#9FC3E3" if kind == "dark" else INK3, FM))
    return "".join(out)


def pill(x, y, s, fg=BLUE, bg=WHITE, size=15, mono=True, anchor="middle", bold=600):
    """Etiqueta con borde (como las de los cables). y = línea base del texto."""
    w = len(s) * (size * (0.6 if mono else 0.52)) + 24
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<rect x="{x0:.1f}" y="{y - size - 5:.1f}" width="{w:.1f}" height="{size + 13}" rx="{(size + 13) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, bold, fg, FM if mono else FB, anchor="middle"))


def code(x, y, w, s, size=15, color="#D9E9F8", h=40):
    """Línea de código o menú sobre fondo oscuro."""
    s = s.replace("  ", "\u00a0\u00a0")  # respeta espacios dobles en SVG
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03213C"/>' + text(x + 16, y + h / 2 + size * 0.35, s, size, 500, color, FM)


def codebox(x, y, w, lines, size=15, lh=26, title=None):
    """Bloque de código de varias líneas. lines: str o (str, color)."""
    top = 30 if title else 14
    h = top + len(lines) * lh + 10
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#03213C"/>']
    if title:
        out.append(text(x + 16, y + 22, title, 13, 500, "#7FA6C9", FM, ls=1.5))
    for i, ln in enumerate(lines):
        s, col = (ln, "#D9E9F8") if isinstance(ln, str) else ln
        s = "\u00a0" * (len(s) - len(s.lstrip(" "))) + s.lstrip(" ")  # sangría visible en SVG
        out.append(text(x + 16, y + top + 4 + (i + 0.6) * lh, s, size, 500, col, FM))
    return "".join(out), h


def wire(points, kind="data", arrow=False, dash=None):
    """Cable poligonal (codos rectos) por una lista de puntos."""
    col, sw, d0 = Cable.STY[kind]
    dash = dash or d0
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    mk = {BLUE: "a-blue", CYAN: "a-cyan", INK3: "a-gray", OK: "a-ok", ALERT: "a-alert"}.get(col, "a-blue")
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + (f' marker-end="url(#{mk})"' if arrow else "") + "/>"
    if kind in ("data", "power+", "power-", "relay") and not arrow:
        (x1, y1), (x2, y2) = points[0], points[-1]
        s += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="4.5" fill="{col}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="4.5" fill="{col}"/>'
    return s


def icon(x, y, name, color=BLUE, scale=1.2, sw=1.8):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'


def lifeline(x, y1, y2, title, sub=None, w=190):
    """Columna de un diagrama de secuencia."""
    out = [f'<rect x="{x - w / 2}" y="{y1}" width="{w}" height="{62 if sub else 48}" rx="12" fill="{DEEP}"/>',
           text(x, y1 + (27 if sub else 30), title, 17, 600, WHITE, FB, anchor="middle")]
    if sub:
        out.append(text(x, y1 + 49, sub, 14, 400, "#9FC3E3", FM, anchor="middle"))
    top = y1 + (62 if sub else 48)
    out.append(f'<path d="M{x} {top}V{y2}" stroke="{LINE2}" stroke-width="2" stroke-dasharray="6 6"/>')
    return "".join(out)


def msg(x1, x2, y, label, kind="flow", above=True, size=15, color=None):
    """Flecha horizontal de un diagrama de secuencia con texto encima."""
    col = color or {"flow": BLUE, "ok": OK, "alert": ALERT, "logical": INK3, "relay": CYAN, "warn": WARN}[kind]
    mk = {BLUE: "a-blue", OK: "a-ok", ALERT: "a-alert", INK3: "a-gray", CYAN: "a-cyan", WARN: "a-gray"}[col]
    dash = ' stroke-dasharray="8 6"' if kind == "logical" else ""
    xe = x2 - 6 if x2 > x1 else x2 + 6
    return (f'<path d="M{x1} {y}H{xe}" stroke="{col}" stroke-width="3"{dash} marker-end="url(#{mk})"/>'
            + text((x1 + x2) / 2, y - 10 if above else y + 22, label, size, 600, col, FM, anchor="middle"))


def bullet_list(x, y, items, w, size=16, gap=10, color=INK2):
    """Lista con viñetas cortas. items: str o (str, kind) con kind ok/alert/warn para el punto."""
    out, yy = [], y
    for it in items:
        s, kd = (it, "info") if isinstance(it, str) else it
        col = {"info": CYAN, "ok": OK, "alert": ALERT, "warn": WARN}[kd]
        out.append(f'<circle cx="{x + 5}" cy="{yy - size * 0.33:.1f}" r="4.5" fill="{col}"/>')
        svg, hh = wrap(x + 20, yy, s, w - 20, size, 400, color)
        out.append(svg)
        yy += hh + gap
    return "".join(out), yy


def arrow(a, b, kind="flow", label=None, **kw):
    return Cable(a, b, kind=kind, label=label, arrow=True, **kw)


def box(x, y, w, h, title, lines=(), kind="info", title_size=18, size=15, mono=False, lh=None):
    """Tarjeta con título y líneas cortas debajo."""
    out = [panel(x, y, w, h, title, kind, title_size=title_size)]
    lh = lh or size * 1.45
    for i, s in enumerate(lines):
        if isinstance(s, tuple):
            s, col = s
        else:
            col = INK2 if kind != "dark" else "#D9E9F8"
        out.append(text(x + 20, y + 62 + i * lh, s, size, 500 if mono else 400, col, FM if mono else FB))
    return "".join(out)


def tag(x, y, s, kind="info", size=15, mono=True, anchor="middle"):
    """Chip de color con significado. kind: info|ok|warn|alert|gray|dark|cyan."""
    bg, fg = {"info": (SOFT, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT),
              "gray": (WHITE, INK3), "dark": (DEEP, WHITE), "cyan": (CYAN, WHITE)}[kind]
    w = len(s) * (size * (0.6 if mono else 0.53)) + 24
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    return (f'<rect x="{x0:.1f}" y="{y - size - 6:.1f}" width="{w:.1f}" height="{size + 14}" rx="{(size + 14) / 2:.1f}" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y, s, size, 600, fg, FM if mono else FB, anchor="middle"))


def hline(x1, x2, y, color=LINE, sw=1.5):
    return f'<path d="M{x1} {y}H{x2}" stroke="{color}" stroke-width="{sw}"/>'


def rect(x, y, w, h, fill=WHITE, stroke=LINE2, rx=12, sw=2, dash=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"{d}/>'


def mid(x, y, s, size=16, weight=500, color=INK2, font=FB):
    return text(x, y, s, size, weight, color, font, anchor="middle")


def hump(xc, half, base, top, color, sw=2.5, op=0.12):
    """Campana de un canal WiFi (centro, medio ancho en px, base y tope)."""
    xl, xr = xc - half, xc + half
    return (f'<path d="M{xl:.1f} {base}C{xl + half * 0.45:.1f} {top},{xr - half * 0.45:.1f} {top},{xr:.1f} {base}" '
            f'fill="{color}" fill-opacity="{op}" stroke="{color}" stroke-width="{sw}"/>')


def badge(x, y, s, color=CYAN, r=18, size=17):
    """Círculo con una letra o número (para recorridos a, b, c o 1, 2, 3 dentro de una figura)."""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>' + text(x, y + size * 0.36, s, size, 700, WHITE, FD, anchor="middle")


def lines(x, y, items, size=16, lh=26, color=INK2, font=FB, weight=400):
    """Varias líneas sueltas, una debajo de otra. items: str o (str, color)."""
    out = []
    for i, s in enumerate(items):
        s, col = (s, color) if isinstance(s, str) else s
        out.append(text(x, y + i * lh, s, size, weight, col, font))
    return "".join(out)


# ---------------------------------------------------------------- piezas de incendio (genéricas, sin marcas)
LED = {None: LINE2, "ok": OK, "alarm": ALERT, "fault": WARN, "off": LINE, "test": CYAN}


def detector(cx, cy, r=32, title=None, sub=None, hl=None, state=None, size=16):
    """Detector puntual visto desde abajo: base, cámara y LED central. state colorea el LED."""
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHITE}" stroke="{hl or LINE2}" stroke-width="{3 if hl else 2.5}"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{r * 0.64:.1f}" fill="{SOFT}" stroke="{LINE2}" stroke-width="1.5"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{max(4, r * 0.17):.1f}" fill="{LED[state]}"/>']
    if title:
        out.append(text(cx, cy + r + 22, title, size, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(cx, cy + r + 42, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def pulsador(cx, cy, s=56, title=None, sub=None, hl=None):
    """Pulsador manual: caja cuadrada roja con ventana central."""
    x, y = cx - s / 2, cy - s / 2
    out = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="8" fill="{ALERT}" stroke="{hl or ALERT}" stroke-width="{3 if hl else 2}"/>',
           f'<rect x="{x + s * .2:.1f}" y="{y + s * .2:.1f}" width="{s * .6:.1f}" height="{s * .6:.1f}" rx="4" fill="{WHITE}"/>',
           f'<rect x="{x + s * .34:.1f}" y="{y + s * .44:.1f}" width="{s * .32:.1f}" height="{s * .12:.1f}" rx="2" fill="{ALERT}"/>']
    if title:
        out.append(text(cx, cy + s / 2 + 22, title, 16, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(cx, cy + s / 2 + 42, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def sirena(cx, cy, s=58, title=None, sub=None, hl=None, on=False):
    """Sirena con baliza: cuerpo redondeado, parlante y destello arriba. on=True dibuja ondas."""
    x, y = cx - s / 2, cy - s / 2
    out = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s * .28:.1f}" fill="{WHITE}" stroke="{hl or LINE2}" stroke-width="{3 if hl else 2.5}"/>',
           f'<rect x="{x + s * .22:.1f}" y="{y - 6:.1f}" width="{s * .56:.1f}" height="12" rx="6" fill="{ALERT if on else ALERT_BG}" stroke="{ALERT}" stroke-width="1.5"/>',
           f'<circle cx="{cx}" cy="{cy + 4}" r="{s * .22:.1f}" fill="none" stroke="{INK3}" stroke-width="2.5"/>',
           f'<circle cx="{cx}" cy="{cy + 4}" r="{s * .07:.1f}" fill="{INK3}"/>']
    if on:
        for k in (1, 2):
            rr = s * (.5 + .16 * k)
            out.append(f'<path d="M{cx + rr * .7:.1f} {cy - rr * .45:.1f}A{rr:.1f} {rr:.1f} 0 0 1 {cx + rr * .7:.1f} {cy + rr * .55:.1f}" fill="none" stroke="{ALERT}" stroke-width="2.5" stroke-linecap="round"/>')
    if title:
        out.append(text(cx, cy + s / 2 + 22, title, 16, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(cx, cy + s / 2 + 42, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def iso(x, y, closed=True, w=34, color=None):
    """Aislador entre b1 y b2: interruptor cerrado (conduce) o abierto (aisló)."""
    col = color or (INK2 if closed else ALERT)
    if closed:
        bar = f'<path d="M{x + 7} {y}H{x + w - 7}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
    else:
        bar = f'<path d="M{x + 7} {y}L{x + w - 9} {y - 12}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
    return (f'<circle cx="{x + 5}" cy="{y}" r="4.5" fill="{WHITE}" stroke="{col}" stroke-width="2.5"/>'
            f'<circle cx="{x + w - 5}" cy="{y}" r="4.5" fill="{WHITE}" stroke="{col}" stroke-width="2.5"/>' + bar)


def term(x, y, s, color=INK2, anchor="middle", below=False):
    """Borne: punto con su nombre (b1+, a−, LSN1...)."""
    return f'<circle cx="{x}" cy="{y}" r="6" fill="{WHITE}" stroke="{color}" stroke-width="2.5"/>' + text(x, y + (24 if below else -12), s, 15, 600, color, FM, anchor=anchor)


def elemento(x, y, w=150, h=92, title="Detector", sub="", hl=None, iso_closed=True, state=None, terms=True):
    """Elemento LSN genérico con aislador entre b1+ y b2+ y borne a−. Devuelve (svg, anclas)."""
    by = y + 34
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{hl or LINE2}" stroke-width="{3 if hl else 2}"/>',
           text(x + w / 2, y + h - 30, title, 16, 600, INK, FB, anchor="middle")]
    if sub:
        out.append(text(x + w / 2, y + h - 11, sub, 14, 400, INK3, FM, anchor="middle"))
    out.append(iso(x + w / 2 - 17, by, iso_closed))
    out.append(f'<path d="M{x} {by}H{x + w / 2 - 17}M{x + w / 2 + 17} {by}H{x + w}" stroke="{INK3}" stroke-width="2"/>')
    if state:
        out.append(f'<circle cx="{x + w - 16}" cy="{y + 16}" r="7" fill="{LED[state]}"/>')
    an = {"b1": (x, by), "b2": (x + w, by), "a": (x + w / 2, y + h)}
    if terms:
        out.append(text(x + 6, by - 10, "b1+", 14, 600, BLUE, FM))
        out.append(text(x + w - 6, by - 10, "b2+", 14, 600, BLUE, FM, anchor="end"))
    return "".join(out), an


def lsn_module(x, y, w=230, h=120, title="Módulo LSN", sub="LSN 1500 A", dark=True):
    """Módulo de lazo con bornes LSN1 (a− b+) a la izquierda y LSN2 (a− b+) a la derecha, abajo."""
    fill = DEEP if dark else WHITE
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{DEEP if dark else LINE2}" stroke-width="2"/>',
           text(x + 20, y + 34, title, 18, 600, WHITE if dark else INK, FD),
           text(x + 20, y + 58, sub, 15, 400, "#9FC3E3" if dark else INK3, FM)]
    yy = y + h
    an = {"LSN1_b": (x + 40, yy), "LSN1_a": (x + 80, yy), "LSN2_a": (x + w - 80, yy), "LSN2_b": (x + w - 40, yy)}
    col = "#9FC3E3" if dark else INK2
    out.append(text(x + 60, y + h - 14, "LSN1", 14, 600, col, FM, anchor="middle"))
    out.append(text(x + w - 60, y + h - 14, "LSN2", 14, 600, col, FM, anchor="middle"))
    for k, (px, py) in an.items():
        out.append(f'<circle cx="{px}" cy="{py}" r="6" fill="{WHITE}" stroke="{BLUE if k.endswith("b") else INK2}" stroke-width="2.5"/>')
    return "".join(out), an


def controlador(x, y, w=420, h=300, screen=(), title=None, labels=True, leds=None):
    """Frente del controlador del panel (esquema genérico, no a escala): pantalla táctil,
    18 LED de estado, 6 botones fijos y 3 teclas de función. screen: líneas de texto en la pantalla."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{DEEP}"/>']
    sx, sy, sw_, sh = x + 70, y + 22, w - 92, h - 104
    out.append(f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh}" rx="8" fill="{WHITE}" stroke="{CYAN}" stroke-width="2"/>')
    for i, s in enumerate(screen):
        s, col = (s, INK2) if isinstance(s, str) else s
        out.append(text(sx + 14, sy + 28 + i * 24, s, 15, 600 if i == 0 else 400, col, FM if i else FB))
    leds = leds or {}
    for i in range(9):
        for j in range(2):
            k = i * 2 + j
            col = leds.get(k, "#24496E")
            out.append(f'<circle cx="{x + 24 + j * 20}" cy="{sy + 10 + i * (sh - 16) / 8:.1f}" r="5.5" fill="{col}"/>')
    by = y + h - 62
    bw = min(36, (sw_ - 40) / 9 - 8)
    for i in range(6):
        out.append(f'<rect x="{sx + i * (bw + 8):.1f}" y="{by}" width="{bw:.1f}" height="26" rx="6" fill="#24496E" stroke="#3E6A93" stroke-width="1.5"/>')
    for i in range(3):
        out.append(f'<rect x="{sx + sw_ - bw - i * (bw + 8):.1f}" y="{by}" width="{bw:.1f}" height="26" rx="6" fill="{NAVY}" stroke="{CYAN}" stroke-width="1.5"/>')
    if title:
        out.append(text(x + w / 2, y + h - 12, title, 15, 600, "#9FC3E3", FM, anchor="middle"))
    an = {"screen": (sx + sw_ / 2, sy), "leds": (x + 34, sy + sh / 2), "fixed": (sx + 3 * (bw + 8) - 4, by + 26), "fkeys": (sx + sw_ - 1.5 * bw - 8, by + 26),
          "screen_r": (sx + sw_, sy + 30)}
    return "".join(out), an


def callout(x1, y1, x2, y2, s, color=INK2, anchor="start", size=15):
    """Línea fina de un punto (x1,y1) a una etiqueta en (x2,y2)."""
    return (f'<circle cx="{x1}" cy="{y1}" r="4" fill="{color}"/><path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="1.5"/>'
            + text(x2 + (6 if anchor == "start" else -6), y2 + 5, s, size, 600, color, FB, anchor=anchor))
