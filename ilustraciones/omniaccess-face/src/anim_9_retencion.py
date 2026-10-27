"""Teoría de Historial y reportes: la retención del Bucket FACE vence todo objeto a los N días, también las fotos de alta."""
from _anim_face import *

caps = ["Al Bucket FACE entran las capturas de cada evento y las fotos de alta.",
        "Con 30 días de retención, cada objeto vence a los 30 días de creado.",
        "La foto de alta de Ana también vence: la regla es para todo el bucket."]
a = new(24, "Retención", "Retención del Bucket FACE: la regla no distingue", caps, still=2, size=17)

a.add(a.box(48, 176, 1104, 70, a.INK, rx=12))
a.add(a.text(70, 218, "mc ilm rule add ALIAS/face --expire-days 30", 19, a.WHITE, a.MONO, 600))
a.add(a.text(1130, 218, "= Almacenamiento · Bucket FACE", 15, DARK_SUB, a.MONO, 600, "end"))

X0, X1, AY = 170, 1110, 500
px = (X1 - X0) / 40
dx = lambda d: X0 + d * px
a.add(f'<line x1="{X0}" y1="{AY}" x2="{X1}" y2="{AY}" stroke="{a.GREY}" stroke-width="2"/>')
for d in range(0, 41, 5):
    a.add(f'<line x1="{dx(d)}" y1="{AY - 6}" x2="{dx(d)}" y2="{AY + 6}" stroke="{a.GREY}" stroke-width="2"/>' + a.text(dx(d), AY + 30, f"día {d}", 15, a.GREY, a.MONO, 600, "middle"))
# el "hoy" avanza
key = [(0, 0), (33.3, 14), (66.6, 35), (97, 40), (100, 40)]


def pct_of(day):
    for (p0, d0), (p1, d1) in zip(key, key[1:]):
        if d0 <= day <= d1 and d1 > d0:
            return p0 + (day - d0) / (d1 - d0) * (p1 - p0)
    return 100


win = (f'<rect x="{-30 * px}" y="282" width="{30 * px}" height="{AY - 282}" fill="{a.OKBG}" opacity=".8"/>'
       + a.text(-12, 300, "últimos 30 días", 15, a.OK, a.MONO, 600, "end"))
cur = f'<line x1="0" y1="270" x2="0" y2="{AY + 8}" stroke="{a.BLUE}" stroke-width="3"/>' + a.pill(0, 258, "hoy", a.WHITE, a.BLUE, size=13, anchor="middle")
a.add(f'<defs><clipPath id="ax"><rect x="{X0}" y="250" width="{X1 - X0}" height="300"/></clipPath></defs>')
mv = a.move([(p, dx(d), 0) for p, d in key])
a.add('<g clip-path="url(#ax)">' + a.group(win, mv, still=0) + '</g>')
a.add(a.group(cur, a.move([(p, dx(d), 0) for p, d in key]), still=0))
a.add('<g clip-path="url(#ax)">' + a.group(f'<g transform="translate({dx(40)},0)">' + win + '</g>', a.keyframes([(0, 0), (100, 0)]), still=1) + '</g>')
a.add(a.group(f'<g transform="translate({dx(40)},0)">' + cur + '</g>', a.keyframes([(0, 0), (100, 0)]), still=1))


def obj(day, alta=False):
    x = dx(day)
    if alta:
        s = a.box(x - 22, 330, 44, 52, a.WHITE, a.BLUE, rx=6, sw=3) + person(a, x, 348, .34, fill="#7F9AB3") + a.text(x, 404, "foto de alta", 14, a.BLUE, a.MONO, 600, "middle")
    else:
        s = a.box(x - 14, 436, 28, 34, a.SLATE, a.GREY, rx=4, sw=1.5) + person(a, x, 448, .2, fill="#9DB2C6")
    born, dies = pct_of(day), pct_of(day + 30)
    pts = [(0, 0), (max(born - .01, 0), 0), (born + .5, 1)]
    if dies < 100:
        pts += [(dies, 1), (dies + 1.2, 0), (100, 0)]
    else:
        pts += [(99.5, 1), (100, 0)]
    still = 1 if (day + 30 > 40) else 0
    a.add(a.group(s, a.keyframes(pts), still=still))


for d in (0, 3, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39):
    obj(d)
obj(6, alta=True)
a.add(a.text(X0 - 8, 458, "capturas", 14, a.GREY, a.MONO, 600, "end"))
# rastro de la foto de alta borrada
dd = pct_of(36)
a.add(a.group(a.box(dx(6) - 22, 330, 44, 52, "none", a.BAD, rx=6, sw=2.5, extra='stroke-dasharray="5 4"') + a.text(dx(6), 404, "borrada el día 36", 14, a.BAD, a.MONO, 600, "middle"),
              a.show(dd + 1, 100, .6), still=1))
a.add(a.text(48, 592, "La retención se decide con el responsable de los datos, con un plan para resguardar las fotos de alta.", 17, a.INK, a.SANS, 600))
a.add(a.text(48, 624, "Valor 0: no se borra nada y el bucket crece sin límite.", 16, a.TXT))
write(a, "9-t1.svg", "Retención del Bucket FACE", [20, 55, 92])
