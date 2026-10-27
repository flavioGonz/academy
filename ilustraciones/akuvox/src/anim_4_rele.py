#!/usr/bin/env python3
"""Lección 4 · teoría: el relé conmuta COM entre NC y NO; qué hace cada cerradura en el tiempo y al cortarse la luz."""
from _anim_akuvox import Anim, A, token, appear, lock, finish

a = Anim(T=24, kicker="AKUVOX · RELÉ Y CERRADURA", title="El relé conmuta: qué hace cada cerradura")
a.steps([
    "En reposo, el COM está unido al NC.",
    "Se activa el relé (PIN, tarjeta, DTMF, HTTP o botón): COM pasa a NO.",
    "Pasa el tiempo de Access Control > Relay y el COM vuelve al NC.",
    "Se corta la fuente: COM + NO queda trabada, COM + NC queda libre.",
], still=1)

PH = [(0, 25), (25, 50), (50, 75), (75, 100)]
RED, BLK, CY = A.BAD, A.INK, A.CYAN


def wire(pts, color, w=4, dash=""):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{da}/>'


def on(inner, phases, still_on):
    """inner visible en las fases indicadas (lista de índices)."""
    for i in phases:
        a.add(a.group(inner, a.show(PH[i][0], PH[i][1], 0.8), still=1 if i == still_on else 0))


def panel(ox, contact, title, sub, load, closed_phases, texts):
    """contact: 'NO' o 'NC' (el borne que alimenta la carga). texts: [(estado, color, tension)] por fase."""
    a.add(a.box(ox, 172, 540, 360, A.WHITE, A.LINE, rx=18))
    a.add(a.text(ox + 22, 206, title, 20, A.INK, A.HEAD, 600))
    a.add(a.text(ox + 22, 230, sub, 15, A.GREY, A.MONO))
    # fuente
    a.add(a.box(ox + 22, 258, 150, 84, A.SLATE, None, rx=12))
    a.add(a.text(ox + 40, 292, "Fuente 12 V", 17, A.INK, A.SANS, 600))
    a.add(a.text(ox + 40, 318, "aparte", 14, A.GREY, A.MONO))
    on(a.box(ox + 22, 258, 150, 84, A.BADBG, RED, rx=12, sw=2) + a.text(ox + 40, 292, "Fuente 12 V", 17, A.BAD, A.SANS, 600)
       + a.text(ox + 40, 318, "sin energía", 14, A.BAD, A.MONO, 600), [3], -1)
    # relé
    COM, NO, NC = (ox + 262, 340), (ox + 352, 292), (ox + 352, 388)
    a.add(a.box(ox + 222, 252, 168, 176, "#F2F7FC", A.LINE, rx=12))
    a.add(a.text(ox + 238, 278, "Relé A", 16, A.INK, A.SANS, 600))
    for (x, y), lab in ((COM, "COM"), (NO, "NO"), (NC, "NC")):
        a.add(f'<circle cx="{x}" cy="{y}" r="8" fill="{A.WHITE}" stroke="{A.INK}" stroke-width="2.5"/>')
        a.add(a.text(x, y + {"COM": 30, "NO": -16, "NC": 30}[lab], lab, 14, A.INK, A.MONO, 600, "middle"))
    blade_nc = f'<line x1="{COM[0]}" y1="{COM[1]}" x2="{NC[0] - 9}" y2="{NC[1] - 4}" stroke="{A.INK}" stroke-width="5" stroke-linecap="round"/>'
    blade_no = f'<line x1="{COM[0]}" y1="{COM[1]}" x2="{NO[0] - 9}" y2="{NO[1] + 4}" stroke="{A.INK}" stroke-width="5" stroke-linecap="round"/>'
    on(blade_nc, [0, 2, 3], 1)
    on(blade_no, [1], 1)
    # cables base (gris) y energizados
    LX = ox + 470
    feed = NO if contact == "NO" else NC
    plus = [(ox + 172, 280), (ox + 200, 280), (ox + 200, COM[1]), (COM[0] - 8, COM[1])]
    out = [(feed[0] + 8, feed[1]), (LX, feed[1]), (LX, 414)]
    back = [(LX, 500), (LX, 512), (ox + 96, 512), (ox + 96, 342)]
    for p in (plus, out, back):
        a.add(wire(p, A.LINE, 4))
    on(wire(plus, RED, 4), [0, 1, 2], 1)
    on(wire(out, CY, 5) + wire(back, BLK, 4), closed_phases, 1)
    # carga
    a.add(a.box(LX - 70, 414, 140, 86, A.WHITE, A.INK, rx=12, sw=2))
    a.add(a.text(LX, 440, load, 15, A.INK, A.SANS, 600, "middle"))
    for i, (est, col, v) in enumerate(texts):
        op = col == A.OK
        inner = (lock(a, LX - 52, 466, open_=op, color=col, s=0.8)
                 + a.text(LX - 16, 484, est, 15, col, A.MONO, 600))
        on(inner, [i], 1)
        on(a.pill(LX - 84, 472, v, col, A.OKBG if col == A.OK else A.BADBG, 14, 28, "end"), [i], 1)


panel(48, "NO", "COM + NO · cerradura", "fail-secure", "Cerradura",
      [1], [("trabada", A.BAD, "0 V"), ("abre", A.OK, "12 V"), ("trabada", A.BAD, "0 V"), ("trabada", A.BAD, "0 V")])
panel(612, "NC", "COM + NC · electroimán", "fail-safe", "Electroimán",
      [0, 2], [("trabada", A.BAD, "12 V"), ("libre", A.OK, "0 V"), ("trabada", A.BAD, "12 V"), ("libre", A.OK, "0 V")])

# línea de tiempo con cursor
TY = 572
labels = ["reposo", "relé activo", "reposo", "corte de luz"]
cols = [A.SLATE, "#E4F5FB", A.SLATE, A.BADBG]
fg = [A.GREY, A.CYAN, A.GREY, A.BAD]
W = 1104 / 4
for i, lab in enumerate(labels):
    x = 48 + i * W
    a.add(a.box(x + 2, TY, W - 4, 40, cols[i], None, rx=8))
    a.add(a.text(x + W / 2, TY + 26, lab, 15, fg[i], A.MONO, 600, "middle"))
a.add(a.text(48 + W * 1.5, TY + 64, "tiempo de apertura: Access Control > Relay", 14, A.GREY, A.MONO, 400, "middle"))
cur = f'<path d="M0 0 L-9 -14 L9 -14 z" fill="{A.BLUE}"/>'
token(a, [(52, TY - 2), (1148, TY - 2)], 0, 100, cur, hold=100)

finish(a, "4-t1.svg", "El relé conmuta entre NC y NO",
       "Animación en cuatro tiempos con dos circuitos iguales salvo el borne: a la izquierda una cerradura cableada en COM y NO (fail-secure), "
       "a la derecha un electroimán en COM y NC (fail-safe), los dos con fuente de 12 V aparte. "
       "1: en reposo el COM toca el NC; la cerradura tiene 0 V y está trabada, el electroimán tiene 12 V y sostiene la puerta. "
       "2: el portero activa el relé por PIN, tarjeta, DTMF, HTTP o botón y el COM pasa al NO; la cerradura recibe 12 V y abre, el electroimán queda en 0 V y libera. "
       "3: pasa el tiempo configurado en Access Control > Relay y el COM vuelve al NC; las dos quedan trabadas. "
       "4: se corta la fuente; la cerradura en NO sigue trabada y el electroimán en NC queda libre.",
       [12, 37, 62, 88])
