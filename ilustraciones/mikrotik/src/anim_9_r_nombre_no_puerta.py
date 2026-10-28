#!/usr/bin/env python3
"""Lección 9 (Nombre, no puerta) · Resumen: el nombre DDNS resuelve a la IP pública, pero el paquete se encuentra con el firewall de siempre."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · NOMBRE, NO PUERTA · EN LA RED", "El nombre te da una IP, no una puerta",
             ["El celular pregunta por el nombre: la nube contesta la IP pública, TTL 60 s.",
              "Con esa IP prueba WinBox al 8291: el paquete llega al router.",
              "El firewall de fábrica lo descarta: el nombre no abrió nada.",
              "Lo que sí entra es lo que tiene su regla, como el túnel UDP 13231."], still=2)

XC, XN, XR = 170, 540, 960
head(a, XC, 178, "Celular del técnico", "datos móviles", w=260)
head(a, XN, 178, "DNS de IP Cloud", "sn.mynetname.net", w=260, kind="cloud")
head(a, XR, 178, "Router del cliente", "WAN 203.0.113.10", w=300, kind="router")
for x in (XC, XN, XR):
    lifeline(a, x, 248, 450)

NAME = "<serie>.sn.mynetname.net"
# 1. resolver
msg(a, XC, XN, 290, f"A? {NAME}", 2, 25, lsize=14)
msg(a, XN, XC, 340, "203.0.113.10 · TTL 60", 9, 25, a.OK)
# 2 y 3. WinBox
msg(a, XC, XR, 300, "TCP 8291 → 203.0.113.10", 27, 75, still=1)
en(a, a.box(XR - 150, 320, 300, 76, a.BADBG, a.BAD, rx=12, sw=2) + a.text(XR, 350, "input · drop all not", 15, a.BAD, a.MONO, 600, "middle")
   + a.text(XR, 374, "coming from LAN", 15, a.BAD, a.MONO, 600, "middle"), 52, 75, still=1)
en(a, mark(a, XR - 166, 300, ok=False, r=14), 52, 75, still=1)
en(a, a.text(XC + 14, 350, "WinBox: sin respuesta", 15, a.BAD, a.SANS, 600), 56, 75, still=1)
# 4. túnel
msg(a, XC, XR, 300, "UDP 13231 · WireGuard", 77, 100, a.OK)
en(a, a.box(XR - 150, 320, 300, 76, a.OKBG, a.OK, rx=12, sw=2) + a.text(XR, 350, "input · accept", 15, a.OK, a.MONO, 600, "middle")
   + a.text(XR, 374, "dst-port=13231", 15, a.OK, a.MONO, 600, "middle"), 82, 100)
en(a, a.text(XC + 14, 350, "túnel arriba: WinBox por adentro", 15, a.OK, a.SANS, 600), 86, 100)

# panel
a.add(a.box(48, 474, 1104, 116, a.INK, rx=12))
a.add(a.text(66, 504, "/ip/cloud/print", 14, SKY, a.MONO))
a.add(a.text(66, 534, "dns-name:", 15, SKY, a.MONO))
a.add(a.text(220, 534, NAME, 15, a.WHITE, a.MONO, 600))
a.add(a.text(66, 562, "public-address:", 15, SKY, a.MONO))
a.add(a.text(220, 562, "203.0.113.10", 15, a.WHITE, a.MONO, 600))
a.add(a.text(640, 534, "el nombre sigue a la IP pública;", 15, SKY, a.SANS, 600))
a.add(a.text(640, 562, "quién entra lo decide el firewall", 15, GOLD, a.SANS, 600))

narr(a, [
    (0, 25, "IP Cloud solo publica un nombre que apunta a la IP desde la que el router llega a la nube.", a.TXT),
    (25, 50, "El nombre llevó el paquete hasta la puerta correcta.", a.TXT),
    (50, 75, "La configuración por defecto descarta lo que llega de internet, y está bien.", a.BAD),
    (75, 100, "Para entrar de afuera, un túnel con su regla, no un puerto de gestión abierto.", a.OK),
], still_idx=2)

escribir(a, "9-r1.svg", "El nombre DDNS no abre nada",
         "Animación en cuatro tiempos con el celular del técnico, el DNS de IP Cloud (sn.mynetname.net) y el router del cliente con WAN 203.0.113.10. Abajo, el /ip/cloud/print con dns-name y public-address. "
         "1: el celular pregunta por <serie>.sn.mynetname.net y la nube contesta 203.0.113.10 con TTL de 60 segundos. "
         "2: con esa IP, el celular prueba WinBox al puerto 8291 y el paquete llega al router. "
         "3: la regla de input drop all not coming from LAN lo descarta y WinBox no recibe respuesta: el nombre no abrió nada. "
         "4: lo que sí entra es lo que tiene su regla, como el túnel WireGuard por UDP 13231, aceptado en input; con el túnel arriba, WinBox va por adentro.",
         [12, 40, 62, 70, 92])
