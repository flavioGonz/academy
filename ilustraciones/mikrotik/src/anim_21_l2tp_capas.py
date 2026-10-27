#!/usr/bin/env python3
"""Lección 21 · L2TP con IPsec. Teoría "Cómo funciona": al conectar, el orden es de afuera hacia adentro.
1 IPsec negocia (UDP 500, 4500 con NAT).  2 Los datos van en ESP.  3 L2TP por UDP 1701.  4 PPP autentica y da la IP.
"""
from _anim_mikrotik_14_26 import Anim, msg, packet, out

a = Anim(T=24, kicker="MIKROTIK · L2TP/IPSEC", title="Al conectar, de afuera hacia adentro")
a.steps([
    "IPsec negocia por UDP 500 con la clave precompartida. Con NAT, pasa a 4500.",
    "Ya hay canal cifrado: los datos viajan en ESP, o en UDP 4500 con NAT-T.",
    "Dentro del canal cifrado se arma el túnel L2TP, por UDP 1701.",
    "Por último PPP: usuario y contraseña, y una IP del pool para el cliente.",
], still=3)

Y0, Y1 = 186, 616
# extremos
a.add(a.box(48, Y0, 210, Y1 - Y0, a.WHITE, a.LINE, rx=18))
a.add(a.text(153, Y0 + 40, "Notebook", 20, a.INK, a.HEAD, 600, "middle"))
a.add(a.text(153, Y0 + 64, "cliente nativo", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.box(942, Y0, 210, Y1 - Y0, a.INK, rx=18))
a.add(a.text(1047, Y0 + 40, "MikroTik", 20, a.WHITE, a.HEAD, 600, "middle"))
a.add(a.text(1047, Y0 + 64, "203.0.113.10", 15, "#9FC3E3", a.MONO, 400, "middle"))
for i, (t, s_) in enumerate([("use-ipsec=", 0), ("required", 0), ("/ppp/secret", 75), ("service=l2tp", 75), ("pool", 75), ("192.168.89.x", 75)]):
    a.add(a.group(a.text(962, Y0 + 120 + i * 26 + (14 if i >= 2 else 0) + (14 if i >= 4 else 0), t, 15, "#FFD28A" if i % 2 else "#C9DDF0", a.MONO, 600 if i % 2 else 400),
                  a.show(s_, 100), still=1))

L, R = 272, 928
# capas
BANDS = [  # x, y, w, h, color, título, aparece
    (L, Y0, R - L, Y1 - Y0, a.BLUE, "IPsec · cifra y protege", 18),
    (L + 26, 330, R - L - 52, Y1 - 330 - 14, a.CYAN, "L2TP · el túnel · UDP 1701", 50),
    (L + 52, 440, R - L - 104, Y1 - 440 - 26, a.OK, "PPP · identifica y da la IP", 75),
]
for x, y, w, h, col, t, on in BANDS:
    a.add(a.group(a.box(x, y, w, h, col, col, rx=16, sw=2.5, extra='fill-opacity=".07"')
                  + a.text(x + 16, y + 26, t, 16, col, a.MONO, 600), a.show(on, 100), still=1))

# 1: IKE
msg(a, L + 4, R - 4, 252, "IKE · UDP 500", 3, end=25, sub="clave precompartida (ipsec-secret)", still=0)
msg(a, R - 4, L + 4, 306, "acuerdan cómo cifrar", 10, end=25, still=0)
a.add(a.group(a.pill(600, 228, "con NAT en el medio: UDP 4500", a.AMB, a.AMBBG, 15, 30, "middle"), a.show(13, 25), still=0))
# 2: ESP
for t in (28, 36, 44):
    packet(a, "ESP · protocolo 50", [(0, L + 110, 268), (t, L + 110, 268), (t + 5, R - 110, 268), (100, R - 110, 268)], t, t + 5.4, a.BLUE)
a.add(a.group(a.text(600, 312, "o dentro de UDP 4500 si hay NAT (NAT-T)", 15, a.BLUE, a.MONO, 600, "middle"), a.show(25, 100), still=1))
a.add(a.group(a.text(600, 266, "datos en ESP (protocolo 50)", 16, a.BLUE, a.MONO, 600, "middle"), a.show(50, 100), still=1))
# 3: L2TP
msg(a, L + 30, R - 30, 404, "se arma el túnel", 53, still=1, color=a.CYAN)
# 4: PPP
msg(a, L + 56, R - 56, 510, "usuario y contraseña", 78, still=1, color=a.OK)
msg(a, R - 56, L + 56, 566, "IP del pool · DNS del perfil", 86, still=1, color=a.OK)

a.add(a.group(a.pill(153, Y0 + 120, "conectado", a.OK, a.OKBG, 15, 30, "middle")
              + a.text(153, Y0 + 182, "IP 192.168.89.x", 15, a.OK, a.MONO, 600, "middle"), a.show(90, 100), still=1))
a.add(a.group(a.text(153, Y0 + 120, "conectando…", 15, a.GREY, a.MONO, 400, "middle"), a.show(0, 90), still=0))

out(a, 21, 1, "L2TP/IPsec: las tres capas en orden",
    "Animación en cuatro tiempos entre una notebook con el cliente nativo y el MikroTik 203.0.113.10. "
    "1: IPsec negocia por IKE en UDP 500, con la clave precompartida (ipsec-secret), y acuerda cómo cifrar; con un NAT en el medio pasa a UDP 4500. Se forma la capa IPsec. "
    "2: con el canal cifrado, los datos viajan en ESP, el protocolo IP 50, o dentro de UDP 4500 si hay NAT-T. "
    "3: dentro del canal cifrado se arma el túnel L2TP por UDP 1701. "
    "4: por último PPP: el cliente manda usuario y contraseña del /ppp/secret con service=l2tp y recibe una IP del pool 192.168.89.x y los DNS del perfil. Queda conectado.",
    [10, 38, 62, 95])
