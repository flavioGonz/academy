#!/usr/bin/env python3
"""Lección 35 · Teoría · Controladora en el tablero: lo que decide queda adentro.
Sale de teoria_md: historia (panel central, lector conectado por Wiegand, la controladora guarda usuarios y
decide; lo que decide y lo que abre queda del lado de adentro) y Cómo funciona (recibe la lectura, busca al
usuario, revisa permisos y horario, activa el relé de esa puerta; cálculo de energía por puerta)."""
from _anim_akuvox_29_42 import new, out, box, travel, when, check

a = new(20, "A094 Y A095 · CONTROLADORA", "Controladora en el tablero: lo que decide queda adentro")
a.steps([
    "El lector de la puerta 3 lee la tarjeta y manda el número por Wiegand.",
    "La controladora busca al usuario y revisa permisos y horario.",
    "Activa el relé de la puerta 3: la cerradura se libera.",
    "Afuera quedan lector y cerradura. Lo que decide y lo que abre, en el tablero.",
], still=3)

# zonas
a.add(f'<rect x="48" y="176" width="372" height="380" rx="18" fill="none" stroke="{a.GREY}" stroke-width="2" stroke-dasharray="8 6"/>')
a.add(a.text(68, 204, "PUERTA 3 · AFUERA", 15, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))
a.add(f'<rect x="446" y="176" width="22" height="380" rx="6" fill="#C9D6E3"/>')
a.add(a.text(457, 574, "pared", 15, a.GREY, a.MONO, 600, "middle"))
a.add(f'<rect x="494" y="176" width="658" height="380" rx="18" fill="none" stroke="{a.BLUE}" stroke-width="2" stroke-dasharray="8 6"/>')
a.add(a.text(514, 204, "TABLERO · ADENTRO", 15, a.BLUE, a.MONO, 600, extra='letter-spacing="1.5"'))
when(a, f'<rect x="494" y="176" width="658" height="380" rx="18" fill="none" stroke="{a.OK}" stroke-width="4"/>', 76, 100, still=1)

# cables (antes que las cajas)
a.add(f'<path d="M318 266 H560" fill="none" stroke="{a.BLUE}" stroke-width="4"/>')
a.add(a.text(382, 254, "Wiegand", 15, a.BLUE, a.MONO, 600, "middle"))
RX = [560 + i * 76 for i in range(4)]          # relés 1..4
a.add(f'<path d="M{RX[2] + 30} 474 V510 H260 V470" fill="none" stroke="{a.CYAN}" stroke-width="4"/>')

a.add(box(72, 224, 246, 84, "Lector", "puerta 3", "card"))
a.add(box(72, 386, 246, 84, "Cerradura", "puerta 3", "lock"))
# controladora
a.add(a.box(560, 224, 290, 120, a.INK, rx=16))
a.add(a.text(584, 262, "A094 o A095", 20, a.WHITE, a.HEAD, 600))
a.add(a.text(584, 288, "usuarios, permisos", 15, "#9FC3E3", a.MONO))
a.add(a.text(584, 310, "y horarios", 15, "#9FC3E3", a.MONO))
for i, x in enumerate(RX):
    a.add(a.box(x, 390, 60, 84, a.WHITE, a.LINE2 if hasattr(a, "LINE2") else a.LINE, rx=10))
    a.add(a.text(x + 30, 424, "relé", 15, a.GREY, a.MONO, 600, "middle"))
    a.add(a.text(x + 30, 448, str(i + 1), 17, a.INK, a.MONO, 600, "middle"))
    a.add(f'<path d="M{x + 30} 344 V390" stroke="{a.LINE}" stroke-width="2"/>')
when(a, f'<rect x="{RX[2]}" y="390" width="60" height="84" rx="10" fill="{a.OKBG}" stroke="{a.OK}" stroke-width="3"/>'
     + a.text(RX[2] + 30, 424, "relé", 15, a.OK, a.MONO, 600, "middle") + a.text(RX[2] + 30, 448, "3", 17, a.OK, a.MONO, 600, "middle"), 52, 100, still=1)

# t1: lectura viaja
travel(a, (330, 266), (548, 266), 4, 14, "número", a.WHITE, a.BLUE, hold=4)
# t2: chequeos
chk = [("usuario", 29), ("permiso puerta 3", 35), ("horario", 41)]
for i, (lbl, t) in enumerate(chk):
    y = 252 + i * 46
    when(a, check(a, 900, y, True, 14) + a.text(924, y + 6, lbl, 17, a.INK, a.SANS, 600), t, 100, still=1)
# t3: relé -> cerradura
travel(a, (RX[2] + 30, 474), (318, 510), 54, 62, None, bg=a.CYAN, dot=10, hold=0.5)
when(a, f'<rect x="70" y="384" width="250" height="88" rx="17" fill="none" stroke="{a.OK}" stroke-width="3"/>'
     + a.pill(196, 480, "liberada", a.OK, a.OKBG, 15, 26, "middle"), 62, 74, still=0)
# t4: rótulos
when(a, a.pill(234, 320, "solo lee", a.GREY, "#E6EDF4", 15, 26, "middle"), 77, 100, still=1)
when(a, a.pill(890, 400, "decide y abre", a.OK, a.OKBG, 15, 30), 77, 100, still=1)

a.add(a.text(48, 608, "Energía por puerta: lector + cerradura contra la salida de 12 V que los alimenta.", 18, a.INK, a.SANS, 600))
a.add(a.text(48, 636, "Si no entra, la cerradura va con fuente propia y el relé solo abre y cierra ese circuito.", 17, a.TXT, a.SANS, 600))

out(a, 35, 1, "Controladora en el tablero",
    "Animación con dos zonas separadas por una pared: afuera, en la puerta 3, un lector y una cerradura; adentro, en el tablero, una controladora A094 o A095 con cuatro relés. "
    "Tiempo 1: el lector lee la tarjeta y manda el número por Wiegand a la controladora. "
    "Tiempo 2: la controladora verifica el usuario, el permiso a la puerta 3 y el horario. "
    "Tiempo 3: activa el relé 3 y la cerradura de la puerta 3 se libera. "
    "Tiempo 4: se marca que afuera solo queda lo que lee y lo que traba; lo que decide y lo que abre está en el tablero. "
    "Abajo: la energía se calcula por puerta, lector más cerradura contra la salida de 12 V; si no entra, la cerradura lleva fuente propia.",
    [10, 45, 66, 90])
