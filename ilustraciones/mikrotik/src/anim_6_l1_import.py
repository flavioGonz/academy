#!/usr/bin/env python3
"""Lección 6 · Laboratorio, paso 4: /import verbose=yes dry-run lee el archivo línea por línea y simula sin
aplicar nada. Sin dry-run, verbose para en la línea que falla y muestra dónde, pero lo anterior ya se aplicó.
Fuente: Configuration Management (verbose, dry-run solo con verbose; import con verbose muestra el lugar del fallo)."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · BACKUP PRIMERO · LABORATORIO", title="El import lee el archivo línea por línea")
a.steps([
    "verbose=yes dry-run: recorre despues.rsc línea por línea y no aplica nada.",
    "Termina la simulación: la configuración del equipo sigue igual.",
    "Sin dry-run, en un equipo sin ether5: para en esa línea y te dice dónde.",
    "Lo de antes ya se aplicó. Corregís el .rsc y lo probás otra vez en seco.",
], still=2)

FX, FY, FW = 48, 180, 520
LINES = ["# <fecha> by RouterOS 7.x", "/interface bridge", "add name=bridge", "/interface bridge port",
         "add bridge=bridge interface=ether5", "/system identity", "set name=LAB-MT01"]
LH = 40
a.add(a.box(FX, FY, FW, 64 + LH * len(LINES), a.WHITE, a.LINE, rx=16))
a.add(glyph(a, "card", FX + 18, FY + 12, a.BLUE, 1.1))
a.add(a.text(FX + 54, FY + 34, "despues.rsc", 17, a.INK, a.MONO, 600))
Y0 = FY + 52


def ly(i):
    return Y0 + i * LH


# cursor que recorre (pasada 1: dry-run; pasada 2: real, frena en la línea 4)
cur = f'<rect x="{FX + 10}" y="0" width="{FW - 20}" height="{LH - 6}" rx="6" fill="#E3EEF9" stroke="{a.BLUE}" stroke-width="2"/>'
def steps_path(t0, dt, n, hold=0.7):
    pts = [(0, 0, ly(0)), (t0, 0, ly(0))]
    for i in range(1, n):
        ta = t0 + i * dt
        pts += [(ta - hold, 0, ly(i - 1)), (ta, 0, ly(i))]
    return pts + [(100, 0, ly(n - 1))]


p1 = steps_path(3, 2.8, len(LINES))
a.add(a.group(cur, a.move(p1), a.show(3, 24, 0.6), still=0))
p2 = steps_path(52, 2.6, 5)
a.add(a.group(cur, a.move(p2), a.show(52, 62, 0.6), still=0))
for i, t in enumerate(LINES):
    a.add(a.text(FX + 24, ly(i) + 24, t, 15, a.GREY if t.startswith("#") else a.INK, a.MONO, 400 if t.startswith("#") else 600))
bad = a.box(FX + 10, ly(4), FW - 20, LH - 6, a.BADBG, a.BAD, rx=6, sw=2) + a.text(FX + 24, ly(4) + 24, LINES[4], 15, a.BAD, a.MONO, 600)
a.add(during(a, bad, 62, 82, still=1))
fix = (a.box(FX + 10, ly(4), FW - 20, LH - 6, a.OKBG, a.OK, rx=6, sw=2)
       + a.text(FX + 24, ly(4) + 24, "add bridge=bridge interface=ether4", 15, a.OK, a.MONO, 600))
a.add(during(a, fix, 84, 100))
okrows = "".join(a.box(FX + 10, ly(i), FW - 20, LH - 6, "none", a.OK, rx=6, sw=1.5) for i in (1, 2))
a.add(during(a, okrows, 62, 100, still=1))
a.add(during(a, a.text(FX + FW - 24, ly(2) + 24, "ya aplicada", 15, a.AMB, a.MONO, 600, "end"), 62, 100, still=1))

# terminal y estado del equipo de prueba
TX, TW = 600, 552
a.add(a.box(TX, FY, TW, 240, a.INK, rx=16))
a.add(a.text(TX + 18, FY + 30, "EQUIPO DE PRUEBA · TERMINAL", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
OUT = [
    (0, 50, ["/import file-name=despues.rsc", "  verbose=yes dry-run"], a.WHITE, 0),
    (5, 25, ["leyendo línea por línea…", "nada se aplica"], SKY, 0),
    (25, 50, ["simulación terminada", "la configuración no cambió"], MINT, 0),
    (50, 100, ["/import file-name=despues.rsc", "  verbose=yes"], a.WHITE, 1),
    (62, 100, ["para en la línea con ether5:", "esa interfaz no existe acá"], "#FF9E8A", 1),
]
for t0, t1, ls, c, st in OUT:
    k = 0 if ls[0].startswith("/") else 1
    body = "".join(a.text(TX + 18 + (32 if l.startswith("  ") else 0), FY + 70 + k * 84 + j * 30, l.strip(), 15, c, a.MONO, 600 if c != a.WHITE else 400) for j, l in enumerate(ls))
    a.add(during(a, body, t0, t1, still=st))

SY = FY + 260
a.add(a.box(TX, SY, TW, 104, a.WHITE, a.LINE, rx=16))
a.add(a.text(TX + 18, SY + 32, "Configuración del equipo de prueba", 16, a.INK, a.SANS, 600))
a.add(during(a, a.pill(TX + 18, SY + 50, "sin cambios", a.OK, a.OKBG, 15, 30), 0, 50))
a.add(during(a, a.pill(TX + 18, SY + 50, "aplicando línea por línea…", a.BLUE, "#E3EEF9", 15, 30), 51, 62))
a.add(during(a, a.pill(TX + 18, SY + 50, "ya tiene el bridge nuevo", a.AMB, a.AMBBG, 15, 30)
             + a.text(TX + 300, SY + 71, "identity: sin cambiar", 15, a.TXT, a.MONO), 62, 100, still=1))

a.add(note(a, 48, 548, 1104, 74, "Por eso: primero en seco, y el import real en un equipo de prueba",
           ["La documentación recomienda importar en la misma versión de RouterOS."], "amb"))

write(a, 6, "l1", "Import en seco y con verbose",
      "Animación en cuatro tiempos con el archivo despues.rsc, la terminal del equipo de prueba y su configuración. "
      "1: /import file-name=despues.rsc verbose=yes dry-run recorre el archivo línea por línea y no aplica nada. "
      "2: la simulación termina y la configuración del equipo sigue sin cambios. "
      "3: el import real con verbose=yes, en un equipo que no tiene ether5, aplica las primeras líneas y para en add bridge=bridge interface=ether5, mostrando dónde falló. "
      "4: lo anterior ya se aplicó, porque el import ejecuta línea por línea; se corrige la interfaz en el .rsc, por ejemplo a ether4, y se prueba otra vez en seco. "
      "Conviene el import real en un equipo de prueba y en la misma versión de RouterOS.",
      [10, 36, 66, 90])
