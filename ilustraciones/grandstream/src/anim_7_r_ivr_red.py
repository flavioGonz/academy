#!/usr/bin/env python3
"""Lección 7 (IVR con horario) · Resumen, "Cómo se ve en la red": lo que viaja cuando alguien llama al IVR desde
afuera. La UCM atiende la llamada del troncal, manda la bienvenida por RTP, recibe la tecla como evento RFC 4733 y
recién ahí llama al grupo; la pata con el proveedor sigue siendo la misma. Fuentes: la lección (la ruta entrante
apunta al IVR; teclas como eventos RFC 4733; Office Time decide el destino de la tecla); RFC 3261 (INVITE, 200 OK,
ACK), RFC 4733."""
from _anim_gs_red import R

g = R(T=28, fix=86, kicker="GRANDSTREAM · IVR CON HORARIO · CÓMO SE VE EN LA RED",
      title="Una llamada al IVR, vista en la red")
g.steps([
    "Entra la llamada por el troncal y la ruta entrante la manda al IVR 7000.",
    "El IVR atiende: 200 OK, y la bienvenida viaja como audio RTP hacia quien llama.",
    "Quien llama marca 1: llega como evento RFC 4733 y es horario de oficina.",
    "La UCM llama al grupo ventas; atiende un teléfono y la central une las dos patas.",
])

XP, XU, XV = 150, 560, 980
g.lane(XP, 176, 600, "Quien llama", "por el troncal SIP", w=230)
g.lane(XU, 176, 600, "UCM · IVR 7000", "ruta entrante → 7000", w=250)
g.lane(XV, 176, 600, "Ring Group ventas", "teléfonos de ventas", w=250)

g.msg(XP, XU, 258, "INVITE", g.BLUE, 2, 8, tok="INVITE")
g.msg(XU, XP, 298, "200 OK · el IVR atiende", g.OK, 27, 31)
g.msg(XP, XU, 332, "ACK", g.BLUE, 32, 35)
for k in range(3):
    t = 37 + k * 4
    g.token([(XU, 370), (XP, 370)], t, t + 4, g.chip("RTP · bienvenida", bg=g.CYAN, size=13, h=24), hold=t + 4.3)
g.appear(g.text(XU + 18, 375, "«para ventas, marque 1…»", 15, g.CYAN, g.MONO, 600), 37, 100)
g.msg(XP, XU, 418, "RTP · evento: tecla 1", g.BLUE, 52, 58, tok="tecla 1")
g.appear(g.pill(XU + 16, 432, "Office Time → Ring Group ventas", g.OK, g.OKBG, 13, 26), 59, 100)
g.msg(XU, XV, 486, "INVITE", g.BLUE, 76, 80, tok="INVITE")
g.msg(XV, XU, 524, "200 OK · atiende", g.OK, 82, 85)
for k in range(3):
    t = 87 + k * 3.5
    g.token([(XP, 566), (XU, 566)], t, t + 3, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 3.2)
    g.token([(XU, 566), (XV, 566)], t + 1, t + 4, g.chip("RTP", bg=g.OK, size=13, h=24), hold=min(t + 4.2, 100))
g.fijo_only(f'<g transform="translate(355 566)">' + g.chip("RTP", bg=g.OK, size=13, h=24) + '</g>'
            + f'<g transform="translate(770 566)">' + g.chip("RTP", bg=g.OK, size=13, h=24) + '</g>')
g.appear(g.text(770, 596, "la pata del troncal sigue igual: la central une las dos", 15, g.OK, g.SANS, 600, "middle"), 86, 100)

g.status(640, [
    (0, 25, "El destino lo pone la ruta entrante: el IVR es una extensión más, la 7000.", g.INK),
    (25, 50, "Desde el 200 OK la llamada está atendida, aunque todavía no habló nadie.", g.AMB),
    (50, 75, "La tecla viaja dentro del audio; la hora de la central elige el destino.", g.INK),
    (75, 100, "Fuera de horario, la misma tecla 1 iría al buzón de la 1001.", g.GREY),
], size=16)

g.done(7, "r1", "Una llamada al IVR, vista en la red",
       "Animación en cuatro tiempos con tres líneas de vida: quien llama por el troncal SIP, la UCM con el IVR 7000 y el Ring Group ventas. "
       "1: entra el INVITE por el troncal y la ruta entrante lo manda al IVR 7000, que es una extensión más. "
       "2: el IVR atiende con 200 OK, el otro lado confirma con ACK y la bienvenida, para ventas marque 1, viaja como audio RTP hacia quien llama; desde el 200 OK la llamada está atendida. "
       "3: quien llama marca 1; la tecla llega dentro del RTP como evento RFC 4733 y, como es horario de oficina, la condición Office Time manda la llamada al Ring Group ventas. "
       "4: la UCM manda un INVITE al grupo, atiende un teléfono con 200 OK y el audio pasa de quien llama a la UCM y de la UCM a ventas: la pata del troncal sigue igual y la central une las dos. "
       "Fuera de horario, la misma tecla iría al buzón de la 1001.",
       [8, 40, 62, 90])
