#!/usr/bin/env python3
"""Lección 29 (Diagnóstico por terminal), Laboratorio paso 4: qué le pasa al origen del ping.
El ping normal sale con la IP de la WAN; con src-address=192.168.88.1 el masquerade lo traduce y conntrack lo devuelve;
con el masquerade apagado el normal sigue andando y el de la LAN sale con una IP privada que no vuelve."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=26, kicker="MIKROTIK · LABORATORIO · PASO 4", title="Ping normal sí, ping desde la LAN no: masquerade roto")
a.steps([
    "/ping 1.1.1.1 sale con la IP de la WAN: va y vuelve.",
    "Con src-address=192.168.88.1, masquerade lo traduce y vuelve.",
    "Masquerade apagado: el ping normal sigue andando.",
    "El de la LAN sale con 192.168.88.1: la respuesta no vuelve.",
], still=3)

# ---- router por dentro
a.add(a.box(48, 176, 430, 236, a.SLATE, "#C2D4E6", rx=18) + a.text(68, 204, "Router", 18, a.INK, a.HEAD, 600))
a.add(a.box(68, 218, 170, 62, a.WHITE, a.LINE, rx=12) + a.text(84, 244, "LAN", 15, a.GREY, a.MONO) + a.text(84, 268, "192.168.88.1", 15, a.INK, a.MONO, 600))
a.add(a.box(268, 218, 190, 62, a.INK, rx=12) + a.text(284, 244, "ether1 · WAN", 15, LIGHT, a.MONO) + a.text(284, 268, "203.0.113.10", 15, "#FFFFFF", a.MONO, 600))
a.add(a.box(68, 296, 390, 102, a.WHITE, a.LINE, rx=12) + a.text(84, 322, "srcnat", 16, a.INK, a.MONO, 700) + a.text(84, 344, "defconf: masquerade", 15, a.TXT, a.MONO))
en(a, a.pill(442, 304, "habilitada", a.OK, a.OKBG, 14, 26, "end"), 0, 50)
en(a, a.pill(442, 304, "deshabilitada", a.BAD, a.BADBG, 14, 26, "end"), 50, 100, still=1)
a.add(dev(a, 560, 200, 260, 84, "Proveedor", "gw 203.0.113.1", "server"))
a.add(dev(a, 900, 200, 252, 84, "Internet", "1.1.1.1", "globe"))
a.add(linea(458, 249, 560, 242, a.LINE, 4) + linea(820, 242, 900, 242, a.LINE, 4))
a.add(linea(478, 376, 1152, 376, a.LINE, 2, "4 8"))

OUT = [(400, 376), (700, 376), (1030, 376)]
BACK = list(reversed(OUT))
LAN = [(153, 292), (153, 376), (290, 376)]


def ida(lbl, c, t0, t1, hold=0.5):
    viaje(a, lbl, OUT, t0, t1, bg=c, size=14, hold=hold)


# 1
ida("de 203.0.113.10", a.BLUE, 3, 10)
viaje(a, "a 203.0.113.10", BACK, 11, 18, bg=a.OK, size=14, hold=0.5)
# 2
viaje(a, "de 192.168.88.1", LAN, 27, 31, bg=a.BLUE, size=14, hold=0.3)
en(a, a.text(760, 426, "masquerade: 192.168.88.1 pasa a 203.0.113.10", 15, a.AMB, a.MONO, 600, "middle"), 31, 47)
ida("de 203.0.113.10", a.AMB, 32, 38)
viaje(a, "a 203.0.113.10", BACK, 39, 44, bg=a.OK, size=14, hold=0.3)
viaje(a, "a 192.168.88.1", list(reversed(LAN)), 45, 48, bg=a.OK, size=14, hold=1)
# 3
ida("de 203.0.113.10", a.BLUE, 52, 59)
viaje(a, "a 203.0.113.10", BACK, 60, 67, bg=a.OK, size=14, hold=0.5)
# 4
viaje(a, "de 192.168.88.1", LAN, 77, 80, bg=a.BLUE, size=14, hold=0.3)
en(a, a.text(760, 426, "sin masquerade: sale tal cual", 15, a.BAD, a.MONO, 600, "middle"), 80, 100, still=1)
ida("de 192.168.88.1", a.BAD, 81, 88, hold=12)
en(a, marca(a, 1140, 200, ok=False) + a.text(1026, 316, "respuesta a una IP privada:", 15, a.BAD, a.SANS, 700, "middle")
   + a.text(1026, 338, "no tiene cómo volver", 15, a.BAD, a.SANS, 700, "middle"), 88, 100, still=1)
fijo(a, place(pill_c(a, "de 192.168.88.1", "#FFFFFF", a.BAD, 14), 1030, 376))

# ---- terminal
TX, TY, TW = 48, 444, 1104
a.add(a.box(TX, TY, TW, 150, a.INK, rx=16) + a.text(TX + 22, TY + 30, "TERMINAL", 13, LIGHT, a.MONO, 400, extra='letter-spacing="1.8"'))
TL = [
    (0, 25, ["> /ping 1.1.1.1 count=3"], "sent=3 received=3 packet-loss=0%", MINT),
    (25, 50, ["> /ping 1.1.1.1 src-address=192.168.88.1 count=3"], "sent=3 received=3 packet-loss=0%", MINT),
    (50, 75, ['> /ip/firewall/nat/disable [find comment="defconf: masquerade"]', "> /ping 1.1.1.1 count=3"], "sent=3 received=3 packet-loss=0%", MINT),
    (75, 100, ['> /ip/firewall/nat/disable [find comment="defconf: masquerade"]', "> /ping 1.1.1.1 src-address=192.168.88.1 count=3"], "sent=3 received=0 packet-loss=100%", CORAL),
]
for k, (t0, t1, cmds, res, c) in enumerate(TL):
    s = "".join(a.text(TX + 22, TY + 62 + i * 26, ln, 15, "#FFFFFF", a.MONO) for i, ln in enumerate(cmds))
    s += a.text(TX + 22, TY + 62 + len(cmds) * 26 + 6, res, 16, c, a.MONO, 700)
    en(a, s, t0, t1, still=1 if k == 3 else 0)

narr(a, [
    (0, 25, "El router sale con la IP de la interfaz por donde sale: ese ping no necesita NAT.", a.TXT),
    (25, 50, "Con origen de la LAN, la prueba sigue el mismo camino que una PC de la oficina.", a.OK),
    (50, 75, "El router \"tiene internet\": por eso el ping normal no alcanza para probar el NAT.", a.AMB),
    (75, 100, "Así se ve un masquerade roto. Volvé a habilitarlo con nat/enable.", a.BAD),
], y=640, still_idx=3)

escribir(a, "29-l1", "Ping normal sí, ping desde la LAN no",
         "Animación en cuatro tiempos del paso 4. El router por dentro, con la LAN 192.168.88.1, la regla srcnat defconf: masquerade y ether1 con la IP de WAN 203.0.113.10; "
         "afuera, el proveedor con gateway 203.0.113.1 e internet con 1.1.1.1. Abajo, la terminal. "
         "1: /ping 1.1.1.1 sale con origen 203.0.113.10, la IP de la WAN, y la respuesta vuelve. "
         "2: con src-address=192.168.88.1 el paquete pasa por masquerade, que cambia el origen a 203.0.113.10; la respuesta vuelve y conntrack la devuelve a 192.168.88.1. "
         "3: con el masquerade deshabilitado, el ping normal sigue andando porque ya sale con la IP de la WAN. "
         "4: el ping con src-address=192.168.88.1 sale tal cual, con una IP privada, y la respuesta no tiene cómo volver: sent=3 received=0 packet-loss=100%. Así se ve un masquerade roto.",
         [6, 35, 46, 62, 90])
