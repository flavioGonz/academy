#!/usr/bin/env python3
"""Lección 6 · Resumen, "Cómo se ve en la red": el camino coherente de punta a punta con un switch de terceros entre
el gateway y el AP. El AP manda la gestión sin etiqueta y los SSID etiquetados (20 y 30); si el switch del medio la
espera etiquetada, la gestión cae en otra VLAN y no hay inform; corregido, todo llega; un switch no administrable
descarta o pierde las etiquetas. Fuentes: theory_md y lab.md (paso 5) de la lección: LazyAdmin y UniHosted."""
from _anim_red_unifi import *  # noqa

a = new(26, "Puertos con perfil", "Un switch de terceros en el medio: el camino tiene que coincidir", [
    "El AP manda su gestión sin etiqueta y cada SSID con la suya: 20 y 30.",
    "Si el switch del medio espera la gestión etiquetada, cae en otra VLAN: sin inform.",
    "Corregido: gestión sin etiqueta, SSID etiquetados. Todo llega a su red.",
    "Un switch no administrable en el medio descarta o pierde las etiquetas.",
], still=2)

Y, H = 186, 96
a.add(dev(a, 48, Y, 250, H, "Gateway UniFi", "gestión · 20 · 30", icon="server", dark=True))
a.add(dev(a, 860, Y, 292, H, "AP", "gestión sin etiqueta", ap=True, sub2="SSID 20 y 30"))
SW = a.box(420, Y, 320, H, a.WHITE, a.LINE, rx=14) + glyph(a, "server", 438, Y + 18)
a.add(SW)
vis(a, a.text(482, Y + 34, "Switch de terceros", 19, a.INK, a.SANS, 600) + a.text(482, Y + 58, "administrable", 15, a.GREY, a.MONO), 0, 2)
vis(a, a.text(482, Y + 34, "Switch no administrable", 19, a.BAD, a.SANS, 600) + a.text(482, Y + 58, "no entiende VLAN", 15, a.BAD, a.MONO), 3)
a.add(wire(298, Y + 48, 420, Y + 48, a.BLUE, 4))
a.add(wire(740, Y + 48, 860, Y + 48, a.BLUE, 4))

LG, L20, L30 = 318, 350, 382
for yy in (LG, L20, L30):
    a.add(wire(173, yy, 1006, yy, a.LINE, 2, "3 7"))
for cx in (173, 580, 1006):
    a.add(wire(cx, Y + H, cx, L30, a.LINE, 2, "3 7"))
a.add(a.text(1012, LG + 5, "", 15))

# tarjeta del puerto del switch hacia el AP
PX, PY = 380, 420
a.add(a.box(PX, PY, 400, 140, a.WHITE, a.LINE, rx=14))
a.add(a.text(PX + 20, PY + 32, "Puerto del switch hacia el AP", 17, a.INK, a.SANS, 600))
vis(a, a.text(PX + 20, PY + 66, "gestión:  sin etiqueta", 16, a.INK, a.MONO, 600) + a.text(PX + 20, PY + 96, "VLAN 20, 30:  etiquetadas", 16, a.INK, a.MONO, 600), 0)
vis(a, a.text(PX + 20, PY + 66, "gestión:  etiquetada", 16, a.BAD, a.MONO, 600) + a.text(PX + 20, PY + 96, "VLAN 20, 30:  etiquetadas", 16, a.INK, a.MONO, 600)
    + a.text(PX + 20, PY + 124, "lo sin etiqueta va a otra VLAN", 15, a.BAD, a.SANS, 600), 1)
vis(a, a.text(PX + 20, PY + 66, "gestión:  sin etiqueta", 16, a.OK, a.MONO, 600) + a.text(PX + 20, PY + 96, "VLAN 20, 30:  etiquetadas", 16, a.OK, a.MONO, 600)
    + a.text(PX + 20, PY + 124, "igual que espera el AP", 15, a.OK, a.SANS, 600), 2)
vis(a, a.text(PX + 20, PY + 66, "sin configuración de VLAN", 16, a.BAD, a.MONO, 600)
    + a.text(PX + 20, PY + 96, "las etiquetas no se respetan", 16, a.BAD, a.MONO, 600), 3)

