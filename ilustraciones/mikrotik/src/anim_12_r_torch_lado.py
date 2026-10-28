#!/usr/bin/env python3
"""Lección 12 (Torch y sniffer), Resumen: Torch en el bridge contra Torch en ether1. En la LAN cada flujo tiene su IP;
después del masquerade todo sale con la IP del router. Cuando la cámara se corta, se ve en el bridge."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · TORCH · EN LA RED", title="Torch en el bridge sabe quién es quién; en ether1, no")
a.steps([
    "La cámara sube video y la PC navega: cada uno con su IP.",
    "Torch en bridge: una fila por equipo, con su tasa.",
    "Después del masquerade, en ether1 todo es 203.0.113.10.",
    "La cámara se corta a ratos: en el bridge se ve cuál es.",
], still=3)

a.add(dev(a, 48, 176, 236, 80, "Cámara entrada", "192.168.88.50", "camera"))
a.add(dev(a, 48, 268, 236, 80, "PC", "192.168.88.20", "laptop"))
a.add(a.box(372, 176, 320, 172, a.INK, rx=18) + a.text(392, 206, "Router", 18, "#FFFFFF", a.SANS, 600))
for x, w, t in ((388, 92, "bridge"), (488, 112, "masquerade"), (608, 72, "ether1")):
    a.add(a.box(x, 236, w, 34, a.NAVY2, "#4E7396", rx=8, sw=1.5) + a.text(x + w / 2, 258, t, 14, "#FFFFFF", a.MONO, 600, "middle"))
en(a, a.box(386, 234, 96, 38, "none", a.CYAN, rx=9, sw=3) + a.text(434, 296, "Torch acá", 15, a.CYAN, a.SANS, 700, "middle"), 25, 50)
en(a, a.box(606, 234, 76, 38, "none", GOLD, rx=9, sw=3) + a.text(644, 296, "y acá", 15, GOLD, a.SANS, 700, "middle"), 50, 75)
en(a, a.box(386, 234, 96, 38, "none", a.CYAN, rx=9, sw=3) + a.text(434, 296, "Torch acá", 15, a.CYAN, a.SANS, 700, "middle"), 75, 100, still=1)
a.add(dev(a, 900, 204, 252, 104, "Internet", "198.51.100.30 nube", "globe", sub2="192.0.2.80 web"))
a.add(linea(284, 216, 388, 248, a.LINE, 3) + linea(284, 308, 388, 260, a.LINE, 3) + linea(692, 253, 900, 253, a.LINE, 4))

# paquetes
for t0 in (3, 27, 52):
    viaje(a, "de .50", [(300, 222), (360, 240)], t0, t0 + 3, bg=a.BLUE, size=14, hold=0.3)
    viaje(a, "de .20", [(300, 302), (360, 268)], t0 + 1, t0 + 4, bg=a.CYAN, size=14, hold=0.3)
    viaje(a, "de 203.0.113.10", [(760, 253), (840, 253)], t0 + 5, t0 + 9, bg=a.AMB, size=14, hold=0.5)
for t0 in (78, 86):
    viaje(a, "de .20", [(300, 302), (360, 268)], t0, t0 + 3, bg=a.CYAN, size=14, hold=0.3)
en(a, marca(a, 300, 196, ok=False) + a.text(300, 170, "corte", 15, a.BAD, a.SANS, 700, "middle"), 76, 100, still=1)


def panel_torch(x, titulo, filas, t0, still):
    s = a.box(x, 372, 540, 222, a.INK, rx=16) + a.text(x + 22, 402, titulo, 15, LIGHT, a.MONO)
    s += a.text(x + 22, 432, "origen", 14, LIGHT, a.MONO) + a.text(x + 196, 432, "destino", 14, LIGHT, a.MONO) + a.text(x + 518, 432, "tasa", 14, LIGHT, a.MONO, 400, "end")
    a.add(s)
    for i, (o, d) in enumerate(filas):
        y = 466 + i * 48
        en(a, a.text(x + 22, y, o, 16, "#FFFFFF", a.MONO, 600) + a.text(x + 196, y, d, 16, "#FFFFFF", a.MONO)
           + f'<rect x="{x + 400}" y="{y - 12}" width="118" height="10" rx="5" fill="#2C4A6B"/>', t0, 100, still=still)


panel_torch(48, "/tool/torch bridge", [("192.168.88.50", "198.51.100.30"), ("192.168.88.20", "192.0.2.80")], 25, 1)
panel_torch(612, "/tool/torch ether1", [("203.0.113.10", "198.51.100.30"), ("203.0.113.10", "192.0.2.80")], 50, 1)


def barra(x, y, pts, color, t0, still=0):
    k = a.keyframes(pts, "transform", "scaleX({})")
    a.add(a.group(f'<rect x="{x}" y="{y}" width="118" height="10" rx="5" fill="{color}"/>', k,
                  a.keyframes([(0, 0), (t0, 0), (t0 + 1, 1), (100, 1)]), still=still, origin=f"{x}px {y + 5}px"))


# cámara: pareja hasta 75, después se corta a ratos
cam = [(0, .8), (75, .8), (77, 0), (82, 0), (84, .75), (88, .75), (90, 0), (96, 0), (98, .8), (100, .8)]
pc = [(0, .3), (30, .35), (50, .25), (70, .35), (90, .3), (100, .3)]
barra(448, 454, cam, MINT, 25)
barra(448, 502, pc, MINT, 25)
barra(1012, 454, cam, GOLD, 50)
barra(1012, 502, pc, GOLD, 50)
fijo(a, f'<rect x="448" y="502" width="{118 * .3}" height="10" rx="5" fill="{MINT}"/>'
        f'<rect x="1012" y="502" width="{118 * .3}" height="10" rx="5" fill="{GOLD}"/>')
en(a, a.text(70, 572, "la fila de .50 cae a cero: es la cámara o su cable", 15, CORAL, a.SANS, 700), 77, 100, still=1)
en(a, a.text(634, 572, "una fila cae, pero las dos son 203.0.113.10", 15, GOLD, a.SANS, 700), 77, 100, still=1)
en(a, a.text(634, 572, "el origen ya es la IP del router", 15, GOLD, a.SANS, 700), 52, 77)

narr(a, [
    (0, 25, "Torch no genera tráfico: mira lo que pasa por una interfaz y lo agrupa en flujos.", a.TXT),
    (25, 50, "En el bridge, antes del NAT, la cámara es 192.168.88.50.", a.OK),
    (50, 75, "El masquerade ya reescribió el origen: del lado de afuera no sabés quién es quién.", a.AMB),
    (75, 100, "Antes de tocar el router, revisá la cámara y su cable. Después, apagá Torch.", a.BAD),
], y=640, still_idx=3)

escribir(a, "12-r1", "Torch en el bridge contra Torch en ether1",
         "Animación en cuatro tiempos. A la izquierda la cámara de la entrada, 192.168.88.50, y una PC, 192.168.88.20; en el centro el router con bridge, masquerade y ether1; "
         "a la derecha internet, con la nube de la app en 198.51.100.30 y una web en 192.0.2.80. Abajo, dos ventanas de Torch: en bridge y en ether1. "
         "1: la cámara sube video y la PC navega; los paquetes llegan al bridge cada uno con su IP y salen por ether1 con la del router, 203.0.113.10. "
         "2: Torch en bridge muestra una fila por equipo, 192.168.88.50 y 192.168.88.20, cada una con su tasa. "
         "3: Torch en ether1 muestra las dos filas con origen 203.0.113.10: el masquerade ya reescribió el origen. "
         "4: la cámara se corta a ratos; en el bridge la fila de 192.168.88.50 cae a cero y se sabe que es la cámara o su cable; en ether1 una fila cae, pero las dos son 203.0.113.10.",
         [10, 35, 60, 80, 92])
