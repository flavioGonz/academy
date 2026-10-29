#!/usr/bin/env python3
"""Lección 3 · Laboratorio, paso 6: comprobar en el teléfono que la cuenta registró y que la hora es la correcta.
Lo que pasa en la red: REGISTER de la cuenta 1 contra la UCM y, para la hora, la consulta NTP (que responde en UTC)
más la zona horaria que bajó con la Global Policy (Montevideo, UTC-3). Fuentes: guía Zero Config (la categoría
Localization incluye zona horaria y servidor NTP; prioridad de plantillas; lo tocado a mano no se pisa); NTP RFC 5905."""
from _anim_gs_red import R

g = R(T=24, fix=68, kicker="GRANDSTREAM · ZERO CONFIG · LABORATORIO",
      title="Registrado y con la hora de acá: qué lo confirma")
g.steps([
    "Con el XML aplicado, el teléfono registra la cuenta 1: REGISTER 1001 y 200 OK.",
    "Para la hora le pregunta al servidor NTP: la respuesta viene en UTC.",
    "Le suma la zona de la Global Policy, Montevideo (UTC-3): muestra 10:00.",
    "Si la hora sale corrida 3 horas, la zona no llegó: plantilla o algo tocado a mano.",
])

Y, H = 190, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 250, H, "UCM", "192.168.88.20", icon="ucm", dark=True))
g.add(g.dev(470, Y, 250, H, "GRP26xx", "aprovisionado", icon="tel"))
g.add(g.dev(902, Y, 250, H, "Servidor NTP", "de la Global Policy", icon="clock"))
g.add(g.wire(298, YL, 470, YL, g.BLUE))
g.add(g.wire(720, YL, 902, YL, g.BLUE))
LANE = Y - 20
g.token([(560, LANE), (190, LANE)], 3, 10, g.chip("REGISTER 1001", bg=g.BLUE, size=13, h=26), hold=11)
g.token([(190, LANE), (560, LANE)], 13, 20, g.chip("200 OK", bg=g.OK, size=13, h=26), hold=21)
g.token([(640, LANE), (1010, LANE)], 28, 35, g.chip("NTP: ¿qué hora es?", bg=g.BLUE, size=13, h=26), hold=36)
g.token([(1010, LANE), (640, LANE)], 38, 45, g.chip("13:00 UTC", bg=g.OK, size=13, h=26), hold=46)

# pantalla del teléfono
SX, SY, SW, SH = 420, 344, 350, 196
g.add(g.box(SX, SY, SW, SH, "#E9F1F8", g.LINE, rx=18))
g.add(g.box(SX + 18, SY + 18, SW - 36, SH - 36, "#03213C", None, rx=10))
g.add(g.text(SX + 36, SY + 50, "pantalla del GRP", 14, g.SKY, g.MONO))
g.appear(g.text(SX + 36, SY + 92, "1001  sin registrar", 20, g.GOLD, g.MONO, 600), 0, 20)
g.appear(g.text(SX + 36, SY + 92, "1001  registrada", 20, g.MINT, g.MONO, 600), 20, 100)
g.appear(g.text(SX + 36, SY + 138, "--:--", 30, "#D9E9F8", g.MONO, 600), 0, 50)
g.appear(g.text(SX + 36, SY + 138, "10:00", 30, g.MINT, g.MONO, 600), 50, 75)
g.appear(g.text(SX + 36, SY + 138, "13:00", 30, g.GOLD, g.MONO, 600), 75, 100)
g.appear(g.text(SX + 160, SY + 136, "Montevideo", 16, g.SKY, g.MONO), 50, 75)
g.appear(g.text(SX + 160, SY + 136, "zona: GMT", 16, g.GOLD, g.MONO), 75, 100)

# cuenta a la izquierda
g.add(g.box(48, SY, 340, SH, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, SY + 34, "La cuenta", 17, g.INK, g.SANS, 600))
g.add(g.text(68, SY + 66, "cuenta 1 → extensión 1001", 15, g.TXT, g.MONO))
g.add(g.text(68, SY + 94, "servidor: 192.168.88.20", 15, g.TXT, g.MONO))
g.appear(g.text(68, SY + 140, "200 OK: la central la acepta", 16, g.OK, g.SANS, 600) + g.mark(352, SY + 135, True, 14), 20, 100)

# la hora a la derecha
g.add(g.box(812, SY, 340, SH, g.WHITE, g.LINE, rx=14))
g.add(g.text(832, SY + 34, "La hora", 17, g.INK, g.SANS, 600))
g.appear(g.text(832, SY + 66, "NTP: 13:00 UTC", 16, g.TXT, g.MONO, 600), 45, 100)
g.appear(g.text(832, SY + 94, "zona Montevideo: UTC-3", 16, g.OK, g.MONO, 600)
         + g.text(832, SY + 122, "13:00 - 3 h = 10:00", 16, g.OK, g.MONO, 600), 50, 75)
g.appear(g.text(832, SY + 94, "zona que quedó: GMT", 16, g.BAD, g.MONO, 600)
         + g.text(832, SY + 122, "muestra 13:00: 3 h corrida", 16, g.BAD, g.MONO, 600), 75, 100)
g.appear(g.text(832, SY + 168, "Global Policy: Montevideo", 15, g.GREY, g.MONO), 50, 100)

g.status(612, [
    (0, 25, "En el teléfono: la cuenta 1001 figura registrada, no en rojo ni en gris.", g.OK),
    (25, 50, "NTP da la hora universal; la zona la pone el teléfono.", g.INK),
    (50, 75, "Hora correcta: la Global Policy llegó y se aplicó.", g.OK),
    (75, 100, "Otra plantilla con más prioridad o un ajuste a mano: reset de fábrica y que lo tome Zero Config.", g.BAD),
], size=16)

g.done(3, "l1", "Registrado y con la hora de acá: qué lo confirma",
       "Animación en cuatro tiempos con la UCM en 192.168.88.20, un GRP26xx ya aprovisionado y el servidor NTP de la Global Policy; abajo, la pantalla del teléfono, la cuenta y la hora. "
       "1: con el XML aplicado, el teléfono manda REGISTER 1001 y la UCM responde 200 OK; la pantalla pasa de sin registrar a 1001 registrada. "
       "2: para la hora, el teléfono le pregunta al servidor NTP y la respuesta viene en hora universal, 13:00 UTC. "
       "3: le aplica la zona de la Global Policy, Montevideo, UTC-3, y la pantalla muestra 10:00. "
       "4: si la hora sale corrida 3 horas, por ejemplo 13:00 con zona GMT, la zona no llegó: hay otra plantilla con más prioridad o alguien la cambió a mano en el teléfono; se resetea de fábrica y se deja que lo tome Zero Config.",
       [8, 40, 64, 90])
