#!/usr/bin/env python3
"""Lección 31 (DNS transparente) · Resumen: la tele con el DNS clavado, antes y después del redirect; la excepción dns-libre y el DoH que pasa igual."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · DNS TRANSPARENTE · EN LA RED", "La tele pregunta a 8.8.8.8 y contesta el router",
             ["Sin reglas: la tele le pregunta a 8.8.8.8 y el bloqueo del router no la alcanza.",
              "Con el redirect, la misma consulta la contesta el router: 0.0.0.0.",
              "El servidor en dns-libre sale directo a su DNS: es la excepción.",
              "Un celular con DoH va cifrado por el 443: la regla del 53 no lo ve."], still=1)

dev(a, 48, 200, 220, 96, "Tele", "192.168.88.40", "DNS fijo 8.8.8.8", ssize=14)
dev(a, 48, 344, 220, 96, "Servidor", "192.168.88.10", "en dns-libre", ssize=14)
dev(a, 48, 476, 220, 96, "Celular", "192.168.88.254", "DoH activado", ssize=14)
dev(a, 920, 200, 232, 96, "8.8.8.8", "DNS de Google", "puerto 53", kind="isp", ssize=14)
dev(a, 920, 476, 232, 96, "Servidor DoH", "HTTPS · 443", kind="isp", ssize=14)

# router
RX, RW = 340, 520
a.add(a.box(RX, 186, RW, 392, a.INK, rx=18))
a.add(a.text(RX + 20, 214, "Router", 18, a.WHITE, a.HEAD, 600))
en(a, a.text(RX + 110, 214, "sin reglas de NAT para el 53", 14, SKY, a.MONO), 0, 25)
en(a, a.text(RX + 110, 214, "dstnat · redirect udp y tcp 53", 14, MINT, a.MONO, 600), 25, 100, still=1)
en(a, a.text(RX + 110, 234, "src-address-list=!dns-libre", 14, MINT, a.MONO), 25, 100, still=1)
a.add(a.box(RX + 150, 300, 220, 64, a.NAVY2, rx=12))
a.add(a.text(RX + 260, 328, "resolver del router", 15, a.WHITE, a.SANS, 600, "middle"))
a.add(a.text(RX + 260, 350, "adlist: ads.example.net", 13, SKY, a.MONO, 400, "middle"))

def dot(c):
    return f'<circle cx="0" cy="0" r="10" fill="{c}" stroke="#FFFFFF" stroke-width="2.5"/>'

# 1. sin reglas
go(a, "", [(268, 250), (920, 250)], 2, 9, hold=0, inner=dot(a.BLUE))
go(a, "", [(920, 266), (268, 266)], 11, 18, hold=6, inner=dot(a.AMB))
en(a, a.text(600, 290, "A? ads.example.net → 8.8.8.8", 14, a.WHITE, a.MONO, 600, "middle"), 2, 25)
en(a, a.pill(158, 166 + 136, "la publicidad carga", a.AMB, a.AMBBG, 13, 26, anchor="middle"), 18, 25)

# 2. con redirect
go(a, "", [(268, 250), (RX + 260, 250), (RX + 260, 300)], 27, 33, hold=0, inner=dot(a.BLUE))
go(a, "", [(RX + 200, 300), (RX + 200, 266), (268, 266)], 36, 42, hold=8, inner=dot(a.OK))
en(a, ring(a, RX + 147, 297, 226, 70, MINT, rx=14, sw=3), 32, 50, still=1)
en(a, a.text(600, 290, "A? ads.example.net → 8.8.8.8", 14, a.WHITE, a.MONO, 600, "middle"), 27, 50, still=1)
en(a, a.text(RX + 120, 396, "vuelve 0.0.0.0 con origen 8.8.8.8:", 14, MINT, a.MONO, 600), 38, 50, still=1)
en(a, a.text(RX + 120, 416, "la tele no nota el cambio", 14, MINT, a.MONO, 600), 38, 50, still=1)
en(a, a.pill(158, 302, "bloqueado", a.OK, a.OKBG, 13, 26, anchor="middle"), 42, 50, still=1)

# 3. servidor dns-libre
go(a, "", [(268, 392), (880, 392), (880, 250), (920, 250)], 52, 61, hold=6, inner=dot(a.BLUE))
en(a, a.text(600, 404, "dns-libre: no se redirige", 14, GOLD, a.MONO, 600, "middle"), 54, 75)

# 4. DoH
go(a, "", [(268, 524), (920, 524)], 78, 86, hold=10, inner=dot(a.GREY))
en(a, a.text(1036, 464, "llega por TLS 443", 14, a.GREY, a.MONO, 600, "middle"), 84, 100)
en(a, a.text(600, 504, "cifrado: no es tráfico al 53", 14, GOLD, a.MONO, 600, "middle"), 80, 100)

narr(a, [
    (0, 25, "Estáticas y bloqueos del router valen solo para quien le pregunta al router.", a.TXT),
    (25, 50, "dst-address-type=!local: lo que ya iba al router no se toca.", a.OK),
    (50, 75, "Un DNS propio va en dns-libre antes de crear las reglas.", a.AMB),
    (75, 100, "DoH: hay paliativos, no un candado.", a.TXT),
], still_idx=1)

escribir(a, "31-r1.svg", "DNS transparente en la red",
         "Animación en cuatro tiempos con tres equipos de la LAN (una tele con DNS fijo 8.8.8.8, un servidor en la lista dns-libre y un celular con DoH), el router con su resolver "
         "y una adlist que bloquea ads.example.net, y del lado de internet 8.8.8.8 y un servidor DoH. 1: sin reglas de NAT, la tele le pregunta a 8.8.8.8 por ads.example.net, "
         "Google le contesta y la publicidad carga: el bloqueo del router no la alcanza. 2: con el redirect de udp y tcp 53, la misma consulta la desvía el router a su resolver, "
         "que contesta 0.0.0.0 con origen 8.8.8.8, y la tele no nota el cambio. 3: el servidor está en dns-libre, así que su consulta sale directo a su DNS. "
         "4: el celular con DoH va cifrado por el 443 al servidor DoH; no es tráfico al 53 y la regla no lo ve.",
         [12, 40, 46, 62, 90])
