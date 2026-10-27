#!/usr/bin/env python3
"""Lección 30, teoría "Resolver con caché" y "Estados de respuesta". Cinco tiempos (25 s)."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, LIGHT, GOLD, MINT

a = Anim(T=25, kicker="MIKROTIK · DNS", title="El resolver del router: primero la caché")
a.steps([
    "La notebook le pregunta al router por UDP 53.",
    "No está en estáticas ni en caché: pregunta a servers.",
    "Guarda la respuesta por su TTL y contesta.",
    "Otro equipo pregunta lo mismo: sale de la caché.",
    "Un nombre que no existe vuelve como NXDOMAIN.",
], still=3)

# ---- nodos
TOP, BOT = 186, 472
nodo(a, 48, 214, 230, 80, "Notebook", "192.168.88.254", dark=False)
nodo(a, 48, 362, 230, 80, "Celular", "192.168.88.31", dark=False)
nodo(a, 922, 214, 230, 80, "servers", "1.1.1.1 · primero", dark=False)
nodo(a, 922, 362, 230, 80, "dynamic-servers", "del proveedor · después", dark=False, size=18)
for x, y0, y1 in ((163, TOP, 214), (600, TOP, 208), (1037, TOP, 214), (163, 442, BOT), (600, 448, BOT)):
    a.add(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{a.LINE}" stroke-width="3"/>')
a.add(f'<line x1="163" y1="{TOP}" x2="1037" y2="{TOP}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
a.add(f'<line x1="163" y1="{BOT}" x2="600" y2="{BOT}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
a.add(f'<path d="M832 402 H918" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="5 6"/>')

RX, RY, RW, RH = 372, 208, 456, 240
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 24, RY + 36, "MikroTik", 20, "#FFFFFF", a.HEAD, 600))
a.add(a.text(RX + RW - 24, RY + 36, "/ip/dns · :53", 15, LIGHT, a.MONO, 400, "end"))
a.add(a.text(RX + 24, RY + 68, "ESTÁTICAS", 15, LIGHT, a.MONO, 400, extra='letter-spacing="1.5"'))
a.add(a.box(RX + 16, RY + 78, RW - 32, 38, a.NAVY2, rx=10) + a.text(RX + 32, RY + 103, "nvr.lan  A 192.168.88.50", 16, "#FFFFFF", a.MONO, 600))
a.add(a.text(RX + 24, RY + 144, "CACHÉ", 15, LIGHT, a.MONO, 400, extra='letter-spacing="1.5"'))
CR = RY + 154
a.add(f'<rect x="{RX + 16}" y="{CR}" width="{RW - 32}" height="38" rx="10" fill="none" stroke="#2C5680" stroke-width="2" stroke-dasharray="6 5"/>')
en(a, a.text(RX + 32, CR + 25, "vacía para este nombre", 15, LIGHT, a.MONO), 0, 41)
row = (a.box(RX + 16, CR, RW - 32, 38, a.NAVY2, rx=10)
       + a.text(RX + 32, CR + 25, "example.org  A 192.0.2.80", 16, "#FFFFFF", a.MONO, 600)
       + a.text(RX + RW - 30, CR + 25, "TTL 300 s", 15, GOLD, a.MONO, 600, "end"))
en(a, row, 41, 100, still=1)
en(a, f'<rect x="{RX + 14}" y="{CR - 2}" width="{RW - 28}" height="42" rx="11" fill="none" stroke="{MINT}" stroke-width="3"/>', 64, 78, still=1)
en(a, f'<rect x="{RX + 14}" y="{RY + 76}" width="{RW - 28}" height="42" rx="11" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="6 5"/>'
      + f'<rect x="{RX + 14}" y="{CR - 2}" width="{RW - 28}" height="42" rx="11" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="6 5"/>', 7, 19)
SYT = RY + 222
en(a, a.text(RX + 24, SYT, "busca acá primero: no está", 16, GOLD, a.SANS, 600), 7, 20)
en(a, a.text(RX + 24, SYT, "pregunta arriba: primero servers", 16, LIGHT, a.SANS, 600), 20, 40)
en(a, a.text(RX + 24, SYT, "la guarda durante su TTL", 16, MINT, a.SANS, 600), 41, 60)
en(a, a.text(RX + 24, SYT, "la contesta de la caché, sin salir", 16, MINT, a.SANS, 600), 61, 80, still=1)
en(a, a.text(RX + 24, SYT, "el nombre no existe arriba", 16, "#FFB4A3", a.SANS, 600), 81, 100)

# ---- paquetes: la notebook y los servidores por el carril de arriba, el celular por el de abajo
Q = "¿example.org?"
A = "A 192.0.2.80"
paquete(a, Q, [(1, 163, TOP), (6, 600, TOP)], 1, 7.5, bg=a.CYAN)
paquete(a, Q, [(21, 600, TOP), (26, 1037, TOP)], 21, 28, bg=a.CYAN)
paquete(a, A, [(30, 1037, TOP), (35, 600, TOP)], 30, 37, bg=a.OK)
paquete(a, A, [(42, 600, TOP), (48, 163, TOP)], 42, 52, bg=a.OK)
paquete(a, Q, [(61, 163, BOT), (66, 600, BOT)], 61, 67.5, bg=a.CYAN)
paquete(a, A, [(69, 600, BOT), (75, 163, BOT)], 69, 79, bg=a.OK)
Q2 = "¿exampel.org?"
paquete(a, Q2, [(81, 163, TOP), (84, 600, TOP), (85, 600, TOP), (88, 1037, TOP)], 81, 89, bg=a.CYAN)
paquete(a, "NXDOMAIN", [(89, 1037, TOP), (92, 600, TOP), (93, 600, TOP), (97, 163, TOP)], 89, 99.5, bg=a.BAD)
en(a, marca(a, 300, BOT, ok=True), 75, 80, still=1)
fijo(a, f'<g transform="translate(163 {BOT})">' + __import__("_anim_mt2739").pill_c(a, A, "#FFFFFF", a.OK) + "</g>")

# ---- estados
SY = 500
a.add(a.box(48, SY, 1104, 104, a.WHITE, a.LINE, rx=16))
a.add(a.text(70, SY + 30, "Cómo vuelve la respuesta", 18, a.INK, a.HEAD, 600))
EST = [("NOERROR", "el nombre existe", a.OK, a.OKBG, [(41, 80)]),
       ("NXDOMAIN", "no existe o está bloqueado", a.BAD, a.BADBG, [(89, 100)]),
       ("SERVFAIL", "no hubo respuesta de arriba", a.AMB, a.AMBBG, [])]
for i, (n, s, c, bg, w) in enumerate(EST):
    x = 70 + i * 362
    a.add(a.box(x, SY + 46, 344, 44, a.SLATE, rx=12))
    if w:
        ventanas(a, a.box(x, SY + 46, 344, 44, bg, c, rx=12, sw=2.5), w, still=1 if i == 0 else 0)
    a.add(a.text(x + 16, SY + 74, n, 16, c, a.MONO, 600))
    a.add(a.text(x + 120, SY + 74, s, 15, a.TXT, a.SANS))

narr(a, [
    (0, 20, "El DHCP le dio 192.168.88.1 como DNS: todas las consultas llegan al router.", a.TXT),
    (20, 40, "Primero los de servers; los dynamic-servers del proveedor, después.", a.TXT),
    (40, 60, "NOERROR: el router guarda la respuesta durante su TTL y la reenvía.", a.OK),
    (60, 80, "Mientras dure el TTL, nadie de la LAN sale a internet por ese nombre.", a.OK),
    (80, 100, "NXDOMAIN es un nombre mal escrito o bloqueado; SERVFAIL, un problema arriba.", a.BAD),
], y=640, still_idx=3)

escribir(a, f"{SITE}/30-t1.svg", "Resolver con caché del MikroTik",
         "Animación en cinco tiempos. 1: la notebook pregunta por example.org al router por UDP 53; el router busca en sus estáticas y en la caché y no lo encuentra. "
         "2: pregunta a sus servidores de arriba, primero los de servers, 1.1.1.1; los dynamic-servers del proveedor van después. "
         "3: guarda la respuesta, A 192.0.2.80, durante su TTL de 300 segundos y se la contesta a la notebook: NOERROR. "
         "4: el celular pregunta lo mismo y el router contesta desde la caché, sin salir a internet. "
         "5: una consulta por exampel.org, mal escrito, vuelve como NXDOMAIN. Abajo, los tres estados: NOERROR, el nombre existe; NXDOMAIN, no existe; SERVFAIL, no hubo respuesta de arriba.",
         [4, 24, 33, 45, 63, 72, 86, 95], f"{PREV}/_t30")
