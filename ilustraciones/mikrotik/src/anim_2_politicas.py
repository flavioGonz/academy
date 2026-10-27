#!/usr/bin/env python3
"""Lección 2 · teoría: address al autenticar, políticas de entrada, políticas de acción y el log con nombre."""
from _anim_mikrotik_1_13 import *

a = Anim(T=24, kicker="MIKROTIK · LECCIÓN 2 · CÓMO FUNCIONA", title="Cada pedido pasa por los controles del usuario")
a.steps([
    "mesa.ayuda entra por WinBox desde la LAN: address y winbox, bien.",
    "Pide /ip/address/print: necesita read, y su grupo la tiene.",
    "Pide /system/reboot: necesita reboot. El grupo no la tiene.",
    "El mismo usuario desde afuera: no coincide con address.",
], still=2)

# usuario
UX, UY, UW, UH = 48, 186, 250, 150
a.add(device(a, UX, UY, UW, UH, "mesa.ayuda", "grupo monitoreo"))
a.add(a.group(a.text(UX + 18, UY + 110, "desde 192.168.88.10", 15, a.INK, a.MONO, 600), a.show(0, 75), still=1))
a.add(during(a, a.text(UX + 18, UY + 110, "desde 203.0.113.25", 15, a.BAD, a.MONO, 600), 75, 100))

# controles
G = [(330, "¿Desde dónde?", "address=", "192.168.88.0/24"),
     (540, "¿Cómo entra?", "local · ssh", "winbox"),
     (750, "¿Qué hace?", "read · test", "sin write ni reboot")]
GW, GY, GH = 190, 186, 150
for gx, t, l1, l2 in G:
    a.add(a.box(gx, GY, GW, GH, a.WHITE, a.LINE))
    a.add(a.text(gx + 16, GY + 32, t, 17, a.INK, a.SANS, 600))
    a.add(a.text(gx + 16, GY + 64, l1, 14, a.TXT, a.MONO))
    a.add(a.text(gx + 16, GY + 88, l2, 14, a.TXT, a.MONO))
a.add(a.text(330 + 16, GY + 128, "al autenticar", 13, a.GREY, a.MONO))
a.add(a.text(540 + 16, GY + 128, "política de entrada", 13, a.GREY, a.MONO))
a.add(a.text(750 + 16, GY + 128, "política de acción", 13, a.GREY, a.MONO))

# resultado
RX, RW = 970, 182
a.add(a.box(RX, GY, RW, GH, a.INK))
a.add(a.text(RX + 16, GY + 32, "Router", 17, a.WHITE, a.SANS, 600))
res = [(12, 25, "Entra", "sesión abierta", MINT, 0),
       (33, 50, "Se ejecuta", "muestra las IP", MINT, 0),
       (56, 75, "Rechazado", "falta reboot", GOLD, 1),
       (81, 98.5, "Rechazado", "login fallido", GOLD, 0)]
for t0, t1, l1, l2, col, st in res:
    a.add(a.group(a.text(RX + 16, GY + 72, l1, 20, col, a.SANS, 600) + a.text(RX + 16, GY + 100, l2, 14, SKY, a.MONO),
                  a.show(t0, t1, 0.8), still=st))

# camino
PY = 392
a.add(line(180, PY, 1060, PY, a.LINE, 3, "4 6"))
MY = GY + GH + 0
gc = [gx + GW / 2 for gx, *_ in G]


def mark(ok, i, t0, t1, st=0):
    f = check if ok else xmark
    a.add(during(a, f(a, gc[i], PY - 40), t0, t1, still=st))


# 1. login desde la LAN
a.add(travel(a, pkt(a, "login winbox", a.BLUE, size=14), [(180, PY), (1060, PY)], 2, 12, hold=11))
mark(True, 0, 5, 24.5); mark(True, 1, 7.5, 24.5); mark(True, 2, 10, 24.5)
# 2. lectura
a.add(travel(a, pkt(a, "/ip/address/print", a.BLUE, size=14), [(660, PY), (1060, PY)], 27, 33, hold=15))
mark(True, 2, 30, 49.5)
# 3. reboot
a.add(travel(a, pkt(a, "/system/reboot", a.AMB, size=14), [(640, PY), (750, PY)], 52, 56, hold=17.5, still=0))
a.add(still_only(a, place(a, pkt(a, "/system/reboot", a.AMB, size=14), 750, PY)))
mark(False, 2, 56, 74.5, st=1)
# 4. desde afuera
a.add(travel(a, pkt(a, "login winbox", a.BAD, size=14), [(180, PY), (300, PY)], 77, 81, hold=17.5))
mark(False, 0, 81, 98.5)

# estado
ST = 450
for t0, t1, txt, col, st in [
        (0, 25, "La sesión se abre y el log anota el nombre del usuario.", a.OK, 0),
        (25, 50, "Ver la configuración usa read: el router la muestra.", a.OK, 0),
        (50, 75, "Si una acción necesita una política que el grupo no tiene, el router la rechaza.", a.BAD, 1),
        (75, 100, "address se evalúa al autenticar, aparte del firewall: el login no se acepta.", a.BAD, 0)]:
    a.add(a.group(a.text(600, ST, txt, 16, col, a.SANS, 600, "middle"), a.show(t0, t1, 0.8), still=st))

# grupo y log
a.add(a.box(48, 480, 520, 120, a.WHITE, a.LINE))
a.add(a.text(66, 510, "/user/group · monitoreo", 15, a.INK, a.MONO, 600))
x = 66
for pol in ["local", "ssh", "winbox", "read", "test"]:
    a.add(a.pill(x, 528, pol, a.OK, a.OKBG))
    x += len(pol) * 14 * 0.62 + 26 + 10
a.add(a.text(66, 586, "no tiene:", 14, a.GREY, a.MONO))
x = 160
pos = {}
for pol in ["write", "reboot", "policy"]:
    a.add(a.pill(x, 566, pol, a.BAD, a.BADBG))
    pos[pol] = x
    x += int(len(pol) * 14 * 0.62 + 26) + 10
# resaltado de la política que falta
wr = int(len("reboot") * 14 * 0.62 + 26)
a.add(during(a, a.box(pos["reboot"] - 4, 562, wr + 8, 36, "none", a.BAD, rx=18, sw=2.5), 56, 74.5, still=1))

a.add(term(a, 600, 480, 552, ["user mesa.ayuda logged in", "from 192.168.88.10 via winbox"], title="/LOG/PRINT", size=15))
a.add(a.group(a.box(610, 516, 532, 52, "none", MINT, rx=8, sw=2), a.show(12, 25), still=0))
a.add(a.text(48, 640, "Con usuarios propios, el log dice quién fue. Con admin compartido, no dice nada útil.", 16, a.TXT, a.SANS, 600))

p, pre = out(2, 1)
a.write(p, title="Los controles de un usuario en RouterOS",
        desc="Animación en cuatro tiempos con el usuario mesa.ayuda del grupo monitoreo (políticas local, ssh, winbox, read y test; sin write, reboot ni policy). "
             "1: entra por WinBox desde 192.168.88.10: pasa el control de address (192.168.88.0/24) y el de política de entrada (winbox); se abre la sesión y el log anota "
             "user mesa.ayuda logged in from 192.168.88.10 via winbox. 2: pide /ip/address/print, que necesita read: se ejecuta. 3: pide /system/reboot, que necesita reboot: "
             "el grupo no la tiene y el router lo rechaza. 4: el mismo usuario intenta entrar desde 203.0.113.25: no coincide con address y el login no se acepta, aparte del firewall.",
        preview=[14, 40, 66, 92], prefix=pre)
