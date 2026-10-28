#!/usr/bin/env python3
"""Lección 28 · L2TP saliente · Resumen ("Cómo se ve en la red").
La sucursal detrás de CGNAT llama a la central: la respuesta vuelve como established sin abrir puertos,
una conexión nueva desde internet muere en el CGNAT, y por el túnel la central sí llega a la LAN de la sucursal.
"""
from _anim_mk_32_39 import *

a = Anim(T=27, kicker="MIKROTIK · L2TP SALIENTE · CÓMO SE VE EN LA RED", title="La sucursal llama: sale, y lo de vuelta entra")
a.steps([
    "La sucursal llama: IKE sale hacia 203.0.113.10 y el CGNAT anota la traducción.",
    "La central contesta. En el hAP llega como established: input lo deja pasar.",
    "Arriba IPsec (UDP 4500 por el NAT), adentro L2TP y PPP: l2tp-central 10.255.1.2.",
    "Una conexión nueva desde internet hacia la sucursal muere en el CGNAT.",
    "Por el túnel sí: la central llega a 192.168.88.0/24 por 10.255.1.2.",
], still=4, size=17)

TY, TH = 186, 96
CY = TY + TH / 2
# túnel (detrás de los equipos)
a.add(during(a, a.box(280, CY - 22, 640, 44, a.OK, a.OK, rx=22, sw=2, extra='fill-opacity=".14"'), 44, 100, still=1))
a.add(line(288, CY, 912, CY, a.LINE, 3, "5 7"))
a.add(during(a, a.text(746, CY - 32, "túnel · IPsec · UDP 4500", 15, a.OK, a.MONO, 600, "middle")
             + a.text(746, CY + 42, "adentro L2TP y PPP", 15, a.OK, a.MONO, 600, "middle"), 46, 100, still=1))
a.add(during(a, a.text(746, CY - 32, "internet", 15, a.GREY, a.MONO, 400, "middle"), 0, 45))

a.add(router(a, 48, TY, 240, TH, "hAP sucursal", "WAN 100.72.15.4", "LAN 192.168.88.0/24"))
a.add(a.box(360, TY + 6, 220, TH - 12, a.AMBBG, a.AMB, rx=14))
a.add(a.text(380, TY + 38, "CGNAT del proveedor", 16, a.AMB, a.SANS, 600))
a.add(a.text(380, TY + 64, "198.51.100.40", 15, a.AMB, a.MONO))
a.add(router(a, 912, TY, 240, TH, "Central", "203.0.113.10", "LAN 10.10.1.0/24"))

# anotación del CGNAT
a.add(during(a, a.pill(470, 300, "anota 100.72.15.4 ↔ 198.51.100.40", a.AMB, a.AMBBG, 14, 28, "middle"), 6, 100, still=1))
# interfaz del túnel
a.add(during(a, a.pill(48, 300, "l2tp-central 10.255.1.2", a.OK, a.OKBG, 14, 28), 54, 100, still=1))

# input del hAP
IX, IY = 48, 360
a.add(a.box(IX, IY, 520, 128, a.INK, rx=14))
a.add(a.text(IX + 18, IY + 28, "hAP · /ip/firewall/filter · input", 15, SKY, a.MONO))
a.add(a.box(IX + 14, IY + 40, 492, 36, a.NAVY2, rx=8))
a.add(a.text(IX + 28, IY + 64, "defconf: accept established,related,untracked", 15, MINT, a.MONO, 600))
a.add(a.box(IX + 14, IY + 82, 492, 36, a.NAVY2, rx=8))
a.add(a.text(IX + 28, IY + 106, "defconf: drop all not coming from LAN", 15, ROSE, a.MONO, 600))
a.add(during(a, a.box(IX + 10, IY + 36, 500, 44, "none", MINT, rx=10, sw=3), 34, 42))
a.add(during(a, a.pill(IX + 506, IY + 6, "sin abrir puertos", a.OK, a.OKBG, 13, 24, "end"), 34, 100, still=1))

