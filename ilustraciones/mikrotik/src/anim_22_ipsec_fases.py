#!/usr/bin/env python3
"""Lección 22 · IPsec entre marcas. Teoría "Cómo funciona": fase 1 (conocerse), fase 2 (dos SA de un solo sentido)
y policies espejo que deciden qué tráfico se cifra.
"""
from _anim_mikrotik_14_26 import Anim, msg, packet, out

a = Anim(T=26, kicker="MIKROTIK · IPSEC", title="Fase 1, fase 2 y las dos SA de un túnel")
a.steps([
    "Fase 1: acuerdan cifrado, hash y grupo DH, y se autentican. Queda un canal seguro.",
    "Fase 2, por ese canal: acuerdan la proposal y crean dos SA, una por sentido.",
    "Un paquete de 192.168.88.x a 10.10.10.x coincide con la policy: sale cifrado.",
    "La respuesta usa la otra SA. En B la policy es la misma, al revés.",
], still=1)

Y0, Y1 = 178, 640
A0, A1, B0, B1 = 48, 300, 900, 1152
a.add(a.box(A0, Y0, A1 - A0, Y1 - Y0, a.INK, rx=18))
a.add(a.text(A0 + 22, Y0 + 38, "Sitio A · MikroTik", 19, a.WHITE, a.HEAD, 600))
a.add(a.text(A0 + 22, Y0 + 62, "LAN 192.168.88.0/24", 15, "#9FC3E3", a.MONO))
a.add(a.box(B0, Y0, B1 - B0, Y1 - Y0, a.INK, rx=18))
a.add(a.text(B0 + 22, Y0 + 38, "Sitio B · otra marca", 19, a.WHITE, a.HEAD, 600))
a.add(a.text(B0 + 22, Y0 + 62, "LAN 10.10.10.0/24", 15, "#9FC3E3", a.MONO))


def side(x, lines, on, still, col="#C9DDF0"):
    s = ""
    for i, (t, c) in enumerate(lines):
        s += a.text(x, Y0 + 112 + i * 24, t, 15, c or col, a.MONO, 600 if c else 400)
    a.add(a.group(s, a.show(on, 100), still=still))


side(A0 + 22, [("active-peers", "#FFFFFF"), ("1 peer: B", None)], 13, 1)
side(B0 + 22, [("active-peers", "#FFFFFF"), ("1 peer: A", None)], 13, 1)
for x in (A0 + 22, B0 + 22):
    a.add(a.group(a.text(x, Y0 + 182, "installed-sa", 15, "#FFFFFF", a.MONO, 600) + a.text(x, Y0 + 206, "2: una de ida,", 15, "#C9DDF0", a.MONO)
                  + a.text(x, Y0 + 230, "una de vuelta", 15, "#C9DDF0", a.MONO), a.show(42, 100), still=1))


def policy(x, src, dst, on_hl, off_hl):
    base = (a.box(x, Y0 + 290, 216, 112, a.NAVY2, rx=12) + a.text(x + 14, Y0 + 316, "policy", 15, "#FFFFFF", a.MONO, 600)
            + a.text(x + 14, Y0 + 342, f"src {src}", 15, "#C9DDF0", a.MONO) + a.text(x + 14, Y0 + 366, f"dst {dst}", 15, "#C9DDF0", a.MONO)
            + a.text(x + 14, Y0 + 390, "→ cifrar con la SA", 15, "#FFD28A", a.MONO, 600))
    a.add(base)
    a.add(a.group(a.box(x, Y0 + 290, 216, 112, "none", "#FFD28A", rx=12, sw=3), a.show(on_hl, off_hl), still=0))


policy(A0 + 18, "192.168.88.0/24", "10.10.10.0/24", 52, 66)
policy(B0 + 18, "10.10.10.0/24", "192.168.88.0/24", 77, 90)
a.add(a.group(a.text((B0 + B1) / 2, Y0 + 432, "= espejo de A", 15, "#5BE0A5", a.MONO, 600, "middle"), a.show(77, 100), still=1))

