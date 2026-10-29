#!/usr/bin/env python3
"""Lección 2 · Resumen, "Cómo se ve en la red": un AP que viene de otra obra. Sigue buscando a su host viejo; se borra
allá, reset de fábrica (vuelve a http://unifi:8080/inform y ubnt/ubnt), aparece pendiente con Update Required y se
adopta con Adopt and Upgrade. Fuentes: idea_md, theory_md y lab.md de la lección (LazyAdmin, HostiFi)."""
from _anim_red_unifi import *  # noqa

a = new(26, "Adopción limpia", "Un AP de otra obra: borrar, resetear, adoptar", [
    "El AP viene de otra obra: sigue mandando inform a su controlador viejo.",
    "El controlador nuevo no puede adoptarlo: el AP todavía tiene otro host.",
    "Se borra en el viejo y reset de fábrica: vuelve a unifi:8080 y se anuncia.",
    "Firmware viejo: Adopt and Upgrade. Actualiza, reinicia y queda conectado.",
], still=3)

AX, AY, AW, AH = 48, 186, 380, 150
a.add(a.box(AX, AY, AW, AH, a.WHITE, a.LINE, rx=14))
a.add(ap_icon(a, AX + 40, AY + 40, 20))
a.add(a.text(AX + 76, AY + 47, "AP usado", 20, a.INK, a.HEAD, 600))
a.add(a.text(AX + 22, AY + 84, "inform:", 15, a.GREY, a.MONO))
vis(a, a.text(AX + 22, AY + 108, "http://ctrl-viejo:8080/inform", 15, a.BAD, a.MONO, 600), 0, 1)
vis(a, a.text(AX + 22, AY + 108, "http://unifi:8080/inform", 15, a.INK, a.MONO, 600), 2)
vis(a, a.text(AX + 22, AY + 108, "controlador nuevo", 15, a.OK, a.MONO, 600), 3)
vis(a, a.text(AX + 22, AY + 134, "SSH: claves de la otra obra", 15, a.TXT, a.MONO), 0, 1)
vis(a, a.text(AX + 22, AY + 134, "SSH: ubnt / ubnt (de fábrica)", 15, a.TXT, a.MONO), 2)
vis(a, a.text(AX + 22, AY + 134, "SSH: claves de este sitio", 15, a.TXT, a.MONO), 3)

OX, OY = 792, 180
a.add(a.box(OX, OY, 360, 96, a.SLATE, a.LINE, rx=14, extra='stroke-dasharray="7 6"'))
a.add(a.text(OX + 22, OY + 40, "Controlador viejo", 19, a.GREY, a.SANS, 600))
a.add(a.text(OX + 22, OY + 66, "otra obra · otra red", 15, a.GREY, a.MONO))
vis(a, pill(a, OX + 340, OY + 54, "Forget", "amb", anchor="end"), 2)

NX, NY = 792, 312
a.add(dev(a, NX, NY, 360, 120, "Controlador nuevo", "este sitio · UniFi Network", icon="server", dark=True))
vis(a, pill(a, NX + 62, NY + 76, "no se puede adoptar", "bad"), 1)
vis(a, pill(a, NX + 62, NY + 76, "Pending (Update Required)", "amb"), 2)
vis(a, pill(a, NX + 62, NY + 76, "Connected", "ok"), 3)

OLD = [(428, 226), (792, 226)]
NEW_UP = [(428, 300), (600, 300), (600, 372), (792, 372)]
a.add(poly(OLD, a.LINE, 2.5, "6 6"))
a.add(poly(NEW_UP, a.LINE, 2.5, "6 6"))

# 1 · inform al viejo, que no llega
s0, s1 = ph(a, 0)
for k in range(3):
    go(a, [(436, 226), (640, 226)], s0 + 2 + k * 7, s0 + 7 + k * 7, "inform", a.CYAN, hold=s0 + 7.5 + k * 7, still=1 if k == 1 and False else 0)
