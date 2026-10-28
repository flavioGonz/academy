#!/usr/bin/env python3
"""Lección 19 (Back To Home) · Laboratorio paso 4: un usuario con LAN y otro de solo internet, y por qué importa la lista LAN."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · BACK TO HOME · PASO 4", "Con LAN y sin LAN: la regla dinámica decide",
             ["tecnico-lucia (allow-lan=yes) pide el NVR: llega.",
              "invitado (allow-lan=no) pide el NVR: la regla dinámica lo corta hacia la lista LAN.",
              "invitado pide una web: sale a internet a través del router, con masquerade.",
              "Una red local que no está en la lista LAN no queda protegida."], still=1)

dev(a, 48, 210, 236, 96, "tecnico-lucia", "allow-lan=yes", "192.168.216.2", ssize=14, tsize=17)
dev(a, 48, 420, 236, 96, "invitado", "allow-lan=no", "192.168.216.3", ssize=14, tsize=17)

RX, RW = 360, 440
a.add(a.box(RX, 186, RW, 360, a.INK, rx=18))
a.add(a.text(RX + 20, 216, "Router · back-to-home-vpn", 17, a.WHITE, a.HEAD, 600))
a.add(a.text(RX + 20, 248, "reglas dinámicas que crea Back To Home", 13, SKY, a.MONO))
a.add(a.box(RX + 16, 262, RW - 32, 86, a.NAVY2, rx=10))
a.add(a.text(RX + 30, 288, "forward · drop", 14, ROSE, a.MONO, 600))
a.add(a.text(RX + 30, 310, "de back-to-home-lan-restricted-peers", 13, a.WHITE, a.MONO))
a.add(a.text(RX + 30, 332, "hacia la lista LAN", 13, a.WHITE, a.MONO))
a.add(a.box(RX + 16, 360, RW - 32, 52, a.NAVY2, rx=10))
a.add(a.text(RX + 30, 384, "srcnat · masquerade", 14, MINT, a.MONO, 600))
a.add(a.text(RX + 30, 402, "lo que sale del túnel", 13, a.WHITE, a.MONO))
a.add(a.text(RX + 20, 446, "lista LAN:", 14, SKY, a.MONO))
a.add(a.text(RX + 120, 446, "bridge (192.168.88.0/24)", 14, a.WHITE, a.MONO, 600))
a.add(a.text(RX + 20, 470, "fuera de LAN:", 14, SKY, a.MONO))
a.add(a.text(RX + 136, 470, "ether5 (10.10.50.0/24)", 14, GOLD, a.MONO, 600))
a.add(a.text(RX + 20, 504, "restringidos:", 14, SKY, a.MONO))
a.add(a.text(RX + 136, 504, "invitado", 14, ROSE, a.MONO, 600))

dev(a, 900, 196, 252, 84, "NVR", "192.168.88.50 · bridge", ssize=14, tsize=17)
dev(a, 900, 318, 252, 84, "Equipo en ether5", "10.10.50.20 · fuera de LAN", ssize=13, tsize=17)
dev(a, 900, 446, 252, 84, "Internet", "ve la IP del cliente", kind="isp", ssize=14, tsize=17)

def p(label, c):
    return pillc(a, label, bg=c, size=13, h=26)
def ok_at(x, y, t0, t1, ok=True, still=0):
    en(a, mark(a, x, y, ok=ok), t0, t1, still)

# 1. lucia al NVR
go(a, "", [(284, 238), (850, 238)], 2, 10, hold=12, inner=p("NVR", a.BLUE))
ok_at(850, 204, 10, 25)
# 2. invitado al NVR
go(a, "", [(284, 448), (322, 448), (322, 305)], 27, 33, hold=15, inner=p("NVR", a.GREY))
en(a, ring(a, RX + 13, 259, RW - 26, 92, ROSE, rx=12, sw=3), 33, 50, still=1)
ok_at(RX + RW - 30, 280, 34, 50, ok=False, still=1)
fijo(a, at(p("NVR", a.GREY), 322, 305))
# 3. invitado a una web
go(a, "", [(284, 488), (850, 488)], 53, 61, hold=12, inner=p("web", a.GREY))
en(a, ring(a, RX + 13, 357, RW - 26, 58, MINT, rx=12, sw=3), 56, 75)
ok_at(850, 454, 61, 75)
# 4. ether5 fuera de LAN
go(a, "", [(284, 470), (850, 470), (850, 360)], 78, 87, hold=10, inner=p("ether5", a.BAD))
en(a, ring(a, 897, 315, 258, 90, a.AMB, rx=18), 86, 100)
en(a, ring(a, RX + 10, 452, RW - 20, 28, GOLD, rx=8, sw=2), 80, 100)

narr(a, [
    (0, 25, "allow-lan=yes con client-allowed-address acota a qué redes llega.", a.OK),
    (25, 50, "Los de solo internet van a una lista dinámica, y la regla los frena hacia LAN.", a.BAD),
    (50, 75, "El sitio web ve la IP del cliente: el tráfico sale por su conexión.", a.TXT),
    (75, 100, "Por eso el paso 5: revisá que todas tus redes locales estén en la lista LAN.", a.AMB),
], still_idx=1)

escribir(a, "19-l1.svg", "Usuarios de Back To Home con y sin LAN",
         "Animación en cuatro tiempos con dos usuarios de Back To Home, tecnico-lucia (allow-lan=yes, 192.168.216.2) e invitado (allow-lan=no, 192.168.216.3); el router con las reglas dinámicas "
         "(drop en forward de la lista back-to-home-lan-restricted-peers hacia la lista LAN, y masquerade de lo que sale del túnel); y a la derecha el NVR en el bridge (192.168.88.50), "
         "un equipo en ether5 (10.10.50.20) que no está en la lista LAN, e internet. 1: tecnico-lucia pide el NVR y llega. "
         "2: invitado pide el NVR; está en la lista de restringidos y la regla dinámica lo corta hacia la lista LAN. 3: invitado pide una web y sale a internet a través del router con masquerade. "
         "4: invitado llega al equipo de ether5 porque esa red no está en la lista LAN: la restricción depende de esa lista.",
         [12, 40, 64, 70, 94])
