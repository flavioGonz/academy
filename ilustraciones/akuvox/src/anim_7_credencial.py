#!/usr/bin/env python3
"""Lección 7 · teoría: qué revisa el portero cuando alguien presenta una credencial (usuario, horario, relé)."""
from _anim_akuvox import Anim, A, token, chip, appear, mark, finish

a = Anim(T=24, kicker="AKUVOX · USUARIOS Y HORARIOS", title="Qué revisa el portero antes de abrir")
a.steps([
    "Martes 10:00, PIN 482913: el portero busca a quién pertenece.",
    "Su horario es Lun a Vie 08 a 18: está adentro, dispara Relay A.",
    "El mismo PIN a las 19:30: fuera de su horario, se rechaza.",
    "PIN público: no está atado a nadie, abre a cualquier hora.",
], still=1)
PH = [(0, 25), (25, 50), (50, 75), (75, 100)]

BX = [48, 330, 612, 894]
BY, BW, BH = 184, 258, 116
heads = ["Credencial", "¿De quién es?", "¿Está en horario?", "Relé"]
for i, x in enumerate(BX):
    a.add(a.box(x, BY, BW, BH, A.WHITE, A.LINE))
    a.add(a.text(x + 18, BY + 30, heads[i], 17, A.GREY, A.SANS, 600))
    if i < 3:
        a.add(f'<path d="M{x + BW + 4} {BY + BH / 2} H{x + BW + 18}" stroke="{A.GREY}" stroke-width="3"/>'
              + f'<path d="M{x + BW + 24} {BY + BH / 2} l-9 -6 v12 z" fill="{A.GREY}"/>')


def val(i, s, color, ph, still_ph, size=19, y=BY + 68, fam=None):
    for p in ph:
        a.add(a.group(a.text(BX[i] + 18, y, s, size, color, fam or A.MONO, 600), a.show(PH[p][0] + (2 + i * 3), PH[p][1], 0.8),
                      still=1 if p == still_ph else 0))


def sub(i, s, color, ph, still_ph):
    val(i, s, color, ph, still_ph, size=14, y=BY + 96)


# columna 1: credencial y hora
val(0, "PIN 482913", A.INK, [0, 1, 2], 1)
val(0, "PIN público", A.AMB, [3], -1)
for p, h in ((0, "martes 10:00"), (1, "martes 10:00"), (2, "martes 19:30"), (3, "martes 19:30")):
    a.add(a.group(a.text(BX[0] + 18, BY + 96, h, 14, A.GREY, A.MONO), a.show(PH[p][0], PH[p][1], 0.8), still=1 if p == 1 else 0))
# columna 2: usuario
val(1, "Prueba Tres", A.INK, [0, 1, 2], 1, fam=A.SANS)
sub(1, "Directory > User", A.GREY, [0, 1, 2], 1)
val(1, "nadie", A.AMB, [3], -1, fam=A.SANS)
sub(1, "no se busca usuario", A.AMB, [3], -1)
# columna 3: horario
val(2, "Lun a Vie 08 a 18", A.INK, [1, 2], 1, size=17, fam=A.SANS)
sub(2, "10:00: adentro", A.OK, [1], 1)
sub(2, "19:30: afuera", A.BAD, [2], -1)
val(2, "sin horario", A.AMB, [3], -1, fam=A.SANS)
# columna 4: relé
val(3, "Relay A abre", A.OK, [1], 1, fam=A.SANS)
val(3, "rechaza", A.BAD, [2], -1, fam=A.SANS)
val(3, "abre", A.AMB, [3], -1, fam=A.SANS)
sub(3, "a cualquier hora", A.AMB, [3], -1)
for p, ok in ((1, True), (2, False), (3, True)):
    a.add(a.group(mark(a, BX[3] + BW - 30, BY + 30, ok, 15), a.show(PH[p][0] + 12, PH[p][1], 0.8), still=1 if p == 1 else 0))

# ficha que recorre el circuito
for p, lab, col in ((0, "PIN", A.BLUE), (2, "PIN", A.BLUE), (3, "PIN público", A.AMB)):
    t0 = PH[p][0] + 1
    token(a, [(BX[0] + BW / 2, BY + BH + 22), (BX[3] + BW / 2, BY + BH + 22)], t0, t0 + 12 if p != 0 else t0 + 6,
          chip(a, lab, bg=col, size=13, h=24), hold=t0 + 13 if p != 0 else t0 + 6.5)
