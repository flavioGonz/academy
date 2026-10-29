#!/usr/bin/env python3
"""Lección 6 · Laboratorio, paso 1: el ARP antes del primer ping al gateway. Sin entrada en ip neigh, el servidor
pregunta por broadcast quién tiene 192.168.88.1; todos los equipos de la LAN lo reciben y solo el router contesta,
directo, con su MAC. La entrada queda en ip neigh (REACHABLE) y sale el echo request. Para 1.1.1.1 la IP de destino
cambia pero la MAC de destino sigue siendo la del gateway. Fuentes: RFC 826 (ARP), ip-neighbour(8) (estados),
teoría y laboratorio de la lección (ip neigh, ping al gateway y a 1.1.1.1). MAC de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · RED · LABORATORIO", "Antes del primer ping: ARP busca la MAC del gateway")
a.steps([
    "ip neigh no tiene al gateway: el servidor pregunta por broadcast.",
    "Todos lo reciben; solo 192.168.88.1 contesta, directo, con su MAC.",
    "ip neigh guarda la MAC y sale el echo request al gateway.",
    "Para 1.1.1.1 cambia la IP de destino; la MAC sigue siendo la del gateway.",
], still=3)

BUS = 318
a.add(camino(f"M70 {BUS} H1130", "#C2D4E6", 6) + a.text(1130, BUS + 26, "LAN 192.168.88.0/24", 14, a.GREY, a.MONO, 600, "end"))
DEV = {"srv": (60, "Servidor", ".88.50 · 52:54:00:12:34:56", "server", True),
       "cam": (452, "Cámara", ".88.30", "camera", False),
       "rtr": (830, "Router", ".88.1 · 02:00:00:aa:bb:01", "shield", False)}
CXs = {}
for k, (x, t, s, ic, dk) in DEV.items():
    w = {"srv": 310, "cam": 230, "rtr": 290}[k]
    a.add(dev(a, x, 176, w, 80, t, s, ic, dark=dk, ssize=14))
    cx = x + w / 2
    CXs[k] = cx
    a.add(camino(f"M{cx} 256 V{BUS}", "#C2D4E6", 4))
# salida a internet desde el router
a.add(camino(f"M{CXs['rtr'] + 145} 216 H1190", "#C2D4E6", 3, "6 6"))
a.add(a.text(1192, 204, "internet", 14, a.GREY, a.MONO, 600, "end"))

S, C, R = CXs["srv"], CXs["cam"], CXs["rtr"]
dotc = lambda col: f'<circle r="10" fill="{col}" stroke="#FFFFFF" stroke-width="3"/>'
# 1 broadcast
viaje(a, "", [(S, 262), (S, BUS)], 3, 6, inner=dotc(a.AMB), hold=0)
viaje(a, "", [(S, BUS), (C, BUS), (C, 262)], 6, 14, inner=dotc(a.AMB), hold=1)
viaje(a, "", [(S, BUS), (R, BUS), (R, 262)], 6, 18, inner=dotc(a.AMB), hold=1)
en(a, a.pill(C + 14, 270, "no es para mí", a.GREY, a.SLATE, 14, 28), 15, 50)
# 2 respuesta unicast
viaje(a, "", [(R, 262), (R, BUS), (S, BUS), (S, 262)], 28, 40, inner=dotc(a.OK), hold=1)
# 3 echo al gateway
viaje(a, "", [(S, 262), (S, BUS), (R, BUS), (R, 262)], 56, 66, inner=dotc(a.BLUE), hold=1)
# 4 echo a 1.1.1.1 vía router
viaje(a, "", [(S, 262), (S, BUS), (R, BUS), (R, 262), (R + 145, 216), (1186, 216)], 78, 94, inner=dotc(a.BLUE), hold=2)
fijo(a, place(dotc(a.BLUE), R, BUS))

# trama actual
FY = 350
a.add(a.text(48, FY + 18, "la trama en el cable", 15, a.GREY, a.SANS, 600))
COLS = [(48, 250, "MAC destino"), (308, 250, "MAC origen"), (568, 584, "qué lleva")]
for x, w, h in COLS:
    a.add(a.box(x, FY + 30, w, 84, a.WHITE, a.LINE, rx=10) + a.text(x + 14, FY + 54, h, 14, a.GREY, a.MONO, 600))


def trama(t0, t1, d, o, q, q2, col, still=0):
    s = (mono(a, 62, FY + 88, d, 15, col, 700) + mono(a, 322, FY + 88, o, 15, a.INK, 600)
         + a.text(582, FY + 80, q, 15, col, a.SANS, 700) + a.text(582, FY + 104, q2, 15, a.TXT, a.SANS, 500))
    en(a, s, t0, t1, still)


trama(0, 25, "ff:ff:ff:ff:ff:ff", "52:54:00:12:34:56", "ARP request (broadcast)", "¿quién tiene 192.168.88.1? avisale a .88.50", a.AMB)
trama(25, 50, "52:54:00:12:34:56", "02:00:00:aa:bb:01", "ARP reply (directo al que preguntó)", "192.168.88.1 está en 02:00:00:aa:bb:01", a.OK)
trama(50, 75, "02:00:00:aa:bb:01", "52:54:00:12:34:56", "ICMP echo request", "IP destino 192.168.88.1", a.BLUE)
trama(75, 100, "02:00:00:aa:bb:01", "52:54:00:12:34:56", "ICMP echo request", "IP destino 1.1.1.1: el router la reenvía", a.BLUE, still=1)
en(a, a.box(44, FY + 26, 258, 92, "none", GOLD, rx=12, sw=3), 78, 100, still=1)

# ip neigh
TY = 478
a.add(tterm(a, 48, TY, 1104, 92))
en(a, trow(a, 48, TY + 34, "$ ip neigh", 15) + trow(a, 48, TY + 62, ("(sin entrada para 192.168.88.1)", T_COM), 15), 0, 40)
en(a, trow(a, 48, TY + 34, "$ ip neigh", 15) + trow(a, 48, TY + 62, ("192.168.88.1 dev ens18 lladdr 02:00:00:aa:bb:01 REACHABLE", T_OK), 15), 40, 100, still=1)

narr(a, [
    (0, 25, "Para mandar una trama en la LAN hace falta la MAC: la IP sola no alcanza.", None),
    (25, 50, "La cámara recibe la pregunta y la descarta; el router contesta solo al servidor.", a.OK),
    (50, 75, "Con la MAC en la tabla, los pings siguientes salen sin preguntar.", None),
    (75, 100, "Todo lo que va afuera de la LAN se le entrega al gateway: por eso su MAC.", a.AMB),
], y=606, still_idx=3)
a.add(a.text(48, 636, "MAC de ejemplo.", 15, a.GREY, a.SANS, 500))

escribir(a, "6-l1", "Antes del primer ping: ARP busca la MAC del gateway",
         "Animación en cuatro tiempos con una LAN 192.168.88.0/24: el servidor .88.50 con MAC 52:54:00:12:34:56, una cámara .88.30 y el router .88.1 con MAC 02:00:00:aa:bb:01, que sale a internet. "
         "Debajo, la trama que viaja, con MAC destino, MAC origen y qué lleva, y la salida de ip neigh. "
         "1: ip neigh no tiene al gateway y el servidor manda un ARP request a ff:ff:ff:ff:ff:ff: ¿quién tiene 192.168.88.1? "
         "2: la cámara lo recibe y lo descarta; el router contesta con un ARP reply directo al servidor: 192.168.88.1 está en 02:00:00:aa:bb:01. "
         "3: ip neigh muestra 192.168.88.1 dev ens18 lladdr 02:00:00:aa:bb:01 REACHABLE y sale el echo request con la MAC del router. "
         "4: el ping a 1.1.1.1 lleva IP destino 1.1.1.1, pero la MAC destino sigue siendo la del gateway, que lo reenvía a internet.",
         [10, 36, 62, 90])
