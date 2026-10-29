#!/usr/bin/env python3
"""Lección 1 · teoría: Neighbors escucha MNDP; clic en la IP necesita ruteo, clic en la MAC no; la MAC no cruza routers."""
from _anim_mikrotik_1_13 import *

a = Anim(T=20, kicker="MIKROTIK · CÓMO FUNCIONA", title="Por la MAC entrás sin IP, pero solo en tu segmento")
a.steps([
    "El router se anuncia por MNDP: MAC, identidad y versión.",
    "Clic en la IP: WinBox abre TCP 8291, y eso necesita ruteo.",
    "Clic en la MAC: viajan tramas Ethernet directas. Entrás.",
    "Las tramas no cruzan routers: la MAC solo sirve en tu segmento.",
], still=2)

# ---- escena
NX, NY, NW, NH = 48, 186, 350, 226
a.add(device(a, NX, NY, NW, NH, "Notebook · WinBox", "pestaña Neighbors"))
TY = NY + 78
a.add(a.box(NX + 16, TY, NW - 32, 34, a.SLATE, rx=8))
a.add(a.text(NX + 28, TY + 22, "MAC", 13, a.GREY, a.MONO))
a.add(a.text(NX + 184, TY + 22, "IP", 13, a.GREY, a.MONO))
a.add(a.text(NX + 254, TY + 22, "IDENTITY", 13, a.GREY, a.MONO))
row = (a.box(NX + 16, TY + 42, NW - 32, 40, a.WHITE, a.BLUE, rx=8, sw=2)
       + a.text(NX + 28, TY + 68, "AA:BB:CC:00:11:22", 14, a.INK, a.MONO, 600)
       + a.text(NX + 184, TY + 68, "0.0.0.0", 14, a.TXT, a.MONO)
       + a.text(NX + 254, TY + 68, "MikroTik", 14, a.TXT, a.MONO))
a.add(a.group(row, a.show(12, 100), still=1))
a.add(a.group(a.text(NX + 28, TY + 112, "aparece aunque no tenga IP en tu red", 15, a.TXT), a.show(12, 100), still=1))
a.add(during(a, a.box(NX + 175, TY + 46, 76, 32, "none", a.AMB, rx=6, sw=2.5), 26, 48))
a.add(during(a, a.box(NX + 22, TY + 46, 160, 32, "none", a.OK, rx=6, sw=2.5), 51, 73, still=1))

SY = 320
RX, RY, RW, RH = 600, 250, 210, 140
L0 = NX + NW
a.add(line(L0, SY, RX, SY, a.BLUE, 4))
a.add(a.text((L0 + RX) / 2, SY - 34, "mismo segmento", 14, a.BLUE, a.MONO, 600, "middle"))
a.add(a.text((L0 + RX) / 2, SY - 14, "Ethernet · capa 2", 13, a.GREY, a.MONO, 400, "middle"))
a.add(device(a, RX, RY, RW, RH, "Router", "AA:BB:CC:00:11:22", dark=True, ssize=13, sub2="sin IP en tu red"))
a.add(line(RX + RW, SY, 960, SY, a.GREY, 3, "7 6"))
a.add(a.text(885, SY - 30, "otro segmento", 13, a.GREY, a.MONO, 400, "middle"))
a.add(device(a, 960, RY, 192, RH, "Otro equipo", "detrás del router", ssize=13))

PY = SY + 46
MID = (L0 + RX) / 2
ST = 452   # línea de estado
# 1. anuncio MNDP
a.add(travel(a, pkt(a, "MNDP", a.BLUE, size=14), [(RX - 50, PY), (L0 + 50, PY)], 2, 10, hold=10))
a.add(during(a, a.text(600, ST, "El router manda anuncios de capa 2 con su MAC, identidad y versión.", 16, a.BLUE, a.SANS, 600, "middle"), 2, 23))
# 2. clic en la IP
a.add(travel(a, pkt(a, "TCP 8291", a.AMB, size=14), [(L0 + 60, PY), (MID + 10, PY)], 27, 32, hold=14))
a.add(during(a, xmark(a, MID + 82, PY), 32, 48))
a.add(during(a, a.text(600, ST, "Sin una IP de tu red en el router, la notebook no tiene ruta: no llega.", 16, a.BAD, a.SANS, 600, "middle"), 32, 48))
# 3. clic en la MAC
a.add(travel(a, pkt(a, "trama", a.OK, size=14), [(L0 + 50, PY), (RX - 50, PY)], 52, 59, hold=13))
a.add(still_only(a, place(a, pkt(a, "trama", a.OK, size=14), RX - 50, PY)))
a.add(during(a, check(a, RX + RW - 26, RY + 26), 59, 73, still=1))
a.add(during(a, a.text(600, ST, "La trama va a la MAC del router y llega directo: entrás sin IP.", 16, a.OK, a.SANS, 600, "middle"), 59, 73, still=1))
# 4. no cruza routers
a.add(travel(a, pkt(a, "trama", a.OK, size=14), [(L0 + 50, PY), (RX - 50, PY)], 77, 84, hold=14))
a.add(during(a, xmark(a, 885, SY), 84, 98.5))
a.add(during(a, a.text(885, SY + 46, "no pasa", 14, a.BAD, a.MONO, 600, "middle"), 84, 98.5))
a.add(during(a, a.text(600, ST, "Para el equipo de atrás, la trama no cruza el router: la MAC no sirve.", 16, a.BAD, a.SANS, 600, "middle"), 84, 98.5))

# ---- pie fijo
a.add(note(a, 48, 482, 540, 92, "Clic en la IP", ["WinBox abre una conexión TCP al puerto 8291.", "Necesita ruteo: tu notebook tiene que llegar a esa IP."], "amb"))
a.add(note(a, 612, 482, 540, 92, "Clic en la MAC", ["Viaja en tramas Ethernet directas, sin IP.", "No cruza routers: solo en el mismo segmento."], "ok"))
a.add(a.text(48, 622, "Neighbors escucha anuncios de capa 2: por eso ves equipos con IP 0.0.0.0 o de otra red.", 16, a.TXT, a.SANS, 600))

p, pre = out(1, 1)
a.write(p, title="Entrar por IP o por MAC en WinBox",
        desc="Animación en cuatro tiempos. 1: el router de laboratorio se anuncia por MNDP en el segmento y aparece en la pestaña Neighbors "
             "de WinBox con su MAC AA:BB:CC:00:11:22 e IP 0.0.0.0. 2: clic en la IP: WinBox intenta TCP al puerto 8291, pero sin IP en la misma red "
             "no hay ruta y no llega. 3: clic en la MAC: la trama Ethernet llega directo al router y entrás sin IP. 4: una trama dirigida a un equipo "
             "detrás del router no pasa: la MAC solo sirve en el mismo segmento.",
        preview=[8, 38, 62, 90], prefix=pre)
