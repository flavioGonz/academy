#!/usr/bin/env python3
"""Lección 20 (Concentrador CHR) · Resumen: los sitios sin IP pública llaman al CHR; el hub aprende de dónde viene cada uno y la notebook llega a cualquiera por su IP de túnel."""
from _anim_r20_31 import *

a, _ = nuevo(27, "MIKROTIK · CONCENTRADOR CHR · EN LA RED", "Los sitios llaman al CHR; vos entrás por el CHR",
             ["Cada sitio, detrás de su CGNAT, abre su túnel hacia 198.51.100.20:13231.",
              "El hub no llama a nadie: anota de qué IP pública viene cada peer.",
              "Tu notebook se conecta al hub como un peer más.",
              "WinBox a 10.10.10.3: el hub lo manda por el peer que tiene ese /32."], still=3)

# CHR
CX, CY, CW, CH = 380, 180, 440, 190
a.add(a.box(CX, CY, CW, CH, a.INK, rx=18))
a.add(a.text(CX + 20, CY + 32, "CHR en un VPS", 19, a.WHITE, a.HEAD, 600))
a.add(a.text(CX + 200, CY + 32, "198.51.100.20 · wg-hub", 14, SKY, a.MONO))
a.add(a.text(CX + 20, CY + 58, "PEER        ALLOWED-ADDRESS  CURRENT-ENDPOINT", 13, SKY, a.MONO))
PEERS = [("sitio-a", "10.10.10.2/32"), ("sitio-b", "10.10.10.3/32"), ("sitio-c", "10.10.10.4/32"), ("notebook", "10.10.10.10/32")]
py = []
for i, (n, al) in enumerate(PEERS):
    y = CY + 84 + i * 26
    py.append(y)
    a.add(a.text(CX + 20, y, n, 14, a.WHITE, a.MONO, 600))
    a.add(a.text(CX + 140, y, al, 14, a.WHITE, a.MONO))
EP = [(2, "203.0.113.61"), (6, "203.0.113.62"), (10, "192.0.2.80"), (52, "198.51.100.77")]
for i, (t, lab) in enumerate(EP):
    flip(a, CX + 292, py[i], [(0, t + 6, "(vacío)", SKY), (t + 6, 100, lab, MINT)], size=14, still_idx=1)

SITES = [("Sitio A", "10.10.10.2", 48), ("Sitio B", "10.10.10.3", 330), ("Sitio C", "10.10.10.4", 612)]
for n, ip, x in SITES:
    dev(a, x, 478, 250, 92, n, f"wg-central {ip}", "detrás de CGNAT", kind="router", ssize=13, tsize=17)
dev(a, 900, 196, 252, 100, "Tu notebook", "peer del hub", "10.10.10.10", ssize=14, tsize=17)

LINES = [[(173, 478), (173, 410), (420, 410), (420, CY + CH)],
         [(455, 478), (455, CY + CH)],
         [(737, 478), (737, CY + CH)]]
for pts in LINES:
    a.add(poly(pts, a.LINE, 3, "6 6"))
for sx in (173, 455, 737):
    a.add(a.pill(sx + 12, 440, "CGNAT", a.GREY, a.SLATE, 12, 24))
NB = [(900, 246), (CX + CW, 246)]
a.add(poly(NB, a.LINE, 3, "6 6"))

def p(label, c):
    return pillc(a, label, bg=c, size=12, h=24)

# 1. los sitios llaman
for i, t in enumerate((2, 6, 10)):
    go(a, "", LINES[i], t, t + 6, hold=1, inner=p("handshake", a.OK))
    en(a, poly(LINES[i], a.OK, 3.5), t + 6, 100, still=1)
# 2. aprende
en(a, ring(a, CX + 282, CY + 66, 150, 84, MINT, rx=10, sw=2.5), 27, 50)
en(a, a.text(CX + CW - 10, CY + CH - 10, "la IP pública de cada CGNAT", 13, GOLD, a.SANS, 600, "end"), 27, 50)
en(a, note(a, 900, 478, 252, 92, "keepalive", ["persistent-keepalive=25s", "en cada sitio: el CGNAT", "no olvida el túnel."], "ok", tsize=15, lsize=14), 28, 100, still=1)
# 3. notebook
go(a, "", [NB[0], NB[1]], 52, 57, hold=1, inner=p("handshake", a.OK))
en(a, poly(NB, a.OK, 3.5), 58, 100, still=1)
# 4. WinBox a 10.10.10.3
go(a, "", [NB[0], NB[1]], 77, 81, hold=0, inner=p("WinBox a 10.10.10.3", a.INK))
en(a, ring(a, CX + 10, py[1] - 18, CW - 20, 26, GOLD, rx=8, sw=2.5), 81, 100, still=1)
go(a, "", [(455, CY + CH), (455, 404)], 83, 87, hold=10, inner=p("WinBox a 10.10.10.3", a.INK))
en(a, ring(a, 327, 475, 256, 98, GOLD, rx=18), 89, 100, still=1)

narr(a, [
    (0, 25, "El CGNAT deja volver lo que el sitio abrió: por eso llama el sitio, no el hub.", a.TXT),
    (25, 50, "El sitio lleva endpoint y keepalive; el hub no tiene endpoint: espera.", a.OK),
    (50, 75, "Un peer por técnico, con su /32, igual que un peer por sitio.", a.TXT),
    (75, 100, "allowed-address es la tabla de ruteo del túnel: cada /32, un sitio.", a.AMB),
], still_idx=3)

escribir(a, "20-r1.svg", "Concentrador CHR con túneles salientes",
         "Animación en cuatro tiempos con un CHR en un VPS (198.51.100.20, interfaz wg-hub) y su tabla de peers con allowed-address y endpoint, tres sitios detrás de CGNAT (sitio-a 10.10.10.2, "
         "sitio-b 10.10.10.3, sitio-c 10.10.10.4) y la notebook del técnico (10.10.10.10). 1: cada sitio abre su túnel saliente con un handshake hacia 198.51.100.20:13231, atravesando su CGNAT. "
         "2: el hub no llama a nadie: anota como current-endpoint la IP pública del CGNAT desde la que le llegó cada peer, y persistent-keepalive=25s en los sitios mantiene abierto cada CGNAT. "
         "3: la notebook se conecta al hub como un peer más. 4: WinBox a 10.10.10.3 va de la notebook al hub, que lo manda por el peer sitio-b porque tiene ese /32 en allowed-address, y llega al sitio B.",
         [12, 36, 62, 84, 94])
