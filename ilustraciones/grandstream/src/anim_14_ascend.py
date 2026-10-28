#!/usr/bin/env python3
"""Lección 14 · teoría: varias FXO en una troncal; Ascend toma siempre la primera libre."""
from _anim_grandstream import G

g = G(T=24, fix=92, kicker="GRANDSTREAM · TRONCAL ANALÓGICA", title="Varias FXO en una troncal: sale por la primera libre")
g.steps([
    "Sale la llamada A: con Ascend, la troncal prueba el FXO1, está libre y lo toma.",
    "Sale la B con el FXO1 ocupado: la troncal pasa al FXO2.",
    "Corta la A: el FXO1 vuelve a quedar libre.",
    "Sale la C: Ascend arranca otra vez por el FXO1.",
])
K = [0, 25, 50, 75, 100]
LIBRE, USO = "#0A63B8", "#F29A1F"

g.add(g.node(48, 210, 220, 84, "Internas", "1001, 1002, 1003"))
g.add(g.node(420, 200, 300, 104, "Antel_Grupo", "FXO 1, 2 · Ascend", dark=True, tsize=22))
PX = 900
ys = [180, 262, 344, 426]
for i, y in enumerate(ys):
    g.add(g.box(PX, y, 252, 64, g.WHITE, g.LINE, rx=12))
    g.add(g.text(PX + 24, y + 40, f"FXO{i + 1}", 19, g.INK, g.MONO, 600))
    if i >= 2:
        g.add(g.text(PX + 232, y + 40, "sin línea", 15, g.GREY, g.SANS, 500, "end"))
# estados de FXO1 y FXO2
def estado(i, t0, t1, st):
    y = ys[i]
    col = USO if st == "uso" else LIBRE
    lab = "en uso" if st == "uso" else "libre"
    g.appear(g.box(PX, y, 252, 64, "none", col, rx=12, sw=3) + g.pillc(PX + 176, y + 18, lab, g.WHITE, col, size=15, h=28), t0, t1)
estado(0, 0, 9, "libre"); estado(0, 9, 52, "uso"); estado(0, 52, 84, "libre"); estado(0, 84, 100, "uso")
estado(1, 0, 34, "libre"); estado(1, 34, 100, "uso")

# líneas
g.add(f'<path d="M268 252H420" stroke="{g.LINE}" stroke-width="4"/>')
for y in ys[:2]:
    g.add(f'<path d="M720 252 L{PX} {y + 32}" stroke="{g.LINE}" stroke-width="3"/>')
# llamadas
def llamada(lbl, t0, port, col):
    g.token([(268, 252), (420, 252)], t0, t0 + 3, g.chip(lbl, bg=col, size=15, h=26))
    g.token([(720, 252), (PX, ys[port] + 32)], t0 + 3.5, t0 + 7, g.chip(lbl, bg=col, size=15, h=26))
    g.appear(g.pillc(PX - 70, ys[port] + 18, lbl, g.WHITE, col, size=15, h=28), t0 + 7, {"A": 52, "B": 100, "C": 100}[lbl])
llamada("A", 2, 0, g.CYAN)
llamada("B", 27, 1, g.BLUE)
llamada("C", 77, 0, g.OK)
# prueba del FXO1 ocupado
g.appear(g.mark(PX + 40, ys[0] - 2, False, 13) + g.text(PX - 10, ys[0] - 10, "ocupado", 15, g.BAD, g.SANS, 600, "end"), 29, 37)
g.appear(g.pillc(PX + 126, ys[0] + 18, "corta", g.GREY, g.SLATE, size=15, h=28), 50, 58)

g.add(g.note(48, 520, 1104, None, ["DAHDI Out Line Selection: Ascend (de fábrica) empieza siempre por el 1; Poll alterna; Descend arranca por la última."], "info"))
g.add(g.note(48, 590, 1104, None, ["Para entrar, la ruta es por troncal: si las líneas van a destinos distintos, cada una lleva su propia troncal."], "amb"))

g.finish(14, 1, "Varias FXO en una troncal: sale por la primera libre",
         "Animación en cuatro tiempos con las internas 1001 a 1003, una troncal Antel_Grupo con los FXO 1 y 2 en modo Ascend y los cuatro FXO del UCM a la derecha (el 3 y el 4 sin línea). "
         "1: sale la llamada A; la troncal prueba el FXO1, está libre y lo toma, que pasa a en uso. "
         "2: sale la llamada B; el FXO1 está ocupado, así que la troncal la manda por el FXO2. "
         "3: la llamada A corta y el FXO1 vuelve a libre. "
         "4: sale la llamada C y Ascend arranca otra vez por el FXO1. "
         "Notas: DAHDI Out Line Selection en Ascend, el de fábrica, empieza siempre por el puerto 1; Poll alterna y Descend arranca por la última. Para las entrantes la ruta es por troncal, así que si las líneas van a destinos distintos cada una lleva su troncal.",
         [12, 37, 62, 92])
