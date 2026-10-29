#!/usr/bin/env python3
"""Lección 3 · Resumen, "Cómo se ve en la red": adopción en capa 3 de un AP de un sitio remoto con el controlador
detrás de NAT. El inform va a http://unifi.example.com:8080/inform; sin Override el controlador anuncia su IP interna
y el AP no llega; con Inform Host + Override anuncia el nombre alcanzable. Inform por TCP 8080 y STUN por UDP 3478.
Fuentes: theory_md y lab.md de la lección; help.ui.com, "Required Ports Reference" (TCP 8080: comunicación de
dispositivos; UDP 3478: STUN para adopción y comunicación de dispositivos)."""
from _anim_red_unifi import *  # noqa

a = new(26, "Inform remoto", "Controlador detrás de NAT: qué dirección recibe el AP", [
    "El AP del sitio remoto tiene la URL: http://unifi.example.com:8080/inform.",
    "El inform sale por TCP 8080, cruza el NAT del sitio y el reenvío de la oficina.",
    "Sin Override, el controlador le anuncia su IP interna: el AP ya no llega.",
    "Con Inform Host y Override anuncia el nombre: inform por 8080 y STUN por 3478.",
], still=3)

Y, H = 186, 100
YL = Y + 52
a.add(dev(a, 48, Y, 196, H, "AP", "sitio remoto", ap=True, sub2="192.168.88.20"))
a.add(dev(a, 282, Y, 206, H, "Router sitio", "NAT", icon="server", sub2="198.51.100.7"))
a.add(a.box(522, Y + 20, 132, 64, "#EAF2FA", a.LINE, rx=30, sw=2, extra='stroke-dasharray="7 6"'))
a.add(a.text(588, Y + 58, "internet", 15, a.GREY, a.MONO, 400, "middle"))
a.add(dev(a, 688, Y, 222, H, "Router oficina", "8080 y 3478 → VM", icon="shield", sub2="203.0.113.10"))
a.add(dev(a, 944, Y, 208, H, "Controlador", "VM con NAT", icon="server", dark=True, sub2="10.10.10.5"))
for x1, x2 in ((244, 282), (488, 522), (654, 688), (910, 944)):
    a.add(wire(x1, YL, x2, YL, a.BLUE, 4))

# tarjetas de abajo
CY = 372
L1, L2 = 314, 346
a.add(wire(146, L1, 1048, L1, a.LINE, 2, "3 7"))
a.add(wire(146, L2, 1048, L2, a.LINE, 2, "3 7"))
for cx in (146, 385, 799, 1048):
    a.add(wire(cx, Y + H, cx, L2, a.LINE, 2, "3 7"))
a.add(a.box(48, CY, 520, 118, a.WHITE, a.LINE, rx=14))
a.add(a.text(68, CY + 34, "Lo que el AP tiene como inform", 17, a.INK, a.SANS, 600))
vis(a, a.text(68, CY + 70, "http://unifi.example.com:8080/inform", 16, a.INK, a.MONO, 600), 0, 1)
vis(a, a.text(68, CY + 70, "http://10.10.10.5:8080/inform", 16, a.BAD, a.MONO, 600), 2)
vis(a, a.text(68, CY + 70, "http://unifi.example.com:8080/inform", 16, a.OK, a.MONO, 600), 3)
vis(a, a.text(68, CY + 100, "por option 43, DNS o set-inform", 15, a.TXT, a.SANS), 0, 1)
vis(a, a.text(68, CY + 100, "10.10.10.5 es privada: no se llega desde el sitio", 15, a.BAD, a.SANS, 600), 2)
vis(a, a.text(68, CY + 100, "un nombre que resuelve a 203.0.113.10", 15, a.OK, a.SANS, 600), 3)

a.add(a.box(608, CY, 544, 118, a.WHITE, a.LINE, rx=14))
a.add(a.text(628, CY + 34, "Settings > System > Advanced", 17, a.INK, a.SANS, 600))
vis(a, a.text(628, CY + 70, "Inform Host:  sin Override", 16, a.GREY, a.MONO, 600), 0, 2)
vis(a, a.text(628, CY + 70, "Inform Host:  unifi.example.com", 16, a.INK, a.MONO, 600), 3)
vis(a, a.text(628, CY + 100, "anuncia la IP que conoce: la interna", 15, a.TXT, a.SANS), 0, 2)
vis(a, check(a, 640, CY + 95, 11) + a.text(660, CY + 100, "Override: anuncia el nombre alcanzable", 15, a.OK, a.SANS, 600), 3)

