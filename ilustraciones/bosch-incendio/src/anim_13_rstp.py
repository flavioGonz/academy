"""Teoría de Paneles en red: el anillo Ethernet con RSTP ante un corte."""
from _anim_bi import *

caps = ["RSTP deja bloqueado el enlace C a A: no hay bucle.",
        "Se corta el cable entre A y B.",
        "RSTP habilita el enlace de reserva: A llega a B por C.",
        "El panel avisa la falla de red; todos siguen comunicados."]
a = new(24, "Red", "Un corte en el anillo: el enlace de reserva entra", caps, still=3)

A, B, C = (220, 270), (980, 270), (600, 520)
for (x, y), t, ip in ((A, "Panel A", "192.168.1.1"), (B, "Panel B", "192.168.1.2"), (C, "Panel C", "192.168.1.3")):
    a.add(card(a, x - 120, y - 50, 240, 100, t, ip, dark=True))
ab, bc, ca = "M342 270 H858", "M980 322 V520 H722", "M478 520 H220 V322"
a.add(f'<path d="{ab}" stroke="{a.BLUE}" stroke-width="4"/><path d="{bc}" fill="none" stroke="{a.BLUE}" stroke-width="4"/>')
# C-A: bloqueado (0,1) y activo (2,3)
vis(a, f'<path d="{ca}" fill="none" stroke="{a.GREY}" stroke-width="4" stroke-dasharray="6 8"/>' + a.pill(250, 420, "bloqueado por RSTP", a.GREY, a.SLATE), 0, 1)
vis(a, f'<path d="{ca}" fill="none" stroke="{a.BLUE}" stroke-width="4"/>' + a.pill(250, 420, "habilitado", a.OK, a.OKBG), 2, 3)
flow(a, ab, a.CYAN, 0, width=6)
flow(a, bc, a.CYAN, 0, width=6)
vis(a, a.box(570, 246, 60, 48, a.BG, rx=8) + f'<path d="M584 256 l32 28 M616 256 l-32 28" stroke="{a.BAD}" stroke-width="5" stroke-linecap="round"/>', 1, 3)
flow(a, "M220 322 V520 H478", a.CYAN, 2, 3, width=6)
flow(a, "M722 520 H980 V322", a.CYAN, 2, 3, width=6)
vis(a, a.pill(600, 200, "falla de red", a.AMB, a.AMBBG, anchor="middle"), 3)
vis(a, a.pill(980, 360, "llega por C", a.OK, a.OKBG, anchor="middle"), 2, 3)
a.add(a.text(48, 640, "Por eso los puertos 1 y 2 de cada controlador se usan para la red de paneles: arman el anillo.", 16, a.TXT))
write(a, "13-t1.svg", "El anillo con RSTP", [12, 37, 62, 90])
