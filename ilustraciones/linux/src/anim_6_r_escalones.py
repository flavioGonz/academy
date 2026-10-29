#!/usr/bin/env python3
"""Lección 6 (Escalera de red), Resumen: qué viaja por el cable en cada escalón, con todo funcionando.
Gateway: ARP y ping a 192.168.88.1. IP pública: ping a 1.1.1.1 por la ruta default. Nombre: consulta DNS al
nameserver 192.168.88.1 por UDP 53. Puerto: saludo TCP al 80 y respuesta HTTP de curl. Fuentes: teoría y
laboratorio de la lección (escalones, red 192.168.88.0/24, nameservers del netplan), RFC 826 (ARP),
RFC 792 (ICMP echo), RFC 1035 (DNS sobre UDP 53) y RFC 9293 (saludo TCP)."""
from _anims_lnx_rl import *

a = nueva(30, "LINUX · RED · EN LA RED", "Qué viaja por el cable en cada escalón")
a.steps([
    "Gateway: ARP pregunta por 192.168.88.1 y después vuelve el ping.",
    "IP pública: el ping a 1.1.1.1 sale por la ruta default, vía el router.",
    "Nombre: consulta DNS al 192.168.88.1 por UDP 53; vuelve la IP.",
    "Puerto: SYN al 80, SYN-ACK, y curl recibe las cabeceras HTTP.",
], still=3)

a.add(dev(a, 48, 196, 250, 96, "Servidor", "ens18 · .88.50/24", "server", dark=True, sub2="default via .88.1"))
a.add(dev(a, 430, 196, 230, 96, "Router", "192.168.88.1", "shield", sub2="gateway y DNS"))
a.add(dev(a, 880, 176, 272, 78, "1.1.1.1", "IP pública", "globe"))
a.add(dev(a, 880, 300, 272, 78, "deb.debian.org", "servidor web", "globe"))
a.add(camino("M298 244 H430", "#C2D4E6", 4))
a.add(camino("M660 230 C 760 230, 780 215, 880 215", "#C2D4E6", 4))
a.add(camino("M660 262 C 760 262, 780 339, 880 339", "#C2D4E6", 4))
a.add(a.text(364, 226, "LAN", 14, a.GREY, a.MONO, 600, "middle") + a.text(770, 196, "internet", 14, a.GREY, a.MONO, 600, "middle"))

P1 = [(310, 244), (418, 244)]
P1b = list(reversed(P1))
PI = [(310, 244), (418, 244), (680, 230), (780, 222), (868, 215)]
PD = [(310, 244), (418, 244), (680, 262), (780, 300), (868, 339)]


def ida(lbl, pts, t0, t1, c=a.BLUE, size=13):
    viaje(a, lbl, pts, t0, t1, bg=c, size=size, hold=0.3)


def vuelta(lbl, pts, t0, t1, c=a.OK, size=13):
    viaje(a, lbl, list(reversed(pts)), t0, t1, bg=c, size=size, hold=0.3)


# 1 gateway
ida("ARP", P1, 2, 7, a.AMB)
vuelta("ARP", P1, 8, 13, a.AMB)
ida("echo", P1, 15, 19)
vuelta("echo", P1, 20, 24)
# 2 IP pública
ida("echo", PI, 27, 37)
vuelta("echo", PI, 38, 48)
# 3 DNS
ida("DNS", P1, 52, 58, a.CYAN)
en(a, a.text(545, 316, "consulta afuera", 15, a.GREY, a.SANS, 600, "middle") + a.text(545, 338, "y responde", 15, a.GREY, a.SANS, 600, "middle"), 58, 66)
vuelta("DNS", P1, 66, 73, a.CYAN)
# 4 puerto
ida("SYN", PD, 77, 83)
vuelta("SYN-ACK", PD, 83.5, 89.5)
vuelta("HTTP", PD, 91, 97.5)
fijo(a, place(pill_c(a, "HTTP", "#FFFFFF", a.OK, 13), 790, 305))
# qué viaja ahora
DET = [(1, 14, "ARP request por broadcast: ¿quién tiene 192.168.88.1? El router responde con su MAC.", a.AMB, 0),
       (14, 25, "ICMP echo request al gateway, y vuelve el echo reply.", a.BLUE, 0),
       (26, 50, "ICMP echo a 1.1.1.1: sale por default via 192.168.88.1 y vuelve por el mismo camino.", a.BLUE, 0),
       (51, 75, "DNS por UDP 53 al 192.168.88.1: debian.org A?  →  A 198.51.100.20 (IP de ejemplo).", a.CYAN, 0),
       (76, 100, "TCP al 80 de deb.debian.org: SYN, SYN-ACK, y curl recibe las cabeceras HTTP.", a.OK, 1)]
