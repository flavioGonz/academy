#!/usr/bin/env python3
"""Lección 3 · teoría: available-from deja el puerto visible; drop en input lo descarta antes del servicio."""
from _anim_mikrotik_1_13 import *

a = Anim(T=22, kicker="MIKROTIK · LECCIÓN 3 · CÓMO FUNCIONA", title="available-from contesta; el drop en input calla")
a.steps([
    "Un escáner de internet prueba el puerto 8291 del router.",
    "Solo available-from: el servicio contesta y después corta. Se ve abierto.",
    "Con drop en input: el paquete se descarta antes de llegar al servicio.",
    "Sin respuesta, el escáner no tiene nada que anotar.",
], still=3)

LANES = [(176, "Solo available-from", "sin drop para 8291"), (370, "available-from + drop en input", "drop desde internet")]
CX, CW, LH = 470, 682, 170
for y0, name, fw in LANES:
    a.add(device(a, 48, y0, 230, LH, "Escáner", "desde internet"))
    a.add(a.box(CX, y0, CW, LH, a.WHITE, a.LINE))
    a.add(a.text(CX + 20, y0 + 30, "Router · " + name, 17, a.INK, a.SANS, 600))
    a.add(a.box(CX + 20, y0 + 46, 250, 64, a.SLATE, rx=10))
    a.add(a.text(CX + 36, y0 + 72, "firewall · input", 16, a.INK, a.SANS, 600))
    a.add(a.text(CX + 36, y0 + 96, fw, 14, a.BAD if "drop" in fw and "sin" not in fw else a.TXT, a.MONO))
    a.add(a.box(CX + 290, y0 + 46, 372, 64, a.INK, rx=10))
    a.add(a.text(CX + 306, y0 + 72, "WinBox · TCP 8291", 16, a.WHITE, a.SANS, 600))
    a.add(a.text(CX + 306, y0 + 96, "available-from=192.168.88.0/24", 14, SKY, a.MONO))
    a.add(line(282, y0 + 140, CX + CW - 20, y0 + 140, a.LINE, 3, "4 6"))

yA, yB = LANES[0][0], LANES[1][0]
SVC = CX + 290 + 186
FWX = CX + 20 + 125
# carril A
a.add(travel(a, pkt(a, "→ 8291", a.BAD, size=14), [(340, yA + 140), (SVC, yA + 140)], 2, 13, hold=11))
a.add(travel(a, pkt(a, "respuesta", a.AMB, size=14), [(SVC, yA + 140), (360, yA + 140)], 27, 38, hold=11, still=1))
a.add(during(a, a.text(CX + CW - 20, yA + 30, "contesta y después corta", 15, a.AMB, a.MONO, 600, "end"), 13, 50, still=1))
a.add(during(a, a.text(66, yA + 122, "8291: abierto", 16, a.AMB, a.MONO, 600), 38, 100, still=1))
a.add(during(a, a.text(66, yA + 146, "lo anota", 14, a.AMB, a.MONO), 38, 100, still=1))
# carril B
a.add(travel(a, pkt(a, "→ 8291", a.BAD, size=14), [(340, yB + 140), (FWX - 40, yB + 140)], 52, 60, hold=14, still=0))
a.add(during(a, xmark(a, FWX + 40, yB + 140), 60, 100, still=1))
a.add(during(a, a.text(CX + CW - 20, yB + 30, "descartado antes del servicio", 15, a.BAD, a.MONO, 600, "end"), 60, 100, still=1))
a.add(during(a, a.text(66, yB + 122, "esperando…", 15, a.GREY, a.MONO), 61, 76))
a.add(during(a, a.text(66, yB + 122, "8291: sin", 16, a.OK, a.MONO, 600) + a.text(66, yB + 146, "respuesta", 16, a.OK, a.MONO, 600), 76, 100, still=1))

a.add(a.text(48, 584, "Los escáneres recorren internet probando 8291, 22, 23, 21, 80 y 8728 todo el tiempo.", 16, a.TXT, a.SANS, 600))
a.add(a.text(48, 616, "Por eso MikroTik prefiere el firewall y deja available-from como capa extra.", 16, a.INK, a.SANS, 600))

p, pre = out(3, 1)
a.write(p, title="available-from contra drop en input",
        desc="Animación en cuatro tiempos con dos routers, uno solo con available-from=192.168.88.0/24 en WinBox (TCP 8291) y otro que además tiene un drop "
             "en la cadena input para lo que viene de internet. 1: un escáner de internet manda un paquete al 8291 del primero y llega al servicio. "
             "2: el servicio contesta y después corta la conexión; el escáner anota el puerto como abierto. 3: en el segundo router, el drop en input "
             "descarta el paquete antes de llegar al servicio. 4: sin respuesta, el escáner no tiene nada que anotar. MikroTik prefiere el firewall y deja "
             "available-from como capa extra.",
        preview=[10, 34, 62, 90], prefix=pre)
