#!/usr/bin/env python3
"""Teoría lección 6 (VLAN completa): el pedido DHCP de una cámara en la VLAN 20, tramo por tramo,
con la etiqueta 802.1Q que se pone y se saca.
Salida: site2/ilustraciones/omada/6-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(24, "VLAN 802.1Q", "La etiqueta 20 solo viaja por el uplink")
F = a.steps([
    "La cámara pide IP por DHCP: la trama sale sin etiqueta.",
    "El puerto la mete en la VLAN 20, su nativa. Por el uplink viaja con la etiqueta 20.",
    "El gateway la recibe en su interfaz de la VLAN 20 y responde desde ese DHCP.",
    "En el puerto 5 el switch saca la etiqueta: la cámara recibe 10.10.20.x.",
], still=1)

Y, H = 196, 80
WY = Y + H / 2
a.add(nodo(a, 48, Y, 200, H, "Cámara", "no sabe de VLAN", dark=False))
a.add(nodo(a, 440, Y, 240, H, "Switch", "puerto 5 · uplink"))
a.add(nodo(a, 900, Y, 252, H, "Gateway ER", "VLAN 20 · 10.10.20.1"))
a.add(linea(a, 248, WY, 440, WY, a.BLUE, 4))
a.add(linea(a, 680, WY, 900, WY, a.BLUE, 4))
a.add(a.text(344, WY + 46, "sin etiqueta", 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text(790, WY + 46, "etiqueta 20", 15, a.AMB, a.MONO, 600, "middle"))


def trama(label, tag, color):
    w = int(len(label) * 15 * 0.62 + 26)
    s = f'<rect x="{-w / 2}" y="-15" width="{w}" height="30" rx="8" fill="{color}"/>' + a.text(0, 5, label, 15, a.WHITE, a.MONO, 600, "middle")
    if tag:
        s += f'<rect x="{-w / 2 - 44}" y="-15" width="40" height="30" rx="8" fill="{a.AMB}"/>' + a.text(-w / 2 - 24, 5, "20", 15, a.WHITE, a.MONO, 600, "middle")
    return s


(a0, a1), (b0, b1), (c0, c1), (d0, d1) = F
viaje(a, trama("pedido", False, a.BLUE), 290, WY - 30, 410, WY - 30, a0 + 4, a1 - 6, hold=4)
viaje(a, trama("pedido", True, a.BLUE), 735, WY - 30, 860, WY - 30, b0 + 6, b1 - 6, hold=4)
viaje(a, trama("oferta", True, a.OK), 860, WY - 30, 735, WY - 30, c0 + 6, c1 - 6, hold=4)
viaje(a, trama("oferta", False, a.OK), 410, WY - 30, 304, WY - 30, d0 + 4, d1 - 8, hold=8)
# cuadro fijo: la trama etiquetada en el uplink
solo_fijo(a, f'<g transform="translate(800 {WY - 30})">{trama("pedido", True, a.BLUE)}</g>')
en(a, chip(a, 148, Y + H + 8, "10.10.20.x", a.OK, a.OKBG, anchor="middle", stroke=a.OK), d1 - 9, 100, fade=0.6)

# las tres patas
PATAS = [("Puerto 5 · perfil CCTV", "VLAN 20 nativa (PVID)"), ("Uplink · perfil All", "VLAN 20 tagueada"),
         ("Gateway · red CCTV", "interfaz VLAN 20 + DHCP")]
PY, PW = 338, 352
for i, (t, s) in enumerate(PATAS):
    x = 48 + i * (PW + 24)
    a.add(a.box(x, PY, PW, 84, a.WHITE, a.LINE))
    a.add(f'<circle cx="{x + 30}" cy="{PY + 32}" r="15" fill="{a.SLATE}"/>' + a.text(x + 30, PY + 38, str(i + 1), 15, a.INK, a.MONO, 600, "middle"))
    a.add(a.text(x + 56, PY + 38, t, 18, a.INK, a.HEAD, 600))
    a.add(a.text(x + 56, PY + 64, s, 15, a.TXT, a.MONO))
for i, t0 in enumerate([a1 - 6, b1 - 6, c0 + 4]):
    x = 48 + i * (PW + 24)
    en(a, a.box(x, PY, PW, 84, "none", a.OK, rx=14, sw=3) + ok(a, x + PW - 28, PY + 32, 13), t0, 100, still=1 if i < 2 else 0)

# anatomía de la trama
AY = 456
a.add(a.text(48, AY, "La trama por dentro", 18, a.INK, a.HEAD, 600))
CAMPOS = [("Destino", 150, a.SLATE, a.INK), ("Origen", 150, a.SLATE, a.INK), ("TAG", 250, a.AMBBG, a.AMB),
          ("Tipo", 110, a.SLATE, a.INK), ("Datos: DHCP", 330, a.SLATE, a.INK)]


def anatomia(con_tag):
    s, x = "", 48
    for nom, w, bg, fg in CAMPOS:
        if nom == "TAG":
            if not con_tag:
                continue
            s += a.box(x, AY + 20, w - 8, 56, bg, a.AMB, rx=10, sw=2)
            s += a.text(x + (w - 8) / 2, AY + 45, "802.1Q · 4 bytes", 15, fg, a.MONO, 600, "middle")
            s += a.text(x + (w - 8) / 2, AY + 66, "VLAN 20 (12 bits)", 15, fg, a.MONO, 400, "middle")
        else:
            s += a.box(x, AY + 20, w - 8, 56, bg, None, rx=10)
            s += a.text(x + (w - 8) / 2, AY + 54, nom, 16, fg, a.SANS, 600, "middle")
        x += w
    return s


en(a, anatomia(False) + a.text(48, AY + 108, "Tramo cámara ↔ puerto 5: trama común, sin etiqueta.", 16, a.TXT, a.SANS), a0, b0, still=0)
en(a, anatomia(True) + a.text(48, AY + 108, "Tramo uplink ↔ gateway: la etiqueta de 4 bytes lleva el número de VLAN (12 bits: 4094 útiles).", 16, a.TXT, a.SANS), b0, d0, still=1)
en(a, anatomia(False) + a.text(48, AY + 108, "Tramo puerto 5 → cámara: la etiqueta ya no está.", 16, a.TXT, a.SANS), d0, 100, still=0)

pie(a, F, [
    "La cámara no sabe de VLAN: el que decide es el perfil del puerto.",
    "Un mismo cable puede llevar varias VLAN separadas por la etiqueta.",
    "Si falla cualquiera de los tres tramos, no hay IP.",
    "La VLAN separa el broadcast, pero no aísla: eso es la ACL.",
], y=640, still=1)

salida(a, 6, 1, "La etiqueta 20 solo viaja por el uplink",
       "Animación en cuatro tiempos: cámara, switch y gateway ER con la VLAN 20 (10.10.20.1). 1: la cámara manda un pedido DHCP sin "
       "etiqueta hasta el puerto 5. 2: el switch lo mete en la VLAN 20 porque es la nativa del puerto y por el uplink lo manda con la "
       "etiqueta 802.1Q de 4 bytes, que lleva el número de VLAN en 12 bits. 3: el gateway lo recibe en su interfaz de la VLAN 20 y responde "
       "desde el DHCP de esa red, también etiquetado. 4: en el puerto 5 el switch saca la etiqueta y la cámara recibe una IP 10.10.20.x. "
       "Abajo se ven las tres patas (puerto con VLAN 20 nativa, uplink con VLAN 20 tagueada, gateway con interfaz y DHCP) y la trama "
       "por dentro, con y sin etiqueta.",
       [14, 37, 62, 90])
