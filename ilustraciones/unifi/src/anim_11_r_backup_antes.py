#!/usr/bin/env python3
"""Lección 11 · Resumen, "Cómo se ve en la red": el backup que viaja antes de actualizar. El .unf sale a la notebook o
un NAS y a una segunda copia fuera del sitio; el autobackup queda en el equipo; se actualiza el piloto y algo falla;
se vuelve con revert (Network 10.5 y posteriores) o restaurando el backup de antes, que es de la versión vieja: un
backup no se carga en un controlador más viejo que el que lo generó. Fuentes: idea_md, theory_md y lab.md de la lección."""
from _anim_red_unifi import *  # noqa

a = new(26, "Backup y etapas", "El backup viaja antes de actualizar, no después", [
    "Antes de actualizar: el backup .unf viaja a la notebook o a un NAS.",
    "Segunda copia fuera del sitio; el autobackup se queda en el equipo.",
    "Actualizás el sitio piloto a la versión nueva y algo falla.",
    "Volvés con revert, o restaurás el backup de antes, que es de la versión vieja.",
], still=3)

CX, CY = 48, 190
a.add(a.box(CX, CY, 340, 130, a.INK, None, rx=14) + glyph(a, "server", CX + 18, CY + 18, a.CYAN)
      + a.text(CX + 62, CY + 34, "Consola del piloto", 19, a.WHITE, a.SANS, 600))
vis(a, a.text(CX + 62, CY + 62, "Network: versión X", 15, SKY, a.MONO), 0, 1)
vis(a, a.text(CX + 62, CY + 62, "Network: versión Y", 15, GOLD, a.MONO, 600), 2)
vis(a, a.text(CX + 62, CY + 62, "Network: versión X", 15, MINT, a.MONO, 600), 3)
vis(a, pill(a, CX + 62, CY + 82, "autobackup: en el equipo", "dark"), 1, 3)

a.add(dev(a, 520, 190, 280, 96, "Notebook o NAS", "copia 1", icon="laptop"))
a.add(dev(a, 872, 190, 280, 96, "Fuera del sitio", "copia 2", icon="cloud"))
a.add(wire(388, 238, 520, 238, a.LINE, 3, "6 6"))
a.add(wire(800, 238, 872, 238, a.LINE, 3, "6 6"))

FILE = lambda c: chip(a, "backup.unf · X", a.WHITE, c, 15, 30)  # noqa: E731
# 1 · a la notebook
s0, s1 = ph(a, 0)
go(a, [(388, 238), (660, 238)], s0 + 3, s0 + 11, inner=FILE(a.BLUE), hold=s0 + 12)
during(a, a.box(48, 360, 520, 150, a.WHITE, a.LINE, rx=14) + a.text(68, 392, "Qué lleva el backup", 17, a.INK, a.SANS, 600)
       + check(a, 80, 422, 10) + a.text(98, 428, "configuración, dispositivos y clientes", 15, a.INK, a.SANS)
       + check(a, 80, 452, 10) + a.text(98, 458, "redes, WiFi, reglas y nombres", 15, a.INK, a.SANS)
       + xmark(a, 80, 482, 10) + a.text(98, 488, "ni video de Protect ni logs locales", 15, a.BAD, a.SANS, 600), s0 + 6, ph(a, 1)[1])
during(a, pill(a, 660, 296, "backup.unf · X", "info", anchor="middle"), s0 + 11.5, 100, still=1)

# 2 · fuera del sitio
s0, s1 = ph(a, 1)
go(a, [(800, 238), (1012, 238)], s0 + 3, s0 + 10, inner=FILE(a.BLUE), hold=s0 + 10.5)
during(a, pill(a, 1012, 296, "backup.unf · X", "info", anchor="middle"), s0 + 10.5, 100, still=1)
during(a, nbox(a, 600, 360, 552, 100, "Dos copias recientes fuera del equipo", ["Si la consola muere, el autobackup se va con ella."], "info"),
       s0 + 5, s1)

