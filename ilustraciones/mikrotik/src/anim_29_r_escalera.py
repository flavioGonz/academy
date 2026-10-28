#!/usr/bin/env python3
"""Lección 29 (Diagnóstico por terminal), Resumen: la escalera de pings en una obra donde "no anda internet".
Contestan la LAN, el gateway y 1.1.1.1; el ping a un nombre ni sale: el router le pregunta a su DNS, no hay respuesta
y da "resolve failed". Conclusión: la conexión anda y lo que falla es el DNS."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=26, kicker="MIKROTIK · DIAGNÓSTICO · EN LA RED", title="\"No anda internet\": la escalera, de adentro hacia afuera")
a.steps([
    "Escalón 1: un equipo de la LAN contesta.",
    "Escalón 2: el gateway del proveedor contesta.",
    "Escalón 3: 1.1.1.1 contesta: hay internet.",
    "Escalón 4: el nombre no se resuelve y el ping ni sale.",
    "Anda el 3 y falla el 4: el problema es el DNS.",
], still=3)

B = [(48, "Notebook", "192.168.88.254", "laptop", False), (274, "Router", "la terminal", None, True),
     (500, "Gateway ISP", "203.0.113.1", "server", False), (726, "Internet", "1.1.1.1", "globe", False),
     (952, "DNS del router", "198.51.100.53", "cloud", False)]
CX = []
for x, t, s, ic, dk in B:
    a.add(dev(a, x, 176, 200, 84, t, s, ic, dark=dk))
    CX.append(x + 100)
for i in range(4):
    a.add(linea(B[i][0] + 200, 218, B[i + 1][0], 218, a.LINE, 4))

LY = 292
R0 = (CX[1], LY)


def ping(i, t0, ok=True, label="ping"):
    tgt = (CX[i], LY)
    viaje(a, label, [R0, tgt], t0, t0 + 5, bg=a.BLUE, size=14, hold=0.3)
    if ok:
        viaje(a, "respuesta", [tgt, R0], t0 + 5.5, t0 + 10, bg=a.OK, size=14, hold=0.3)


ping(0, 2)
ping(2, 22)
ping(3, 42)
viaje(a, "A mikrotik.com?", [R0, (CX[4], LY)], 62, 68, bg=a.AMB, size=14, hold=1)
en(a, marca(a, CX[4] + 90, 176, ok=False) + a.text(CX[4], LY + 2, "sin respuesta", 15, a.BAD, a.SANS, 700, "middle"), 69, 100, still=1)
fijo(a, place(pill_c(a, "A mikrotik.com?", "#FFFFFF", a.AMB, 14), (CX[1] + CX[4]) / 2, LY))

# ---- la escalera
RUNGS = [("1", "LAN", "/ping 192.168.88.254 count=3"), ("2", "gateway", "/ping 203.0.113.1 count=3"),
         ("3", "internet", "/ping 1.1.1.1 count=3"), ("4", "nombre", "/ping mikrotik.com count=3")]
RES = [("contesta", a.OK, a.OKBG, 12), ("contesta", a.OK, a.OKBG, 32), ("contesta", a.OK, a.OKBG, 52), ("resolve failed", a.BAD, a.BADBG, 69)]
for i, ((n, k, cmd), (r, fg, bg, tr)) in enumerate(zip(RUNGS, RES)):
    y = 556 - i * 62
    x = 48 + i * 30
    w = 620
    row = (a.box(x, y, w, 50, a.WHITE, a.LINE, rx=12) + a.box(x + 10, y + 9, 32, 32, a.INK, rx=16)
           + a.text(x + 26, y + 31, n, 16, "#FFFFFF", a.MONO, 700, "middle") + a.text(x + 54, y + 32, k, 16, a.INK, a.SANS, 700)
           + a.text(x + 150, y + 32, cmd, 15, a.TXT, a.MONO))
    t_on = i * 20
    en(a, row, t_on, 100, still=1)
    en(a, a.box(x, y, w, 50, "none", a.BLUE, rx=12, sw=2.5), t_on, t_on + 20, still=1 if i == 3 else 0)
    en(a, a.pill(x + w - 14, y + 11, r, fg, bg, 14, 28, "end"), tr, 100, still=1)

# ---- qué descarta cada escalón
NX, NY, NW = 800, 314, 352
a.add(a.box(NX, NY, NW, 292, a.INK, rx=16) + a.text(NX + 22, NY + 34, "Lo que ya sabés", 17, "#FFFFFF", a.HEAD, 600))
SAB = [("cable, puerto y bridge bien", 12), ("la WAN y el proveedor llegan", 32), ("la ruta por defecto anda", 52),
       ("el DNS no contesta", 69)]
for i, (s, t) in enumerate(SAB):
    c = CORAL if i == 3 else MINT
    yy = NY + 76 + i * 36
    en(a, marca(a, NX + 34, yy - 6, ok=(i != 3), r=11) + a.text(NX + 56, yy, s, 16, c, a.SANS, 600), t, 100, still=1)
en(a, a.box(NX + 16, NY + 214, NW - 32, 62, a.NAVY2, rx=10) + a.text(NX + 32, NY + 240, "Mirá /ip/dns: qué servidores", 16, GOLD, a.SANS, 600)
   + a.text(NX + 32, NY + 264, "usa el router y si contestan", 16, GOLD, a.SANS, 600), 80, 100)

narr(a, [
    (0, 20, "Primero lo más cercano: si la LAN no contesta, lo de afuera no importa.", a.TXT),
    (20, 40, "La WAN está bien: cable al módem, IP o PPPoE.", a.TXT),
    (40, 60, "Con 1.1.1.1 contestando, la conexión a internet funciona.", a.OK),
    (60, 80, "Para un nombre, el router pregunta antes a su DNS; sin respuesta, no hay a quién hacerle ping.", a.BAD),
    (80, 100, "El cliente ve \"no anda internet\", pero lo que falla es un solo servicio.", a.AMB),
], y=644, still_idx=3)

escribir(a, "29-r1", "La escalera de pings en la obra",
         "Animación en cinco tiempos de un cliente que dice que no anda internet. Arriba, en fila: la notebook de la LAN 192.168.88.254, el router con la terminal, "
         "el gateway del proveedor 203.0.113.1, internet con 1.1.1.1 y el DNS que usa el router, 198.51.100.53, de ejemplo. Abajo, la escalera de cuatro escalones con su comando, "
         "y a la derecha lo que ya se sabe. 1: /ping 192.168.88.254 contesta: cable, puerto y bridge bien. 2: /ping 203.0.113.1 contesta: la WAN y el proveedor llegan. "
         "3: /ping 1.1.1.1 contesta: la ruta por defecto anda y hay internet. "
         "4: /ping mikrotik.com no llega a salir: el router le pregunta el nombre a su DNS, no hay respuesta y la terminal dice resolve failed. "
         "5: anda el escalón 3 y falla el 4, así que el problema es el DNS: mirá /ip/dns.",
         [8, 28, 48, 66, 72, 90])
