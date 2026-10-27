"""Teoría lección 8: Last State contra Power On cuando una UPS apaga el servidor en orden."""
from _awin import *

a = new(20, "Corte de luz con UPS: Last State contra Power On")
a.steps(["Se corta la luz: la UPS sostiene los dos servidores.",
         "Batería baja: la UPS los apaga en orden.",
         "Vuelve la luz: Last State recuerda \"apagado\".",
         "Power On arranca siempre: el VMS vuelve solo."], still=3)
# red eléctrica
a.add(a.text(48, 200, "Red eléctrica", 17, a.INK, a.HEAD, 600))
at(a, chip(a, 200, 180, "corte", "bad"), 0, 50, 0)
at(a, chip(a, 200, 180, "volvió", "ok"), 50, 100, 1)
a.add(card(a, 48, 240, 220, 110, "UPS", "con apagado ordenado"))
at(a, a.text(68, 334, "batería ▼", 15, a.AMB, a.MONO, 600), 0, 50, 0)
for k, (y, name) in enumerate(((210, "BIOS: Last State"), (400, "BIOS: Power On"))):
    a.add(line(a, f"M268 295H330V{y + 60}H420", a.GREY, 3))
    a.add(card(a, 420, y, 300, 120, "Servidor del VMS", name))
    a.add(a.text(760, y + 50, "estado:", 15, a.GREY, a.SANS, 500))
    at(a, chip(a, 760, y + 62, "encendido · con UPS", "amb"), 0, 25, 0)
    at(a, chip(a, 760, y + 62, "apagado en orden", "grey"), 25, 50, 0)
# 3 y 4: vuelta de la luz
at(a, chip(a, 760, 272, "sigue apagado", "bad"), 50, 100, 1)
at(a, a.box(420, 210, 300, 120, "none", a.BAD, rx=14, sw=4), 52, 100, 1)
at(a, a.text(760, 320, "recordó \"apagado\": nadie lo prende", 15, a.BAD, a.SANS, 600), 54, 100, 1)
at(a, chip(a, 760, 462, "arrancó solo", "ok"), 75, 100, 1)
at(a, a.box(420, 400, 300, 120, "none", a.OK, rx=14, sw=4), 75, 100, 1)
at(a, a.text(760, 510, "vuelve cada vez que vuelve la luz", 15, a.OK, a.SANS, 600), 77, 100, 1)
at(a, chip(a, 760, 462, "esperando…", "grey"), 50, 75, 0)
caption(a, 590, [(0, 25, "Mientras la UPS aguanta, los dos siguen grabando.", None),
                 (25, 50, "Para Windows fue un apagado prolijo, no un corte.", None),
                 (50, 75, "Last State vuelve solo si el equipo estaba prendido: acá estaba apagado.", a.BAD),
                 (75, 100, "Con UPS, Power On. La contra: también prende lo que apagaste a propósito.", a.OK)], still=3)
write(a, "8-t1.svg", "Corte de luz con UPS: Last State contra Power On",
      "Animación en cuatro tiempos con una UPS que alimenta dos servidores del VMS iguales: uno con el BIOS en Last State y otro en Power On. "
      "1: se corta la luz y la UPS sostiene a los dos, que siguen encendidos. 2: con la batería baja, la UPS los apaga en orden. "
      "3: vuelve la luz; el de Last State recuerda que estaba apagado y sigue apagado, marcado en rojo. "
      "4: el de Power On arranca solo, marcado en verde. Nota final: con UPS conviene Power On, con la contra de que también enciende equipos apagados a propósito.")
