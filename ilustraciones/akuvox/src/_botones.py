"""Ayudantes propios de la lección 39 de Akuvox (configuración de botones y tipos de llamada).
No modifica ilus.py, anim.py ni los demás ayudantes: solo dibuja piezas esquemáticas y rotuladas.

mon_mini()   monitor interior chico con estado en la pantalla (sonando, atendida, rechazó, sin respuesta, reposo)
state_pill() la etiqueta de estado sola (para superponerla en una animación)
field()      una fila de formulario de la web del portero: rótulo a la izquierda, valor en un campo
web_panel()  un bloque de la web (título del bloque y ruta de menú) con filas de field()
lane()       carril con título y subtítulo para la ilustración principal

Todas devuelven fragmentos SVG que sirven en ilus.Canvas (c.add(svg)) y en anim.Anim (a.add(svg)).
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, e  # noqa

OUT = "/home/claude/ies-training/ilustraciones/akuvox/"
SCR = "#0B1A28"

# estado -> (texto, color de fondo, color de texto)
STATES = {
    "ring": ("Sonando", CYAN, WHITE),
    "ok": ("Atendida", OK, WHITE),
    "refused": ("Rechazó", ALERT, WHITE),
    "noanswer": ("Sin respuesta", WARN, WHITE),
    "idle": ("En reposo", "#2A3E52", "#9FC3E3"),
    "cut": ("Dejó de sonar", "#2A3E52", "#9FC3E3"),
    "never": ("No sonó", "#2A3E52", "#F3B1A4"),
}


def save(c, name):
    return c.save(OUT + name)


def state_pill(cx, cy, state, size=15):
    s, bg, fg = STATES[state]
    w = len(s) * size * 0.6 + 28
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - 16}" width="{w:.1f}" height="32" rx="16" fill="{bg}"/>'
            + text(cx, cy + 5.5, s, size, 600, fg, FB, anchor="middle"))


def mon_mini(x, y, title, sub="", state="idle", w=200, h=124, hl=None):
    """Monitor chico (pantalla apaisada) con el estado escrito en la pantalla. Ocupa w x (h + 46)."""
    s = STATES[state]
    stroke = hl or (s[1] if state in ("ring", "ok", "refused", "noanswer") else LINE2)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#F1F4F7" stroke="{stroke}" stroke-width="3"/>',
           f'<rect x="{x + 12}" y="{y + 12}" width="{w - 24}" height="{h - 36}" rx="7" fill="{SCR}"/>',
           f'<circle cx="{x + w / 2}" cy="{y + h - 12}" r="5" fill="{INK3}"/>',
           state_pill(x + w / 2, y + 12 + (h - 36) / 2, state)]
    out.append(text(x + w / 2, y + h + 22, title, 17, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(x + w / 2, y + h + 42, sub, 15, 500, INK3, FM, anchor="middle"))
    return "".join(out)


def field(x, y, label, value, lw=210, fw=260, kind="input", hl=False, size=15):
    """Fila de formulario: rótulo (texto) y campo (input, select o check)."""
    out = [text(x, y + 21, label, size, 500, INK2, FB)]
    fx = x + lw
    if kind == "check":
        out.append(f'<rect x="{fx}" y="{y + 6}" width="22" height="22" rx="4" fill="{BLUE}"/>'
                   f'<path d="M{fx + 5} {y + 17} l5 5 l8 -10" fill="none" stroke="{WHITE}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
        if value:
            out.append(text(fx + 34, y + 23, value, size, 500, INK3, FM))
        return "".join(out)
    out.append(f'<rect x="{fx}" y="{y}" width="{fw}" height="34" rx="6" fill="{SOFT if hl else WHITE}" stroke="{CYAN if hl else LINE2}" stroke-width="{2 if hl else 1.5}"/>')
    out.append(text(fx + 14, y + 22, value, size, 500, INK, FM))
    if kind == "select":
        out.append(f'<path d="M{fx + fw - 24} {y + 14} l7 7 l7 -7" fill="none" stroke="{INK2}" stroke-width="2"/>')
    return "".join(out)


def web_panel(x, y, w, title, path, rows, lw=200, fw=None, hl=None, gap=44):
    """Bloque de la web del portero. rows = [(rótulo, valor, kind)]; hl = índice resaltado. Devuelve (svg, alto)."""
    fw = fw or (w - lw - 48)
    h = 92 + gap * len(rows)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>',
           text(x + 24, y + 34, title, 18, 600, INK, FD),
           text(x + 24, y + 58, path, 14, 500, BLUE, FM),
           f'<path d="M{x + 16} {y + 72}H{x + w - 16}" stroke="{LINE}" stroke-width="1.5"/>']
    for i, r in enumerate(rows):
        lab, val = r[0], r[1]
        kind = r[2] if len(r) > 2 else "input"
        out.append(field(x + 24, y + 84 + i * gap, lab, val, lw, fw, kind, hl == i))
    return "".join(out), h


def lane(x, y, w, h, title, sub, kind="info"):
    bg, fg = {"info": (WHITE, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "cyan": (WHITE, CYAN)}[kind]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{LINE2}" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{y + 14}" width="5" height="{h - 28}" rx="2.5" fill="{fg}"/>'
            + text(x + 22, y + 32, title, 19, 600, INK, FD)
            + text(x + 22, y + 55, sub, 15, 500, INK3, FM))


def dot_mon(cx, cy, label, state="ring", r=26):
    """Monitor como círculo chico con número o letra y color de estado (para carriles compactos)."""
    col = {"ring": CYAN, "ok": OK, "refused": ALERT, "noanswer": WARN, "idle": INK3, "cut": INK3}[state]
    fill = {"ring": WHITE, "ok": OK_BG, "refused": ALERT_BG, "noanswer": WARN_BG, "idle": SOFT, "cut": SOFT}[state]
    return (f'<rect x="{cx - r * 1.3:.1f}" y="{cy - r * 0.9:.1f}" width="{r * 2.6:.1f}" height="{r * 1.8:.1f}" rx="8" fill="{fill}" stroke="{col}" stroke-width="2.5"/>'
            + text(cx, cy + 6, label, 16, 600, INK, FM, anchor="middle"))
