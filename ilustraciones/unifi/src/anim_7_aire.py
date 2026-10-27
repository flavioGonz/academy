#!/usr/bin/env python3
"""Lección 7 · teoría: el aire de un canal se comparte; 4 AP en 20 MHz contra 4 AP en 80 MHz."""
from _anim_unifi import *  # noqa

a = new(26, "Canales", "Un canal es un solo aire: se turnan para hablar", [
    "En el canal 36 transmite un equipo por vez: el resto escucha y espera.",
    "El AP del vecino en el mismo canal también gasta ese aire.",
    "Cuatro AP en 20 MHz: canales 36, 40, 44 y 48, cada uno con su aire.",
    "Los mismos cuatro en 80 MHz: un solo canal, 36 a 48, y se turnan.",
], still=3)


def grow(x, y, w, h, color, t0, t1, hide, label=None, still=0, tsize=14):
    """Bloque de aire que crece de izquierda a derecha entre t0 y t1 y queda hasta hide."""
    inner = a.box(x, y, w, h, color, rx=5)
    if label:
        inner += a.text(x + w / 2, y + h / 2 + 5, label, tsize, A.WHITE, A.MONO, 600, "middle")
    sc = a.keyframes([(0, 0), (t0, 0), (t1, 1), (100, 1)], "transform", "scaleX({})")
    a.add(a.group(inner, sc, a.show(t0, hide, 0.3), still=still, origin=f"{x}px {y}px"))


def track(x0, x1, y, h, w0, w1, blocks, hide, still=0):
    a.add(a.box(x0, y, x1 - x0, h, A.WHITE, A.LINE, rx=6, sw=1.5))
    k = (x1 - x0) / (w1 - w0)
    for t0, t1, col, lab in blocks:
        grow(x0 + (t0 - w0) * k, y + 3, (t1 - t0) * k - 2, h - 6, col, t0, t1, hide, lab, still)


def status(x, y, t_on):
    """Estado del equipo: 'espera' gris y 'transmite' verde en los intervalos t_on."""
    w = 150
    for t0, t1 in t_on:
        at(a, a.box(x, y, w, 28, A.OKBG, A.OK, rx=14, sw=1.5) + a.text(x + w / 2, y + 19, "transmite", 14, A.OK, A.MONO, 600, "middle"), t0, t1, fade=0.3)


# ---------- escena A (tiempos 1 y 2)
SA = []
DEVS = [(48, "AP 1", "canal 36", A.BLUE), (318, "Celular", "cliente de AP 1", A.CYAN),
        (640, "AP del vecino", "también canal 36", A.AMB), (930, "Notebook", "cliente del vecino", "#D9902A")]
BLK = [(2, 8, 0, "AP 1"), (9, 13, 1, "celular"), (14, 19, 0, "AP 1"), (20, 24, 1, "celular"),
       (26, 33, 2, "vecino"), (34, 38, 3, "notebook"), (39, 43, 0, "AP 1"), (44, 49, 2, "vecino")]
scene_a = ""
for x, n, sub, col in DEVS:
    scene_a += node(a, x, 196, 222, 78, n, sub, ssize=14) + f'<rect x="{x}" y="196" width="6" height="78" rx="3" fill="{col}"/>'
    scene_a += a.box(x, 290, 150, 28, "#E6EDF4", rx=14) + a.text(x + 75, 309, "espera", 14, A.GREY, A.MONO, 600, "middle")
scene_a += a.text(160, 384, "AIRE DEL CANAL 36", 14, A.GREY, A.MONO, extra='letter-spacing="1.5"')
scene_a += a.text(160, 480, "tiempo →", 14, A.GREY, A.MONO)
vis(a, scene_a, 0, 1)
for i, (x, n, sub, col) in enumerate(DEVS):
    status(x, 290, [(t0, t1) for t0, t1, d, _ in BLK if d == i])