a.add(a.text(48, 334, "en el cable ahora", 14, a.GREY, a.MONO, 600))
for t0, t1, txt, c, st in DET:
    en(a, a.text(48, 362, txt, 15, c, a.SANS, 700), t0, t1, still=st)

# escalera de estado
LY = 410
RUNG = [("1 interfaz", "ip -br addr · ip route", 0), ("2 gateway", "ping -c3 192.168.88.1", 24), ("3 IP pública", "ping -c3 1.1.1.1", 48),
        ("4 nombre", "dig debian.org +short", 73), ("5 puerto", "curl -sI deb.debian.org", 97)]
for i, (t, c, tk) in enumerate(RUNG):
    x = 48 + i * 222
    a.add(a.box(x, LY, 214, 92, a.WHITE, a.LINE, rx=12) + a.text(x + 16, LY + 30, t, 16, a.INK, a.HEAD, 600) + mono(a, x + 12, LY + 56, c, 14, a.BLUE, 600))
    if tk == 0:
        a.add(marca(a, x + 190, LY + 24, True, 12) + a.text(x + 16, LY + 80, "IP y ruta: ya estaban", 14, a.OK, a.SANS, 600))
    else:
        en(a, a.box(x, LY, 214, 92, "none", a.OK, rx=12, sw=3) + marca(a, x + 190, LY + 24, True, 12), tk, 100, still=1 if tk < 90 else 0)
fijo(a, a.box(48 + 4 * 222, LY, 214, 92, "none", a.OK, rx=12, sw=3) + marca(a, 48 + 4 * 222 + 190, LY + 24, True, 12))
cur = [(0, 25, 1), (25, 50, 2), (50, 75, 3), (75, 100, 4)]
for t0, t1, i in cur:
    en(a, a.box(48 + i * 222 - 5, LY - 5, 224, 102, "none", a.BLUE, rx=15, sw=2.5, extra='stroke-dasharray="7 5"'), t0, t1, still=1 if i == 4 else 0)

# qué prueba cada escalón
narr(a, [
    (0, 25, "Sin la MAC del gateway no sale nada: ARP va primero, y lo deja en ip neigh.", None),
    (25, 50, "Llegar a una IP pública prueba ruta y salida, sin depender del DNS.", a.OK),
    (50, 75, "El nombre se resuelve con el nameserver configurado; dig muestra la respuesta.", a.OK),
    (75, 100, "El servicio contesta en su puerto: la escalera llegó arriba sin fallas.", a.OK),
], y=560, still_idx=3)
a.add(a.text(48, 600, "Si un escalón falla, los de arriba no se prueban: ahí está el problema.", 16, a.GREY, a.SANS, 500))
a.add(a.text(48, 626, "Direcciones de ejemplo; la IP que devuelve el DNS es ilustrativa.", 15, a.GREY, a.SANS, 500))

escribir(a, "6-r1", "Qué viaja por el cable en cada escalón",
         "Animación en cuatro tiempos con el servidor (ens18, 192.168.88.50/24, default via 192.168.88.1), el router 192.168.88.1, que es gateway y DNS, y en internet 1.1.1.1 y deb.debian.org. Abajo, los cinco escalones; el de la interfaz ya está en verde. "
         "1: gateway: una pregunta ARP por 192.168.88.1 y su respuesta con la MAC, y después el echo request y el echo reply del ping. "
         "2: IP pública: el ping a 1.1.1.1 sale por la ruta default, pasa por el router y vuelve. "
         "3: nombre: una consulta DNS por el registro A de debian.org al 192.168.88.1 por UDP 53; el router consulta afuera y responde con una IP de ejemplo. "
         "4: puerto: SYN al 80 de deb.debian.org, SYN-ACK de vuelta y las cabeceras HTTP que recibe curl. Cada escalón se pone en verde cuando termina.",
         [10, 22, 40, 62, 86, 99])
