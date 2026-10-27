"""Teoría de Terminal bien parado: detectar y comparar dependen de la imagen (tamaño en el cuadro y exposición)."""
from _anim_face import *

caps = ["A unos 50 cm: la cara se detecta y la similitud supera el umbral.",
        "Más lejos: la cara queda chica y no se detecta un rostro.",
        "Más cerca: la cara se sale del cuadro.",
        "Con una ventana atrás, la exposición sigue a la ventana: cara en sombra, similitud baja."]
a = new(24, "Imagen", "Detectar y comparar: las dos cosas dependen de la imagen", caps, still=3, size=17)

FX, FY, FW, FH = 48, 182, 460, 330
a.add(f'<defs><clipPath id="fr"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="16"/></clipPath></defs>')
a.add(a.box(FX, FY, FW, FH, "#1B2E44", rx=16))
a.add(a.text(FX + FW / 2, FY + FH + 22, "lo que ve la cámara del terminal", 15, a.GREY, a.MONO, 600, "middle"))
cx = FX + FW / 2
face = lambda cy, s, f="#9DB2C6": person(a, cx, cy, s, fill=f)
det = lambda cy, s: (f'<rect x="{cx - 34 * s}" y="{cy - 34 * s}" width="{68 * s}" height="{74 * s}" rx="8" fill="none" stroke="#5BE0A5" stroke-width="3" stroke-dasharray="8 5"/>'
                     + a.text(cx - 34 * s, cy - 34 * s - 10, "rostro", 15, "#5BE0A5", a.MONO, 600))
vis(a, f'<g clip-path="url(#fr)">' + face(FY + 150, 2.2) + det(FY + 150, 2.2) + '</g>', 0)
vis(a, f'<g clip-path="url(#fr)">' + face(FY + 190, 0.75) + '</g>' + a.text(cx, FY + FH - 22, "cara chica: no encuentra un rostro", 17, "#FFD28A", a.SANS, 600, "middle"), 1)
vis(a, f'<g clip-path="url(#fr)">' + face(FY + 64, 4.8) + '</g>' + a.pill(cx, FY + FH - 50, "se sale del cuadro", a.BAD, a.BADBG, size=16, h=32, anchor="middle"), 2)
win = (f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="#F4F1E4"/>'
       f'<rect x="{FX + 60}" y="{FY + 40}" width="{FW - 120}" height="{FH - 80}" fill="#FFFFFF" stroke="#E2DCC4" stroke-width="6"/>')
vis(a, f'<g clip-path="url(#fr)">' + win + face(FY + 150, 2.2, "#24384C") + det(FY + 150, 2.2).replace("#5BE0A5", "#B26A00") + '</g>'
    + a.text(cx, FY + FH - 22, "la cara queda en sombra", 17, a.BAD, a.SANS, 600, "middle"), 3)

# vista de costado
SX, SY, SW, SH = 540, 182, 612, 200
a.add(a.box(SX, SY, SW, SH, a.WHITE, a.LINE))
a.add(a.text(SX + 18, SY + 30, "De costado", 17, a.INK, a.SANS, 600))
floor = SY + SH - 24
a.add(f'<line x1="{SX + 16}" y1="{floor}" x2="{SX + SW - 16}" y2="{floor}" stroke="{a.GREY}" stroke-width="2"/>')
a.add(f'<rect x="{SX + SW - 34}" y="{SY + 40}" width="14" height="{floor - SY - 40}" fill="#DDE8F2"/>')
a.add(a.box(SX + SW - 52, SY + 70, 18, 46, a.INK, rx=4))
tx_ = SX + SW - 52
pos = {0: (SX + SW - 150, "≈ 50 cm"), 1: (SX + 230, "más lejos"), 2: (SX + SW - 92, "más cerca"), 3: (SX + SW - 150, "≈ 50 cm")}
for st, (px, lab) in pos.items():
    s = (person(a, px, SY + 84, .62) + f'<rect x="{px - 10}" y="{SY + 126}" width="20" height="{floor - SY - 126}" rx="8" fill="#8FA6BC"/>'
         + line(a, px + 16, SY + 84, tx_ - 4, SY + 90, a.CYAN, 2, "5 4", arrow=False)
         + a.text(px, floor + 18, lab, 15, a.INK, a.MONO, 600, "middle"))
    if st == 3:
        s = (f'<rect x="{SX + 40}" y="{SY + 52}" width="90" height="110" fill="#FFF6D8" stroke="#E2C77A" stroke-width="3"/>'
             + a.text(SX + 85, SY + 182, "ventana", 15, a.AMB, a.MONO, 600, "middle")) + s
    vis(a, s, st)

# similitud
BX, BY, BW = 540, 404, 612
a.add(a.box(BX, BY, BW, 122, a.WHITE, a.LINE))
a.add(a.text(BX + 18, BY + 32, "Similitud con la plantilla de Ana", 17, a.INK, a.SANS, 600))
gx0, gx1, gy = BX + 18, BX + BW - 18, BY + 66
a.add(a.box(gx0, gy, gx1 - gx0, 22, a.SLATE, rx=11))
ux = gx0 + (gx1 - gx0) * .7
a.add(f'<line x1="{ux}" y1="{gy - 10}" x2="{ux}" y2="{gy + 32}" stroke="{a.INK}" stroke-width="3"/>' + a.text(ux, gy + 50, "umbral", 15, a.INK, a.MONO, 600, "middle"))
vis(a, a.box(gx0, gy, (gx1 - gx0) * .86, 22, a.OK, rx=11) + a.text(gx0, gy + 50, "identifica: abre", 15, a.OK, a.SANS, 600), 0)
vis(a, a.text(gx0, gy + 50, "sin rostro, no hay comparación", 15, a.GREY, a.SANS, 600), 1, 2)
vis(a, a.box(gx0, gy, (gx1 - gx0) * .45, 22, a.AMB, rx=11) + a.text(gx0, gy + 50, "rasgos distintos: no identifica", 15, a.AMB, a.SANS, 600), 3)

a.add(a.text(48, 586, "Orden de trabajo:", 18, a.INK, a.SANS, 600))
for k, (t, c) in enumerate((("1 · ubicación y luz", a.OK), ("2 · ajustes del equipo", a.BLUE), ("3 · el umbral, al final", a.AMB))):
    a.add(a.pill(48 + k * 290, 598, t, c, a.WHITE, size=16, h=34))
    a.add(a.box(48 + k * 290, 598, int(len(t) * 16 * .62 + 26), 34, "none", c, rx=17, sw=2))
write(a, "2-t1.svg", "Detectar y comparar", [12, 37, 62, 90])
