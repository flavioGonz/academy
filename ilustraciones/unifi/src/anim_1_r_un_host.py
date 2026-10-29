#!/usr/bin/env python3
"""Lección 1 · Resumen, "Cómo se ve en la red": la regla del host único en dos sitios de obra.
Sitio A con UXG: gateway, switch y AP le informan al UniFi OS Server central. Sitio B con UCG: el UCG es su propio
controlador. Adoptar el UCG en el server central no se puede. Site Manager muestra las dos consolas sin guardar
configuración. Fuente: idea_md y theory_md de la lección (regla del host único, Site Manager)."""
from _anim_red_unifi import *  # noqa

a = new(24, "Quién manda", "Un equipo, un solo host: dos sitios, dos maneras", [
    "Sitio A con UXG: gateway, switch y AP le informan al UniFi OS Server central.",
    "Sitio B con UCG: el UCG es el controlador; switch y AP le informan a él.",
    "Adoptar el UCG en el server central no se puede: ya es su propio host.",
    "Site Manager muestra las dos consolas; la configuración sigue en cada una.",
], still=3)

# arriba: server central y Site Manager
a.add(dev(a, 48, 180, 440, 86, "UniFi OS Server", "10.10.10.5 · oficina IES", icon="server", dark=True))
a.add(dev(a, 712, 180, 440, 86, "Site Manager", "unifi.ui.com · no guarda config", icon="cloud"))

# sitios
for fx, name in ((48, "Sitio A · gateway UXG"), (622, "Sitio B · gateway UCG")):
    a.add(a.box(fx, 304, 530, 296, "#EEF4FA", a.LINE, rx=18, sw=2, extra='stroke-dasharray="8 6"'))
    a.add(a.text(fx + 20, 584, name, 17, a.INK, a.SANS, 600))

A_DEV = [(68, "UXG", "gateway"), (233, "Switch", "USW"), (398, "AP", "U7")]
for x, t, s in A_DEV:
    a.add(dev(a, x, 332, 150, 78, t, s, icon="server" if t != "AP" else None, ap=(t == "AP")))
B_DEV = [(807, "Switch", "USW"), (972, "AP", "U7")]
a.add(dev(a, 642, 332, 150, 78, "UCG", "Network", icon="server", dark=True))
for x, t, s in B_DEV:
    a.add(dev(a, x, 332, 150, 78, t, s, icon="server" if t != "AP" else None, ap=(t == "AP")))

# caminos de inform del sitio A (hacia arriba, al server)
A_PATHS = [[(143, 332), (143, 300), (150, 266)], [(308, 332), (308, 300), (268, 266)], [(473, 332), (473, 300), (386, 266)]]
for p in A_PATHS:
    a.add(poly(p, a.CYAN, 2.5, "6 6"))
# caminos de inform del sitio B (por abajo, al UCG)
B_PATHS = [[(882, 410), (882, 452), (735, 452), (735, 410)], [(1047, 410), (1047, 470), (700, 470), (700, 410)]]
for p in B_PATHS:
    a.add(poly(p, a.CYAN, 2.5, "6 6"))

s0, s1 = ph(a, 0)
for k, p in enumerate(A_PATHS):
    go(a, p, s0 + 2 + k * 2.5, s0 + 9 + k * 2.5, "inform", a.CYAN, still=1 if k == 1 else 0, hold=s0 + 12 + k * 2.5)
    go(a, p, s0 + 13 + k * 2.5, s0 + 20 + k * 2.5, "inform", a.CYAN, hold=s0 + 21 + k * 2.5)
vis(a, pill(a, 68, 500, "host: UniFi OS Server 10.10.10.5", "info"), 0, 3)

s0, s1 = ph(a, 1)
for k, p in enumerate(B_PATHS):
    go(a, p, s0 + 2 + k * 3, s0 + 10 + k * 3, "inform", a.CYAN, hold=s0 + 12 + k * 3)
    go(a, p, s0 + 13 + k * 3, s0 + 21 + k * 3, "inform", a.CYAN, hold=s0 + 22 + k * 3)
vis(a, pill(a, 642, 500, "host: el UCG, en el sitio", "info"), 1, 3)

# 3 · intento de adoptar el UCG en el server
s0, s1 = ph(a, 2)
ADOPT = [(488, 236), (600, 236), (717, 326)]
during(a, poly(ADOPT, a.BAD, 2.5, "8 6"), s0 + 1, s1)
go(a, ADOPT, s0 + 2, s0 + 10, "Adopt", a.BAD, hold=s0 + 12)
during(a, xmark(a, 650, 280, 17), s0 + 11, s1)
during(a, pill(a, 674, 268, "ya tiene host", "bad"), s0 + 11, s1)

# 4 · Site Manager conecta con las dos
s0, s1 = ph(a, 3)
SM = [poly([(712, 223), (488, 223)], a.BLUE, 3, "4 7"), poly([(780, 266), (742, 332)], a.BLUE, 3, "4 7")]
vis(a, "".join(SM), 3)
vis(a, pill(a, 600, 190, "conexión directa", "info", anchor="middle"), 3)
vis(a, check(a, 470, 180, 15) + check(a, 776, 340, 15), 3)

status(a, 640, [
    (0, 25, "Cada equipo responde a un solo controlador: en el sitio A, el server central.", a.INK, 0),
    (25, 50, "Un UDM o UCG corre su propio Network: es el host de todo su sitio.", a.INK, 0),
    (50, 75, "Si el plan es un server central, el gateway del sitio tiene que ser UXG o de terceros.", a.BAD, 0),
    (75, 100, "Site Manager es la puerta: entra a cada controlador, el cerebro sigue en el sitio.", a.OK, 1),
])

write(a, 1, "r1", "Un equipo, un solo host",
      "Animación en cuatro tiempos con dos sitios de obra, el UniFi OS Server central de la oficina (10.10.10.5) y Site Manager en unifi.ui.com. "
      "1: en el sitio A, con gateway UXG, el gateway, el switch y el AP mandan su inform al UniFi OS Server central: ese es su único host. "
      "2: en el sitio B, con gateway UCG, el UCG es el controlador; el switch y el AP le informan a él, dentro del sitio. "
      "3: el server central intenta adoptar el UCG y no puede: un UDM o UCG corre su propio Network y no se gestiona desde un server externo; "
      "si el plan es un server central, el gateway tiene que ser UXG o de terceros. "
      "4: Site Manager arma una conexión directa con el UniFi OS Server y con el UCG y muestra las dos consolas, pero no guarda configuración: "
      "la configuración sigue en cada controlador.",
      [12, 37, 62, 90])
