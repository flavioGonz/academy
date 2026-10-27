#!/usr/bin/env python3
"""Lección 38 · Teoría · El switch interno del R49G y la PC que depende de él.
Sale de teoria_md (Cómo funciona): el puerto 1 recibe red y energía, el teléfono reenvía el tráfico de la PC
por el puerto 2; si pierde energía o se reinicia (por ejemplo, una actualización), la PC queda sin red hasta
que vuelva; se resuelve con switch con respaldo de energía y, en puestos críticos, cable propio para la PC."""
from _anim_akuvox_29_42 import new, out, box, travel, when

a = new(24, "TELÉFONOS · R49G", "La PC del guardia navega a través del teléfono")
a.steps([
    "El puerto 1 del R49G recibe la red y la energía del switch.",
    "El R49G toma lo suyo y reenvía el tráfico de la PC por el puerto 2.",
    "El R49G se reinicia (por ejemplo, una actualización): la PC queda sin red.",
    "Vuelve el teléfono y vuelve la red. En puestos críticos: cable propio para la PC.",
], still=1)

RED = "#D2492F"
CY = 300
# cables
a.add(f'<path d="M348 {CY} H500" stroke="{a.BLUE}" stroke-width="5"/>')
a.add(f'<path d="M740 {CY} H920" stroke="{a.BLUE}" stroke-width="5"/>')
dash = a.keyframes([(0, 0), (100, -500)], "stroke-dashoffset")
a.add(a.group(f'<path d="M348 {CY - 12} H500" stroke="{RED}" stroke-width="3.5" stroke-dasharray="12 9"/>', a.show(3, 100), dash, still=1))
a.add(a.text(424, CY + 36, "PoE + red", 15, a.GREY, a.MONO, 600, "middle"))
a.add(a.text(830, CY + 36, "solo red", 15, a.GREY, a.MONO, 600, "middle"))

# switch
a.add(a.box(48, 214, 300, 150, a.INK, rx=18))
a.add(a.text(72, 250, "Switch PoE", 21, a.WHITE, a.HEAD, 600))
a.add(a.text(72, 274, "respaldo de energía", 15, "#9FC3E3", a.MONO))
a.add(a.box(250, 278, 76, 48, a.NAVY2, a.CYAN, rx=8))
# R49G
a.add(a.box(470, 200, 300, 190, a.WHITE, a.LINE, rx=18))
a.add(a.text(494, 236, "R49G", 21, a.INK, a.HEAD, 600))
a.add(a.text(494, 260, "2 puertos Gigabit conmutados", 15, a.GREY, a.MONO))
for x, lbl in ((500, "puerto 1"), (660, "puerto 2")):
    a.add(a.box(x, 278, 80, 48, a.SLATE, a.CYAN, rx=8))
    a.add(a.text(x + 40, 346, lbl, 15, a.INK, a.MONO, 600, "middle"))
a.add(a.arrow(f"M588 {CY} H650", a.GREY, 2.5))
# estado del teléfono
when(a, a.pill(494, 356, "encendido", a.OK, a.OKBG, 15, 26), 4, 50, still=1)
when(a, f'<rect x="470" y="200" width="300" height="190" rx="18" fill="#F7FAFD" opacity=".75"/>'
     + a.pill(620, 230, "reiniciando…", a.AMB, a.AMBBG, 16, 32, "middle"), 51, 75)
when(a, a.pill(494, 356, "encendido", a.OK, a.OKBG, 15, 26), 76, 100)
# PC
a.add(box(920, 258, 232, 84, "PC del guardia", "", "laptop"))
when(a, a.pill(1036, 352, "navega", a.OK, a.OKBG, 15, 28, "middle"), 30, 50, still=1)
when(a, a.pill(1036, 352, "sin red", a.BAD, a.BADBG, 15, 28, "middle"), 52, 76)
when(a, a.pill(1036, 352, "navega", a.OK, a.OKBG, 15, 28, "middle"), 82, 100)

# paquetes de la PC (t2 y t4): ida y vuelta pasando por el teléfono
for base in (27, 79):
    for k in range(3):
        t = base + k * 2.6
        if base == 79 and t > 96:
            continue
        travel(a, (900, CY), (360, CY), t, t + 6, None, bg=a.CYAN, dot=8, hold=0.2)
# t3: el paquete de la PC se queda en el puerto 2
travel(a, (900, CY), (752, CY), 54, 58, None, bg=a.BAD, dot=9, hold=16)
when(a, a.text(830, CY - 18, "no pasa", 15, a.BAD, a.MONO, 600, "middle"), 58, 75)

# t4: alternativa
when(a, f'<path d="M200 364 V450 H1036 V342" fill="none" stroke="{a.OK}" stroke-width="3" stroke-dasharray="9 7"/>'
     + a.pill(520, 436, "puesto crítico: cable propio para la PC", a.OK, a.OKBG, 15, 28), 84, 100)

a.add(a.text(48, 512, "Mientras el R49G esté encendido, la PC navega como si estuviera directo en el switch.", 18, a.INK, a.SANS, 600))
a.add(a.text(48, 542, "Para la central, el R49G es una extensión SIP más: el portero lo llama y, si los dos", 17, a.TXT, a.SANS, 600))
a.add(a.text(48, 568, "acuerdan un códec de video común, el video viaja con la llamada.", 17, a.TXT, a.SANS, 600))

out(a, 38, 1, "La PC del guardia navega a través del teléfono",
    "Animación de un switch PoE conectado al puerto 1 de un teléfono R49G, con la PC del guardia en el puerto 2. "
    "Tiempo 1: el puerto 1 recibe red y energía y el teléfono enciende. "
    "Tiempo 2: el tráfico de la PC entra por el puerto 2, cruza el switch interno del teléfono y sale por el puerto 1; la PC navega. "
    "Tiempo 3: el R49G se reinicia, por ejemplo por una actualización; el tráfico de la PC queda detenido en el puerto 2 y la PC queda sin red. "
    "Tiempo 4: el teléfono vuelve y la PC navega otra vez; para puestos críticos aparece un cable propio del switch a la PC. "
    "Abajo: para la central el R49G es una extensión SIP; el video viaja con la llamada si los dos extremos acuerdan un códec común.",
    [10, 32, 62, 92])
