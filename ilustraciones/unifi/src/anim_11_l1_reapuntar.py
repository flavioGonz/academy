#!/usr/bin/env python3
"""Lección 11 · Laboratorio, paso 5: después de restaurar en un controlador con otra IP, los equipos siguen mandando
inform a la dirección vieja y aparecen Disconnected; por SSH, set-inform a la nueva y vuelven. Las IP son de ejemplo
(viejo 10.10.10.5, nuevo 10.10.10.6). Fuentes: lab.md (pasos 3 a 5) y theory_md de la lección (re-apuntar con option 43,
DNS o set-inform); lección 2 (después de adoptar, el SSH usa las credenciales de Device Authentication del sitio)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Backup y etapas", "Restaurado en otra IP: re-apuntar los equipos", [
    "Restaurado el backup en el nuevo (10.10.10.6), el AP sigue buscando 10.10.10.5.",
    "En el controlador nuevo aparece Disconnected: tiene la config, no la dirección.",
    "Por SSH, con las credenciales del sitio: set-inform a la dirección nueva.",
    "El inform llega al nuevo y el AP vuelve a Connected.",
], still=3, paso=5)

NB, APX, OLD, NEW = 150, 450, 760, 1050
a.add(dev(a, 48, 180, 210, 86, "Notebook", "SSH", icon="laptop"))
a.add(dev(a, 330, 180, 240, 86, "AP", "adoptado", ap=True))
a.add(a.box(640, 180, 240, 86, a.SLATE, a.LINE, rx=14, extra='stroke-dasharray="7 6"') + glyph(a, "server", 658, 198, a.GREY)
      + a.text(702, 214, "Ctrl viejo · apagado", 17, a.GREY, a.SANS, 600) + a.text(702, 240, "10.10.10.5", 15, a.GREY, a.MONO))
a.add(dev(a, 930, 180, 222, 86, "Ctrl nuevo", "10.10.10.6", icon="server", dark=True))
for x in (NB, APX, OLD, NEW):
    lifeline(a, x, 266, 580)
vis(a, pill(a, NEW, 284, "Disconnected", "bad", anchor="middle"), 1, 2)
vis(a, pill(a, NEW, 284, "Connected", "ok", anchor="middle"), 3)

s0, s1 = ph(a, 0)
for k in range(2):
    msg(a, APX, OLD, 330 + k * 44, "inform → 10.10.10.5:8080", s0 + 2 + k * 9, end=ph(a, 1)[1], color=a.AMB, dash="8 6", still=0)
    during(a, xmark(a, OLD - 22, 330 + k * 44, 13), s0 + 5 + k * 9, ph(a, 1)[1])

s0, s1 = ph(a, 1)
during(a, nbox(a, 48, 430, 560, 100, "Tienen la configuración, no la dirección", ["El backup trae dispositivos y config; cada equipo", "sigue con la URL de inform que tenía guardada."], "amb"),
       s0 + 3, s1)

s0, s1 = ph(a, 2)
msg(a, NB, APX, 432, "ssh + set-inform", s0 + 2, end=100, still=1)
during(a, term(a, 520, 410, 632, ["set-inform http://10.10.10.6:8080/inform"], colors={0: GOLD}), s0 + 5, 100, still=1)
during(a, a.text(NB + 10, 470, "usuario y clave del sitio", 15, a.TXT, a.SANS), s0 + 4, 100, still=1)

s0, s1 = ph(a, 3)
msg(a, APX, NEW, 510, "inform → 10.10.10.6:8080", s0 + 2, end=100, still=1)
msg(a, NEW, APX, 556, "respuesta: config del sitio", s0 + 9, end=100, still=1, color=a.OK)

status(a, 628, [
    (0, 25, "Restaurar no cambia lo que cada equipo tiene guardado como inform.", a.INK, 0),
    (25, 50, "Si cambió la IP del controlador, el problema no es el backup.", a.AMB, 0),
    (50, 75, "Con option 43 o DNS se cambia una vez en el sitio, no equipo por equipo.", a.INK, 0),
    (75, 100, "Después de restaurar se revisa: 10.6.101 corrigió un caso que perdía MC-LAG.", a.OK, 1),
])

write(a, 11, "l1", "Re-apuntar los equipos después de restaurar",
      "Animación en cuatro tiempos del paso 5 con la notebook, un AP adoptado, el controlador viejo apagado en 10.10.10.5 y el controlador nuevo en 10.10.10.6, direcciones de ejemplo. "
      "1: restaurado el backup en el controlador nuevo, el AP sigue mandando inform a 10.10.10.5:8080 y no le contesta nadie. "
      "2: en el controlador nuevo el AP figura Disconnected: el backup trajo dispositivos y configuración, pero cada equipo sigue con la URL de inform que tenía guardada. "
      "3: desde la notebook, por SSH con el usuario y la clave del sitio, se ejecuta set-inform http://10.10.10.6:8080/inform. "
      "4: el inform llega al controlador nuevo, vuelve la configuración del sitio y el AP queda Connected. "
      "Con option 43 o DNS el cambio se hace una vez en el sitio, no equipo por equipo.",
      [12, 40, 64, 92])
