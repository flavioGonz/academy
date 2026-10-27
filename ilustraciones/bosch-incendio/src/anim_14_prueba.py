"""Teoría de Aislar y avisar: la secuencia de una prueba segura."""
from _anim_bi import *

caps = ["Aviso al monitoreo y a los ocupantes.",
        "Salidas deshabilitadas, extinción bloqueada: LED amarillo fijo.",
        "Prueba en revisión: el detector da alarma y nada se mueve.",
        "Todo rehabilitado: el LED amarillo fijo se apaga.",
        "Panel en reposo: aviso de fin al monitoreo."]
a = new(30, "Pruebas", "Aislar, probar, rehabilitar, avisar", caps, still=3)

a.add(card(a, 450, 200, 300, 120, "Panel", "", dark=True))
a.add(a.text(470, 296, "LED", 14, "#9FC3E3", a.MONO))
a.add(led(a, 520, 291, "#24496E", 8))
vis(a, led(a, 520, 291, "#F2B01E", 8), 1, 2)
a.add(card(a, 900, 210, 250, 100, "Monitoreo", "empresa y operador"))
a.add(a.box(60, 210, 220, 100, a.WHITE, a.LINE, rx=14)); a.add(det(a, 112, 260, 30)); a.add(a.text(160, 266, "detector", 16, a.INK, a.SANS, 600))
vis(a, led(a, 112, 260, a.BAD, 6), 2)
O = ["Transmisión", "Puertas", "Ventilación", "Extinción"]
for i, t in enumerate(O):
    x = 60 + i * 280
    a.add(a.box(x, 420, 250, 90, a.WHITE, a.LINE, rx=14, sw=2))
    a.add(a.text(x + 20, 458, t, 18, a.INK, a.SANS, 600))
    a.add(line(a, 600, 322, x + 125, 418, a.LINE, 2, arrow=False))
    vis(a, a.box(x, 420, 250, 90, "none", a.GREY, rx=14, sw=3) + a.text(x + 20, 488, "bloqueada por su empresa" if t == "Extinción" else "deshabilitada", 15, a.GREY, a.MONO), 1, 2)
    vis(a, a.box(x, 420, 250, 90, "none", a.OK, rx=14, sw=3) + a.text(x + 20, 488, "rehabilitada", 15, a.OK, a.MONO), 3, 4)
s0, s1 = ph(a, 0)
token(a, "aviso: prueba", [(s0 + 2, 700, 184), (s0 + 14, 1025, 184), (s1 - 1, 1025, 184)], bg=a.BLUE)
s0, s1 = ph(a, 2)
token(a, "alarma", [(s0 + 2, 290, 260), (s0 + 12, 440, 260), (s1 - 1, 440, 260)], bg=a.BAD)
vis(a, a.pill(600, 384, "nada se activa", a.GREY, a.SLATE, anchor="middle"), 2)
s0, s1 = ph(a, 4)
token(a, "aviso: fin", [(s0 + 2, 700, 184), (s0 + 14, 1025, 184), (s1 - 1, 1025, 184)], bg=a.OK)
a.add(a.text(48, 590, "LED amarillo fijo: hay algo deshabilitado. Tiene que terminar apagado.", 17, a.INK, a.SANS, 600))
a.add(a.text(48, 622, "Con gas, la prueba se coordina con la empresa de extinción y su central bloqueada.", 16, a.TXT))
write(a, "14-t1.svg", "Una prueba segura", [10, 30, 50, 70, 90])
