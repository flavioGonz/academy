#!/usr/bin/env python3
"""Lección 4 · Resumen, "Cómo se ve en la red": muchos clientes en Site Manager. Cada consola sale hacia Site Manager
(TCP 443 y 8883) y está en la cuenta UI de la empresa; los técnicos entran con su rol; Blueprints con Drift Inspector
marcan el sitio que se apartó de la plantilla; una consola en la cuenta personal de un técnico se pierde cuando se va.
Fuentes: idea_md, theory_md y lab.md (pasos 1, 4 y 5) de la lección (Fabrics, MSP Groups, Network 10.6.101)."""
from _anim_red_unifi import *  # noqa

a = new(26, "Muchos sitios", "Muchos clientes, una cuenta: quién ve qué", [
    "Cada consola abre su salida a Site Manager; todas en la cuenta de la empresa.",
    "Los técnicos entran con su rol: el 1 solo ve; el 2 solo entra al sitio B.",
    "Blueprint: la plantilla de la empresa. Drift Inspector marca al que se apartó.",
    "Una consola en la cuenta personal de un técnico se va el día que él se va.",
], still=2)

SMX, SMY = 430, 186
a.add(dev(a, SMX, SMY, 340, 90, "Site Manager", "cuenta UI de la empresa", icon="cloud"))
a.add(dev(a, 48, 186, 290, 90, "Técnico 1", "rol: solo ver", icon="user"))
a.add(dev(a, 862, 186, 290, 90, "Técnico 2", "rol: solo el sitio B", icon="user"))

CONS = [(48, "Cliente A", "UCG"), (430, "Cliente B", "CloudKey"), (812, "Oficina", "UniFi OS Server")]
CY = 444
for x, t, s in CONS:
    a.add(dev(a, x, CY, 340, 96, t, s, icon="server", dark=True))
UP = [[(218, CY), (218, 380), (540, 380), (540, 276)], [(600, CY), (600, 276)], [(982, CY), (982, 380), (660, 380), (660, 276)]]
for p in UP:
    a.add(poly(p, a.CYAN, 2.5, "6 6"))

# 1 · salida de cada consola
s0, s1 = ph(a, 0)
for k, p in enumerate(UP):
    go(a, p, s0 + 2 + k * 3, s0 + 10 + k * 3, "443 · 8883", a.CYAN, hold=s0 + 11 + k * 3)
during(a, pill(a, 600, 296, "salen del sitio, nadie entra", "info", anchor="middle"), s0 + 8, s1)

# 2 · roles
s0, s1 = ph(a, 1)
during(a, poly([(338, 231), (430, 231)], a.BLUE, 3) + poly([(770, 231), (862, 231)], a.BLUE, 3), s0 + 1, s1)
for p, c in ((UP[0], a.GREY), (UP[1], a.GREY), (UP[2], a.GREY)):
    go(a, list(reversed(p)), s0 + 5, s0 + 12, "ver", c, hold=s0 + 13)
go(a, list(reversed(UP[1])), s0 + 14, s0 + 20, "Técnico 2", a.BLUE, hold=s0 + 22)
during(a, pill(a, 193, 556, "Técnico 1: solo ver", "grey", anchor="middle") + pill(a, 600, 556, "Técnico 2: puede cambiar", "info", anchor="middle")
       + pill(a, 1007, 556, "Técnico 2: no entra", "bad", anchor="middle"), s0 + 12, s1)

# 3 · Blueprint y Drift Inspector
s0, s1 = ph(a, 2)
during(a, a.box(430, 300, 340, 74, a.WHITE, a.BLUE, rx=14, sw=2.5) + a.text(450, 330, "Blueprint de la empresa", 17, a.INK, a.SANS, 600)
       + a.text(450, 356, "Drift Inspector · 10.6.101", 15, a.BLUE, a.MONO), s0 + 1, s1, still=1)
during(a, pill(a, 193, 556, "igual a la plantilla", "ok", anchor="middle"), s0 + 6, s1, still=1)
during(a, pill(a, 600, 556, "igual a la plantilla", "ok", anchor="middle"), s0 + 9, s1, still=1)
during(a, pill(a, 982, 556, "se apartó: drift", "amb", anchor="middle"), s0 + 12, s1, still=1)

# 4 · cuenta personal
s0, s1 = ph(a, 3)
during(a, a.box(48, CY, 340, 96, a.WHITE, a.BAD, rx=14, sw=2.5) + glyph(a, "server", 66, CY + 18, a.BAD)
       + a.text(110, CY + 34, "Cliente A", 19, a.BAD, a.SANS, 600) + a.text(110, CY + 58, "cuenta personal", 15, a.BAD, a.MONO)
       + a.text(110, CY + 80, "de un técnico", 15, a.BAD, a.MONO), s0 + 1, s1)
during(a, xmark(a, 218, 400, 17), s0 + 8, s1)
during(a, pill(a, 193, 556, "se fue: no aparece más", "bad", anchor="middle"), s0 + 9, s1)

status(a, 628, [
    (0, 25, "Remote Management activo y salida 443 y 8883, DNS y NTP. Ningún puerto de entrada.", a.INK, 0),
    (25, 50, "Fabrics y MSP Groups ordenan administradores y roles para muchos clientes.", a.INK, 0),
    (50, 75, "La configuración sigue en cada consola; la plantilla dice cuál se apartó.", a.AMB, 1),
    (75, 100, "Las consolas son de la empresa; los técnicos entran con su rol.", a.BAD, 0),
])

write(a, 4, "r1", "Muchos clientes en una cuenta",
      "Animación en cuatro tiempos con Site Manager en la cuenta UI de la empresa, dos técnicos y tres consolas: Cliente A con UCG, Cliente B con CloudKey y la oficina con UniFi OS Server. "
      "1: cada consola abre su salida hacia Site Manager por TCP 443 y 8883; salen del sitio y nadie entra, todas en la cuenta de la empresa. "
      "2: los técnicos entran con su rol: el Técnico 1 solo puede ver las tres; el Técnico 2 puede cambiar el sitio B y no entra a los otros. "
      "3: con un Blueprint de la empresa, Drift Inspector (Network 10.6.101) muestra que A y B están iguales a la plantilla y que la oficina se apartó. "
      "4: si la consola del Cliente A está en la cuenta personal de un técnico, el día que se va deja de aparecer para la empresa. "
      "Fabrics y MSP Groups ordenan administradores y roles para muchos clientes.",
      [12, 40, 64, 90])
