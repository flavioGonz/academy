#!/usr/bin/env python3
"""Lección 12 · Laboratorio, paso 4: Port Manager > Time Machine del puerto del AP. El enlace del puerto se cae y
vuelve; todos los clientes de ese AP se desconectan a la misma hora; el Time Machine del puerto lo muestra y se cruza
con el historial del cliente. Horas de ejemplo. Fuentes: lab.md (pasos 2 a 4) y theory_md de la lección (Time Machine
de puertos con filtro de clientes que se conectan y desconectan seguido, serie 10.6)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Mirar primero", "¿El uplink flapeó? La misma hora en el puerto y en el cliente", [
    "El puerto 3 del switch conecta al AP; sus clientes navegan.",
    "A las 10:02 el enlace del puerto 3 se cae y vuelve: el AP queda sin salida.",
    "Todos los clientes de ese AP se cortan a la misma hora, no uno solo.",
    "Time Machine del puerto marca 10:02, igual que el historial: fue el uplink.",
], still=3, paso=4)

a.add(dev(a, 48, 190, 280, 90, "Switch", "puerto 3 → AP", icon="server"))
a.add(dev(a, 520, 190, 260, 90, "AP", "uplink: puerto 3", ap=True))
UP = wire(328, 235, 520, 235, a.BLUE, 4)
DOWN = wire(328, 235, 520, 235, a.BAD, 4, "6 8")
vis(a, UP, 0)
s0, s1 = ph(a, 1)
during(a, UP, s0, s0 + 6)
during(a, DOWN + xmark(a, 424, 235, 15), s0 + 6, s0 + 15)
during(a, UP, s0 + 15, 100, still=1)
during(a, pill(a, 424, 196, "link down", "bad", anchor="middle"), s0 + 6, s0 + 15)
during(a, pill(a, 424, 196, "link up", "ok", anchor="middle"), s0 + 15, s1)

PH = [(930, 236), (1010, 236), (1090, 236)]
WAVE = "".join(arcs(a, 790, 235, [26, 46, 66], a.OK, facing=0, spread=34, width=3))
for x, y in PH:
    a.add(phone_icon(a, x, y))
    vis(a, xmark(a, x, y - 38, 12), 2)
vis(a, WAVE, 0, 1)
vis(a, WAVE, 3)

# dos líneas de tiempo
TX0, TX1 = 260, 1120
t2x = lambda h, m: TX0 + ((h - 9) * 60 + m) / 120 * (TX1 - TX0)  # noqa: E731  (de 9:00 a 11:00)
ROWS = [(360, "Puerto 3 · Time Machine"), (470, "Historial de los clientes")]
for y, lab in ROWS:
    a.add(a.text(48, y + 6, lab, 16, a.INK, a.SANS, 600))
    a.add(wire(TX0, y, TX1, y, a.LINE, 4))
for h in (9, 10, 11):
    x = t2x(h, 0)
    a.add(a.text(x, 540, f"{h}:00", 15, a.GREY, a.MONO, 400, "middle"))
    a.add(wire(x, 340, x, 520, a.LINE, 1.5, "3 6"))
X = t2x(10, 2)
s0, s1 = ph(a, 1)
during(a, pill(a, X + 40, 346, "10:02 link down / up", "bad"), s0 + 8, 100, still=1)
during(a, f'<circle cx="{X}" cy="360" r="9" fill="{a.BAD}"/>', s0 + 8, 100, still=1)
s0, s1 = ph(a, 2)
for k in range(3):
    during(a, f'<circle cx="{X}" cy="{470 + (k - 1) * 0}" r="9" fill="{a.BAD}"/>', s0 + 3, 100, still=1)
during(a, pill(a, X + 40, 456, "10:02 · 3 desconexiones", "bad"), s0 + 3, 100, still=1)
s0, s1 = ph(a, 3)
during(a, a.box(X - 30, 318, 60, 182, "none", GOLD, rx=12, sw=3), s0 + 2, 100, still=1)
during(a, a.box(48, 560, 640, 40, a.OKBG, None, rx=10) + a.text(64, 586, "Misma hora, todos juntos: el uplink, no el WiFi.", 16, a.OK, a.SANS, 600),
       s0 + 5, 100, still=1)

status(a, 630, [
    (0, 25, "Si el cable del AP falla, en el aire no se ve: se ve en el puerto.", a.INK, 0),
    (25, 50, "Sin salida, el AP no tiene adónde mandar el tráfico de nadie.", a.BAD, 0),
    (50, 75, "Muchos clientes a la vez apuntan al AP o a su cable; uno solo, al cliente.", a.AMB, 0),
    (75, 100, "Revisá cable y puerto antes de tocar canales o potencia.", a.OK, 1),
], x=1152, anchor="end", size=16)

write(a, 12, "l1", "Time Machine del puerto del AP",
      "Animación en cuatro tiempos del paso 4 con el switch, su puerto 3 que va al AP, tres celulares en ese AP y dos líneas de tiempo de 9:00 a 11:00: "
      "el Time Machine del puerto 3 y el historial de los clientes. Horas de ejemplo. "
      "1: el enlace del puerto 3 está arriba y los clientes navegan. "
      "2: a las 10:02 el enlace se cae y vuelve, link down y link up, y el AP queda unos segundos sin salida; el Time Machine del puerto lo marca. "
      "3: los tres clientes del AP se desconectan a la misma hora; en su historial aparecen tres desconexiones a las 10:02. "
      "4: la misma hora en las dos líneas, y todos juntos: fue el uplink, no el WiFi. Se revisan cable y puerto antes de tocar canales o potencia.",
      [12, 40, 64, 92])
