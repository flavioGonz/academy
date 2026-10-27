#!/usr/bin/env python3
"""Lección 9 · teoría: un roam paso a paso con 802.11k, v, r y el mínimo RSSI."""
from _anim_unifi import *  # noqa

a = new(25, "Roaming", "Un roam paso a paso: informar, sugerir, acelerar", [
    "802.11k: AP 1 le pasa al celular la lista de vecinos, con AP 2 y su canal.",
    "El celular se aleja y la señal de AP 1 baja: con la lista, escanea poco.",
    "802.11v: AP 1 le sugiere AP 2. Decide el celular; puede ignorarlo.",
    "802.11r: claves derivadas por adelantado, el cambio sale en pocas tramas.",
    "Mínimo RSSI: sin otro AP cerca, AP 1 lo desconecta y el celular se cae.",
], still=3)

A1X, A2X, AY = 60, 940, 176
a.add(a.box(A1X, AY, 200, 86, A.WHITE, A.LINE, rx=14) + ap_icon(a, A1X + 40, AY + 43, 22) + a.text(A1X + 76, AY + 51, "AP 1", 20, A.INK, A.HEAD, 600))
a.add(a.box(A2X, AY, 200, 86, A.WHITE, A.LINE, rx=14) + ap_icon(a, A2X + 40, AY + 43, 22) + a.text(A2X + 76, AY + 51, "AP 2", 20, A.INK, A.HEAD, 600))
vis(a, a.box(A2X, AY, 200, 86, A.SLATE, A.GREY, rx=14) + a.text(A2X + 100, AY + 38, "AP 2", 20, A.GREY, A.HEAD, 600, "middle")
    + a.text(A2X + 100, AY + 64, "no hay otro AP", 14, A.BAD, A.MONO, 600, "middle"), 4)

# recorrido
PY = 400
a.add(line(a, [(120, PY + 70), (1080, PY + 70)], A.LINE, 2, "4 8"))
a.add(a.text(120, PY + 96, "el celular camina →", 14, A.GREY, A.MONO))
X1, X2, X3 = 330, 560, 820
KF = [(0, X1, PY), (20, X1, PY), (32, X2, PY), (60, X2, PY), (70, X3, PY), (80, X3, PY), (80.3, X2, PY), (100, X2, PY)]


HIDE = a.keyframes([(0, 0), (100, 0)])


def fixed_copy(inner):
    """Copia que solo se ve en el cuadro fijo (tiempo 4): el celular junto a AP 2."""
    a.add(a.group(f'<g transform="translate({X3} {PY})">{inner}</g>', HIDE, still=1))


def attach(inner, t0, t1, still=0):
    """Elemento que acompaña al celular (dibujado alrededor de 0,0)."""
    a.add(a.group(inner, a.move(KF), a.show(t0, t1, 0.5), still=0))
    if still:
        fixed_copy(inner)


phone = a.box(-56, -44, 112, 88, A.WHITE, A.LINE, rx=14) + phone_icon(a, 0, -6) + a.text(0, 34, "celular", 14, A.GREY, A.MONO, anchor="middle")
a.add(a.group(phone, a.move(KF), a.keyframes([(0, 1), (100, 1)]), still=0))
fixed_copy(phone)
attach(pill(a, 0, 54, "en AP 1", "info", anchor="middle"), 0, 68)
attach(pill(a, 0, 54, "en AP 2", "ok", anchor="middle"), 68, 80, still=1)
attach(pill(a, 0, 54, "en AP 1", "info", anchor="middle"), 80, 88)
attach(pill(a, 0, 54, "sin red", "bad", anchor="middle"), 88, 99)

# señal de AP 1 sobre el celular
attach(pill(a, 0, -78, "señal de AP 1: buena", "ok", anchor="middle"), 0, 22)
attach(pill(a, 0, -78, "señal de AP 1: baja", "amb", anchor="middle"), 30, 60)

# título de cada mecanismo
for i, (lab, kind) in enumerate([("802.11k · informar", "info"), ("la señal baja", "amb"), ("802.11v · sugerir", "info"),
                                   ("802.11r · acelerar", "ok"), ("mínimo RSSI · patear", "bad")]):
    vis(a, pill(a, 600, AY + 28, lab, kind, size=16, h=32, anchor="middle"), i)

# 1: lista de vecinos
s0, s1 = ph(a, 0)
token(a, [(A1X + 150, AY + 100), (X1 + 40, 296)], s0 + 2, s0 + 9, "vecinos: AP 2 + canal", bg=A.BLUE, hold=s1 - 1)

# 2: escanea pocos canales
vis(a, a.text(X2, PY + 140, "escanea solo los canales de la lista", 16, A.TXT, A.SANS, 600, "middle"), 1)

# 3: sugerencia
s0, s1 = ph(a, 2)
token(a, [(A1X + 150, AY + 100), (X2 - 60, 296)], s0 + 2, s0 + 9, "probá AP 2", bg=A.BLUE, hold=s1 - 1)
vis(a, a.text(X2, PY + 140, "el celular decide: puede ignorarlo", 16, A.TXT, A.SANS, 600, "middle"), 2)

# 4: FT
s0, s1 = ph(a, 3)
for k in range(2):
    token(a, [(X3 + 30, PY - 50), (A2X + 60, AY + 96)], s0 + 9 + k * 4, s0 + 11 + k * 4, "FT", bg=A.OK, hold=s0 + 11.2 + k * 4)
    token(a, [(A2X + 60, AY + 96), (X3 + 30, PY - 50)], s0 + 11 + k * 4, s0 + 13 + k * 4, "FT", bg=A.OK, hold=s0 + 13.2 + k * 4)
vis(a, line(a, [(X3 + 40, PY - 46), (A2X + 70, AY + 92)], A.OK, 3, "6 5"), 3)
vis(a, a.text(X3 - 20, PY + 140, "pocas tramas: la voz no se corta", 16, A.OK, A.SANS, 600, "middle"), 3)

# 5: patear
s0, s1 = ph(a, 4)
token(a, [(A1X + 150, AY + 100), (X2 - 60, 296)], s0 + 3, s0 + 9, "desconexión", bg=A.BAD, hold=s1 - 1)
vis(a, a.text(X2, PY + 140, "bajo el umbral lo patea, y no tiene adónde ir", 16, A.BAD, A.SANS, 600, "middle"), 4)

a.add(note(a, 48, 600, 1104, "El roaming lo decide el cliente. Lo que no tolera Fast Roaming va a un SSID de legado.", "info", size=16, h=44))

write(a, "9-t1.svg", "Roaming con 802.11k, v y r", mid_pcts(a))
