#!/usr/bin/env python3
"""Lección 6 · Resumen, "Cómo se ve en la red": una sola ruta entrante con patrón, By DID y Strip reparte cada número
directo a su interna; si el proveedor cambia el formato del número, el patrón deja de coincidir.
Fuentes: la lección (_2900XXXX, By DID, Strip 4: 29001007 → 1007; Strip cuenta caracteres, el + incluido;
cada formato necesita su patrón; el número real se mira en el CDR)."""
from _anim_gs_red import R

g = R(T=26, fix=70, kicker="GRANDSTREAM · CADA DID · CÓMO SE VE EN LA RED",
      title="Cien números, una ruta: cada DID a su interna")
g.steps([
    "Entra una llamada a 29001007: coincide con _2900XXXX, Strip 4 deja 1007 y suena la 1007.",
    "Entra otra a 29001023: la misma ruta la lleva a la 1023.",
    "Y otra a 29001050: la 1050. Una ruta alcanza para los cien números.",
    "Si el proveedor empieza a mandar +59829001007, ya no coincide: no llega a la 1007.",
])

Y = 196
g.add(g.dev(48, Y, 220, 96, "Proveedor", "troncal SIP", icon="antel"))
RX, RW = 330, 470
g.add(g.box(RX, 186, RW, 250, g.WHITE, g.LINE, rx=16))
g.add(g.text(RX + 20, 218, "Inbound Route del troncal", 17, g.INK, g.SANS, 600))
for k, (n, v) in enumerate([("Pattern", "_2900XXXX"), ("Destination", "By DID"), ("Strip", "4")]):
    g.add(g.text(RX + 20, 252 + k * 26, n, 15, g.GREY, g.MONO) + g.text(RX + 170, 252 + k * 26, v, 16, g.INK, g.MONO, 600))
g.add(g.box(RX + 16, 320, RW - 32, 100, "#03213C", None, rx=12))
g.add(g.text(RX + 34, 346, "número llamado (Request-line)", 14, g.SKY, g.MONO))

EX = 870
exts = [("1007", 186), ("1023", 262), ("1050", 338)]
for n, y in exts:
    g.add(g.dev(EX, y, 282, 64, f"Interna {n}", icon="tel", tsize=18))
g.add(g.wire(268, Y + 48, RX, Y + 48, g.BLUE))

def llamada(num, ext, y, t0, t1):
    g.token([(158, Y - 18), (RX + 235, Y - 18)], t0, t0 + 5, g.chip(f"INVITE {num}", bg=g.BLUE, size=13, h=26), hold=t0 + 5.5)
    g.appear(g.text(RX + 34, 392, num[:4], 28, g.BAD, g.MONO, 600)
             + f'<line x1="{RX + 32}" y1="382" x2="{RX + 106}" y2="382" stroke="{g.BAD}" stroke-width="3"/>'
             + g.text(RX + 110, 392, num[4:], 28, g.MINT, g.MONO, 600)
             + g.text(RX + 230, 392, f"→ interna {ext}", 18, "#D9E9F8", g.SANS, 600), t0 + 6, t1)
    g.arrow([(RX + RW, 380), (EX - 20, y + 32), (EX, y + 32)], t0 + 10, t0 + 14, g.OK, hold=t1)
    g.appear(g.pillc(EX + 230, y + 19, "suena", g.OK, g.OKBG, 13, 26), t0 + 14, t1)

llamada("29001007", "1007", 186, 2, 25)
llamada("29001023", "1023", 262, 27, 50)
llamada("29001050", "1050", 338, 52, 75)

# 4 · otro formato
g.token([(158, Y - 18), (RX + 235, Y - 18)], 77, 82, g.chip("INVITE +59829001007", bg=g.AMB, size=13, h=26), hold=82.5)
g.appear(g.text(RX + 34, 392, "+59829001007", 26, g.GOLD, g.MONO, 600)
         + g.text(RX + 270, 392, "no coincide", 18, "#FF9C86", g.SANS, 600), 83, 100)
g.appear(g.box(RX + 12, 236, RW - 24, 24, "none", g.BAD, rx=6, sw=2.5), 83, 100)
g.appear(g.mark(EX - 30, 218, False, 15), 88, 100)

g.appear(g.note(48, 460, 1104, None, ["Cada llamada se procesa sola: la central lee el número, lo compara con el patrón, saca los primeros 4 caracteres y llama a la interna que queda."], "info"), 0, 75)
g.appear(g.note(48, 460, 1104, None, ["Para ese formato hace falta su propio patrón y Strip 8, porque el + también cuenta. El número real se mira en el CDR, no en la factura."], "amb"), 75, 100)

g.status(620, [
    (0, 25, "29001007 menos 2900 es 1007: la interna existe y suena.", g.OK),
    (25, 50, "Mismo patrón, mismo Strip, otra interna: By DID usa lo que queda.", g.OK),
    (50, 75, "Del 29001000 al 29001099, cada uno a su interna, con una sola ruta.", g.OK),
    (75, 100, "Con otro formato del número, la ruta no lo reconoce.", g.BAD),
])

g.done(6, "r1", "Cien números, una ruta: cada DID a su interna",
       "Animación en cuatro tiempos con el proveedor del troncal SIP, la ruta entrante del troncal (Pattern _2900XXXX, Destination By DID, Strip 4) con un recuadro del número llamado, y las internas 1007, 1023 y 1050. "
       "1: entra un INVITE a 29001007; coincide con el patrón, Strip 4 tacha 2900, queda 1007 y suena la interna 1007. "
       "2: entra otro a 29001023 y la misma ruta lo lleva a la 1023. "
       "3: entra otro a 29001050 y va a la 1050: una sola ruta alcanza para los números del 29001000 al 29001099. "
       "4: si el proveedor empieza a mandar el número como +59829001007, ya no coincide con _2900XXXX y la llamada no llega a la 1007; ese formato necesita su propio patrón y Strip 8, porque el + también cuenta, y el número real se mira en el CDR, no en la factura.",
       [20, 45, 70, 92])