# 1 · DNS del nombre
s0, s1 = ph(a, 0)
during(a, pill(a, 146, Y - 4, "unifi.example.com → 203.0.113.10", "info", anchor="start"), s0 + 3, s1)

# 2 · inform hasta el controlador
s0, s1 = ph(a, 1)
go(a, [(146, L1), (1048, L1)], s0 + 2, s0 + 14, "TCP 8080", a.CYAN, hold=s0 + 15)
during(a, pill(a, 385, Y - 14, "src → 198.51.100.7", "grey", anchor="middle"), s0 + 5, s1)
during(a, pill(a, 799, Y - 14, "→ 10.10.10.5:8080", "grey", anchor="middle"), s0 + 10, s1)
go(a, [(1048, L2), (146, L2)], s0 + 16, s0 + 23, "adoptado", a.OK, hold=s0 + 24)
during(a, nbox(a, 48, 506, 1104, 82, "Firewall de la oficina", ["El 8080 se abre solo hacia las IP de tus sitios o por VPN, nunca a todo internet."], "amb"),
       s0 + 6, 100, still=1)

# 3 · sin Override
s0, s1 = ph(a, 2)
go(a, [(1048, L2), (146, L2)], s0 + 1, s0 + 8, "inform → 10.10.10.5", a.BAD, hold=s0 + 9)
go(a, [(146, L1), (470, L1)], s0 + 11, s0 + 16, "TCP 8080", a.CYAN, hold=s0 + 17)
during(a, xmark(a, 540, L1, 16), s0 + 16, s1)
during(a, pill(a, 146, Y - 4, "offline / adoptando sin fin", "bad"), s0 + 17, s1)

# 4 · con Override
s0, s1 = ph(a, 3)
go(a, [(1048, L2), (146, L2)], s0 + 1, s0 + 7, "inform → unifi.example.com", a.OK, hold=s0 + 8)
go(a, [(146, L1), (1048, L1)], s0 + 9, s0 + 17, "TCP 8080", a.CYAN, hold=s1 - 0.5, still=1)
go(a, [(146, L2), (1048, L2)], s0 + 10, s0 + 18, "UDP 3478 · STUN", a.BLUE, hold=s1 - 0.5, still=1)
during(a, pill(a, 146, Y - 4, "Connected", "ok"), s0 + 18, 100, still=1)

status(a, 640, [
    (0, 25, "En capa 3 no hay anuncio local: el equipo necesita la URL de inform.", a.INK, 0),
    (25, 50, "El inform es HTTP al 8080: tiene que poder llegar desde el sitio.", a.INK, 0),
    (50, 75, "Detrás de NAT o en contenedor, el controlador solo conoce su IP interna.", a.BAD, 0),
    (75, 100, "Inform Host con Override: cada equipo recibe una dirección a la que llega.", a.OK, 1),
])

write(a, 3, "r1", "Inform remoto con el controlador detrás de NAT",
      "Animación en cuatro tiempos con la cadena AP del sitio remoto (192.168.88.20), router del sitio con NAT (198.51.100.7), internet, "
      "router de la oficina (203.0.113.10) que reenvía 8080 y 3478, y el controlador en una VM con NAT (10.10.10.5). "
      "1: el AP tiene como inform http://unifi.example.com:8080/inform, por option 43, DNS o set-inform; el nombre resuelve a 203.0.113.10. "
      "2: el inform sale por TCP 8080, el NAT del sitio cambia el origen a 198.51.100.7 y la oficina lo reenvía a 10.10.10.5:8080; el AP se adopta. "
      "El 8080 se abre solo hacia las IP de los sitios o por VPN. "
      "3: sin Override, el controlador le anuncia su IP interna, http://10.10.10.5:8080/inform; esa IP es privada, el inform muere en el router del sitio y el AP queda offline. "
      "4: con Settings > System > Advanced, Inform Host unifi.example.com y Override marcado, el AP recibe el nombre alcanzable y queda Connected: "
      "inform por TCP 8080 y STUN por UDP 3478.",
      [12, 37, 64, 92])
