#!/usr/bin/env python3
"""Lección 1 · teoría: cómo aparece el portero en la red (DHCP y descubrimiento del IP Scanner)."""
from _anim_akuvox import Anim, A, token, chip, node, note, appear, mark, finish

a = Anim(T=25, kicker="AKUVOX · PRIMER ACCESO", title="Cómo el portero consigue IP y cómo lo encontrás")
a.steps([
    "Al encender, el portero manda DHCPDISCOVER por broadcast a toda la red.",
    "El router le ofrece una IP del rango y el portero la toma con su gateway.",
    "El IP Scanner de la PC pregunta en la red local por equipos Akuvox.",
    "El portero contesta con modelo, IP y MAC. Con la IP entrás por navegador.",
    "Con el firewall de la PC activo, la respuesta se descarta: no aparece nada.",
], still=3)

BUS = 420
PX, RX, CX = 200, 600, 1000      # centros de portero, router y PC
# red
a.add(f'<line x1="70" y1="{BUS}" x2="1130" y2="{BUS}" stroke="{A.BLUE}" stroke-width="4" stroke-linecap="round"/>')
a.add(a.text(70, BUS + 30, "red 192.168.88.0/24", 15, A.BLUE, A.MONO, 600))
for x in (PX, RX, CX):
    a.add(f'<line x1="{x}" y1="322" x2="{x}" y2="{BUS}" stroke="{A.BLUE}" stroke-width="3"/>')

# equipos
a.add(a.box(PX - 120, 232, 240, 90, A.WHITE, A.LINE))
a.add(a.text(PX - 100, 270, "Portero", 20, A.INK, A.HEAD, 600))
appear(a, a.text(PX - 100, 298, "todavía sin IP", 15, A.GREY, A.MONO), 0, 30.5, still=0)
appear(a, a.text(PX - 100, 298, "192.168.88.X · gw .1", 15, A.OK, A.MONO, 600), 30.5, 100, still=1)
a.add(node(a, RX - 130, 232, 260, 90, "Router", "DHCP · gw 192.168.88.1"))
a.add(node(a, CX - 140, 232, 280, 90, "PC · IP Scanner", "misma subred"))

# 1 DISCOVER por broadcast
for dst in (RX, CX):
    token(a, [(PX, 322), (PX, BUS), (dst, BUS), (dst, 322)], 3, 13, chip(a, "DISCOVER", bg=A.GREY), hold=14)
appear(a, a.text(PX + 14, BUS - 14, "broadcast", 15, A.GREY, A.MONO, 600), 3, 20, still=0)
# 2 oferta
token(a, [(RX, 322), (RX, BUS), (PX, BUS), (PX, 322)], 22, 30, chip(a, "oferta · 192.168.88.X"))
appear(a, a.box(PX - 120, 232, 240, 90, "none", A.OK, sw=3), 30.5, 40, still=0)
# 3 consulta del IP Scanner
token(a, [(CX, 322), (CX, BUS), (PX, BUS), (PX, 322)], 42, 52, chip(a, "¿equipos Akuvox?", bg=A.BLUE))
# 4 respuesta
token(a, [(PX, 322), (PX, BUS), (CX, BUS), (CX, 322)], 62, 72, chip(a, "modelo · IP · MAC", bg=A.OK))
# 5 respuesta bloqueada por el firewall de la PC
token(a, [(CX, 322), (CX, BUS), (PX, BUS), (PX, 322)], 80.5, 85, chip(a, "¿equipos Akuvox?", bg=A.BLUE))
token(a, [(PX, 322), (PX, BUS), (CX, BUS), (CX, 346)], 86, 93, chip(a, "modelo · IP · MAC", bg=A.OK), hold=94)
fw = (f'<rect x="{CX - 95}" y="334" width="190" height="30" rx="8" fill="{A.BADBG}" stroke="{A.BAD}" stroke-width="2"/>'
      + a.text(CX, 355, "firewall de la PC", 14, A.BAD, A.MONO, 600, "middle"))
appear(a, fw, 80, 100, still=0)
appear(a, mark(a, CX + 118, 349, ok=False, r=14), 93, 100, still=0)

# resultado del IP Scanner
TX, TY, TW = 760, 478, 392
a.add(a.box(TX, TY, TW, 150, A.WHITE, A.LINE))
a.add(a.box(TX, TY, TW, 34, "#E6EEF6", None, rx=14))
a.add(a.text(TX + 18, TY + 23, "IP Scanner · resultados", 15, A.INK, A.SANS, 600))
a.add(a.text(TX + 18, TY + 62, "MODELO", 13, A.GREY, A.MONO))
a.add(a.text(TX + 130, TY + 62, "IP", 13, A.GREY, A.MONO))
a.add(a.text(TX + 290, TY + 62, "MAC", 13, A.GREY, A.MONO))
appear(a, a.box(TX + 10, TY + 76, TW - 20, 40, A.OKBG, None, rx=8)
       + a.text(TX + 18, TY + 102, "R20A", 16, A.INK, A.MONO, 600)
       + a.text(TX + 130, TY + 102, "192.168.88.X", 16, A.INK, A.MONO, 600)
       + a.text(TX + 290, TY + 102, "XX:XX:…", 16, A.TXT, A.MONO), 72, 80, still=1)
appear(a, a.text(TX + 18, TY + 102, "sin resultados", 16, A.BAD, A.MONO, 600), 93, 100, still=0)
appear(a, a.text(TX + 18, TY + 138, "→ en el navegador: http://192.168.88.X", 14, A.BLUE, A.MONO, 600), 73, 80, still=1)

s, _ = note(a, 48, 478, 560, "Sin pantalla, la IP se anuncia de otra forma",
            ["Voz (un botón), código en el teclado, menú con PIN", "de sistema o el IP Scanner, que sirve para todos.",
             "Pausá el firewall solo mientras escanea."], "info")
a.add(s)

finish(a, "1-t1.svg", "El portero pide IP por DHCP y el IP Scanner lo encuentra",
       "Animación en cinco tiempos sobre la red 192.168.88.0/24 con portero, router y PC con IP Scanner. "
       "1: al encender, el portero, todavía sin IP, manda un DHCPDISCOVER por broadcast que llega a toda la red. "
       "2: el router le ofrece una IP del rango, 192.168.88.X, y el portero la toma con su gateway 192.168.88.1. "
       "3: el IP Scanner de la PC manda una consulta en la red local buscando equipos Akuvox. "
       "4: el portero contesta con modelo, IP y MAC y aparece en la lista de resultados; con esa IP se entra por navegador con admin / admin una sola vez. "
       "5: con el firewall de la PC activo, la respuesta llega y se descarta, y el IP Scanner queda sin resultados. "
       "Nota: sin pantalla, la IP se anuncia por voz, por código en el teclado, por menú con PIN de sistema o con el IP Scanner; el firewall se pausa solo mientras escanea.",
       [8, 27, 47, 75, 95])
