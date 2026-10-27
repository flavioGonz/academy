"""Teoría de Lista de vigilancia: la lista negra del servidor se copia a la lista de bloqueo de cada lectora."""
from _anim_lpr import *

caps = ["Con credencial, SAB2024 está en la lista blanca de cada lectora: el relé abre.",
        "Pasa a lista negra: un PUT la mueve a la lista de bloqueo. P3 no responde.",
        "Nueva lectura en P1: la cámara no cierra el relé y el servidor la deniega.",
        "Al sacarla, vuelve a la lista blanca porque tiene credencial."]
a = new(24, "Lista negra", "La lista negra viaja a cada lectora", caps, still=1)

# servidor
a.add(card(a, 48, 174, 320, 78, "Servidor OmniAccess", "lista de vigilancia", dark=True))
vis(a, a.pill(392, 199, "SAB2024 · residente", a.OK, a.OKBG, size=15, h=30), 0)
vis(a, a.pill(392, 199, "SAB2024 · Lista negra", a.BAD, a.BADBG, size=15, h=30), 1, 2)
vis(a, a.pill(392, 199, "SAB2024 · fuera de la lista", a.OK, a.OKBG, size=15, h=30), 3)

LY, LW, LH = 318, 340, 168
xs = [48, 430, 812]
names = ["P1 - Entrada (21)", "P2 - Salida (22)", "P3 - Servicio (23)"]
# bus de PUT
vis(a, line(a, 208, 252, 208, 286, a.BLUE, 3, arrow=False) + line(a, 208, 286, xs[1] + LW / 2, 286, a.BLUE, 3, arrow=False)
    + line(a, xs[0] + LW / 2, 286, xs[0] + LW / 2, LY - 4, a.BLUE, 3) + line(a, xs[1] + LW / 2, 286, xs[1] + LW / 2, LY - 4, a.BLUE, 3)
    + line(a, xs[1] + LW / 2, 286, xs[2] + LW / 2, 286, a.BAD, 3, "7 6", arrow=False) + line(a, xs[2] + LW / 2, 286, xs[2] + LW / 2, LY - 4, a.BAD, 3, "7 6")
    + a.text(226, 278, "PUT", 15, a.BLUE, a.MONO, 600), 1, d0=2)
for k, (x, n) in enumerate(zip(xs, names)):
    a.add(a.box(x, LY, LW, LH, a.WHITE, a.LINE))
    a.add(a.text(x + 18, LY + 30, n, 17, a.INK, a.SANS, 600))
    a.add(a.box(x + 14, LY + 44, 150, 110, a.OKBG, None, rx=10) + a.text(x + 26, LY + 68, "lista blanca", 15, a.OK, a.MONO, 600))
    a.add(a.box(x + 176, LY + 44, 150, 110, a.BADBG, None, rx=10) + a.text(x + 188, LY + 68, "bloqueo", 15, a.BAD, a.MONO, 600))
    a.add(a.text(x + 26, LY + 132, "SBA1234", 15, a.GREY, a.MONO) + a.text(x + 26, LY + 148, "SCD5678", 15, a.GREY, a.MONO))
    lab, fg, bg = ("ok", a.OK, a.OKBG) if k < 2 else ("no respondió", a.BAD, a.BADBG)
    vis(a, a.pill(x + LW - 12, LY + 12, lab, fg, bg, size=14, anchor="end"), 1, d0=8)

W_, B_ = (lambda x: (x + 89, LY + 100)), (lambda x: (x + 251, LY + 100))
s1a, s1b = ph(a, 1)
s3a, s3b = ph(a, 3)
chipd = lambda: a.pill(0, -14, "SAB2024", a.WHITE, a.INK, size=14, anchor="middle")
for k, x in enumerate(xs):
    wx, wy = W_(x)
    bx, by = B_(x)
    if k < 2:
        pts = [(0, wx, wy), (s1a + 7 + k * 2, wx, wy), (s1a + 11 + k * 2, bx, by), (s3a + 3, bx, by), (s3a + 7, wx, wy), (100, wx, wy)]
        a.add(a.group(chipd(), a.move(pts), still=0))
        a.add(a.group(a.pill(bx, by - 14, "SAB2024", a.WHITE, a.INK, size=14, anchor="middle"), a.keyframes([(0, 0), (100, 0)]), still=1))
    else:
        a.add(a.group(a.pill(wx, wy - 14, "SAB2024", a.WHITE, a.INK, size=14, anchor="middle"), still=1))

# barrera de P1
BX, BY = 66, 590
a.add(f'<rect x="{BX}" y="{BY - 46}" width="20" height="64" rx="4" fill="{a.INK}"/>')
down = f'<rect x="{BX + 14}" y="{BY - 42}" width="130" height="12" rx="6" fill="{a.BAD}"/>'
up = f'<rect x="{BX + 14}" y="{BY - 42}" width="130" height="12" rx="6" fill="{a.OK}" transform="rotate(-34 {BX + 18} {BY - 36})"/>'
a.add(a.text(BX, BY + 44, "barrera de P1", 15, a.GREY, a.MONO, 600))
s0 = ph(a, 0)[0]
a.add(a.group(up, a.show(s0 + 3, ph(a, 0)[1], 0.5), still=0))
a.add(a.group(down, a.keyframes([(0, 1), (s0 + 3, 1), (s0 + 3.5, 0), (ph(a, 0)[1], 0), (ph(a, 0)[1] + .5, 1), (100, 1)]), still=1))
vis(a, a.text(250, 556, "La cámara la tiene en su lista blanca:", 16, a.TXT) + a.text(250, 580, "cierra su relé y sube la barrera.", 16, a.OK, a.SANS, 600), 0, d0=3)
vis(a, a.text(250, 556, "Si una lectora no responde, el resumen", 16, a.TXT) + a.text(250, 580, "lo dice y el servidor la deniega igual.", 16, a.BAD, a.SANS, 600), 1, d0=8)
vis(a, a.pill(250, 512, "lectura SAB2024 en P1", a.WHITE, a.INK, size=14) + a.text(250, 568, "La cámara no cierra el relé.", 16, a.BAD, a.SANS, 600), 2)
vis(a, a.text(250, 556, "Vuelve a la lista blanca porque tiene", 16, a.TXT) + a.text(250, 580, "credencial. Sin credencial, se borra.", 16, a.OK, a.SANS, 600), 3, d0=6)

# monitor
RX = 660
vis(a, a.box(RX, 506, 492, 100, a.BADBG, a.BAD) + a.text(RX + 20, 544, "SAB2024 · LISTA NEGRA · DENEGADA", 17, a.BAD, a.MONO, 600)
    + a.text(RX + 20, 578, "rojo con sonido en el Monitor LPR", 16, a.INK, a.SANS, 600), 2, d0=4)
write(a, "10-t1.svg", "Lista negra en las lectoras", [12, 37, 62, 92])
