#!/usr/bin/env python3
"""Teoría lección 12 (Backup primero): la migración tiene un orden porque cada paso depende del anterior;
Forget antes de tiempo deja los equipos sin controlador.
Salida: site2/ilustraciones/omada/12-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(26, "MIGRACIÓN", "Forget recién cuando el destino tiene todo")
F = a.steps([
    "Exportar e importar: el destino ya conoce los equipos.",
    "Los equipos reciben la nueva dirección (IP o Inform URL) y quedan Connected.",
    "Recién con todos Connected en el destino, Forget en el viejo.",
    "Al revés: Forget antes de tiempo y los equipos quedan sin controlador.",
], still=2)
(a0, a1), (b0, b1), (c0, c1), (d0, d1) = F

OX, NX, PW, PY, PH = 48, 852, 300, 180, 300
a.add(a.box(OX, PY, PW, PH, a.WHITE, a.LINE) + a.box(NX, PY, PW, PH, a.WHITE, a.LINE))
a.add(nodo(a, OX + 14, PY + 14, PW - 28, 62, "Controlador viejo", "origen", tsize=19))
a.add(nodo(a, NX + 14, PY + 14, PW - 28, 62, "Controlador nuevo", "misma versión", tsize=19))
DEV = ["EAP 1", "EAP 2", "Switch"]
RY = [PY + 96 + i * 62 for i in range(3)]


def filas(x):
    for nom, y in zip(DEV, RY):
        a.add(a.box(x + 14, y, PW - 28, 52, a.SLATE, None, rx=10) + a.text(x + 30, y + 32, nom, 17, a.INK, a.SANS, 600))


filas(OX)
filas(NX)


def st(x, y, label, fg, bg):
    return chip(a, x + PW - 26, y + 11, label, fg, bg, anchor="end", stroke=fg)


# --- estados en el viejo
for i, y in enumerate(RY):
    tmig = b0 + 4 + i * 4
    en(a, st(OX, y, "Connected", a.OK, a.OKBG), 0, tmig)
    en(a, st(OX, y, "migrado", a.GREY, a.WHITE), tmig, c0 + 3 + i * 3)
    # Forget en orden (fase 3): la fila desaparece
    tap = a.box(OX + 10, y - 2, PW - 20, 56, a.WHITE, None, rx=10) + a.text(OX + PW / 2, y + 32, "Forget", 16, a.GREY, a.MONO, 600, "middle")
    en(a, tap, c0 + 3 + i * 3, c1, still=1)
    # fase 4: Connected y Forget antes de tiempo
    en(a, st(OX, y, "Connected", a.OK, a.OKBG), d0, d0 + 4)
    en(a, a.box(OX + 10, y - 2, PW - 20, 56, a.BADBG, None, rx=10) + a.text(OX + PW / 2, y + 32, "Forget antes de tiempo", 16, a.BAD, a.MONO, 600, "middle"), d0 + 4, d1)

# --- estados en el nuevo
for i, y in enumerate(RY):
    tcon = b0 + 4 + i * 4
    en(a, st(NX, y, "importado", a.GREY, a.WHITE), a0 + 12, tcon)
    en(a, st(NX, y, "Connected", a.OK, a.OKBG), tcon, c1, still=1)
    en(a, st(NX, y, "importado", a.GREY, a.WHITE), d0, d1)
en(a, a.box(NX + 10, PY + 90, PW - 20, 190, a.WHITE, None, rx=10) + a.text(NX + PW / 2, PY + 190, "todavía vacío", 16, a.GREY, a.MONO, 600, "middle"), 0, a0 + 12)

# --- exportar e importar
cfg = paquete(a, "backup .cfg", a.BLUE)
viaje(a, cfg, OX + PW + 80, PY + 46, NX - 80, PY + 46, a0 + 3, a0 + 11, hold=a1 - a0 - 12)
en(a, a.text(600, PY + 92, "misma Major.Minor.Patch", 15, a.BLUE, a.MONO, 600, "middle"), a0 + 3, a1)

# --- los equipos físicos
EX, EY, EW = 470, 400, 260
a.add(a.box(EX, EY, EW, 92, a.WHITE, a.LINE))
for i, nom in enumerate(DEV):
    cx = EX + 50 + i * 80
    a.add(eap(a, cx, EY + 34, 18) if i < 2 else a.box(cx - 24, EY + 22, 48, 24, a.INK, rx=5))
    a.add(a.text(cx, EY + 76, nom, 15, a.TXT, a.SANS, 600, "middle"))
# a quién le hablan
viejo = a.arrow(f"M{EX - 4} {EY + 46} H{OX + PW + 8}", a.BLUE, 3)
nuevo = a.arrow(f"M{EX + EW + 4} {EY + 46} H{NX - 8}", a.OK, 3)
en(a, viejo + a.text(EX + EW / 2, EY + 124, "hablan con el viejo", 15, a.BLUE, a.MONO, 600, "middle"), 0, b0 + 4)
en(a, nuevo + a.text(EX + EW / 2, EY + 124, "nueva dirección: IP o Inform URL", 15, a.OK, a.MONO, 600, "middle"), b0 + 4, c1, still=1)
en(a, viejo, d0, d0 + 4)
en(a, a.box(EX - 4, EY - 4, EW + 8, 100, "none", a.BAD, rx=16, sw=3) + chip(a, EX + EW / 2, EY + 106, "sin controlador", a.BAD, a.BADBG, anchor="middle", stroke=a.BAD), d0 + 5, d1)

pie(a, F, [
    "Desde la 5.13.11.41, solo se importa un archivo de la misma Major.Minor.Patch.",
    "Cada paso depende del anterior: el destino ya los conoce y los adopta.",
    "Antes de todo: backup descargado fuera del equipo y ventana de mantenimiento.",
    "Nadie los gestiona hasta que alguien les diga a qué controlador ir.",
], y=640, still=2, colores=[a.INK, a.INK, a.INK, a.BAD])

salida(a, 12, 1, "Forget recién cuando el destino tiene todo",
       "Animación en cuatro tiempos con el controlador viejo, el nuevo de la misma versión y tres equipos: EAP 1, EAP 2 y un switch. "
       "1: se exporta el backup .cfg y se importa en el destino, que ahora conoce los equipos como importados; la versión tiene que ser la "
       "misma Major.Minor.Patch. 2: los equipos reciben la nueva dirección, por IP o Inform URL, y uno por uno quedan Connected en el destino "
       "y migrados en el viejo. 3: recién con todos Connected en el destino se hace Forget en el viejo. 4: al revés, con Forget antes de tiempo "
       "en el viejo, los equipos quedan sin controlador y el destino los tiene solo importados.",
       [12, 40, 66, 90])
