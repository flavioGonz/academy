#!/usr/bin/env python3
"""Lección 37 (Dos WAN: PPPoE + DHCP), Resumen: la sesión PPPoE se reconecta a la madrugada y vuelve con otra IP
y otro extremo. La /32 al testigo con gateway=pppoe-antel vuelve sola; una con la IP vieja del concentrador queda colgada."""
from _anims_10_19 import Anim, en, ventanas, fijo, dev, viaje, linea, narr, escribir, pill_c, place, marca, LIGHT, GOLD, MINT, CORAL, GHOST

a = Anim(T=24, kicker="MIKROTIK · PPPOE + DHCP · EN LA RED", title="La sesión vuelve con otra IP: la interfaz no cambia")
a.steps([
    "Sesión arriba: el otro extremo es 198.51.100.1.",
    "A la madrugada la sesión se cae: el local sale por el 4G.",
    "Vuelve con otra IP y otro extremo: 198.51.100.9.",
    "La ruta por pppoe-antel volvió sola; la de la IP vieja, no.",
], still=2)

# ---- arriba: el enlace
a.add(dev(a, 48, 178, 236, 92, "Router", "pppoe-antel", None, dark=True, sub2="ether1"))
a.add(dev(a, 404, 186, 206, 76, "ONT Antel", "modo puente", "server"))
a.add(dev(a, 730, 178, 422, 92, "Concentrador PPPoE", "el otro extremo de la sesión", "globe"))
a.add(linea(284, 224, 404, 224, a.LINE, 4))
a.add(linea(610, 224, 730, 224, a.LINE, 4))
# la sesión (línea lógica por debajo)
SY = 300
ventanas(a, linea(166, SY, 940, SY, a.CYAN, 4, "10 8") + a.text(553, SY + 26, "sesión PPPoE arriba", 15, a.CYAN, a.MONO, 600, "middle"), [(0, 26), (58, 100)], still=1)
en(a, linea(166, SY, 940, SY, a.BAD, 4, "4 10") + a.text(553, SY + 26, "sesión caída: pppoe-antel baja", 15, a.BAD, a.MONO, 600, "middle"), 26, 50)
en(a, linea(166, SY, 940, SY, a.AMB, 4, "4 10") + a.text(553, SY + 26, "se negocia otra vez", 15, a.AMB, a.MONO, 600, "middle"), 50, 58)
a.add(linea(166, 270, 166, SY, a.LINE, 3) + linea(940, 270, 940, SY, a.LINE, 3))
viaje(a, "IPCP: tu IP 203.0.113.80", [(820, 352), (330, 352)], 51, 56, bg=a.BLUE, size=14, hold=1)
viaje(a, "IPCP: yo soy 198.51.100.9", [(820, 352), (330, 352)], 54, 58, bg=a.NAVY2, size=14, hold=1)

# ---- medio: lo que ve el router
PX, PY, PW, PH = 48, 380, 560, 110
a.add(a.box(PX, PY, PW, PH, a.INK, rx=16))
a.add(a.text(PX + 22, PY + 32, "/ip/address · pppoe-antel", 15, LIGHT, a.MONO))
a.add(a.text(PX + 22, PY + 64, "address", 15, LIGHT, a.MONO))
a.add(a.text(PX + 22, PY + 92, "network", 15, LIGHT, a.MONO))
en(a, a.text(PX + 130, PY + 64, "203.0.113.45", 17, "#FFFFFF", a.MONO, 600) + a.text(PX + 130, PY + 92, "198.51.100.1", 17, "#FFFFFF", a.MONO, 600), 0, 26)
en(a, a.text(PX + 130, PY + 64, "(sin dirección)", 17, CORAL, a.MONO, 600), 26, 58)
en(a, a.text(PX + 130, PY + 64, "203.0.113.80", 17, GOLD, a.MONO, 600) + a.text(PX + 130, PY + 92, "198.51.100.9", 17, GOLD, a.MONO, 600), 58, 100, still=1)
fijo(a, a.text(PX + 340, PY + 92, "antes: 198.51.100.1", 15, LIGHT, a.MONO))
en(a, a.text(PX + 340, PY + 92, "antes: 198.51.100.1", 15, LIGHT, a.MONO), 58, 100)

