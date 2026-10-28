#!/usr/bin/env python3
"""Lección 17 · Elegir el canal · Resumen ("Cómo se ve en la red").
Dónde llega cada versión nueva: cada equipo consulta solo la lista de su canal; el banco ve testing, los del cliente
siguen en long-term, y un script automático instala sin prueba lo que salga en su canal.
"""
from _anim_mk_32_39 import *

a = Anim(T=26, kicker="MIKROTIK · ELEGIR EL CANAL · CÓMO SE VE EN LA RED", title="Cada equipo ve solo la lista de su canal")
a.steps([
    "Sale una versión en testing: la ve solo el banco, con channel=testing. Ahí se prueba.",
    "Sale una en stable: el equipo en stable la ve en latest-version. No se instala sola.",
    "Los equipos del cliente consultan long-term: sin cambios hasta que salga un arreglo.",
    "Si ese equipo tiene el script automático, instala sin que lo pruebes. En clientes, no.",
], still=2, size=17)

# ---- servidor con las cuatro listas
SX, SY, SW = 48, 180, 360
a.add(a.box(SX, SY, SW, 360, a.INK, rx=18))
a.add(a.text(SX + 20, SY + 32, "Servidor de MikroTik", 18, a.WHITE, a.SANS, 600))
a.add(a.text(SX + 20, SY + 56, "una lista por canal", 15, SKY, a.MONO))
CH = {"long-term": 250, "stable": 320, "testing": 390, "development": 460}
for n, y in CH.items():
    a.add(a.box(SX + 18, y, SW - 36, 54, a.NAVY2, rx=10))
    a.add(a.text(SX + 34, y + 33, n, 17, a.WHITE, a.MONO, 600))
a.add(during(a, a.pill(SX + SW - 30, CH["testing"] + 14, "nueva", a.INK, GOLD, 14, 26, "end"), 3, 100, still=1))
a.add(during(a, a.pill(SX + SW - 30, CH["stable"] + 14, "nueva", a.INK, GOLD, 14, 26, "end"), 27, 100, still=1))

# ---- equipos
RX, RW, RH = 760, 392, 78
EQ = [  # nombre, canal, y
    ("Banco IES", "channel=testing", 190, "testing"),
    ("Cliente · router 1", "channel=long-term", 290, "long-term"),
    ("Cliente · router 2", "channel=long-term", 386, "long-term"),
    ("Equipo en stable", "channel=stable", 482, "stable"),
]
for name, ch, y, c in EQ:
    a.add(line(SX + SW, CH[c] + 27, RX, y + RH / 2, a.LINE, 2.5, "5 7"))
for name, ch, y, c in EQ:
    a.add(router(a, RX, y, RW, RH, name, ch))


def query(c, y, t, col_back, label_back):
    a.add(travel(a, dot(a, a.CYAN, 8), [(RX, y + RH / 2), (SX + SW, CH[c] + 27)], t, t + 3, hold=0, fade=0.3))
    a.add(travel(a, pkt(a, label_back, col_back, size=13, h=24), [(SX + SW + 50, CH[c] + 27), (RX - 60, y + RH / 2)], t + 3.2, t + 7, hold=1.5))


def status(y, txt, col, bg, t0, t1, still=0):
    a.add(during(a, a.pill(RX + RW - 16, y + 12, txt, col, bg, 14, 26, "end"), t0, t1, still=still))


# 1. banco
query("testing", 190, 4, a.AMB, "nueva")
status(190, "a prueba", a.AMB, a.AMBBG, 13, 100, still=1)
# 2. stable
query("stable", 482, 28, a.AMB, "nueva")
status(482, "latest: nueva", a.AMB, a.AMBBG, 37, 75, still=1)
# 3. cliente
query("long-term", 290, 52, a.OK, "sin cambios")
query("long-term", 386, 55, a.OK, "sin cambios")
status(290, "sin cambios", a.OK, a.OKBG, 61, 100, still=1)
status(386, "sin cambios", a.OK, a.OKBG, 64, 100, still=1)
# 4. script
a.add(during(a, a.box(RX - 4, 478, RW + 8, RH + 8, "none", ROSE, rx=18, sw=3.5), 76, 100))
status(482, "instala solo", a.BAD, a.BADBG, 76, 86)
status(482, "sin probar", a.BAD, a.BADBG, 86, 100)
a.add(travel(a, pkt(a, ".npk", a.BAD, size=13, h=24), [(SX + SW + 50, CH["stable"] + 27), (RX - 60, 521)], 79, 85, hold=1))

narr(a, 48, 596, [
    (0, 25, "El banco propio es donde una versión nueva se gana el lugar.", a.TXT, 0),
    (25, 50, "Ver latest-version no instala nada: instala Install.", a.TXT, 0),
    (50, 75, "Todos los equipos del mismo cliente, en el mismo canal: long-term.", a.OK, 1),
    (75, 100, "El script de la documentación sirve en el banco, no en un cliente.", a.BAD, 0),
])
a.add(a.text(48, 640, "/system/package/update/set channel=long-term  ·  check-for-updates  ·  print", 16, a.TXT, a.MONO))

write(a, 17, "r1", "Cada equipo ve solo la lista de su canal",
      "Animación en cuatro tiempos con el servidor de MikroTik y sus cuatro listas (long-term, stable, testing y development) y cuatro equipos: el banco de IES con channel=testing, "
      "dos routers de un cliente con channel=long-term y un equipo con channel=stable. "
      "1: sale una versión en testing; solo la ve el banco cuando consulta su lista, y ahí se prueba. "
      "2: sale una versión en stable; el equipo en stable la ve en latest-version, pero no se instala sola. "
      "3: los routers del cliente consultan long-term y no hay cambios hasta que long-term saque un arreglo; todos los equipos del cliente van en el mismo canal. "
      "4: si ese equipo tiene el script automático del scheduler, baja e instala la versión nueva sin que nadie la pruebe: en clientes, mejor no.",
      [6, 20, 40, 62, 82, 95])
