#!/usr/bin/env python3
"""Lección 11 (Dos WAN), Resumen: el corte de fibra en un local visto de punta a punta.
El módem sigue vivo, los testigos dejan de contestar, las rutas del ISP1 caen tras dos pruebas y el local sigue por el 4G;
abajo, la fila de pings que el técnico cuenta para el legajo."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, GHOST

a = Anim(T=26, kicker="MIKROTIK · DOS WAN · EN LA RED", title="Se corta la fibra en la vereda: el local sigue por el 4G")
a.steps([
    "Normal: sale todo por la fibra; check-gateway prueba los testigos.",
    "Cortan la fibra afuera: el módem contesta, los testigos no.",
    "Dos pruebas perdidas: caen las rutas del ISP1 y entra el 4G.",
    "Vuelve la fibra: los testigos contestan y el ISP1 recupera el lugar.",
], still=2)

# ---- topología
a.add(dev(a, 48, 292, 218, 92, "Cajas y PCs", "192.168.88.0/24", "card"))
a.add(a.box(336, 282, 196, 112, a.INK, a.INK, rx=16) + a.text(356, 318, "Router", 19, "#FFFFFF", a.SANS, 600)
      + a.text(356, 342, "ether1 · ether2", 15, LIGHT, a.MONO) + a.text(356, 364, "masquerade x2", 15, LIGHT, a.MONO))
a.add(dev(a, 614, 182, 236, 88, "Módem fibra", "gw 203.0.113.9", "server"))
a.add(dev(a, 614, 406, 236, 88, "Router 4G", "gw 192.168.8.1", "wifi"))
a.add(dev(a, 928, 286, 224, 104, "Internet", "testigos ISP1:", "globe", sub2="1.1.1.1 · 9.9.9.9"))
SEG = {  # tramos: (x1, y1, x2, y2)
    "lan": (266, 338, 336, 338), "e1": (532, 312, 614, 250), "f": (850, 250, 928, 318),
    "e2": (532, 364, 614, 450), "g": (850, 450, 928, 358)}
for k, (x1, y1, x2, y2) in SEG.items():
    a.add(linea(x1, y1, x2, y2, a.LINE, 5))
a.add(a.text(562, 262, "ether1", 15, a.GREY, a.MONO, 400, "end"))
a.add(a.text(560, 438, "ether2", 15, a.GREY, a.MONO, 400, "end"))


def camino(tramos, color, wins, still=0):
    s = "".join(linea(*SEG[t], color, 5) for t in tramos)
    ventanas(a, s, wins, still=still)


camino(["lan", "e1", "f"], a.OK, [(0, 27), (80, 100)])
camino(["lan", "e2", "g"], a.AMB, [(49.5, 80)], still=1)
# el corte
cx, cy = 889, 284
en(a, f'<path d="M{cx - 11} {cy - 11} L{cx + 11} {cy + 11} M{cx + 11} {cy - 11} L{cx - 11} {cy + 11}" stroke="{a.BAD}" stroke-width="5" stroke-linecap="round"/>'
   + a.text(864, 238, "fibra cortada", 15, a.BAD, a.MONO, 600), 26, 76, still=1)
en(a, a.text(732, 312, "el módem contesta", 15, a.OK, a.SANS, 600, "middle"), 28, 76, still=1)

# pruebas de check-gateway hacia el testigo (cada 10 s en la realidad; acá, comprimido)
IDA = [(560, 292), (622, 280), (842, 280), (884, 300)]
VUELTA = list(reversed(IDA))
for t0 in (3, 13):
    viaje(a, "ping 1.1.1.1", IDA, t0, t0 + 5, bg=a.BLUE, size=14, hold=0.3)
    viaje(a, "respuesta", VUELTA, t0 + 5.5, t0 + 9.5, bg=a.OK, size=14, hold=0.3)
for t0 in (31, 41):
    viaje(a, "ping 1.1.1.1", IDA[:2] + [(800, 280)], t0, t0 + 4.5, bg=a.BLUE, size=14, hold=3)
    en(a, place(pill_c(a, "testigo: sin respuesta", "#FFFFFF", a.BAD, 14), 732, 348), t0 + 4.5, t0 + 8)
for t0 in (78,):
    viaje(a, "ping 1.1.1.1", IDA, t0, t0 + 5, bg=a.BLUE, size=14, hold=0.3)
    viaje(a, "respuesta", VUELTA, t0 + 5.5, t0 + 9.5, bg=a.OK, size=14, hold=0.3)

# ---- estado de las rutas por defecto
SY = 512
a.add(a.text(48, SY + 20, "rutas 0.0.0.0/0", 15, a.GREY, a.MONO))
a.add(a.text(250, SY + 20, "ISP1 · distance=1", 16, a.INK, a.MONO, 600))
a.add(a.text(700, SY + 20, "ISP2 · distance=2", 16, a.INK, a.MONO, 600))
for t0, t1, lab, fg, bg, st in ((0, 49.5, "activa", a.OK, a.OKBG, 0), (49.5, 80, "inactiva", a.BAD, a.BADBG, 1), (80, 100, "activa", a.OK, a.OKBG, 0)):
    en(a, a.pill(434, SY, lab, fg, bg, 14, 28), t0, t1, still=st)
for t0, t1, lab, fg, bg, st in ((0, 49.5, "en espera", a.GREY, GHOST, 0), (49.5, 80, "activa", a.AMB, a.AMBBG, 1), (80, 100, "en espera", a.GREY, GHOST, 0)):
    en(a, a.pill(884, SY, lab, fg, bg, 14, 28), t0, t1, still=st)

# ---- fila de pings de una PC del local
TY = 566
a.add(a.text(48, TY + 22, "ping -t 1.0.0.1", 15, a.GREY, a.MONO))
N, X0, STEP = 22, 214, 42.6
for i in range(N):
    t = 1 + i * 4.5
    col = a.OK if i <= 5 else (a.BAD if i <= 10 else (a.AMB if i <= 17 else a.OK))
    x = X0 + i * STEP
    a.add(a.box(x, TY, 34, 30, "#FFFFFF", a.LINE, rx=6, sw=1.5))
    en(a, a.box(x, TY, 34, 30, col, rx=6), t, 100, still=1)
for i, s, c in ((6, "corte", a.BAD), (11, "por el 4G", a.AMB), (18, "vuelve", a.OK)):
    en(a, a.text(X0 + i * STEP, TY + 50, s, 15, c, a.SANS, 600), 1 + i * 4.5, 100, still=1)

narr(a, [
    (0, 25, "Los testigos están en internet: si contestan, la fibra sirve de verdad.", a.TXT),
    (25, 50, "Con check-gateway al módem esto no se vería: el módem sigue vivo.", a.BAD),
    (50, 75, "Las cajas siguen cobrando por el 4G; anotá cuántos pings se perdieron.", a.AMB),
    (75, 100, "Al volver, contá otra vez: lo que se armó por el 4G puede cortarse.", a.OK),
], y=652, still_idx=2)

escribir(a, "11-r1", "Corte de fibra: el local sigue por el 4G",
         "Animación en cuatro tiempos de un local con dos salidas: las cajas y PCs en 192.168.88.0/24, el router con masquerade por ether1 y ether2, "
         "el módem de fibra con gateway 203.0.113.9 y el router 4G con gateway 192.168.8.1, ambos hacia internet, donde están los testigos 1.1.1.1 y 9.9.9.9. "
         "Abajo, el estado de las rutas por defecto del ISP1 con distance=1 y del ISP2 con distance=2, y una fila de pings de una PC del local a 1.0.0.1. "
         "1: todo sale por la fibra y check-gateway le hace ping al testigo, que contesta. "
         "2: una obra corta la fibra afuera; el módem sigue vivo y contesta, pero los pings al testigo quedan sin respuesta y la fila de pings se pone roja. "
         "3: tras dos pruebas perdidas las rutas del ISP1 quedan inactivas, entra la del ISP2 y el tráfico sale por el 4G. "
         "4: vuelve la fibra, el testigo contesta, las rutas del ISP1 vuelven a activas y el 4G queda en espera; conviene contar de nuevo los pings al volver.",
         [8, 33, 46, 60, 84, 96])
