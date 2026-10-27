"""Teoría de Entradas y salidas: la corriente por el fin de línea dice el estado de la zona."""
from _anim_bi import *

caps = ["Reposo: una corriente chica pasa por el fin de línea.",
        "Un detector entra en alarma: la corriente sube.",
        "Se repone: la corriente vuelve al valor de reposo.",
        "Cable cortado: no pasa corriente y el módulo marca avería."]
a = new(24, "Fin de línea", "Lo que el módulo lee en una zona convencional", caps, still=0)

a.add(card(a, 48, 220, 240, 110, "FLM-420/4-CON", "zona convencional", dark=True))
a.add(f'<path d="M290 250 H1000 V310" fill="none" stroke="{a.BLUE}" stroke-width="4"/><path d="M290 310 H950" stroke="{a.INK}" stroke-width="3"/>')
for x in (520, 760):
    a.add(f'<path d="M{x} 250 V280 M{x} 310 V300" stroke="{a.GREY}" stroke-width="2"/>')
    a.add(det(a, x, 280, 22))
vis(a, led(a, 520, 280, a.BAD, 5), 1)
# fin de línea
a.add(a.box(950, 290, 100, 40, a.WHITE, a.INK, rx=6, sw=2))
a.add(f'<path d="M962 310 l8 -10 l10 20 l10 -20 l10 20 l10 -20 l8 10" fill="none" stroke="{a.INK}" stroke-width="2"/>')
a.add(a.text(1000, 356, "fin de línea", 15, a.INK, a.SANS, 600, "middle"))
# corriente
flow(a, "M290 250 H1000 V300", a.OK, 0, still=1, width=5, dash="6 18")
flow(a, "M290 250 H520 V280", a.BAD, 1, width=7, dash="10 8")
flow(a, "M290 250 H1000 V300", a.OK, 2, width=5, dash="6 18")
vis(a, f'<path d="M846 236 l24 28 M870 236 l-24 28" stroke="{a.BAD}" stroke-width="5" stroke-linecap="round"/>', 3)
# lectura del módulo
for i, (t, col, bg) in enumerate([("Normal", a.OK, a.OKBG), ("Alarma de zona", a.BAD, a.BADBG), ("Normal", a.OK, a.OKBG), ("Avería", a.AMB, a.AMBBG)]):
    vis(a, a.pill(168, 370, t, col, bg, size=17, anchor="middle"), i)
a.add(a.text(48, 440, "QUÉ LEE EL MÓDULO", 14, a.GREY, a.MONO, 600))
for i, (t, s, col) in enumerate([("Reposo", "corriente chica, por el fin de línea", a.OK), ("Alarma", "corriente más alta, por el detector", a.BAD), ("Corte", "sin corriente: avería", a.AMB)]):
    y = 476 + i * 46
    a.add(f'<circle cx="60" cy="{y - 6}" r="8" fill="{col}"/>')
    a.add(a.text(80, y, t, 18, a.INK, a.SANS, 600))
    a.add(a.text(200, y, s, 17, a.TXT))
a.add(a.text(48, 640, "Sin fin de línea, un cable cortado y una zona en reposo se verían iguales.", 16, a.TXT))
write(a, "7-t1.svg", "Fin de línea", [12, 37, 62, 90])
