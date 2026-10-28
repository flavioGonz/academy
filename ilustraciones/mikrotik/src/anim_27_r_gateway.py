#!/usr/bin/env python3
"""Lección 27 (Rutas estáticas), Resumen: cómo se ve en la red. El gateway es a quién se le pasa el paquete:
la tabla elige la ruta más específica, el próximo salto se resuelve por la red conectada (ARP) y la IP destino no cambia."""
from _anims_10_19 import Anim, en, fijo, dev, viaje, linea, narr, panel, escribir, pill_c, place, LIGHT, GOLD, MINT, GHOST

a = Anim(T=24, kicker="MIKROTIK · RUTAS ESTÁTICAS · EN LA RED", title="El gateway es a quién le pasás el paquete")
a.steps([
    "La PC quiere llegar a 10.20.30.5: no es su red, se lo da al router.",
    "El router busca: coinciden dos rutas y gana la más específica.",
    "El gateway .250 está en el bridge: ARP y el paquete sale hacia él.",
    "Un paquete a 8.8.8.8 solo coincide con 0.0.0.0/0: sale por ether1.",
], still=2)

# ---- topología
a.add(dev(a, 48, 244, 226, 84, "PC de la oficina", "192.168.88.20", "laptop"))
a.add(a.box(424, 200, 212, 112, a.INK, a.INK, rx=16) + a.text(446, 236, "Router", 19, "#FFFFFF", a.SANS, 600)
      + a.text(446, 259, "192.168.88.1", 15, LIGHT, a.MONO))
