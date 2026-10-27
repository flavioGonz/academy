"""Teoría de Primer proyecto: el orden de cada descarga con RPS."""
from _anim_bi import *

caps = ["Antes de tocar: copia de la configuración del panel.",
        "Set Panel Time: la hora del panel queda igual a la de la laptop.",
        "Chequeo de consistencia: sin errores.",
        "Descarga, walk test, diagnóstico como acta y copia final."]
a = new(24, "Descarga", "Copia, hora, consistencia, descarga y acta", caps, still=3)

a.add(card(a, 60, 210, 300, 120, "Laptop con RPS", "FSP-5000-RPS 5.15.28"))
a.add(card(a, 560, 210, 300, 120, "Panel AVENAR", "por USB", dark=True))
a.add(line(a, 362, 270, 556, 270, a.LINE, 3, arrow=False))
s0, s1 = ph(a, 0)
token(a, "copia del panel", [(s0 + 2, 710, 250), (s0 + 16, 210, 250), (s1 - 1, 210, 250)], bg=a.GREY)
# relojes
vis(a, a.pill(210, 370, "10:00", a.INK, a.SLATE, size=18, anchor="middle") + a.pill(710, 370, "10:07", a.BAD, a.BADBG, size=18, anchor="middle"), 0)
vis(a, a.pill(210, 370, "10:00", a.INK, a.SLATE, size=18, anchor="middle") + a.pill(710, 370, "10:00", a.OK, a.OKBG, size=18, anchor="middle"), 1, 3)
vis(a, a.text(460, 420, "Set Panel Time", 18, a.BLUE, a.SANS, 600, "middle"), 1)
vis(a, a.pill(210, 440, "consistencia: 0 errores", a.OK, a.OKBG, anchor="middle"), 2, 3)
s0, s1 = ph(a, 3)
token(a, "descarga", [(s0 + 1, 210, 290), (s0 + 10, 710, 290), (s1 - 1, 710, 290)], bg=a.BLUE)
# checklist
items = ["Copia antes de tocar", "Set Panel Time", "Consistencia sin errores", "Descarga", "Walk test y pruebas", "Diagnóstico como acta", "Copia final"]
when = [0, 1, 2, 3, 3, 3, 3]
a.add(a.box(900, 180, 252, 380, a.WHITE, a.LINE, rx=14))
for k, (t, w) in enumerate(zip(items, when)):
    y = 222 + k * 48
    a.add(a.box(918, y - 18, 24, 24, a.WHITE, a.LINE, rx=5, sw=2))
    a.add(a.text(954, y + 1, t, 15, a.INK))
    vis(a, f'<path d="M922 {y - 6} l6 7 l12 -14" fill="none" stroke="{a.OK}" stroke-width="3.5" stroke-linecap="round"/>', w, 3)
a.add(a.text(48, 620, "Si la hora no coincide, RPS puede pedir una descarga completa aunque no haya cambios.", 17, a.TXT))
write(a, "9-t1.svg", "El orden de cada descarga", [12, 37, 62, 90])
