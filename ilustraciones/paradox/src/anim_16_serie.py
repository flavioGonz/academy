"""Teoría lección 16: el puerto serie desde firmware 7.50 y el desbloqueo."""
from _apdx import *

a = new(22, "Firmware 7.50: el puerto serie cambia de dueño")
a.steps(["Antes de 7.50: una integración de terceros habla por el puerto serie.",
         "Se actualiza a 7.50 o más: el serie atiende solo dispositivos Paradox.",
         "Se compra el código de desbloqueo en BlueEye (5 USD por central).",
         "Cargado en [300] (MG/SP+) o [3000] (EVO): la integración vuelve."], still=1)
a.add(card(a, 48, 220, 300, 150, "Central", None, dark=True))
for s, e, t, still in [(0, 25, "firmware < 7.50", 0), (25, 100, "firmware 7.50 o más", 1)]:
    at(a, a.text(68, 300, t, 17, "#9FE3F7" if s == 0 else "#FFD28A", a.MONO, 700), s, e, still)
at(a, chip(a, 68, 320, "serie desbloqueado", "ok"), 75, 100, 0)
a.add(card(a, 640, 220, 300, 150, "Integración", "domótica de terceros"))
a.add(card(a, 640, 420, 300, 110, "Módulo Paradox", "IP150+ o IP180"))
a.add(a.text(360, 270, "puerto serie", 14, a.GREY, a.MONO, 600))
at(a, line(a, "M348 300H634", a.OK, 5) + a.text(490, 290, "funciona", 15, a.OK, a.MONO, 700, "middle"), 0, 25, 0)
at(a, line(a, "M348 300H634", a.BAD, 5, "8 8") + chip(a, 490, 316, "solo Paradox", "bad", anchor="middle"), 25, 75, 1)
at(a, line(a, "M348 300H634", a.OK, 5) + a.text(490, 290, "funciona", 15, a.OK, a.MONO, 700, "middle"), 75, 100, 0)
a.add(line(a, "M300 370V475H634", a.OK, 4))
a.add(a.text(320, 460, "los módulos Paradox siguen", 15, a.OK, a.SANS, 600))
a.add(card(a, 980, 220, 172, 150, "BlueEye", "Unlock Panel"))
at(a, chip(a, 1000, 330, "5 USD", "amb"), 50, 100, 0)
at(a, a.arrow("M980 330C800 400 500 400 360 352", a.AMB, 3, "6 6") + a.text(640, 404, "código de desbloqueo", 15, a.AMB, a.MONO, 700, "middle"), 50, 75, 0)
caption(a, 600, [(0, 25, "Pasó primero en EVO y después en las plus.", None),
                 (25, 50, "PAI recomienda directamente no actualizar EVO a 7.50 si se usa el serie.", a.AMB),
                 (50, 75, "Se carga desde un TM50, TM70, K641+ o K32LCD+: admiten letras.", None),
                 (75, 100, "La decisión es por sitio: actualizar, desbloquear, migrar o dejar.", a.OK)], still=1)
write(a, "16-t1.svg", "Firmware 7.50: el puerto serie cambia de dueño",
      "Animación en cuatro tiempos. 1: con firmware anterior a 7.50, una integración de terceros funciona por el puerto serie. "
      "2: con firmware 7.50 o más, el serie solo atiende dispositivos Paradox y la integración se corta; los módulos Paradox siguen andando. "
      "3: se compra en BlueEye, con Unlock Panel, el código de desbloqueo, 5 dólares por central. 4: cargado en la sección 300 de MG y SP+ o 3000 de EVO, la integración vuelve a funcionar.")
