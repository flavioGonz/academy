#!/usr/bin/env python3
"""Lección 12 · teoría: traceroute manda paquetes con TTL cada vez mayor y anota quién avisa que se le terminó."""
from _anim_mikrotik_1_13 import *

a = Anim(T=28, kicker="MIKROTIK · LECCIÓN 12 · TRACEROUTE", title="traceroute: un TTL más en cada vuelta")
a.steps([
    "TTL=1: el primer salto lo descarta y avisa. Anotás el salto 1.",
    "TTL=2: pasa el primero y se termina en el segundo. Anotás el salto 2.",
    "TTL=3: llega a 8.8.8.8, que contesta. Ahí termina el recorrido.",
    "Si el camino se corta, la lista muestra hasta qué salto llega.",
], still=2)

Y = 280
X = [148, 438, 728, 1018]
L = lambda i: X[i] - 75
R = lambda i: X[i] + 75   # centros: router, salto 1, salto 2, destino


def p(lab, col):
    return pkt(a, lab, col, size=13, h=28)


a.add(line(X[0], Y, X[3], Y, a.LINE, 3))
# vueltas (paquetes antes que las cajas)
GO, BK = Y - 22, Y + 22
a.add(travel(a, p("TTL 1", a.BLUE), [(R(0) + 45, GO), (L(1) - 45, GO)], 2, 7, hold=0.3))
a.add(travel(a, p("aviso", a.AMB), [(L(1) - 45, BK), (R(0) + 45, BK)], 8, 13, hold=1))
a.add(travel(a, p("TTL 2", a.BLUE), [(R(0) + 45, GO), (L(2) - 45, GO)], 27, 35, hold=0.3))
a.add(travel(a, p("aviso", a.AMB), [(L(2) - 45, BK), (R(0) + 45, BK)], 36, 44, hold=1))
a.add(travel(a, p("TTL 3", a.BLUE), [(R(0) + 45, GO), (L(3) - 45, GO)], 52, 62, hold=0.3))
a.add(travel(a, p("resp.", a.OK), [(L(3) - 45, BK), (R(0) + 45, BK)], 63, 73, hold=1))
a.add(travel(a, p("TTL 3", a.BLUE), [(R(0) + 45, GO), (R(2) + 40, GO)], 77, 85, hold=12))
a.add(during(a, xmark(a, R(2) + 100, GO), 85, 98.5))
a.add(still_only(a, place(a, p("TTL 3", a.BLUE), L(3) - 45, GO) + place(a, p("resp.", a.OK), R(1) + 70, BK)))

NAMES = [("Router", "/tool/traceroute"), ("Salto 1", "tu gateway"), ("Salto 2", "del proveedor"), ("8.8.8.8", "destino")]
for i, (n, s) in enumerate(NAMES):
    a.add(device(a, X[i] - 75, 226, 150, 108, n, s if i else "traceroute", dark=(i == 0), ssize=13))
# TTL que se gasta en cada salto
for i, t0 in ((1, 6), (2, 33)):
    a.add(during(a, a.pill(X[i], 346, "TTL 1 → 0", a.AMB, a.AMBBG, 13, 26, "middle"), t0, t0 + 12))

# lista que se va armando
a.add(a.box(48, 404, 640, 196, a.INK))
a.add(a.text(66, 434, "/tool/traceroute 8.8.8.8", 14, SKY, a.MONO))
rows = [(13, "1", "salto 1", MINT), (44, "2", "salto 2", MINT), (73, "3", "8.8.8.8", MINT)]
for k, (t0, n, h, col) in enumerate(rows):
    a.add(a.group(a.text(66, 472 + k * 34, n, 16, SKY, a.MONO, 600) + a.text(110, 472 + k * 34, h, 16, col, a.MONO, 600),
                  a.keyframes([(0, 0), (t0, 0), (t0 + 1, 1), (75, 1), (75.6, 0 if k == 2 else 1), (98.5, 0 if k == 2 else 1), (100, 0)]), still=1))
a.add(during(a, a.text(66, 472 + 2 * 34, "3", 16, SKY, a.MONO, 600) + a.text(110, 472 + 2 * 34, "sin respuesta", 16, GOLD, a.MONO, 600), 86, 98.5))
a.add(a.note(712, 404, 440, 196, "Pregunta, no mira", ["ping y traceroute generan tráfico de", "prueba: dicen si hay camino y hasta", "qué salto llega.", "", "Lo que hace un equipo ahora lo ve Torch."], "info") if hasattr(a, "note") else
      note(a, 712, 404, 440, 196, "Pregunta, no mira", ["ping y traceroute generan tráfico de", "prueba: dicen si hay camino y hasta", "qué salto llega.", "", "Lo que hace un equipo ahora lo ve Torch."], "info"))

p_, pre = out(12, 2)
a.write(p_, title="Cómo funciona traceroute",
        desc="Animación en cuatro tiempos con el router, un primer salto (tu gateway), un segundo salto del proveedor y el destino 8.8.8.8. 1: sale un paquete con TTL=1; "
             "el primer salto lo descarta y avisa que se le terminó; la lista anota el salto 1. 2: sale otro con TTL=2; pasa el primer salto y se termina en el segundo, que "
             "avisa; la lista anota el salto 2. 3: con TTL=3 llega a 8.8.8.8, que contesta, y termina el recorrido. 4: si el camino se corta después del segundo salto, el "
             "tercero queda sin respuesta y la lista muestra hasta dónde llega.",
        preview=[10, 40, 66, 92], prefix=pre)
