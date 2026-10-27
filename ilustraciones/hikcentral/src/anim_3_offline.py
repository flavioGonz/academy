"""Teoría de Licencia sin sorpresas: activación offline, pedido y respuesta dentro de 24 horas."""
from _anim_hc import *

caps = ["El SYS sin internet genera el pedido, con un solo clic.",
        "El pedido viaja en un pendrive y se sube a kms.hikvision.com.",
        "El portal devuelve el archivo de respuesta de ese pedido.",
        "La respuesta vuelve al SYS, se importa y la licencia queda activa."]
a = new(24, "Licencias", "Activación offline: un pedido, una respuesta, 24 horas", caps, still=3)

a.add(card(a, 48, 210, 300, 92, "SYS", "sin internet", dark=True))
a.add(card(a, 450, 210, 300, 92, "PC con internet", "pendrive"))
a.add(card(a, 852, 210, 300, 92, "Portal de licencias", "kms.hikvision.com"))
REQ, RES = "ActivationRequestFile.bin", "ActivationResponseFile.bin"
s0, s1 = ph(a, 0)
vis(a, a.pill(198, 336, "Generate Request File · 1 clic", a.BLUE, a.SLATE, anchor="middle"), 0)
token(a, REQ, [(s0 + 6, 198, 380), (s1, 198, 380)], bg=a.BLUE)
s0, s1 = ph(a, 1)
token(a, REQ, [(s0, 198, 380), (s0 + 10, 600, 380), (s0 + 13, 600, 380), (s0 + 22, 1002, 380), (s1, 1002, 380)], bg=a.BLUE)
s0, s1 = ph(a, 2)
token(a, RES, [(s0 + 2, 1002, 380), (s0 + 12, 1002, 380), (s0 + 22, 600, 380), (s1, 600, 380)], bg=a.OK)
s0, s1 = ph(a, 3)
token(a, RES, [(s0, 600, 380), (s0 + 10, 198, 380), (s0 + 14, 198, 336)], bg=a.OK)
vis(a, a.pill(198, 336, "Import · Activate", a.OK, a.OKBG, anchor="middle"), 3)
vis(a, a.pill(198, 372, "licencia activa", a.WHITE, a.OK, anchor="middle"), 3)

# reloj de 24 horas
X0, X1, Y = 48, 1152, 452
a.add(a.text(X0, Y - 14, "Tiempo desde que se generó el pedido", 15, a.GREY, a.MONO))
a.add(a.box(X0, Y, X1 - X0, 30, a.SLATE, a.LINE, rx=15))
for i, frac in enumerate([0.03, 0.12, 0.2, 0.26]):
    vis(a, a.box(X0, Y, (X1 - X0) * frac, 30, a.CYAN, rx=15), i)
a.add(a.box(X1 - 2, Y - 10, 4, 50, a.BAD, rx=2))
a.add(a.text(X1, Y + 62, "24 h: después de eso, 1105", 15, a.BAD, a.MONO, 600, "end"))
a.add(a.text(X0, Y + 62, "0 h", 15, a.GREY, a.MONO))
vis(a, a.text(X0 + (X1 - X0) * 0.26 + 10, Y + 22, "dentro del plazo", 15, a.OK, a.SANS, 600), 3)

a.add(a.text(48, 592, "Un segundo clic en Generate invalida el primer pedido, y una respuesta de otro pedido no entra:", 17, a.TXT))
a.add(a.text(48, 620, "en los dos casos, 1105. Con la hora del SYS corrida más de 24 horas, falla por tiempo.", 17, a.TXT))
write(a, "3-t1.svg", "Activación offline", [10, 36, 60, 92])
