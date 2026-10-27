#!/usr/bin/env python3
"""Lección 39 · Teoría · Cerradura NC o NO: qué pasa con la tensión en el tiempo.
Sale de teoria_md: Always con cerradura NC (12 V en reposo, trabada; al abrir el relé corta y se libera; vuelve
la energía), Triggered by Open Relay con cerradura NO (sin tensión en reposo, trabada; al abrir recibe 12 V
el tiempo configurado). Historia: las que abren sin energía (fail-safe) y las que quedan trabadas sin energía
(fail-secure), que Akuvox nombra por el borne: NC y NO. Límite de corriente por modelo."""
from _anim_akuvox_29_42 import new, out, when

a = new(24, "ACCESORIOS · CERRADURAS", "Cerradura NC o NO: la tensión en el tiempo")
a.steps([
    "Reposo: la NC recibe 12 V y queda trabada. La NO no recibe tensión y también.",
    "Abrir: el relé conmuta. La NC pierde los 12 V, la NO los recibe: las dos se liberan.",
    "El relé vuelve: la NC recupera los 12 V y la NO los pierde. Trabadas otra vez.",
    "Sin energía: la NC se libera (salida de emergencia) y la NO queda trabada.",
], still=1)

GX0, GX1 = 330, 900
Q = (GX1 - GX0) / 4
PH = ["reposo", "abrir", "vuelve", "sin energía"]
for i, p in enumerate(PH):
    a.add(a.text(GX0 + Q * i + Q / 2, 196, p, 15, a.GREY, a.MONO, 600, "middle"))
    if i:
        a.add(f'<line x1="{GX0 + Q * i}" y1="206" x2="{GX0 + Q * i}" y2="584" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')


def lock(cx, cy, opened, color):
    sh = (f'<path d="M{cx - 14} {cy - 6} V{cy - 30} a14 14 0 0 1 28 0 V{cy - 22}" fill="none" stroke="{color}" stroke-width="5"/>' if opened
          else f'<path d="M{cx - 14} {cy - 6} V{cy - 20} a14 14 0 0 1 28 0 V{cy - 6}" fill="none" stroke="{color}" stroke-width="5"/>')
    return sh + f'<rect x="{cx - 24}" y="{cy - 8}" width="48" height="40" rx="7" fill="{color}"/>'


def row(y0, title, sub, levels, states):
    """levels: 4 valores (True = 12 V); states: 4 valores (True = liberada)."""
    a.add(a.box(48, y0, 1104, 176, a.WHITE, a.LINE, rx=18))
    a.add(a.text(72, y0 + 44, title, 21, a.INK, a.HEAD, 600))
    for k, line in enumerate(sub.split(" · ")):
        a.add(a.text(72, y0 + 70 + k * 22, line, 15, a.GREY, a.MONO))
    hi, lo = y0 + 50, y0 + 130
    a.add(a.text(GX0 - 10, hi + 5, "12 V", 15, a.TXT, a.MONO, 600, "end"))
    a.add(a.text(GX0 - 10, lo + 5, "0 V", 15, a.TXT, a.MONO, 600, "end"))
    a.add(f'<line x1="{GX0}" y1="{lo}" x2="{GX1}" y2="{lo}" stroke="{a.LINE}" stroke-width="2"/>')
    d, prev = "", None
    for i, lv in enumerate(levels):
        y = hi if lv else lo
        x = GX0 + Q * i
        d += (f"M{x} {y}" if prev is None else f" V{y}") + f" H{x + Q}"
        prev = y
    a.add(f'<path d="{d}" fill="none" stroke="#D2492F" stroke-width="4" stroke-linejoin="round"/>')
    # estado de la cerradura por fase
    for i, st in enumerate(states):
        t0, t1 = 25 * i, 25 * (i + 1)
        c = a.OK if st else a.INK
        g = lock(1000, y0 + 92, st, c) + a.text(1040, y0 + 100, "liberada" if st else "trabada", 17, a.OK if st else a.INK, a.SANS, 600)
        when(a, g, t0 + (0.6 if i else 0), t1, still=1 if i == 1 else 0, fade=0.6)
        # tramo resaltado de la fase actual
        when(a, f'<rect x="{GX0 + Q * i}" y="{y0 + 30}" width="{Q}" height="120" fill="{a.CYAN}" opacity=".08"/>', t0, t1, still=1 if i == 1 else 0, fade=0.6)


row(210, "Cerradura NC", "GND + NC · Always", [True, False, True, False], [False, True, False, True])
row(404, "Cerradura NO", "GND + NO · Triggered by Open Relay", [False, True, False, False], [False, True, False, False])

# cursor del tiempo
cur = f'<line x1="0" y1="206" x2="0" y2="584" stroke="{a.BLUE}" stroke-width="3"/><circle cx="0" cy="206" r="6" fill="{a.BLUE}"/>'
a.add(a.group(cur, a.move([(0, GX0, 0), (100, GX1, 0)]), a.show(0, 100), still=0))

a.add(a.text(48, 622, "Límite por modelo: 500 mA en el R29 V1.1, 1 A en el X915S.", 18, a.INK, a.SANS, 600))
a.add(a.text(48, 648, "Si la cerradura pide más, va con fuente propia y el relé solo conmuta.", 17, a.TXT, a.SANS, 600))

out(a, 39, 1, "Cerradura NC o NO: la tensión en el tiempo",
    "Animación con dos gráficos de tensión en el tiempo, uno para la cerradura NC (entre GND y NC, salida en Always) y otro para la NO (entre GND y NO, salida en Triggered by Open Relay), con un cursor que avanza y el estado de cada cerradura a la derecha. "
    "Tiempo 1, reposo: la NC tiene 12 V y está trabada; la NO tiene 0 V y está trabada. "
    "Tiempo 2, abrir: el relé conmuta; la NC baja a 0 V y se libera; la NO sube a 12 V durante el tiempo configurado y se libera. "
    "Tiempo 3, el relé vuelve: la NC vuelve a 12 V y la NO a 0 V; las dos trabadas. "
    "Tiempo 4, sin energía: las dos quedan en 0 V; la NC se libera, como en una salida de emergencia, y la NO queda trabada. "
    "Abajo: el límite de corriente es por modelo, 500 mA en el R29 V1.1 y 1 A en el X915S; si la cerradura pide más, fuente propia.",
    [12, 37, 62, 88])
