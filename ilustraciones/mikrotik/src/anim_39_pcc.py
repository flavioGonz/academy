#!/usr/bin/env python3
"""Lección 39, teoría "Cómo funciona": PCC reparte por conexión de forma estable y, si un gateway no responde, sigue main."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=28, kicker="MIKROTIK · BALANCEO PCC", title="PCC: cada par cliente servidor, siempre al mismo enlace")
a.steps([
    "Conexión nueva: PCC calcula el resto de dividir por 2. Da 0.",
    "Otro par cliente servidor: da 1. Marca pcc-4g, tabla por-4g.",
    "El mismo par otra vez: mismo resto, mismo enlace.",
    "Si el gateway de por-4g no responde, la búsqueda sigue en main.",
], still=2)

# ---- conexiones
CON = [("PC .10", "198.51.100.20"), ("PC .11", "198.51.100.40"), ("PC .10", "198.51.100.20")]
CY = [184, 268, 352]
for i, ((o, d), y) in enumerate(zip(CON, CY)):
    g = (a.box(48, y, 300, 70, a.WHITE, a.LINE, rx=14) + a.text(66, y + 30, f"{o} → {d}", 16, a.INK, a.MONO, 600)
         + a.text(66, y + 54, "conexión nueva" if i < 2 else "otra conexión, mismo par", 15, a.GREY, a.SANS))
    en(a, g, [1, 26, 51][i], 100, still=1)
en(a, a.box(48, 436, 300, 70, a.WHITE, a.LINE, rx=14) + a.text(66, 466, "PC .11 → 198.51.100.40", 16, a.INK, a.MONO, 600)
      + a.text(66, 490, "nueva, con por-4g caída", 15, a.BAD, a.SANS, 600), 76, 100)

# ---- PCC
PX, PY, PW, PH = 404, 236, 340, 150
a.add(a.box(PX, PY, PW, PH, a.INK, rx=18))
a.add(a.text(PX + 22, PY + 36, "PCC", 20, "#FFFFFF", a.HEAD, 600))
a.add(a.text(PX + 22, PY + 64, "both-addresses:2", 16, LIGHT, a.MONO))
a.add(a.text(PX + 22, PY + 92, "hash(origen, destino) ÷ 2", 15, LIGHT, a.MONO))
for t0, t1, r, st in ((5, 25, "resto 0", 0), (30, 50, "resto 1", 0), (55, 75, "resto 0", 1), (80, 100, "resto 1", 0)):
    en(a, a.text(PX + 22, PY + 128, r, 20, GOLD, a.MONO, 600), t0, t1, still=st)
a.add(a.text(PX + 22, PY + PH + 26, "los restos de este ejemplo son ilustrativos", 15, a.GREY, a.SANS))

# ---- enlaces por resto
RX, RW = 800, 352
LK = [("resto 0 → mark pcc-fija", "tabla por-fija → ether1, la fija", 184), ("resto 1 → mark pcc-4g", "tabla por-4g → ether2, el 4G", 330)]
for t, s, y in LK:
    a.add(a.box(RX, y, RW, 96, a.WHITE, a.LINE, rx=14))
    a.add(a.text(RX + 18, y + 34, t, 16, a.INK, a.MONO, 600))
    a.add(a.text(RX + 18, y + 62, s, 15, a.TXT, a.MONO))
en(a, a.text(RX + 18, 330 + 84, "check-gateway: no responde", 15, a.BAD, a.MONO, 600), 79, 100)
def kh(y, wins, c, still=0):
    ventanas(a, f'<rect x="{RX - 2}" y="{y - 2}" width="{RW + 4}" height="100" rx="15" fill="none" stroke="{c}" stroke-width="3"/>', wins, still)
kh(184, [(10, 25), (60, 75)], a.OK, still=1)
kh(330, [(35, 50)], a.OK)
kh(330, [(79, 100)], a.BAD)

# main
MY = 456
a.add(a.box(404, MY, 748, 120, a.WHITE, a.LINE, rx=14))
a.add(a.text(422, MY + 34, "tabla main", 17, a.INK, a.HEAD, 600))
a.add(a.text(422, MY + 62, "recursivas por la fija, distancia 1", 15, a.TXT, a.MONO))
a.add(a.text(422, MY + 88, "respaldo DHCP del 4G, distancia 2", 15, a.TXT, a.MONO))
ventanas(a, f'<rect x="402" y="{MY - 2}" width="752" height="124" rx="15" fill="none" stroke="{a.OK}" stroke-width="3"/>', [(86, 100)])
en(a, a.text(1134, MY + 34, "sale por la fija", 15, a.OK, a.MONO, 600, "end"), 88, 100)

# ---- paquetes
def viaje(t0, cy, ry, bg):
    paquete(a, "conexión", [(t0, 270, cy + 35), (t0 + 3, 650, PY + 34), (t0 + 6, 650, PY + 34), (t0 + 9, 775, ry + 48)], t0, t0 + 10, bg=bg, size=14)
viaje(1, CY[0], 184, a.CYAN)
viaje(26, CY[1], 330, a.BLUE)
viaje(51, CY[2], 184, a.CYAN)
paquete(a, "conexión", [(76, 270, 471), (79, 650, PY + 34), (82, 650, PY + 34), (85, 775, 378), (87, 775, 378), (90, 775, MY - 4)], 76, 91, bg=a.BLUE, size=14)
en(a, marca(a, 1120, 184 + 30, ok=True, r=13), 60, 75, still=1)

narr(a, [
    (0, 25, "Cada grupo recibe una marca de conexión, y cada marca, una marca de ruteo.", a.TXT),
    (25, 50, "Las conexiones se reparten entre los dos enlaces, no los paquetes.", a.TXT),
    (50, 75, "El mismo par cliente servidor siempre da el mismo resto.", a.OK),
    (75, 100, "El chequeo mira el gateway, no internet. Y lo marcado no usa FastTrack.", a.BAD),
], y=636, still_idx=2)

escribir(a, f"{SITE}/39-t1.svg", "Balanceo PCC por conexión",
         "Animación en cuatro tiempos. PCC con both-addresses:2 toma las direcciones de origen y destino, calcula un hash y se queda con el resto de dividirlo por 2. "
         "1: la conexión de la PC .10 a 198.51.100.20 da resto 0, recibe la marca pcc-fija y va por la tabla por-fija, por ether1. "
         "2: la de la PC .11 a 198.51.100.40 da resto 1, marca pcc-4g, tabla por-4g, por ether2. "
         "3: otra conexión de la PC .10 a 198.51.100.20 da el mismo resto y va otra vez por la fija. "
         "4: el gateway de por-4g no responde a check-gateway; su ruta queda inactiva y la búsqueda sigue en main, donde están las recursivas por la fija y el respaldo del 4G. "
         "Los restos de este ejemplo son ilustrativos.",
         [10, 35, 62, 93], f"{PREV}/_t39")
