#!/usr/bin/env python3
"""Lección 38 (Dos WAN: IP fija + PPPoE), Laboratorio paso 4: lo que hace la regla change-mss con el SYN que sale
por el PPPoE. El MSS 1460 de la PC pasa a 1452 (MTU 1492 menos 40), y el servidor manda segmentos que entran en el PPPoE."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 4", title="El SYN que sale por el PPPoE cambia de MSS")
a.steps([
    "La PC abre una conexión: su SYN anuncia MSS 1460.",
    "Al salir por pppoe-respaldo, change-mss lo baja a 1452.",
    "El servidor manda segmentos de 1452: entran en 1492.",
    "Sin la regla: 1460 + 40 = 1500 y no entra en el PPPoE.",
], still=2)

a.add(dev(a, 48, 176, 224, 84, "PC de la oficina", "192.168.88.30", "laptop"))
a.add(a.box(340, 176, 232, 84, a.INK, a.INK, rx=16) + a.text(360, 210, "Router", 19, "#FFFFFF", a.SANS, 600)
      + a.text(360, 234, "mangle · change-mss", 15, LIGHT, a.MONO))
a.add(dev(a, 900, 176, 252, 84, "Servidor", "198.51.100.20", "server"))
a.add(linea(272, 218, 340, 218, a.LINE, 4))
a.add(linea(572, 218, 900, 218, a.CYAN, 6))
a.add(a.text(736, 250, "pppoe-respaldo · MTU 1492", 15, a.CYAN, a.MONO, 600, "middle"))

viaje(a, "SYN · MSS=1460", [(150, 290), (456, 290)], 3, 11, bg=a.BLUE, size=14, hold=14)
viaje(a, "SYN · MSS=1452", [(660, 186), (820, 186)], 28, 36, bg=a.AMB, size=14, hold=14)
viaje(a, "datos 1452", [(820, 186), (660, 186)], 52, 58, bg=a.OK, size=14, hold=0.5)
viaje(a, "datos 1452", [(456, 290), (160, 290)], 59, 68, bg=a.OK, size=14, hold=7)
fijo(a, place(pill_c(a, "datos 1452", "#FFFFFF", a.OK, 14), 736, 186))
viaje(a, "datos 1460", [(840, 186), (780, 186)], 78, 84, bg=a.BAD, size=14, hold=16)
en(a, marca(a, 690, 218, ok=False) + a.text(690, 292, "no entra en 1492", 15, a.BAD, a.SANS, 700, "middle"), 84, 100)

# ---- la regla
RY = 320
en(a, a.box(48, RY, 1104, 60, a.WHITE, a.LINE, rx=12), 0, 100, still=1)
a.add(a.text(66, RY + 36, "chain=forward out-interface=pppoe-respaldo protocol=tcp tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu", 15, a.INK, a.MONO, 600))
en(a, a.box(48, RY, 1104, 60, "none", a.AMB, rx=12, sw=3), 25, 50, still=0)
en(a, a.box(48, RY, 1104, 60, a.BADBG, a.BAD, rx=12, sw=2) + a.text(600, RY + 37, "sin esta regla", 17, a.BAD, a.SANS, 700, "middle"), 75, 100)

# ---- tamaños (no a escala)
BY = 404
a.add(a.box(48, BY, 1104, 196, a.WHITE, a.LINE, rx=16))
a.add(a.text(68, BY + 32, "Tamaño del paquete IP (no a escala)", 16, a.INK, a.HEAD, 600))
LIM = 900
a.add(linea(LIM, BY + 46, LIM, BY + 184, a.CYAN, 3, "6 6") + a.text(LIM + 10, BY + 62, "MTU 1492", 15, a.CYAN, a.MONO, 600))


def tira(y, datos, total, ok, t0, t1, still=0):
    x0 = 230
    s = a.text(68, y + 26, f"MSS {datos}", 16, a.INK, a.MONO, 700)
    s += a.box(x0, y, 90, 40, "#E5F0FB", a.BLUE, rx=6, sw=1.5) + a.text(x0 + 45, y + 26, "IP 20", 15, a.BLUE, a.MONO, 600, "middle")
    s += a.box(x0 + 94, y, 96, 40, "#E5F0FB", a.BLUE, rx=6, sw=1.5) + a.text(x0 + 142, y + 26, "TCP 20", 15, a.BLUE, a.MONO, 600, "middle")
    end = LIM if ok else LIM + 40
    c, bg = (a.OK, a.OKBG) if ok else (a.BAD, a.BADBG)
    s += a.box(x0 + 194, y, end - (x0 + 194), 40, bg, c, rx=6, sw=1.5) + a.text((x0 + 194 + LIM) / 2, y + 26, f"datos {datos}", 15, c, a.MONO, 600, "middle")
    s += a.text(1140, y + 26, f"= {total}", 17, c, a.MONO, 700, "end")
    if not ok:
        s += a.text(LIM + 20, y + 58, "+8", 15, a.BAD, a.MONO, 700, "middle")
    en(a, s, t0, t1, still=still)


tira(BY + 78, 1452, 1492, True, 52, 100, still=1)
tira(BY + 132, 1460, 1500, False, 76, 100)
en(a, a.text(68, BY + 98, "la PC anunció", 15, a.GREY, a.SANS), 0, 25)
en(a, a.text(230, BY + 104, "1460 = 1500 de Ethernet menos 40 de IP y TCP", 17, a.INK, a.MONO, 600), 4, 25)
en(a, a.text(230, BY + 104, "clamp-to-pmtu: 1492 menos 40 = 1452", 17, a.AMB, a.MONO, 600), 28, 52)

narr(a, [
    (0, 25, "El MSS es el máximo de datos por segmento que cada punta acepta recibir.", a.TXT),
    (25, 50, "La regla solo mira los SYN que salen por pppoe-respaldo y les baja el MSS.", a.AMB),
    (50, 75, "Con 1452 de datos más 40 de encabezados, cada paquete mide 1492: entra entero.", a.OK),
    (75, 100, "Si el aviso ICMP de que no entra no llega, se pierde: páginas que cargan a medias.", a.BAD),
], y=640, still_idx=2)

escribir(a, "38-l1", "El SYN que sale por el PPPoE cambia de MSS",
         "Animación en cuatro tiempos del paso 4. Arriba, una PC de la oficina, el router con la regla de mangle change-mss y un servidor, unidos por pppoe-respaldo con MTU 1492. "
         "En el medio, la regla chain=forward out-interface=pppoe-respaldo protocol=tcp tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu. Abajo, el tamaño del paquete IP, no a escala. "
         "1: la PC abre una conexión y su SYN anuncia MSS 1460, que es 1500 de Ethernet menos 40 de encabezados IP y TCP. "
         "2: al salir por pppoe-respaldo la regla lo baja a 1452, que es 1492 menos 40. "
         "3: el servidor manda segmentos de 1452 bytes de datos; con 20 de IP y 20 de TCP el paquete mide 1492 y entra entero en el PPPoE. "
         "4: sin la regla, el servidor mandaría 1460 de datos, el paquete mediría 1500, 8 bytes más que la MTU del PPPoE, y no entraría: si el aviso ICMP no llega, se pierde y las páginas cargan a medias.",
         [8, 33, 58, 66, 90])