token(a, [(BX[1] + BW / 2, BY + BH + 22), (BX[3] + BW / 2, BY + BH + 22)], 26, 34, chip(a, "PIN", bg=A.BLUE, size=13, h=24), hold=35)

# ficha del usuario
UX, UY, UW = 48, 352, 520
a.add(a.box(UX, UY, UW, 270, A.WHITE, A.LINE))
a.add(a.box(UX, UY, UW, 40, "#E6EEF6", None, rx=14))
a.add(a.text(UX + 18, UY + 27, "Directory > User · Prueba Tres", 16, A.INK, A.SANS, 600))
rows = [("PIN privado", "482913"), ("Tarjetas", "hasta 5"), ("Relé", "Relay A"), ("Horario", "Lun a Vie 08 a 18")]
for k, (c1, c2) in enumerate(rows):
    y = UY + 78 + k * 46
    a.add(a.text(UX + 18, y, c1, 16, A.TXT, A.SANS, 600))
    a.add(a.text(UX + 200, y, c2, 16, A.INK, A.MONO, 600))
    if k < 3:
        a.add(f'<line x1="{UX + 14}" y1="{y + 18}" x2="{UX + UW - 14}" y2="{y + 18}" stroke="{A.LINE}" stroke-width="1.5"/>')
appear(a, a.box(UX + 6, UY + 6, UW - 12, 258, "none", A.BLUE, rx=12, sw=3), 4, 75, still=1)
appear(a, a.box(UX, UY, UW, 270, "#F7FAFD", None, rx=14, extra='opacity=".92"')
       + a.text(UX + UW / 2, UY + 150, "el PIN público no usa esta ficha", 17, A.AMB, A.SANS, 600, "middle"), 76, 100, still=0)

# línea de horario
TX, TY, TW = 612, 352, 540
a.add(a.box(TX, TY, TW, 270, A.WHITE, A.LINE))
a.add(a.text(TX + 18, TY + 34, "Horario del usuario", 17, A.INK, A.SANS, 600))
L, R, Y = TX + 40, TX + TW - 40, TY + 150
a.add(a.box(L, Y - 18, R - L, 36, A.SLATE, None, rx=8))
x8, x18 = L + (R - L) * 8 / 24, L + (R - L) * 18 / 24
a.add(a.box(x8, Y - 18, x18 - x8, 36, A.OKBG, A.OK, rx=8, sw=2) + a.text((x8 + x18) / 2, Y + 6, "Lun a Vie 08 a 18", 15, A.OK, A.SANS, 600, "middle"))
for h in (0, 8, 18, 24):
    x = L + (R - L) * h / 24
    a.add(a.text(x, Y + 46, f"{h:02d}:00", 14, A.GREY, A.MONO, 400, "middle"))


def marker(h, ok, p, still_ph):
    x = L + (R - L) * h / 24
    col = A.OK if ok else A.BAD
    s = (f'<line x1="{x}" y1="{Y - 62}" x2="{x}" y2="{Y - 18}" stroke="{col}" stroke-width="3"/>'
         + mark(a, x, Y - 74, ok, 13) + a.text(x, Y - 96, "10:00" if h == 10 else "19:30", 15, col, A.MONO, 600, "middle"))
    a.add(a.group(s, a.show(PH[p][0] + 8, PH[p][1], 0.8), still=1 if p == still_ph else 0))


marker(10, True, 1, 1)
marker(19.5, False, 2, -1)
appear(a, a.box(TX, TY, TW, 270, "#F7FAFD", None, rx=14, extra='opacity=".92"')
       + a.text(TX + TW / 2, TY + 150, "el PIN público no mira horarios", 17, A.AMB, A.SANS, 600, "middle"), 76, 100, still=0)

finish(a, "7-t1.svg", "Qué revisa el portero antes de abrir",
       "Animación en cuatro tiempos con el recorrido de una credencial: credencial, de quién es, si está en horario y qué relé dispara; abajo la ficha del usuario y su horario. "
       "1: un martes a las 10:00 se marca el PIN privado 482913 y el portero lo encuentra en Directory > User: es de Prueba Tres, con Relay A y horario Lun a Vie 08 a 18. "
       "2: las 10:00 caen dentro del horario y el portero dispara el Relay A. "
       "3: el mismo PIN a las 19:30 queda fuera del horario y se rechaza. "
       "4: con el PIN público no se busca usuario ni horario: cualquiera que lo sepa abre a cualquier hora.",
       [12, 40, 65, 92])
