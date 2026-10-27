"""Teoría lección 12: por qué BitLocker pide la clave de recuperación tras un cambio de BIOS, y qué hace la suspensión."""
from _awin import *

a = new(24, "BitLocker al arrancar: el TPM compara antes de abrir")
a.steps(["Al arrancar, el TPM compara lo que mide con lo que guardó.",
         "Todo igual: libera la llave y Windows arranca sin pedir nada.",
         "Cambió el BIOS: no coincide y aparece la pantalla de recuperación.",
         "Suspendido por un reinicio: arranca y vuelve a proteger."], still=3)
a.add(card(a, 48, 190, 300, 260, "Arranque", "BIOS · firmware · cargador"))
rows = ["BIOS", "firmware", "cargador de arranque"]
for i, r in enumerate(rows):
    y = 300 + i * 46
    a.add(a.box(68, y - 24, 260, 38, a.SLATE, None, rx=8) + a.text(84, y + 2, r, 16, a.TXT, a.MONO, 600))
at(a, a.box(68, 276, 260, 38, a.AMBBG, a.AMB, rx=8, sw=2) + a.text(84, 302, "BIOS nuevo", 16, a.AMB, a.MONO, 700), 50, 100, 1)
a.add(card(a, 450, 190, 300, 260, "TPM", "guarda la llave del disco", dark=True))
a.add(a.text(470, 300, "medición guardada:", 15, "#9FC3E3", a.SANS, 500))
a.add(a.text(470, 330, "BIOS · firmware · cargador", 15, "#FFFFFF", a.MONO, 600))
a.add(card(a, 852, 190, 300, 260, "Disco C:", "cifrado con BitLocker"))
# medición viajando
mv = a.move([(0, 350, 320), (2, 350, 320), (12, 440, 320), (100, 440, 320)])
op = a.keyframes([(0, 0), (2, 0), (2.5, 1), (12, 1), (13, 0), (100, 0)])
a.add(a.group(f'<circle cx="0" cy="0" r="10" fill="{a.CYAN}"/>', mv, op, still=0))
at(a, chip(a, 600, 378, "compara", "info", anchor="middle"), 4, 25, 0)
# 2: coincide -> llave al disco
at(a, a.arrow("M752 320H842", a.OK, 4) + chip(a, 1002, 390, "abre · Windows arranca", "ok", anchor="middle"), 25, 50, 0)
at(a, chip(a, 600, 378, "coincide", "ok", anchor="middle"), 25, 50, 0)
# 3: no coincide -> recuperación
at(a, chip(a, 600, 378, "no coincide", "bad", anchor="middle"), 50, 75, 0)
at(a, a.box(852, 190, 300, 260, a.BADBG, a.BAD, rx=14, sw=3) + a.text(872, 236, "Recuperación", 19, a.BAD, a.HEAD, 600)
   + a.text(872, 268, "escribí la clave de", 16, a.TXT, a.SANS, 500) + a.text(872, 292, "48 dígitos", 16, a.TXT, a.SANS, 500)
   + a.text(872, 340, "######-######-…", 16, a.BAD, a.MONO, 600), 52, 75, 0)
# 4: suspendido
at(a, chip(a, 600, 378, "suspendido: no pide", "amb", anchor="middle"), 75, 100, 1)
at(a, a.arrow("M752 320H842", a.OK, 4) + chip(a, 1002, 390, "arranca · vuelve a proteger", "ok", anchor="middle"), 77, 100, 1)
caption(a, 520, [(0, 25, "El TPM es un chip que guarda la llave y solo la entrega si el arranque es el mismo.", None),
                 (25, 50, "Es lo que pasa todos los días: nadie ve nada.", a.OK),
                 (50, 75, "Para el TPM, un BIOS distinto podría ser alguien manipulando el arranque.", a.BAD),
                 (75, 100, "Suspend-BitLocker -RebootCount 1 deja pasar el cambio una vez y retoma solo.", a.OK)], still=3)
write(a, "12-t1.svg", "BitLocker al arrancar: el TPM compara antes de abrir",
      "Animación en cuatro tiempos con tres bloques: el arranque (BIOS, firmware y cargador), el TPM que guarda la llave y la medición del arranque, y el disco C: cifrado con BitLocker. "
      "1: al encender, el TPM compara lo que mide del arranque con lo que guardó. 2: si coincide, entrega la llave y Windows arranca sin pedir nada. "
      "3: si el BIOS cambió, la medición no coincide y aparece la pantalla de recuperación que pide la clave de 48 dígitos. "
      "4: con BitLocker suspendido por un reinicio, el arranque pasa sin pedir clave y después vuelve a proteger.", pcts=(12, 37, 62, 90))
