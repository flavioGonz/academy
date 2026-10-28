#!/usr/bin/env python3
"""Lección 8 (Túnel de gestión) · Resumen: desde afuera solo entra el túnel; WinBox llega por adentro. El escáner no ve nada."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · TÚNEL DE GESTIÓN · EN LA RED", "De afuera, solo el túnel; WinBox, por adentro",
             ["Un escáner prueba WinBox en la WAN: ninguna regla lo acepta. Drop.",
              "Le manda basura al UDP 13231: pasa el firewall, pero WireGuard no contesta.",
              "La notebook del técnico, con su clave, hace el handshake: el router contesta.",
              "Dentro del túnel, WinBox a 10.10.10.1 entra por wg-gestion."], still=3)

XN, XR, XS = 170, 600, 1030
head(a, XN, 176, "Notebook del técnico", "4G · peer notebook-lucia", w=280)
head(a, XR, 176, "Router del cliente", "WAN 203.0.113.10", w=280, kind="router")
dev(a, XS - 122, 176, 244, 70, "Escáner", "en internet", kind="bad", tsize=17, ssize=14)
for x in (XN, XR, XS):
    lifeline(a, x, 246, 420)

# reglas
RUL = [("accept", "protocol=udp dst-port=13231", "wireguard", a.OK, a.OKBG),
       ("accept", "in-interface=wg-gestion tcp 8291", "winbox por tunel", a.OK, a.OKBG),
       ("drop", "defconf: drop all not coming from LAN", "", a.BAD, a.BADBG)]
a.add(a.text(48, 452, "/ip/firewall/filter · chain=input", 14, a.GREY, a.MONO))
ry = []
for i, (act, m, c_, col, bg) in enumerate(RUL):
    y = 464 + i * 44
    ry.append(y)
    a.add(a.box(48, y, 1104, 38, a.WHITE, a.LINE, rx=10))
    a.add(a.pill(60, y + 6, act, col, bg, 13, 26))
    a.add(a.text(150, y + 25, m, 15, a.INK, a.MONO, 600))
    if c_:
        a.add(a.text(1136, y + 25, f'comment="{c_}"', 14, a.GREY, a.MONO, 400, "end"))
def rr(i, t0, t1, c, still=0):
    en(a, ring(a, 45, ry[i] - 3, 1110, 44, c, rx=12, sw=3), t0, t1, still)

# 1. escáner a 8291
msg(a, XS, XR, 290, "TCP 8291", 3, 25, a.BAD)
rr(2, 7, 25, a.BAD)
en(a, a.text(XR + 160, 330, "sin respuesta", 15, a.BAD, a.SANS, 600, "middle"), 8, 25)
# 2. basura al 13231
msg(a, XS, XR, 290, "UDP 13231 · sin clave válida", 28, 50, a.BAD)
rr(0, 32, 50, a.AMB)
en(a, a.text(XR + 160, 330, "WireGuard descarta en silencio", 15, a.AMB, a.SANS, 600, "middle"), 33, 50)
# 3. handshake
msg(a, XN, XR, 290, "handshake · UDP 13231", 53, 100, a.OK, still=1)
rr(0, 56, 75, a.OK)
msg(a, XR, XN, 330, "respuesta del handshake", 60, 100, a.OK, still=1)
en(a, a.text(XN - 10, 362, "last-handshake: recién", 14, a.OK, a.MONO, 600, "middle"), 64, 100, still=1)
# 4. winbox por dentro
en(a, f'<rect x="{XN}" y="389" width="{XR - XN}" height="14" rx="7" fill="{a.OK}" opacity=".14"/>', 76, 100, still=1)
msg(a, XN, XR, 396, "WinBox → 10.10.10.1", 78, 100, a.INK, still=1, lsize=14)
rr(1, 82, 100, a.OK, still=1)
en(a, a.text(XR + 20, 402, "entra por wg-gestion", 15, a.OK, a.MONO, 600), 82, 100, still=1)

narr(a, [
    (0, 25, "WinBox, SSH y API nunca hacia internet: el drop del final los cubre.", a.BAD),
    (25, 50, "Sin una clave conocida, WireGuard no responde: el puerto parece cerrado.", a.AMB),
    (50, 75, "El puerto del túnel se acepta arriba del drop; lo demás no cambia.", a.OK),
    (75, 100, "WinBox se permite solo por la interfaz del túnel, no por la WAN.", a.OK),
], y=642, still_idx=3)

escribir(a, "8-r1.svg", "El túnel como única puerta",
         "Animación en cuatro tiempos con la notebook del técnico en 4G, el router del cliente con WAN 203.0.113.10 y un escáner en internet. Abajo, tres reglas de input: accept UDP 13231 "
         "(wireguard), accept TCP 8291 con in-interface=wg-gestion (winbox por tunel) y defconf: drop all not coming from LAN. "
         "1: el escáner prueba WinBox al 8291 en la WAN; ninguna regla lo acepta y lo descarta el drop final, sin respuesta. "
         "2: el escáner manda basura al UDP 13231; la regla wireguard lo deja pasar, pero WireGuard no reconoce ninguna clave y lo descarta en silencio. "
         "3: la notebook del técnico, que es un peer con su clave, hace el handshake por UDP 13231 y el router contesta. "
         "4: dentro del túnel, WinBox a 10.10.10.1 entra por la interfaz wg-gestion y lo acepta la regla winbox por tunel.",
         [12, 40, 66, 72, 94])
