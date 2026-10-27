"""Teoría de Quién abre: el orden de controles que atraviesa una lectura en el servidor."""
from _anim_lpr import *

caps = ["SBA1234 llega dos veces en 2 s: la segunda la descarta el antirrebote.",
        "La hora de la cámara vale si está a menos de 10 min de la del servidor.",
        "Si el XML trae whiteList o blackList, manda la cámara.",
        "Si no, normaliza y busca la credencial: con Lista Blanca, Autorizado.",
        "Al final, vigilancia y pases: la lista negra le gana a un pase."]
a = new(25, "Decisión", "Los controles que atraviesa una lectura", caps, still=3)

W, Y, H = 196, 182, 104
gates = [("Antirrebote", ["5 s por matrícula", "20 s por cámara"]),
         ("Hora", ["cámara o servidor"]),
         ("Lista de la cámara", ["whiteList", "blackList"]),
         ("Padrón y modo", ["credencial de", "tipo matrícula"]),
         ("Vigilancia y pases", ["después de decidir"])]
cx = [48 + i * 227 + W / 2 for i in range(5)]
for i, (t, subs) in enumerate(gates):
    x = 48 + i * 227
    s = a.box(x, Y, W, H, a.WHITE, a.LINE) + a.text(x + 16, Y + 32, t, 18, a.INK, a.SANS, 600)
    for k, sub in enumerate(subs):
        s += a.text(x + 16, Y + 60 + k * 22, sub, 15, a.GREY, a.MONO)
    a.add(s)
TY = 330
a.add(line(a, 40, TY, 1160, TY, a.LINE, 2, "4 6"))


def under(i, rows, step, color=None, d0=0):
    x = 48 + i * 227
    inner = "".join(a.text(x + 8, TY + 44 + k * 22, r, 15, color or a.TXT, a.SANS, 600 if k == 0 else 400) for k, r in enumerate(rows))
    vis(a, inner, step, d0=d0)


def mark(i, ok, step, d0=0):
    c, bg = (a.OK, a.OKBG) if ok else (a.BAD, a.BADBG)
    sym = '<path d="M-7 0 L-2 6 L8 -6" fill="none" stroke="%s" stroke-width="3"/>' % c if ok else \
          '<path d="M-6 -6 L6 6 M6 -6 L-6 6" fill="none" stroke="%s" stroke-width="3"/>' % c
    vis(a, f'<g transform="translate({cx[i]},{Y + H})"><circle r="14" fill="{bg}" stroke="{c}" stroke-width="2"/>{sym}</g>', step, d0=d0)


# resultado
RY = 470
a.add(a.box(48, RY, 1104, 96, a.WHITE, a.LINE))
a.add(a.text(72, RY + 36, "RESULTADO", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))


def result(step, txt, label, fg, bg, d0=10):
    vis(a, a.text(72, RY + 70, txt, 17, a.INK, a.SANS, 600) + a.pill(1130, RY + 30, label, fg, bg, size=16, h=36, anchor="end"), step, d0=d0)


# 1 · antirrebote
s0, s1 = ph(a, 0)
token(a, "SBA1234", [(s0 + 1, 40, TY), (s0 + 6, cx[0], TY), (s0 + 12, cx[1] + 40, TY), (s0 + 13, cx[1] + 40, TY)])
token(a, "SBA1234 · 2 s después", [(s0 + 8, 100, TY), (s0 + 13, cx[0] - 10, TY), (s1, cx[0] - 10, TY)], bg=a.GREY)
mark(0, False, 0, d0=13)
under(0, ["la segunda: descartada", "(Debounced)"], 0, a.BAD, d0=13)
result(0, "Misma matrícula dentro de 5 s: se registra una sola vez.", "descartada", a.GREY, "#E6EDF4", d0=13)
# 2 · hora
s0, s1 = ph(a, 1)
token(a, "hora cámara 14:30:02", [(s0 + 1, 60, TY), (s0 + 7, cx[1], TY), (s1, cx[1], TY)], bg=a.BLUE)
mark(1, True, 1, d0=8)
under(1, ["< 10 min: la de la cámara", "si no: la del servidor"], 1, d0=8)
result(1, "El evento queda con la hora de la cámara: 14:30:02.", "hora ok", a.OK, a.OKBG)
# 3 · lista de la cámara
s0, s1 = ph(a, 2)
token(a, "XML con whiteList", [(s0 + 1, 60, TY), (s0 + 5, cx[2], TY), (s0 + 8, cx[2], TY), (s0 + 11, cx[4], TY), (s1, cx[4], TY)])
mark(2, True, 2, d0=5)
under(2, ["manda la cámara"], 2, a.OK, d0=5)
under(3, ["no hace falta"], 2, a.GREY, d0=9)
result(2, "La cámara ya la tenía en su lista blanca y cerró su relé.", "Autorizado", a.OK, a.OKBG, d0=11)
# 4 · padrón
s0, s1 = ph(a, 3)
token(a, "SBA-1234", [(s0 + 1, 60, TY), (s0 + 5, cx[2], TY), (s0 + 8, cx[3] - 4, TY)])
token(a, "SBA1234", [(s0 + 8, cx[3], TY), (s0 + 10, cx[3], TY), (s0 + 12, cx[4], TY), (s1, cx[4], TY)], still=1)
under(2, ["sin lista en el XML"], 3, a.GREY, d0=5)
mark(3, True, 3, d0=8)
under(3, ["SBA-1234 → SBA1234", "en el padrón", "Modo: Lista Blanca"], 3, d0=8)
result(3, "Normalizada, encontrada y con el modo en Lista Blanca: pasa sola.", "Autorizado", a.OK, a.OKBG, d0=12)
# 5 · vigilancia y pases
s0, s1 = ph(a, 4)
token(a, "SAB2024 · con pase", [(s0 + 1, 60, TY), (s0 + 5, cx[3], TY), (s0 + 7, cx[3], TY), (s0 + 9, cx[4], TY), (s1, cx[4], TY)], bg=a.AMB)
under(3, ["no está en el padrón"], 4, a.AMB, d0=5)
mark(4, False, 4, d0=9)
under(4, ["pase: coincide", "lista negra: gana"], 4, a.BAD, d0=9)
result(4, "Tiene pase, pero está en lista negra: rojo con sonido en el monitor.", "Lista negra", a.BAD, a.BADBG, d0=10)

a.add(a.text(48, 612, "Para el guardia, tres colores:", 17, a.TXT))
a.add(a.pill(300, 594, "verde Autorizado", a.OK, a.OKBG, size=15, h=30))
a.add(a.pill(490, 594, "ámbar Denegado", a.AMB, a.AMBBG, size=15, h=30))
a.add(a.pill(666, 594, "rojo lista negra", a.BAD, a.BADBG, size=15, h=30))
write(a, "2-t1.svg", "Orden de decisión de una lectura", [14, 34, 56, 75, 95])
