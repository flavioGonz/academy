import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *


def pair(pts, off=14):
    """Par LSN: b (azul) sobre la ruta y a (oscuro) corrido hacia adentro."""
    return wire(pts, "data") 


# ---------------------------------------------------------------- 3.svg: el lazo
c = Canvas(K(), "Un solo par de cables para todo el lazo")
c.add(rect(60, 140, 260, 110, DEEP, DEEP, rx=14))
c.add(text(80, 178, "Módulo de lazo", 19, 600, WHITE, FD))
c.add(text(80, 204, "LSN 0300 A o LSN 1500 A", 15, 400, "#9FC3E3", FM))
c.add(text(100, 238, "LSN1", 14, 600, "#9FC3E3", FM, anchor="middle"))
c.add(text(280, 238, "LSN2", 14, 600, "#9FC3E3", FM, anchor="middle"))
# b (azul) y a (oscuro) en paralelo
c.add(f'<path d="M100 250V560H800V330H280V250" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>')
c.add(f'<path d="M114 250V546H786V344H294V250" fill="none" stroke="{BLACK}" stroke-width="3" stroke-linejoin="round"/>')
c.add(text(126, 300, "b", 16, 700, BLUE, FM)); c.add(text(126, 322, "a", 16, 700, BLACK, FM))
for x, k in [(250, "d"), (420, "d"), (590, "p")]:
    c.add(rect(x - 34, 520, 68, 66, GROUND, GROUND, rx=10, sw=0))
    c.add(detector(x, 553, 28) if k == "d" else pulsador(x, 553, 50))
c.add(rect(762, 405, 76, 76, GROUND, GROUND, rx=10, sw=0))
c.add(sirena(800, 443, 52))
for x in (420, 610):
    c.add(rect(x - 34, 304, 68, 66, GROUND, GROUND, rx=10, sw=0))
    c.add(detector(x, 337, 28))
c.add(text(340, 430, "sale por LSN1, recorre", 16, 500, INK2))
c.add(text(340, 454, "y vuelve por LSN2", 16, 500, INK2))
c.add(text(48, 640, "Detectores, pulsadores, sirenas y módulos van en el mismo lazo, cada uno con su dirección.", 16, 500, INK2))
c.add(box(880, 130, 272, 150, "LSN improved", ["254 elementos por módulo", "con un solo classic: 127", "y sin derivaciones T-tap"], kind="info", size=16))
c.add(box(880, 300, 272, 120, "LSN 0300 A", ["hasta 300 mA", "hasta 1600 m de cable"], size=16, mono=False))
c.add(box(880, 440, 272, 140, "LSN 1500 A", ["hasta 1500 mA (improved)", "hasta 3000 m de cable", "300 mA si hay classic"], size=16))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso1: cableado en lazo
c = Canvas(K(1), "Cableá los tres en lazo: b pasa por el aislador")
c.add(rect(430, 136, 340, 128, DEEP, DEEP, rx=14))
c.add(mid(600, 180, "LSN 0300 A", 20, 600, WHITE, FD))
c.add(mid(600, 206, "módulo de lazo del panel", 15, 400, "#9FC3E3", FM))
for (x, y, s, col, an) in [(430, 180, "LSN1 a−", INK2, "end"), (430, 230, "LSN1 b+", BLUE, "end"), (770, 180, "LSN2 a−", INK2, "start"), (770, 230, "LSN2 b+", BLUE, "start")]:
    c.add(f'<circle cx="{x}" cy="{y}" r="6" fill="{WHITE}" stroke="{col}" stroke-width="2.5"/>')
    c.add(text(x + (-12 if an == "end" else 12), y - 8, s, 14, 600, col, FM, anchor=an))
c.add(wire([(430, 180), (40, 180), (40, 520), (210, 520), (210, 470)], "power-"))
c.add(wire([(430, 230), (60, 230), (60, 394), (90, 394)], "data"))
c.add(wire([(210, 470), (210, 520), (600, 520), (600, 470)], "power-"))
c.add(wire([(600, 470), (600, 520), (990, 520), (990, 470)], "power-"))
c.add(wire([(990, 470), (990, 520), (1160, 520), (1160, 180), (770, 180)], "power-"))
c.add(wire([(330, 394), (480, 394)], "data"))
c.add(wire([(720, 394), (870, 394)], "data"))
c.add(wire([(1110, 394), (1140, 394), (1140, 230), (770, 230)], "data"))
for i, x in enumerate((90, 480, 870)):
    s, an = elemento(x, 360, 240, 110, f"Detector {i + 1}", "FAP-425-O-R")
    c.add(s)
    c.add(text(x + 130, 496, "a−", 14, 600, INK2, FM))
    c.add(tag(x + 120, 340, "perillas 000", "gray", size=14))
c.add(Note(48, 552, 540, "b entra por b1+ y sale por b2+, con el aislador en el medio. La línea a es común a todos.", title="b atraviesa, a acompaña", kind="info"))
c.add(Note(612, 552, 540, "Con 000 el panel numera solo, por orden de cable. Es el ajuste de fábrica y no admite T-tap.", title="000 = automático", kind="info"))
save(c, "3-paso1.svg")

# ---------------------------------------------------------------- 3-paso3: perillas
c = Canvas(K(3), "Tres perillas: centenas, decenas y unidades")


def dial(cx, cy, d, r=34, hl=False):
    ang = math.radians(-90 + 36 * d)
    px, py = cx + (r - 9) * math.cos(ang), cy + (r - 9) * math.sin(ang)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHITE}" stroke="{CYAN if hl else LINE2}" stroke-width="{3 if hl else 2.5}"/>'
            f'<path d="M{cx} {cy}L{px:.1f} {py:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="6" fill="{INK}"/>' + text(cx, cy + r + 26, str(d), 20, 700, BLUE if hl else INK2, FM, anchor="middle"))


import math
for i in range(3):
    y = 150 + i * 140
    c.add(rect(48, y, 620, 120, WHITE, LINE2, rx=16))
    c.add(text(72, y + 50, f"Detector {i + 1}", 19, 600, INK, FD))
    c.add(text(72, y + 78, f"dirección {i + 1:03d}", 16, 500, BLUE, FM))
    for j, d in enumerate((0, 0, i + 1)):
        c.add(dial(330 + j * 110, y + 48, d, 30, hl=(j == 2)))
for j, s in enumerate(("centenas", "decenas", "unidades")):
    c.add(mid(330 + j * 110, 140, s, 15, 600, INK3))
c.add(Table(700, 150, ["Perillas", "Modo"], [["0 0 0", "automático, de fábrica, sin T-tap"], ["001 a 254", "manual, permite T-tap"], ["CL 0 0", "modo classic"]], [140, 312], hl_row=1, row_h=46, mono_cols=(0,)))
c.add(Note(700, 360, 452, "Se cambian con el lazo desenergizado. Después, en la configuración del lazo en RPS se marca T-tap y se vuelve a autodetectar.", title="Antes de girar", kind="info"))
c.add(Note(700, 500, 452, "Más de 254 no está permitido, y en un mismo lazo no se mezcla automático con manual: con manual, todos del 1 al 254.", title="Dos errores típicos", kind="alert"))
save(c, "3-paso3.svg")
