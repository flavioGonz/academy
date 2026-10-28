#!/usr/bin/env python3
"""Lección 37 (Dos WAN: PPPoE + DHCP), Laboratorio paso 8: por qué Netwatch necesita la blackhole a 9.9.9.9.
Con la sesión caída, sin blackhole el ping de Netwatch saldría por el 4G y daría up de mentira; con ella se descarta,
y el up-script corre recién cuando la fibra vuelve."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=26, kicker="MIKROTIK · LABORATORIO · PASO 8", title="La blackhole para que el testigo no se vea por el 4G")
a.steps([
    "Normal: Netwatch le hace ping a 9.9.9.9 por pppoe-antel.",
    "Sesión caída y sin blackhole: el ping sale por el 4G y da up.",
    "Con la blackhole en distancia 20, el ping se descarta: down.",
    "Vuelve la fibra: up, y el up-script borra las conexiones UDP.",
], still=2)

a.add(dev(a, 48, 190, 250, 100, "Router", "Netwatch: 9.9.9.9", None, dark=True, sub2="type=simple 10s"))
a.add(dev(a, 560, 172, 250, 84, "Fibra Antel", "pppoe-antel", "server"))
a.add(dev(a, 560, 300, 250, 84, "Router 4G", "ether2 · 192.168.8.1", "wifi"))
a.add(dev(a, 900, 232, 252, 92, "Internet", "testigo 9.9.9.9", "globe"))
a.add(linea(298, 222, 560, 214, a.LINE, 4))
a.add(linea(298, 262, 560, 342, a.LINE, 4))
a.add(linea(810, 214, 900, 266, a.LINE, 4))
a.add(linea(810, 342, 900, 292, a.LINE, 4))
en(a, linea(298, 222, 560, 214, a.BAD, 4, "5 9") + a.text(430, 200, "sesión caída", 15, a.BAD, a.MONO, 600, "middle"), 25, 75, still=1)
en(a, a.text(420, 268, "si no estuviera la blackhole", 15, a.AMB, a.SANS, 600, "middle"), 27, 50)
# la blackhole
bh = (f'<circle cx="400" cy="262" r="20" fill="{a.INK}"/><circle cx="400" cy="262" r="11" fill="#000000"/>'
      + a.text(400, 302, "blackhole", 15, a.INK, a.MONO, 700, "middle"))
en(a, bh, 50, 75, still=1)

PP = [(330, 222), (470, 218), (685, 214), (860, 240)]
P4 = [(330, 262), (470, 300), (685, 342), (860, 318)]
viaje(a, "ping 9.9.9.9", PP, 3, 11, bg=a.BLUE, size=14, hold=0.5)
viaje(a, "respuesta", list(reversed(PP)), 12, 20, bg=a.OK, size=14, hold=0.5)
viaje(a, "ping 9.9.9.9", P4, 28, 36, bg=a.BLUE, size=14, hold=0.5)
viaje(a, "respuesta", list(reversed(P4)), 37, 45, bg=a.AMB, size=14, hold=0.5)
viaje(a, "ping 9.9.9.9", [(330, 262), (392, 262)], 53, 57, bg=a.BLUE, size=14, hold=0.1)
en(a, place(pill_c(a, "descartado", "#FFFFFF", a.BAD, 14), 480, 262), 57.5, 70)
fijo(a, place(pill_c(a, "ping descartado", "#FFFFFF", a.BAD, 14), 506, 262))
viaje(a, "ping 9.9.9.9", PP, 77, 84, bg=a.BLUE, size=14, hold=0.5)
viaje(a, "respuesta", list(reversed(PP)), 85, 92, bg=a.OK, size=14, hold=0.5)

# ---- tabla
TX, TY, TW = 48, 404, 724
a.add(a.box(TX, TY, TW, 196, a.WHITE, a.LINE, rx=16) + a.text(TX + 22, TY + 32, "/ip/route · lo que mira el ping de Netwatch", 16, a.INK, a.HEAD, 600))
ROWS = [("9.9.9.9/32", "pppoe-antel", "1"), ("9.9.9.9/32", "blackhole", "20"), ("0.0.0.0/0", "192.168.8.1 (4G)", "2")]
RY = [TY + 48, TY + 96, TY + 144]
for (d, g, k), y in zip(ROWS, RY):
    a.add(a.box(TX + 12, y, TW - 24, 42, a.SLATE, rx=10) + a.text(TX + 24, y + 28, d, 16, a.INK, a.MONO, 600)
          + a.text(TX + 190, y + 28, g, 16, a.TXT, a.MONO) + a.text(TX + 440, y + 28, "dist " + k, 16, a.INK, a.MONO, 600))
E = TX + TW - 22
ACT, INA, ESP = ("activa", a.OK, a.OKBG), ("inactiva", a.BAD, a.BADBG), ("espera", a.GREY, GHOST)
SCH = [(0, 25, [ACT, ESP, ESP]), (25, 50, [INA, ("no existe", a.GREY, GHOST), ACT]), (50, 75, [INA, ACT, ACT]), (75, 100, [ACT, ESP, ESP])]
for k, (t0, t1, sts) in enumerate(SCH):
    for i, (s, fg, bg) in enumerate(sts):
        en(a, a.pill(E, RY[i] + 7, s, fg, bg, 14, 28, "end"), t0, t1, still=1 if k == 2 else 0)
en(a, a.box(TX + 12, RY[2], TW - 24, 42, "none", a.AMB, rx=10, sw=2.5), 25, 50)
en(a, a.box(TX + 12, RY[1], TW - 24, 42, "none", a.INK, rx=10, sw=2.5), 50, 75, still=1)

# ---- Netwatch
NX, NW = 800, 352
a.add(a.box(NX, TY, NW, 196, a.INK, rx=16) + a.text(NX + 22, TY + 32, "Netwatch · 9.9.9.9", 16, "#FFFFFF", a.HEAD, 600))
for t0, t1, s, fg, bg, st in ((0, 25, "up", a.OK, a.OKBG, 0), (25, 50, "up (de mentira)", a.AMB, a.AMBBG, 0),
                              (50, 86, "down", a.BAD, a.BADBG, 1), (86, 100, "up", a.OK, a.OKBG, 0)):
    en(a, a.pill(NX + 22, TY + 52, s, fg, bg, 16, 34), t0, t1, still=st)
en(a, a.text(NX + 22, TY + 120, "el up-script borraría las UDP", 15, GOLD, a.SANS, 600)
   + a.text(NX + 22, TY + 142, "con la fibra todavía caída", 15, GOLD, a.SANS, 600), 30, 50)
en(a, a.text(NX + 22, TY + 120, "no corre nada: la fibra", 15, LIGHT, a.SANS, 600)
   + a.text(NX + 22, TY + 142, "sigue caída", 15, LIGHT, a.SANS, 600), 55, 86, still=1)
en(a, a.text(NX + 22, TY + 120, "corre el up-script:", 15, MINT, a.SANS, 600)
   + a.text(NX + 22, TY + 146, "connection/remove", 15, "#FFFFFF", a.MONO, 600)
   + a.text(NX + 22, TY + 168, "[find protocol=udp]", 15, "#FFFFFF", a.MONO, 600), 86, 100)

narr(a, [
    (0, 25, "El ping de Netwatch es del router y sigue la tabla main, como cualquier paquete.", a.TXT),
    (25, 50, "Sin la /32 por pppoe-antel, 9.9.9.9 se alcanzaría por la ruta por defecto del 4G.", a.AMB),
    (50, 75, "La blackhole entra solo cuando la /32 por pppoe-antel no está: el testigo no se ve por otro lado.", a.TXT),
    (75, 100, "Con la fibra de vuelta, el up-script limpia lo UDP que quedó armado por el 4G.", a.OK),
], y=640, still_idx=2)

escribir(a, "37-l2", "La blackhole del testigo de Netwatch",
         "Animación en cuatro tiempos del paso 8. El router corre una sonda Netwatch simple a 9.9.9.9 cada 10 segundos; tiene la fibra por pppoe-antel y el router 4G por ether2. "
         "Abajo, las rutas que mira el ping: 9.9.9.9/32 por pppoe-antel en distancia 1, 9.9.9.9/32 blackhole en distancia 20 y la ruta por defecto del 4G por 192.168.8.1 en distancia 2, "
         "y el estado de Netwatch. 1: normal, el ping va por pppoe-antel, vuelve y Netwatch está up. "
         "2: se cae la sesión y, si no estuviera la blackhole, el ping a 9.9.9.9 saldría por la ruta por defecto del 4G, volvería, y Netwatch daría up de mentira: el up-script borraría las conexiones UDP con la fibra caída. "
         "3: con la blackhole en distancia 20, que queda activa cuando la /32 por pppoe-antel no está, el ping se descarta y Netwatch queda down sin correr nada. "
         "4: vuelve la fibra, la /32 por pppoe-antel vuelve a activa, el ping contesta, Netwatch pasa a up y el up-script borra las conexiones UDP que quedaron armadas por el 4G.",
         [8, 33, 42, 60, 80, 95])
