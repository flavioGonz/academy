#!/usr/bin/env python3
"""Lección 28 · teoría: clave web perdida en un portero de un botón: SmartPlus, PC Manager en la LAN o llave del equipo a soporte."""
from _anim_akuvox_15_28 import *

a = new(20, "AKUVOX · LECCIÓN 28", "Clave perdida en un portero de un botón: tres caminos")
a.steps([
    "Sin pantalla y sin la clave web, no hay cómo entrar a configurar el E12 o el E13S.",
    "Caminos 1 y 2: SmartPlus, o PC Manager desde una PC en la misma LAN.",
    "Camino 3: exportás la llave del equipo con la herramienta y la mandás a soporte.",
    "Soporte devuelve un archivo para desbloquear. Por eso la clave se anota el primer día.",
], still=3)

# portero
a.add(I.Intercom(60, 196, "E12 o E13S", "un botón, sin pantalla").svg())
a.add(at(a, mark(135, 300, True) + a.text(135, 350, "desbloqueado", 15, "#5BE0A5", a.MONO, 600, "middle"), 92, 100, still=0))

# web del equipo
W = I.Window(262, 196, 320, 140, "Web del equipo", rows=[("Clave web", "?")], hl=0).svg()
a.add(W)
a.add(at(a, mark(300, 306, False) + a.text(330, 312, "no entra", 15, a.BAD, a.MONO, 600), 3, 100, still=1))
a.add(f'<path d="M210 260 H262" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="6 6"/>')


def num(x, y, n):
    return f'<circle cx="{x}" cy="{y}" r="16" fill="{a.CYAN}"/>' + a.text(x, y + 6, str(n), 16, a.WHITE, a.MONO, 700, "middle")


# caminos 1 y 2
a.add(I.CloudBox(770, 172, "SmartPlus", "nube de Akuvox", w=300).svg())
a.add(I.Laptop(770, 268, "PC Manager", "PC en la misma LAN", w=300).svg())
for y, n in ((214, 1), (310, 2)):
    a.add(f'<path d="M582 260 C680 260 680 {y} 762 {y}" fill="none" stroke="{I.LINE2}" stroke-width="3"/>')
    a.add(num(1100, y, n))
a.add(at(a, f'<path d="M582 260 C680 260 680 214 762 214 M582 260 C680 260 680 310 762 310" fill="none" stroke="{a.CYAN}" stroke-width="4"/>'
         + a.box(766, 168, 308, 92, "none", a.CYAN, rx=18, sw=3) + a.box(766, 264, 308, 92, "none", a.CYAN, rx=18, sw=3), 26, 50, still=0))

# camino 3
TY = 436
a.add(I.Laptop(420, TY - 42, "Herramienta", "en la PC", w=240).svg())
a.add(I.Generic(830, TY - 42, "Soporte de Akuvox", "devuelve un archivo", icon="user", w=262).svg())
a.add(num(1114, TY, 3))
a.add(f'<path d="M210 {TY} H420 M660 {TY} H830" stroke="{I.LINE2}" stroke-width="3"/>')
a.add(packet(a, "llave del equipo", (250, TY - 30), (380, TY - 30), 52, 58, hide=59, size=15))
a.add(packet(a, "llave del equipo", (700, TY - 30), (790, TY - 30), 60, 67, hide=72, size=15))
a.add(packet(a, "archivo de desbloqueo", (790, TY + 30), (700, TY + 30), 77, 83, color=a.OK, hide=84, size=15))
a.add(packet(a, "archivo de desbloqueo", (380, TY + 30), (300, TY + 30), 85, 91, color=a.OK, hide=93, size=15))
a.add(at(a, a.text(740, TY - 58, "a soporte", 15, a.BLUE, a.MONO, 600, "middle"), 58, 75, still=0))
a.add(at(a, a.text(315, TY - 58, "exportar", 15, a.BLUE, a.MONO, 600, "middle"), 51, 75, still=0))
a.add(at(a, a.text(740, TY + 72, "vuelve", 15, a.OK, a.MONO, 600, "middle") + a.text(315, TY + 72, "desbloquear", 15, a.OK, a.MONO, 600, "middle"), 76, 100, still=1))
a.add(at(a, f'<path d="M210 {TY} H420 M660 {TY} H830" stroke="{a.CYAN}" stroke-width="4"/>', 51, 100, still=1))

# nota final
a.add(at(a, a.box(48, 586, 1104, 56, a.OKBG, a.OK, rx=14, sw=1.5)
         + a.text(70, 621, "Recuperar el acceso no es trivial: la clave web se cambia y se documenta en la primera visita.", 17, a.INK, a.SANS, 600), 78, 100, still=1))

a.write(*out(28)[:1], title="Recuperar el acceso a un portero de un botón",
        desc=("Animación en cuatro tiempos. 1: un E12 o E13S, de un botón y sin pantalla, con la clave web perdida: la web del equipo no deja entrar. "
              "2: los caminos 1 y 2 son SmartPlus o PC Manager desde una PC en la misma LAN. "
              "3: el camino 3 es exportar la llave del equipo con la herramienta en la PC y mandarla a soporte de Akuvox. "
              "4: soporte devuelve un archivo para desbloquear, que vuelve al portero y lo desbloquea. Por eso la clave web se cambia y se documenta en la primera visita."),
        preview=[12, 40, 64, 88, 96], prefix=out(28)[1])