during(a, xmark(a, 660, 226, 16), s0 + 6, s1 + 0.1)
during(a, a.text(660, 266, "no llega", 15, a.BAD, a.MONO, 600, "middle"), s0 + 6, s1)

# 2 · el nuevo no lo adopta
s0, s1 = ph(a, 1)
go(a, [(436, 226), (640, 226)], s0 + 2, s0 + 7, "inform", a.CYAN, hold=s0 + 7.5)
during(a, xmark(a, 660, 226, 16), s0 + 6, s1)
during(a, nbox(a, 48, 456, 640, 108, "Todavía tiene dueño", [
    "Un equipo responde a un solo host. Mientras siga adoptado",
    "en el controlador viejo, lo sigue buscando a él.",
], "amb"), s0 + 3, s1)

# 3 · Forget + reset + anuncio
s0, s1 = ph(a, 2)
during(a, nbox(a, 48, 456, 640, 108, "Borrar allá y resetear", [
    "Forget en el controlador viejo y reset de 10 segundos",
    "(o set-default por SSH): vuelve a la URL de fábrica.",
], "info"), s0 + 2, s1)
for k in range(3):
    go(a, NEW_UP, s0 + 9 + k * 5, s0 + 14 + k * 5, "aviso UDP 10001", a.GREY, hold=s0 + 14.4 + k * 5)

# 4 · Adopt and Upgrade
s0, s1 = ph(a, 3)
go(a, list(reversed(NEW_UP)), s0 + 1, s0 + 5, "Adopt and Upgrade", a.BLUE, hold=s0 + 5.5)
STG = [("baja firmware", a.BLUE), ("lo escribe", a.BLUE), ("reinicia", a.AMB), ("inform :8080", a.OK)]
for i, (t, c) in enumerate(STG):
    x = 48 + i * 162
    during(a, a.box(x, 470, 150, 56, a.WHITE, c, rx=12, sw=2.5) + a.text(x + 75, 504, t, 15, c, a.MONO, 600, "middle"),
           s0 + 5 + i * 3.5, 100, still=1)
    if i:
        during(a, a.arrow(f"M{x - 12} 498 H{x - 2}", a.GREY, 2.5), s0 + 5 + i * 3.5, 100, still=1)
during(a, a.text(48, 556, "Si no actualiza solo: upgrade <url> por SSH, con el firmware del modelo.", 15, a.TXT, a.SANS, 600),
       s0 + 17, 100, still=1)
go(a, NEW_UP, s0 + 18, s0 + 22, "inform", a.CYAN, hold=s1 - 0.5, still=1)

status(a, 640, [
    (0, 25, "Sin borrarlo allá, el AP sigue fiel a su host viejo, aunque no lo encuentre.", a.INK, 0),
    (25, 50, "No aparece para adoptar: un equipo, un solo host.", a.AMB, 0),
    (50, 75, "Reseteado, el AP se anuncia en la red local y el controlador lo ve pendiente.", a.INK, 0),
    (75, 100, "El desfase de firmware es la falla más común: actualizar y recién ahí adoptar.", a.OK, 1),
])

write(a, 2, "r1", "Readoptar un AP que viene de otra obra",
      "Animación en cuatro tiempos con un AP usado, su controlador viejo de otra obra y el controlador nuevo del sitio. "
      "1: el AP sigue mandando su inform a http://ctrl-viejo:8080/inform y no llega. "
      "2: el controlador nuevo no puede adoptarlo porque el AP todavía tiene otro host: un equipo responde a un solo controlador. "
      "3: se hace Forget en el controlador viejo y reset de fábrica de 10 segundos o set-default; el AP vuelve a http://unifi:8080/inform y a ubnt / ubnt, "
      "se anuncia en la red local por UDP 10001 y aparece Pending Adoption (Update Required). "
      "4: con Adopt and Upgrade baja el firmware, lo escribe, reinicia y manda inform por 8080 al controlador nuevo: queda Connected con las claves SSH del sitio. "
      "Si no actualiza solo, upgrade con la URL del firmware del modelo por SSH. El desfase de firmware es la falla más común.",
      [12, 37, 62, 92])
