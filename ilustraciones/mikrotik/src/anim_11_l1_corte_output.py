#!/usr/bin/env python3
"""Lección 11 (Dos WAN), Laboratorio paso 5: el corte simulado. Las reglas de drop en chain=output descartan
los pings de check-gateway que genera el router; lo de la notebook pasa por forward y sigue por el ISP1 hasta que,
con dos pruebas perdidas, caen las rutas recursivas y lo nuevo sale por el 4G."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 5", title="El corte simulado engaña solo al router")
a.steps([
    "Las reglas van en output: solo tocan lo que genera el router.",
    "check-gateway prueba el testigo: output lo descarta.",
    "La notebook pasa por forward: el ISP1 anda y vuelve.",
    "Segunda prueba perdida: caen las rutas y lo nuevo va al 4G.",
], still=1)

# ---- router por dentro
a.add(a.box(290, 176, 470, 312, a.SLATE, "#C2D4E6", rx=18) + a.text(310, 204, "Router", 18, a.INK, a.HEAD, 600))
a.add(a.box(306, 298, 150, 48, a.INK, rx=12) + a.text(381, 328, "check-gateway", 15, "#FFFFFF", a.MONO, 600, "middle"))
a.add(a.box(476, 200, 266, 146, a.WHITE, a.LINE, rx=14) + a.text(494, 226, "chain=output", 16, a.INK, a.MONO, 700))
a.add(a.box(476, 360, 266, 112, a.WHITE, a.LINE, rx=14) + a.text(494, 386, "chain=forward", 16, a.INK, a.MONO, 700)
      + a.text(494, 408, "sin reglas del corte", 15, a.GREY, a.SANS))
for i, ip in enumerate(("1.1.1.1", "9.9.9.9")):
    a.add(a.text(494, 250 + i * 22, f"icmp a {ip}: drop", 15, a.TXT, a.MONO))
en(a, a.box(476, 200, 266, 146, "none", a.AMB, rx=14, sw=3), 0, 25)
en(a, a.text(494, 296, "lab corte isp1", 15, a.AMB, a.MONO, 600), 0, 100, still=1)

# ---- afuera
a.add(dev(a, 48, 404, 214, 84, "Notebook", "ether3", "laptop"))
a.add(dev(a, 846, 176, 306, 84, "Internet", "testigos · 1.0.0.1", "globe"))
a.add(dev(a, 846, 290, 306, 84, "Módem ISP1", "gw 203.0.113.9", "server"))
a.add(dev(a, 846, 404, 306, 84, "Router 4G", "gw 192.168.8.1", "wifi"))
a.add(linea(262, 446, 476, 446, a.LINE, 4))
a.add(linea(742, 440, 846, 332, a.LINE, 4))
a.add(linea(742, 446, 846, 446, a.LINE, 4))
a.add(linea(1000, 290, 1000, 260, a.LINE, 4))
a.add(f'<path d="M1152 446 H1176 V218 H1152" fill="none" stroke="{a.LINE}" stroke-width="4"/>')
a.add(a.text(800, 368, "ether1", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text(794, 480, "ether2", 15, a.GREY, a.MONO, 400, "middle"))
a.add(linea(742, 322, 846, 322, a.LINE, 3, "6 6"))

# ---- paquetes
NB_ISP1 = [(196, 446), (580, 446), (742, 440), (846, 332), (1000, 300), (1000, 266)]
NB_4G = [(196, 446), (580, 446), (742, 446), (790, 446)]
for t0 in (4, 52):
    viaje(a, "ping 1.0.0.1", NB_ISP1, t0, t0 + 9, bg=a.CYAN, size=14, hold=0.5)
    en(a, marca(a, 1120, 218, ok=True) + a.text(1100, 246, "vuelve", 15, a.OK, a.SANS, 600, "end"), t0 + 9, t0 + 18)
for t0, n in ((27, 1), (76, 2)):
    viaje(a, "ping 1.1.1.1", [(381, 322), (560, 322), (660, 322)], t0, t0 + 5, bg=a.BLUE, size=14, hold=0.1)
    en(a, marca(a, 716, 322, ok=False) + place(pill_c(a, "descartado", "#FFFFFF", a.BAD, 14), 626, 322), t0 + 5, t0 + 14)
fijo(a, marca(a, 716, 322, ok=False) + place(pill_c(a, "descartado", "#FFFFFF", a.BAD, 14), 626, 322))
viaje(a, "lo nuevo", NB_4G, 86, 93, bg=a.AMB, size=14, hold=6)
en(a, a.text(1000, 396, "sale por el 4G", 15, a.AMB, a.SANS, 600, "middle"), 92, 100)

# ---- estado
SY = 512
a.add(a.box(48, SY, 1104, 70, a.WHITE, a.LINE, rx=14))
a.add(a.text(68, SY + 42, "pruebas perdidas", 15, a.GREY, a.MONO))
for t0, t1, s, fg, bg, st in ((0, 33, "0 de 2", a.GREY, GHOST, 0), (33, 81, "1 de 2", a.AMB, a.AMBBG, 1), (81, 100, "2 de 2", a.BAD, a.BADBG, 0)):
    en(a, a.pill(232, SY + 21, s, fg, bg, 15, 30), t0, t1, still=st)
a.add(a.text(388, SY + 42, "ISP1 · distance=1", 16, a.INK, a.MONO, 600))
a.add(a.text(780, SY + 42, "ISP2 · distance=2", 16, a.INK, a.MONO, 600))
for t0, t1, s, fg, bg, st in ((0, 83, "activa", a.OK, a.OKBG, 1), (83, 100, "inactiva", a.BAD, a.BADBG, 0)):
    en(a, a.pill(566, SY + 21, s, fg, bg, 15, 30), t0, t1, still=st)
for t0, t1, s, fg, bg, st in ((0, 83, "en espera", a.GREY, GHOST, 1), (83, 100, "activa", a.AMB, a.AMBBG, 0)):
    en(a, a.pill(958, SY + 21, s, fg, bg, 15, 30), t0, t1, still=st)

narr(a, [
    (0, 25, "Las dos reglas descartan ICMP del router hacia los testigos del ISP1, nada más.", a.TXT),
    (25, 50, "check-gateway nace en el propio router: output lo descarta antes de que salga.", a.BAD),
    (50, 75, "El ISP1 sigue andando: este corte simulado engaña solo al check-gateway.", a.AMB),
    (75, 100, "Mide el cambio de rutas; el corte de verdad se prueba en la ventana del paso 8.", a.AMB),
], y=630, still_idx=1)

escribir(a, "11-l1", "El corte simulado engaña solo al router",
         "Animación en cuatro tiempos del paso 5. En el centro, el router por dentro: check-gateway, la cadena output con las dos reglas "
         "del laboratorio que descartan ICMP hacia 1.1.1.1 y 9.9.9.9, y la cadena forward sin reglas del corte. A la izquierda la notebook en ether3; "
         "a la derecha el módem del ISP1, el router 4G e internet. Abajo, las pruebas perdidas y el estado de las rutas del ISP1 con distance=1 y del ISP2 con distance=2. "
         "1: las reglas van en output, así que solo tocan los paquetes que genera el router; un ping de la notebook a 1.0.0.1 sale por el ISP1 y vuelve. "
         "2: check-gateway le hace ping al testigo y la regla de output lo descarta antes de salir: una prueba perdida. "
         "3: la notebook pasa por forward, no por output, y sus pings siguen saliendo por el ISP1 y volviendo, porque ese enlace anda. "
         "4: la segunda prueba se pierde, las rutas del ISP1 quedan inactivas, entra la del ISP2 y lo nuevo sale por el 4G. "
         "El corte simulado mide el cambio de rutas; el corte de verdad se prueba en la ventana del paso 8.",
         [8, 30, 40, 60, 80, 93])
