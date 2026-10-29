#!/usr/bin/env python3
"""Lección 9 · Resumen, "Cómo se ve en la red": por qué corosync quiere su propia red. Los nodos se pasan el token de
corosync (UDP 5405-5412); si la red está cargada por un backup o el almacenamiento, el token se demora más que el
timeout y la membresía se rearma; con red propia no pasa; y un segundo enlace de menor prioridad (link1) lo sostiene
si el principal se corta.
Fuentes: guía de administración (red de clúster: latencia, NIC dedicada, no compartir con storage, protocolo de
token, timeouts, links redundantes con prioridad por Kronosnet, UDP 5405-5412)."""
from _anim_pmx_red import *

a = new(24, "Tres votos", "Corosync en su propia red: el token no espera")
a.steps([
    "Los tres nodos se pasan el token de corosync por link0, su red propia.",
    "Si corosync compartiera la red del backup, el token llega tarde.",
    "Con red propia, el backup va por su lado y corosync ni se entera.",
    "Se corta link0: knet pasa a link1, de menor prioridad, y el clúster sigue.",
], still=2)

NX = [48, 450, 852]
NY, NW, NH = 182, 300, 84
A_Y, B_Y = 352, 452
DROP = [x + 120 for x in NX]
for x in DROP:
    a.add(line(x - 40, NY + NH, x - 40, A_Y - 22, a.BLUE, 3))
    a.add(line(x + 40, NY + NH, x + 40, B_Y - 22, a.GREY, 3))
for i, x in enumerate(NX):
    a.add(dev(a, x, NY, NW, NH, f"pve{i + 1} · 1 voto", "", icon="server", dark=True, tsize=19))
# buses
a.add(a.box(48, A_Y - 22, 1104, 44, a.WHITE, a.LINE, rx=12))
a.add(a.text(66, A_Y + 6, "link0 · switch de corosync", 15, a.BLUE, a.MONO, 700))
a.add(a.text(1134, A_Y + 6, "UDP 5405-5412 · < 5 ms", 15, a.GREY, a.MONO, 400, "end"))
a.add(a.box(48, B_Y - 22, 1104, 44, a.WHITE, a.LINE, rx=12))
a.add(a.text(66, B_Y + 6, "red de VMs y backups", 15, a.TXT, a.MONO, 700))
at(a, a.text(1134, B_Y + 6, "link1 · prioridad menor", 15, a.AMB, a.MONO, 600, "end"), 75, 100)
# PBS en la red de backups
a.add(dev(a, 820, 500, 332, 76, "PBS", "backup nocturno en curso", icon="shield", tsize=18))
a.add(line(986, B_Y + 22, 986, 500, a.GREY, 3))
# corte de link0 (paso 4)
at(a, a.box(40, A_Y - 26, 1120, 52, a.BG, rx=12, extra='opacity=".75"') + xmark(a, 600, A_Y, 17) + a.text(630, A_Y + 6, "link0 cortado", 16, a.BAD, a.SANS, 700), 76, 100)


def token(bus_y, t0, t1, color, laps=1, delay=None):
    xs = [DROP[0] - 40, DROP[1] - 40, DROP[2] - 40] if bus_y == A_Y else [DROP[0] + 40, DROP[1] + 40, DROP[2] + 40]
    pts = []
    for _ in range(laps):
        pts += [(xs[0], NY + NH), (xs[0], bus_y), (xs[1], bus_y), (xs[1], NY + NH), (xs[1], bus_y), (xs[2], bus_y), (xs[2], NY + NH), (xs[2], bus_y), (xs[0], bus_y)]
    pts.append((xs[0], NY + NH))
    a.add(travel(a, pkt(a, "token", color, size=15), pts, t0, t1, hold=0.3))


token(A_Y, 2, 23, a.BLUE, laps=2)
# 2 · red compartida: tráfico de backup y token demorado
for k in range(16):
    t = 26 + k * 1.4
    a.add(travel(a, a.box(-14, -9, 28, 18, a.CYAN, rx=4), [(986, B_Y), (DROP[k % 3] + 40, B_Y)], t, t + 3, hold=0.1, fade=0.2))
a.add(travel(a, pkt(a, "token", a.AMB, size=15), [(DROP[0] + 40, NY + NH), (DROP[0] + 40, B_Y), (DROP[1] + 40 - 160, B_Y)], 27, 36, hold=14))
at(a, chip(a, DROP[1] - 200, B_Y + 32, "token demorado > timeout", "bad"), 37, 50)
for x in NX:
    at(a, chip(a, x + 62, NY + 46, "membresía se rearma", "bad", h=26, size=14), 41, 50)
at(a, a.box(48, A_Y - 22, 1104, 44, a.SLATE, rx=12) + a.text(66, A_Y + 6, "(si corosync no tuviera red propia)", 15, a.GREY, a.MONO), 25, 50)
# 3 · backup en su red, token por link0
for k in range(16):
    t = 52 + k * 1.4
    a.add(travel(a, a.box(-14, -9, 28, 18, a.CYAN, rx=4), [(986, B_Y), (DROP[k % 3] + 40, B_Y)], t, t + 3, hold=0.1, fade=0.2))
token(A_Y, 52, 73, a.OK, laps=2)
for x in NX:
    at(a, chip(a, x + 62, NY + 46, "3 de 3 · quórum", "ok", h=26, size=14), 52, 75, still=1)
# 4 · link1
token(B_Y, 78, 98, a.AMB, laps=1)
for x in NX:
    at(a, chip(a, x + 62, NY + 46, "3 de 3 · por link1", "amb", h=26, size=14), 80, 100)

status(a, 628, [
    (0, 25, "Corosync usa poco ancho de banda, pero necesita que cada mensaje llegue rápido y siempre igual.", a.INK, 0),
    (25, 50, "Si el token tarda más que el timeout, un nodo cree que perdió a los otros aunque estén vivos.", a.BAD, 0),
    (50, 75, "Una placa de 1 Gbit dedicada alcanza: lo que importa es que nadie le robe el lugar.", a.OK, 1),
    (75, 100, "La red de VMs como link1 de baja prioridad: más lenta, pero mejor que no tener conexión.", a.AMB, 0),
], size=17)

write(a, 9, "r1", "Corosync en su propia red: el token no espera",
      "Animación en cuatro tiempos con tres nodos, pve1, pve2 y pve3, de un voto cada uno, conectados a dos redes: link0, el switch de corosync con UDP 5405 a 5412 y latencia menor a 5 ms, y la red de VMs y backups, donde un PBS está haciendo el backup nocturno. "
      "1: los tres nodos se pasan el token de corosync por link0, una y otra vez. "
      "2: si corosync compartiera la red del backup, el tráfico del backup demora el token más que el timeout; cada nodo cree que perdió a los otros aunque estén vivos y la membresía del clúster se rearma. "
      "3: con red propia, el backup va por la red de VMs y el token sigue circulando por link0 sin demoras: los tres nodos ven 3 de 3 votos y hay quórum. "
      "4: se corta link0; como la red de VMs está configurada como link1, de prioridad menor, Kronosnet pasa el tráfico de corosync a link1 y el clúster sigue con 3 de 3.",
      [10, 40, 48, 66, 90])
