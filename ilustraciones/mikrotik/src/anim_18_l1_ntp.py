#!/usr/bin/env python3
"""Lección 18 (Cloud a fondo) · Laboratorio paso 3: la hora aproximada de la nube contra el intercambio NTP con sus cuatro tiempos."""
from _anim_r20_31 import *

a, _ = nuevo(26, "MIKROTIK · CLOUD A FONDO · PASO 3", "Hora de la nube o hora de NTP",
             ["Sin NTP, al arrancar el router toma una hora aproximada de la nube.",
              "Con NTP, el router anota T1 al preguntar; el servidor, T2 y T3.",
              "La respuesta llega en T4: con los cuatro tiempos sale la demora y el desfase.",
              "El reloj queda preciso para logs e IPsec. Y update-time=no."], still=2)

XR, XC, XN = 190, 600, 1010
head(a, XR, 178, "Router", "/system/ntp/client", w=260, kind="router")
head(a, XC, 178, "IP Cloud", "update-time", w=240, kind="cloud")
head(a, XN, 178, "pool.ntp.org", "servidor NTP", w=260, kind="isp")
for x in (XR, XC, XN):
    lifeline(a, x, 248, 462)

# reloj del router
a.add(a.box(48, 478, 284, 108, a.INK, rx=14))
a.add(a.text(66, 506, "reloj del router", 14, SKY, a.MONO))
flip(a, 66, 550, [(0, 6, "sin hora", ROSE), (6, 30, "≈ aproximada", GOLD), (30, 66, "≈ aproximada", GOLD), (66, 100, "ajustado", MINT)], size=24, still_idx=3)

# 1. nube
en(a, a.pill(XR + 16, 262, "arranca · NTP apagado", a.AMB, a.AMBBG, 13, 26), 1, 25)
msg(a, XC, XR, 316, "hora aproximada", 3, 25, a.AMB)

# 2 y 3: NTP con flechas inclinadas
def sloped(x1, y1, x2, y2, label, t0, t1, end, c, still=0):
    d = f"M{x1} {y1} L{x2 - (8 if x2 > x1 else -8)} {y2 - 1}"
    en(a, a.arrow(d, c, 3) + a.text((x1 + x2) / 2, (y1 + y2) / 2 - 14, label, 15, c, a.MONO, 600, "middle"), t0 + (t1 - t0) * .6, end, still)
    go(a, "", [(x1, y1), (x2, y2)], t0, t1, hold=0.2, inner=f'<circle r="8" fill="{c}"/>')

def tmark(x, y, lab, t0, end, c, right=True, still=0):
    en(a, f'<circle cx="{x}" cy="{y}" r="6" fill="{c}"/>' + a.text(x + (14 if right else -14), y + 6, lab, 17, c, a.MONO, 600, "start" if right else "end"), t0, end, still)

sloped(XR, 290, XN, 340, "consulta NTP", 28, 36, 100, a.BLUE, still=1)
tmark(XR, 290, "T1", 28, 100, a.BLUE, right=False, still=1)
tmark(XN, 340, "T2", 36, 100, a.BLUE, still=1)
tmark(XN, 380, "T3", 42, 100, a.OK, still=1)
sloped(XN, 380, XR, 430, "respuesta: T1, T2, T3", 44, 52, 100, a.OK, still=1)
tmark(XR, 430, "T4", 53, 100, a.OK, right=False, still=1)

en(a, a.box(372, 478, 780, 108, a.WHITE, a.LINE, rx=14)
   + a.text(392, 512, "demora  = (T4 − T1) − (T3 − T2)", 17, a.INK, a.MONO, 600)
   + a.text(392, 546, "desfase = ((T2 − T1) + (T3 − T4)) / 2", 17, a.INK, a.MONO, 600)
   + a.text(392, 574, "el viaje de ida y vuelta se descuenta: no adelanta ni atrasa", 14, a.TXT, a.SANS), 54, 75, still=1)
en(a, term(a, 372, 478, 780, ["/system/ntp/client/set enabled=yes servers=pool.ntp.org", "/system/ntp/client/print", "/ip/cloud/set update-time=no"], size=15, lh=24, colors={2: GOLD}), 76, 100)

narr(a, [
    (0, 25, "update-time solo actúa si el cliente NTP está apagado, y la hora es aproximada.", a.AMB),
    (25, 50, "Cada mensaje NTP lleva las marcas de tiempo de quien lo manda.", a.TXT),
    (50, 75, "NTP mide la ida y vuelta y la descuenta: por eso es preciso.", a.OK),
    (75, 100, "Logs con hora correcta y SA de IPsec que no se caen por reloj.", a.OK),
], still_idx=2)

escribir(a, "18-l1.svg", "Hora con NTP",
         "Animación en cuatro tiempos con tres líneas de vida: el router con su cliente NTP, IP Cloud con update-time y el servidor pool.ntp.org. Abajo a la izquierda, el reloj del router. "
         "1: al arrancar, con el cliente NTP apagado, el router toma una hora aproximada de la nube. 2: con NTP, el router manda la consulta y anota T1; el servidor anota T2 al recibirla y T3 al contestar. "
         "3: la respuesta llega al router en T4, y con los cuatro tiempos calcula la demora, (T4 − T1) − (T3 − T2), y el desfase, ((T2 − T1) + (T3 − T4)) / 2: el viaje de ida y vuelta se descuenta. "
         "4: el reloj queda ajustado, con los comandos del paso 3: cliente NTP con pool.ntp.org y update-time=no.",
         [12, 40, 62, 70, 92])
