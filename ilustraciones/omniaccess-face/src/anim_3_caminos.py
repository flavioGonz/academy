"""Teoría de El terminal avisa: dos caminos de red, uno de ida (aviso) y uno de vuelta (foto y Relé)."""
from _anim_face import *

caps = ["Los dos caminos andan: el aviso llega y el servidor trae la foto.",
        "Se corta el aviso (terminal → servidor): no llega nada.",
        "Se corta la vuelta (servidor → terminal): evento sin foto y Relé que no responde."]
a = new(21, "Dos caminos", "Dos caminos de red: ida para el aviso, vuelta para la foto", caps, still=2, size=17)
S = [sp[0] for sp in a.spans]

a.add(terminal(a, 70, 206, w=110, h=170, label="Terminal facial"))
a.add(a.text(125, 428, "192.0.2.21", 15, a.GREY, a.MONO, 600, "middle"))
a.add(card(a, 880, 206, 272, 84, "Servidor de eventos", "192.0.2.10 · puerto 10000", dark=True, tsize=18))
A_Y, B_Y = 228, 276
a.add(line(a, 190, A_Y, 874, A_Y, a.BLUE, 3))
a.add(a.text(220, A_Y - 14, "IDA · aviso por Action URL", 16, a.BLUE, a.SANS, 600))
a.add(line(a, 874, B_Y, 190, B_Y, a.CYAN, 3, "8 6"))
a.add(a.text(220, B_Y + 30, "VUELTA · foto del registro y botón Relé", 16, "#0B7FA3", a.SANS, 600))
a.add(a.text(220, B_Y + 54, "con el usuario y la clave de la API del equipo", 15, a.GREY, a.MONO))
a.add(line(a, 1016, 290, 1016, 316, a.GREY, 2.5))

# monitor
MX, MY = 880, 320
a.add(a.box(MX, MY, 272, 200, a.WHITE, a.LINE) + a.text(MX + 16, MY + 28, "Monitor Facial", 16, a.INK, a.SANS, 600))
vis(a, a.box(MX + 16, MY + 44, 240, 110, a.OKBG, a.OK, rx=10) + person(a, MX + 66, MY + 78, .5, fill="#9DB2C6")
    + a.text(MX + 110, MY + 90, "Ana Ejemplo", 15, a.INK, a.SANS, 600) + a.text(MX + 110, MY + 114, "con foto", 14, a.OK, a.MONO, 600), 0, d0=12)
vis(a, a.text(MX + 136, MY + 104, "no llega nada", 17, a.BAD, a.SANS, 600, "middle"), 1, d0=6)
vis(a, a.box(MX + 16, MY + 44, 240, 110, a.WHITE, a.AMB, rx=10) + a.box(MX + 30, MY + 58, 72, 82, a.SLATE, rx=6)
    + a.text(MX + 66, MY + 104, "?", 26, a.GREY, a.MONO, 600, "middle")
    + a.text(MX + 116, MY + 90, "Ana Ejemplo", 15, a.INK, a.SANS, 600) + a.text(MX + 116, MY + 114, "sin foto", 14, a.AMB, a.MONO, 600)
    + a.pill(MX + 16, MY + 162, "Relé · no responde", a.GREY, a.SLATE, size=13), 2, d0=8)

# fichas que viajan
for st in (0, 2):
    token(a, "aviso", [(S[st] + 2, 260, A_Y), (S[st] + 8, 800, A_Y), (S[st] + 9, 800, A_Y)], size=13)
token(a, "foto", [(S[0] + 9, 800, B_Y), (S[0] + 14, 260, B_Y), (S[0] + 15, 260, B_Y)], bg=a.CYAN, size=13)
token(a, "foto", [(S[0] + 15, 260, B_Y), (S[0] + 20, 800, B_Y), (S[0] + 21, 800, B_Y)], bg=a.CYAN, size=13)
token(a, "aviso", [(S[1] + 2, 260, A_Y), (S[1] + 5, 500, A_Y), (S[1] + 9, 500, A_Y)], bg=a.GREY, size=13)
token(a, "foto", [(S[2] + 9, 800, B_Y), (S[2] + 12, 600, B_Y), (S[2] + 16, 600, B_Y)], bg=a.GREY, size=13)
vis(a, xmark(a, 560, A_Y, 18), 1, d0=3)
vis(a, xmark(a, 540, B_Y, 18), 2, d0=8)

# qué revisar
a.add(a.box(48, 546, 1104, 92, a.WHITE, a.LINE))
a.add(a.text(72, 580, "Qué revisar", 18, a.INK, a.SANS, 600))
vis(a, a.text(72, 612, "Nada: el evento aparece con su foto en el monitor.", 17, a.OK, a.SANS, 600), 0, d0=12)
vis(a, a.text(72, 612, "La URL al puerto 10000, el firewall y que la MAC del aviso sea la de la ficha del equipo.", 17, a.TXT), 1, d0=6)
vis(a, a.text(72, 612, "El usuario y la clave de la API del terminal, y que el servidor llegue al equipo por la red.", 17, a.TXT), 2, d0=8)
write(a, "3-t2.svg", "Dos caminos de red", [17, 45, 85])
