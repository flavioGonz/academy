#!/usr/bin/env python3
"""Lección 12 · Resumen, "Cómo se ve en la red": el backup programado guardado fuera del controlador salva la obra.
Backup Schedule manda el .cfg al SFTP; muere el disco del controlador; uno nuevo de la misma versión restaura el .cfg
y los equipos vuelven a Connected."""
from _anim_om_red import *

a = nueva(28, "BACKUP PRIMERO", "Se murió el disco del controlador: el .cfg estaba afuera")
F = a.steps([
    "Domingo 3:00: Backup Schedule manda el .cfg de la configuración al SFTP de IES.",
    "Martes: muere el disco del mini PC. Los equipos siguen con lo último, sin gestión.",
    "Controlador nuevo, misma versión y misma IP: Restore from Backup File con el .cfg.",
    "Los equipos vuelven a Connected: sitios, redes y SSID como estaban.",
], still=3)

CY = 190
# controlador viejo / nuevo
at(a, dev(a, 48, CY, 340, 100, "Controlador", "mini PC del cliente", icon="server", dark=True, sub2="v6.2.10.17"), 0, 28, still=0)
at(a, a.box(48, CY, 340, 100, a.BADBG, a.BAD, rx=14, sw=2) + glyph(a, "x", 66, CY + 18, a.BAD)
   + a.text(110, CY + 34, "Disco muerto", 19, a.BAD, a.SANS, 600) + a.text(110, CY + 58, "con él, todo lo local", 15, a.BAD, a.MONO), 28, 52)
at(a, dev(a, 48, CY, 340, 100, "Controlador nuevo", "misma versión, misma IP", icon="server", dark=True, sub2="v6.2.10.17"), 52, 100, still=1)
# SFTP
a.add(dev(a, 460, CY, 320, 100, "SFTP de IES", "otro equipo, otro lugar", icon="server"))
at(a, chip(a, 620, CY + 112, "omada-cliente_v6.2.10.17_domingo.cfg", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 12, 100, still=1)
# equipos
a.add(a.box(48, 380, 732, 162, a.WHITE, a.LINE, rx=16))
a.add(a.text(68, 410, "Equipos del sitio", 16, a.GREY, a.SANS, 600))
DEV = [(160, "EAP 1"), (330, "EAP 2"), (520, "Switch"), (690, "ER")]
for x, t in DEV:
    a.add(eap(a, x, 450, 22) if t.startswith("EAP") else a.box(x - 34, 432, 68, 36, a.INK, rx=8))
    a.add(a.text(x, 492, t, 15, a.INK, a.MONO, 600, "middle"))
for t0, t1, lab, fg, bg in ((0, 28, "Connected", a.OK, a.OKBG), (28, 82, "sin gestión", a.AMB, a.AMBBG), (82, 100, "Connected", a.OK, a.OKBG)):
    for x, _ in DEV:
        at(a, chip(a, x, 500, lab, fg, bg, anchor="middle"), t0, t1, still=1 if t0 == 82 else 0)

# 1: el backup viaja
travel(a, pkt(a, ".cfg", a.OK), [(388, CY + 50), (460, CY + 50)], 4, 9, hold=1)
# 2: equipos siguen andando
at(a, a.text(414, 568, "la red sigue con la última configuración; nadie puede cambiar nada", 15, a.AMB, a.SANS, 600, "middle"), 30, 52)
# 3: restore
travel(a, pkt(a, ".cfg", a.OK), [(460, CY + 50), (388, CY + 50)], 56, 61, hold=1)
at(a, a.box(48, CY + 112, 340, 46, a.WHITE, a.BLUE, rx=10, sw=1.5) + a.text(66, CY + 141, "Restore from Backup File", 16, a.BLUE, a.MONO, 600), 54, 100, still=1)
# 4: vuelven
for x, _ in DEV:
    travel(a, dot(a, a.OK, 7), [(x, 432), (218, CY + 160)], 77, 81, hold=0.3)

# panel de calendario
PX, PW = 820, 332
a.add(a.box(PX, CY, PW, 340, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 20, CY + 32, "La semana", 16, a.INK, a.SANS, 600))
EV = [(0, "Dom 3:00", "Backup Schedule · semanal", a.OK), (25, "Mar 10:12", "falla el disco", a.BAD),
      (50, "Mar 11:30", "controlador nuevo + restore", a.BLUE), (75, "Mar 11:45", "todo Connected", a.OK)]
for i, (t0, d, t, col) in enumerate(EV):
    y = CY + 72 + i * 64
    at(a, f'<circle cx="{PX + 30}" cy="{y}" r="8" fill="{col}"/>' + a.text(PX + 50, y + 6, d, 15, col, a.MONO, 600)
       + a.text(PX + 50, y + 30, t, 15, a.TXT, a.SANS), t0 + 1, 100, still=1)
at(a, a.text(PX + 20, CY + 326, "horarios de ejemplo", 15, a.GREY, a.SANS), 0, 100, still=1)

status(a, 610, [
    (0, 25, "Save to File Server: el backup queda en otro equipo y sobrevive al host.", a.INK, 0),
    (25, 50, "Un backup guardado en el mismo disco del controlador muere con él.", a.BAD, 0),
    (50, 75, "La cuenta que creás en el asistente se reemplaza por la del backup.", a.INK, 0),
    (75, 100, "Sin el .cfg en el SFTP, esto era rehacer la obra entera.", a.OK, 1),
], x=48, anchor="start", size=16)

write(a, 12, "r1", "El backup fuera del controlador salva la obra",
      "Animación en cuatro tiempos con el controlador del cliente en un mini PC (v6.2.10.17), el SFTP de IES en otro equipo, los equipos del sitio (dos EAP, un switch y un ER) y un calendario de la semana con horarios de ejemplo. "
      "1: el domingo a las 3:00, Backup Schedule manda el archivo .cfg de la configuración al SFTP de IES, con Save to File Server. "
      "2: el martes muere el disco del mini PC y con él todo lo que estaba guardado ahí; los equipos quedan sin controlador y siguen con la última configuración, pero nadie puede cambiar nada. "
      "3: se instala un controlador nuevo de la misma versión y en la misma IP y, en el asistente, Restore from Backup File con el .cfg del domingo; la cuenta creada en el asistente se reemplaza por la del backup. "
      "4: los equipos vuelven a Connected con sitios, redes y SSID como estaban.",
      [8, 36, 62, 90])
