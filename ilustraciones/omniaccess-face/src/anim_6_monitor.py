"""Teoría de Monitor y evento: carga de 24 h, evento en vivo por WebSocket y el orden de respaldo de foto y nombre."""
from _anim_face import *

caps = ["Al abrir, el monitor carga los eventos de rostro de las últimas 24 horas.",
        "Un evento nuevo llega por WebSocket: va arriba, a Entrada o Salida según el terminal.",
        "La foto: la captura del momento; si no, la de la ficha; si no, la del evento.",
        "El nombre: el de la ficha; si no, el del terminal; si no, Desconocido."]
a = new(24, "Monitor", "Monitor Facial: de dónde sale cada dato", caps, still=3, size=17)
S = [sp[0] for sp in a.spans]

a.add(card(a, 48, 200, 236, 80, "Servidor de eventos", "emite cada evento", dark=True, tsize=17))
a.add(line(a, 284, 240, 340, 240, a.BLUE, 3) + a.text(312, 228, "WS", 14, a.BLUE, a.MONO, 600, "middle"))
MX, MY, MW, MH = 344, 178, 808, 296
a.add(a.box(MX, MY, MW, MH, a.WHITE, a.LINE))
a.add(a.text(MX + 20, MY + 32, "Monitor Facial", 18, a.INK, a.SANS, 600) + a.pill(MX + 170, MY + 13, "LIVE", a.OK, a.OKBG, size=13))
cols = [("ENTRADA", MX + 20, 200), ("ÚLTIMO EVENTO", MX + 238, 332), ("SALIDA", MX + 588, 200)]
for t, x, w in cols:
    a.add(a.text(x, MY + 64, t, 13, a.GREY, a.MONO, 600, extra='letter-spacing="1.2"'))


def thumb(x, y, c=None, name=None):
    s = a.box(x, y, 56, 56, a.SLATE, c or a.LINE, rx=8, sw=2) + person(a, x + 28, y + 20, .36, fill="#9DB2C6")
    return s


# carga de 24 h
k = 0
for col_x in (MX + 20, MX + 588):
    for r in range(2):
        for c in range(3):
            if col_x == MX + 588 and r == 1 and c == 2:
                continue
            t = S[0] + 2 + k * 0.9
            a.add(a.group(thumb(col_x + c * 66, MY + 150 + r * 66, a.BAD if (k in (4, 9)) else None), a.show(t, 100, .5), still=1))
            k += 1
vis(a, a.pill(MX + 20, MY + 290 - 14, "últimas 24 h", a.BLUE, "#E3EEF9", size=13) + a.pill(MX + 588, MY + 290 - 14, "últimas 24 h", a.BLUE, "#E3EEF9", size=13), 0, d0=8)
# evento nuevo
s1 = S[1]
token(a, "evento · entrada", [(s1 + 1, 200, 300), (s1 + 6, MX + 110, MY + 110), (s1 + 7, MX + 110, MY + 110)], size=13)
a.add(a.group(thumb(MX + 20, MY + 76, a.OK) + thumb(MX + 86, MY + 76) + thumb(MX + 152, MY + 76), a.show(s1 + 7, 100, .5), still=1))
# centro: último evento
CX0, CY0 = MX + 238, MY + 76
a.add(a.box(CX0, CY0, 332, 200, a.INK, rx=12))
vis(a, a.box(CX0 + 16, CY0 + 16, 120, 140, "#14395E", a.OK, rx=10, sw=3) + person(a, CX0 + 76, CY0 + 62, .8, fill="#9DB2C6")
    + a.text(CX0 + 152, CY0 + 50, "Ana Ejemplo", 18, a.WHITE, a.SANS, 600) + a.text(CX0 + 152, CY0 + 76, "Portería peatonal", 15, DARK_SUB, a.MONO)
    + a.pill(CX0 + 152, CY0 + 92, "Permitido", a.WHITE, a.OK, size=13) + a.pill(CX0 + 152, CY0 + 126, "Entrada", a.WHITE, a.BLUE, size=13), 1, 2, d0=7)
vis(a, a.box(CX0 + 16, CY0 + 16, 120, 140, "#14395E", a.BAD, rx=10, sw=3) + person(a, CX0 + 76, CY0 + 62, .8, fill="#6E88A1")
    + a.text(CX0 + 152, CY0 + 50, "Desconocido", 18, a.WHITE, a.SANS, 600) + a.text(CX0 + 152, CY0 + 76, "Portería peatonal", 15, DARK_SUB, a.MONO)
    + a.pill(CX0 + 152, CY0 + 92, "Denegado", a.WHITE, a.BAD, size=13), 3, d0=10)
a.add(a.group(a.box(CX0 + 16, CY0 + 16, 120, 140, "#14395E", a.OK, rx=10, sw=3) + person(a, CX0 + 76, CY0 + 62, .8, fill="#9DB2C6")
    + a.text(CX0 + 152, CY0 + 50, "Ana Ejemplo", 18, a.WHITE, a.SANS, 600) + a.text(CX0 + 152, CY0 + 76, "Portería peatonal", 15, DARK_SUB, a.MONO)
    + a.pill(CX0 + 152, CY0 + 92, "Permitido", a.WHITE, a.OK, size=13), a.show(S[3], S[3] + 9.5, .6), still=0))
vis(a, a.text(CX0 + 166, CY0 + 178, "verde Permitido · rojo Denegado", 14, DARK_SUB, a.MONO, 600, "middle"), 1, 3, d0=7)


def chain(x, y, title, items, step, pick_times):
    s = a.box(x, y, 540, 140, a.WHITE, a.LINE) + a.text(x + 20, y + 32, title, 17, a.INK, a.SANS, 600)
    a.add(s)
    for i, it in enumerate(items):
        bx = x + 20 + i * 172
        a.add(a.box(bx, y + 52, 160, 66, a.SLATE, rx=10) + a.text(bx + 12, y + 76, f"{i + 1}", 15, a.GREY, a.MONO, 600)
              + a.text(bx + 12, y + 104, it, 15, a.INK, a.SANS, 600))
    for i, (t0, t1, st) in pick_times.items():
        bx = x + 20 + i * 172
        a.add(a.group(a.box(bx - 3, y + 49, 166, 72, "none", a.OK if i < 2 else a.BAD, rx=12, sw=3.5), a.show(t0, t1, .6), still=st))


chain(48, 494, "Foto: la primera que exista", ["captura del momento", "foto de la ficha", "imagen del evento"], 2,
      {0: (S[2] + 2, S[3], 0)})
chain(612, 494, "Nombre: el primero que exista", ["ficha vinculada", "nombre del terminal", "Desconocido"], 3,
      {0: (S[3] + 2, S[3] + 6, 0), 1: (S[3] + 6, S[3] + 10, 0), 2: (S[3] + 10, 100, 1)})
write(a, "6-t1.svg", "Monitor Facial en vivo", [12, 40, 56, 66, 94])
