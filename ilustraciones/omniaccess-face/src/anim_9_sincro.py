"""Teoría de Historial y reportes: con la red cortada el terminal anota igual; Auditoría Hardware trae solo lo que falta."""
from _anim_face import *

caps = ["Con red, cada acceso llega por aviso y queda en los dos lados.",
        "Se corta la red: el terminal sigue abriendo y anota en su registro.",
        "Auditoría Hardware lee los últimos registros y crea los que faltan.",
        "Los que ya estaban (misma hora, ± 2 s) no se duplican."]
a = new(22, "Sincronizar", "Corte de red: el terminal anota, la sincronización completa", caps, still=3, size=17)
S = [sp[0] for sp in a.spans]

LX, RX, W, Y = 48, 652, 500, 176
a.add(a.box(LX, Y, W, 330, a.WHITE, a.LINE) + a.text(LX + 20, Y + 32, "Registro del terminal (doorlog)", 18, a.INK, a.SANS, 600))
a.add(a.box(RX, Y, W, 330, a.WHITE, a.LINE) + a.text(RX + 20, Y + 32, "Eventos en OmniAccess", 18, a.INK, a.SANS, 600))
rows = [("10:00:03", "10:00:04", "Ana Ejemplo"), ("10:05:41", "10:05:42", "Bruno Ejemplo"), ("10:12:17", None, "Carla Ejemplo"), ("10:20:55", None, "Ana Ejemplo")]
ry = lambda k: Y + 60 + k * 58


def row(x, t, n, tag=None, fg=None, bg=None):
    s = a.box(x + 16, ry(k), W - 32, 46, bg or a.SLATE, fg, rx=8, sw=2) + a.text(x + 32, ry(k) + 30, t, 16, a.INK, a.MONO, 600) + a.text(x + 140, ry(k) + 30, n, 16, a.INK, a.SANS)
    if tag:
        s += a.pill(x + W - 28, ry(k) + 9, tag, a.BLUE, "#E3EEF9", size=13, anchor="end")
    return s


for k, (tl, tr, n) in enumerate(rows):
    st = 0 if k < 2 else 1
    t0 = S[st] + 2 + (k % 2) * 7
    a.add(a.group(row(LX, tl, n), a.show(t0, 100, .5), still=1))
    if tr:
        token(a, "aviso", [(t0 + 1, LX + W - 40, ry(k) + 23), (t0 + 5, RX + 60, ry(k) + 23), (t0 + 6, RX + 60, ry(k) + 23)], size=13)
        a.add(a.group(row(RX, tr, n, "aviso"), a.show(t0 + 6, 100, .5), still=1))
    else:
        a.add(a.group(row(RX, tl, n, "SINCRO_HW", a.BLUE, "#EEF5FC"), a.show(S[2] + 8 + (k - 2) * 3, 100, .5), still=1))
# red
mid = (LX + W + RX) / 2
a.add(line(a, LX + W + 6, Y + 120, RX - 6, Y + 120, a.LINE, 3, arrow=False))
vis(a, line(a, LX + W + 6, Y + 120, RX - 6, Y + 120, a.OK, 3, arrow=False) + a.text(mid, Y + 106, "red", 14, a.OK, a.MONO, 600, "middle"), 0)
vis(a, xmark(a, mid, Y + 120, 16) + a.text(mid, Y + 156, "sin red", 14, a.BAD, a.MONO, 600, "middle"), 1, d0=1)
vis(a, a.text(LX + 20, Y + 306, "el terminal abre y anota igual", 15, a.AMB, a.SANS, 600), 1, d0=3)
# auditoría
vis(a, a.box(LX + 10, ry(0) - 6, W - 20, 4 * 58 + 2, "none", a.CYAN, rx=12, sw=3)
    + a.text(mid, Y + 214, "Auditoría", 14, "#0B7FA3", a.MONO, 600, "middle") + a.text(mid, Y + 232, "Hardware", 14, "#0B7FA3", a.MONO, 600, "middle")
    + line(a, LX + W + 6, Y + 250, RX - 6, Y + 250, a.CYAN, 3), 2, d0=2)
vis(a, a.text(RX + 20, Y + 306, "creados por sincronización", 15, a.BLUE, a.SANS, 600), 2, d0=10)
# duplicados evitados
for k in range(2):
    vis(a, a.box(RX + 12, ry(k) - 4, W - 24, 54, "none", a.OK, rx=10, sw=3), 3, d0=2 + k * 3)
vis(a, a.text(RX + 20, Y + 306, "10:00:03 y 10:00:04: ya está, no se duplica", 15, a.OK, a.SANS, 600), 3, d0=6)

a.add(a.box(48, 536, 1104, 100, a.SLATE, None, rx=14))
a.add(a.text(72, 572, "Auditoría Hardware → Sincronizar memoria", 18, a.INK, a.SANS, 600))
a.add(a.text(72, 604, "Existe para terminales Akuvox. Los eventos traídos así llevan SINCRO_HW en el detalle.", 16, a.TXT))
write(a, "9-t2.svg", "Corte de red y sincronización", [12, 40, 66, 94])
