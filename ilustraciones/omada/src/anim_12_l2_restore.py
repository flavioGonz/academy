#!/usr/bin/env python3
"""Lección 12 · Laboratorio, paso 4: Restore from Backup File en el asistente del controlador nuevo.
La cuenta creada en el asistente se reemplaza por la del backup; un .cfg de una versión más nueva no entra en una más vieja."""
from _anim_om_red import *

a = nueva(26, "BACKUP PRIMERO", "Restore from Backup File: qué entra y qué no", "l")
F = a.steps([
    "Asistente del controlador nuevo: Create a Local Account, una cuenta de paso.",
    "Siguiente: Restore from Backup File con el .cfg de la misma versión. Entra.",
    "La cuenta de paso se reemplaza por la del backup: sitios, redes y SSID vuelven.",
    "Al revés no: un .cfg de una versión más nueva no entra en un controlador más viejo.",
], still=2)

# ventana del asistente
WX, WY, WW, WH = 48, 186, 560, 384
a.add(a.box(WX, WY, WW, WH, a.WHITE, a.LINE, rx=16))
a.add(a.box(WX, WY, WW, 48, a.SLATE, rx=16) + a.box(WX, WY + 32, WW, 16, a.SLATE, rx=0))
a.add(a.text(WX + 20, WY + 31, "https://<IP-del-controlador-nuevo>:8043", 15, a.INK, a.MONO))
at(a, a.text(WX + 24, WY + 90, "Create a Local Account", 19, a.INK, a.SANS, 600)
   + a.box(WX + 24, WY + 112, 320, 38, a.WHITE, a.LINE, rx=8) + a.text(WX + 38, WY + 137, "usuario: de-paso", 15, a.INK, a.MONO)
   + a.box(WX + 24, WY + 160, 320, 38, a.WHITE, a.LINE, rx=8) + a.text(WX + 38, WY + 185, "clave: ********", 15, a.INK, a.MONO), 0, 25)
at(a, a.text(WX + 24, WY + 90, "Restore from Backup File", 19, a.INK, a.SANS, 600)
   + a.box(WX + 24, WY + 112, WW - 48, 38, a.WHITE, a.BLUE, rx=8) + a.text(WX + 38, WY + 137, "omada-lab_v6.2.10.17_2026-10-27.cfg", 15, a.INK, a.MONO), 25, 75, still=1)
at(a, a.text(WX + 24, WY + 90, "Restore from Backup File", 19, a.INK, a.SANS, 600)
   + a.box(WX + 24, WY + 112, WW - 48, 38, a.WHITE, a.BAD, rx=8) + a.text(WX + 38, WY + 137, "omada-lab_v6.3.0.111_....cfg", 15, a.BAD, a.MONO), 75, 100)
# contenido restaurado
at(a, a.text(WX + 24, WY + 220, "Sitios", 15, a.GREY, a.SANS, 600) + a.text(WX + 160, WY + 220, "Central · Sucursal", 15, a.INK, a.MONO, 600)
   + a.text(WX + 24, WY + 250, "Redes", 15, a.GREY, a.SANS, 600) + a.text(WX + 160, WY + 250, "LAN · CCTV · Invitados", 15, a.INK, a.MONO, 600)
   + a.text(WX + 24, WY + 280, "SSID", 15, a.GREY, a.SANS, 600) + a.text(WX + 160, WY + 280, "Oficina · Huespedes-Lab", 15, a.INK, a.MONO, 600)
   + a.text(WX + 24, WY + 310, "Cuenta", 15, a.GREY, a.SANS, 600) + a.text(WX + 160, WY + 310, "la del backup", 15, a.OK, a.MONO, 600), 56, 75, still=1)
at(a, a.text(WX + 24, WY + 220, "No se puede restaurar:", 17, a.BAD, a.SANS, 600)
   + a.text(WX + 24, WY + 250, "el archivo es de una versión", 16, a.INK, a.SANS)
   + a.text(WX + 24, WY + 276, "más nueva que este controlador.", 16, a.INK, a.SANS), 82, 100)

# versiones a la derecha
VX = 660
a.add(dev(a, VX, 186, 492, 84, "Controlador nuevo", "v6.2.10.17", icon="server", dark=True))
at(a, dev(a, VX, 300, 492, 84, "Backup .cfg", "v6.2.10.17 · la misma", icon="card"), 25, 75, still=1)
at(a, dev(a, VX, 300, 492, 84, "Backup .cfg", "v6.3.0.111 · más nueva", icon="card", stroke=a.BAD), 75, 100)
travel(a, pkt(a, ".cfg", a.OK), [(VX + 246, 300), (VX + 246, 270)], 30, 34, hold=0.5)
at(a, check(a, VX + 470, 342, 14), 34, 75, still=1)
travel(a, pkt(a, ".cfg", a.BAD), [(VX + 246, 300), (VX + 246, 280)], 79, 82, hold=0.3)
at(a, xmark(a, VX + 470, 342, 14), 82, 100)
# cuenta
at(a, chip(a, VX, 404, "cuenta de-paso", a.GREY, a.SLATE), 2, 52)
at(a, chip(a, VX, 404, "cuenta de-paso", a.GREY, a.SLATE) + line(VX + 10, 419, VX + 150, 419, a.BAD, 2.5)
   + chip(a, VX + 180, 404, "cuenta del backup", a.OK, a.OKBG, stroke=a.OK), 52, 75, still=1)
at(a, note(a, VX, 450, 492, 120, "Uno por versión", ["Bajar de versión es reinstalar y restaurar el backup", "de esa misma versión: guardá uno antes de cada", "actualización, con la versión en el nombre."], "amb"), 75, 100)
at(a, note(a, VX, 450, 492, 120, "Después de restaurar", ["Entrá con la cuenta de siempre y verificá sitios,", "redes y SSID. La migración de equipos va por", "Global View > Settings > Migration."], "info"), 0, 75, still=1)

status(a, 618, [
    (0, 25, "La cuenta del asistente es de paso: el restore la pisa.", a.INK, 0),
    (25, 50, "Misma versión del controlador que la del archivo.", a.INK, 0),
    (50, 75, "Si no ves lo que esperabas, el .cfg no era el último: por eso la fecha en el nombre.", a.OK, 1),
    (75, 100, "Para volver atrás hace falta el backup de la versión vieja.", a.BAD, 0),
], x=48, anchor="start", size=16)

write(a, 12, "l2", "Restore from Backup File en el controlador nuevo",
      "Animación en cuatro tiempos con el asistente del controlador nuevo (v6.2.10.17) y el archivo de backup. "
      "1: en el asistente se elige Create a Local Account y se crea una cuenta de paso. "
      "2: en el paso siguiente, Restore from Backup File con omada-lab_v6.2.10.17_2026-10-27.cfg, de la misma versión que el controlador: entra. "
      "3: la cuenta de paso se reemplaza por la del backup y vuelven los sitios, las redes y los SSID; se verifica entrando con la cuenta de siempre. "
      "4: al revés no: un .cfg de una versión más nueva, por ejemplo 6.3.0.111, no se restaura en un controlador 6.2.10.17. "
      "Bajar de versión es reinstalar y restaurar el backup de esa misma versión, por eso se guarda uno por versión con la versión en el nombre.",
      [8, 36, 62, 90])
