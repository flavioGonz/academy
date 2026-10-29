#!/usr/bin/env python3
"""Lección 5 · Resumen, "Cómo se ve en la red": tres redes por función en el mismo uplink. Cada trama lleva su
etiqueta 802.1Q (TPID 0x8100 y VLAN ID de 12 bits); el gateway saca la etiqueta y cada VLAN es una subred con su
DHCP; con el firewall clásico el ruteo entre VLANs se permite por defecto; con zonas, Hotspot hacia Internal es
Allow Return y el invitado no puede iniciar. Fuentes: theory_md e idea_md de la lección (IEEE 802.1Q, LazyAdmin,
WunderTech, notas de Network 11.0.97); el formato de la etiqueta es el de IEEE 802.1Q."""
from _anim_red_unifi import *  # noqa

a = new(26, "VLAN por función", "Tres redes en un cable, y quién puede hablar con quién", [
    "Por el uplink viajan las tres redes: cada trama lleva su etiqueta 802.1Q.",
    "El gateway lee la etiqueta: cada VLAN es una subred con su puerta y su DHCP.",
    "Antes, firewall clásico: entre VLANs se ruteaba y se permitía por defecto.",
    "Con zonas: Invitados está en Hotspot y no puede iniciar hacia Internal.",
], still=3)

C10, C20, C30 = a.BLUE, a.AMB, a.CYAN
ROWS = [(186, "NVR · Staff", "10.10.10.20", "laptop", C10, "VLAN 10"),
        (296, "Celular · Invitados", "192.168.20.31", "phone", C20, "VLAN 20"),
        (406, "Cámara · CCTV", "192.168.30.11", "camera", C30, "VLAN 30")]
PORTY = [286, 346, 406]
for (y, t, s, ic, c, v), py in zip(ROWS, PORTY):
    a.add(dev(a, 48, y, 260, 90, t, s, icon=ic))
    a.add(poly([(308, y + 45), (350, y + 45), (350, py), (400, py)], c, 4))
    a.add(a.text(318, y + 37, v[5:], 15, c, a.MONO, 600))

a.add(dev(a, 400, 246, 180, 200, "Switch", "USW", icon="server"))
a.add(wire(580, 336, 760, 336, C10, 4))
a.add(wire(580, 346, 760, 346, C20, 4))
a.add(wire(580, 356, 760, 356, C30, 4))
a.add(a.text(670, 384, "uplink · trunk", 15, a.GREY, a.MONO, 400, "middle"))

GX, GY, GW, GH = 760, 186, 392, 310
a.add(a.box(GX, GY, GW, GH, a.INK, None, rx=14))
a.add(glyph(a, "server", GX + 18, GY + 18, a.CYAN))
a.add(a.text(GX + 62, GY + 40, "Gateway UniFi", 20, a.WHITE, a.HEAD, 600))
GROWS = [("VLAN 10", "10.10.10.1/24", C10, "Internal"), ("VLAN 20", "192.168.20.1/24", C20, "Hotspot"), ("VLAN 30", "192.168.30.1/24", C30, "Internal")]
for i, (v, n, c, z) in enumerate(GROWS):
    yy = GY + 92 + i * 70
    row = (f'<rect x="{GX + 20}" y="{yy - 22}" width="6" height="44" rx="3" fill="{c}"/>'
           + a.text(GX + 40, yy - 2, v, 16, a.WHITE, a.MONO, 600)
           + a.text(GX + 40, yy + 20, f"{n} · DHCP", 15, SKY, a.MONO))
    vis(a, row, 1, 3)
    vis(a, pill(a, GX + GW - 18, yy - 14, z, "ok" if z == "Internal" else "amb", anchor="end"), 3)

# 1 · tramas etiquetadas por el uplink
s0, s1 = ph(a, 0)
for k, (c, v) in enumerate(((C10, "VID 10"), (C20, "VID 20"), (C30, "VID 30"))):
    go(a, [(590, 300), (750, 300)], s0 + 2 + k * 6, s0 + 7 + k * 6, v, c, hold=s0 + 7.5 + k * 6)
