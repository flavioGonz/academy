#!/usr/bin/env python3
"""Lección 34 (Descubrir vecinos), Laboratorio paso 2: lo que trae la trama LLDP de un switch de otra marca y cómo
RouterOS arma con eso la fila del vecino. EtherType 0x88CC a la multicast 01:80:C2:00:00:0E, los TLV obligatorios
(Chassis ID, Port ID, TTL) y los opcionales (nombre, capacidades, IP de gestión)."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · LABORATORIO · PASO 2", title="Lo que trae la trama LLDP del switch")
a.steps([
    "El switch manda su trama: EtherType 0x88CC, a una multicast.",
    "Primero los TLV obligatorios: chasis, puerto y TTL.",
    "Después los opcionales: nombre, capacidades, IP de gestión.",
    "Con eso RouterOS arma la fila del vecino en ether3.",
], still=2)

a.add(dev(a, 48, 180, 290, 84, "Switch del rack", "otra marca · LLDP", "server"))
a.add(dev(a, 862, 180, 290, 84, "Router", "ether3", None, dark=True))
a.add(linea(338, 222, 862, 222, a.LINE, 4))
for t0 in (3, 28, 53):
    viaje(a, "trama LLDP", [(420, 222), (780, 222)], t0, t0 + 8, bg=a.NAVY2, size=14, hold=1)
fijo(a, place(pill_c(a, "trama LLDP", "#FFFFFF", a.NAVY2, 14), 600, 222))
en(a, a.text(600, 252, "los switches estándar no la reenvían: la ve solo el vecino directo", 15, a.GREY, a.SANS, 600, "middle"), 6, 100, still=1)


def seg(x, y, w, k, v, c, bg):
    return (a.box(x, y, w, 52, bg, c, rx=8, sw=1.5) + a.text(x + 12, y + 21, k, 14, c, a.MONO, 600)
            + a.text(x + 12, y + 43, v, 15, a.INK, a.MONO, 600))


def fila(y, titulo, segs, t0, c, bg):
    s = a.text(48, y + 33, titulo, 15, a.GREY, a.SANS, 700)
    x = 230
    for i, (w, k, v) in enumerate(segs):
        s += seg(x, y, w, k, v, c, bg)
        x += w + 8
    en(a, s, t0, 100, still=1)


fila(286, "Ethernet", [(300, "destino", "01:80:C2:00:00:0E"), (250, "origen", "MAC del switch"), (230, "EtherType", "0x88CC")], 8, a.BLUE, "#E5F0FB")
fila(350, "obligatorios", [(300, "Chassis ID", "MAC del switch"), (250, "Port ID", "puerto 24 (ej.)"), (230, "TTL", "120 s (ej.)")], 28, a.OK, a.OKBG)
fila(414, "opcionales", [(300, "System Name", "sw-rack"), (250, "Capabilities", "bridge"), (230, "Mgmt Address", "192.168.88.2")], 53, a.AMB, a.AMBBG)
en(a, a.text(1040, 383, "y al final, End", 15, a.GREY, a.SANS, 600), 30, 100, still=1)

# ---- la fila del vecino
TY = 482
a.add(a.box(48, TY, 1104, 118, a.INK, rx=16) + a.text(70, TY + 30, "lo que queda en la tabla · /ip/neighbor/print detail", 15, LIGHT, a.MONO))
en(a, a.text(70, TY + 62, "interface=ether3,bridge  identity=sw-rack  address=192.168.88.2", 16, "#FFFFFF", a.MONO, 600)
   + a.text(70, TY + 90, "mac-address=(la del switch)  system-caps=bridge  discovered-by=lldp", 16, "#FFFFFF", a.MONO, 600), 76, 100)
en(a, a.text(70, TY + 72, "esperando el anuncio…", 16, LIGHT, a.MONO), 0, 76, still=1)

narr(a, [
    (0, 25, "LLDP no usa IP: es una trama Ethernet propia, con su EtherType.", a.TXT),
    (25, 50, "Cada TLV es tipo, largo y valor; sin estos tres, la trama no vale.", a.OK),
    (50, 75, "Lo opcional depende del equipo: cámaras y NVR, según modelo y firmware.", a.AMB),
    (75, 100, "El TTL dice cuánto recordarlo: si no llega otro anuncio a tiempo, el vecino se borra.", a.TXT),
], y=640, still_idx=2)

escribir(a, "34-l1", "Lo que trae la trama LLDP del switch",
         "Animación en cuatro tiempos del paso 2. El switch del rack, de otra marca, manda una trama LLDP al router por ether3; los switches estándar no la reenvían, así que la ve solo el vecino directo. "
         "1: el encabezado Ethernet lleva destino 01:80:C2:00:00:0E, una multicast, origen la MAC del switch y EtherType 0x88CC. "
         "2: adentro van primero los TLV obligatorios: Chassis ID con la MAC del switch, Port ID con su puerto, de ejemplo el 24, y TTL, de ejemplo 120 segundos. "
         "3: después los opcionales: System Name sw-rack, Capabilities bridge y Mgmt Address 192.168.88.2, y al final End. "
         "4: con eso /ip/neighbor/print detail muestra interface=ether3,bridge, identity=sw-rack, address=192.168.88.2, la MAC del switch, system-caps=bridge y discovered-by=lldp.",
         [8, 33, 58, 85, 95])
