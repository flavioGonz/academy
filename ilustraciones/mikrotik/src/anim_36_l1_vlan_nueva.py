#!/usr/bin/env python3
"""Lección 36 (Zonas con listas) · Laboratorio paso 6: una VLAN nueva sin zona cae al drop final; al entrar a ADMIN hereda la política sin tocar reglas."""
from _anim_r20_31 import *

a, _ = nuevo(24, "MIKROTIK · ZONAS CON LISTAS · PASO 6", "Una red nueva hereda la política al entrar a su lista",
             ["vlan10-admin ya tiene IP, pero todavía no está en ninguna zona.",
              "La PC pide internet: ninguna regla de zona coincide. Drop final.",
              "Un member/add la mete en ADMIN. No se toca ninguna regla.",
              "El mismo paquete coincide con lab: ADMIN a WAN y sale."], still=3)

dev(a, 48, 182, 330, 100, "PC de administración", "vlan10-admin · 10.10.10.20", ssize=14)

# listas
a.add(a.box(48, 296, 380, 236, a.WHITE, a.LINE, rx=14))
a.add(a.text(66, 326, "/interface/list", 15, a.GREY, a.MONO))
a.add(a.text(66, 364, "ADMIN", 16, a.INK, a.MONO, 600))
flip(a, 196, 364, [(0, 54, "vacía", a.GREY), (54, 100, "vlan10-admin", a.OK)], size=16, still_idx=1)
en(a, ring(a, 56, 340, 364, 36, a.OK, rx=10, sw=3), 54, 75)
a.add(a.text(66, 410, "GESTION", 16, a.INK, a.MONO, 600))
a.add(a.text(196, 410, "bridge, VPN", 16, a.TXT, a.MONO))
a.add(a.text(66, 456, "CLIENTES", 16, a.INK, a.MONO, 600))
a.add(a.text(196, 456, "include=ADMIN,CCTV,…", 15, a.TXT, a.MONO))
en(a, a.text(196, 484, "por include: vlan10-admin", 15, a.OK, a.MONO, 600), 56, 100, still=1)
en(a, a.text(66, 516, "DNS y DHCP del router, sin regla nueva", 14, a.OK, a.SANS, 600), 58, 100, still=1)

# reglas de forward
RULES = [("accept", "GESTION → todas", "lab: GESTION a todas", a.OK, a.OKBG),
         ("accept", "ADMIN → WAN", "lab: ADMIN a WAN", a.OK, a.OKBG),
         ("accept", "INVITADOS → WAN", "lab: INVITADOS a WAN", a.OK, a.OKBG),
         ("accept", "ADMIN → CCTV (NVR)", "lab: ADMIN al NVR", a.OK, a.OKBG),
         ("drop", "el resto · log", "lab: drop final entre zonas", a.BAD, a.BADBG)]
RX, RW, R0, RS, RH = 540, 612, 206, 64, 52
a.add(a.text(RX, R0 - 12, "chain=forward · in-interface-list → out-interface-list", 15, a.GREY, a.MONO))
cy = []
for i, (act, m, c_, col, bg) in enumerate(RULES):
    y = R0 + i * RS
    cy.append(y + RH / 2)
    a.add(a.box(RX, y, RW, RH, a.WHITE, a.LINE, rx=12))
    a.add(a.pill(RX + 14, y + 12, act, col, bg, 14, 28))
    a.add(a.text(RX + 110, y + 32, m, 15, a.INK, a.MONO, 600))
    a.add(a.text(RX + RW - 16, y + 32, c_, 14, a.GREY, a.MONO, 400, "end"))
PX = 484
a.add(wire(PX, cy[0], PX, cy[-1], a.LINE, 2, "4 6"))

def hit(i, t0, t1, c, still=0):
    en(a, ring(a, RX - 3, R0 + i * RS - 3, RW + 6, RH + 6, c, rx=14), t0, t1, still)

# 1. sin zona
en(a, a.text(66, 300 - 12, "", 1), 0, 1)
en(a, a.pill(66, 244, "sin zona: en ninguna lista", a.AMB, a.AMBBG, 14, 28), 2, 52)

# 2. baja hasta el drop final
pts = [(26, 348, 230), (28, PX, 230), (29, PX, cy[0])]
t = 29
for k in range(1, 5):
    t += 2.4
    pts.append((t, PX, cy[k]))
pts.append((49, PX, cy[4]))
go(a, "", [(378, 230), (PX, 230)], 26, 28, hold=0, inner=pillc(a, "internet", bg=a.GREY, size=14))
go(a, "", [(PX, 230), (PX, cy[0]), (PX, cy[4])], 28, 38, hold=11, inner=pillc(a, "internet", bg=a.GREY, size=14))
hit(4, 38, 50, a.BAD)
en(a, mark(a, RX + RW - 250, cy[4] - 30, ok=False), 38, 50)

# 3. member add
en(a, term(a, 48, 548, 700, ["/interface/list/member/add list=ADMIN interface=vlan10-admin"], size=15), 52, 100, still=1)

# 4. el mismo paquete sale por ADMIN a WAN
go(a, "", [(378, 230), (PX, 230), (PX, cy[0]), (PX, cy[1])], 77, 83, hold=17, inner=pillc(a, "internet", bg=a.OK, size=14))
hit(1, 83, 100, a.OK, still=1)
fijo(a, at(pillc(a, "internet", bg=a.OK, size=14), PX, cy[1]))
en(a, a.text(RX + RW - 16, cy[4] + 50, "las reglas no cambiaron", 15, a.OK, a.SANS, 600, "end"), 80, 100, still=1)

narr(a, [
    (0, 25, "Una interfaz que no está en ninguna lista no coincide con ninguna regla de zona.", a.TXT),
    (25, 50, "El drop final corta el forward de toda red que no tenga zona.", a.BAD),
    (50, 75, "La interfaz entra a ADMIN y, por include, también a CLIENTES.", a.TXT),
    (75, 100, "Internet, DNS y el NVR, como cualquier ADMIN. Y nada más.", a.OK),
], still_idx=3)

escribir(a, "36-l1.svg", "Una VLAN nueva entra a su zona",
         "Animación en cuatro tiempos con una PC de administración en vlan10-admin (10.10.10.20), las listas de interfaces y cinco reglas de forward: "
         "GESTION a todas, ADMIN a WAN, INVITADOS a WAN, ADMIN al NVR y el drop final entre zonas con log ZONA-DROP. "
         "1: la VLAN 10 ya tiene IP pero no está en ninguna zona; la lista ADMIN está vacía. 2: la PC pide internet, el paquete baja por todas las reglas sin coincidir y lo corta el drop final. "
         "3: con /interface/list/member/add list=ADMIN interface=vlan10-admin la interfaz entra a ADMIN y, por include, también a CLIENTES, que tiene DNS y DHCP del router. "
         "4: el mismo paquete coincide con lab: ADMIN a WAN y sale; las reglas no cambiaron.",
         [10, 35, 45, 62, 92])