a.add(dev(a, 862, 166, 290, 92, "Router del depósito", "192.168.88.250 · LAN", "server", sub2="atrás: 10.20.30.0/24"))
a.add(dev(a, 862, 270, 290, 92, "Proveedor", "gw 203.0.113.1", "globe", sub2="atrás: internet"))
a.add(linea(274, 286, 424, 286, a.LINE, 4))
a.add(linea(636, 236, 862, 212, a.LINE, 4))
a.add(linea(636, 290, 862, 316, a.LINE, 4))
a.add(a.text(349, 314, "bridge", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text(700, 328, "ether1", 15, a.GREY, a.MONO, 400, "middle"))

# ---- paquetes
viaje(a, "a 10.20.30.5", [(232, 286), (530, 286)], 2, 12, bg=a.BLUE, hold=11)
viaje(a, "a 10.20.30.5", [(530, 286), (530, 286)], 25, 25.5, bg=a.BLUE, hold=24)
viaje(a, "ARP ¿quién es .250?", [(640, 230), (752, 218)], 51, 56, bg=a.AMB, hold=1.5, size=14)
viaje(a, "soy .250: mi MAC", [(752, 218), (640, 230)], 58, 62, bg=a.OK, hold=1.5, size=14)
viaje(a, "a 10.20.30.5", [(580, 242), (770, 222)], 64, 71, bg=a.BLUE, hold=4, still=0)
fijo(a, place(pill_c(a, "a 10.20.30.5", "#FFFFFF", a.BLUE), 760, 223))
viaje(a, "a 8.8.8.8", [(232, 286), (530, 286)], 76, 82, bg=a.CYAN, hold=0.5)
viaje(a, "a 8.8.8.8", [(590, 286), (790, 308)], 83, 90, bg=a.CYAN, hold=9)

# ---- tabla
TX, TY, TW = 48, 384, 648
panel(a, TX, TY, TW, 230, "/ip/route", "lo que mira el router", dark=False)
for x, s in ((22, "dst-address"), (226, "gateway"), (418, "dist")):
    a.add(a.text(TX + x, TY + 62, s, 15, a.GREY, a.MONO))
ROWS = [("10.20.30.0/24", "192.168.88.250", "1"), ("0.0.0.0/0", "203.0.113.1", "1"), ("192.168.88.0/24", "bridge", "0")]
RY = [TY + 74, TY + 122, TY + 170]
for i, (d, g, k) in enumerate(ROWS):
    a.add(a.box(TX + 12, RY[i], TW - 24, 42, a.SLATE, rx=10))
    a.add(a.text(TX + 22, RY[i] + 28, d, 16, a.INK, a.MONO, 600))
    a.add(a.text(TX + 226, RY[i] + 28, g, 16, a.TXT, a.MONO))
    a.add(a.text(TX + 418, RY[i] + 28, k, 16, a.INK, a.MONO, 600))
END = TX + TW - 22


def estado(i, label, fg, bg, t0, t1, still=0, ring=None):
    s = a.pill(END, RY[i] + 7, label, fg, bg, 14, 28, "end")
    if ring:
        s = a.box(TX + 12, RY[i], TW - 24, 42, "none", ring, rx=10, sw=2.5) + s
    en(a, s, t0, t1, still=still)


estado(1, "coincide /0", a.GREY, GHOST, 28, 50)
estado(0, "gana: /24", a.OK, a.OKBG, 32, 75, still=1, ring=a.OK)
estado(2, "conectada: .250 está acá", a.BLUE, "#E5F0FB", 39, 75, still=1, ring=a.BLUE)
estado(0, "no coincide", a.GREY, GHOST, 76, 100)
estado(1, "gana: única", a.OK, a.OKBG, 79, 100, ring=a.OK)

# ---- el paquete
PX, PY, PW = 724, 384, 428
panel(a, PX, PY, PW, 230, "El paquete", "lo que viaja")
for y, s in ((PY + 72, "IP origen"), (PY + 108, "IP destino"), (PY + 144, "MAC destino")):
    a.add(a.text(PX + 22, y, s, 15, LIGHT, a.MONO))
a.add(a.text(PX + 168, PY + 72, "192.168.88.20", 17, "#FFFFFF", a.MONO, 600))
en(a, a.text(PX + 168, PY + 108, "10.20.30.5", 17, "#FFFFFF", a.MONO, 600), 0, 75, still=1)
en(a, a.text(PX + 168, PY + 108, "8.8.8.8", 17, "#FFFFFF", a.MONO, 600), 75, 100)
en(a, a.text(PX + 168, PY + 144, "la del router", 17, "#FFFFFF", a.MONO, 600), 0, 64)
en(a, a.text(PX + 168, PY + 144, "la de .250", 17, GOLD, a.MONO, 600), 64, 75, still=1)
en(a, a.text(PX + 168, PY + 144, "la de 203.0.113.1", 17, "#FFFFFF", a.MONO, 600), 75, 100)
en(a, a.text(PX + 22, PY + 190, "La IP destino no cambia:", 16, GOLD, a.SANS, 600)
   + a.text(PX + 22, PY + 212, "cambia a quién se le entrega la trama.", 16, GOLD, a.SANS, 600), 64, 75, still=1)
en(a, a.text(PX + 22, PY + 190, "Desde la PC hasta el router:", 16, LIGHT, a.SANS, 600)
   + a.text(PX + 22, PY + 212, "su gateway es 192.168.88.1.", 16, LIGHT, a.SANS, 600), 0, 50)

narr(a, [
    (0, 25, "La PC compara 10.20.30.5 con su máscara /24: no es su red, va a su gateway.", a.TXT),
    (25, 50, "Primero manda la máscara más larga; la distancia solo desempata rutas al mismo destino.", a.TXT),
    (50, 75, "El próximo salto se resuelve por la ruta conectada: ARP pregunta la MAC de .250.", a.AMB),
    (75, 100, "Lo que no tiene una ruta más específica sale por la ruta por defecto.", a.OK),
], still_idx=2)

escribir(a, "27-r1", "El gateway es a quién le pasás el paquete",
         "Animación en cuatro tiempos. Una PC de la oficina, 192.168.88.20, el router 192.168.88.1, y dos próximos saltos: "
         "el router del depósito en la misma LAN, 192.168.88.250, con la red 10.20.30.0/24 detrás, y el gateway del proveedor 203.0.113.1 por ether1. "
         "Abajo, la tabla /ip/route con 10.20.30.0/24 por 192.168.88.250, 0.0.0.0/0 por 203.0.113.1 y la conectada 192.168.88.0/24 en bridge, "
         "y un panel con la IP de origen, la IP de destino y la MAC de destino del paquete. "
         "1: la PC quiere llegar a 10.20.30.5, que no está en su /24, y se lo entrega a su gateway, el router. "
         "2: en la tabla coinciden 0.0.0.0/0 y 10.20.30.0/24; gana la /24 por ser más específica, y su gateway .250 está en la red conectada del bridge. "
         "3: el router pregunta por ARP la MAC de .250, el depósito contesta y el paquete sale hacia él: la IP destino sigue siendo 10.20.30.5, "
         "solo cambia la MAC de destino. 4: un paquete a 8.8.8.8 solo coincide con 0.0.0.0/0 y sale por ether1 hacia 203.0.113.1.",
         [8, 33, 54, 60, 70, 90])
