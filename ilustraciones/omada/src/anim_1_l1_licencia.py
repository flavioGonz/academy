#!/usr/bin/env python3
"""Lección 1 · Laboratorio, paso 3: la vida de una licencia de Central Standard. Corre desde que se activa,
el equipo sin licencia queda Unactivated, aviso 30 días antes, y al vencer el equipo sigue con lo último
pero se apagan gestión, monitoreo, Portal, Fast Roaming y Schedule."""
from _anim_om_red import *

a = nueva(24, "DÓNDE VIVE", "Una licencia de Central Standard, de punta a punta", "l")
F = a.steps([
    "Se activa la licencia: el plazo empieza a correr, esté asignada o no.",
    "Se asigna al EAP: el equipo pasa a gestionarse desde Omada Central.",
    "30 días antes del vencimiento llega el aviso por correo: alguien tiene que renovar.",
    "Vence: el EAP sigue con lo último, pero se apagan las funciones del controlador.",
], still=3)

# línea de tiempo
X0, X1, Y = 120, 1080, 268
a.add(a.box(48, 190, 1104, 150, a.WHITE, a.LINE, rx=16))
a.add(line(X0, Y, X1, Y, a.LINE, 8))
TICKS = [(X0, "activación"), (330, "asignada al EAP"), (880, "aviso: 30 días"), (X1, "vence")]
for x, lab in TICKS:
    a.add(line(x, Y - 14, x, Y + 14, a.GREY, 2))
    a.add(a.text(x, Y + 40, lab, 15, a.GREY, a.MONO, 400, "middle"))
a.add(a.text(72, 222, "Plazo de la licencia", 16, a.INK, a.SANS, 600))
# barra que se llena con el tiempo (escalones por fase)
fill_pts = [(0, X0), (22, 330), (50, 880), (72, X1), (100, X1)]
fill = a.keyframes([(p, f"{(x - X0) / (X1 - X0):.3f}") for p, x in fill_pts], "transform", "scaleX({})")
a.n += 1
c = f"c{a.n}"
a.css.append(f".{c}{{transform-box:view-box;transform-origin:{X0}px {Y}px;transform:scaleX(1);animation:{fill} {a.T}s linear infinite}}")
a.add(f'<g class="{c}">{line(X0, Y, X1, Y, a.BLUE, 8)}</g>')
# marcador "hoy"
mv = a.move([(0, X0, Y), (22, 330, Y), (50, 880, Y), (72, X1, Y), (100, X1, Y)])
a.add(a.group(f'<circle r="13" fill="{a.WHITE}" stroke="{a.BLUE}" stroke-width="4"/>', mv, a.keyframes([(0, 1), (100, 1)]), still=0))
solo_fijo(a, f'<circle cx="{X1}" cy="{Y}" r="13" fill="{a.WHITE}" stroke="{a.BAD}" stroke-width="4"/>')
at(a, chip(a, X1, 206, "vencida", a.BAD, a.BADBG, anchor="end", stroke=a.BAD), 74, 100, still=1)
at(a, chip(a, 880, 206, "renovar", a.AMB, a.AMBBG, anchor="middle", stroke=a.AMB), 52, 74)

# equipos
a.add(dev(a, 48, 362, 330, 96, "Omada Central", "Standard · nube de TP-Link", icon="cloud", dark=True))
a.add(dev(a, 48, 478, 330, 96, "EAP del local", "sitio Sucursal", icon="wifi"))
a.add(dev(a, 420, 362, 300, 96, "Aviso por correo", "al responsable", icon="user", sub2="30 días antes"))
# enlace Central - EAP
a.add(line(213, 458, 213, 478, a.LINE, 3))
for t0 in (32, 40):
    travel(a, dot(a, a.CYAN), [(250, 458), (250, 478)], t0, t0 + 2, hold=0.5)
at(a, line(213, 458, 213, 478, a.OK, 4), 30, 76)
at(a, line(213, 458, 213, 478, a.BAD, 4, "5 4"), 76, 100, still=1)
# aviso por correo
travel(a, dot(a, a.AMB), [(378, 410), (420, 410)], 54, 57, hold=0.5)
at(a, check(a, 690, 410, 13), 57, 100)

# estado del EAP (panel derecho)
PX, PY, PW, PH = 750, 362, 402, 212
a.add(a.box(PX, PY, PW, PH, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 22, PY + 34, "Estado del EAP en Central", 16, a.GREY, a.SANS, 600))
at(a, chip(a, PX + 22, PY + 54, "Unactivated", a.AMB, a.AMBBG, stroke=a.AMB)
   + a.text(PX + 22, PY + 118, "Adoptado pero sin licencia:", 16, a.INK)
   + a.text(PX + 22, PY + 142, "no se gestiona. La licencia", 16, a.INK)
   + a.text(PX + 22, PY + 166, "activada ya está corriendo.", 16, a.INK), 0, 25)
at(a, chip(a, PX + 22, PY + 54, "Connected", a.OK, a.OKBG, stroke=a.OK)
   + a.text(PX + 22, PY + 118, "Gestión, monitoreo, Portal,", 16, a.INK)
   + a.text(PX + 22, PY + 142, "Fast Roaming y Schedule", 16, a.INK)
   + a.text(PX + 22, PY + 166, "andando.", 16, a.INK), 25, 75)
at(a, chip(a, PX + 22, PY + 54, "licencia vencida", a.BAD, a.BADBG, stroke=a.BAD)
   + a.text(PX + 22, PY + 112, "Sigue con la última configuración.", 16, a.INK)
   + a.text(PX + 22, PY + 136, "Se apagan gestión, monitoreo,", 16, a.BAD, a.SANS, 600)
   + a.text(PX + 22, PY + 160, "Portal, Fast Roaming y Schedule.", 16, a.BAD, a.SANS, 600), 75, 100, still=1)

status(a, 618, [
    (0, 25, "Activar licencias antes de tener los equipos es pagar días que no se usan.", a.AMB, 0),
    (25, 50, "Las desvinculaciones de una licencia son limitadas: asignala al equipo correcto.", a.INK, 0),
    (50, 75, "En la planilla: cuántas licencias, cuándo vencen y quién las renueva.", a.INK, 0),
    (75, 100, "La red sigue andando, pero sin portal ni cambios hasta renovar.", a.BAD, 1),
], x=48, anchor="start")

write(a, 1, "l1", "La vida de una licencia de Omada Central Standard",
      "Animación en cuatro tiempos con una línea de tiempo del plazo de la licencia, Omada Central Standard, el EAP de un local y el correo del responsable de renovar. "
      "1: se activa la licencia y el plazo empieza a correr aunque todavía no esté asignada; el EAP adoptado sin licencia figura Unactivated y no se gestiona. "
      "2: la licencia se asigna al EAP, que pasa a Connected con gestión, monitoreo, Portal, Fast Roaming y Schedule andando; las desvinculaciones de una licencia son limitadas. "
      "3: 30 días antes del vencimiento llega un aviso por correo y alguien tiene que renovar. "
      "4: la licencia vence; el EAP sigue funcionando con la última configuración, pero se apagan la gestión, el monitoreo, el Portal, Fast Roaming y Schedule hasta renovar.",
      [8, 36, 60, 88])
