#!/usr/bin/env python3
"""Lección 19 (Back To Home) · Resumen: el celular del técnico entra al NVR, directo o por relay según vpn-relay-ipv4-status."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · BACK TO HOME · EN LA RED", "Del celular al NVR: directo o por relay",
             ["Con IP pública, el nombre vpn.mynetname.net apunta al router: reachable directly.",
              "El túnel WireGuard va directo; el celular usa una IP de 192.168.216.0/24.",
              "Detrás de CGNAT: reachable via relay. El nombre apunta al relay, que no lee nada.",
              "Con allow-lan=yes y 192.168.88.0/24 permitido, el celular llega al NVR."], still=3)

dev(a, 48, 340, 210, 100, "Celular", "datos móviles", "192.168.216.2", ssize=14)
dev(a, 760, 330, 230, 120, "Router", "back-to-home-vpn", "192.168.216.1/24", sub3="LAN 192.168.88.1", kind="router", ssize=14)
dev(a, 1020, 340, 132, 100, "NVR", "192.168.88.50", ssize=13, tsize=17)
dev(a, 420, 492, 250, 90, "Relay de MikroTik", "pasa paquetes cifrados", "sin poder leerlos", kind="cloud", ssize=13)

# /ip/cloud/print
a.add(a.box(300, 186, 690, 104, a.INK, rx=14))
a.add(a.text(318, 214, "/ip/cloud/print", 14, SKY, a.MONO))
a.add(a.text(318, 244, "vpn-relay-ipv4-status:", 15, SKY, a.MONO))
a.add(a.text(318, 272, "vpn-dns-name resuelve a:", 15, SKY, a.MONO))
flip(a, 560, 244, [(0, 50, "reachable directly", MINT), (50, 100, "reachable via relay", GOLD)], size=15, still_idx=1)
flip(a, 560, 272, [(0, 50, "la IP pública del router", MINT), (50, 100, "el relay que usa el router", GOLD)], size=15, still_idx=1)

# carriles
DIR = [(258, 380), (760, 380)]
REL = [(258, 410), (330, 410), (330, 537), (420, 537)]
REL2 = [(670, 537), (712, 537), (712, 410), (760, 410)]
en(a, poly(DIR, a.OK, 4, "10 6"), 27, 50)
en(a, a.text(510, 368, "túnel directo · UDP", 14, a.OK, a.MONO, 600, "middle"), 27, 50)
en(a, poly(REL, a.AMB, 4, "10 6") + poly(REL2, a.AMB, 4, "10 6"), 52, 100, still=1)
en(a, a.text(510, 470, "el router mantiene abierta la conexión al relay", 14, a.AMB, a.SANS, 600, "middle"), 54, 75, still=1)
en(a, a.box(304, 366, 412, 34, a.BADBG, rx=10) + a.text(510, 389, "CGNAT: de afuera no se entra al router", 14, a.BAD, a.SANS, 600, "middle"), 52, 100, still=1)

def p(label, c):
    return pillc(a, label, bg=c, size=13, h=26)

# 1. DNS
go(a, "", [(153, 326), (153, 318)], 3, 5, hold=18, inner=p("A? <serie>.vpn.mynetname.net", a.BLUE))
# 2. túnel directo
go(a, "", DIR, 30, 38, hold=8, inner=p("WireGuard", a.OK))
# 3. por relay
go(a, "", REL + [(545, 537)], 56, 63, hold=0, inner=p("cifrado", a.INK))
go(a, "", [(545, 537)] + [(670, 537)] + REL2, 63, 70, hold=4, inner=p("cifrado", a.INK))
# 4. al NVR
go(a, "", REL + [(545, 537)], 77, 82, hold=0, inner=p("a 192.168.88.50", a.INK))
go(a, "", [(545, 537), (670, 537)] + REL2, 82, 87, hold=0, inner=p("a 192.168.88.50", a.INK))
go(a, "", [(990, 390), (1020, 390)], 87.5, 89, hold=8, inner=f'<circle r="9" fill="{a.OK}" stroke="#fff" stroke-width="2.5"/>')
en(a, ring(a, 1017, 337, 138, 106, a.OK, rx=18), 89, 100, still=1)
en(a, a.text(1086, 470, "allow-lan=yes", 14, a.OK, a.MONO, 600, "middle") + a.text(1086, 490, "client-allowed-", 14, a.OK, a.MONO, 600, "middle")
   + a.text(1086, 508, "address=", 14, a.OK, a.MONO, 600, "middle") + a.text(1086, 526, "192.168.88.0/24", 14, a.OK, a.MONO, 600, "middle"), 80, 100, still=1)

narr(a, [
    (0, 25, "El celular no elige el camino: lo decide el nombre al que se conecta.", a.TXT),
    (25, 50, "Directo es lo más rápido: el celular le habla al router.", a.OK),
    (50, 75, "Por relay da una vuelta más y puede ir más lento, pero cifrado de punta a punta.", a.AMB),
    (75, 100, "La LAN se da a quien la necesita; el resto, solo internet a través del router.", a.OK),
], still_idx=3)

escribir(a, "19-r1.svg", "Back To Home directo o por relay",
         "Animación en cuatro tiempos con un celular en datos móviles, el router con la interfaz back-to-home-vpn (192.168.216.1/24) y LAN 192.168.88.1, el NVR en 192.168.88.50 "
         "y un relay de MikroTik. Arriba, /ip/cloud/print con vpn-relay-ipv4-status y a qué resuelve vpn-dns-name. "
         "1: con IP pública, el estado es reachable directly y el nombre <serie>.vpn.mynetname.net resuelve a la IP pública del router. "
         "2: el túnel WireGuard va directo del celular al router; el celular usa 192.168.216.2. "
         "3: detrás de CGNAT, el estado pasa a reachable via relay: el nombre resuelve al relay, el router mantiene abierta su conexión con él y el tráfico pasa cifrado, sin que el relay pueda leerlo. "
         "4: el usuario tiene allow-lan=yes y client-allowed-address=192.168.88.0/24, así que el paquete del celular llega al NVR.",
         [6, 36, 66, 88, 96])
