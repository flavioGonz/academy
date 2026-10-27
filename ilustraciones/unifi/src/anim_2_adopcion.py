#!/usr/bin/env python3
"""Lección 2 · teoría: descubrimiento en capa 2, Adopt e inform periódico; y el segundo DHCP."""
from _anim_unifi import *  # noqa

a = new(24, "Adopción", "Del reset al inform: cómo se adopta un AP", [
    "El AP toma IP por DHCP y se anuncia en la red local (UDP 10001).",
    "Adopt: el controlador le da la config, su URL de inform y claves SSH nuevas.",
    "Inform periódico por TCP 8080: van estadísticas, vuelven cambios.",
    "Si el módem del cliente también da IP, el AP va a otro rango y nadie lo ve.",
], still=2)

# AP
AX, AY, AW, AH = 60, 210, 300, 120
a.add(a.box(AX, AY, AW, AH, A.WHITE, A.LINE, rx=14))
a.add(ap_icon(a, AX + 44, AY + 42, 22))
a.add(a.text(AX + 80, AY + 50, "AP reseteado", 20, A.INK, A.HEAD, 600))
vis(a, a.text(AX + 24, AY + 86, "IP 192.168.88.20", 15, A.TXT, A.MONO), 0, 2)
vis(a, a.text(AX + 24, AY + 86, "IP de otro rango", 15, A.BAD, A.MONO, 600), 3)
vis(a, a.text(AX + 24, AY + 108, "SSH: ubnt / ubnt", 15, A.TXT, A.MONO), 0, 0)
s0, s1 = ph(a, 1)
at(a, a.text(AX + 24, AY + 108, "SSH: claves del sitio", 15, A.OK, A.MONO, 600), s0 + 12, ph(a, 3)[1], still=1)

# controlador
CX, CY, CW, CH = 840, 210, 310, 120
a.add(a.box(CX, CY, CW, CH, A.INK, None, rx=14))
a.add(a.text(CX + 22, CY + 44, "Controlador", 20, A.WHITE, A.HEAD, 600))
a.add(a.text(CX + 22, CY + 68, "UniFi Network", 15, SUB_DARK, A.MONO))
vis(a, pill(a, CX + 22, CY + 80, "Pending Adoption", "amb"), 0)
vis(a, pill(a, CX + 22, CY + 80, "adoptando", "info"), 1)
vis(a, pill(a, CX + 22, CY + 80, "conectado", "ok"), 2)
vis(a, pill(a, CX + 22, CY + 80, "no lo ve", "bad"), 3)

# red local (bus) y DHCP
BUS = 400
a.add(line(a, [(AX + 150, AY + AH), (AX + 150, BUS)], A.GREY, 2.5))
a.add(line(a, [(CX + 155, CY + CH), (CX + 155, BUS)], A.GREY, 2.5))
a.add(line(a, [(AX + 150, BUS), (CX + 155, BUS)], A.GREY, 3))
a.add(a.text(600, BUS - 12, "misma red · misma VLAN", 15, A.GREY, A.MONO, anchor="middle"))
a.add(line(a, [(600, BUS), (600, 450)], A.GREY, 2.5))
a.add(node(a, 470, 450, 260, 70, "Servidor DHCP", "uno solo en esta red", ssize=14))

# 1: DHCP y anuncio
s0, s1 = ph(a, 0)
token(a, [(600, 440), (600, BUS), (AX + 150, BUS), (AX + 150, AY + AH + 16)], s0 + 1, s0 + 8, "IP 192.168.88.20", bg=A.GREY, hold=s0 + 9)
for k in range(3):
    token(a, [(AX + AW + 10, 270), (CX - 14, 270)], s0 + 10 + k * 4, s0 + 15 + k * 4, "aviso UDP 10001", bg=A.CYAN, hold=s0 + 15.4 + k * 4)

# 2: Adopt
s0, s1 = ph(a, 1)
for k, lab in enumerate(["config del sitio", "URL de inform", "claves SSH"]):
    token(a, [(CX - 14, 240 + k * 30), (AX + AW + 90, 240 + k * 30)], s0 + 1 + k * 3, s0 + 9 + k * 3, lab, bg=A.BLUE, hold=s1 - 1)
at(a, a.text(AX + 24, AY + 108, "SSH: ubnt / ubnt", 15, A.GREY, A.MONO) + f'<line x1="{AX + 22}" y1="{AY + 103}" x2="{AX + 180}" y2="{AY + 103}" stroke="{A.BAD}" stroke-width="2.5"/>', s0, s0 + 12)

# 3: inform periódico
s0, s1 = ph(a, 2)
for k in range(3):
    token(a, [(AX + AW + 60, 255), (CX - 60, 255)], s0 + 1 + k * 7, s0 + 6 + k * 7, "inform :8080", bg=A.CYAN, hold=s0 + 6.3 + k * 7, still=1 if k == 1 else 0)
    token(a, [(CX - 60, 295), (AX + AW + 60, 295)], s0 + 4 + k * 7, s0 + 8 + k * 7, "cambios", bg=A.BLUE, hold=s0 + 8.3 + k * 7, still=1 if k == 1 else 0)

# 4: segundo DHCP
vis(a, a.box(60, 450, 300, 70, A.AMBBG, A.AMB, rx=14) + a.text(80, 480, "Módem del cliente", 20, A.INK, A.HEAD, 600)
    + a.text(80, 504, "también reparte IP", 14, A.AMB, A.MONO, 600) + line(a, [(210, 450), (210, BUS)], A.AMB, 2.5), 3)
s0, s1 = ph(a, 3)
token(a, [(270, 436), (270, AY + AH + 16)], s0 + 2, s0 + 7, "IP de otro rango", bg=A.AMB, hold=s0 + 8)
token(a, [(AX + AW + 10, 270), (600, 270)], s0 + 10, s0 + 15, "aviso", bg=A.CYAN, hold=s1 - 1)
vis(a, xmark(a, 660, 270), 3)
vis(a, note(a, 60, 560, 1092, "Un solo DHCP: el descubrimiento en capa 2 necesita la misma red.", "bad", size=15, h=40), 3)

write(a, "2-t1.svg", "Cómo se adopta un AP UniFi", mid_pcts(a))
