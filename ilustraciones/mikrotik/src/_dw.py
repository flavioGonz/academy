"""Ayudantes para las ilustraciones de dos WAN (lecciones 11, 37, 38 y 39). Encima de _mt.py, sin tocar ilus.py."""
from _mt import *  # noqa


def router_box(c, x, y, w=200, h=250, p1="ether1", p2="ether2", sub=None, lan="bridge · LAN"):
    """Router oscuro con dos puertos WAN (arriba y abajo) y la LAN a la izquierda. Devuelve anclas."""
    c.add(rect(x, y, w, h, DEEP, DEEP, 2, 18))
    c.add(text(x + 20, y + 36, "Router", 20, 600, WHITE, FD))
    if sub:
        c.add(text(x + w - 18, y + 36, sub, 14, 500, CYAN, FM, anchor="end"))
    c.add(rect(x + 18, y + 58, w - 36, 40, BLUE, BLUE, 0, 8))
    c.add(text(x + w / 2, y + 84, p1, 15, 600, WHITE, FM, anchor="middle"))
    c.add(rect(x + 18, y + h - 58, w - 36, 40, "#0B3A66", "#4E7396", 2, 8))
    c.add(text(x + w / 2, y + h - 32, p2, 15, 600, WHITE, FM, anchor="middle"))
    c.add(text(x + 20, y + h / 2 + 6, lan, 15, 500, "#9FC3E3", FM))
    return {"p1": (x + w, y + 78), "p2": (x + w, y + h - 38), "lan": (x, y + h / 2)}


def wan_box(c, x, y, w, title, lines, chip=None, chip_kind="blue", hl=BLUE, h=None, icon_name=None):
    """Caja de una WAN: título, líneas en mono y un chip de distancia abajo. Devuelve (izq, der, alto)."""
    h = h or (64 + 28 * len(lines) + (44 if chip else 0))
    c.add(rect(x, y, w, h, WHITE, hl, 2.5, 16))
    tx = x + 20
    if icon_name:
        c.add(icon(x + 18, y + 16, icon_name, hl, 1.15))
        tx = x + 54
    c.add(text(tx, y + 38, title, 19, 600, INK, FD))
    for i, ln in enumerate(lines):
        c.add(text(x + 20, y + 72 + 28 * i, ln, 15, 500, INK2, FM))
    if chip:
        c.add(pill(x + 18, y + h - 22, chip, chip_kind, anchor="start"))
    return (x, y + h / 2), (x + w, y + h / 2), h


def witness_box(c, x, y, w, title, hosts, color=BLUE):
    h = 52 + 30 * len(hosts)
    c.add(rect(x, y, w, h, WHITE, color, 2, 16))
    c.add(text(x + 18, y + 32, title, 16, 600, INK, FB))
    for i, s in enumerate(hosts):
        c.add(text(x + 18, y + 64 + 30 * i, s, 16, 600, color, FM))
    return (x, y + h / 2), h


def route_table(c, x, y, rows_, widths, head=("Destino", "Gateway", "Dist.", "Estado"), row_h=42, size=15):
    t, h = ctable(x, y, list(head), rows_, widths, row_h=row_h, col_fonts=[FM, FM, FM, FB][:len(widths)] + [FB] * max(0, len(widths) - 4), size=size)
    c.add(t)
    return h