X0, X1 = 160, 1150
a.add(a.group(a.box(X0, 396, X1 - X0, 54, A.WHITE, A.LINE, rx=6, sw=1.5), a.show(0, 50), still=0))
k = (X1 - X0) / 50
for t0, t1, d, lab in BLK:
    grow(X0 + t0 * k, 399, (t1 - t0) * k - 2, 48, DEVS[d][3], t0, t1, 50, lab)
vis(a, note(a, 48, 520, 1104, "Mientras uno transmite, los demás del canal escuchan y esperan su turno.", "info"), 0)
vis(a, note(a, 48, 520, 1104, "El vecino no es tuyo, pero comparte el canal: su tiempo de aire es tiempo que tus equipos esperan.", "amb"), 1)

# ---------- escena B (tiempos 3 y 4)
LP, RP = 40, 620
pan = ""
pan += a.box(LP, 180, 540, 390, A.WHITE, A.LINE, rx=16)
pan += a.text(LP + 22, 216, "20 MHz", 20, A.INK, A.HEAD, 600) + a.text(LP + 104, 216, "cuatro canales distintos", 15, A.GREY, A.MONO)
pan += a.box(RP, 180, 540, 390, A.WHITE, A.LINE, rx=16)
pan += a.text(RP + 22, 216, "80 MHz", 20, A.INK, A.HEAD, 600) + a.text(RP + 104, 216, "todos en 36 a 48", 15, A.GREY, A.MONO)
CH = ["36", "40", "44", "48"]
APC = [A.BLUE, A.CYAN, A.OK, A.NAVY2]
for i in range(4):
    y = 248 + i * 74
    pan += a.box(LP + 20, y, 78, 44, A.SLATE, rx=10) + a.text(LP + 59, y + 28, f"AP {i + 1}", 16, A.INK, A.MONO, 600, "middle")
    pan += a.pill(LP + 108, y + 8, CH[i], A.BLUE, "#E4EFFA", 14)
    pan += a.box(RP + 20, y, 78, 44, A.SLATE, rx=10) + a.text(RP + 59, y + 28, f"AP {i + 1}", 16, A.INK, A.MONO, 600, "middle")
vis(a, pan, 2, 3)
for i in range(4):
    y = 248 + i * 74
    o = i * 0.8
    bl = [(51 + o, 62 + o, APC[i], None), (63 + o, 73.5, APC[i], None)]
    a.add(a.group(a.box(LP + 180, y + 2, 340, 40, A.WHITE, A.LINE, rx=6, sw=1.5), a.show(50, 100), still=1))
    kk = 340 / 25
    for t0, t1, col, lab in bl:
        grow(LP + 180 + (t0 - 50) * kk, y + 5, (t1 - t0) * kk - 2, 34, col, t0, t1, 100, lab, still=1)
    a.add(a.group(a.box(RP + 112, y + 2, 408, 40, A.WHITE, A.LINE, rx=6, sw=1.5), a.show(50, 100), still=1))
kk = 408 / 25
turns = [76, 79, 82, 85, 88, 91, 94, 97]
for j, t0 in enumerate(turns):
    i = j % 4
    y = 248 + i * 74
    grow(RP + 112 + (t0 - 75) * kk, y + 5, 3 * kk - 2, 34, APC[i], t0, t0 + 2.8, 100, None, still=1)
vis(a, a.text(LP + 22, 556, "transmiten a la vez, cada uno en su canal", 15, A.OK, A.SANS, 600), 2, 3)
vis(a, a.text(RP + 22, 556, "más rápido cuando le toca, pero espera turno", 15, A.AMB, A.SANS, 600), 3)
vis(a, note(a, 48, 590, 1104, "El ancho se elige por la cantidad de clientes y vecinos, no por lo que dice la caja.", "info", size=16, h=44), 3)

write(a, "7-t1.svg", "El tiempo de aire de un canal WiFi", mid_pcts(a))
