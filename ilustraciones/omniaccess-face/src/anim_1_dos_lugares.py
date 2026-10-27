"""Teoría de Quién decide la puerta: el terminal abre solo; OmniAccess registra según el Modo Face."""
from _anim_face import *

caps = ["El terminal compara la cara con su memoria, la reconoce y dispara el relé.",
        "Aviso por Action URL al 10000; el servidor trae la foto y, en Lista Blanca, Permitido.",
        "En Lista Negra, la misma persona: la puerta abre igual y se registra Denegado.",
        "Sin red, la puerta sigue abriendo: el aviso no llega al servidor."]
a = new(24, "Dos lugares", "La puerta la abre el terminal; OmniAccess la registra", caps, still=2, size=17)
S = [sp[0] for sp in a.spans]

a.add(a.box(48, 186, 500, 330, "none", "#C2D4E6", rx=22, extra='stroke-dasharray="7 7"'))
a.add(a.text(70, 180, "EN LA PUERTA · DECIDE", 14, a.OK, a.MONO, 600))
a.add(a.box(640, 186, 512, 330, "none", "#C2D4E6", rx=22, extra='stroke-dasharray="7 7"'))
a.add(a.text(662, 180, "EN EL SERVIDOR · REGISTRA", 14, a.BLUE, a.MONO, 600))

# puerta
a.add(person(a, 118, 290, 1.0, extra='opacity="1"'))
a.add(a.text(118, 400, "Ana Ejemplo", 15, a.INK, a.SANS, 600, "middle"))
a.add(terminal(a, 210, 222, label="Terminal facial"))
a.add(a.pill(204, 428, "memoria: caras", a.INK, a.SLATE, size=13))
LX, LY = 430, 300
body = a.box(LX, LY + 34, 70, 56, a.INK, rx=10)
closed = f'<path d="M{LX + 14} {LY + 36} V{LY + 14} a21 21 0 0 1 42 0 V{LY + 36}" fill="none" stroke="{a.INK}" stroke-width="8"/>'
opened = f'<path d="M{LX + 14} {LY + 36} V{LY + 14} a21 21 0 0 1 42 0 V{LY + 4}" fill="none" stroke="{a.OK}" stroke-width="8" transform="translate(0 -14)"/>'
a.add(body + a.text(LX + 35, LY + 116, "cerradura", 15, a.INK, a.SANS, 600, "middle"))
opn = [(S[0] + 10, S[0] + 23), (S[2] + 3, S[2] + 21), (S[3] + 5, S[3] + 22)]
pts_o = [(0, 0)]
for p, q in opn:
    pts_o += [(p, 0), (p + .6, 1), (q, 1), (q + .6, 0)]
pts_o += [(100, 0)]
a.add(a.group(opened + a.text(LX + 35, LY + 140, "abre", 15, a.OK, a.MONO, 600, "middle"), a.keyframes(pts_o), still=1))
a.add(a.group(closed, a.keyframes([(p, 1 - v) for p, v in pts_o]), still=0))
for p, q in opn:
    a.add(a.group(line(a, 306, 362, LX - 6, 362, a.OK, 3), a.show(p - 2, p + 4, .5), still=0))
    a.add(a.group(f'<ellipse cx="258" cy="292" rx="34" ry="44" fill="none" stroke="{a.OK}" stroke-width="4"/>', a.show(p - 5, p, .5), still=0))
a.add(a.group(line(a, 306, 362, LX - 6, 362, a.OK, 3) + f'<ellipse cx="258" cy="292" rx="34" ry="44" fill="none" stroke="{a.OK}" stroke-width="4"/>', a.keyframes([(0, 0), (100, 0)]), still=1))
a.add(a.text(368, 352, "relé", 14, a.OK, a.MONO, 600, "middle"))

# servidor
a.add(card(a, 664, 214, 250, 74, "Servidor de eventos", "puerto 10000", dark=True, tsize=18))
a.add(a.box(664, 312, 250, 74, a.WHITE, a.LINE) + a.text(684, 342, "Modo Face", 18, a.INK, a.SANS, 600))
vis(a, a.text(684, 368, "Lista Blanca", 15, a.OK, a.MONO, 600), 0, 1)
vis(a, a.text(684, 368, "Lista Negra", 15, a.BAD, a.MONO, 600), 2, 3)
a.add(line(a, 789, 288, 789, 310, a.GREY, 2.5))
a.add(a.box(940, 214, 192, 284, a.WHITE, a.LINE) + a.text(956, 244, "Monitor Facial", 17, a.INK, a.SANS, 600))
a.add(line(a, 914, 251, 938, 251, a.GREY, 2.5))


def evcard(lab, fg, bg):
    return (a.box(956, 264, 160, 150, bg, fg, rx=12) + person(a, 1036, 300, .55, fill="#9DB2C6")
            + a.text(1036, 376, "Ana Ejemplo", 15, a.INK, a.SANS, 600, "middle") + a.text(1036, 400, lab, 14, fg, a.MONO, 600, "middle"))


vis(a, evcard("Permitido", a.OK, a.OKBG), 1, d0=15)
vis(a, evcard("Denegado", a.BAD, a.BADBG), 2, 3, d0=13)
vis(a, a.text(1036, 446, "sin evento nuevo", 14, a.GREY, a.MONO, 600, "middle"), 3, d0=10)

# enlace de red
a.add(line(a, 306, 252, 662, 252, "#C2D4E6", 2.5, "6 6", arrow=False))
token(a, "Action URL", [(S[1] + 2, 380, 252), (S[1] + 9, 600, 252), (S[1] + 10, 600, 252)], size=13)
token(a, "foto", [(S[1] + 10, 600, 280), (S[1] + 14, 380, 280), (S[1] + 15, 380, 280)], bg=a.BLUE, size=13)
token(a, "foto", [(S[1] + 15, 380, 280), (S[1] + 19, 600, 280), (S[1] + 20, 600, 280)], bg=a.BLUE, size=13)
token(a, "Action URL", [(S[2] + 5, 380, 252), (S[2] + 11, 600, 252), (S[2] + 12, 600, 252)], size=13)
token(a, "Action URL", [(S[3] + 6, 380, 252), (S[3] + 10, 470, 252), (S[3] + 14, 470, 252)], bg=a.GREY, size=13)
vis(a, xmark(a, 545, 252, 18) + a.text(545, 298, "sin red", 15, a.BAD, a.MONO, 600, "middle"), 3, d0=2)
vis(a, a.text(1036, 470, "la puerta ya se abrió", 14, a.BAD, a.SANS, 600, "middle"), 2, d0=14)

a.add(a.box(48, 546, 1104, 92, a.WHITE, a.LINE))
a.add(a.text(72, 582, "El Modo Face es una regla de registro, no de apertura.", 18, a.INK, a.SANS, 600))
a.add(a.text(72, 614, "Para que alguien no entre, lo que cuenta es qué caras tiene cargadas el terminal.", 17, a.TXT))
write(a, "1-t1.svg", "Dos lugares: puerta y servidor", [12, 40, 66, 90])
