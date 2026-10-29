#!/usr/bin/env python3
"""Lección 6 · Laboratorio, paso 4: llamada de prueba y el número que llegó de verdad, en el CDR. La factura muestra
2900 1007; el proveedor puede mandarlo en otro formato y el Strip se calcula con ese. Fuentes: la lección (el Strip se
calcula con el número exacto que manda el proveedor, mirado en el CDR o en una captura; +59829001007 con Strip 8)."""
from _anim_gs_red import R

g = R(T=24, fix=60, kicker="GRANDSTREAM · CADA DID · LABORATORIO",
      title="La primera llamada de prueba: qué número llegó")
g.steps([
    "Llamás desde tu celular al 2900 1007, el número como figura en la factura.",
    "El proveedor le entrega la llamada a la UCM con el número en su propio formato.",
    "El CDR muestra lo que llegó: +59829001007, con código de país y el más.",
    "Con ese número se calcula: su patrón y Strip 8 dejan 1007, y la interna suena.",
])

Y, H = 190, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 240, H, "Tu celular", "prueba", icon="phone"))
g.add(g.cloud(318, Y + 14, 130, 68, "red pública"))
g.add(g.dev(478, Y, 240, H, "Proveedor", "troncal SIP", icon="antel"))
g.add(g.dev(748, Y, 200, H, "UCM", "CDR > CDR", icon="ucm", dark=True))
g.add(g.dev(978, Y, 174, H, "1007", "interna", icon="tel"))
for x1, x2 in ((288, 318), (448, 478), (718, 748), (948, 978)):
    g.add(g.wire(x1, YL, x2, YL, g.BLUE))
LANE = Y - 20
g.token([(168, LANE), (598, LANE)], 3, 14, g.chip("2900 1007", bg=g.BLUE, size=13, h=26), hold=15)
g.token([(598, LANE), (848, LANE)], 28, 38, g.chip("INVITE +59829001007", bg=g.CYAN, size=13, h=26), hold=50)
g.appear(g.wire(948, YL, 978, YL, g.OK, 6), 80, 100)
g.appear(g.pillc(1065, Y + H + 12, "suena", g.OK, g.OKBG, 13, 26), 84, 100)

# factura y CDR
FY = 350
g.add(g.box(48, FY, 330, 170, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, FY + 32, "Factura del cliente", 16, g.INK, g.SANS, 600))
g.add(g.text(68, FY + 78, "2900 1007", 28, g.INK, g.MONO, 600))
g.add(g.text(68, FY + 116, "formato para personas,", 15, g.GREY, g.SANS))
g.add(g.text(68, FY + 138, "no el que viaja en SIP", 15, g.GREY, g.SANS))

CX, CW = 404, 748
g.add(g.box(CX, FY, CW, 170, g.WHITE, g.LINE, rx=14))
g.add(g.text(CX + 20, FY + 32, "CDR > CDR · última entrante", 16, g.INK, g.SANS, 600))
for t, dx in (("hora", 20), ("de", 140), ("número llamado", 330)):
    g.add(g.text(CX + dx, FY + 66, t, 14, g.GREY, g.MONO))
g.add(g.box(CX + 10, FY + 80, CW - 20, 44, g.SLATE, None, rx=8))
g.appear(g.text(CX + 20, FY + 108, "10:42", 17, g.INK, g.MONO, 600) + g.text(CX + 140, FY + 108, "tu celular", 17, g.INK, g.MONO, 600), 50, 100)
g.appear(g.text(CX + 330, FY + 108, "+59829001007", 20, g.BAD, g.MONO, 600), 52, 100)
g.appear(g.text(CX + 20, FY + 108, "(esperando la llamada)", 16, g.GREY, g.SANS), 0, 50)
g.appear(g.box(CX + 318, FY + 84, 190, 36, "none", g.BAD, rx=8, sw=2.5), 52, 75)
g.appear(g.text(CX + 20, FY + 152, "12 caracteres, el + incluido: los 8 primeros sobran", 15, g.TXT, g.SANS, 600), 56, 100)

# cálculo
KY = 546
g.appear(g.box(48, KY, 1104, 56, "#03213C", None, rx=12)
         + g.text(68, KY + 37, "+5982900", 22, "#FF9C86", g.MONO, 600)
         + f'<line x1="66" y1="{KY + 29}" x2="176" y2="{KY + 29}" stroke="#FF9C86" stroke-width="3"/>'
         + g.text(180, KY + 37, "1007", 22, g.MINT, g.MONO, 600)
         + g.text(270, KY + 36, "Strip 8, con un patrón para ese formato → interna 1007", 17, "#D9E9F8", g.SANS, 600), 76, 100)
g.appear(g.box(48, KY, 1104, 56, "#03213C", None, rx=12)
         + g.text(68, KY + 36, "Con Strip 4 sobre +59829001007 quedaría 29001007: una interna que no existe.", 17, "#F6C35B", g.SANS, 600), 52, 76)

g.status(636, [
    (0, 25, "Una llamada real muestra el número tal como lo manda el proveedor.", g.INK),
    (25, 50, "Cada proveedor elige el formato: con 598, con +, o los 8 dígitos.", g.INK),
    (50, 75, "El dato para el patrón y el Strip sale de acá, no de la factura.", g.BAD),
    (75, 100, "Anotá el formato en la ficha del troncal.", g.OK),
])

g.done(6, "l1", "La primera llamada de prueba: qué número llegó",
       "Animación en cuatro tiempos con tu celular, la red pública, el proveedor del troncal SIP, la UCM y la interna 1007; abajo, la factura del cliente, el CDR y el cálculo del Strip. "
       "1: llamás desde el celular al 2900 1007, como figura en la factura. "
       "2: el proveedor le entrega la llamada a la UCM con un INVITE con el número en su propio formato, en el ejemplo +59829001007. "
       "3: en CDR > CDR la última entrante muestra como número llamado +59829001007, con código de país y el más: 12 caracteres, de los que sobran los 8 primeros; con Strip 4 quedaría 29001007, una interna que no existe. "
       "4: con ese número se calcula: un patrón para ese formato y Strip 8 dejan 1007, y la interna suena. "
       "El dato sale del CDR, no de la factura, y se anota en la ficha del troncal.",
       [8, 36, 62, 90])
