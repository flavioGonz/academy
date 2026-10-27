#!/usr/bin/env python3
"""Lección 11 · teoría: cómo lee nmap -sS cada puerto (SYN-ACK abierto, RST cerrado, silencio filtrado)."""
from _anim_akuvox import Anim, A, token, chip, appear, mark, finish

a = Anim(T=24, kicker="AKUVOX · PORTERO BLINDADO", title="Qué le contesta el portero a nmap")
a.steps([
    "nmap -sS manda un SYN a cada puerto TCP y mira qué vuelve.",
    "Vuelve SYN-ACK: el puerto está abierto. Desde usuarios, es un hueco.",
    "Vuelve RST: el puerto está cerrado. El SYN pasó, pero no hay servicio.",
    "No vuelve nada: el firewall descartó el SYN. El puerto queda filtrado.",
], still=3)

ROWS = [(272, "80", "web"), (382, "23", "telnet"), (492, "554", "RTSP")]
PCX, FWX, POX = 48, 470, 840
# PC
a.add(a.box(PCX, 180, 250, 380, A.WHITE, A.LINE))
a.add(a.text(PCX + 20, 214, "PC de usuarios", 19, A.INK, A.HEAD, 600))
a.add(a.text(PCX + 20, 238, "nmap -sS 10.10.10.21", 14, A.GREY, A.MONO))
# firewall
a.add(a.box(FWX, 180, 150, 380, A.SLATE, A.LINE))
a.add(a.text(FWX + 75, 214, "Firewall", 18, A.INK, A.HEAD, 600, "middle"))
a.add(a.text(FWX + 75, 238, "reglas VLAN", 14, A.GREY, A.MONO, 400, "middle"))
# portero
a.add(a.box(POX, 180, 312, 380, A.WHITE, A.LINE))
a.add(a.text(POX + 20, 214, "Portero", 19, A.INK, A.HEAD, 600))
a.add(a.text(POX + 20, 238, "10.10.10.21 · VLAN porteros", 14, A.GREY, A.MONO))
for y, port, svc in ROWS:
    a.add(f'<line x1="{PCX + 250}" y1="{y}" x2="{POX}" y2="{y}" stroke="{A.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
    a.add(a.box(POX + 16, y - 26, 280, 52, A.SLATE, None, rx=10))
    a.add(a.text(POX + 32, y + 6, f"TCP {port}", 17, A.INK, A.MONO, 600))
    a.add(a.text(POX + 140, y + 6, svc, 15, A.GREY, A.MONO))
    a.add(a.text(PCX + 20, y + 6, f"{port}/tcp", 16, A.INK, A.MONO, 600))

# 1: SYN a los tres
for i, (y, port, _) in enumerate(ROWS):
    end = FWX + 75 if port == "554" else POX + 4
    token(a, [(PCX + 260, y - 14), (end, y - 14)], 3 + i * 1.5, 12 + i * 1.5, chip(a, "SYN", bg=A.BLUE, size=13, h=24),
          hold=13.2 + i * 1.5)
# 2: SYN-ACK desde el 80
y80 = ROWS[0][0]
token(a, [(POX - 6, y80 + 14), (PCX + 262, y80 + 14)], 28, 37, chip(a, "SYN-ACK", bg=A.BAD, size=13, h=24), hold=37.6)
appear(a, a.pill(PCX + 236, y80 - 14, "abierto", A.BAD, A.BADBG, 14, 28, "end"), 37, 100, still=1)
appear(a, a.box(POX + 16, y80 - 26, 280, 52, "none", A.BAD, rx=10, sw=3) + a.text(POX + 284, y80 + 6, "hueco", 14, A.BAD, A.MONO, 600, "end"), 37, 100, still=1)
# 3: RST desde el 23
y23 = ROWS[1][0]
token(a, [(POX - 6, y23 + 14), (PCX + 262, y23 + 14)], 53, 62, chip(a, "RST", bg=A.AMB, size=13, h=24), hold=62.6)
appear(a, a.pill(PCX + 236, y23 - 14, "cerrado", A.AMB, A.AMBBG, 14, 28, "end"), 62, 100, still=1)
# 4: silencio en el 554
y554 = ROWS[2][0]
appear(a, mark(a, FWX + 75, y554 - 14, False, 15) + a.text(FWX + 75, y554 + 30, "descarta", 14, A.BAD, A.MONO, 600, "middle"), 77, 100, still=1)
appear(a, a.text(PCX + 120, y554 + 40, "esperando…", 14, A.GREY, A.MONO), 78, 88, still=0)
appear(a, a.pill(PCX + 236, y554 - 14, "filtrado", A.OK, A.OKBG, 14, 28, "end"), 88, 100, still=1)

a.add(a.text(48, 600, "Desde la red de usuarios, lo esperado es que todo figure filtrado. Lo que conteste es un hueco.", 16, A.INK, A.SANS, 600))
a.add(a.text(48, 628, "-sU prueba UDP: es más lento, porque un puerto UDP abierto no responde.", 15, A.TXT, A.SANS))

finish(a, "11-t1.svg", "Cómo lee nmap -sS cada puerto",
       "Animación en cuatro tiempos con la PC de la red de usuarios a la izquierda, el firewall de la VLAN en el medio y el portero 10.10.10.21 a la derecha, con tres puertos de ejemplo: TCP 80, 23 y 554. "
       "1: nmap -sS manda un SYN a cada puerto; los del 80 y el 23 llegan al portero y el del 554 queda en el firewall. "
       "2: el 80 contesta SYN-ACK y nmap lo marca abierto: desde la red de usuarios es un hueco. "
       "3: el 23 contesta RST y nmap lo marca cerrado: el SYN pasó pero no hay servicio. "
       "4: del 554 no vuelve nada porque el firewall descartó el SYN, y nmap lo marca filtrado. "
       "Nota: desde la red de usuarios lo esperado es que todo figure filtrado; -sU prueba UDP y es más lento porque un puerto UDP abierto no responde.",
       [12, 40, 66, 95])
