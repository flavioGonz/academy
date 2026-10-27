"""Teoría de Probar detectores: modo revisión y walk test simultáneo."""
from _anim_bi import *

caps = ["Fuera de revisión: el detector evalúa la señal; el aerosol no parece fuego.",
        "La zona pasa a modo revisión: el detector se prepara para la prueba.",
        "Aerosol con el cabezal: alarma dentro de los 10 s.",
        "Walk test simultáneo: si un sensor no responde, no hay alarma."]
a = new(24, "Pruebas", "En revisión el detector se prepara para la prueba", caps, still=2)

a.add(a.box(48, 170, 560, 22, "#E9EFF5", a.LINE, rx=6))
a.add(det(a, 330, 230, 36))
vis(a, led(a, 330, 230, a.CYAN, 8), 1)
vis(a, led(a, 330, 230, a.BAD, 8), 2)
for i in (0, 2):
    vis(a, f'<path d="M296 272 H364 L356 318 H304 Z" fill="#E5F0FB" stroke="{a.BLUE}" stroke-width="2.5"/><path d="M330 318 V470" stroke="{a.BLUE}" stroke-width="6" stroke-linecap="round"/>', i)
vis(a, a.pill(330, 500, "aerosol: evalúa, todavía sin alarma", a.AMB, a.AMBBG, anchor="middle"), 0)
vis(a, a.pill(330, 500, "modo revisión: preparado", a.CYAN, a.WHITE, anchor="middle"), 1)
vis(a, a.pill(330, 500, "alarma en hasta 10 s", a.WHITE, a.BAD, anchor="middle"), 2)
a.add(card(a, 700, 190, 450, 110, "Panel", "zona 3", dark=True))
vis(a, a.pill(1130, 206, "normal", a.GREY, a.SLATE, anchor="end"), 0)
vis(a, a.pill(1130, 206, "zona en revisión", a.CYAN, a.WHITE, anchor="end"), 1, 2)
vis(a, a.pill(1130, 206, "walk test simultáneo", a.CYAN, a.WHITE, anchor="end"), 3)
# simultáneo
for k, (t, ok) in enumerate((("óptico", True), ("térmico", True), ("CO", False))):
    y = 350 + k * 56
    vis(a, a.box(700, y, 450, 44, a.WHITE, a.LINE, rx=10) + a.text(720, y + 29, t, 17, a.INK, a.SANS, 600)
        + a.pill(1130, y + 8, "responde" if ok else "no responde", a.OK if ok else a.BAD, a.OKBG if ok else a.BADBG, anchor="end"), 3)
vis(a, a.text(700, 540, "Sin los tres, el panel no muestra alarma:", 17, a.BAD, a.SANS, 600), 3)
vis(a, a.text(700, 566, "el sensor de CO está fallando.", 17, a.BAD, a.SANS, 600), 3)
a.add(a.text(48, 630, "Al terminar, la zona sale de revisión: en revisión no da alarma de fuego normal.", 17, a.TXT))
write(a, "15-t1.svg", "Modo revisión", [12, 37, 62, 90])
