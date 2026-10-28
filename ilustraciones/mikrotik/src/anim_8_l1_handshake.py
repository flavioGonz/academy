#!/usr/bin/env python3
"""Lección 8 (Túnel de gestión) · Laboratorio paso 5: el handshake de WireGuard al activar el túnel y lo que muestra peers/print."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · TÚNEL DE GESTIÓN · PASO 5", "Activás el túnel: handshake y last-handshake",
             ["La notebook manda Handshake Initiation a 203.0.113.10:13231.",
              "El router conoce esa clave pública: contesta Handshake Response.",
              "Hay sesión: last-handshake vuelve a cero y aparece desde dónde llegó.",
              "WinBox a 10.10.10.1 viaja cifrado; sin tráfico, un keepalive cada 25 s."], still=2)

XN, XR = 170, 640
head(a, XN, 176, "Notebook", "10.10.10.2 · 4G", w=250)
head(a, XR, 176, "Router", "wg-gestion · 10.10.10.1", w=270, kind="router")
for x in (XN, XR):
    lifeline(a, x, 246, 592)

msg(a, XN, XR, 288, "Handshake Initiation", 3, 100, a.BLUE, still=1, sub="UDP a 203.0.113.10:13231", subcolor=a.GREY)
msg(a, XR, XN, 360, "Handshake Response", 28, 100, a.OK, still=1)
en(a, a.text(XR - 14, 400, "clave pública conocida: notebook-lucia", 14, a.OK, a.MONO, 600, "end"), 30, 100, still=1)
msg(a, XN, XR, 450, "datos · WinBox a 10.10.10.1", 78, 100, a.INK)
for k, t in enumerate((86, 93)):
    msg(a, XN, XR, 510 + k * 40, "keepalive", t, 100, a.CYAN, lsize=14)
en(a, a.text(XN + 10, 600, "cada 25 s, si no hay tráfico", 14, a.CYAN, a.SANS, 600), 88, 100)

# peers/print
PX = 800
a.add(a.box(PX, 246, 352, 346, a.INK, rx=14))
a.add(a.text(PX + 18, 276, "/interface/wireguard/peers/print", 13, SKY, a.MONO))
rows = [("name", [(0, 100, "notebook-lucia", a.WHITE)], 0),
        ("allowed-address", [(0, 100, "10.10.10.2/32", a.WHITE)], 0),
        ("current-endpoint-address", [(0, 52, "(vacío)", SKY), (52, 100, "198.51.100.77", MINT)], 1),
        ("current-endpoint-port", [(0, 52, "(vacío)", SKY), (52, 100, "40312", MINT)], 1),
        ("last-handshake", [(0, 52, "(nunca)", SKY), (52, 70, "0s", MINT), (70, 85, "6s", MINT), (85, 100, "13s", MINT)], 1),
        ("rx / tx", [(0, 78, "0 / 0", SKY), (78, 100, "suben", MINT)], 0)]
for i, (k, vals, st) in enumerate(rows):
    y = 312 + i * 44
    a.add(a.text(PX + 18, y, k, 14, SKY, a.MONO))
    flip(a, PX + 18, y + 20, vals, size=15, still_idx=st)
en(a, ring(a, PX + 8, 312 + 2 * 44 - 22, 336, 140, MINT, rx=10, sw=2.5), 52, 75, still=1)
en(a, a.text(PX + 18, 578, "la IP pública del 4G, la que ve el router", 13, GOLD, a.SANS, 600), 52, 100, still=1)

narr(a, [
    (0, 25, "WireGuard no tiene usuario ni clave: el primer mensaje ya va firmado con la clave.", a.TXT),
    (25, 50, "Si la clave no estuviera cargada en el peer, el router no contestaría nada.", a.OK),
    (50, 75, "Si last-handshake dice nunca, revisá claves, Endpoint y la regla del 13231.", a.AMB),
    (75, 100, "El NAT del 4G sigue abierto gracias al keepalive.", a.TXT),
], y=642, still_idx=2)

escribir(a, "8-l1.svg", "Handshake de WireGuard",
         "Animación en cuatro tiempos con dos líneas de vida, la notebook (10.10.10.2, en 4G) y el router (wg-gestion, 10.10.10.1), y a la derecha la salida de /interface/wireguard/peers/print. "
         "1: al activar el túnel, la notebook manda Handshake Initiation por UDP a 203.0.113.10:13231. 2: el router conoce la clave pública del peer notebook-lucia y contesta Handshake Response. "
         "3: hay sesión: last-handshake pasa de nunca a 0s y current-endpoint-address y current-endpoint-port muestran 198.51.100.77 y 40312, la IP pública del 4G desde la que llegó la notebook. "
         "4: WinBox a 10.10.10.1 viaja cifrado como datos, rx y tx suben, y si no hay tráfico la notebook manda un keepalive cada 25 segundos.",
         [10, 40, 62, 82, 96])
