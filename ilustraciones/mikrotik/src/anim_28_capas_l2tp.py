#!/usr/bin/env python3
"""Lección 28, teoría "Tres capas" y "El cliente llama": IPsec, después L2TP, después PPP.
Cinco tiempos (25 s). Cuadro fijo: tiempo 5, las tres capas armadas.
"""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, LIGHT

a = Anim(T=25, kicker="MIKROTIK · L2TP/IPSEC", title="El cliente llama: tres capas, en orden")
a.steps([
    "use-ipsec=yes: el cliente crea solo el peer y la policy de IPsec.",
    "IKE negocia las claves por UDP 500 (UDP 4500 si hay NAT, NAT-T).",
    "IPsec arriba: desde acá todo viaja cifrado en ESP.",
    "Adentro, L2TP arma el túnel y la sesión por UDP 1701.",
    "PPP autentica y aparece la interfaz con su IP de túnel.",
], still=4)

Y0, H = 196, 138
nodo(a, 48, Y0, 236, H, "Sucursal", "cliente L2TP", sub2="use-ipsec=yes")
nodo(a, 916, Y0, 236, H, "Central", "servidor L2TP", sub2="203.0.113.10")
CY = Y0 + H / 2
a.add(f'<line x1="284" y1="{CY}" x2="916" y2="{CY}" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="5 7"/>')
a.add(a.text(600, Y0 - 8, "internet", 15, a.GREY, a.MONO, 400, "middle"))

# ---- capas (anillos)
ipsec = (a.box(300, Y0, 600, H, a.OKBG, a.OK, rx=40, sw=2.5)
         + a.text(326, Y0 + 19, "IPsec · ESP cifrado", 15, a.OK, a.MONO, 600))
l2tp = (a.box(320, Y0 + 26, 560, H - 52, "#E4F0FB", a.BLUE, rx=30, sw=2.5)
        + a.text(346, Y0 + 45, "L2TP · UDP 1701", 15, a.BLUE, a.MONO, 600))
ppp = (a.box(340, Y0 + 52, 520, H - 104, a.WHITE, a.CYAN, rx=17, sw=2.5)
       + a.text(600, Y0 + 75, "PPP · 10.255.1.2 ⇄ 10.255.1.1", 16, a.INK, a.MONO, 600, "middle"))
en(a, ipsec, 40, 100, still=1)
en(a, l2tp, 70, 100, still=1)
en(a, ppp, 90, 100, still=1)

# ---- mensajes
L, R = 400, 800
paquete(a, "IKE · UDP 500", [(21, L, CY), (25, R, CY), (26, R, CY), (30, L, CY), (31, L, CY), (35, R, CY), (36, R, CY), (39.4, L, CY)], 21, 39.4, bg=a.AMB)
paquete(a, "L2TP · UDP 1701", [(61, L, CY), (65, R, CY), (66, R, CY), (69.4, L, CY)], 61, 69.4, bg=a.BLUE)
paquete(a, "PPP · usuario", [(81, L, CY), (85, R, CY), (86, R, CY), (89.4, L, CY)], 81, 89.4, bg=a.CYAN)
en(a, a.pill(600, Y0 + H + 14, "con NAT en el medio: UDP 4500", a.AMB, a.AMBBG, 15, 30, "middle"), 22, 40)

# ---- panel del cliente
PY = 392
a.add(a.box(48, PY, 560, 200, a.WHITE, a.LINE, rx=16))
a.add(a.text(70, PY + 32, "En la sucursal aparece", 18, a.INK, a.HEAD, 600))
items = [
    (2, "peer y policy de IPsec hacia connect-to", a.TXT),
    (41, "IPsec establecido: ESP con la central", a.OK),
    (91, "interfaz l2tp-central · 10.255.1.2", a.INK),
    (93, "ruta 10.255.1.1/32 hacia el otro extremo", a.INK),
]
for i, (t, s, c) in enumerate(items):
    y = PY + 70 + i * 34
    en(a, f'<circle cx="78" cy="{y - 5}" r="5" fill="{c}"/>' + a.text(94, y, s, 16, c, a.MONO, 600 if i >= 2 else 400), t, 100, still=1)

# ---- capas, de afuera hacia adentro
QX = 640
a.add(a.box(QX, PY, 512, 200, a.WHITE, a.LINE, rx=16))
a.add(a.text(QX + 22, PY + 32, "De afuera hacia adentro", 18, a.INK, a.HEAD, 600))
capas = [
    ("IPsec", "IKE por UDP 500 o 4500, datos en ESP", a.OK, (20, 60)),
    ("L2TP", "control por UDP 1701: túnel y sesión", a.BLUE, (60, 80)),
    ("PPP", "usuario, contraseña y direcciones", a.CYAN, (80, 100)),
]
for i, (n, s, c, w) in enumerate(capas):
    y = PY + 54 + i * 46
    a.add(a.box(QX + 16, y, 480, 38, a.SLATE, rx=10))
    ventanas(a, a.box(QX + 16, y, 480, 38, a.WHITE, c, rx=10, sw=2.5), [w], still=1 if i == 2 else 0)
    a.add(a.text(QX + 32, y + 25, n, 16, c, a.MONO, 600))
    a.add(a.text(QX + 100, y + 25, s, 15, a.TXT, a.SANS))

narr(a, [
    (0, 20, "La conexión sale de la sucursal: anda aunque esté detrás de CGNAT.", a.TXT),
    (20, 40, "Primero se negocian las claves; todavía no viaja nada de L2TP.", a.AMB),
    (40, 60, "L2TP no cifra: lo protege el ESP de IPsec que lo envuelve.", a.OK),
    (60, 80, "L2TP viaja por adentro de IPsec y lleva las sesiones PPP.", a.BLUE),
    (80, 100, "Al final PPP: usuario, contraseña y una IP de túnel en cada punta.", a.INK),
], y=628, still_idx=4)

escribir(a, f"{SITE}/28-t1.svg", "L2TP/IPsec: tres capas en orden",
        "Animación en cinco tiempos. 1: con use-ipsec=yes, el cliente L2TP de la sucursal crea solo el peer y la policy de IPsec hacia la central, 203.0.113.10. "
        "2: IKE negocia las claves por UDP 500, o UDP 4500 si hay NAT en el medio. 3: con IPsec arriba, todo viaja cifrado en ESP; aparece la capa exterior. "
        "4: adentro, L2TP arma el túnel y la sesión por UDP 1701. 5: adentro de L2TP, PPP autentica con usuario y contraseña; "
        "en la sucursal aparece la interfaz l2tp-central con 10.255.1.2 y una ruta /32 hacia 10.255.1.1, el otro extremo.",
        [10, 27, 50, 67, 90], f"{PREV}/_t28")
