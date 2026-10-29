#!/usr/bin/env python3
"""Lección 40 · Teoría · Nube o local: dónde vive la base de datos.
Sale de teoria_md (Cómo funciona): en la nube los equipos inician la conexión hacia afuera (no se abren
puertos), la app anda desde cualquier lugar, sin internet las funciones de nube se detienen (plan B de la
lección 11); en local el servidor sigue sin internet y a cambio alguien lo mantiene (energía, respaldos y
actualizaciones); un administrador por equipo."""
from _anim_akuvox_29_42 import new, out, box, travel, when

a = new(24, "SOFTWARE Y NUBE", "Nube o local: dónde vive la base de datos")
a.steps([
    "Nube: los equipos inician la conexión hacia afuera. No se abren puertos.",
    "La app del residente anda desde cualquier lugar, a través de la nube.",
    "Se corta internet: las funciones de nube se detienen. El servidor local sigue.",
    "A cambio, el servidor local pide energía, respaldos y actualizaciones.",
], still=2)


def panel(x0, title, color):
    a.add(a.box(x0, 172, 540, 392, a.WHITE, a.LINE, rx=18))
    a.add(a.text(x0 + 24, 204, title, 20, color, a.HEAD, 600))
    a.add(f'<rect x="{x0 + 20}" y="334" width="500" height="214" rx="16" fill="none" stroke="{a.GREY}" stroke-width="2" stroke-dasharray="7 6"/>')
    a.add(a.text(x0 + 36, 358, "EDIFICIO", 15, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))


def cut(x, y, t0, t1=100, still=0):
    when(a, f'<circle cx="{x}" cy="{y}" r="16" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2"/>'
         f'<path d="M{x - 6} {y - 6} l12 12 M{x + 6} {y - 6} l-12 12" stroke="{a.BAD}" stroke-width="3" stroke-linecap="round"/>', t0, t1, still=still)


# ---------- NUBE
L = 48
panel(L, "Nube · SmartPlus", a.BLUE)
# enlaces (antes que las cajas)
a.add(f'<path d="M{L + 270} 476 H{L + 316}" stroke="{a.BLUE}" stroke-width="3"/>')          # equipos - router
a.add(f'<path d="M{L + 420} 412 V316" stroke="{a.BLUE}" stroke-width="3"/>')               # router - nube
a.add(f'<path d="M{L + 252} 262 H{L + 300}" stroke="{a.BLUE}" stroke-width="3" stroke-dasharray="6 5"/>')  # app - nube
a.add(box(L + 300, 226, 220, 84, "Nube", "SmartPlus", "cloud"))
a.add(box(L + 24, 226, 228, 84, "App", "cualquier lugar", "phone"))
a.add(box(L + 316, 412, 200, 74, "Router", "nada entrante", "globe"))
a.add(box(L + 44, 434, 226, 84, "Equipos", "portero, monitor", "bell"))
# t1 saliente
travel(a, (L + 276, 476), (L + 310, 476), 3, 7, None, bg=a.CYAN, dot=8, hold=0.3)
travel(a, (L + 420, 404), (L + 420, 318), 8, 14, "saliente", a.WHITE, a.BLUE, hold=6)
when(a, a.pill(L + 270, 380, "la conexión sale del edificio", a.BLUE, "#E6F1FB", 15, 28, "middle"), 4, 50, still=0)
# t2 app <-> nube <-> equipos
for t in (28, 36, 44):
    travel(a, (L + 258, 262), (L + 296, 262), t, t + 3, None, bg=a.CYAN, dot=8, hold=0.2)
    travel(a, (L + 420, 318), (L + 420, 404), t + 3, t + 6, None, bg=a.CYAN, dot=8, hold=0.2)
when(a, a.pill(L + 520, 184, "app: funciona", a.OK, a.OKBG, 15, 26, "end"), 30, 50)
# t3 corte
cut(L + 420, 364, 51, 100, still=1)
when(a, a.pill(L + 520, 184, "app: se detiene", a.BAD, a.BADBG, 15, 26, "end"), 52, 100, still=1)

# ---------- LOCAL
R = 612
panel(R, "Local · SDMC o ACMS", a.INK)
a.add(f'<path d="M{R + 270} 476 H{R + 320}" stroke="{a.GREY}" stroke-width="3"/>')            # servidor - equipos
a.add(f'<path d="M{R + 410} 412 V316" stroke="{a.GREY}" stroke-width="3"/>')               # router - internet
a.add(box(R + 300, 226, 220, 84, "Internet", "", "globe"))
a.add(box(R + 320, 412, 180, 74, "Router", "", "globe"))
a.add(box(R + 44, 434, 226, 84, "Servidor", "en el edificio", "server", dark=True))
a.add(box(R + 300, 504 - 2, 200, 40, "", "", None))
a.add(a.text(R + 400, 528, "equipos del edificio", 15, a.INK, a.MONO, 600, "middle"))
a.add(f'<path d="M{R + 270} 500 V522 H{R + 300}" fill="none" stroke="{a.OK}" stroke-width="3"/>')
cut(R + 410, 364, 51, 100, still=1)
# tráfico local siempre
for t in (6, 30, 56, 64, 72, 82, 90):
    travel(a, (R + 274, 522), (R + 296, 522), t, t + 3, None, bg=a.OK, dot=7, hold=0.2)
when(a, a.pill(R + 157, 400, "sigue andando", a.OK, a.OKBG, 15, 26, "middle"), 53, 100, still=1)
# t4 mantenimiento
when(a, a.pill(R + 36, 252, "energía", a.AMB, a.AMBBG, 15, 28)
     + a.pill(R + 132, 252, "respaldos", a.AMB, a.AMBBG, 15, 28)
     + a.pill(R + 36, 286, "actualizaciones", a.AMB, a.AMBBG, 15, 28)
     + a.text(R + 36, 238, "alguien lo mantiene:", 15, a.AMB, a.MONO, 600), 77, 100)

a.add(a.text(48, 604, "Un equipo, un administrador: si la nube y el software local configuran el mismo equipo,", 17, a.TXT, a.SANS, 600))
a.add(a.text(48, 630, "cada uno pisa lo que hizo el otro. Se define uno y se anota en la ficha.", 17, a.TXT, a.SANS, 600))

out(a, 40, 1, "Nube o local: dónde vive la base de datos",
    "Animación con dos paneles. A la izquierda, nube SmartPlus: equipos del edificio, un router sin nada entrante, la nube y la app del residente. "
    "A la derecha, local: un servidor en el edificio conectado a los equipos, y el router hacia internet. "
    "Tiempo 1: en la nube, la conexión sale del edificio hacia la nube; no se abren puertos. "
    "Tiempo 2: la app del residente se comunica con los equipos a través de la nube, desde cualquier lugar. "
    "Tiempo 3: se corta internet en los dos edificios; en la nube las funciones se detienen, en el local el servidor sigue andando con los equipos. "
    "Tiempo 4: el servidor local pide que alguien lo mantenga: energía, respaldos y actualizaciones. "
    "Abajo: un equipo con un solo administrador, anotado en la ficha.",
    [10, 40, 62, 90])