TK = [(LG, "gestión", a.GREY), (L20, "VID 20", a.AMB), (L30, "VID 30", a.CYAN)]
# 1 · lo que manda el AP
s0, s1 = ph(a, 0)
for k, (yy, lab, c) in enumerate(TK):
    go(a, [(1006, yy), (173, yy)], s0 + 2 + k * 4, s0 + 14 + k * 4, lab, c, hold=s0 + 15 + k * 4)

# 2 · gestión etiquetada en el medio
s0, s1 = ph(a, 1)
go(a, [(1006, LG), (650, LG)], s0 + 2, s0 + 8, "gestión", a.GREY, hold=s1 - 0.5)
during(a, xmark(a, 580, LG, 16), s0 + 8, s1)
for k, (yy, lab, c) in enumerate(TK[1:]):
    go(a, [(1006, yy), (173, yy)], s0 + 4 + k * 3, s0 + 15 + k * 3, lab, c, hold=s0 + 16 + k * 3)
during(a, pill(a, 1152, Y - 14, "sin inform: offline", "bad", anchor="end"), s0 + 9, s1)
during(a, nbox(a, 800, 420, 352, 140, "Caso de LazyAdmin", ["Un lector no logró que su AP", "anduviera hasta dejar la gestión", "sin etiqueta en el switch."], "amb"),
       s0 + 3, s1)

# 3 · corregido
s0, s1 = ph(a, 2)
for k, (yy, lab, c) in enumerate(TK):
    go(a, [(1006, yy), (173, yy)], s0 + 2 + k * 4, s0 + 14 + k * 4, lab, c, hold=s1 - 0.5, still=1)
during(a, pill(a, 1152, Y - 14, "Connected", "ok", anchor="end"), s0 + 12, s1, still=1)
during(a, check(a, 270, Y - 2, 14), s0 + 18, s1, still=1)

# 4 · no administrable
s0, s1 = ph(a, 3)
go(a, [(1006, LG), (173, LG)], s0 + 2, s0 + 13, "gestión", a.GREY, hold=s0 + 14)
for k, (yy, lab, c) in enumerate(TK[1:]):
    go(a, [(1006, yy), (650, yy)], s0 + 4 + k * 3, s0 + 9 + k * 3, lab, c, hold=s1 - 0.5)
    during(a, xmark(a, 580, yy, 15), s0 + 9 + k * 3, s1)
during(a, nbox(a, 800, 420, 352, 140, "Según UniHosted", ["Un switch no administrable", "descarta o pierde las etiquetas:", "los SSID 20 y 30 no llegan."], "bad"),
       s0 + 3, s1)

status(a, 610, [
    (0, 25, "El AP es un trunk: gestión en la nativa y cada SSID por su VLAN.", a.INK, 0),
    (25, 50, "Mismo cable, otra idea de qué es nativa: el AP queda sin gestión.", a.BAD, 0),
    (50, 75, "Las mismas VLAN de punta a punta, con la gestión sin etiqueta.", a.OK, 1),
    (75, 100, "En el camino de un AP con varias VLAN, solo switches administrables.", a.BAD, 0),
])

write(a, 6, "r1", "Un switch de terceros entre el gateway y el AP",
      "Animación en cuatro tiempos con el gateway UniFi, un switch de terceros en el medio y un AP con la gestión sin etiqueta y los SSID en las VLAN 20 y 30. "
      "1: el AP manda la gestión sin etiqueta y las tramas de cada SSID con su etiqueta, VID 20 y VID 30, y todo llega al gateway. "
      "2: si el puerto del switch del medio espera la gestión etiquetada, lo que llega sin etiqueta va a otra VLAN: la gestión no llega, no hay inform y el AP queda offline; "
      "es el caso de un lector de LazyAdmin, que no logró que su AP anduviera hasta dejar la gestión sin etiqueta. "
      "3: corregido, el puerto lleva la gestión sin etiqueta y las VLAN 20 y 30 etiquetadas, igual que espera el AP: todo llega y el AP queda Connected. "
      "4: con un switch no administrable en el medio, según UniHosted, las etiquetas se descartan o se pierden y los SSID 20 y 30 no llegan.",
      [12, 37, 64, 90])
