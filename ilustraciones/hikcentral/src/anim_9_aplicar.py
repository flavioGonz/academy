"""Teoría de Niveles de acceso: la controladora decide con su copia; aplicar es enviar."""
from _anim_hc import *

caps = ["En el SYS se asigna Oficina hábil a Prueba Lab: queda pendiente.",
        "Pasa la tarjeta: la controladora no tiene ese permiso y deniega.",
        "Aplicar cambios: viaja solo ese registro y la controladora sigue online.",
        "La misma tarjeta pasa de nuevo: concedido, con lo que tiene guardado."]
a = new(26, "Acceso", "La puerta decide con su copia: aplicar es enviarla", caps, still=3)

a.add(a.box(48, 186, 420, 270, a.INK, a.INK, rx=18))
a.add(a.text(72, 222, "SYS · base de datos", 19, a.WHITE, a.SANS, 600))
a.add(a.text(72, 262, "Personas y niveles", 15, DARK_SUB, a.MONO))
a.add(a.box(72, 278, 372, 44, a.NAVY2, rx=10) + a.text(90, 306, "Otra persona · Depósito", 15, "#D9E9F8", a.MONO))
vis(a, a.box(72, 334, 372, 44, a.NAVY2, a.CYAN, rx=10, sw=2) + a.text(90, 362, "Prueba Lab · Oficina hábil", 15, a.WHITE, a.MONO, 600), 0, 3)
vis(a, a.pill(72, 400, "pendiente de aplicar", a.AMB, a.AMBBG), 0, 1)
vis(a, a.pill(72, 400, "aplicado", a.OK, a.OKBG), 3)

a.add(a.box(732, 186, 420, 270, a.WHITE, a.LINE, rx=18))
a.add(a.text(756, 222, "Controladora · Puerta Lab", 19, a.INK, a.SANS, 600))
a.add(a.text(756, 262, "Lo que tiene guardado", 15, a.GREY, a.MONO))
a.add(a.box(756, 278, 372, 44, a.SLATE, rx=10) + a.text(774, 306, "Otra persona · Depósito", 15, a.TXT, a.MONO))
vis(a, a.box(756, 334, 372, 44, a.OKBG, a.OK, rx=10, sw=2) + a.text(774, 362, "Prueba Lab · Oficina hábil", 15, a.OK, a.MONO, 600), 2, 3)
vis(a, a.pill(756, 400, "online", a.OK, a.OKBG), 0, 3)
a.add(line(a, 468, 320, 732, 320, a.LINE, 3, arrow=False, dash="6 6"))

s0, s1 = ph(a, 2)
token(a, "solo el cambio", [(s0 + 3, 490, 300), (s0 + 14, 712, 300)], bg=a.BLUE)
vis(a, a.text(600, 350, "Apply (Initial): sin marcar", 15, a.BLUE, a.MONO, 600, "middle"), 2, 3)

# tarjeta
a.add(a.text(756, 510, "tarjeta de Prueba Lab", 15, a.GREY, a.MONO))
for k in (1, 3):
    s0, s1 = ph(a, k)
    token(a, "0001234567", [(s0 + 2, 940, 560), (s0 + 9, 940, 470)], bg=a.CYAN)
s0, s1 = ph(a, 1)
a.add(a.group(a.pill(940, 520, "denegado: no la conoce", a.BAD, a.BADBG, anchor="middle"), a.show(s0 + 9, s1), still=0))
s0, s1 = ph(a, 3)
a.add(a.group(a.pill(940, 520, "concedido", a.OK, a.OKBG, anchor="middle"), a.show(s0 + 9, s1), still=1))

a.add(a.text(48, 512, "Editar en la plataforma no cambia la puerta.", 17, a.TXT))
a.add(a.text(48, 540, "Aplicar es lo que lleva el cambio a cada", 17, a.TXT))
a.add(a.text(48, 568, "controladora.", 17, a.TXT))
a.add(a.text(48, 628, "Apply (Initial) borra y reescribe todo: mientras tanto, la puerta queda offline.", 17, a.BAD, a.SANS, 600))
write(a, "9-t1.svg", "Aplicar a los dispositivos", [10, 36, 62, 92])
