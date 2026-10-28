#!/usr/bin/env python3
"""Lección 33 (Reglas de protección) · Resumen: lo que llega por la WAN y en qué regla de fábrica queda cada cosa."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · REGLAS DE PROTECCIÓN · EN LA RED", "Lo que llega por la WAN, regla por regla",
             ["Vuelve la respuesta de una descarga de la PC: established, pasa arriba de todo.",
              "Un bot prueba SSH y otro el DNS del router: input, drop.",
              "Una conexión nueva a la LAN sin port forwarding: forward, drop.",
              "Lo publicado con dst-nat pasa: el drop de forward lo exceptúa."], still=3)

SRC = [("Sitio web", "respuesta de una descarga", "isp"),
       ("Bot", "SSH 22 y DNS 53 al router", "bad"),
       ("Desde la WAN", "nueva, a 192.168.88.20", "bad"),
       ("Celular del dueño", "a la IP pública :8000", "isp")]
for i, (t, s_, k) in enumerate(SRC):
    dev(a, 48, 188 + i * 100, 236, 82, t, s_, kind=k, ssize=13, tsize=17)
SY = [229 + i * 100 for i in range(4)]
dev(a, 916, 210, 236, 82, "PC", "192.168.88.20", ssize=14)
dev(a, 916, 440, 236, 82, "NVR publicado", "192.168.88.50:8000", ssize=14)

# router con las dos cadenas
RX, RW = 332, 540
a.add(a.box(RX, 178, RW, 400, a.INK, rx=18))
IN = ["DNS no desde WAN (udp y tcp 53)",
      "defconf: accept established,related",
      "defconf: drop invalid",
      "defconf: accept ICMP",
      "defconf: drop all not coming from LAN"]
FW = ["defconf: fasttrack",
      "defconf: accept established,related",
      "defconf: drop invalid",
      "defconf: drop all from WAN not DSTNATed"]
a.add(a.text(RX + 20, 206, "input · al router", 15, SKY, a.MONO, 600))
a.add(a.text(RX + 20, 404, "forward · a la LAN", 15, SKY, a.MONO, 600))
iy, fy = [], []
for i, r in enumerate(IN):
    y = 216 + i * 34
    iy.append(y + 14)
    a.add(a.box(RX + 16, y, RW - 32, 28, a.NAVY2, rx=7))
    a.add(a.text(RX + 30, y + 20, r, 14, a.WHITE, a.MONO))
for i, r in enumerate(FW):
    y = 414 + i * 34
    fy.append(y + 14)
    a.add(a.box(RX + 16, y, RW - 32, 28, a.NAVY2, rx=7))
    a.add(a.text(RX + 30, y + 20, r, 14, a.WHITE, a.MONO))

def rr(y, t0, t1, c, still=0):
    en(a, ring(a, RX + 13, y - 17, RW - 26, 34, c, rx=9, sw=2.5), t0, t1, still)

def dot(c):
    return f'<circle cx="0" cy="0" r="11" fill="{c}" stroke="#FFFFFF" stroke-width="3"/>'

LX = RX - 22
# 1. respuesta established a la PC
go(a, "", [(284, SY[0]), (LX, SY[0]), (LX, fy[0])], 2, 7, hold=0, inner=dot(a.OK))
go(a, "", [(LX, fy[0]), (RX + RW + 22, fy[0]), (RX + RW + 22, 251), (916, 251)], 8, 15, hold=6, inner=dot(a.OK))
rr(fy[0], 7, 25, MINT)
en(a, a.text(RX + RW - 30, fy[0] + 5, "established", 13, MINT, a.MONO, 600, "end"), 7, 25)

# 2. bot: DNS y SSH
go(a, "", [(284, SY[1]), (LX, SY[1]), (LX, iy[0])], 27, 32, hold=8, inner=dot(a.BAD))
rr(iy[0], 32, 50, ROSE)
go(a, "", [(284, SY[1] + 14), (LX - 26, SY[1] + 14), (LX - 26, iy[4])], 36, 41, hold=8, inner=dot(a.BAD))
rr(iy[4], 41, 50, ROSE)
en(a, a.text(270, SY[1] + 33, "sin respuesta", 14, a.BAD, a.MONO, 600, "end"), 42, 50)

# 3. nueva a la LAN sin dst-nat
go(a, "", [(284, SY[2]), (LX, SY[2]), (LX, fy[3])], 52, 58, hold=16, inner=dot(a.BAD))
rr(fy[3], 58, 75, ROSE)
en(a, a.text(270, SY[2] + 33, "sin respuesta", 14, a.BAD, a.MONO, 600, "end"), 60, 75)

# 4. lo publicado
go(a, "", [(284, SY[3]), (LX, SY[3]), (LX, fy[3])], 77, 82, hold=0, inner=dot(a.OK))
go(a, "", [(LX, fy[3]), (RX + RW + 22, fy[3]), (RX + RW + 22, 481), (916, 481)], 83, 90, hold=10, inner=dot(a.OK))
en(a, ring(a, RX + 13, fy[3] - 17, RW - 26, 34, GOLD, rx=9, sw=2.5) + a.text(RX + RW - 30, fy[3] + 5, "dstnat: no aplica", 13, GOLD, a.MONO, 600, "end"), 81, 100, still=1)
fijo(a, at(dot(a.OK), RX + RW + 22, 481))

narr(a, [
    (0, 25, "Arriba va lo establecido: la mayoría del tráfico sale ahí, sin mirar el resto.", a.OK),
    (25, 50, "input cuida al router: lo que no aceptaste arriba, desde afuera no entra.", a.BAD),
    (50, 75, "forward cuida a la LAN: desde la WAN, lo nuevo no pasa.", a.BAD),
    (75, 100, "Un port forwarding es la única excepción: connection-nat-state=dstnat.", a.AMB),
], still_idx=3)

escribir(a, "33-r1.svg", "Lo que llega por la WAN",
         "Animación en cuatro tiempos con cuatro orígenes en internet a la izquierda, el router en el centro con las reglas de input (DNS no desde WAN, accept established y related, "
         "drop invalid, accept ICMP, drop all not coming from LAN) y las de forward (fasttrack, accept established y related, drop invalid, drop all from WAN not DSTNATed), y a la "
         "derecha una PC (192.168.88.20) y un NVR publicado (192.168.88.50:8000). 1: vuelve la respuesta de una descarga de la PC; es established, la toma la primera regla de forward y llega a la PC. "
         "2: un bot prueba el DNS del router y lo corta la regla DNS no desde WAN; otro prueba SSH y lo corta drop all not coming from LAN; ninguno recibe respuesta. "
         "3: una conexión nueva desde la WAN hacia 192.168.88.20 sin port forwarding la corta drop all from WAN not DSTNATed. "
         "4: el celular del dueño entra a la IP pública por el 8000; como tiene dst-nat, el drop de forward no le aplica y llega al NVR.",
         [10, 40, 46, 64, 92])
