#!/usr/bin/env python3
"""Lección 7 · Laboratorio, paso 1: AirView > Environment o Airtime Scan. Con el escaneo Full la radio deja de atender
a sus clientes, recorre los canales y mide cuánto aire usan los vecinos; al terminar vuelve y los clientes reconectan.
Los valores de las barras son ilustrativos, con el patrón del caso de std.rocks (36 a 48 saturados, 52 a 64 más
limpios). Fuentes: lab.md (paso 1 y aviso) y la ilustración 7-paso1 de la lección."""
from _anim_red_unifi import *  # noqa

a = new(24, "Canales angostos", "Airtime Scan: la radio deja de atender para escuchar", [
    "Antes del escaneo, la radio de 5 GHz atiende a sus clientes en su canal.",
    "Scan Full: la radio deja a sus clientes y salta de canal en canal.",
    "En cada canal mide cuánto aire ocupan los vecinos.",
    "Termina: la radio vuelve, los clientes reconectan y tenés el mapa.",
], still=3, paso=1)

# AP y clientes
a.add(dev(a, 48, 190, 280, 90, "AP · radio 5 GHz", "canal 44 · 40 MHz", ap=True))
PH = [(108, 420), (188, 440), (268, 420)]
for x, y in PH:
    a.add(phone_icon(a, x, y))
for i, (x, y) in enumerate(PH):
    vis(a, poly([(188, 280), (x, y - 24)], a.OK, 2.5, "5 5"), 0)
    vis(a, poly([(188, 280), (x, y - 24)], a.OK, 2.5, "5 5"), 3)
    vis(a, xmark(a, x, y - 40, 12), 1, 2)
vis(a, pill(a, 188, 486, "clientes conectados", "ok", anchor="middle"), 0)
vis(a, pill(a, 188, 486, "clientes desconectados", "bad", anchor="middle"), 1, 2)
vis(a, pill(a, 188, 486, "reconectan", "ok", anchor="middle"), 3)

# gráfico de canales
CH = [36, 40, 44, 48, 52, 56, 60, 64]
USE = [0.82, 0.74, 0.88, 0.70, 0.22, 0.16, 0.26, 0.14]
GX, GY, GW, GH = 420, 200, 732, 250
a.add(a.box(GX, GY - 10, GW, GH + 80, a.WHITE, a.LINE, rx=14))
a.add(a.text(GX + 20, GY + 22, "uso de aire por canal (ilustrativo)", 15, a.GREY, a.MONO))
BW, X0, BASE = 62, GX + 40, GY + GH - 10
a.add(wire(GX + 24, BASE, GX + GW - 24, BASE, a.INK, 2))
for i, (c, u) in enumerate(zip(CH, USE)):
    x = X0 + i * 84
    a.add(a.text(x + BW / 2, BASE + 28, str(c), 16, a.INK, a.MONO, 600, "middle"))
    h = u * 190
    col = a.BAD if u > 0.5 else a.OK
    bar = a.box(x, BASE - h, BW, h, col, None, rx=6, extra='fill-opacity=".8"')
    t = ph(a, 1)[0] + 3 + i * 4.2
    during(a, bar, t + 2, 100, still=1)
a.add(a.text(X0 + 1.5 * 84 + BW / 2, BASE + 56, "sin DFS", 15, a.GREY, a.SANS, 400, "middle"))
a.add(a.text(X0 + 5.5 * 84 + BW / 2, BASE + 56, "DFS", 15, a.GREY, a.SANS, 400, "middle"))
# la radio que salta
s0 = ph(a, 1)[0]
kf = [(0, X0 + BW / 2, GY + 52)]
for i in range(len(CH)):
    t = s0 + 3 + i * 4.2
    kf += [(t, X0 + i * 84 + BW / 2, GY + 52), (t + 3.6, X0 + i * 84 + BW / 2, GY + 52)]
kf.append((100, X0 + 7 * 84 + BW / 2, GY + 52))
ear = a.box(-38, -15, 76, 30, a.INK, None, rx=15) + a.text(0, 6, "escucha", 15, a.WHITE, a.MONO, 600, "middle")
a.add(a.group(ear, a.move(kf), a.show(s0 + 2.5, s0 + 3 + 8 * 4.2, 0.5), still=0))

vis(a, a.text(GX + GW / 2, BASE - 120, "la radio está en su canal: no se mide nada", 16, a.GREY, a.SANS, 600, "middle"), 0)
s0, s1 = ph(a, 3)
during(a, nbox(a, 420, 536, 732, 64, "", ["36 a 48 saturados, 52 a 64 más limpios: con esto se fija el ancho y se eligen canales."], "info"),
       s0 + 2, 100, still=1)

status(a, 640, [
    (0, 25, "Si el AP tiene análisis en tiempo real, Environment ya lo muestra sin cortar.", a.INK, 0),
    (25, 50, "Una radio no puede atender y escuchar otros canales a la vez.", a.BAD, 0),
    (50, 75, "Lo que se mide es el aire ocupado, tuyo y de los vecinos.", a.INK, 0),
    (75, 100, "El escaneo Full desconecta a los clientes de esa radio: fuera de horario.", a.AMB, 1),
])

write(a, 7, "l1", "Airtime Scan en el AP",
      "Animación en cuatro tiempos del paso 1 con un AP cuya radio de 5 GHz está en el canal 44 a 40 MHz, tres celulares conectados y un gráfico ilustrativo de uso de aire en los canales 36 a 64. "
      "1: antes del escaneo, la radio atiende a sus clientes en su canal y no mide nada. "
      "2: con el Airtime Scan Full la radio deja a sus clientes, que quedan desconectados, y salta de canal en canal escuchando. "
      "3: en cada canal mide cuánto aire ocupan los vecinos; en el ejemplo, 36 a 48 sin DFS saturados y 52 a 64, que son DFS, más limpios, como en el caso de std.rocks. "
      "4: termina el escaneo, la radio vuelve y los clientes reconectan; con ese mapa se fija el ancho y se eligen canales. "
      "Si el AP tiene análisis en tiempo real, AirView > Environment lo muestra sin cortar; el escaneo Full se hace fuera de horario.",
      [12, 37, 64, 92])