QX, QW = 636, 516
a.add(a.box(QX, PY, QW, PH, a.WHITE, a.LINE, rx=16))
a.add(a.text(QX + 22, PY + 32, "con gateway=pppoe-antel, el local sale por", 15, a.GREY, a.MONO))
for t0, t1, s, c, st in ((0, 26, "la fibra (recursivas por pppoe-antel)", a.OK, 0), (26, 60, "el 4G (DHCP, distancia 2)", a.AMB, 0),
                         (60, 100, "la fibra otra vez, sin tocar nada", a.OK, 1)):
    en(a, a.text(QX + 22, PY + 72, s, 18, c, a.SANS, 600), t0, t1, still=st)

# ---- abajo: las dos formas de escribir la /32 al testigo
RY = 512
ROWS = [("así", "1.1.1.1/32 gateway=pppoe-antel scope=10", a.OK), ("así no", "1.1.1.1/32 gateway=198.51.100.1 scope=10", a.BAD)]
for i, (tag, r, c) in enumerate(ROWS):
    y = RY + i * 54
    a.add(a.box(48, y, 1104, 46, a.SLATE, rx=10))
    a.add(a.text(66, y + 30, tag, 16, c, a.SANS, 700))
    a.add(a.text(150, y + 30, r, 16, a.INK, a.MONO, 600))
END = 1136
ST = {0: [(0, 26, "activa", a.OK, a.OKBG, 0), (26, 60, "inactiva", a.BAD, a.BADBG, 0), (60, 100, "activa", a.OK, a.OKBG, 1)],
      1: [(0, 26, "activa", a.OK, a.OKBG, 0), (26, 100, "inactiva", a.BAD, a.BADBG, 1)]}
for i, lst in ST.items():
    for t0, t1, s, fg, bg, st in lst:
        en(a, a.pill(END, RY + i * 54 + 9, s, fg, bg, 14, 28, "end"), t0, t1, still=st)
en(a, a.text(END - 120, RY + 54 + 30, "ese extremo ya no existe", 15, a.BAD, a.MONO, 600, "end"), 60, 100, still=1)
en(a, a.box(48, RY, 1104, 46, "none", a.OK, rx=10, sw=2.5) + a.box(48, RY + 54, 1104, 46, "none", a.BAD, rx=10, sw=2.5), 75, 100)

narr(a, [
    (0, 25, "Las rutas a los testigos 1.1.1.1 y 9.9.9.9 apuntan a la interfaz, no a una IP.", a.TXT),
    (25, 50, "La interfaz baja, las /32 quedan inactivas y entra la ruta del 4G en distancia 2.", a.AMB),
    (50, 75, "IPCP entrega otra dirección y otro extremo; el nombre pppoe-antel sigue igual.", a.TXT),
    (75, 100, "En RouterOS 7 el nombre de la interfaz alcanza como gateway; la IP habría que corregirla a mano.", a.OK),
], still_idx=2)

escribir(a, "37-r1", "La sesión PPPoE vuelve con otra IP",
         "Animación en cuatro tiempos. Arriba, el router con pppoe-antel por ether1, el ONT de Antel en modo puente y el concentrador PPPoE, "
         "con la sesión dibujada como una línea entre el router y el concentrador. En el medio, la dirección de pppoe-antel y por dónde sale el local. "
         "Abajo, dos formas de escribir la ruta al testigo: así, 1.1.1.1/32 con gateway=pppoe-antel; así no, 1.1.1.1/32 con gateway=198.51.100.1. "
         "1: la sesión está arriba con address 203.0.113.45 y network 198.51.100.1; las dos rutas están activas y el local sale por la fibra. "
         "2: a la madrugada la sesión se cae, la interfaz baja, las dos rutas quedan inactivas y el local sale por el 4G con su ruta en distancia 2. "
         "3: la sesión se negocia otra vez e IPCP entrega otra dirección, 203.0.113.80, y otro extremo, 198.51.100.9; la ruta por pppoe-antel vuelve a activa y el local sale de nuevo por la fibra. "
         "4: la ruta escrita con la IP vieja queda inactiva porque ese extremo ya no existe; en RouterOS 7 el nombre de la interfaz alcanza como gateway.",
         [10, 35, 53, 56, 66, 90])
