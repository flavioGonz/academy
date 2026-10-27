"""Teoría lección 2: ARP llega antes que el ping; por eso la MAC aparece aunque el ICMP esté bloqueado."""
from _awin import *

a = new(20, "ARP primero, ping después")
a.steps(["Tu equipo pregunta a todos: ¿quién tiene la .20?",
         "La cámara contesta con su MAC: queda en la tabla.",
         "Recién ahí sale el ping, y la cámara lo descarta.",
         "Ping fallido y MAC en la tabla: la cámara está viva."], still=3)
Y = 400
a.add(line(a, f"M168 {Y}H1040", a.BLUE, 4))
for x in (168, 700, 1040):
    a.add(line(a, f"M{x} 300V{Y}", a.BLUE, 4) + dot(a, x, Y, 6, a.BLUE))
a.add(card(a, 48, 200, 240, 100, "Tu notebook", "192.168.88.10", dark=True))
a.add(card(a, 580, 200, 240, 100, "Gateway", "192.168.88.1"))
a.add(card(a, 920, 200, 232, 100, "Cámara", "192.168.88.20"))
a.add(a.text(600, Y + 30, "misma subred · 192.168.88.0/24", 15, a.GREY, a.MONO, 500, "middle"))

# 1: broadcast a todos
for (x, t0) in ((700, 2), (1040, 2)):
    mv = a.move([(0, 168, 300), (t0, 168, 300), (t0 + 5, 168, Y), (t0 + 15, x, Y), (t0 + 20, x, 300), (100, x, 300)])
    op = a.keyframes([(0, 0), (t0, 0), (t0 + 0.5, 1), (t0 + 20, 1), (t0 + 21, 0), (100, 0)])
    a.add(a.group('<circle cx="0" cy="0" r="11" fill="#FFB020" stroke="#fff" stroke-width="2"/>', mv, op, still=0))
at(a, chip(a, 350, 330, "ARP · ¿quién tiene 192.168.88.20?", "amb"), 2, 25, 0)
# 2: respuesta de la cámara
mv = a.move([(0, 1040, 300), (27, 1040, 300), (30, 1040, Y), (42, 168, Y), (46, 168, 300), (100, 168, 300)])
op = a.keyframes([(0, 0), (27, 0), (27.5, 1), (46, 1), (47, 0), (100, 0)])
a.add(a.group(f'<circle cx="0" cy="0" r="11" fill="{a.OK}" stroke="#fff" stroke-width="2"/>', mv, op, still=0))
at(a, chip(a, 520, 330, "soy yo · 00-11-22-33-44-20", "ok"), 27, 50, 0)
# tabla ARP
a.add(a.box(48, 470, 560, 120, "#03213C", None, rx=14))
a.add(a.text(68, 498, "arp -a", 15, "#9FC3E3", a.MONO, 500))
a.add(a.text(68, 530, "192.168.88.1    00-11-22-33-44-01".replace(" ", "\u00a0"), 17, "#D9E9F8", a.MONO, 500))
at(a, a.text(68, 562, "192.168.88.20   00-11-22-33-44-20".replace(" ", "\u00a0"), 17, "#9FE3F7", a.MONO, 600), 44, 100, 1)
at(a, a.box(58, 541, 540, 30, "none", a.CYAN, rx=6, sw=2), 76, 100, 1)
# 3: ping bloqueado
mv = a.move([(0, 168, 300), (52, 168, 300), (55, 168, Y), (66, 1000, Y), (100, 1000, Y)])
op = a.keyframes([(0, 0), (52, 0), (52.5, 1), (67, 1), (68, 0), (100, 0)])
a.add(a.group(f'<circle cx="0" cy="0" r="11" fill="{a.BLUE}" stroke="#fff" stroke-width="2"/>', mv, op, still=0))
at(a, chip(a, 540, 330, "ping · ICMP", "info"), 52, 75, 0)
at(a, a.box(980, 360, 40, 80, a.BAD, None, rx=8) + a.text(1000, 408, "×", 30, "#fff", a.SANS, 700, "middle"), 64, 100, 1)
at(a, chip(a, 1152, 456, "firewall: ICMP bloqueado", "bad", anchor="end"), 66, 100, 1)
caption(a, 625, [(0, 25, "ARP pregunta por IP y pide la MAC: es lo primero que pasa al hablar con alguien de tu subred.", None),
                 (25, 50, "La respuesta llega aunque la cámara tenga el ping bloqueado: ARP no es ICMP.", a.OK),
                 (50, 75, "El ping sí es ICMP. Si el firewall lo descarta, ves \"tiempo de espera agotado\".", a.BAD),
                 (75, 100, "Con la MAC en la tabla, no mandes a nadie al sitio todavía: el equipo responde.", a.OK)], still=3)
write(a, "2-t1.svg", "ARP primero, ping después",
      "Animación en cuatro tiempos con una notebook, un gateway y una cámara en la misma subred 192.168.88.0/24. 1: la notebook manda una pregunta ARP a todos: quién tiene 192.168.88.20. "
      "2: la cámara contesta con su MAC, 00-11-22-33-44-20, y aparece en la tabla de arp -a. 3: recién después sale el ping, que es ICMP, y el firewall de la cámara lo descarta. "
      "4: queda el ping fallido y la MAC resaltada en la tabla: la cámara está viva. El cuadro fijo muestra la tabla con la MAC y el ping bloqueado.")
