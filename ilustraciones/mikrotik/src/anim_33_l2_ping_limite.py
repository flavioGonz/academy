#!/usr/bin/env python3
"""Lección 33 (Reglas de protección) · Laboratorio paso 2: ping desde WAN con limit=5,10:packet; lo que excede baja al drop; el resto del ICMP no se toca."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · REGLAS DE PROTECCIÓN · PASO 2", "Ping desde la WAN, con límite",
             ["Un ping suelto (echo request, 8:0) coincide con ping WAN limitado: contesta.",
              "Llega una ráfaga: los primeros entran por el límite de 5 por segundo y ráfaga 10.",
              "Lo que pasa del límite no coincide y baja a ping WAN excedido: drop.",
              "Un ICMP de otro tipo, como fragmentación necesaria, no es 8:0: sigue como antes."], still=2)

dev(a, 48, 200, 220, 96, "Notebook WAN", "192.0.2.50", "ping a la IP WAN", ssize=14)

RULES = [("accept", "defconf: accept established,related,untracked", a.OK, a.OKBG),
         ("drop", "defconf: drop invalid", a.BAD, a.BADBG),
         ("accept", "ping WAN limitado  limit=5,10:packet", a.OK, a.OKBG),
         ("drop", "ping WAN excedido  icmp-options=8:0", a.BAD, a.BADBG),
         ("accept", "defconf: accept ICMP", a.OK, a.OKBG),
         ("drop", "defconf: drop all not coming from LAN", a.BAD, a.BADBG)]
RX, RW, R0, RS, RH = 350, 560, 196, 56, 46
a.add(a.text(RX, R0 - 12, "chain=input", 15, a.GREY, a.MONO))
cy = []
for i, (act, txt, c, bg) in enumerate(RULES):
    y = R0 + i * RS
    cy.append(y + RH / 2)
    nuevo_ = i in (2, 3)
    a.add(a.box(RX, y, RW, RH, a.WHITE, a.BLUE if nuevo_ else a.LINE, rx=11, sw=2))
    a.add(a.pill(RX + 12, y + 9, act, c, bg, 14, 28))
    a.add(a.text(RX + 102, y + 29, txt, 15, a.INK, a.MONO, 600 if nuevo_ else 400))
a.add(a.text(RX + RW, R0 - 12, "en azul, las dos del paso 2", 14, a.BLUE, a.SANS, 600, "end"))
PX = 318
a.add(wire(PX, cy[0], PX, cy[-1], a.LINE, 2, "4 6"))

def dot(c, r=9):
    return f'<circle cx="0" cy="0" r="{r}" fill="{c}" stroke="#FFFFFF" stroke-width="2.5"/>'
def hit(i, t0, t1, c, still=0):
    en(a, ring(a, RX - 3, R0 + i * RS - 3, RW + 6, RH + 6, c, rx=13), t0, t1, still)

OUT = RX + RW + 40
# 1. ping suelto
go(a, "", [(268, 248), (PX, 248), (PX, cy[2]), (RX - 14, cy[2])], 2, 7, hold=0, inner=dot(a.BLUE))
hit(2, 7, 24, a.OK)
go(a, "", [(PX, cy[2] + 14), (PX, 280), (268, 280)], 9, 13, hold=2, inner=dot(a.OK))
en(a, a.text(160, 330, "echo reply", 15, a.OK, a.MONO, 600, "middle"), 11, 24)

# 2 y 3. ráfaga
pas, dro = 0, 0
for k in range(18):
    t0 = 27 + k * 2.6
    ok = k < 10 or k in (12, 15)
    if ok:
        go(a, "", [(268, 248), (PX, 248), (PX, cy[2]), (RX - 14, cy[2])], t0, t0 + 2.4, hold=0.3, inner=dot(a.BLUE, 8))
    else:
        go(a, "", [(268, 248), (PX, 248), (PX, cy[3]), (RX - 14, cy[3])], t0, t0 + 2.8, hold=0.3, inner=dot(a.GREY, 8))
hit(2, 27, 52, a.OK)
en(a, a.text(160, 330, "ráfaga: decenas", 14, a.GREY, a.MONO, 600, "middle") + a.text(160, 350, "por segundo", 14, a.GREY, a.MONO, 600, "middle") + a.text(160, 372, "(en cámara lenta)", 13, a.GREY, a.SANS, 400, "middle"), 27, 75)
hit(3, 53, 75, a.BAD, still=1)
fijo(a, at(dot(a.GREY, 8), RX - 14, cy[3]))

# contadores
a.add(a.box(946, 196, 206, 330, a.INK, rx=16))
a.add(a.text(966, 228, "contadores", 15, SKY, a.MONO))
a.add(a.text(966, 268, "limitado", 15, a.WHITE, a.MONO, 600))
a.add(a.text(966, 360, "excedido", 15, a.WHITE, a.MONO, 600))
okk = [k for k in range(18) if k < 10 or k in (12, 15)]
arr = [7] + [27 + k * 2.6 + 2.4 for k in okk]
lim = [(0, arr[0], "0", MINT)]
for n, t in enumerate(arr):
    lim.append((t, arr[n + 1] if n + 1 < len(arr) else 100, str(n + 1), MINT))
flip(a, 966, 306, lim, size=26, still_idx=len(lim) - 1)
exc = [(0, 55, "0", ROSE)]
vals = [k for k in range(18) if not (k < 10 or k in (12, 15))]
for n, k in enumerate(vals):
    t = 27 + k * 2.6 + 2.8
    nxt = 27 + vals[n + 1] * 2.6 + 2.8 if n + 1 < len(vals) else 100
    exc.append((t, nxt, str(n + 1), ROSE))
flip(a, 966, 398, exc, size=26, still_idx=len(exc) - 1)
en(a, a.text(966, 440, "drop, sin", 15, ROSE, a.SANS, 600) + a.text(966, 462, "respuesta", 15, ROSE, a.SANS, 600), 56, 100, still=1)

a.add(note(a, 48, 540, 862, 58, "", ["limit=5,10:packet: hasta 5 paquetes por segundo, con una ráfaga de 10. Lo que no entra, sigue a la regla de abajo."], "info"))

# 4. otro ICMP
go(a, "", [(268, 248), (PX, 248), (PX, cy[4]), (RX - 42, cy[4])], 78, 85, hold=12, inner=pillc(a, "tipo 3", bg=a.CYAN, size=13, h=26))
en(a, a.text(RX + RW - 14, cy[2] + 5, "no es 8:0", 14, a.GREY, a.MONO, 600, "end") + a.text(RX + RW - 14, cy[3] + 5, "no es 8:0", 14, a.GREY, a.MONO, 600, "end"), 80, 100)

narr(a, [
    (0, 25, "icmp-options=8:0 es solo el echo request: el ping de toda la vida.", a.TXT),
    (25, 50, "limit cuenta paquetes por tiempo: mientras no se pase, la regla coincide.", a.OK),
    (50, 75, "Un barrido o una inundación de pings no consigue respuesta del router.", a.BAD),
    (75, 100, "Traceroute y el ajuste de MTU necesitan esos otros ICMP: no se cortan.", a.TXT),
], still_idx=2)

escribir(a, "33-l2.svg", "Ping desde WAN con límite",
         "Animación en cuatro tiempos con la notebook WAN (192.0.2.50) que hace ping a la IP WAN del router y la cadena input con seis reglas: accept established, related y untracked; "
         "drop invalid; las dos nuevas del paso 2, ping WAN limitado con limit=5,10:packet y ping WAN excedido con icmp-options=8:0; accept ICMP de fábrica y drop all not coming from LAN. "
         "A la derecha, los contadores de las dos reglas nuevas. 1: un ping suelto coincide con ping WAN limitado y vuelve el echo reply. "
         "2: llega una ráfaga de pings y los primeros entran por el límite de 5 por segundo con ráfaga de 10. 3: lo que pasa del límite no coincide con la regla limitada, baja a ping WAN excedido "
         "y se descarta sin respuesta. 4: un ICMP de otro tipo, como fragmentación necesaria (tipo 3), no es 8:0: las dos reglas nuevas no lo tocan y sigue como antes.",
         [10, 38, 62, 70, 92])
