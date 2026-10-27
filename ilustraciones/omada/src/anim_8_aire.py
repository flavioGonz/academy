#!/usr/bin/env python3
"""Teoría lección 8 (Menos potencia): en un canal habla uno por vez; con canales que no se pisan cada AP tiene su aire;
3 dB menos es la mitad de la potencia y la celda se achica.
Salida: site2/ilustraciones/omada/8-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(24, "CANAL Y POTENCIA", "En un canal habla uno por vez")
F = a.steps([
    "Dos EAP en el mismo canal se escuchan: se turnan para hablar.",
    "Cada uno espera al otro, aunque tenga pocos clientes: se frenan los dos.",
    "En canales que no se pisan, 1 y 6, cada uno tiene su aire: hablan a la vez.",
    "Recién ahí, potencia: de 28 a 25 dBm es la mitad, y la celda se achica.",
], still=2)
(a0, a1), (b0, b1), (c0, c1), (d0, d1) = F

CY = 372
E1, E2 = 230, 480
BLUEC, GREENC = a.BLUE, a.OK


def celda(cx, color):
    return f'<circle cx="{cx}" cy="{CY}" r="160" fill="{color}" fill-opacity=".09" stroke="{color}" stroke-width="2"/>'


# celdas: tamaño completo hasta la fase 4, después se achican
for cx, col in ((E1, BLUEC), (E2, GREENC)):
    k = a.keyframes([(0, 1), (d0 + 2, 1), (d0 + 8, 0.72), (99, 0.72), (100, 1)], "transform", "scale({})")
    a.add(a.group(celda(cx, col), k, a.keyframes([(0, 1), (100, 1)]), still=1, origin=f"{cx}px {CY}px"))
a.add(eap(a, E1, CY - 10, 26, BLUEC) + eap(a, E2, CY - 10, 26, GREENC))
a.add(a.text(E1, CY + 40, "EAP 1", 17, a.INK, a.HEAD, 600, "middle") + a.text(E2, CY + 40, "EAP 2", 17, a.INK, a.HEAD, 600, "middle"))
# canales
fase(a, chip(a, E1, CY + 54, "canal 6", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB) + chip(a, E2, CY + 54, "canal 6", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), F, 0, 1)
fase(a, chip(a, E1, CY + 54, "canal 1", BLUEC, a.WHITE, anchor="middle", stroke=BLUEC) + chip(a, E2, CY + 54, "canal 6", GREENC, a.WHITE, anchor="middle", stroke=GREENC), F, 2, 3, still=1)
# potencia
fase(a, chip(a, E1, CY - 76, "28 dBm", a.INK, a.WHITE, anchor="middle", stroke=a.LINE) + chip(a, E2, CY - 76, "28 dBm", a.INK, a.WHITE, anchor="middle", stroke=a.LINE), F, 0, 2, still=1)
fase(a, chip(a, E1, CY - 76, "25 dBm", a.OK, a.OKBG, anchor="middle", stroke=a.OK) + chip(a, E2, CY - 76, "25 dBm", a.OK, a.OKBG, anchor="middle", stroke=a.OK), F, 3)
# "se escuchan"
fase(a, a.arrow(f"M{E1 + 40} {CY - 10} H{E2 - 44}", a.AMB, 2.5) + a.arrow(f"M{E2 - 40} {CY - 10} H{E1 + 44}", a.AMB, 2.5)
     + chip(a, (E1 + E2) / 2, CY - 64, "se escuchan", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), F, 0, 1)

# --- panel derecho: tiempo de aire
RX, RY, RW = 712, 190, 440
a.add(a.box(RX, RY, RW, 380, a.WHITE, a.LINE))
fase(a, a.text(RX + 22, RY + 34, "Tiempo de aire", 19, a.INK, a.HEAD, 600), F, 0, 2, still=1)
fase(a, a.text(RX + 22, RY + 34, "Potencia", 19, a.INK, a.HEAD, 600), F, 3)
BX, BW, BH = RX + 22, RW - 44, 40


def seg_bar(y, segs, t_start, t_end, still=0, labels=True):
    """segs: lista de (color, texto) que aparecen uno tras otro entre t_start y t_end."""
    w = BW / len(segs)
    en(a, a.box(BX, y, BW, BH, a.SLATE, None, rx=8), t_start - 2, t_end, still)
    step = (t_end - t_start - 4) / len(segs)
    for i, (col, lab) in enumerate(segs):
        t = t_start + i * step
        inner = a.box(BX + i * w + 1, y, w - 2, BH, col, None, rx=6) + (a.text(BX + i * w + w / 2, y + 26, lab, 15, a.WHITE, a.MONO, 600, "middle") if lab else "")
        en(a, inner, t, t_end, still, fade=0.4)


# fases 1-2: un canal compartido
fase(a, a.text(RX + 22, RY + 74, "canal 6, compartido", 16, a.AMB, a.MONO, 600), F, 0, 1)
seg_bar(RY + 88, [(BLUEC, "1"), (GREENC, "2")] * 4, a0 + 2.5, b1)
fase(a, a.text(RX + 22, RY + 160, "Mientras uno habla, el otro espera.", 17, a.TXT, a.SANS)
     + a.text(RX + 22, RY + 188, "Se frenan los dos.", 17, a.BAD, a.SANS, 600), F, 1)
# fase 3: dos canales
fase(a, a.text(RX + 22, RY + 74, "canal 1 · EAP 1", 16, BLUEC, a.MONO, 600) + a.text(RX + 22, RY + 154, "canal 6 · EAP 2", 16, GREENC, a.MONO, 600), F, 2, still=1)
fase(a, a.box(BX, RY + 88, BW, BH, a.SLATE, None, rx=8) + a.box(BX, RY + 168, BW, BH, a.SLATE, None, rx=8), F, 2, still=1)
for y, col in ((RY + 88, BLUEC), (RY + 168, GREENC)):
    k = a.keyframes([(0, 0), (c0 + 2, 0), (c0 + 14, 1), (100, 1)], "transform", "scaleX({})")
    a.add(a.group(a.box(BX, y, BW, BH, col, None, rx=8), k, a.show(c0 + 2, c1, 0.6), still=1, origin=f"{BX}px {y}px"))
fase(a, a.text(RX + 22, RY + 250, "En 2.4 GHz: 1, 6 u 11, a 20 MHz.", 17, a.TXT, a.SANS)
     + a.text(RX + 22, RY + 278, "En 5 GHz: distintos entre vecinos.", 17, a.TXT, a.SANS), F, 2, still=1)
# fase 4: potencia
fase(a, a.text(RX + 22, RY + 74, "dBm es una escala logarítmica", 16, a.INK, a.MONO, 600)
     + a.text(RX + 22, RY + 120, "28 dBm", 16, a.INK, a.MONO, 600) + a.box(RX + 110, RY + 100, 300, 30, a.BLUE, None, rx=8)
     + a.text(RX + 22, RY + 170, "25 dBm", 16, a.INK, a.MONO, 600) + a.box(RX + 110, RY + 150, 150, 30, a.OK, None, rx=8)
     + a.text(RX + 270, RY + 171, "la mitad", 16, a.OK, a.SANS, 600)
     + a.text(RX + 22, RY + 236, "3 dB menos = la mitad de la potencia.", 17, a.TXT, a.SANS)
     + a.text(RX + 22, RY + 264, "Con EAP a menos de 12 m, la celda", 17, a.TXT, a.SANS)
     + a.text(RX + 22, RY + 290, "se achica sin dejar huecos.", 17, a.TXT, a.SANS)
     + a.text(RX + 22, RY + 340, "Medí: debajo de -70 dBm, un escalón más.", 17, a.AMB, a.SANS, 600), F, 3)

pie(a, F, [
    "El aire es un medio compartido.",
    "Más EAP en el mismo canal no suma velocidad: reparte el mismo aire.",
    "Por eso primero canal y ancho, y después potencia.",
    "Menos potencia también ayuda al roaming: el cliente suelta antes al AP lejano.",
], y=640, still=2)

salida(a, 8, 1, "En un canal habla uno por vez",
       "Animación en cuatro tiempos con dos EAP vecinos y sus celdas superpuestas. 1: los dos están en el canal 6, se escuchan y se "
       "turnan: la barra de tiempo de aire se llena alternando EAP 1 y EAP 2. 2: cada uno espera al otro aunque tenga pocos clientes y "
       "usa la mitad del aire. 3: con canales que no se pisan, 1 y 6, cada EAP tiene su propio aire y las dos barras se llenan a la vez; "
       "en 2.4 GHz se usan 1, 6 u 11 a 20 MHz. 4: la potencia baja de 28 a 25 dBm, que es la mitad porque 3 dB menos es la mitad, y las "
       "celdas se achican sin dejar huecos; si un punto queda por debajo de -70 dBm, un escalón más en ese AP.",
       [14, 40, 66, 92])
