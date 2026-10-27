"""Teoría de Alarmas con criterio: del disparo a la alarma, pasando por los filtros y las acciones."""
from _anim_hc import *

caps = ["Se activa la entrada 1 (contacto de puerta) y el NVR avisa a la plataforma.",
        "Llegan dos disparos más en 30 s: Ignore Repetitive los cuenta como uno.",
        "Trigger Recording guarda de 10 s antes a 30 s después, bloqueado 7 días.",
        "Trigger Alarm: la alarma de prioridad alta llega al guardia, que la reconoce."]
a = new(28, "Eventos", "Del disparo a la alarma: filtrar, grabar y avisar", caps, still=3)

a.add(card(a, 48, 214, 230, 92, "Entrada 1", "contacto de puerta"))
a.add(a.box(330, 186, 520, 300, a.WHITE, a.LINE, rx=18))
a.add(a.text(354, 220, "Regla en HikCentral", 18, a.INK, a.SANS, 600))
ST = [("Ignore Repetitive", "30 s"), ("Trigger Recording", "CAM-02 · pre 10 s · post 30 s"), ("Lock Video Files", "7 días"), ("Trigger Alarm", "prioridad alta · usuario guardia")]
for i, (k, v) in enumerate(ST):
    y = 240 + i * 58
    a.add(a.box(354, y, 472, 48, a.SLATE, rx=10))
    a.add(a.text(372, y + 30, k, 16, a.INK, a.MONO, 600))
    a.add(a.text(808, y + 30, v, 14, a.GREY, a.MONO, anchor="end"))
hl = [(0, 1), (2, 2), (2, 2), (3, 3)]
for i, (p0, p1) in enumerate(hl):
    vis(a, a.box(354, 240 + i * 58, 472, 48, "none", a.CYAN, rx=10, sw=3), p0, p1, still=1 if i == 3 else 0)
a.add(card(a, 902, 214, 250, 92, "Control Client", "usuario guardia"))

s0, s1 = ph(a, 0)
token(a, "disparo", [(s0 + 4, 163, 330), (s0 + 14, 340, 264)], bg=a.AMB)
vis(a, a.pill(163, 340, "1 evento", a.AMB, a.AMBBG, anchor="middle"), 0, 3)
s0, s1 = ph(a, 1)
for k in range(2):
    token(a, "disparo", [(s0 + 3 + k * 8, 163, 330), (s0 + 11 + k * 8, 340, 264)], bg=a.AMB)
vis(a, a.text(163, 400, "+2 en 30 s", 15, a.GREY, a.MONO, 600, "middle"), 1, 3)
vis(a, a.text(163, 424, "siguen siendo 1", 15, a.OK, a.SANS, 600, "middle"), 1, 3)

# clip
X0, Y, SC = 330, 520, 13
t0 = X0 + 10 * SC
a.add(a.text(48, Y + 24, "clip de CAM-02", 15, a.INK, a.MONO, 600))
clip = (a.box(X0, Y, 10 * SC, 36, "#E5F0FB", a.BLUE, rx=8) + a.text(X0 + 5 * SC, Y + 24, "pre 10 s", 14, a.BLUE, a.MONO, 600, "middle")
        + a.box(t0, Y, 30 * SC, 36, a.OKBG, a.OK, rx=8) + a.text(t0 + 15 * SC, Y + 24, "post 30 s", 14, a.OK, a.MONO, 600, "middle")
        + f'<path d="M{t0} {Y - 10} V{Y + 46}" stroke="#D2492F" stroke-width="3"/>'
        + a.text(t0, Y + 66, "disparo", 14, a.BAD, a.MONO, 600, "middle")
        + a.pill(t0 + 30 * SC + 16, Y + 4, "bloqueado 7 días", a.WHITE, a.INK))
vis(a, clip, 2, 3)

s0, s1 = ph(a, 3)
token(a, "ALARMA · alta", [(s0 + 2, 860, 430), (s0 + 10, 1027, 340)], bg=a.BAD)
a.add(a.group(a.pill(1027, 330, "alarma · prioridad alta", a.WHITE, a.BAD, anchor="middle"), a.show(s0 + 10, s1), still=1))
a.add(a.group(a.pill(1027, 370, "reconocida", a.OK, a.OKBG, anchor="middle"), a.show(s0 + 15, s1), still=1))
a.add(a.text(48, 640, "Sin Trigger Alarm, todo esto queda como evento: registrado, pero sin avisar a nadie.", 17, a.TXT))
write(a, "8-t1.svg", "Del disparo a la alarma", [10, 36, 62, 94])
