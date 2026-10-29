#!/usr/bin/env python3
"""Lección 8 · Laboratorio, paso 4: qué ve nmap o nc desde otra máquina. open: el SYN llega y el servicio contesta
SYN-ACK. closed: el puerto pasa el firewall pero nada escucha, el kernel responde RST (connection refused).
filtered: un DROP descarta el SYN, no vuelve nada, nmap reintenta y lo marca filtered (en nc, timeout).
Fuentes: teoría y laboratorio de la lección (open, closed, filtered; refused contra timeout), documentación de nmap
(estados de puertos) y RFC 9293 (RST a un puerto sin escucha). Puertos y servicios de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · FIREWALL · LABORATORIO", "open, closed, filtered: lo que vuelve por el cable")
a.steps([
    "22: el SYN pasa la regla y sshd contesta SYN-ACK. open.",
    "Un puerto permitido sin servicio: el kernel contesta RST. closed.",
    "443 sin regla: el DROP no contesta; nmap reintenta y marca filtered.",
    "Se prueba desde otra máquina: en el propio servidor el camino es otro.",
], still=2)

a.add(dev(a, 48, 166, 300, 70, "Otra VM de gestión", "nmap -Pn · nc -zv", "laptop", ssize=14))
a.add(dev(a, 852, 166, 300, 70, "Servidor .88.50", "nftables · policy drop", "server", dark=True, ssize=14))
FWX = 760
a.add(a.box(FWX - 18, 252, 36, 300, a.NAVY2, None, rx=10))
a.add(f'<text x="{FWX}" y="402" font-family="{a.MONO}" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 {FWX} 402)">cadena input</text>')
L = 370
LANES = [(290, "22/tcp", "regla accept · sshd escucha"), (400, "8080/tcp", "accept (ejemplo) · nada escucha"), (510, "443/tcp", "sin regla · cae en policy drop")]
for y, p, d in LANES:
    a.add(camino(f"M{L} {y} H{FWX - 18}", "#C2D4E6", 3) + camino(f"M{FWX + 18} {y} H1000", "#C2D4E6", 3))
    a.add(a.box(1000, y - 26, 152, 52, a.WHITE, a.LINE, rx=10) + mono(a, 1016, y - 3, p, 15, a.INK, 700) + a.text(1016, y + 18, "", 14, a.GREY))
    a.add(a.text(FWX + 30, y - 36, d, 15, a.GREY, a.SANS, 600))

def ida(y, t0, t1, lbl="SYN"):
    viaje(a, lbl, [(L + 30, y), (990, y)], t0, t1, bg=a.BLUE, size=13, hold=0.3)


def vuelta(y, t0, t1, lbl, c):
    viaje(a, lbl, [(990, y), (L + 30, y)], t0, t1, bg=c, size=13, hold=0.3)


def res(y, t0, txt, c, bg, nc, still=0):
    en(a, a.pill(48, y - 15, txt, c, bg, 15, 30) + a.text(48, y + 38, nc, 14, c, a.MONO, 600), t0, 100, still=still)


# 1 open
ida(290, 3, 10)
vuelta(290, 11, 18, "SYN-ACK", a.OK)
en(a, a.text(1076, 310, "sshd", 14, a.OK, a.MONO, 700, "middle"), 9, 100, still=1)
res(290, 18, "open", a.OK, a.OKBG, "nc: succeeded!", still=1)
# 2 closed
ida(400, 28, 35)
vuelta(400, 36, 43, "RST", a.BAD)
en(a, a.text(1076, 420, "nadie", 14, a.BAD, a.MONO, 700, "middle"), 34, 100, still=1)
res(400, 43, "closed", a.BAD, a.BADBG, "nc: Connection refused", still=1)
# 3 filtered
viaje(a, "SYN", [(L + 30, 510), (FWX - 30, 510)], 53, 58, bg=a.BLUE, size=13, hold=0.5)
en(a, marca(a, FWX - 34, 510, False, 13), 58, 100, still=1)
viaje(a, "SYN (otra vez)", [(L + 50, 510), (FWX - 70, 510)], 62, 67, bg=a.BLUE, size=13, hold=0.5)
en(a, a.text(560, 548, "no vuelve nada", 15, a.BAD, a.SANS, 700, "middle"), 59, 100, still=1)
res(510, 69, "filtered", a.AMB, a.AMBBG, "nc: espera hasta el timeout", still=1)
# 4 desde el propio servidor
en(a, nota(a, 852, 566, 300, 60, "En el propio servidor", ["va por lo: iif lo accept"], "amb", 15, 15), 76, 100)
en(a, a.box(40, 268, 300, 300, "none", a.BLUE, rx=14, sw=2.5, extra='stroke-dasharray="7 5"'), 76, 100)

narr(a, [
    (0, 25, "open: algo escucha y el firewall deja pasar desde ese origen.", a.OK),
    (25, 50, "closed: el paquete llegó; el problema es el servicio, no el firewall.", a.BAD),
    (50, 75, "filtered: el paquete se descartó; refused y timeout no son lo mismo.", a.AMB),
    (75, 100, "Lo que importa es lo que ve la red: probá desde la máquina que va a usar el servicio.", None),
], y=640, still_idx=2)

escribir(a, "8-l1", "open, closed, filtered: lo que vuelve por el cable",
         "Animación en cuatro tiempos con otra VM de gestión a la izquierda, que corre nmap -Pn o nc -zv, la cadena input con policy drop en el medio y el servidor 192.168.88.50 a la derecha, con tres puertos de ejemplo. "
         "1: 22/tcp tiene regla accept y sshd escucha: el SYN pasa y vuelve SYN-ACK; nmap dice open y nc succeeded. "
         "2: 8080/tcp está permitido pero nada escucha: el kernel contesta RST; nmap dice closed y nc Connection refused. "
         "3: 443/tcp no tiene regla: el SYN cae en policy drop, no vuelve nada, nmap reintenta y lo marca filtered; nc espera hasta el timeout. "
         "4: se prueba desde otra máquina, porque en el propio servidor el tráfico va por lo, que tiene iif lo accept.",
         [10, 38, 64, 90])
