#!/usr/bin/env python3
"""Lección 4 (Input y forward) · Laboratorio paso 6: NVR a NTP, reject para el resto del NVR y drop para las cámaras, vistos en el cable."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · INPUT Y FORWARD · PASO 6", "Reject avisa, drop calla",
             ["El NVR pide la hora por UDP 123: coincide con lab: NVR a NTP y sale.",
              "El NVR abre una web: baja hasta lab: NVR resto, que la rechaza.",
              "Vuelve un ICMP admin prohibited: el NVR se entera al instante.",
              "La cámara quiere salir: el drop no contesta y ella reintenta y espera."], still=2)

dev(a, 48, 196, 214, 96, "NVR", "192.168.88.50", ssize=14)
dev(a, 48, 456, 214, 96, "Cámara", "192.168.88.101", ssize=14)
dev(a, 958, 196, 194, 96, "Internet", "out-interface-", "list=WAN", kind="isp", ssize=14)

RULES = [("accept", "lab: NVR a NTP", "udp 123", a.OK, a.OKBG),
         ("accept", "lab: NVR a su nube", "nube-nvr", a.OK, a.OKBG),
         ("reject", "lab: NVR resto", "icmp-admin-prohibited", a.AMB, a.AMBBG),
         ("drop", "lab: camaras sin internet", "", a.BAD, a.BADBG)]
RX, RW, R0, RS, RH = 330, 520, 214, 66, 52
a.add(a.text(RX, R0 - 14, "chain=forward  ·  las de la configuración por defecto, arriba", 15, a.GREY, a.MONO))
cy = []
for i, (act, name, extra, c, bg) in enumerate(RULES):
    y = R0 + i * RS
    cy.append(y + RH / 2)
    a.add(a.box(RX, y, RW, RH, a.WHITE, a.LINE, rx=12))
    a.add(a.pill(RX + 14, y + 12, act, c, bg, 14, 28))
    a.add(a.text(RX + 108, y + 32, name, 15, a.INK, a.MONO, 600))
    if extra:
        a.add(a.text(RX + RW - 16, y + 32, extra, 14, a.GREY, a.MONO, 400, "end"))

def hit(i, t0, t1, c, still=0):
    y = R0 + i * RS
    en(a, ring(a, RX - 3, y - 3, RW + 6, RH + 6, c, rx=14), t0, t1, still)

PX = 296
a.add(wire(PX, cy[0], PX, cy[-1], a.LINE, 2, "4 6"))
# 1. NTP
go(a, "NTP", [(262, 244), (PX, 244), (PX, cy[0])], 2, 5, hold=4, bg=a.BLUE, size=14)
hit(0, 6, 24, a.OK)
go(a, "NTP", [(RX + RW + 34, cy[0]), (922, cy[0])], 9, 13, hold=8, bg=a.OK, size=14)

# 2. web del NVR baja hasta el reject
go(a, "TCP 443", [(262, 244), (PX, 244), (PX, cy[2])], 27, 33, hold=3, bg=a.BLUE, size=14)
hit(2, 34, 75, a.AMB, still=1)

# 3. vuelve el ICMP
go(a, "ICMP", [(PX, cy[2]), (155, cy[2]), (155, 318)], 51, 57, hold=1, bg=a.AMB, size=14)
en(a, a.text(155, cy[2] + 36, "admin prohibited", 15, a.AMB, a.MONO, 600, "middle"), 51, 75, still=1)
fijo(a, at(pillc(a, "ICMP", bg=a.AMB, size=14), 210, cy[2]))
en(a, a.box(48, 292, 214, 46, a.AMBBG, rx=10) + a.text(155, 321, "falla al instante", 15, a.AMB, a.SANS, 600, "middle"), 58, 75, still=1)

# 4. cámara y drop
for k, t0 in enumerate((78, 86, 94)):
    go(a, "SYN", [(262, 504), (PX, 504), (PX, cy[3])], t0, t0 + 3, hold=1.5, bg=a.GREY, size=14)
    en(a, a.text(905, 444 + k * 30, f"SYN {k + 1}: sin respuesta", 15, a.BAD, a.MONO, 600), t0 + 3, 100)
hit(3, 80, 100, a.BAD)
en(a, mark(a, RX + RW + 26, cy[3], ok=False), 81, 100)
en(a, a.text(905, 416, "la cámara reintenta", 15, a.GREY, a.SANS, 600), 80, 100)

narr(a, [
    (0, 25, "Lo nuevo que sale de la LAN baja por forward hasta la primera que coincide.", a.TXT),
    (25, 50, "No es NTP ni su nube: llega a la regla del resto del NVR.", a.TXT),
    (50, 75, "Adentro conviene reject: el equipo no queda colgado esperando.", a.AMB),
    (75, 100, "Hacia afuera, drop: al que escanea no se le contesta nada.", a.BAD),
], still_idx=2)

escribir(a, "4-l2.svg", "Reject y drop en forward",
         "Animación en cuatro tiempos con el NVR (192.168.88.50) y una cámara (192.168.88.101) a la izquierda, internet a la derecha y cuatro reglas de forward en orden: "
         "accept lab: NVR a NTP (UDP 123), accept lab: NVR a su nube, reject lab: NVR resto con icmp-admin-prohibited y drop lab: camaras sin internet. "
         "1: el NVR pide la hora por UDP 123, coincide la primera regla y el paquete sale a internet. 2: el NVR abre una página web por TCP 443 y baja hasta la regla de reject. "
         "3: el router le devuelve un ICMP admin prohibited y la conexión falla al instante. 4: la cámara manda un SYN, el drop lo descarta sin contestar y la cámara reintenta "
         "varias veces sin respuesta.",
         [10, 38, 60, 70, 96])
