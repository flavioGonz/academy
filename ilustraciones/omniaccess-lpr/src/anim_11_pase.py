"""Teoría de Padrón y reportes: el pase de invitado tolera errores de lectura; la lista negra gana igual."""
from _anim_lpr import *

caps = ["Hay un pase activo y vigente para la patente SBA1234.",
        "La cámara lee SBA1Z34: un carácter distinto. Con 6 o más, se toleran 2.",
        "Si la patente está en lista negra, gana la lista negra aunque haya pase."]
a = new(18, "Pases", "Pase de invitado: coincidencia tolerante", caps, still=1)

a.add(a.box(48, 186, 300, 300, a.WHITE, a.LINE))
a.add(a.text(70, 222, "Pase de visita", 19, a.INK, a.SANS, 600))
vis(a, a.text(70, 252, "Visita prueba", 16, a.TXT) + plate(a, 198, 314, "SBA 1234", w=220, h=62, size=30), 0, 1)
vis(a, a.text(70, 252, "Visita prueba 2", 16, a.TXT) + plate(a, 198, 314, "SAB 2024", w=220, h=62, size=30), 2)
a.add(a.pill(70, 372, "activo", a.OK, a.OKBG, size=14) + a.pill(160, 372, "vigente ahora", a.OK, a.OKBG, size=14))
a.add(a.text(70, 438, "Invitados → Nuevo pase", 15, a.GREY, a.MONO, 600))
a.add(a.text(70, 462, "patente y vigencia", 15, a.GREY, a.MONO, 600))

X0, BW, G = 420, 62, 10
rows_y = (238, 384)
a.add(a.text(X0, rows_y[0] - 26, "PASE", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))
a.add(a.text(X0, rows_y[1] - 26, "LECTURA DE LA CÁMARA", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))


def row(y, txt, diff=(), col=None):
    s = ""
    for k, ch in enumerate(txt):
        x = X0 + k * (BW + G)
        fg, bg = (a.AMB, a.AMBBG) if k in diff else (col or (a.INK, a.SLATE))
        s += a.box(x, y, BW, 70, bg, fg if k in diff else None, rx=10, sw=3) + a.text(x + BW / 2, y + 47, ch, 30, fg, a.MONO, 600, "middle")
    return s


vis(a, row(rows_y[0], "SBA1234"), 0, 1)
vis(a, row(rows_y[1], "SBA1Z34", diff=(4,)), 1, d0=2)
vis(a, a.text(X0 + 4 * (BW + G) + BW / 2, rows_y[1] + 98, "1 diferencia", 16, a.AMB, a.SANS, 600, "middle"), 1, d0=4)
vis(a, row(rows_y[0], "SAB2024"), 2)
vis(a, row(rows_y[1], "SAB2024"), 2, d0=2)
vis(a, a.pill(X0 + 7 * (BW + G) - 6, rows_y[1] + 84, "lista negra", a.BAD, a.BADBG, size=15, h=30, anchor="end"), 2, d0=5)

# regla
RY = 520
a.add(a.box(48, RY, 1104, 110, a.WHITE, a.LINE))
a.add(a.text(72, RY + 38, "Cuántos errores tolera", 18, a.INK, a.SANS, 600))
a.add(a.text(72, RY + 72, "6 caracteres o más: hasta 2  ·  menos de 6: 1", 17, a.BLUE, a.MONO, 600))
a.add(a.text(72, RY + 98, "Solo pases activos y dentro de su vigencia.", 16, a.TXT))
vis(a, a.pill(1128, RY + 34, "coincide con el pase", a.OK, a.OKBG, size=16, h=36, anchor="end"), 1, d0=6)
vis(a, a.pill(1128, RY + 34, "Lista negra · denegada", a.BAD, a.BADBG, size=16, h=36, anchor="end"), 2, d0=7)
vis(a, a.pill(1128, RY + 34, "esperando lectura", a.GREY, "#E6EDF4", size=16, h=36, anchor="end"), 0)
write(a, "11-t2.svg", "Pase con tolerancia", [15, 50, 85])
