#!/usr/bin/env python3
"""Lección 32, teoría "Del DNS al firewall": FWD con address-list contra el nombre directo en una address-list, con DNS por turnos."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=26, kicker="MIKROTIK · BLOQUEO POR DNS", title="Del DNS al firewall: la lista anota lo que contestó")
a.steps([
    "La notebook pregunta; la estática FWD deja seguir la consulta.",
    "Arriba contestan 192.0.2.21: va a la notebook y a la lista.",
    "La notebook conecta a esa IP: el forward la corta.",
    "Otra forma: el nombre en una address-list. El router resuelve solo.",
    "Al router le tocó otra IP: la conexión de la notebook pasa.",
], still=2)

TOP, BOT = 174, 360
nodo(a, 48, 200, 220, 80, "Notebook", "192.168.88.254", dark=False)
nodo(a, 932, 200, 220, 80, "example.org", "DNS por turnos", dark=False)
RX, RY, RW, RH = 392, 196, 416, 136
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 22, RY + 34, "MikroTik", 20, "#FFFFFF", a.HEAD, 600))
a.add(a.box(RX + 16, RY + 48, RW - 32, 34, a.NAVY2, rx=9) + a.text(RX + 30, RY + 71, "static FWD example.org", 15, "#FFFFFF", a.MONO, 600))
a.add(a.box(RX + 16, RY + 88, RW - 32, 34, a.NAVY2, rx=9) + a.text(RX + 30, RY + 111, "forward: reject dst-address-list", 15, "#FFB4A3", a.MONO, 600))
for x, y0, y1 in ((158, TOP, 200), (600, TOP, RY), (1042, TOP, 200), (158, 280, BOT), (600, RY + RH, BOT), (1042, 280, BOT)):
    a.add(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{a.LINE}" stroke-width="3"/>')
for y in (TOP, BOT):
    a.add(f'<line x1="158" y1="{y}" x2="1042" y2="{y}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')

Q = "¿example.org?"
paquete(a, Q, [(1, 158, TOP), (7, 600, TOP), (8, 600, TOP), (15, 1042, TOP)], 1, 17)
paquete(a, "192.0.2.21", [(21, 1042, TOP), (27, 600, TOP), (29, 600, TOP), (35, 158, TOP)], 21, 38, bg=a.OK)
paquete(a, "conexión a 192.0.2.21", [(41, 158, BOT), (49, 600, BOT), (59.5, 600, BOT)], 41, 59.5, bg=a.BLUE)
en(a, marca(a, 600 + 150, BOT, ok=False) + a.text(780, BOT + 6, "reject", 16, a.BAD, a.MONO, 600), 49, 60, still=1)
paquete(a, "el router: ¿example.org?", [(61, 600, TOP), (69, 1042, TOP), (71, 1042, TOP)], 61, 72, bg=a.GREY)
paquete(a, "192.0.2.35", [(72, 1042, TOP), (79, 600, TOP)], 72, 80, bg=a.AMB)
paquete(a, "conexión a 192.0.2.21", [(81, 158, BOT), (88, 600, BOT), (95, 1042, BOT), (99.5, 1042, BOT)], 81, 99.5, bg=a.BLUE)
en(a, a.text(600, BOT + 34, "no está en la lista: pasa", 16, a.AMB, a.MONO, 600, "middle"), 88, 100)
fijo(a, f'<g transform="translate(600 {BOT})">' + pill_c(a, "conexión a 192.0.2.21", "#FFFFFF", a.BLUE) + "</g>")

# ---- las dos listas
LY, LH = 408, 182
def panel(x, titulo, sub, tag, tagc):
    a.add(a.box(x, LY, 540, LH, a.WHITE, a.LINE, rx=16))
    a.add(a.text(x + 22, LY + 32, titulo, 18, a.INK, a.HEAD, 600))
    a.add(a.text(x + 22, LY + 56, sub, 15, a.GREY, a.MONO))
    a.add(a.pill(x + 518, LY + 14, tag, tagc, a.SLATE, 14, 26, "end"))
    a.add(f'<rect x="{x + 16}" y="{LY + 72}" width="508" height="44" rx="11" fill="none" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="6 5"/>')

panel(48, "FWD con address-list", "anota lo que el router contestó", "exacto", a.OK)
panel(612, "El nombre en la address-list", "el router lo resuelve por su cuenta", "puede errar", a.AMB)
ra = a.box(64, LY + 72, 508, 44, a.OKBG, rx=11) + a.text(82, LY + 100, "192.0.2.21", 17, a.INK, a.MONO, 600) + a.text(556, LY + 100, "dura el TTL", 15, a.OK, a.MONO, 600, "end")
en(a, ra, 30, 100, still=1)
en(a, f'<rect x="62" y="{LY + 70}" width="512" height="48" rx="12" fill="none" stroke="{a.BAD}" stroke-width="3"/>', 49, 60, still=1)
en(a, a.text(64, LY + 150, "La notebook conecta a la misma IP que está en la lista.", 15, a.TXT, a.SANS), 41, 100, still=1)
rb = a.box(628, LY + 72, 508, 44, a.AMBBG, rx=11) + a.text(646, LY + 100, "example.org → 192.0.2.35", 17, a.INK, a.MONO, 600)
en(a, rb, 79, 100)
en(a, a.text(628, LY + 150, "La notebook tenía 192.0.2.21: la lista no la tiene.", 15, a.AMB, a.SANS, 600), 88, 100)

narr(a, [
    (0, 20, "La estática FWD no contesta ella: manda la consulta hacia arriba.", a.TXT),
    (20, 40, "La lista se llena sola, con las IP que les tocaron a los equipos.", a.OK),
    (40, 60, "La regla de forward corta exactamente esa conexión.", a.BAD),
    (60, 80, "Con CDN o DNS por turnos, el router puede recibir otras direcciones.", a.AMB),
    (80, 100, "Por eso conviene la FWD con address-list y no el nombre directo.", a.TXT),
], y=636, still_idx=2)

escribir(a, f"{SITE}/32-t1.svg", "Del DNS al firewall",
         "Animación en cinco tiempos. 1: la notebook pregunta por example.org y la estática FWD del router deja que la consulta siga hacia arriba. "
         "2: arriba contestan 192.0.2.21; el router se la pasa a la notebook y la anota en la address-list por el tiempo del TTL. "
         "3: la notebook conecta a 192.0.2.21 y la regla de forward con dst-address-list la rechaza. "
         "4: la otra forma es poner el nombre directo en una address-list; el router lo resuelve por su cuenta y, con DNS por turnos, le toca 192.0.2.35. "
         "5: la notebook conecta a 192.0.2.21, que no está en esa lista, y la conexión pasa.",
         [10, 32, 54, 76, 94], f"{PREV}/_t32")
