#!/usr/bin/env python3
"""Lección 8 (Túnel de gestión) · Laboratorio paso 4: AllowedIPs en la notebook decide qué va por el túnel; con 0.0.0.0/0 iría todo."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · TÚNEL DE GESTIÓN · PASO 4", "AllowedIPs: qué va por el túnel y qué no",
             ["Un paquete a 10.10.10.1 está dentro de AllowedIPs = 10.10.10.0/24.",
              "WireGuard lo cifra y lo manda en UDP al Endpoint 203.0.113.10:13231.",
              "Un paquete a una web no está en AllowedIPs: sale directo por el 4G.",
              "Con AllowedIPs = 0.0.0.0/0, la web también iría por el túnel."], still=2)

# notebook por dentro
a.add(a.box(48, 182, 520, 400, a.WHITE, a.LINE, rx=18))
a.add(a.text(70, 214, "Notebook", 19, a.INK, a.HEAD, 600))
a.add(a.text(180, 214, "app WireGuard · 10.10.10.2/32", 14, a.GREY, a.MONO))
dev(a, 70, 236, 170, 70, "WinBox", "a 10.10.10.1", tsize=16, ssize=14)
dev(a, 70, 350, 170, 70, "Navegador", "a una web", tsize=16, ssize=14)
a.add(a.box(290, 236, 254, 184, a.SLATE, a.LINE, rx=14))
a.add(a.text(306, 264, "¿destino en AllowedIPs?", 15, a.INK, a.SANS, 600))
flip(a, 306, 296, [(0, 76, "10.10.10.0/24", a.BLUE), (76, 100, "0.0.0.0/0", a.BAD)], size=20, still_idx=0)
a.add(a.text(306, 330, "sí → por el túnel", 15, a.OK, a.MONO, 600))
a.add(a.text(306, 356, "no → ruta de siempre", 15, a.TXT, a.MONO, 600))
dev(a, 70, 470, 200, 84, "wg (túnel)", "cifra y encapsula", kind="router", tsize=16, ssize=14)
dev(a, 310, 470, 234, 84, "4G", "salida normal", kind="isp", tsize=16, ssize=14)

dev(a, 900, 196, 252, 96, "Router del cliente", "203.0.113.10:13231", "red 10.10.10.0/24", kind="router", ssize=14)
dev(a, 900, 470, 252, 84, "Sitio web", "198.51.100.200", kind="isp", ssize=14)
a.add(poly([(270, 512), (720, 512), (720, 244), (900, 244)], a.LINE, 3, "6 6"))
a.add(wire(544, 528, 900, 528, a.LINE, 3, "6 6"))

def p(label, c):
    return pillc(a, label, bg=c, size=13, h=28)

# 1. WinBox a 10.10.10.1
go(a, "", [(240, 271), (290, 271)], 2, 5, hold=4, inner=p("a 10.10.10.1", a.BLUE))
en(a, ring(a, 286, 232, 262, 192, a.OK, rx=16), 9, 25)
go(a, "", [(300, 300), (300, 460), (170, 460)], 13, 20, hold=4, inner=p("a 10.10.10.1", a.BLUE))
# 2. encapsula y sale
go(a, "", [(270, 512), (720, 512), (720, 244), (800, 244)], 28, 40, hold=10,
   inner=p("UDP :13231 · cifrado", a.INK))
en(a, a.text(910, 330, "por fuera, solo se ve", 14, a.GREY, a.SANS, 600) + a.text(910, 350, "un UDP al router", 14, a.GREY, a.SANS, 600), 32, 50)
# 3. navegador
go(a, "", [(240, 385), (290, 385)], 52, 55, hold=3, inner=p("a 198.51.100.200", a.GREY))
en(a, ring(a, 286, 232, 262, 192, a.GREY, rx=16), 57, 66)
go(a, "", [(420, 430), (420, 470)], 59, 62, hold=0, inner=p("a 198.51.100.200", a.GREY))
go(a, "", [(544, 528), (800, 528)], 63, 69, hold=7, inner=p("a 198.51.100.200", a.GREY))
fijo(a, at(p("a 198.51.100.200", a.GREY), 720, 528))
# 4. 0.0.0.0/0
en(a, ring(a, 286, 232, 262, 192, a.BAD, rx=16), 77, 100)
go(a, "", [(270, 512), (720, 512), (720, 244), (800, 244)], 82, 92, hold=6, inner=p("la web, por el túnel", a.BAD))
en(a, mark(a, 722, 528, ok=False), 80, 100)

narr(a, [
    (0, 25, "En la notebook, AllowedIPs funciona como una tabla de rutas del túnel.", a.TXT),
    (25, 50, "Adentro va el paquete original; afuera, un UDP al puerto del túnel.", a.TXT),
    (50, 75, "Para gestión alcanza con la red del túnel: el resto sigue por tu conexión.", a.OK),
    (75, 100, "Todo tu tráfico saldría por el cliente: no lo pongas si solo querés gestión.", a.BAD),
], still_idx=2)

escribir(a, "8-l2.svg", "AllowedIPs en la notebook",
         "Animación en cuatro tiempos con la notebook por dentro (WinBox, el navegador, la decisión de AllowedIPs, la interfaz del túnel y la salida 4G) y, afuera, el router del cliente "
         "en 203.0.113.10:13231 y un sitio web en 198.51.100.200. 1: un paquete de WinBox a 10.10.10.1 está dentro de AllowedIPs = 10.10.10.0/24 y va a la interfaz del túnel. "
         "2: WireGuard lo cifra y lo manda dentro de un UDP al Endpoint 203.0.113.10:13231; por fuera solo se ve ese UDP. "
         "3: un paquete del navegador a 198.51.100.200 no está en AllowedIPs y sale directo por el 4G. "
         "4: con AllowedIPs = 0.0.0.0/0, la web también iría por el túnel y saldría a internet por el cliente.",
         [12, 36, 66, 72, 90])
