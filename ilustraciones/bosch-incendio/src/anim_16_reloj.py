"""Teoría de Mantener y registrar: el reloj del panel y el historial."""
from _anim_bi import *

caps = ["Antes de 4.8: en un año el reloj del panel puede correrse hasta 80 min.",
        "Un evento de las 03:12 queda en el panel con otra hora.",
        "Con firmware 4.8, el desvío baja a 10 min por año.",
        "En cada visita, Set Panel Time: relojes iguales y hora anotada."]
a = new(24, "Mantenimiento", "Un reloj corrido desordena el historial", caps, still=3)

a.add(card(a, 100, 190, 400, 200, "Hora real", "monitoreo y laptop"))
a.add(card(a, 700, 190, 400, 200, "Hora del panel", "historial de 10000 mensajes", dark=True))
vis(a, a.text(300, 366, "03:12", 34, a.INK, a.MONO, 700, "middle"), 0, 3)
vis(a, a.text(900, 366, "01:52", 34, a.BAD, a.MONO, 700, "middle"), 0, 1)
vis(a, a.text(900, 366, "03:02", 34, a.AMB, a.MONO, 700, "middle"), 2)
vis(a, a.text(900, 366, "03:12", 34, "#7FE0B0", a.MONO, 700, "middle"), 3)
vis(a, a.pill(900, 404, "hasta 80 min por año", a.BAD, a.BADBG, anchor="middle"), 0, 1)
vis(a, a.pill(900, 404, "hasta 10 min por año", a.AMB, a.AMBBG, anchor="middle"), 2)
vis(a, a.pill(900, 404, "Set Panel Time", a.OK, a.OKBG, anchor="middle"), 3)
vis(a, a.box(100, 450, 1000, 90, a.BADBG, a.BAD, rx=14, sw=2) + a.text(124, 488, "Monitoreo: alarma 03:12   ·   Panel: alarma 01:52", 20, a.BAD, a.MONO, 600)
    + a.text(124, 520, "el informe no coincide con lo que vio el monitoreo", 16, a.TXT), 1)
vis(a, a.box(100, 450, 1000, 90, a.OKBG, a.OK, rx=14, sw=2) + a.text(124, 488, "Informe: hora antes 03:02 · corregida con Set Panel Time", 20, a.OK, a.MONO, 600)
    + a.text(124, 520, "monitoreo y panel cuentan la misma historia", 16, a.TXT), 3)
a.add(a.text(48, 620, "Horas de ejemplo. Bosch sugiere revisar el reloj en cada mantenimiento.", 17, a.TXT))
write(a, "16-t1.svg", "El reloj del panel", [12, 37, 62, 90])
