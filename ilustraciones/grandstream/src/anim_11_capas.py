#!/usr/bin/env python3
"""Lección 11 · teoría: cada intento muere en una capa distinta (router, Geo-IP, Fail2ban, rutas)."""
from _anim_grandstream import G

g = G(T=28, fix=97, kicker="GRANDSTREAM · CENTRAL CERRADA", title="Cada intento se frena en una capa distinta")
g.steps([
    "Prueban SSH desde internet: el router no tiene ese puerto abierto.",
    "Llega un REGISTER desde un país que no se usa: Geo-IP lo descarta.",
    "Un barrido falla REGISTER una y otra vez: Fail2ban banea esa IP 600 s.",
    "Con una extensión robada llaman al exterior: privilegio y PIN lo frenan.",
])

GX = {"router": 420, "geo": 600, "f2b": 780, "rutas": 990}
LAB = {"router": ("Router", "solo puertos con motivo"), "geo": ("Geo-IP", "países que se usan"),
       "f2b": ("Fail2ban", "banea al que insiste"), "rutas": ("Rutas", "privilegio y PIN")}
for k, x in GX.items():
    t, sub = LAB[k]
    g.add(g.box(x - 13, 232, 26, 352, g.SLATE, g.LINE, rx=13, sw=1.5))
    g.add(g.text(x, 196, t, 18, g.INK, g.HEAD, 600, "middle"))
    g.add(g.text(x, 218, sub, 13, g.GREY, g.MONO, 400, "middle"))
g.add(g.node(1060, 380, 92, 64, "UCM", dark=True, tsize=18))

ROWS = [270, 350, 430, 520]
SRC = [("SSH :22", "desde internet"), ("REGISTER", "desde otro país"), ("REGISTER", "barrido de claves"), ("INVITE 00…", "extensión robada")]
for (a, b), y in zip(SRC, ROWS):
    g.add(g.text(48, y - 2, a, 17, g.INK, g.MONO, 600) + g.text(48, y + 20, b, 14, g.GREY, g.SANS))
    g.add(f'<line x1="210" y1="{y}" x2="1050" y2="{y}" stroke="{g.LINE}" stroke-width="1.5" stroke-dasharray="3 7"/>')


def attempt(row, gate, t0, t1, label, col=g.BAD, after=100, note=None):
    y = ROWS[row]
    gx = GX[gate] - 34
    g.token([(230, y), (gx, y)], t0, t1, g.chip(label, bg=col, size=13, h=24), hold=t1 + 1.5)
    g.appear(g.mark(GX[gate] + 34, y, False, 14), t1, after)
    if note:
        g.appear(g.text(GX[gate] + 56, y + 5, note, 14, g.BAD, g.MONO, 600), t1, after)


attempt(0, "router", 3, 11, "SSH", note="cerrado")
attempt(1, "geo", 28, 37, "REGISTER", note="país bloqueado")
# barrido: tres fallas y el baneo
y = ROWS[2]
for k, t in enumerate([52, 56.5, 61]):
    g.token([(230, y), (GX["f2b"] - 34, y)], t, t + 3.5, g.chip(f"falla {k + 1}", bg=g.AMB, size=13, h=24), hold=t + 4)
g.appear(g.box(GX["f2b"] - 13, ROWS[2] - 26, 26, 52, g.BAD, None, rx=13), 66, 100)
attempt(2, "f2b", 67, 72, "REGISTER", note="baneada 600 s")
# extensión robada: pasa todo, frena en rutas
y = ROWS[3]
g.token([(230, y), (GX["rutas"] - 34, y)], 78, 90, g.chip("INVITE 00…", bg=g.BLUE, size=13, h=24), hold=91.5)
g.appear(g.mark(GX["rutas"] + 34, y, False, 14), 90, 100)
g.appear(g.text(GX["rutas"], y + 48, "nivel bajo, sin PIN", 14, g.BAD, g.MONO, 600, "middle"), 90, 100)
for k in ("router", "geo", "f2b"):
    g.appear(g.mark(GX[k], y - 26, True, 10), 80 + list(GX).index(k) * 3, 100)

g.fijo_only("".join(f'<g transform="translate({x} {yy})">' + g.chip(l, bg=c, size=13, h=24) + "</g>"
                    for x, yy, l, c in [(GX["router"] - 50, ROWS[0], "SSH", g.BAD), (GX["geo"] - 66, ROWS[1], "REGISTER", g.BAD),
                                        (GX["f2b"] - 66, ROWS[2], "REGISTER", g.BAD), (GX["rutas"] - 76, ROWS[3], "INVITE 00…", g.BLUE)]))

g.add(g.note(48, 600, 1104, None, ["Y la administración aparte: web solo para la lista blanca (hasta 10 IPs), 5 fallos de login son 5 minutos afuera, SSH y AMI apagados."], "info"))

g.finish(11, 1, "Cada intento se frena en una capa distinta",
         "Animación en cuatro tiempos con cuatro capas en columnas, de afuera hacia adentro: router, que solo abre puertos con motivo; Geo-IP, que deja pasar solo los países que se usan; Fail2ban, que banea al que insiste; y rutas, con privilegio y PIN; al final, la UCM. "
         "1: alguien prueba SSH, puerto 22, desde internet y se frena en el router: el puerto está cerrado. "
         "2: llega un REGISTER desde un país que no se usa y Geo-IP lo descarta. "
         "3: un barrido falla REGISTER tres veces seguidas; Fail2ban banea esa IP 600 segundos y el siguiente intento ya no pasa. "
         "4: con una extensión robada, un INVITE a un número internacional pasa router, Geo-IP y Fail2ban, pero la ruta lo frena: el nivel de la extensión no alcanza y no tiene el PIN. "
         "Nota: la administración va aparte: web solo para la lista blanca, de hasta 10 IPs; 5 fallos de login son 5 minutos de bloqueo; SSH y AMI apagados.",
         [9, 34, 62, 97])
