"""Ayudantes propios de las lecciones 43 y 44 de Akuvox (theme de monitores y porteros).
No modifica ilus.py, anim.py ni los demás ayudantes: solo dibuja pantallas esquemáticas y rotuladas.

Las pantallas son genéricas (sin logos ni copias de capturas): rectángulos, íconos simples y rótulos
en español que dicen qué hay en cada área. Sirven igual en ilus.Canvas (c.add(svg)) y en anim.Anim (a.add(svg)).

mon_screen()   monitor interior apaisado: 'default' (áreas con íconos), 'calllist' (lista de contactos),
               'saver' (protector con imagen) o 'off'
door_screen()  portero táctil vertical: 'villa', 'building', 'office', 'directory', 'keypad', 'gate_empty',
               'gate', 'saver'
tile()         un área de la pantalla de inicio (ícono + rótulo), resaltable
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa
from ilus import text, e  # noqa

OUT = "/home/claude/ies-training/ilustraciones/akuvox/"
SCR, TILE, TXT2 = "#0B1A28", "#1F3347", "#9FC3E3"


def save(c, name):
    return c.save(OUT + name)


# ---------------------------------------------------------------- íconos mínimos (dibujados, sin marcas)
def glyph(cx, cy, kind, color=WHITE, s=1.0):
    """Íconos simples de 24 px aprox. kind: call, msg, dnd, alarm, sos, unlock, contacts, monitor, settings, pin,
    search, face, list, home, image, clock, building, gear."""
    k = s
    if kind == "call":
        return f'<path d="M{cx - 9 * k} {cy - 9 * k} q-2 10 8 18 q10 8 12 4 l-4 -6 l-5 2 q-6 -4 -8 -10 l3 -4 z" fill="{color}"/>'
    if kind == "msg":
        return f'<rect x="{cx - 11 * k}" y="{cy - 8 * k}" width="{22 * k}" height="{16 * k}" rx="3" fill="none" stroke="{color}" stroke-width="2.4"/><path d="M{cx - 11 * k} {cy - 7 * k} L{cx} {cy + 1 * k} L{cx + 11 * k} {cy - 7 * k}" fill="none" stroke="{color}" stroke-width="2.4"/>'
    if kind == "dnd":
        return f'<circle cx="{cx}" cy="{cy}" r="{11 * k}" fill="none" stroke="{color}" stroke-width="2.6"/><path d="M{cx - 6 * k} {cy} H{cx + 6 * k}" stroke="{color}" stroke-width="3"/>'
    if kind == "alarm":
        return f'<path d="M{cx} {cy - 12 * k} L{cx + 11 * k} {cy - 7 * k} V{cy + 1 * k} Q{cx + 10 * k} {cy + 9 * k} {cx} {cy + 13 * k} Q{cx - 10 * k} {cy + 9 * k} {cx - 11 * k} {cy + 1 * k} V{cy - 7 * k} Z" fill="none" stroke="{color}" stroke-width="2.6"/>'
    if kind == "sos":
        return f'<circle cx="{cx}" cy="{cy}" r="{12 * k}" fill="none" stroke="{color}" stroke-width="2.4"/>' + text(cx, cy + 4.5 * k, "SOS", 11 * k, 700, color, FM, anchor="middle")
    if kind == "unlock":
        return (f'<rect x="{cx - 9 * k}" y="{cy - 2 * k}" width="{18 * k}" height="{14 * k}" rx="3" fill="{color}"/>'
                f'<path d="M{cx - 5 * k} {cy - 2 * k} V{cy - 7 * k} a5 5 0 0 1 10 0" fill="none" stroke="{color}" stroke-width="2.6"/>')
    if kind == "contacts":
        return f'<circle cx="{cx}" cy="{cy - 5 * k}" r="{5 * k}" fill="{color}"/><path d="M{cx - 10 * k} {cy + 11 * k} q10 -16 20 0 z" fill="{color}"/>'
    if kind == "monitor":
        return f'<rect x="{cx - 12 * k}" y="{cy - 8 * k}" width="{24 * k}" height="{16 * k}" rx="3" fill="none" stroke="{color}" stroke-width="2.4"/><circle cx="{cx}" cy="{cy}" r="{4 * k}" fill="{color}"/>'
    if kind == "settings" or kind == "gear":
        return f'<circle cx="{cx}" cy="{cy}" r="{9 * k}" fill="none" stroke="{color}" stroke-width="5" stroke-dasharray="4 3"/><circle cx="{cx}" cy="{cy}" r="{4 * k}" fill="{color}"/>'
    if kind == "pin":
        out = []
        for i in range(3):
            for j in range(3):
                out.append(f'<circle cx="{cx - 8 * k + j * 8 * k}" cy="{cy - 8 * k + i * 8 * k}" r="{2.6 * k}" fill="{color}"/>')
        return "".join(out)
    if kind == "search":
        return f'<circle cx="{cx - 3 * k}" cy="{cy - 3 * k}" r="{8 * k}" fill="none" stroke="{color}" stroke-width="2.6"/><path d="M{cx + 3 * k} {cy + 3 * k} l7 7" stroke="{color}" stroke-width="3"/>'
    if kind == "face":
        return f'<path d="M{cx - 12 * k} {cy - 6 * k} v-6 h6 M{cx + 6 * k} {cy - 12 * k} h6 v6 M{cx + 12 * k} {cy + 6 * k} v6 h-6 M{cx - 6 * k} {cy + 12 * k} h-6 v-6" fill="none" stroke="{color}" stroke-width="2.4"/><circle cx="{cx}" cy="{cy - 2 * k}" r="{5 * k}" fill="none" stroke="{color}" stroke-width="2"/>'
    if kind == "list":
        return "".join(f'<rect x="{cx - 11 * k}" y="{cy - 9 * k + i * 7 * k}" width="{22 * k}" height="{3.4 * k}" rx="1.5" fill="{color}"/>' for i in range(3))
    if kind == "building":
        return f'<rect x="{cx - 8 * k}" y="{cy - 12 * k}" width="{16 * k}" height="{24 * k}" fill="none" stroke="{color}" stroke-width="2.4"/>' + "".join(f'<rect x="{cx - 4 * k + j * 5 * k}" y="{cy - 8 * k + i * 6 * k}" width="{3 * k}" height="{3 * k}" fill="{color}"/>' for i in range(3) for j in range(2))
    if kind == "image":
        return f'<rect x="{cx - 12 * k}" y="{cy - 9 * k}" width="{24 * k}" height="{18 * k}" rx="2" fill="none" stroke="{color}" stroke-width="2.4"/><path d="M{cx - 10 * k} {cy + 7 * k} l7 -8 l5 5 l4 -4 l6 7 z" fill="{color}"/>'
    if kind == "clock":
        return f'<circle cx="{cx}" cy="{cy}" r="{11 * k}" fill="none" stroke="{color}" stroke-width="2.4"/><path d="M{cx} {cy - 6 * k} V{cy} l5 4" fill="none" stroke="{color}" stroke-width="2.6"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{9 * k}" fill="{color}"/>'


def tile(x, y, w, h, label, kind, hl=None, size=15, warn=False):
    """Área de la pantalla de inicio: rectángulo con ícono y rótulo. hl = color de borde para resaltar."""
    fill = TILE
    stroke = hl or ("#30495F")
    sw = 3 if hl else 1.5
    lab_col = WARN_BG if warn else WHITE
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            + glyph(x + w / 2, y + h / 2 - 9, kind, hl or WHITE, 1.0)
            + text(x + w / 2, y + h - 12, label, size, 600, lab_col if not hl else hl, FB, anchor="middle"))


# ---------------------------------------------------------------- monitor interior (apaisado)
DEFAULT_AREAS = [("Llamar", "call"), ("Mensajes", "msg"), ("DND", "dnd"), ("Alarma", "alarm")]


def mon_frame(x, y, w, h, hl=None):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#F1F4F7" stroke="{hl or LINE2}" stroke-width="{3 if hl else 2}"/>'
            f'<rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 28}" rx="10" fill="{SCR}"/>')


def mon_screen(x, y, w=380, h=250, mode="default", areas=None, hl_area=None, hl=None, title=None, sub=None, clock="10:24"):
    """Monitor apaisado esquemático. areas: lista de (rótulo, ícono) para el modo default.
    hl_area: índice del área resaltada (CYAN) o (índice, color)."""
    sx, sy, sw, sh = x + 14, y + 14, w - 28, h - 28
    out = [mon_frame(x, y, w, h, hl)]
    if mode != "off":
        out.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="26" rx="10" fill="#132739"/>')
        out.append(text(sx + 12, sy + 19, clock, 15, 600, TXT2, FM))
    if mode == "default":
        areas = areas or DEFAULT_AREAS
        n = len(areas)
        gap = 10
        tw = (sw - 20 - gap * (n - 1)) / n
        th = sh - 26 - 70
        out.append(text(sx + 14, sy + 56, clock, 26, 600, WHITE, FD))
        for i, (lab, kind) in enumerate(areas):
            col = None
            if hl_area is not None:
                hi, hc = (hl_area, CYAN) if isinstance(hl_area, int) else hl_area
                col = hc if i == hi else None
            out.append(tile(sx + 10 + i * (tw + gap), sy + 26 + 50, tw, th, lab, kind, col, 15))
    elif mode == "calllist":
        lw = sw * 0.58
        rows = ["Portero calle", "Portón", "Conserjería", "Apto 302"]
        for i, r in enumerate(rows):
            ry = sy + 36 + i * ((sh - 46) / len(rows))
            rh = (sh - 46) / len(rows) - 6
            out.append(f'<rect x="{sx + 10}" y="{ry}" width="{lw - 10}" height="{rh}" rx="8" fill="{TILE}"/>')
            out.append(glyph(sx + 30, ry + rh / 2, "contacts", TXT2, 0.7))
            out.append(text(sx + 48, ry + rh / 2 + 5, r, 15, 600, WHITE, FB))
            out.append(glyph(sx + lw - 18, ry + rh / 2 + 1, "call", CYAN, 0.6))
        bx = sx + lw + 10
        bw = sw - lw - 20
        mini = [("Monitor", "monitor"), ("DND", "dnd"), ("Más", "list")]
        bh = (sh - 46 - 8 * (len(mini) - 1)) / len(mini)
        for i, (lab, kind) in enumerate(mini):
            cy = sy + 36 + i * (bh + 8)
            out.append(f'<rect x="{bx}" y="{cy:.1f}" width="{bw}" height="{bh:.1f}" rx="8" fill="{TILE}"/>')
            out.append(glyph(bx + 20, cy + bh / 2, kind, WHITE, 0.75))
            out.append(text(bx + 38, cy + bh / 2 + 5, lab, 15, 600, WHITE, FB))
    elif mode == "saver":
        out.append(f'<rect x="{sx + 10}" y="{sy + 34}" width="{sw - 20}" height="{sh - 44}" rx="8" fill="#16324D"/>')
        out.append(f'<path d="M{sx + 10} {sy + sh - 10} l{sw * 0.3} -{sh * 0.45} l{sw * 0.18} {sh * 0.25} l{sw * 0.14} -{sh * 0.14} l{sw * 0.38 - 20} {sh * 0.34} z" fill="#24507A"/>')
        out.append(text(sx + sw / 2, sy + 76, "Edificio Rambla", 20, 600, WHITE, FD, anchor="middle"))
        out.append(text(sx + sw / 2, sy + 102, "protector: Local Pictures", 15, 500, TXT2, FM, anchor="middle"))
    elif mode == "off":
        out.append(text(sx + sw / 2, sy + sh / 2 + 5, "pantalla apagada", 15, 500, "#5F7C96", FM, anchor="middle"))
    if title:
        out.append(text(x + w / 2, y + h + 28, title, 18, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(x + w / 2, y + h + 50, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


# ---------------------------------------------------------------- portero táctil (vertical)
def door_frame(x, y, w, h, hl=None):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#2A3644" stroke="{hl or DEEP}" stroke-width="{3 if hl else 2}"/>'
            f'<circle cx="{x + w / 2}" cy="{y + 16}" r="5" fill="#0B1A28" stroke="#5F7C96" stroke-width="1.5"/>'
            f'<rect x="{x + 12}" y="{y + 32}" width="{w - 24}" height="{h - 44}" rx="10" fill="{SCR}"/>')


def _round_icon(cx, cy, r, label, kind, col=CYAN):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TILE}" stroke="{col}" stroke-width="2.5"/>'
            + glyph(cx, cy, kind, WHITE, 1.0)
            + text(cx, cy + r + 18, label, 15, 600, WHITE, FB, anchor="middle"))


def door_screen(x, y, w=210, h=340, mode="building", hl=None, title=None, sub=None, langs=None):
    """Portero vertical esquemático. mode: villa, building, office, directory, keypad, gate_empty, gate, saver."""
    sx, sy, sw, sh = x + 12, y + 32, w - 24, h - 44
    out = [door_frame(x, y, w, h, hl)]
    cx = sx + sw / 2
    if mode == "villa":
        for i, (lab, kind) in enumerate([("Contacto", "contacts"), ("PIN", "pin"), ("Llamar", "call")]):
            out.append(_round_icon(cx, sy + 42 + i * ((sh - 44) / 3), 22, lab, kind))
    elif mode == "building":
        out.append(f'<rect x="{sx + 12}" y="{sy + 12}" width="{sw - 24}" height="{sh * 0.36}" rx="8" fill="#132739" stroke="#30495F" stroke-dasharray="5 4"/>')
        out.append(glyph(cx, sy + 12 + sh * 0.16, "face", TXT2, 1.4))
        out.append(text(cx, sy + 12 + sh * 0.36 - 10, "rostro", 15, 500, TXT2, FM, anchor="middle"))
        tw, th = (sw - 34) / 2, (sh * 0.58 - 34) / 2
        labs = [("PIN", "pin"), ("Llamar", "call"), ("Directorio", "list"), ("Recepción", "contacts")]
        for i, (lab, kind) in enumerate(labs):
            tx = sx + 12 + (i % 2) * (tw + 10)
            ty = sy + sh * 0.42 + (i // 2) * (th + 10)
            out.append(tile(tx, ty, tw, th, lab, kind, None, 15))
        if langs:
            out.append(text(cx, sy + sh - 4, "  ".join(langs), 15, 600, CYAN, FM, anchor="middle"))
    elif mode == "office":
        out.append(f'<rect x="{sx + 12}" y="{sy + 14}" width="{sw - 24}" height="34" rx="17" fill="{TILE}"/>')
        out.append(glyph(sx + 32, sy + 31, "search", TXT2, 0.7))
        out.append(text(sx + 48, sy + 36, "Buscar", 15, 500, TXT2, FB))
        for i, r in enumerate(["Administración", "Contaduría", "Ventas", "Soporte"]):
            ry = sy + 60 + i * 44
            out.append(f'<rect x="{sx + 12}" y="{ry}" width="{sw - 24}" height="36" rx="8" fill="{TILE}"/>')
            out.append(text(sx + 24, ry + 24, r, 15, 600, WHITE, FB))
        out.append(text(cx, sy + sh - 14, "sectores", 15, 500, TXT2, FM, anchor="middle"))
    elif mode == "directory":
        out.append(text(cx, sy + 26, "Directorio", 15, 600, WHITE, FD, anchor="middle"))
        for i, r in enumerate(["101  García", "102  Pereira", "201  Rodríguez", "202  Silva", "301  Méndez"]):
            ry = sy + 40 + i * 42
            out.append(f'<rect x="{sx + 10}" y="{ry}" width="{sw - 20}" height="34" rx="8" fill="{TILE}"/>')
            out.append(text(sx + 18, ry + 23, r, 15, 600, WHITE, FM))
            out.append(glyph(sx + sw - 26, ry + 17, "call", CYAN, 0.55))
    elif mode == "keypad":
        out.append(f'<rect x="{sx + 14}" y="{sy + 12}" width="{sw - 28}" height="34" rx="8" fill="#132739" stroke="{CYAN}" stroke-width="1.5"/>')
        out.append(text(cx, sy + 35, "• • • •", 16, 600, WHITE, FM, anchor="middle"))
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "C", "0", "OK"]
        kw, kh = (sw - 28 - 16) / 3, (sh - 70 - 30) / 4
        for i, kk in enumerate(keys):
            kx = sx + 14 + (i % 3) * (kw + 8)
            ky = sy + 58 + (i // 3) * (kh + 8)
            fill = OK if kk == "OK" else TILE
            out.append(f'<rect x="{kx:.1f}" y="{ky:.1f}" width="{kw:.1f}" height="{kh:.1f}" rx="8" fill="{fill}"/>')
            out.append(text(kx + kw / 2, ky + kh / 2 + 6, kk, 17, 600, WHITE, FM, anchor="middle"))
    elif mode in ("gate", "gate_empty"):
        out.append(text(cx, sy + 26, "Elegí el edificio", 15, 600, WHITE, FD, anchor="middle"))
        if mode == "gate":
            for i, r in enumerate(["Torre A", "Torre B", "Torre C"]):
                ry = sy + 44 + i * 52
                out.append(f'<rect x="{sx + 10}" y="{ry}" width="{sw - 20}" height="42" rx="8" fill="{TILE}"/>')
                out.append(glyph(sx + 32, ry + 21, "building", TXT2, 0.7))
                out.append(text(sx + 52, ry + 26, r, 14, 600, WHITE, FB))
            out.append(text(cx, sy + sh - 16, "desde SmartPlus", 15, 600, OK_BG, FM, anchor="middle"))
        else:
            out.append(f'<rect x="{sx + 14}" y="{sy + 50}" width="{sw - 28}" height="{sh - 90}" rx="8" fill="none" stroke="{WARN}" stroke-width="2" stroke-dasharray="6 5"/>')
            out.append(text(cx, sy + sh / 2 + 4, "sin edificios", 15, 600, WARN_BG, FB, anchor="middle"))
            out.append(text(cx, sy + sh / 2 + 24, "para mostrar", 15, 600, WARN_BG, FB, anchor="middle"))
    elif mode == "saver":
        out.append(f'<rect x="{sx + 8}" y="{sy + 8}" width="{sw - 16}" height="{sh - 16}" rx="8" fill="#16324D"/>')
        out.append(f'<path d="M{sx + 8} {sy + sh - 8} l{sw * 0.35} -{sh * 0.35} l{sw * 0.2} {sh * 0.18} l{sw * 0.45 - 16} {sh * 0.17} z" fill="#24507A"/>')
        out.append(text(cx, sy + 60, "Edificio", 18, 600, WHITE, FD, anchor="middle"))
        out.append(text(cx, sy + 84, "Rambla", 18, 600, WHITE, FD, anchor="middle"))
        out.append(text(cx, sy + 114, "protector", 15, 500, TXT2, FM, anchor="middle"))
    if title:
        out.append(text(x + w / 2, y + h + 28, title, 18, 600, INK, FB, anchor="middle"))
    if sub:
        out.append(text(x + w / 2, y + h + 50, sub, 15, 400, INK3, FM, anchor="middle"))
    return "".join(out)


def menu_path(x, y, s, size=15, color=BLUE, bg=WHITE):
    """Ruta de menú en una píldora con borde (texto mono)."""
    w = len(s) * size * 0.6 + 24
    return (f'<rect x="{x}" y="{y - size - 6}" width="{w:.1f}" height="{size + 14}" rx="{(size + 14) / 2:.1f}" fill="{bg}" stroke="{color}" stroke-width="1.5"/>'
            + text(x + 12, y + 1, s, size, 600, color, FM))
