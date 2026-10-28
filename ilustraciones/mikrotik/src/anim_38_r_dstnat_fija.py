#!/usr/bin/env python3
"""Lección 38 (Dos WAN: IP fija + PPPoE), Resumen: quién entra al NVR y por dónde. El dst-nat atado a ether1,
a la IP fija y a la lista de la central deja entrar solo a la central por la fija; con in-interface-list=WAN,
lo que entra por el PPPoE responde por la fija y se pierde."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=28, kicker="MIKROTIK · IP FIJA + PPPOE · EN LA RED", title="Quién entra al NVR, y por qué IP")
a.steps([
    "La central pide 203.0.113.10:8443: dst-nat al NVR, y abre.",
    "Otro de internet prueba el mismo puerto: no está en la lista.",
    "La central prueba por la IP del PPPoE: la regla no coincide.",
    "Así no: con la lista WAN, la respuesta sale por la fija y se pierde.",
], still=0)

# ---- equipos
a.add(dev(a, 48, 252, 236, 92, "NVR", "192.168.88.20:443", "server"))
a.add(a.box(360, 184, 300, 220, a.INK, a.INK, rx=18) + a.text(382, 218, "Router", 19, "#FFFFFF", a.SANS, 600))
a.add(a.text(646, 250, "ether1 · 203.0.113.10", 15, LIGHT, a.MONO, 400, "end"))
a.add(a.text(646, 376, "pppoe-respaldo · 192.0.2.45", 15, LIGHT, a.MONO, 400, "end"))
a.add(dev(a, 880, 180, 272, 92, "Central de monitoreo", "198.51.100.50", "shield", sub2="en la lista monitoreo"))
a.add(dev(a, 880, 312, 272, 92, "Otro en internet", "198.51.100.200", "user"))
W1, W2, BX = 266, 356, 852
a.add(linea(660, W1, BX, W1, a.LINE, 4) + linea(660, W2, BX, W2, a.LINE, 4))
a.add(linea(BX, 200, BX, 404, "#C2D4E6", 6))
a.add(a.text(BX, 428, "internet", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text(756, W1 + 26, "IP fija", 15, a.GREY, a.SANS, 600, "middle"))
a.add(a.text(756, W2 + 26, "PPPoE (dinámica)", 15, a.GREY, a.SANS, 600, "middle"))
a.add(linea(284, 298, 360, 298, a.LINE, 4))
a.add(linea(BX, 226, 880, 226, a.LINE, 3) + linea(BX, 358, 880, 358, a.LINE, 3))

CEN = (880, 226)
OTR = (880, 358)
P1, P2 = (690, W1), (690, W2)
chip = lambda s, c, t0, t1, st=0: en(a, place(pill_c(a, s, "#FFFFFF", c, 14), 510, 300), t0, t1, still=st)

# 1: la central por la fija
viaje(a, "SYN :8443", [CEN, (BX, 226), (BX, W1), P1], 2, 8, bg=a.BLUE, size=14, hold=0.5)
chip("dst-nat → 192.168.88.20:443", a.OK, 8.5, 25, st=1)
viaje(a, "SYN", [(400, 298), (300, 298)], 11, 14, bg=a.BLUE, size=14, hold=0.5)
viaje(a, "SYN-ACK", [(300, 298), (400, 298)], 15, 17, bg=a.OK, size=14, hold=0.3)
viaje(a, "SYN-ACK", [P1, (BX, W1), (BX, 226), CEN], 18, 22, bg=a.OK, size=14, hold=0.5)
en(a, marca(a, 1152, 226, ok=True), 22, 25, still=1)
fijo(a, place(pill_c(a, "SYN-ACK por la fija", "#FFFFFF", a.OK, 14), 760, W1 + 26))
# 2: otro de internet
viaje(a, "SYN :8443", [OTR, (BX, 358), (BX, W1), P1], 27, 33, bg=a.BLUE, size=14, hold=0.5)
chip("no está en monitoreo", a.AMB, 33.5, 41)
chip("input: drop, no es LAN", a.BAD, 41, 50)
en(a, marca(a, 676, W1 + 28, ok=False), 34, 50)
# 3: la central por la IP del PPPoE
viaje(a, "SYN a 192.0.2.45:8443", [CEN, (BX, 226), (BX, W2), P2], 52, 58, bg=a.BLUE, size=14, hold=0.5)
chip("atada a ether1: no coincide", a.AMB, 58.5, 66)
chip("input: drop, no es LAN", a.BAD, 66, 75)
en(a, marca(a, 676, W2 - 28, ok=False), 59, 75)
# 4: así no
viaje(a, "SYN :8443", [CEN, (BX, 226), (BX, W2), P2], 77, 81, bg=a.BLUE, size=14, hold=0.3)
chip("dst-nat → NVR (lista WAN)", a.AMB, 81.5, 100)
viaje(a, "SYN", [(400, 298), (300, 298)], 82, 84, bg=a.BLUE, size=14, hold=0.3)
viaje(a, "SYN-ACK", [(300, 298), (400, 298)], 85, 87, bg=a.OK, size=14, hold=0.3)
viaje(a, "SYN-ACK de 192.0.2.45", [(560, W1), (752, W1)], 88, 92, bg=a.BAD, size=14, hold=8)
en(a, a.box(668, W1 + 14, 176, 50, a.BADBG, rx=8) + a.text(678, W1 + 34, "con la IP del PPPoE", 15, a.BAD, a.SANS, 600) + a.text(678, W1 + 55, "por la fija: se pierde", 15, a.BAD, a.SANS, 600), 92, 100)

# ---- la regla
RY = 456
regla_ok = (a.box(48, RY, 1104, 112, a.WHITE, a.OK, rx=14, sw=2) + a.text(68, RY + 30, "así", 16, a.OK, a.SANS, 700)
            + a.text(68, RY + 60, "chain=dstnat in-interface=ether1 dst-address=203.0.113.10 protocol=tcp dst-port=8443", 15, a.INK, a.MONO, 600)
            + a.text(68, RY + 86, "src-address-list=monitoreo action=dst-nat to-addresses=192.168.88.20 to-ports=443", 15, a.INK, a.MONO, 600))
regla_no = (a.box(48, RY, 1104, 112, a.BADBG, a.BAD, rx=14, sw=2) + a.text(68, RY + 30, "así no", 16, a.BAD, a.SANS, 700)
            + a.text(68, RY + 60, "chain=dstnat in-interface-list=WAN protocol=tcp dst-port=8443", 15, a.INK, a.MONO, 600)
            + a.text(68, RY + 86, "action=dst-nat to-addresses=192.168.88.20 to-ports=443", 15, a.INK, a.MONO, 600))
en(a, regla_ok, 0, 75, still=1)
en(a, regla_no, 75, 100)

narr(a, [
    (0, 25, "Coinciden la interfaz, la IP fija, el puerto y la lista: el NVR contesta por la fija, la ruta principal.", a.OK),
    (25, 50, "Sin dst-nat el pedido es para el router, y el input de fábrica lo descarta.", a.TXT),
    (50, 75, "La IP dinámica del PPPoE no publica nada: es lo que se busca.", a.TXT),
    (75, 100, "Lo que entra por el PPPoE responde por la ruta por defecto, la fija, con otra IP: no abre.", a.BAD),
], y=640, still_idx=0)

escribir(a, "38-r1", "Quién entra al NVR, y por qué IP",
         "Animación en cuatro tiempos. A la izquierda el NVR, 192.168.88.20:443; en el centro el router con la IP fija 203.0.113.10 en ether1, que es la principal, "
         "y pppoe-respaldo con una IP dinámica de ejemplo, 192.0.2.45; a la derecha, por internet, la central de monitoreo 198.51.100.50, que está en la lista monitoreo, y otro equipo 198.51.100.200. "
         "Abajo, la regla de dst-nat. 1: la central manda un SYN a 203.0.113.10:8443; la regla atada a ether1, a la IP fija, al puerto y a la lista coincide, el router lo pasa al NVR y el SYN-ACK vuelve por la fija: abre. "
         "2: el otro equipo prueba el mismo puerto; no está en la lista, no hay dst-nat y el input de fábrica lo descarta porque no viene de la LAN. "
         "3: la central prueba por la IP del PPPoE; la regla está atada a ether1 y no coincide: descartado. "
         "4: así no: con in-interface-list=WAN y sin dst-address, lo que entra por el PPPoE llega al NVR, pero la respuesta sale por la ruta por defecto, la fija, con la IP del PPPoE, y se pierde.",
         [6, 20, 35, 45, 62, 90, 97])
