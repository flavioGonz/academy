"""Teoría de Cámara bien parada: lo que le llega al OCR con perspectiva, pocos píxeles o movimiento."""
from _anim_lpr import *

caps = ["Bien: de frente, 150 a 200 px de ancho y el auto frenando.",
        "Perspectiva: con más de 30°, los caracteres se aplastan o se inclinan.",
        "Tamaño: con pocos píxeles, 8 y B o 0 y D se vuelven iguales.",
        "Movimiento: un auto rápido sale movido. Leer donde frena lo evita."]
a = new(22, "OCR", "Lo que ve el OCR: perspectiva, tamaño y movimiento", caps, still=2)

a.add('<defs><filter id="bl" x="-10%" y="-20%" width="120%" height="140%"><feGaussianBlur stdDeviation="4.5"/></filter>'
      '<filter id="mb" x="-25%" y="-10%" width="150%" height="120%"><feGaussianBlur stdDeviation="13 0"/></filter></defs>')
FX, FY, FW, FH = 48, 184, 600, 300
a.add(a.box(FX, FY, FW, FH, a.INK, rx=16))
a.add(a.text(FX + 20, FY + 32, "RECORTE QUE RECIBE EL OCR", 14, DARK_SUB, a.MONO, 600, extra='letter-spacing="1.5"'))
PCX, PCY = FX + FW / 2, FY + FH / 2 + 14
P = "SBD 1080"
big = lambda extra="": plate(a, PCX, PCY, P, w=330, h=96, size=50, extra=extra)
vis(a, big(), 0)
vis(a, big(f'transform="translate({PCX} {PCY}) skewX(-28) scale(1 0.48) translate({-PCX} {-PCY})"'), 1)
grid = "".join(f'<line x1="{PCX - 165 + k * 15}" y1="{PCY - 48}" x2="{PCX - 165 + k * 15}" y2="{PCY + 48}" stroke="#04223D" stroke-opacity=".18" stroke-width="2"/>' for k in range(1, 22)) + \
       "".join(f'<line x1="{PCX - 165}" y1="{PCY - 48 + k * 15}" x2="{PCX + 165}" y2="{PCY - 48 + k * 15}" stroke="#04223D" stroke-opacity=".18" stroke-width="2"/>' for k in range(1, 7))
vis(a, big('filter="url(#bl)"') + grid, 2)
vis(a, big('filter="url(#mb)"'), 3)
labs = ["de frente · 150 a 200 px de ancho", "ángulo de más de 30°", "pocos píxeles por carácter", "auto rápido: sale movido"]
for i, l in enumerate(labs):
    vis(a, a.text(PCX, FY + FH - 26, l, 17, a.WHITE, a.SANS, 600, "middle"), i)

# lectura carácter por carácter
RX = 700
a.add(a.text(RX, FY + 22, "LO QUE LEE, CARÁCTER POR CARÁCTER", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))
chars = list("SBD1080")
BW, BG = 58, 8
states = [  # por tiempo: lista de (texto, color) por carácter
    [(c, "ok") for c in chars],
    [("S", "ok"), ("?", "amb"), ("D", "ok"), ("1", "ok"), ("?", "amb"), ("8", "ok"), ("?", "amb")],
    [("S", "ok"), ("B/8", "amb"), ("D/0", "amb"), ("1", "ok"), ("0/D", "amb"), ("8/B", "amb"), ("0/D", "amb")],
    [("?", "bad"), ("?", "bad"), ("?", "bad"), ("1", "amb"), ("?", "bad"), ("?", "bad"), ("?", "bad")],
]
col = {"ok": (a.OK, a.OKBG), "amb": (a.AMB, a.AMBBG), "bad": (a.BAD, a.BADBG)}
for t, st in enumerate(states):
    inner = ""
    for k, (c, s) in enumerate(st):
        fg, bg = col[s]
        x = RX + k * (BW + BG)
        inner += a.box(x, FY + 44, BW, 78, bg, fg, rx=10) + a.text(x + BW / 2, FY + 96, c, 26 if len(c) == 1 else 17, fg, a.MONO, 600, "middle")
    vis(a, inner, t)
verd = [("SBD1080: lectura segura", a.OK), ("varios caracteres dudosos", a.AMB),
        ("cinco caracteres con dos candidatos", a.AMB), ("no sale una patente confiable", a.BAD)]
for t, (v, c) in enumerate(verd):
    vis(a, a.text(RX, FY + 162, v, 20, c, a.SANS, 600), t)
why = [["Patente derecha y grande:", "cada carácter tiene forma propia."],
       ["Mirando muy de arriba o de costado,", "las letras se deforman."],
       ["La medida útil es el ancho de la patente", "en la imagen, no los megapíxeles."],
       ["El obturador no alcanza a congelarlo.", "Donde frena, sale nítido."]]
for t, rows in enumerate(why):
    vis(a, "".join(a.text(RX, FY + 206 + k * 26, r, 17, a.TXT) for k, r in enumerate(rows)), t)

a.add(a.box(48, 516, 1104, 120, a.WHITE, a.LINE))
a.add(a.text(72, 552, "Las tres se arreglan en la obra, no en el panel", 19, a.INK, a.SANS, 600))
a.add(a.text(72, 584, "Ángulo vertical y horizontal hasta 30°  ·  patente de 130 a 300 px de ancho  ·  leer donde el auto frena", 17, a.TXT))
a.add(a.text(72, 614, "ángulo vertical = arctan((H - h) / D)", 16, a.BLUE, a.MONO, 600))
write(a, "3-t1.svg", "Lo que ve el OCR", [12, 37, 62, 87])
