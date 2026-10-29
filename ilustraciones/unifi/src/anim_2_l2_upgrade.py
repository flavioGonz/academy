#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 5: Pending Adoption (Update Required) y upgrade <url> por SSH. El AP baja él mismo la
imagen, la escribe, reinicia (la sesión SSH se corta) y vuelve con la versión nueva; recién ahí Adopt.
Fuentes: lab.md e idea_md de la lección (desfase de firmware según LazyAdmin; HostiFi, equipos que piden actualizar)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Adopción limpia", "upgrade por SSH: el AP baja su propio firmware", [
    "Pending Adoption (Update Required): el firmware es muy viejo para adoptar.",
    "upgrade <url>: el AP descarga la imagen él mismo, por HTTPS.",
    "Escribe la imagen y reinicia: la sesión SSH se corta, es lo esperado.",
    "Vuelve con la versión nueva: info lo confirma y Adopt ya funciona.",
], still=3, paso=5)

NB, APX, DL = 168, 600, 1032
a.add(dev(a, 48, 180, 240, 86, "Notebook", "SSH al AP", icon="laptop"))
a.add(dev(a, 450, 180, 300, 86, "AP", "192.168.88.20", ap=True))
a.add(dev(a, 892, 180, 260, 86, "Descargas", "firmware del modelo", icon="globe"))
lifeline(a, NB, 266, 600)
lifeline(a, APX, 266, 600)
lifeline(a, DL, 266, 600)

vis(a, pill(a, APX, 284, "Pending (Update Required)", "amb", anchor="middle"), 0, 1)
vis(a, pill(a, APX, 284, "reiniciando", "bad", anchor="middle"), 2)
vis(a, pill(a, APX, 284, "versión nueva", "ok", anchor="middle"), 3)

s0, s1 = ph(a, 0)
during(a, nbox(a, 48, 330, 500, 108, "Desfase de firmware", ["La falla más común: el equipo es más viejo", "que lo que el controlador acepta adoptar."], "amb"),
       s0 + 2, s1)

s0, s1 = ph(a, 1)
msg(a, NB, APX, 346, "upgrade <url-del-firmware>", s0 + 2, end=100, still=1)
msg(a, APX, DL, 400, "GET · HTTPS", s0 + 8, end=100, still=1, sub="necesita DNS y salida")
msg(a, DL, APX, 470, "imagen del modelo", s0 + 15, end=100, still=1, color=a.OK)

s0, s1 = ph(a, 2)
during(a, a.box(APX + 16, 500, 200, 40, a.AMBBG, None, rx=10) + a.text(APX + 116, 526, "escribe · reinicia", 15, a.AMB, a.MONO, 600, "middle"),
       s0 + 2, 100, still=1)
during(a, a.arrow(f"M{APX - 12} 540 H{NB + 4}", a.BAD, 3, "8 6") + a.text((NB + APX) / 2, 532, "SSH cerrada", 15, a.BAD, a.MONO, 600, "middle"),
       s0 + 6, s1)

s0, s1 = ph(a, 3)
msg(a, NB, APX, 578, "ssh + info", s0 + 2, end=100, still=1)
during(a, term(a, 892, 494, 260, ["Version: nueva", "Status: Not Adopted"], colors={0: MINT}), s0 + 8, 100, still=1)
during(a, pill(a, 892, 576, "Adopt en el controlador", "ok"), s0 + 12, 100, still=1)

status(a, 640, [
    (0, 25, "Si no actualiza solo, lo actualizás vos por SSH.", a.INK, 0),
    (25, 50, "La URL es la del firmware de tu modelo, de la página de descargas.", a.INK, 0),
    (50, 75, "No lo desenchufes mientras escribe la imagen.", a.BAD, 0),
    (75, 100, "Con el firmware al día, la adopción sale a la primera.", a.OK, 1),
])

write(a, 2, "l2", "upgrade por SSH antes de adoptar",
      "Animación en cuatro tiempos del paso 5 con la notebook, el AP en 192.168.88.20 y la página de descargas del firmware. "
      "1: el AP figura Pending Adoption (Update Required): el desfase de firmware, la falla más común, deja al equipo más viejo de lo que el controlador acepta. "
      "2: por SSH se escribe upgrade con la URL del firmware del modelo; el AP descarga la imagen él mismo por HTTPS, así que necesita DNS y salida a internet. "
      "3: escribe la imagen y reinicia; la sesión SSH se corta, es lo esperado, y no hay que desenchufarlo. "
      "4: al volver, ssh e info muestran la versión nueva con Status Not Adopted, y Adopt ya funciona.",
      [12, 37, 62, 92])
