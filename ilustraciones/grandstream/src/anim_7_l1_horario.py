#!/usr/bin/env python3
"""Lección 7 (IVR con horario) · Laboratorio, paso 1: Office Time/Holiday. La central compara su hora con esa
definición y la tecla 1 cambia de destino; con la zona horaria mal, el cambio ocurre a la hora equivocada.
Fuentes: la lección (la central compara la hora actual con Office Time/Holiday; conviene la zona horaria bien
configurada; tecla 1: Office Time → Ring Group ventas, fuera de horario → Voicemail 1001; el 1 de mayo, feriado
cargado, también al buzón). Uruguay: UTC-3."""
from _anim_gs_red import R

g = R(T=26, fix=88, kicker="GRANDSTREAM · IVR CON HORARIO · LABORATORIO",
      title="El reloj de la central elige el destino")
g.steps([
    "Office Time de lunes a viernes, 9 a 18: un martes a las 10:00 la tecla 1 va a ventas.",
    "El mismo martes a las 20:00 es fuera de horario: la tecla 1 va al buzón de la 1001.",
    "El 1 de mayo, cargado como Holiday: a las 10:00 también va al buzón.",
    "Con la zona en GMT, a las 16:30 de acá la central cree que son las 19:30: buzón.",
])

# línea del día
LX, LY, LW = 48, 236, 1104
def xh(h):
    return LX + LW * h / 24
g.add(g.text(LX, LY - 16, "un día en la central", 15, g.GREY, g.MONO))
g.add(g.box(LX, LY, LW, 34, "#E6EDF4", rx=8))
g.appear(g.box(xh(9), LY, xh(18) - xh(9), 34, g.OKBG, g.OK, rx=8, sw=2) + g.text(xh(13.5), LY + 23, "Office Time 9 a 18", 15, g.OK, g.MONO, 600, "middle"), 0, 50)
g.appear(g.box(xh(9), LY, xh(18) - xh(9), 34, g.OKBG, g.OK, rx=8, sw=2) + g.text(xh(13.5), LY + 23, "Office Time 9 a 18", 15, g.OK, g.MONO, 600, "middle"), 75, 100)
g.appear(g.box(LX, LY, LW, 34, g.AMBBG, g.AMB, rx=8, sw=2) + g.text(xh(18), LY + 23, "Holiday: 1 de mayo, todo el día", 15, g.AMB, g.MONO, 600, "middle"), 50, 75)
for h in (0, 6, 9, 12, 18, 24):
    g.add(g.text(xh(h), LY + 56, f"{h}:00", 14, g.GREY, g.MONO, 400, "middle" if 0 < h < 24 else ("start" if h == 0 else "end")))

def cursor(h, t0, t1, color, label, dy=0):
    x = xh(h)
    g.appear(f'<line x1="{x}" y1="{LY - 8}" x2="{x}" y2="{LY + 42}" stroke="{color}" stroke-width="4"/>'
             + g.pillc(x, LY + 66 + dy, label, g.WHITE, color, 14, 28), t0, t1)

cursor(10, 2, 25, g.BLUE, "martes 10:00")
cursor(20, 27, 50, g.BLUE, "martes 20:00")
cursor(10, 52, 75, g.BLUE, "1 de mayo 10:00")
cursor(16.5, 77, 100, g.INK, "acá: 16:30")
cursor(19.5, 80, 100, g.BAD, "la central: 19:30", dy=36)

# destinos de la tecla 1
DY = 400
g.add(g.text(48, DY - 14, "IVR 7000 · tecla 1", 16, g.INK, g.SANS, 600))
g.add(g.box(48, DY, 530, 92, g.WHITE, g.LINE, rx=14) + g.text(70, DY + 36, "Office Time", 15, g.GREY, g.MONO)
      + g.text(70, DY + 66, "Ring Group ventas", 20, g.INK, g.HEAD, 600))
g.add(g.box(622, DY, 530, 92, g.WHITE, g.LINE, rx=14) + g.text(644, DY + 36, "Out of Office Time", 15, g.GREY, g.MONO)
      + g.text(644, DY + 66, "Voicemail 1001", 20, g.INK, g.HEAD, 600))
g.appear(g.box(48, DY, 530, 92, "none", g.OK, rx=14, sw=3.5) + g.pill(420, DY + 32, "ahora", g.WHITE, g.OK, 14, 28), 4, 25)
g.appear(g.box(622, DY, 530, 92, "none", g.AMB, rx=14, sw=3.5) + g.pill(994, DY + 32, "ahora", g.WHITE, g.AMB, 14, 28), 29, 75)
g.appear(g.box(622, DY, 530, 92, "none", g.BAD, rx=14, sw=3.5) + g.pill(994, DY + 32, "ahora", g.WHITE, g.BAD, 14, 28), 82, 100)

g.appear(g.note(48, 516, 1104, None, ["System Settings > Time Settings > Office Time/Holiday: la central compara su hora con esta definición en cada llamada."], "info"), 0, 75)
g.appear(g.note(48, 516, 1104, None, ["La zona horaria de la UCM tiene que ser la de Montevideo (UTC-3): si no, el horario cambia a la hora equivocada."], "bad"), 75, 100)

g.status(632, [
    (0, 25, "Dentro de Office Time: la tecla 1 toma el primer destino.", g.OK),
    (25, 50, "Fuera de horario, la misma tecla cambia de destino sola.", g.AMB),
    (50, 75, "El feriado va cargado aparte: ese día no hay Office Time.", g.AMB),
    (75, 100, "Para probar fuera de horario, se cambia el horario de oficina y se vuelve a llamar.", g.INK),
])

g.done(7, "l1", "El reloj de la central elige el destino",
       "Animación en cuatro tiempos con una línea de un día en la central, con Office Time de 9 a 18, y abajo los dos destinos de la tecla 1 del IVR 7000: Office Time al Ring Group ventas y Out of Office Time al Voicemail 1001. "
       "1: un martes a las 10:00, dentro de Office Time, la tecla 1 va al Ring Group ventas. "
       "2: el mismo martes a las 20:00 es fuera de horario y la tecla 1 va al buzón de la 1001. "
       "3: el 1 de mayo, cargado como Holiday, a las 10:00 también va al buzón. "
       "4: con la zona horaria de la UCM en GMT, a las 16:30 de Montevideo la central cree que son las 19:30 y la tecla 1 va al buzón con la oficina abierta. "
       "Se configura en System Settings > Time Settings > Office Time/Holiday, y la zona horaria tiene que ser la de Montevideo, UTC-3. Para probar fuera de horario se cambia el horario de oficina y se vuelve a llamar.",
       [10, 36, 62, 90])