L, R = A1 + 6, B0 - 6
# fase 1
a.add(a.text(L + 14, 206, "FASE 1 · UDP 500 (4500 con NAT)", 15, a.GREY, a.MONO, 600))
msg(a, L, R, 250, "cifrado · hash · grupo DH", 2, end=100, still=1, color=a.BLUE)
msg(a, R, L, 300, "autenticación: clave o certificado", 9, end=100, still=1, color=a.BLUE)
a.add(a.group(a.box(L + 10, 326, R - L - 20, 40, a.AMBBG, a.AMB, rx=20, sw=2)
              + a.text((L + R) / 2, 352, "canal seguro para seguir negociando", 15, a.AMB, a.MONO, 600, "middle"), a.show(14, 100), still=1))
# fase 2
a.add(a.text(L + 14, 404, "FASE 2 · por el canal seguro", 15, a.GREY, a.MONO, 600))
msg(a, L, R, 444, "proposal: ESP · cifrado · hash · PFS · lifetime", 27, end=100, still=1, color=a.OK, lsize=15)
SA1, SA2 = 506, 590
a.add(a.group(a.box(L + 10, SA1 - 22, R - L - 20, 44, a.OKBG, a.OK, rx=22, sw=2)
              + a.text(L + 30, SA1 + 6, "SA de ida A → B", 15, a.OK, a.MONO, 600)
              + a.text(R - 30, SA1 + 6, "SPI propio", 15, a.OK, a.MONO, 400, "end"), a.show(36, 100), still=1))
a.add(a.group(a.box(L + 10, SA2 - 22, R - L - 20, 44, a.OKBG, a.OK, rx=22, sw=2)
              + a.text(L + 30, SA2 + 6, "SA de vuelta B → A", 15, a.OK, a.MONO, 600)
              + a.text(R - 30, SA2 + 6, "SPI propio", 15, a.OK, a.MONO, 400, "end"), a.show(40, 100), still=1))
# paquetes
a.add(a.group(a.box(L + 10, SA1 - 22, R - L - 20, 44, "none", a.BLUE, rx=22, sw=4), a.show(55, 70), still=0))
a.add(a.group(a.box(L + 10, SA2 - 22, R - L - 20, 44, "none", a.CYAN, rx=22, sw=4), a.show(79, 94), still=0))
packet(a, "ESP · 192.168.88.x → 10.10.10.x", [(0, L + 180, SA1 + 40), (56, L + 180, SA1 + 40), (68, R - 180, SA1 + 40), (100, R - 180, SA1 + 40)], 55, 70, a.BLUE, size=15, h=30)
packet(a, "ESP · 10.10.10.x → 192.168.88.x", [(0, R - 180, SA2 - 40), (80, R - 180, SA2 - 40), (92, L + 180, SA2 - 40), (100, L + 180, SA2 - 40)], 79, 94, a.CYAN, size=15, h=30)

out(a, 22, 1, "IPsec: fase 1, fase 2 y SA",
    "Animación en cuatro tiempos entre el Sitio A (MikroTik, LAN 192.168.88.0/24) y el Sitio B (otra marca, LAN 10.10.10.0/24). "
    "1: en la fase 1, por UDP 500 (4500 con NAT), acuerdan cifrado, hash y grupo DH y se autentican con clave o certificado; queda un canal seguro y cada lado ve al otro en active-peers. "
    "2: en la fase 2, por ese canal, acuerdan la proposal (ESP, cifrado, hash, PFS y lifetime) y crean dos SA de un solo sentido, cada una con su SPI: una de ida A a B y otra de vuelta; installed-sa muestra dos por router. "
    "3: un paquete de 192.168.88.x a 10.10.10.x coincide con la policy de A (src 192.168.88.0/24, dst 10.10.10.0/24) y sale cifrado en ESP por la SA de ida. "
    "4: la respuesta vuelve por la SA de vuelta; la policy de B es la misma con las redes al revés, un espejo exacto.",
    [10, 45, 62, 88])
