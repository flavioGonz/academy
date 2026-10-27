#!/usr/bin/env python3
"""Lección 33, teoría "Connection tracking" y "Orden": paquetes que bajan por la cadena input hasta la primera regla que coincide."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=24, kicker="MIKROTIK · FIREWALL", title="Input: de arriba abajo, manda la primera que coincide")
a.steps([
    "Nuevo desde internet al 22: baja hasta el drop del final.",
    "Nuevo desde la oficina: lo acepta la regla de admins.",
    "El paquete siguiente es established: sale en la primera.",
    "Uno que no encaja con ninguna conexión es invalid: drop.",
], still=2)

RULES = [("accept", "connection-state=established,related,untracked", a.OK),
         ("drop", "connection-state=invalid", a.BAD),
         ("accept", "protocol=icmp", a.OK),
         ("accept", "src-address-list=admins", a.OK),
         ("drop", "in-interface-list=!LAN", a.BAD)]
RX, RW, R0, RS, RHh = 292, 562, 196, 60, 48
a.add(a.text(RX, R0 - 14, "chain=input", 15, a.GREY, a.MONO))
cy = []
for i, (act, s, c) in enumerate(RULES):
    y = R0 + i * RS
    cy.append(y + RHh / 2)
    a.add(a.box(RX, y, RW, RHh, a.WHITE, a.LINE, rx=12))
    a.add(a.text(RX + 18, y + 30, str(i + 1), 15, a.GREY, a.MONO, 600))
    a.add(a.pill(RX + 42, y + 10, act, c, a.OKBG if c == a.OK else a.BADBG, 14, 28))
    a.add(a.text(RX + 136, y + 30, s, 15, a.INK, a.MONO))

def hit(i, t0, t1, ok, still=0):
    y = R0 + i * RS
    c = a.OK if ok else a.BAD
    en(a, f'<rect x="{RX - 3}" y="{y - 3}" width="{RW + 6}" height="{RHh + 6}" rx="14" fill="none" stroke="{c}" stroke-width="3.5"/>'
          + marca(a, RX + RW + 26, y + RHh / 2, ok=ok), t0, t1, still)

PX = 150
a.add(a.text(PX, R0 - 14, "paquete que llega", 15, a.GREY, a.MONO, 400, "middle"))
a.add(f'<line x1="{PX}" y1="{R0}" x2="{PX}" y2="{cy[-1]}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
for c in cy:
    a.add(f'<line x1="{PX + 100}" y1="{c}" x2="{RX}" y2="{c}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="2 6"/>')

def baja(label, bg, t0, hasta, t_end):
    pts = [(t0, PX, cy[0])]
    t = t0 + 2
    for k in range(1, hasta + 1):
        pts.append((t, PX, cy[k])); t += 2.2
    pts.append((t_end, PX, cy[hasta]))
    paquete(a, label, pts, t0, t_end, bg=bg)
    return t - 2.2

t = baja("nuevo · WAN → :22", a.GREY, 1, 4, 24.5)
hit(4, t, 25, False)
t = baja("nuevo · admins → :22", a.CYAN, 26, 3, 49.5)
hit(3, t, 50, True)
t = baja("established", a.OK, 51, 0, 74.5)
hit(0, 52, 75, True, still=1)
t = baja("invalid", a.BAD, 76, 1, 99.5)
hit(1, t, 100, False)
fijo(a, f'<g transform="translate({PX} {cy[0]})">' + pill_c(a, "established", "#FFFFFF", a.OK) + "</g>")

# ---- tabla de conexiones
CX, CW = 914, 238
a.add(a.box(CX, R0, CW, 4 * RS + RHh, a.INK, rx=16))
a.add(a.text(CX + 18, R0 + 32, "Conexiones", 18, "#FFFFFF", a.HEAD, 600))
a.add(a.text(CX + 18, R0 + 56, "connection tracking", 15, LIGHT, a.MONO))
en(a, a.text(CX + 18, R0 + 104, "vacía", 15, LIGHT, a.MONO), 0, 37)
ent = a.box(CX + 12, R0 + 80, CW - 24, 76, a.NAVY2, rx=10) + a.text(CX + 26, R0 + 106, "admins → :22", 16, "#FFFFFF", a.MONO, 600)
en(a, ent, 37, 100, still=1)
en(a, a.pill(CX + 26, R0 + 118, "new", GOLD, "#2C4A6B", 14, 28), 37, 52)
en(a, a.pill(CX + 26, R0 + 118, "established", MINT, "#1E4D52", 14, 28), 52, 100, still=1)
en(a, a.text(CX + 18, R0 + 200, "lo invalid no", 15, "#FFB4A3", a.MONO, 600) + a.text(CX + 18, R0 + 222, "encaja con nada", 15, "#FFB4A3", a.MONO, 600), 79, 100)
en(a, a.text(CX + 18, R0 + 200, "la conversación", 15, LIGHT, a.MONO) + a.text(CX + 18, R0 + 222, "queda anotada", 15, LIGHT, a.MONO), 37, 76, still=1)

# ---- estados
SY = 508
a.add(a.box(48, SY, 1104, 92, a.WHITE, a.LINE, rx=16))
EST = [("new", "el primer paquete", a.AMB), ("established", "lo que sigue de una aceptada", a.OK),
       ("related", "nace de otra: error ICMP, datos FTP", a.BLUE), ("invalid", "no encaja con nada", a.BAD)]
for i, (n, s, c) in enumerate(EST):
    x = 70 + i * 272
    a.add(a.text(x, SY + 38, n, 17, c, a.MONO, 600))
    a.add(a.text(x, SY + 66, s, 15, a.TXT, a.SANS))

narr(a, [
    (0, 25, "No coincide con nada de lo permitido y llega al drop final.", a.TXT),
    (25, 50, "Lo nuevo que querés permitir va arriba del drop; la conexión queda en la tabla.", a.TXT),
    (50, 75, "La mayoría del tráfico sale en la regla 1: rápido, sin mirar el resto.", a.OK),
    (75, 100, "El drop de invalid va justo después de los accept de lo establecido.", a.BAD),
], y=638, still_idx=2)

escribir(a, f"{SITE}/33-t1.svg", "Firewall input y estados de conexión",
         "Animación en cuatro tiempos sobre la cadena input, con cinco reglas en orden: accept de established, related y untracked; drop de invalid; accept de ICMP; "
         "accept de la lista admins; drop de lo que no viene de la LAN. 1: un paquete nuevo desde internet al puerto 22 baja regla por regla y lo descarta el drop final. "
         "2: un paquete nuevo desde una dirección de la lista admins coincide en la regla 4, se acepta y la conexión entra a la tabla como new. "
         "3: el paquete siguiente de esa conversación ya es established y sale aceptado en la primera regla. "
         "4: un paquete que no encaja con ninguna conexión es invalid y lo descarta la regla 2.",
         [12, 40, 60, 88], f"{PREV}/_t33")
