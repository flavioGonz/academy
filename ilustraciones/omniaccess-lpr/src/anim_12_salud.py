"""Teoría de Lecturas que faltan: la salud de dispositivos abre y cierra alertas con umbrales distintos."""
from _anim_lpr import *

caps = ["Cada sondeo deja una muestra; se guardan 14 días.",
        "Un sondeo sin respuesta no abre nada: con dos seguidos, se abre la alerta.",
        "Memoria: abre al pasar 95 % y recién cierra al bajar de 90 %.",
        "Reloj: se abre con más de 120 s de diferencia contra el servidor."]
a = new(24, "Salud", "Salud de dispositivos: alertas que no parpadean", caps, still=2)
S = [sp[0] for sp in a.spans]

# A · sondeos
AX, AY, AW, AH = 48, 176, 540, 230
a.add(a.box(AX, AY, AW, AH, a.WHITE, a.LINE))
a.add(a.text(AX + 20, AY + 34, "Sondeos · P1 - Entrada (21)", 18, a.INK, a.SANS, 600))
states = ["ok"] * 6 + ["fail", "ok", "fail", "fail2", "ok", "ok"]
DY = AY + 110
for k, st in enumerate(states):
    x = AX + 40 + k * 42
    t = (S[0] + 2 + k * 3.6) if k < 6 else (S[1] + [1, 4, 7, 10, 17, 20][k - 6])
    c = {"ok": a.OK, "fail": a.AMB, "fail2": a.BAD}[st]
    inner = f'<circle cx="{x}" cy="{DY}" r="13" fill="{c}"/>'
    if st != "ok":
        inner += f'<path d="M{x - 5} {DY - 5} L{x + 5} {DY + 5} M{x + 5} {DY - 5} L{x - 5} {DY + 5}" stroke="#FFFFFF" stroke-width="3"/>'
    a.add(a.group(inner, a.show(t, 100, 0.5), still=1))
a.add(f'<line x1="{AX + 24}" y1="{DY + 26}" x2="{AX + AW - 24}" y2="{DY + 26}" stroke="{a.LINE}" stroke-width="2"/>')
a.add(a.text(AX + 20, DY + 56, "una muestra por sondeo · historial de 14 días", 15, a.GREY, a.MONO, 600))
x6, x9, x10 = AX + 40 + 6 * 42, AX + 40 + 8 * 42, AX + 40 + 9 * 42
a.add(a.group(a.text(x6, DY - 26, "1", 15, a.AMB, a.MONO, 600, "middle"), a.show(S[1] + 2, 100, .5), still=1))
a.add(a.group(a.text(x10 - 21, DY - 26, "2 seguidos", 15, a.BAD, a.MONO, 600, "middle"), a.show(S[1] + 10, 100, .5), still=1))
a.add(a.group(a.pill(AX + 20, AY + AH - 34, "Sin respuesta: abierta", a.WHITE, a.BAD, size=14), a.show(S[1] + 10, S[1] + 17, .5), still=0))
a.add(a.group(a.pill(AX + 20, AY + AH - 34, "Sin respuesta: cerrada", a.OK, a.OKBG, size=14), a.show(S[1] + 17, 100, .5), still=1))

# B · memoria
BX, BY, BW, BH = 612, 176, 540, 230
a.add(a.box(BX, BY, BW, BH, a.WHITE, a.LINE))
a.add(a.text(BX + 20, BY + 34, "Memoria · NVR de prueba", 18, a.INK, a.SANS, 600))
gx0, gx1, gy0, gy1 = BX + 30, BX + BW - 124, BY + 200, BY + 58   # 80 % abajo, 100 % arriba
yv = lambda v: gy0 - (v - 80) / 20 * (gy0 - gy1)
vals = [86, 89, 92, 96, 97, 94, 92, 91, 89, 87]
xs = [gx0 + k * (gx1 - gx0) / (len(vals) - 1) for k in range(len(vals))]
pts = " ".join(f"{x:.1f},{yv(v):.1f}" for x, v in zip(xs, vals))
a.add(f'<polyline points="{pts}" fill="none" stroke="{a.BLUE}" stroke-width="3.5" stroke-linejoin="round"/>')
# cortina que revela la línea durante el tiempo 3
cover = a.box(0, gy1 - 14, gx1 - gx0 + 20, gy0 - gy1 + 28, a.WHITE, rx=0)
a.add('<defs><clipPath id="plot"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath></defs>' % (gx0 - 6, gy1 - 16, gx1 - gx0 + 12, gy0 - gy1 + 32))
s0, s1 = ph(a, 2)
a.add('<g clip-path="url(#plot)">' + a.group(cover, a.move([(0, gx0 - 4, 0), (s0 + 1, gx0 - 4, 0), (s1 - 3, gx1 + 8, 0), (100, gx1 + 8, 0)]),
              a.keyframes([(0, 1), (s1 - 3, 1), (s1 - 2.5, 0), (100, 0)]), still=0) + '</g>')
