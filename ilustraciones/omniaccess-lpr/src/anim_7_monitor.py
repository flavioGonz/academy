"""Teoría de Monitor en vivo: WebSocket, cola con redibujo en tandas y el color que sale de tres datos."""
from _anim_lpr import *

caps = ["El receptor emite cada lectura por WebSocket a los navegadores abiertos.",
        "En una ráfaga, el monitor junta y redibuja unas 4 veces por segundo.",
        "Cada tarjeta se pinta con tres datos: decisión, vigilancia y sin chapa.",
        "Lista negra: rojo con sonido hasta abrir el evento, y ventana abajo a la izquierda."]
a = new(22, "Monitor", "Del receptor a la pantalla, en tandas", caps, still=2, size=17)
YEL, YELBG = "#8A6D00", "#FFF6BF"

a.add(card(a, 48, 206, 210, 86, "Receptor", "puerto 10000", dark=True))
NX, NY, NW, NH = 330, 182, 300, 316
a.add(a.box(NX, NY, NW, NH, a.WHITE, a.LINE))
a.add(a.text(NX + 20, NY + 32, "Navegador del puesto", 18, a.INK, a.SANS, 600))
a.add(a.text(NX + 20, NY + 56, "cola de lecturas", 15, a.GREY, a.MONO))
a.add(line(a, 258, 249, NX - 4, 249, a.BLUE, 3))
a.add(a.text(294, 236, "WS", 15, a.BLUE, a.MONO, 600, "middle"))
MX, MY, MW, MH = 700, 182, 452, 316
a.add(a.box(MX, MY, MW, MH, a.WHITE, a.LINE))
a.add(a.text(MX + 20, MY + 32, "Monitor LPR", 18, a.INK, a.SANS, 600))
a.add(line(a, NX + NW + 4, 340, MX - 4, 340, a.BLUE, 3))

kinds = {"ok": (a.OK, a.OKBG, "Autorizado"), "den": (a.AMB, a.AMBBG, "Denegado"), "sin": (YEL, YELBG, "sin lectura"),
         "neg": (a.BAD, a.BADBG, "Lista negra")}
cards = [("SBA1234", "ok"), ("SCD5678", "den"), ("SBB4321", "ok"), ("sin chapa", "sin"), ("SAC1010", "ok"), ("SDE9090", "den"), ("SBA9876", "ok")]
CW, CH = 132, 60
pos = [(MX + 16 + (k % 3) * (CW + 12), MY + 50 + (k // 3) * (CH + 10)) for k in range(8)]


def tcard(k, plate_txt, kind):
    fg, bg, lab = kinds[kind]
    x, y = pos[k]
    return a.box(x, y, CW, CH, bg, fg, rx=10) + a.text(x + 14, y + 26, plate_txt, 17, a.INK, a.MONO, 600) + a.text(x + 14, y + 48, lab, 14, fg, a.MONO, 600)


s0 = ph(a, 0)[0]
token(a, "SBA1234", [(s0 + 2, 150, 249), (s0 + 4, 150, 249), (s0 + 9, NX + 80, 300), (s0 + 12, NX + 80, 300)], size=13)
a.add(a.group(tcard(0, *cards[0]), a.show(s0 + 13, 100), still=1))
# 2 · ráfaga: cola y dos tandas
s0 = ph(a, 1)[0]
QX, QY = NX + 24, NY + 76
tick = [s0 + 12, s0 + 19]
for k in range(1, 7):
    t0 = s0 + 1 + (k - 1) * 1.2
    arr = t0 + 3.5
    out = tick[0] if k <= 3 else tick[1]
    token(a, cards[k][0], [(t0, 150, 249), (arr, QX + 70, QY + (k - 1) * 34 + 14)], size=13)
    a.add(a.group(a.pill(QX + 70, QY + (k - 1) * 34, cards[k][0], a.WHITE, a.CYAN, size=13, anchor="middle"), a.show(arr, out, 0.5), still=0))
    a.add(a.group(tcard(k, *cards[k]), a.show(out + 0.5, 100), still=1))
for t in tick:
    a.add(a.group(a.box(NX + NW - 120, NY + NH - 52, 104, 34, a.BLUE, rx=17) + a.text(NX + NW - 68, NY + NH - 29, "redibuja", 15, a.WHITE, a.MONO, 600, "middle"),
                  a.show(t - 1, t + 2, 0.4), still=0))
vis(a, a.text(NX + 20, NY + NH - 28, "~250 ms", 16, a.BLUE, a.MONO, 600), 1)
# 3 · reglas de color
RY = 524
vis(a, a.text(48, RY + 4, "EL COLOR SALE DE TRES DATOS", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'), 2, 3)
rules = [("decisión Autorizado", "verde · pasa solo", "ok"), ("decisión Denegado", "ámbar · se verifica", "den"),
         ("vigilancia: lista negra", "rojo con sonido", "neg"), ("vino sin chapa", "amarillo · se mira la foto", "sin")]
for k, (q, r, kind) in enumerate(rules):
    fg, bg, _ = kinds[kind]
    x = 48 + k * 278
    vis(a, a.box(x, RY + 20, 262, 84, bg, fg, rx=12) + a.text(x + 16, RY + 52, q, 16, a.INK, a.SANS, 600) + a.text(x + 16, RY + 80, r, 15, fg, a.MONO, 600), 2, 3)
# 4 · lista negra
s0 = ph(a, 3)[0]
token(a, "SAB2024", [(s0 + 2, 150, 249), (s0 + 7, NX + 80, 300), (s0 + 9, NX + 80, 300)], bg=a.BAD, size=13)
a.add(a.group(tcard(7, "SAB2024", "neg"), a.show(s0 + 10, 100), still=0))
x, y = pos[7]
waves = "".join(f'<path d="M{x + CW + 8 + i * 9} {y + 14 - i * 4} Q{x + CW + 18 + i * 9} {y + 30} {x + CW + 8 + i * 9} {y + 46 + i * 4}" fill="none" stroke="{a.BAD}" stroke-width="3"/>' for i in range(3))
a.add(a.group(waves, a.keyframes([(0, 0), (s0 + 10, 0), (s0 + 11, 1), (s0 + 14, .2), (s0 + 17, 1), (s0 + 20, .2), (s0 + 23, 1), (99, 1), (100, 0)]), still=0))
a.add(a.group(a.box(MX + 16, MY + MH - 60, 250, 48, a.BAD, rx=10) + a.text(MX + 30, MY + MH - 30, "Lista negra", 16, a.WHITE, a.SANS, 600)
              + a.text(MX + 140, MY + MH - 30, "SAB2024", 15, "#FFD9D1", a.MONO, 600), a.show(s0 + 12, 100), still=0))
write(a, "7-t1.svg", "Monitor LPR en vivo", [10, 33, 45, 62, 92])
