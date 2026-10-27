"""Teoría lección 13: una falla de AC, del TBL al reporte."""
from _apdx import *

a = new(24, "Una falla de AC: se ve ya, se reporta después")
a.steps(["Se corta la red: TBL enciende el 2 y el LED de estado cambia de ritmo.",
         "En el submenú del 2, el 2 (falla de AC). La central espera [839].",
         "Pasan 15 min de fábrica: recién ahí reporta la falla a monitoreo.",
         "Vuelve la red: la falla se restaura sola y TBL se apaga."], still=1)
# teclado
a.add(a.box(48, 180, 300, 340, "#F1F4F7", "#C2D4E6", rx=20, sw=2))
a.add(a.box(72, 204, 252, 70, "#0B3A66", None, rx=8))
for s, e, t, still in [(0, 25, "TBL: 2", 0), (25, 75, "2 > 2: falla AC", 1), (75, 100, "sin fallas", 0)]:
    at(a, a.text(90, 248, t, 22, "#9FE3F7", a.MONO, 700), s, e, still)
for i in range(10):
    r, k = divmod(i, 5)
    x, y = 72 + k * 50, 300 + r * 56
    a.add(a.box(x, y, 42, 42, a.WHITE, "#C2D4E6", rx=8) + a.text(x + 21, y + 27, str(i + 1), 16, a.GREY, a.MONO, 600, "middle"))
at(a, a.box(122, 300, 42, 42, a.CYAN, None, rx=8) + a.text(143, 327, "2", 16, "#fff", a.MONO, 700, "middle"), 0, 75, 1)
a.add(a.text(72, 470, "LED de estado:", 15, a.GREY, a.SANS, 600))
at(a, chip(a, 72, 482, "1 s sí, 1 s no", "amb"), 0, 75, 1)
at(a, chip(a, 72, 482, "un destello por segundo", "ok"), 75, 100, 0)
# línea de tiempo
X0, X1, Y = 420, 1140, 330
a.add(line(a, f"M{X0} {Y}H{X1}", a.LINE, 10))
at(a, line(a, f"M{X0} {Y}H760", a.AMB, 10) + a.text(590, Y - 22, "retardo [839] · 15 min", 16, a.AMB, a.MONO, 700, "middle"), 0, 100, 1)
at(a, line(a, f"M760 {Y}H1000", a.BAD, 10), 50, 100, 0)
for x, lab in [(420, "corte"), (760, "reporte"), (1000, "vuelve la red")]:
    a.add(f'<circle cx="{x}" cy="{Y}" r="9" fill="#fff" stroke="{a.INK}" stroke-width="3"/>' + a.text(x, Y + 38, lab, 15, a.INK, a.SANS, 600, "middle"))
mv = a.move([(0, 420, Y), (50, 760, Y), (75, 1000, Y), (100, 1000, Y)])
a.add(a.group(f'<circle cx="0" cy="0" r="14" fill="{a.CYAN}" stroke="#fff" stroke-width="3"/>', mv, a.keyframes([(0, 1), (100, 1)]), still=0))
a.add(card(a, 760, 420, 392, 100, "Monitoreo", None))
at(a, a.text(784, 494, "nada todavía", 17, a.GREY, a.SANS, 600), 0, 50, 1)
at(a, a.text(784, 494, "falla de AC · abonado 1A01", 17, a.BAD, a.SANS, 700), 50, 100, 0)
caption(a, 600, [(0, 25, "El cliente oye pitidos: la central ya está diciendo qué le pasa.", None),
                 (25, 50, "El retardo evita mandar a monitoreo cada microcorte de luz.", None),
                 (50, 75, "El valor de [839] se acuerda con la empresa de monitoreo.", a.AMB),
                 (75, 100, "Otras fallas no se van solas: un módulo quitado se borra en [955].", None)], still=1)
write(a, "13-t1.svg", "Una falla de AC: se ve ya, se reporta después",
      "Animación en cuatro tiempos con un teclado y una línea de tiempo. 1: se corta la red, TBL enciende el grupo 2 y el LED de estado pasa a un segundo encendido y uno apagado. "
      "2: en el submenú aparece la falla de AC y la central espera el retardo de la sección 839, 15 minutos de fábrica. 3: pasado el retardo, la central reporta la falla de AC a monitoreo. "
      "4: vuelve la red, la falla se restaura sola, TBL se apaga y el LED vuelve a un destello por segundo.", pcts=(12, 37, 62, 90))
