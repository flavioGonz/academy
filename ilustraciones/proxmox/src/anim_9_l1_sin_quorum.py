#!/usr/bin/env python3
"""Lección 9 · Laboratorio, paso 4: apagás pve2 en un clúster de dos nodos. pve1 deja de recibir sus mensajes,
Total votes baja a 1 con Quorum 2, Quorate pasa a No, /etc/pve queda en solo lectura y crear una VM falla.
Fuentes: guía de administración (pvecm status: Expected votes, Total votes, Quorum, Flags; sin quórum /etc/pve
solo lectura), tarjeta de la lección (paso 4)."""
from _anim_pmx_red import *

a = new(24, "Tres votos", "Apagás pve2: lo que cambia en pvecm status", lab=True)
a.steps([
    "Los dos nodos se ven: 2 votos de 2 esperados, Quorate: Yes.",
    "Apagás pve2: pve1 deja de recibir sus mensajes de corosync.",
    "Total votes 1, Quorum 2: sin mayoría, /etc/pve queda en solo lectura.",
    "Probás crear una VM en pve1: no te deja.",
], still=2)

a.add(dev(a, 48, 186, 300, 84, "pve1 · 10.10.10.11", "1 voto", icon="server", dark=True, tsize=18))
at(a, dev(a, 48, 420, 300, 84, "pve2 · 10.10.10.12", "1 voto", icon="server", dark=True, tsize=18), 0, 26)
at(a, a.box(48, 420, 300, 84, a.SLATE, a.LINE, rx=14, sw=2, extra='stroke-dasharray="8 6"') + glyph(a, "server", 66, 438, a.GREY)
   + a.text(110, 454, "pve2 · apagado", 18, a.GREY, a.SANS, 600) + a.text(110, 478, "sin voto", 15, a.GREY, a.MONO), 26, 100, still=1)
at(a, line(198, 270, 198, 420, a.BLUE, 4), 0, 27)
at(a, line(198, 270, 198, 420, a.LINE, 4, "8 8"), 27, 100, still=1)
for t in (2, 10, 18):
    a.add(travel(a, f'<circle r="8" fill="{a.CYAN}"/>', [(198, 412), (198, 278)], t, t + 3, hold=0.2, fade=0.2))
    a.add(travel(a, f'<circle r="8" fill="{a.CYAN}"/>', [(198, 278), (198, 412)], t + 4, t + 7, hold=0.2, fade=0.2))
at(a, chip(a, 216, 330, "corosync", "info"), 0, 27)
at(a, xmark(a, 198, 345) + a.text(222, 351, "nada llega", 15, a.BAD, a.SANS, 600), 30, 50)
# /etc/pve
at(a, chip(a, 48, 290, "/etc/pve: lectura y escritura", "ok"), 0, 50)
at(a, chip(a, 48, 290, "/etc/pve: solo lectura", "bad"), 52, 100, still=1)

# terminal
TX, TY, TW, TH = 392, 182, 760, 412
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
a.add(tline(a, TX + 20, TY + 60, "# pvecm status", MINT))
L = [TY + 92 + i * 26 for i in range(10)]
a.add(tline(a, TX + 20, L[0], "Quorum information", SKY))
at(a, tline(a, TX + 20, L[1], "Quorate:          Yes", MINT), 0, 52)
at(a, tline(a, TX + 20, L[1], "Quorate:          No", CORAL), 52, 100, still=1)
a.add(tline(a, TX + 20, L[3], "Votequorum information", SKY))
a.add(tline(a, TX + 20, L[4], "Expected votes:   2"))
a.add(tline(a, TX + 20, L[5], "Highest expected: 2"))
a.add(tline(a, TX + 20, L[6], "Total votes:"))
at(a, tline(a, TX + 182, L[6], "2"), 0, 40)
at(a, tline(a, TX + 182, L[6], "1", GOLD), 40, 100, still=1)
a.add(tline(a, TX + 20, L[7], "Quorum:           2"))
at(a, tline(a, TX + 182 + 27, L[7], "Activity blocked", CORAL), 52, 100, still=1)
a.add(tline(a, TX + 20, L[8], "Flags:"))
at(a, tline(a, TX + 182, L[8], "Quorate", MINT), 0, 52)
at(a, a.box(TX + 12, L[6] - 20, 300, 28, "none", GOLD, rx=6, sw=2), 40, 52)
# paso 4
at(a, a.box(TX + 12, TY + TH - 92, TW - 24, 80, "#3A1F1A", rx=10) + tline(a, TX + 28, TY + TH - 62, "# qm create 120 --name prueba ...", MINT)
   + tline(a, TX + 28, TY + TH - 32, "cluster not ready - no quorum?", CORAL), 78, 100)
at(a, tline(a, TX + 20, TY + TH - 40, "1 de 2 no es mayoría: hacen falta 2", SKY), 52, 76, still=1)

status(a, 632, [
    (0, 25, "Con dos nodos, el quórum es 2: hace falta que estén los dos.", a.INK, 0),
    (25, 50, "Para pve1 no hay diferencia entre pve2 apagado y un cable de corosync cortado.", a.AMB, 0),
    (50, 75, "Sin quórum nada cambia: ni crear, ni arrancar, ni que la HA actúe.", a.BAD, 1),
    (75, 100, "Esto es lo que resuelve el QDevice del paso 5: un tercer voto.", a.BLUE, 0),
])

write(a, 9, "l1", "Apagás pve2: lo que cambia en pvecm status",
      "Animación en cuatro tiempos con pve1 en 10.10.10.11, pve2 en 10.10.10.12 y la salida de pvecm status en pve1. "
      "1: los dos nodos se pasan mensajes de corosync; pvecm status muestra Expected votes 2, Total votes 2, Quorum 2, Flags Quorate y Quorate: Yes; /etc/pve acepta lectura y escritura. "
      "2: se apaga pve2 y a pve1 no le llega nada; para pve1 es lo mismo que un cable de corosync cortado. Total votes baja a 1. "
      "3: con Total votes 1 y Quorum 2 no hay mayoría: la línea Quorum dice Activity blocked, Quorate pasa a No y /etc/pve queda en solo lectura; no se crea, no se arranca y la HA no actúa. "
      "4: qm create en pve1 falla con cluster not ready - no quorum?. Es lo que resuelve el QDevice del paso 5 con un tercer voto.",
      [8, 36, 62, 66, 92])