for v, lab, c in ((95, "95 % abre", a.BAD), (90, "90 % cierra", a.OK)):
    a.add(f'<line x1="{gx0}" y1="{yv(v)}" x2="{gx1}" y2="{yv(v)}" stroke="{c}" stroke-width="2" stroke-dasharray="6 5"/>')
    a.add(a.text(gx1 + 8, yv(v) + 5, lab, 15, c, a.MONO, 600))

frac = lambda k: s0 + 1 + (s1 - 4 - s0) * k / (len(vals) - 1)
a.add(a.group(a.pill(BX + BW - 20, BY + 16, "abierta · 96 %", a.WHITE, a.BAD, size=14, anchor="end"), a.show(frac(3), frac(8), .5), still=0))
a.add(a.group(a.pill(BX + BW - 20, BY + 16, "cerrada · 89 %", a.OK, a.OKBG, size=14, anchor="end"), a.show(frac(8), 100, .5), still=1))
a.add(a.group(a.text(xs[6], yv(82), "entre 95 y 90 %: sigue abierta", 14, a.BAD, a.MONO, 600, "middle"), a.show(frac(5), 100, .5), still=1))

# C · reloj
CY = 432
a.add(a.box(48, CY, 1104, 120, a.WHITE, a.LINE))
a.add(a.text(68, CY + 34, "Reloj · desfase contra el servidor", 18, a.INK, a.SANS, 600))
X0, X1 = 68, 1000
px = (X1 - X0) / 180
a.add(a.box(X0, CY + 58, X1 - X0, 22, a.SLATE, rx=11))
a.add(f'<line x1="{X0 + 120 * px}" y1="{CY + 50}" x2="{X0 + 120 * px}" y2="{CY + 88}" stroke="{a.BAD}" stroke-width="3"/>')
a.add(a.text(X0 + 120 * px, CY + 108, "120 s", 15, a.BAD, a.MONO, 600, "middle"))
a.add(a.text(X0, CY + 108, "0 s", 15, a.GREY, a.MONO, 600))
s0, s1 = ph(a, 3)
fill = a.keyframes([(0, 0.25), (s0 + 1, 0.25), (s1 - 4, 1), (100, 1)], "transform", "scaleX({})")
a.add(a.group(a.box(X0, CY + 58, 150 * px, 22, a.AMB, rx=11), fill, a.show(s0, 100, .3), still=0, origin=f"{X0}px {CY + 69}px"))
a.add(a.group(a.box(X0, CY + 58, 0.25 * 150 * px, 22, a.OK, rx=11), a.show(0, s0, .3), still=1))
tcross = s0 + 1 + (s1 - 5 - s0) * ((120 / 150 - .25) / .75)
a.add(a.group(a.pill(1132, CY + 56, "alerta de reloj", a.WHITE, a.BAD, size=14, anchor="end"), a.show(tcross, 100, .5), still=0))

a.add(a.text(48, 590, "Cada alerta guarda su motivo y se cierra sola cuando el equipo vuelve a estar bien.", 17, a.TXT))
a.add(a.text(48, 622, "Dispositivos → historial y alertas de cada equipo", 16, a.BLUE, a.MONO, 600))
write(a, "12-t1.svg", "Salud de dispositivos", [20, 42, 58, 72, 96])
