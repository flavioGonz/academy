"""Teoría de Día y noche: alarma demorada en modo día y el pulsador que la anula."""
from _anim_bi import *

caps = ["Modo día: un detector da prealarma y arranca el tiempo (3 min de ejemplo).",
        "El personal investiga mientras corre el tiempo.",
        "Vence el tiempo sin que se confirme falsa alarma: alarma general.",
        "Si alguien acciona un pulsador durante la demora: alarma inmediata."]
a = new(24, "Retardos", "La demora da tiempo a investigar; el pulsador la corta", caps, still=3)

a.add(a.box(48, 200, 200, 120, a.WHITE, a.LINE, rx=14))
a.add(det(a, 100, 260, 30)); a.add(a.text(150, 266, "detector", 16, a.INK, a.SANS, 600))
vis(a, led(a, 100, 260, a.BAD, 6), 0, 2)
a.add(card(a, 330, 200, 300, 120, "Panel", "modo día", dark=True))
vis(a, a.pill(480, 350, "prealarma al personal", a.AMB, a.AMBBG, anchor="middle"), 0, 1)
# temporizador
X0, X1 = 330, 1100
a.add(a.box(X0, 420, X1 - X0, 34, a.SLATE, a.LINE, rx=17, sw=2))
for k, t in enumerate(("0", "1 min", "2 min", "3 min")):
    a.add(a.text(X0 + (X1 - X0) * k / 3, 486, t, 15, a.GREY, a.MONO, 400, "middle"))
s0, _ = ph(a, 0)
_, e1 = ph(a, 1)
grow = a.keyframes([(0, 0), (s0 + 3, 0), (e1, 1), (100, 1)], "transform", "scaleX({})")
a.add(a.group(a.box(X0, 420, X1 - X0, 34, a.AMB, rx=17), grow, a.show(s0 + 3, e1 + 25), still=0, origin=f"{X0}px 437px"))
vis(a, a.box(X0, 420, (X1 - X0) * 0.4, 34, a.AMB, rx=17) + a.text(X0 + (X1 - X0) * 0.4 + 14, 444, "demora cortada", 16, a.BAD, a.SANS, 600), 3)
vis(a, a.box(700, 200, 220, 120, a.WHITE, a.LINE, rx=14) + a.text(720, 250, "Personal", 18, a.INK, a.SANS, 600) + a.text(720, 278, "investiga", 15, a.GREY, a.MONO), 1)
vis(a, a.pill(1150, 260, "ALARMA GENERAL", a.WHITE, a.BAD, size=18, anchor="end"), 2)
# pulsador
vis(a, a.box(700, 200, 120, 120, a.BAD, rx=14) + a.box(730, 230, 60, 60, a.WHITE, rx=6) + a.box(745, 255, 30, 10, a.BAD, rx=3), 3)
vis(a, a.pill(1150, 260, "ALARMA INMEDIATA", a.WHITE, a.BAD, size=18, anchor="end"), 3)
vis(a, a.text(840, 360, "el pulsador anula el retardo", 17, a.BAD, a.SANS, 600), 3)
a.add(a.text(48, 560, "BS 5839-1 limita la demora a 6 minutos. El tiempo real lo fija el proyecto firmado.", 17, a.TXT))
a.add(a.text(48, 590, "Ningún retardo sobre pulsadores: un pulsador es una persona que vio fuego.", 17, a.BAD, a.SANS, 600))
write(a, "12-t1.svg", "La demora y el pulsador", [12, 37, 62, 90])