# ruta en la central
a.add(a.box(912, 360, 240, 128, a.WHITE, a.LINE, rx=14))
a.add(a.text(930, 388, "ruta en la central", 15, a.GREY, a.MONO))
a.add(a.text(930, 418, "192.168.88.0/24", 17, a.INK, a.MONO, 600))
a.add(a.text(930, 444, "gateway=10.255.1.2", 15, a.TXT, a.MONO))
a.add(during(a, a.box(908, 356, 248, 136, "none", a.OK, rx=16, sw=3), 80, 92))

# internet que intenta entrar
a.add(dev(a, 640, 372, 230, 84, "Internet", "conexión nueva", "globe", tsize=17))

# 1. IKE de ida
a.add(travel(a, pkt(a, "IKE · UDP 500", size=14, h=28), [(300, CY), (350, CY)], 1, 4, hold=1.5))
a.add(travel(a, pkt(a, "IKE · UDP 500", size=14, h=28), [(620, CY), (880, CY)], 7, 14, hold=2))
# 2. respuesta
a.add(travel(a, pkt(a, "respuesta", a.OK, size=14, h=28), [(880, CY), (620, CY)], 21, 27, hold=1))
a.add(travel(a, pkt(a, "respuesta", a.OK, size=14, h=28), [(350, CY), (300, CY)], 29, 32, hold=2))
# 4. intento desde internet
a.add(travel(a, pkt(a, "SYN nuevo", a.BAD, size=14, h=28), [(700, 372), (560, 300), (520, 290)], 62, 68, hold=2))
a.add(during(a, xmark(a, 548, 270), 69, 80))
a.add(during(a, a.text(755, 486, "no hay traducción para esto", 15, a.BAD, a.SANS, 600, "middle"), 69, 80))
# 5. por el túnel
a.add(travel(a, pkt(a, "→ 192.168.88.50", a.OK, size=14, h=28), [(860, CY), (650, CY)], 82, 86, hold=0.5))
a.add(travel(a, dot(a, a.OK), [(345, CY), (300, CY)], 88, 91, hold=8))
a.add(during(a, check(a, 262, TY + 22), 91, 100, still=1))
a.add(still_only(a, place(pkt(a, "→ 192.168.88.50", a.OK, size=14, h=28), 746, CY)))

narr(a, 48, 548, [
    (0, 20, "La conexión la abre la sucursal: el hAP y el CGNAT la anotan.", a.TXT, 0),
    (20, 40, "La respuesta encaja con lo anotado: entra por la primera regla de input.", a.OK, 0),
    (40, 60, "El túnel es una conexión que salió de la sucursal y sigue abierta.", a.OK, 0),
    (60, 80, "Por eso el port forwarding no sirve detrás de CGNAT, y el túnel saliente sí.", a.BAD, 0),
    (80, 100, "Lo que viene por el túnel no entra por la lista WAN: en forward pasa.", a.OK, 1),
])
a.add(a.text(48, 640, "/interface/l2tp-client · connect-to=203.0.113.10 use-ipsec=yes add-default-route=no", 16, a.TXT, a.MONO))

write(a, 28, "r1", "La sucursal llama: sale, y lo de vuelta entra",
      "Animación en cinco tiempos con el hAP de la sucursal (WAN 100.72.15.4, LAN 192.168.88.0/24), el CGNAT del proveedor con la IP compartida 198.51.100.40 y la central 203.0.113.10 con LAN 10.10.1.0/24. "
      "1: la sucursal llama: el cliente L2TP manda IKE por UDP 500 hacia 203.0.113.10 y el CGNAT anota la traducción de 100.72.15.4 a 198.51.100.40. "
      "2: la central contesta; la respuesta encaja con lo anotado, llega al hAP como established y la primera regla de input, accept established,related,untracked, la deja pasar sin abrir puertos. "
      "3: se arma IPsec, por UDP 4500 porque hay NAT, y adentro L2TP y PPP: en la sucursal aparece l2tp-central con 10.255.1.2. "
      "4: una conexión nueva desde internet hacia la sucursal muere en el CGNAT: no hay traducción para ella. Por eso detrás de CGNAT no sirve el port forwarding y el túnel saliente sí. "
      "5: por el túnel, la central llega a 192.168.88.0/24 con la ruta gateway=10.255.1.2; lo que viene por el túnel no entra por la lista WAN y en forward pasa.",
      [5, 12, 30, 50, 66, 74, 88])