TAG = [("MAC destino", 160, a.WHITE), ("MAC origen", 150, a.WHITE), ("802.1Q · 0x8100 · VID 20", 300, a.AMBBG), ("tipo", 90, a.WHITE), ("datos", 200, a.WHITE)]
x = 48
tag = a.text(48, 532, "La trama en el uplink:", 15, a.TXT, a.SANS, 600)
for lab, w, bg in TAG:
    tag += a.box(x, 546, w - 8, 44, bg, a.AMB if bg == a.AMBBG else a.LINE, rx=8, sw=2)
    tag += a.text(x + (w - 8) / 2, 574, lab, 15, a.AMB if bg == a.AMBBG else a.INK, a.MONO, 600, "middle")
    x += w
tag += a.text(x + 4, 574, "4 bytes, 12 bits de VLAN", 15, a.AMB, a.SANS, 600)
during(a, tag, s0 + 1, s1)

# 2 · el gateway: subred, puerta y DHCP
s0, s1 = ph(a, 1)
go(a, [(750, 300), (590, 300)], s0 + 3, s0 + 9, "Ack · 192.168.20.31", C20, hold=s0 + 10)
during(a, a.text(48, 560, "Cada VLAN es un dominio aparte: sin DHCP propio, el cliente se asocia y no recibe IP.", 16, a.INK, a.SANS, 600),
       s0 + 1, s1)

FWD = [(308, 341), (350, 341), (350, 346), (580, 346), (740, 346)]
BACK = [(740, 356), (580, 356), (350, 406), (350, 451), (308, 451)]
# 3 · clásico: pasa
s0, s1 = ph(a, 2)
go(a, FWD, s0 + 2, s0 + 9, "→ cámara", C20, hold=s0 + 9.5)
go(a, BACK, s0 + 10, s0 + 17, "→ cámara", C20, hold=s0 + 20)
during(a, check(a, 330, 451, 15), s0 + 17, s1)
during(a, nbox(a, 48, 520, 700, 76, "Firewall clásico", ["Permitía el tráfico entre VLANs por defecto: había que escribir los bloqueos."], "bad"),
       s0 + 1, s1)

# 4 · zonas: bloqueado
s0, s1 = ph(a, 3)
go(a, FWD[:-1] + [(690, 346)], s0 + 2, s0 + 9, "→ cámara", C20, hold=s1 - 0.5, still=1)
during(a, xmark(a, 742, 346, 17), s0 + 9, 100, still=1)
during(a, nbox(a, 48, 520, 700, 76, "Firewall por zonas (Network 11 migra todos los sitios)", ["Hotspot hacia Internal es Allow Return: solo contesta, nunca inicia."], "ok"),
       s0 + 1, 100, still=1)

status(a, 640, [
    (0, 25, "Un SSID se asigna a una red y sale por su VLAN.", a.INK, 0),
    (25, 50, "Separar en capa 2 es la mitad: la otra mitad pasa en el gateway.", a.INK, 0),
    (50, 75, "Sin bloqueos escritos, el celular del invitado llegaba a la cámara.", a.BAD, 0),
    (75, 100, "Cada red en su zona: la Zone Matrix dice qué puede hablar con qué.", a.OK, 1),
])

write(a, 5, "r1", "Tres redes por función en un mismo cable",
      "Animación en cuatro tiempos con un NVR en la red Staff (VLAN 10, 10.10.10.20), un celular en Invitados (VLAN 20, 192.168.20.31) y una cámara en CCTV (VLAN 30, 192.168.30.11), "
      "un switch y el gateway UniFi unidos por un uplink troncal. "
      "1: por el uplink viajan las tres redes; cada trama lleva la etiqueta 802.1Q de 4 bytes, con 0x8100 y un VLAN ID de 12 bits, por ejemplo VID 20. "
      "2: el gateway lee la etiqueta; cada VLAN es una subred con su puerta y su DHCP: 10.10.10.1/24, 192.168.20.1/24 y 192.168.30.1/24, y el celular recibe 192.168.20.31. "
      "3: antes, con el firewall clásico, el tráfico entre VLANs se permitía por defecto y el celular del invitado llegaba a la cámara. "
      "4: con el firewall por zonas, al que Network 11 migra todos los sitios, Staff y CCTV están en Internal e Invitados en Hotspot; "
      "Hotspot hacia Internal es Allow Return, el invitado no puede iniciar y la conexión se bloquea en el gateway.",
      [10, 37, 62, 90])
