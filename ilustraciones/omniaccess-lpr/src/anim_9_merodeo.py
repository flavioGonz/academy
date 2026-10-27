"""Teoría de Permanencia y merodeo: la ventana de 30 minutos, la tercera pasada y el silencio de 30 minutos."""
from _anim_lpr import *

caps = ["Con cada lectura con chapa, se cuentan las pasadas de los últimos 30 min.",
        "Segunda pasada, por otro acceso. La lectura sin chapa no cuenta.",
        "Tercera pasada y no es residente: alerta Merodeo y entrada en la bitácora.",
        "Cuarta pasada: no vuelve a avisar por esa matrícula durante 30 min.",
        "Un residente autorizado puede pasar varias veces: no abre alerta."]
a = new(26, "Merodeo", "Merodeo: una ventana de 30 minutos que cuenta pasadas", caps, still=2, size=17)

X0, X1 = 150, 1130
pm = (X1 - X0) / 60
tx = lambda m: X0 + m * pm
a.add('<defs><clipPath id="tl"><rect x="%d" y="0" width="%d" height="675"/></clipPath></defs>' % (X0, X1 - X0))


def axis(y, label, sub):
    s = a.text(48, y - 70, label, 18, a.INK, a.MONO, 600) + a.text(48 + len(label) * 11.5 + 14, y - 70, sub, 16, a.GREY)
    s += f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{a.GREY}" stroke-width="2"/>'
    for m in range(0, 61, 10):
        s += f'<line x1="{tx(m)}" y1="{y - 6}" x2="{tx(m)}" y2="{y + 6}" stroke="{a.GREY}" stroke-width="2"/>' + a.text(tx(m), y + 40, f"21:{m:02d}" if m < 60 else "22:00", 15, a.GREY, a.MONO, 600, "middle")
    return s


Y1 = 300
a.add(axis(Y1, "SCD5678", "no registrada"))
reads = [(0, "P1", 0), (10, "P2", 1), (25, "P1", 2), (32, "P2", 3)]
# ventana que acompaña a cada lectura
wpts = []
for m, _, st in reads:
    s0, s1 = ph(a, st)
    wpts += [(s0 + 1, tx(m) - 30 * pm, 0), (s1 - 0.5, tx(m) - 30 * pm, 0)]
win = f'<rect x="0" y="{Y1 - 28}" width="{30 * pm}" height="48" rx="8" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2" stroke-dasharray="6 5"/>' \
      + a.text(30 * pm - 10, Y1 - 36, "últimos 30 min", 15, a.BAD, a.MONO, 600, "end")
mv = a.move([(0, wpts[0][1], 0)] + [(p, x, y) for p, x, y in wpts] + [(100, wpts[-1][1], 0)])
a.add(f'<g clip-path="url(#tl)">' + a.group(win, mv, a.show(ph(a, 0)[0] + 1, ph(a, 3)[1] - 0.5), still=0) + '</g>')
a.add(f'<g clip-path="url(#tl)">' + a.group(f'<rect x="{tx(-5)}" y="{Y1 - 28}" width="{30 * pm}" height="48" rx="8" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2" stroke-dasharray="6 5"/>'
                                          + a.text(tx(25) - 10, Y1 - 36, "últimos 30 min", 15, a.BAD, a.MONO, 600, "end"),
                                          a.keyframes([(0, 0), (100, 0)]), still=1) + '</g>')
for m, acc, st in reads:
    vis(a, f'<circle cx="{tx(m)}" cy="{Y1}" r="11" fill="{a.BAD if st >= 2 else a.INK}"/>' + a.text(tx(m), Y1 + 66, acc, 15, a.INK, a.MONO, 600, "middle"), st, 3, d0=1)
vis(a, f'<circle cx="{tx(15)}" cy="{Y1}" r="10" fill="{a.WHITE}" stroke="{a.GREY}" stroke-width="3"/>' + a.text(tx(15), Y1 + 66, "sin chapa", 15, a.GREY, a.MONO, 600, "middle"), 1, 3, d0=4)
# contador
CXc = 1000
vis(a, a.box(CXc - 10, 168, 162, 62, a.WHITE, a.LINE, rx=12) + a.text(CXc + 6, 192, "pasadas", 15, a.GREY, a.MONO, 600), 0, 3)
for st, n, c in ((0, "1", a.INK), (1, "2", a.INK), (2, "3", a.BAD), (3, "3", a.BAD)):
    vis(a, a.text(CXc + 120, 220, n, 30, c, a.MONO, 600, "middle"), st, d0=1)
# alerta y bitácora
AY = 420
vis(a, a.box(48, AY, 520, 74, a.BAD, rx=12) + a.text(70, AY + 32, "Merodeo · SCD5678", 19, a.WHITE, a.SANS, 600)
    + a.text(70, AY + 58, "3 pasadas en 30 min · 2 accesos", 15, "#FFD9D1", a.MONO, 600), 2, 3, d0=2)
vis(a, a.box(590, AY, 562, 74, a.WHITE, a.LINE, rx=12) + a.text(612, AY + 32, "Bitácora", 18, a.INK, a.SANS, 600)
    + a.text(612, AY + 58, "21:25 · Merodeo SCD5678 · 3 pasadas", 15, a.TXT, a.MONO), 2, 3, d0=4)
vis(a, f'<rect x="{tx(25)}" y="{Y1 + 82}" width="{30 * pm}" height="10" rx="5" fill="{a.AMB}"/>', 3)
vis(a, a.text(tx(25) - 12, Y1 + 93, "sin aviso hasta 21:55", 15, a.AMB, a.SANS, 600, "end"), 3)
# 5 · residente
Y2 = 560
vis(a, axis(Y2, "SBA1234", "residente autorizado"), 4)
for m in (2, 8, 14, 21, 27):
    vis(a, f'<circle cx="{tx(m)}" cy="{Y2}" r="11" fill="{a.OK}"/>', 4, d0=1 + m / 6)
vis(a, a.pill(1152, Y2 - 66, "no abre alerta", a.OK, a.OKBG, size=15, anchor="end"), 4, d0=7)
a.add(a.text(48, 650, "La alerta es un indicio: lo que decide si se escala es el historial de la matrícula y la grabación.", 16, a.TXT))
write(a, "9-t1.svg", "Merodeo en el tiempo", [10, 30, 50, 70, 92])
