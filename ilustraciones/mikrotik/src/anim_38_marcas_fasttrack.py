#!/usr/bin/env python3
"""Lección 38, teoría "Cómo funciona": marca de conexión, marca de ruteo, tabla por-fija y el escape por FastTrack."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=30, kicker="MIKROTIK · RUTEO POR POLÍTICAS", title="La respuesta sale por donde entró la conexión")
a.steps([
    "Entra una conexión nueva por ether1: mark-connection entra-fija.",
    "El NVR responde: la conexión marcada le pone mark-routing por-fija.",
    "La tabla por-fija la saca por 203.0.113.9: por la fija.",
    "Si FastTrack toma la conexión, saltea el mangle: main, PPPoE.",
    "FastTrack solo para no-mark: la marcada sigue por la fija.",
], still=2)

# ---- fila de equipos (con el PPPoE como principal, en main)
nodo(a, 48, 178, 220, 80, "NVR", "192.168.88.20:443", dark=False)
nodo(a, 470, 178, 260, 80, "Router", "dst-nat :8443 → NVR")
a.add(a.box(900, 164, 252, 60, a.WHITE, a.LINE, rx=14) + a.text(918, 190, "IP fija · ether1", 17, a.INK, a.HEAD, 600) + a.text(918, 212, "203.0.113.10", 15, a.GREY, a.MONO))
a.add(a.box(900, 234, 252, 60, a.WHITE, a.LINE, rx=14) + a.text(918, 260, "PPPoE · principal", 17, a.INK, a.HEAD, 600) + a.text(918, 282, "la ruta por defecto de main", 15, a.GREY, a.MONO))
for d in ("M268 218 H470", "M730 194 H900", "M730 264 H900"):
    a.add(f'<path d="{d}" stroke="{a.LINE}" stroke-width="3"/>')

paquete(a, "nueva · :8443", [(1, 850, 194), (9, 800, 194), (19, 800, 194)], 1, 19.5, bg=a.CYAN, size=14)
paquete(a, "respuesta", [(21, 320, 218), (30, 396, 218), (39, 396, 218)], 21, 39.5, bg=a.BLUE, size=14)
paquete(a, "respuesta", [(41, 780, 194), (50, 830, 194), (59.5, 830, 194)], 41, 59.5, bg=a.OK, size=14)
en(a, marca(a, 830, 229, ok=True, r=13), 50, 60, still=1)
paquete(a, "respuesta", [(61, 320, 218), (66, 396, 218), (69, 396, 218)], 61, 69.5, bg=a.BLUE, size=14)
paquete(a, "respuesta", [(70, 780, 264), (77, 830, 264), (79.5, 830, 264)], 70, 79.5, bg=a.BAD, size=14)
en(a, a.text(830, 312, "otra IP: no abre", 15, a.BAD, a.MONO, 600, "middle"), 76, 80)
paquete(a, "respuesta", [(81, 320, 218), (86, 396, 218), (89, 396, 218)], 81, 89.5, bg=a.BLUE, size=14)
paquete(a, "respuesta", [(90, 780, 194), (97, 830, 194), (99.5, 830, 194)], 90, 99.5, bg=a.OK, size=14)
fijo(a, f'<g transform="translate(830 194)">' + pill_c(a, "respuesta", "#FFFFFF", a.OK, 14) + "</g>")

# ---- paneles
PY, PH = 330, 270
def panel(x, w, t, dark=False):
    a.add(a.box(x, PY, w, PH, a.INK if dark else a.WHITE, None if dark else a.LINE, rx=16))
    a.add(a.text(x + 20, PY + 32, t, 17, "#FFFFFF" if dark else a.INK, a.HEAD, 600))

# conntrack
panel(48, 300, "Conntrack", dark=True)
a.add(a.text(68, PY + 58, "la marca de conexión queda", 15, LIGHT, a.SANS))
a.add(a.text(68, PY + 78, "guardada para toda la conexión", 15, LIGHT, a.SANS))
ent = (a.box(62, PY + 100, 272, 92, a.NAVY2, rx=12) + a.text(78, PY + 128, "198.51.100.50 →", 15, "#FFFFFF", a.MONO, 600)
       + a.text(78, PY + 150, "203.0.113.10:8443", 15, "#FFFFFF", a.MONO, 600) + a.text(78, PY + 176, "mark: entra-fija", 15, GOLD, a.MONO, 600))
en(a, ent, 8, 100, still=1)
en(a, a.text(68, PY + 226, "FastTrack: la saltea", 15, "#FFB4A3", a.MONO, 600) + a.text(68, PY + 248, "el firewall y el mangle", 15, "#FFB4A3", a.MONO, 600), 61, 80)

# mangle
MX, MW = 366, 452
panel(MX, MW, "/ip/firewall/mangle")
RULES = [("prerouting · in-interface=ether1 · nueva", "→ mark-connection entra-fija"),
         ("prerouting · desde la LAN · entra-fija", "→ mark-routing por-fija")]
for i, (l1, l2) in enumerate(RULES):
    y = PY + 52 + i * 70
    a.add(a.box(MX + 14, y, MW - 28, 62, a.SLATE, rx=10))
    a.add(a.text(MX + 28, y + 25, l1, 15, a.INK, a.MONO))
    a.add(a.text(MX + 28, y + 49, l2, 15, a.BLUE, a.MONO, 600))
yf = PY + 196
a.add(a.box(MX + 14, yf, MW - 28, 62, a.SLATE, rx=10))
a.add(a.text(MX + 28, yf + 25, "filter · fasttrack-connection", 15, a.INK, a.MONO))
en(a, a.text(MX + 28, yf + 49, "established,related", 15, a.TXT, a.MONO, 600), 0, 61, still=1)
en(a, a.text(MX + 28, yf + 49, "established,related", 15, a.BAD, a.MONO, 600), 61, 80)
en(a, a.text(MX + 28, yf + 49, "established,related connection-mark=no-mark", 15, a.OK, a.MONO, 600), 80, 100)
def mh(y, h, wins, c, still=0):
    ventanas(a, f'<rect x="{MX + 12}" y="{y - 2}" width="{MW - 24}" height="{h + 4}" rx="11" fill="none" stroke="{c}" stroke-width="3"/>', wins, still)
mh(PY + 52, 62, [(9, 20)], a.CYAN)
mh(PY + 122, 62, [(30, 60)], a.CYAN, still=1)
mh(yf, 62, [(61, 80)], a.BAD)
mh(yf, 62, [(81, 100)], a.OK)

# tablas
TX, TW = 836, 316
panel(TX, TW, "Tablas de ruteo")
TB = [("main", "0.0.0.0/0 → PPPoE"), ("por-fija", "0.0.0.0/0 → 203.0.113.9")]
for i, (n, r) in enumerate(TB):
    y = PY + 52 + i * 86
    a.add(a.box(TX + 14, y, TW - 28, 74, a.SLATE, rx=10))
    a.add(a.text(TX + 28, y + 28, n, 16, a.INK, a.MONO, 600))
    a.add(a.text(TX + 28, y + 54, r, 15, a.TXT, a.MONO))
def th(i, wins, c, still=0):
    y = PY + 52 + i * 86
    ventanas(a, f'<rect x="{TX + 12}" y="{y - 2}" width="{TW - 24}" height="78" rx="11" fill="none" stroke="{c}" stroke-width="3"/>', wins, still)
th(1, [(40, 60), (89, 100)], a.OK, still=1)
th(0, [(69, 80)], a.BAD)
a.add(a.text(TX + 22, PY + 246, "sin marca de ruteo: main", 15, a.GREY, a.SANS))

narr(a, [
    (0, 20, "La marca de ruteo es por paquete; la de conexión queda en conntrack.", a.TXT),
    (20, 40, "El paquete del NVR no trae nada de ether1: lo reconoce por su conexión.", a.TXT),
    (40, 60, "Responde desde 203.0.113.10, la IP a la que llegó el pedido.", a.OK),
    (60, 80, "FastTrack trabaja solo con la tabla main: la respuesta se escapa.", a.BAD),
    (80, 100, "Limitar FastTrack a no-mark lo evita, a costa de algo de CPU.", a.OK),
], y=640, still_idx=2)

escribir(a, f"{SITE}/38-t1.svg", "Marcas de conexión y FastTrack",
         "Animación en cinco tiempos, con el PPPoE como principal en la tabla main y la IP fija 203.0.113.10 en ether1. "
         "1: entra por ether1 una conexión nueva de la central, 198.51.100.50, al puerto 8443, que va por dst-nat al NVR; mangle le pone mark-connection entra-fija y la marca queda en conntrack. "
         "2: el NVR responde; su paquete llega desde la LAN con la conexión marcada y mangle le pone mark-routing por-fija. "
         "3: la tabla por-fija tiene la ruta por defecto por 203.0.113.9 y la respuesta sale por la IP fija, por donde entró. "
         "4: si la conexión entra en FastTrack, saltea el mangle; sin marca de ruteo usa main y la respuesta sale por el PPPoE, con otra IP, y no abre. "
         "5: con la regla de FastTrack limitada a connection-mark=no-mark, la conexión marcada sigue saliendo por la fija.",
         [12, 34, 55, 76, 95], f"{PREV}/_t38")
