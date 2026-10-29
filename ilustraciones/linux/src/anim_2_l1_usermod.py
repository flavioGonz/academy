#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 1: usermod -aG tecnicos. Con -a el grupo se agrega a los secundarios;
con -G solo, la lista de secundarios se reemplaza (y se pierde, por ejemplo, sudo). El grupo nuevo vale para
las sesiones que empiezan después: id <usuario> lo muestra, pero la sesión ya abierta sigue con los grupos viejos.
Fuentes: usermod(8) (-G reemplaza la lista de grupos suplementarios; -a, con -G, agrega) y la teoría de la lección."""
from _anims_lnx_rl import *

a = nueva(24, "LINUX · GRUPOS · LABORATORIO", "usermod -aG suma; sin la a, reemplaza")
a.steps([
    "Tu usuario tecnico está en sudo (ejemplo): lo dice id tecnico.",
    "usermod -G tecnicos, sin la a: la lista se reemplaza y sudo se va.",
    "Desde el principio, con -aG: tecnicos se suma y sudo queda.",
    "El grupo vale desde la próxima sesión: salí y volvé a entrar.",
], still=2)

# ---- tarjeta de grupos
CX, CY, CW, CH = 48, 176, 560, 300
a.add(a.box(CX, CY, CW, CH, a.WHITE, a.LINE, rx=16) + a.text(CX + 22, CY + 38, "Grupos de tecnico", 19, a.INK, a.HEAD, 600))
a.add(a.text(CX + 22, CY + 84, "principal", 15, a.GREY, a.SANS, 600) + a.text(CX + 22, CY + 164, "secundarios", 15, a.GREY, a.SANS, 600))
a.add(a.pill(CX + 140, CY + 64, "tecnico", a.INK, a.SLATE, 16, 32))
a.add(a.text(CX + 270, CY + 86, "usermod -G no lo toca", 15, a.GREY, a.SANS, 500))
SX, SY = CX + 140, CY + 144
# sudo: presente 0-25, tachado 25-37, ausente 37-50, presente 50-100
ventanas(a, a.pill(SX, SY, "sudo", a.BLUE, "#E5F0FB", 16, 32), [(0, 30), (50, 100)], still=1)
en(a, a.pill(SX, SY, "sudo", a.BAD, a.BADBG, 16, 32) + linea(SX + 6, SY + 16, SX + 76, SY + 16, a.BAD, 3), 30, 50)
en(a, a.text(SX, SY + 60, "sudo se perdió: ya no podés administrar", 15, a.BAD, a.SANS, 700), 33, 50)
# tecnicos
en(a, a.pill(SX + 100, SY, "tecnicos", a.AMB, a.AMBBG, 16, 32), 28, 50)
en(a, a.pill(SX + 100, SY, "tecnicos", a.OK, a.OKBG, 16, 32), 58, 100, still=1)
en(a, a.text(SX, SY + 60, "sudo queda y tecnicos se suma al final", 15, a.OK, a.SANS, 700), 60, 75, still=1)
en(a, a.text(SX, SY + 60, "en la base de usuarios ya está", 15, a.OK, a.SANS, 700), 75, 100)
# flechas de cambio
viaje(a, "-G tecnicos", [(SX + 340, SY - 40), (SX + 150, SY - 4)], 26, 29, bg=a.BAD, size=14, hold=3)
viaje(a, "-aG tecnicos", [(SX + 340, SY - 40), (SX + 150, SY - 4)], 54, 57.5, bg=a.OK, size=14, hold=3)
en(a, a.box(CX + 10, CY + 110, CW - 20, 120, "none", a.BAD, rx=12, sw=3), 30, 50)
en(a, a.box(CX + 10, CY + 110, CW - 20, 120, "none", a.OK, rx=12, sw=3), 58, 75, still=1)

# ---- terminal
TX, TY, TW, TH = 632, 176, 520, 300
a.add(tterm(a, TX, TY, TW, TH, "TERMINAL"))
def filas(rows, t0, t1, still=0):
    s = ""
    for i, r in enumerate(rows):
        s += trow(a, TX, TY + 60 + i * 30, r, 15)
    en(a, s, t0, t1, still)


filas(["$ id tecnico", ("uid=1000(tecnico) gid=1000(tecnico)", T_OUT), ("groups=1000(tecnico),27(sudo)", T_OK)], 0, 25)
filas(["$ sudo usermod -G tecnicos tecnico", "$ id tecnico", ("uid=1000(tecnico) gid=1000(tecnico)", T_OUT),
       ("groups=1000(tecnico),1003(tecnicos)", T_ERR), ("# sin la a: se fue 27(sudo)", T_WARN)], 25, 50)
filas(["$ sudo usermod -aG tecnicos tecnico", "$ id tecnico", ("uid=1000(tecnico) gid=1000(tecnico)", T_OUT),
       ("groups=1000(tecnico),27(sudo),1003(tecnicos)", T_OK), ("# la a agrega: sudo sigue", T_COM)], 50, 75, still=1)
filas([("# en la sesión que ya estaba abierta:", T_COM), "$ id", ("groups=1000(tecnico),27(sudo)", T_WARN),
       ("# todavía sin tecnicos", T_COM), ("# salí y volvé a entrar; después:", T_COM), "$ id", ("groups=...,27(sudo),1003(tecnicos)", T_OK)], 75, 100)
a.add(a.text(TX, TY + TH + 24, "números de grupo de ejemplo", 15, a.GREY, a.SANS, 500))

# ---- línea de tiempo de sesiones (paso 4)
LY = 540
en(a, a.text(48, LY - 16, "sesión abierta antes del cambio", 15, a.AMB, a.SANS, 600)
   + a.box(48, LY - 4, 520, 14, a.AMBBG, a.AMB, rx=7, sw=1.5)
   + a.text(48 + 560, LY + 8, "usermod", 15, a.INK, a.MONO, 700)
   + linea(600, LY - 24, 600, LY + 24, a.INK, 2, "4 4")
   + a.text(680, LY - 16, "sesión nueva", 15, a.OK, a.SANS, 600)
   + a.box(680, LY - 4, 472, 14, a.OKBG, a.OK, rx=7, sw=1.5), 75, 100)
en(a, a.text(48, LY + 36, "sus grupos se fijaron al entrar", 15, a.TXT, a.SANS, 500)
   + a.text(680, LY + 36, "ya entra con tecnicos", 15, a.OK, a.SANS, 600), 78, 100)

narr(a, [
    (0, 25, "Antes de tocar grupos, mirá cuáles tiene el usuario.", None),
    (25, 50, "-G sin -a deja solo los grupos que nombrás: si era tu usuario, perdiste sudo.", a.BAD),
    (50, 75, "Con -aG, la lista crece y nada se pierde.", a.OK),
    (75, 100, "Los grupos de una sesión se cargan al entrar: el cambio aplica en la próxima.", None),
], still_idx=2)

escribir(a, "2-l1", "usermod -aG suma; sin la a, reemplaza",
         "Animación en cuatro tiempos con la tarjeta de grupos del usuario tecnico a la izquierda, con su grupo principal tecnico y los secundarios, y una terminal a la derecha. "
         "1: id tecnico muestra groups con tecnico y 27(sudo). "
         "2: sudo usermod -G tecnicos tecnico, sin la a, reemplaza la lista: id muestra tecnico y tecnicos, sudo aparece tachado en rojo y ya no se puede administrar. "
         "3: desde el principio, con sudo usermod -aG tecnicos tecnico, tecnicos se suma al final y sudo queda, en verde. "
         "4: en la sesión que ya estaba abierta, id todavía no muestra tecnicos; una línea de tiempo muestra que los grupos se fijan al entrar y que la sesión nueva ya entra con tecnicos. Los números de grupo son de ejemplo.",
         [10, 36, 64, 90])
