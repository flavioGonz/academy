#!/usr/bin/env python3
"""Lección 12 · Resumen, "Cómo se ve en la red": los tres patrones del historial de conexión y roaming según Purple.
Roam en el borde (lo esperado), desconexión y reconexión (hueco de cobertura) y ping-pong (dos AP que llegan con
potencia pareja de más); después, un solo cambio y probar. Fuentes: idea_md, theory_md y lab.md de la lección."""
from _anim_red_unifi import *  # noqa

a = new(28, "Mirar primero", "Tres patrones en el historial del cliente", [
    "Roam en el borde: baja la señal del AP 1 y el celular pasa al AP 2. Lo esperado.",
    "Hueco de cobertura: pierde el AP 1 antes de encontrar el AP 2.",
    "Ping-pong: quieto en el medio, va y viene entre dos AP que le llegan parejos.",
    "Un solo cambio: bajar la potencia de un AP, probar con el mismo cliente.",
], still=2)

Y = 300
A1, A2 = (160, Y), (1040, Y)
a.add(f'<defs><clipPath id="pl12"><rect x="48" y="178" width="1104" height="232" rx="16"/></clipPath></defs>')
a.add(a.box(48, 178, 1104, 232, a.WHITE, a.LINE, rx=16))


def cells(r1, r2, op=0.12):
    return (f'<g clip-path="url(#pl12)"><circle cx="{A1[0]}" cy="{Y}" r="{r1}" fill="{a.BLUE}" fill-opacity="{op}" stroke="{a.BLUE}" stroke-width="2.5" stroke-dasharray="8 6"/>'
            f'<circle cx="{A2[0]}" cy="{Y}" r="{r2}" fill="{a.CYAN}" fill-opacity="{op}" stroke="{a.CYAN}" stroke-width="2.5" stroke-dasharray="8 6"/></g>')


vis(a, cells(500, 500), 0)
vis(a, cells(360, 360), 1)
vis(a, cells(620, 620), 2)
vis(a, cells(560, 420), 3)
for (x, y), lab in ((A1, "AP 1"), (A2, "AP 2")):
    a.add(ap_icon(a, x, y, 24) + a.text(x, y - 40, lab, 16, a.INK, a.SANS, 600, "middle"))

# celular
PH = phone_icon(a, 0, 0)
s = a.spans
kf = [(0, 260, Y + 40), (s[0][0] + 2, 260, Y + 40), (s[0][1] - 4, 940, Y + 40), (s[1][0] + 0.5, 260, Y + 40), (s[1][0] + 2, 260, Y + 40),
      (s[1][1] - 4, 940, Y + 40), (s[2][0] + 0.5, 600, Y + 40), (100, 600, Y + 40)]
a.add(a.group(PH, a.move(kf), a.show(0, 100, 0.3), still=0))
still_only(a, phone_icon(a, 600, Y + 40))

# enlaces por tiempo
def link(t0, t1, ap, col=None, still=0, x=None):
    xx = x if x is not None else 600
    during(a, poly([(xx, Y + 18), (ap[0] + (26 if ap == A1 else -26), Y)], col or a.OK, 2.5, "5 5"), t0, t1, still=still)


s0, s1 = ph(a, 0)
during(a, pill(a, 600, 196, "borde de celda: cambia de AP", "ok", anchor="middle"), s0 + 12, s1 - 1)
s0, s1 = ph(a, 1)
during(a, a.box(470, 190, 260, 40, a.BADBG, None, rx=10) + a.text(600, 216, "sin señal de ninguno", 16, a.BAD, a.SANS, 600, "middle"), s0 + 10, s0 + 16)
s0, s1 = ph(a, 2)
for k in range(4):
    t = s0 + 1 + k * 6
    link(t, t + 5.6, A1 if k % 2 == 0 else A2, a.AMB, still=1 if k == 0 else 0)
s0, s1 = ph(a, 3)
link(s0 + 3, 100, A1, a.OK, still=0)
during(a, pill(a, 600, 196, "potencia del AP 2 un nivel más baja", "info", anchor="middle"), s0 + 2, 100)

# historial
HX, HY = 48, 432
a.add(a.box(HX, HY, 1104, 150, a.WHITE, a.LINE, rx=16))
a.add(a.text(HX + 20, HY + 32, "Historial de conexión y roaming del cliente", 16, a.INK, a.SANS, 600))


def evs(i, items):
    s = ""
    for j, (txt, kind) in enumerate(items):
        s += pill(a, HX + 20 + j * 270, HY + 56, txt, kind)
    return s


vis(a, evs(0, [("10:02 roam AP 1 → AP 2", "ok")]) + a.text(HX + 20, HY + 124, "Lectura: lo esperado, nada que tocar.", 16, a.OK, a.SANS, 600), 0)
vis(a, evs(1, [("10:02 desconexión", "bad"), ("10:03 reconexión AP 2", "amb")]) + a.text(HX + 20, HY + 124, "Lectura: hueco de cobertura, o un equipo que no tolera una función.", 16, a.BAD, a.SANS, 600), 1)
vis(a, evs(2, [("10:02 AP 1 → AP 2", "amb"), ("10:03 AP 2 → AP 1", "amb"), ("10:04 AP 1 → AP 2", "amb")])
    + a.text(HX + 20, HY + 124, "Lectura: los dos AP le llegan con potencia pareja de más.", 16, a.AMB, a.SANS, 600), 2)
vis(a, evs(3, [("10:20 conectado AP 1", "ok")]) + a.text(HX + 20, HY + 124, "Un cambio, la misma prueba. Si empeora, volvés lo último que tocaste.", 16, a.OK, a.SANS, 600), 3)

status(a, 628, [
    (0, 25, "Antes de tocar nada, el historial: qué le pasó al cliente y a qué hora.", a.INK, 0),
    (25, 50, "Un hueco se arregla con cobertura: un AP más o cable, no con Fast Roaming.", a.INK, 0),
    (50, 75, "El ping-pong no es mala suerte: dos celdas que se pisan de más.", a.AMB, 1),
    (75, 100, "Cambiá una cosa, probala y recién después la siguiente.", a.OK, 0),
])

write(a, 12, "r1", "Tres patrones en el historial del cliente",
      "Animación en cuatro tiempos con el AP 1 y el AP 2 en los extremos de un local, un celular y abajo el historial de conexión y roaming del cliente. "
      "1: el celular camina, la señal del AP 1 baja y en el borde de la celda pasa al AP 2: el historial muestra un roam, lo esperado. "
      "2: con celdas que no llegan a tocarse, el celular pierde el AP 1 antes de encontrar el AP 2: desconexión y reconexión, un hueco de cobertura o un equipo que no tolera una función. "
      "3: el celular quieto en el medio va y viene entre el AP 1 y el AP 2: ping-pong, los dos le llegan con potencia pareja de más. "
      "4: un solo cambio, la potencia del AP 2 un nivel más baja, y la misma prueba: queda conectado al AP 1; si empeora, se vuelve lo último que se tocó.",
      [14, 38, 64, 92])