# línea de versiones (3 y 4)
LX, LY = 600, 400
s0, s1 = ph(a, 2)
during(a, a.box(LX, LY - 40, 552, 150, a.WHITE, a.LINE, rx=14) + a.text(LX + 20, LY - 8, "Versión del piloto", 17, a.INK, a.SANS, 600)
       + a.box(LX + 20, LY + 20, 140, 50, a.OKBG, a.OK, rx=10, sw=2) + a.text(LX + 90, LY + 52, "X", 18, a.OK, a.MONO, 600, "middle")
       + a.arrow(f"M{LX + 166} {LY + 45} H{LX + 230}", a.GREY, 2.5)
       + a.box(LX + 238, LY + 20, 140, 50, a.BADBG, a.BAD, rx=10, sw=2) + a.text(LX + 308, LY + 52, "Y", 18, a.BAD, a.MONO, 600, "middle"),
       s0 + 1, 100, still=1)
during(a, a.text(LX + 400, LY + 52, "falla", 16, a.BAD, a.SANS, 600), s0 + 8, s1)
during(a, glyph(a, "warn", CX + 296, CY + 16, a.AMB), s0 + 8, s1)
during(a, nbox(a, 48, 360, 520, 150, "Por eso, antes, las notas", ["Network 11.0 pide UniFi OS 6.0, borra el", "historial de estadísticas, quita USG y pasa", "todo a zonas. Un salto así no se prueba en todos."], "amb"),
       s0 + 3, s1)

s0, s1 = ph(a, 3)
during(a, a.path_back if False else a.arrow(f"M{LX + 308} {LY + 76} C{LX + 308} {LY + 104} {LX + 90} {LY + 104} {LX + 90} {LY + 78}", a.OK, 2.5)
       + a.text(LX + 400, LY + 52, "vuelta a X", 16, a.OK, a.SANS, 600), s0 + 2, 100, still=1)
go(a, [(660, 262), (388, 262)], s0 + 6, s0 + 13, inner=FILE(a.OK), hold=s1 - 0.5)
during(a, nbox(a, 48, 360, 520, 150, "Por qué el backup de antes", ["Un backup no se carga en un controlador más", "viejo que el que lo generó: el de antes es de X.", "Network 10.5 y posteriores también revierten."], "ok"),
       s0 + 4, 100, still=1)

status(a, 628, [
    (0, 25, "Antes de actualizar, backup. Siempre.", a.INK, 0),
    (25, 50, "Dos copias recientes fuera del equipo, con fecha en la planilla.", a.INK, 0),
    (50, 75, "Por eso se actualiza un piloto primero, con alguien atento.", a.AMB, 0),
    (75, 100, "Un backup hecho después de actualizar ya no vuelve a la versión vieja.", a.OK, 1),
])

write(a, 11, "r1", "El backup viaja antes de actualizar",
      "Animación en cuatro tiempos con la consola del sitio piloto en la versión X de Network, una copia en la notebook o un NAS y otra fuera del sitio. "
      "1: antes de actualizar se baja el backup .unf de la versión X a la notebook o al NAS; lleva configuración, dispositivos y clientes, redes, WiFi, reglas y nombres, "
      "pero no el video de Protect ni los logs locales. "
      "2: una segunda copia va fuera del sitio; el autobackup queda dentro del equipo y, si la consola muere, se va con ella. "
      "3: se actualiza el piloto a la versión Y y algo falla; por eso antes se leen las notas: Network 11.0 pide UniFi OS 6.0, borra el historial de estadísticas, quita USG y pasa todo a zonas. "
      "4: se vuelve a X con el revert de Network 10.5 y posteriores, o restaurando el backup de antes, que es de X: "
      "un backup no se carga en un controlador más viejo que el que lo generó, así que uno hecho después de actualizar ya no sirve para volver.",
      [12, 40, 64, 92])
