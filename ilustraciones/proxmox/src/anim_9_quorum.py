"""Teoría lección 9: corosync, votos y quórum (dos nodos, corte, QDevice)."""
from _apmx import *

a = new(20, "Corosync y quórum: quién puede seguir escribiendo")
a.steps(["Dos nodos se escuchan por corosync: 2 de 2 votos.",
         "Se corta el enlace: cada uno ve 1 de 2. Ninguno tiene mayoría.",
         "Con un QDevice, el clúster espera 3 votos.",
         "Cae pve2: pve1 y el QDevice suman 2 de 3. Sigue andando."], still=3)
P1, P2, Q = (90, 220), (850, 220), (470, 440)


def nodebox(x, y, name, sub, st="up"):
    fill, stroke, col, sc = {"up": (a.INK, a.INK, "#FFFFFF", "#9FC3E3"), "down": (a.SLATE, a.LINE, a.GREY, a.GREY),
                             "qd": ("#FFFFFF", a.CYAN, a.CYAN, a.GREY)}[st]
    dash = 'stroke-dasharray="7 6"' if st == "down" else ""
    return a.box(x, y, 260, 96, fill, stroke, rx=16, sw=2.5, extra=dash) + a.text(x + 130, y + 42, name, 22, col, a.MONO, 700, "middle") + a.text(x + 130, y + 70, sub, 15, sc, a.SANS, 500, "middle")


a.add(nodebox(*P1, "pve1", "1 voto"))
at(a, nodebox(*P2, "pve2", "1 voto"), 0, 75, 0)
at(a, nodebox(*P2, "pve2", "apagado", "down"), 75, 100, 1)
at(a, nodebox(*Q, "QDevice", "corosync-qnetd · 1 voto", "qd"), 50, 100, 1)
# enlace corosync
at(a, line(a, "M350 268 H850", a.BLUE, 4), 0, 25, 0)
at(a, line(a, "M350 268 H560", a.BLUE, 4) + line(a, "M640 268 H850", a.BLUE, 4) + a.text(600, 278, "✕", 30, a.BAD, a.SANS, 700, "middle")
   + chip(a, 600, 300, "enlace cortado", "bad", anchor="middle"), 25, 50, 0)
at(a, line(a, "M350 268 H850", a.BLUE, 4), 50, 75, 0)
at(a, line(a, "M350 268 H850", a.LINE, 4, "8 8"), 75, 100, 1)
at(a, line(a, "M110 316 V488 H470", a.CYAN, 3, "8 6") + line(a, "M1090 316 V488 H730", a.CYAN, 3, "8 6"), 50, 75, 0)
at(a, line(a, "M110 316 V488 H470", a.CYAN, 3, "8 6") + line(a, "M1090 316 V488 H730", a.LINE, 3, "8 6"), 75, 100, 1)
# latidos
for s, e in [(0, 25), (50, 75)]:
    a.add(a.group(dot(a, 0, 0, 9, a.CYAN), a.move([(s, 360, 268), (s + 12, 840, 268), (e, 360, 268)]), a.show(s, e), still=0))
# estado de cada nodo
def st(x, label, kind, s, e, still=0):
    at(a, chip(a, x + 130, 334, label, kind, 16, anchor="middle", h=32), s, e, still)


st(P1[0], "2 de 2 · quórum", "ok", 0, 25)
st(P2[0], "2 de 2 · quórum", "ok", 0, 25)
st(P1[0], "1 de 2 · solo lectura", "bad", 25, 50)
st(P2[0], "1 de 2 · solo lectura", "bad", 25, 50)
st(P1[0], "3 de 3 · quórum", "ok", 50, 75)
st(P2[0], "3 de 3 · quórum", "ok", 50, 75)
st(P1[0], "2 de 3 · quórum", "ok", 75, 100, 1)
caption(a, 610, [(0, 25, "Corosync lleva los mensajes del clúster y la configuración de /etc/pve a todos los nodos.", None),
                 (25, 50, "Sin mayoría nadie escribe: es preferible quedarse quieto a que dos mitades hagan cosas distintas.", a.BAD),
                 (50, 75, "El QDevice no corre VMs: solo aporta un voto, por TCP, desde un tercer equipo.", a.CYAN),
                 (75, 100, "Con tres votos, perder uno deja mayoría. Por eso un clúster de dos nodos se entrega con QDevice.", a.OK)], still=3)
write(a, "9-t1.svg", "Corosync y quórum: quién puede seguir escribiendo",
      "Animación en cuatro tiempos. 1: pve1 y pve2 se intercambian mensajes por corosync; cada uno ve 2 de 2 votos y hay quórum. "
      "2: se corta el enlace; cada nodo ve 1 de 2 votos, ninguno tiene mayoría y los dos pasan a solo lectura. "
      "3: se suma un QDevice con corosync-qnetd en un tercer equipo; el clúster espera 3 votos y tiene 3. "
      "4: pve2 se apaga; pve1 y el QDevice suman 2 de 3 votos, mantienen el quórum y el clúster sigue andando.")
