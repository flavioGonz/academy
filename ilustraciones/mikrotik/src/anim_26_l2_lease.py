#!/usr/bin/env python3
"""Lección 26 · Laboratorio, paso 5: la cámara toma dirección, el lease aparece dinámico (D) y make-static lo
convierte en reserva para esa MAC. Fuente: DHCP (flags D dynamic, make-static: convierte un lease dinámico en estático)."""
from _anim_red_1_9 import *

a = Anim(T=24, kicker="MIKROTIK · ASIGNAR IP · LABORATORIO", title="De lease dinámico a reserva con make-static")
a.steps([
    "La cámara pide dirección y dhcp-cctv le da 10.10.20.100, del pool.",
    "En la lista de leases aparece con D: dinámico, prestado por un tiempo.",
    "make-static: la D desaparece y la dirección queda reservada para esa MAC.",
    "Se reinicie o venza el lease, esa cámara vuelve a recibir 10.10.20.100.",
], still=2)

CM, RT = 220, 900
a.add(dev(a, 48, 176, 300, 76, "Cámara", "AA:BB:CC:00:20:64", icon="camera"))
a.add(dev(a, 760, 176, 392, 76, "Router · dhcp-cctv", "ether5 · pool .100 a .199", icon="server", dark=True))
YM = 214
a.add(line(348, YM, 760, YM, a.BLUE, 4))
DORA = [("Discover", a.BLUE, 1), ("Offer", a.OK, -1), ("Request", a.BLUE, 1), ("Ack", a.OK, -1)]


def dora(t0, k=2.2):
    for i, (n, c, d) in enumerate(DORA):
        t = t0 + i * k
        p0, p1 = (420, YM) if d > 0 else (690, YM), (690, YM) if d > 0 else (420, YM)
        a.add(travel(a, pkt(a, n, c, size=15), [p0, p1], t, t + k * 0.8, hold=0.1, fade=0.3))


dora(3)
dora(80)
a.add(during(a, a.text(554, YM + 52, "10.10.20.100", 16, a.OK, a.MONO, 600, "middle"), 12, 25))
a.add(during(a, a.text(554, YM + 52, "reinicio: otra vez 10.10.20.100", 16, a.OK, a.MONO, 600, "middle"), 89, 100))

# tabla de leases
TX, TY, TW = 48, 290, 1104
a.add(a.box(TX, TY, TW, 196, a.WHITE, a.LINE, rx=16))
a.add(a.text(TX + 20, TY + 34, "/ip/dhcp-server/lease/print where server=dhcp-cctv", 16, a.INK, a.MONO, 600))
a.add(a.text(TX + 20, TY + 64, "Flags: D - dynamic", 15, a.GREY, a.MONO))
cols = [(TX + 64, "ADDRESS"), (TX + 280, "MAC-ADDRESS"), (TX + 540, "SERVER"), (TX + 720, "STATUS")]
a.add(a.box(TX + 16, TY + 80, TW - 32, 34, a.SLATE, rx=8))
for x, c in cols:
    a.add(a.text(x, TY + 103, c, 15, a.GREY, a.MONO))
RY = TY + 124
rowc = (a.text(TX + 64, RY + 30, "10.10.20.100", 16, a.INK, a.MONO, 600)
        + a.text(TX + 280, RY + 30, "AA:BB:CC:00:20:64", 16, a.INK, a.MONO, 600)
        + a.text(TX + 540, RY + 30, "dhcp-cctv", 16, a.TXT, a.MONO)
        + a.text(TX + 720, RY + 30, "bound", 16, a.OK, a.MONO, 600))
dyn = a.box(TX + 16, RY, TW - 32, 46, a.AMBBG, a.AMB, rx=8, sw=2) + a.text(TX + 34, RY + 30, "D", 17, a.AMB, a.MONO, 600) + rowc
sta = a.box(TX + 16, RY, TW - 32, 46, a.OKBG, a.OK, rx=8, sw=2) + rowc
a.add(during(a, dyn, 14, 52))
a.add(during(a, sta, 52, 100, still=1))
a.add(during(a, a.text(TX + TW - 30, RY + 30, "dinámico", 15, a.AMB, a.MONO, 600, "end"), 26, 52))
a.add(during(a, a.text(TX + TW - 30, RY + 30, "estático · reservado", 15, a.OK, a.MONO, 600, "end"), 54, 100, still=1))

# explicación y comando
a.add(during(a, note(a, 48, 508, 1104, 92, "Con D", ["Si el lease vence y se libera, la dirección vuelve al pool y la puede tomar otro equipo.", "Para una cámara que el NVR busca siempre en la misma IP, conviene reservarla."], "amb"), 26, 52))
a.add(during(a, a.box(48, 508, 1104, 92, a.INK, rx=14)
             + a.text(70, 546, "/ip/dhcp-server/lease/make-static [find address=10.10.20.100]", 16, a.WHITE, a.MONO)
             + a.text(70, 578, "La reserva queda atada a la MAC: esa cámara siempre recibe 10.10.20.100.", 16, MINT, a.SANS, 600), 52, 100, still=1))
a.add(during(a, a.text(48, 540, "Conectás la cámara (o la notebook en DHCP) a ether5 y mirás el lease.", 17, a.TXT, a.SANS, 600), 0, 26))

a.add(a.text(48, 640, "Las fijas (NVR, switches) van del .2 al .99, fuera del pool; las cámaras del pool, reservadas con make-static.", 16, a.TXT, a.SANS, 600))

write(a, 26, "l2", "Lease dinámico y reserva",
      "Animación en cuatro tiempos con una cámara (MAC AA:BB:CC:00:20:64) en ether5 y el servidor dhcp-cctv del router (pool .100 a .199). "
      "1: la cámara pide dirección con Discover, Offer, Request y Ack, y recibe 10.10.20.100. "
      "2: en /ip/dhcp-server/lease/print where server=dhcp-cctv aparece con la marca D, dinámico y bound; si vence y se libera, la dirección vuelve al pool y la puede tomar otro equipo. "
      "3: /ip/dhcp-server/lease/make-static [find address=10.10.20.100] saca la D: el lease queda estático, reservado para esa MAC. "
      "4: la cámara se reinicia, vuelve a pedir y recibe otra vez 10.10.20.100. "
      "Las IP fijas van del .2 al .99, fuera del pool.",
      [10, 36, 62, 92])
