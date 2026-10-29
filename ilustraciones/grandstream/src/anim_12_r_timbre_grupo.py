#!/usr/bin/env python3
"""Lección 12 (Portero en la central) · Resumen, "Cómo se ve en la red": el timbre del GDS3710 llama al grupo 6000,
la UCM hace sonar a los dos teléfonos a la vez, atiende recepción y la central cancela la llamada al otro; la imagen
depende del modelo. Fuentes: la lección (GDS registrado como 8001; Doorbell Mode Call Doorbell Number al 6000; la
UCM hace sonar a todos los miembros; GRP2601 a 2604, 2612 y 2613 solo audio; GRP2614 en adelante con imagen);
RFC 3261 (INVITE, 200 OK, CANCEL y 487 a las ramas que no atendieron)."""
from _anim_gs_red import R

g = R(T=28, fix=70, kicker="GRANDSTREAM · PORTERO EN LA CENTRAL · CÓMO SE VE EN LA RED",
      title="Un timbre, dos teléfonos: suena en los dos, atiende uno")
g.steps([
    "Tocan el timbre: el GDS3710, registrado como 8001, manda un INVITE al grupo 6000.",
    "La UCM llama a los dos miembros a la vez: suenan recepción y seguridad.",
    "Atiende recepción: la central le cancela la llamada a seguridad, que deja de sonar.",
    "Hablan por la central; el GRP2614 muestra además la imagen, un GRP2602 no.",
])

XG, XU, XR, XS = 130, 420, 720, 1020
g.lane(XG, 176, 600, "GDS3710", "extensión 8001", w=200)
g.lane(XU, 176, 600, "UCM", "Ring Group 6000", w=210)
g.lane(XR, 176, 600, "Recepción", "GRP2614", w=200)
g.lane(XS, 176, 600, "Seguridad", "GRP2602", w=200)

g.msg(XG, XU, 262, "INVITE 6000", g.BLUE, 3, 9, tok="INVITE")
g.msg(XU, XR, 304, "INVITE", g.BLUE, 27, 32)
g.arrow([(XU, 340), (XS, 340)], 27, 34, g.BLUE)
g.appear(g.text(880, 330, "INVITE", 15, g.BLUE, g.MONO, 600, "middle"), 33.5, 100)
g.appear(g.pillc(XR, 360, "suena", g.CYAN, "#E3F4FA", 13, 24), 33, 54)
g.appear(g.pillc(XS, 376, "suena", g.CYAN, "#E3F4FA", 13, 24), 35, 58)
g.msg(XR, XU, 414, "200 OK · atiende", g.OK, 52, 56)
g.arrow([(XU, 450), (XS, 450)], 57, 61, g.AMB)
g.appear(g.text(880, 440, "CANCEL", 15, g.AMB, g.MONO, 600, "middle"), 60.5, 100)
g.arrow([(XS, 486), (XU, 486)], 62, 65, g.GREY, dashed=True)
g.appear(g.text(880, 476, "487 · cancelada", 15, g.GREY, g.MONO, 600, "middle"), 64.5, 100)
g.appear(g.pillc(XS, 506, "dejó de sonar", g.GREY, g.SLATE, 13, 24), 65, 100)
g.msg(XU, XG, 522, "200 OK", g.OK, 66, 70)
for k in range(3):
    t = 78 + k * 5
    g.token([(XG, 562), (XU, 562)], t, t + 4, g.chip("audio", bg=g.OK, size=13, h=24), hold=t + 4.2)
    g.token([(XU, 562), (XR, 562)], t + 1.5, t + 5.5, g.chip("audio", bg=g.OK, size=13, h=24), hold=t + 5.7)
g.appear(g.pillc(XR, 592, "además, imagen JPEG", g.OK, g.OKBG, 13, 24), 80, 100)
g.appear(g.pillc(XS, 548, "GRP2602: solo audio", g.GREY, g.SLATE, 13, 24), 80, 100)

g.status(640, [
    (0, 25, "El portero es una extensión más: el timbre es una llamada a un número.", g.INK),
    (25, 50, "El grupo reparte la atención: si recepción no está, atiende seguridad.", g.INK),
    (50, 75, "El primero que atiende se queda con la llamada; al resto se le cancela.", g.OK),
    (75, 100, "Para abrir: el PIN por DTMF durante la llamada, o OpenDoor sin atender.", g.INK),
], size=16)

g.done(12, "r1", "Un timbre, dos teléfonos: suena en los dos, atiende uno",
       "Animación en cuatro tiempos con cuatro líneas de vida: el portero GDS3710 registrado como extensión 8001, la UCM con el Ring Group 6000, recepción con un GRP2614 y seguridad con un GRP2602. "
       "1: tocan el timbre y el GDS3710 manda un INVITE al 6000. "
       "2: la UCM manda un INVITE a cada miembro a la vez y suenan los dos teléfonos. "
       "3: recepción atiende con 200 OK; la central le manda CANCEL a seguridad, que responde 487 y deja de sonar, y la UCM le contesta 200 OK al portero. "
       "4: el audio va del portero a la UCM y de la UCM a recepción; el GRP2614 muestra además la imagen JPEG del portero, y un GRP2602 solo tendría audio. "
       "Para abrir se usa el PIN por DTMF durante la llamada o la tecla OpenDoor sin atender.",
       [8, 40, 62, 92])
