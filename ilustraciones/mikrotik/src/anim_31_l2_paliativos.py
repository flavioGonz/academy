#!/usr/bin/env python3
"""Lección 31 (DNS transparente) · Laboratorio paso 6: dominio canario de Firefox, DoT cortado en el 853 y el DoH a mano que pasa igual."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · DNS TRANSPARENTE · PASO 6", "Dos paliativos y lo que no cubren",
             ["Antes de prender DoH por su cuenta, Firefox pregunta por el dominio canario.",
              "La estática contesta NXDOMAIN: Firefox no lo prende y sigue por el 53.",
              "Un equipo con DNS sobre TLS prueba el 853: reject. Vuelve al 53.",
              "DoH configurado a mano va por el 443: Torch lo ve, la regla no."], still=1)

XN, XR, XI = 180, 590, 1010
en(a, dev(a, XN - 132, 178, 264, 70, "Notebook con Firefox", "192.168.88.254", tsize=17, ssize=14, add=False), 0, 50, still=1)
en(a, dev(a, XN - 132, 178, 264, 70, "Celular", "DNS privado (DoT)", tsize=17, ssize=14, add=False), 50, 75)
en(a, dev(a, XN - 132, 178, 264, 70, "Equipo con DoH a mano", "192.168.88.254", tsize=17, ssize=14, add=False), 75, 100)
head(a, XR, 178, "Router", "resolver + firewall", w=270, kind="router")
head(a, XI, 178, "Internet", "DoT :853 · DoH :443", w=270, kind="isp")
for x in (XN, XR, XI):
    lifeline(a, x, 248, 450)

# 1 y 2: canario
msg(a, XN, XR, 290, "A? use-application-dns.net", 3, 50, still=1)
en(a, a.box(XR + 18, 306, 300, 50, a.WHITE, a.OK, rx=12, sw=2) + a.text(XR + 34, 328, "estática type=NXDOMAIN", 14, a.OK, a.MONO, 600)
   + a.text(XR + 34, 347, "use-application-dns.net", 14, a.TXT, a.MONO), 10, 50, still=1)
msg(a, XR, XN, 380, "NXDOMAIN", 28, 50, a.OK, still=1)
en(a, a.text(XN + 14, 420, "Firefox: no activa DoH solo", 15, a.OK, a.SANS, 600), 32, 50, still=1)
en(a, a.text(XN + 14, 442, "sigue con el DNS del sistema, por el 53", 15, a.TXT, a.SANS), 34, 50, still=1)

# 3. DoT
msg(a, XN, XI, 290, "TCP 853 · DNS sobre TLS", 53, 75, lost=True, frac=0.47)
en(a, a.box(XR - 4, 304, 330, 50, a.WHITE, a.AMB, rx=12, sw=2) + a.text(XR + 12, 326, "forward dst-port=853", 14, a.AMB, a.MONO, 600)
   + a.text(XR + 12, 345, "reject icmp-admin-prohibited", 14, a.TXT, a.MONO), 56, 75)
msg(a, XR, XN, 372, "ICMP admin prohibited", 60, 75, a.AMB)
msg(a, XN, XR, 420, "UDP 53 → al redirect", 66, 75, a.OK)

# 4. DoH a mano
msg(a, XN, XI, 300, "HTTPS 443 a 1.1.1.1", 78, 100, a.GREY)
en(a, a.text(XR, 340, "para el firewall es una web más", 15, a.GREY, a.SANS, 600, "middle"), 82, 100)
torch = term(a, 48, 476, 760, ["/tool/torch bridge src-address=192.168.88.254/32 ip-protocol=tcp port=443", "", ""], size=14, lh=23)
for x, h, v in ((66, "SRC-ADDRESS", "192.168.88.254"), (286, "DST-ADDRESS", "1.1.1.1"), (466, "DST-PORT", "443")):
    torch += a.text(x, 529, h, 14, SKY, a.MONO) + a.text(x, 552, v, 14, GOLD, a.MONO, 600)
en(a, torch, 84, 100)
en(a, note(a, 48, 476, 760, 112, "Lo que hacen los paliativos", [
    "El canario frena el DoH automático de Firefox. Cortar el 853 manda",
    "los equipos al 53. Quien configura DoH a mano o usa VPN, pasa igual."], "amb"), 0, 84, still=1)
a.add(note(a, 836, 476, 316, 112, "Para ver si alguien lo usa", ["Torch con port=443 hacia", "1.1.1.1 o 8.8.8.8."], "info"))

narr(a, [
    (0, 25, "El dominio canario es una señal de Mozilla para redes con filtros.", a.TXT),
    (25, 50, "Una sola estática basta: vale para toda la LAN que usa el router.", a.OK),
    (50, 75, "Reject avisa al instante: el equipo no se queda esperando el 853.", a.AMB),
    (75, 100, "DoH va dentro de HTTPS: no hay puerto que lo distinga.", a.TXT),
], still_idx=1)

escribir(a, "31-l2.svg", "Paliativos para DoH",
         "Animación en cuatro tiempos con tres líneas de vida: un equipo de la LAN, el router con su resolver y su firewall, e internet con servidores DoT (853) y DoH (443). "
         "1: Firefox, antes de prender DoH por su cuenta, pregunta por use-application-dns.net. 2: el router tiene una estática type=NXDOMAIN para ese nombre y contesta NXDOMAIN, "
         "así que Firefox no activa DoH solo y sigue con el DNS del sistema por el 53. 3: un celular con DNS privado prueba TCP 853; la regla de forward lo rechaza con ICMP admin prohibited "
         "y el equipo vuelve a preguntar por UDP 53, donde lo toma el redirect. 4: un equipo con DoH configurado a mano va por HTTPS 443 a 1.1.1.1: para el firewall es una web más; "
         "Torch con port=443 lo muestra.",
         [12, 40, 62, 72, 94])
