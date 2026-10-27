#!/usr/bin/env python3
"""Lección 34 · Teoría · WR01: tres caminos hasta el relé, y todo queda registrado.
Sale de teoria_md (Cómo funciona): web y API (pedido HTTP con usuario y clave), Bluetooth (decide con su
lista de usuarios), patente de una cámara LPR compatible (desde 1401.30.11.221); cada apertura queda en
el registro; las entradas hacen el camino inverso (un pulsador le avisa al WR01)."""
from _anim_akuvox_29_42 import new, out, box, travel, when

a = new(24, "A15 Y WR01 · RELÉ DE BORDE", "WR01: tres caminos al relé, un solo registro")
a.steps([
    "Web o API: un pedido HTTP con usuario y clave hace actuar el relé 1.",
    "Bluetooth: el celular se acerca y el WR01 decide con su lista de usuarios.",
    "Patente: la cámara LPR manda la lectura; abre si está autorizada.",
    "Al revés: el pulsador avisa por la entrada 1. Todo queda en el registro.",
], still=2)

# cables fijos
for y in (218, 324, 430):
    a.add(f'<path d="M298 {y} C380 {y} 400 321 470 321" fill="none" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="6 6"/>')
a.add(f'<path d="M740 300 C820 300 830 238 902 238" fill="none" stroke="{a.CYAN}" stroke-width="4"/>')
a.add(f'<path d="M740 342 C820 342 830 404 902 404" fill="none" stroke="{a.CYAN}" stroke-width="4"/>')

a.add(box(48, 176, 250, 84, "Web o API", "HTTP + usuario", "laptop"))
a.add(box(48, 282, 250, 84, "Celular", "credencial BLE", "phone"))
a.add(box(48, 388, 250, 84, "Cámara LPR", "lee la patente", "camera"))
a.add(box(470, 266, 270, 110, "WR01", "lista de usuarios", "bolt", dark=True))
a.add(box(902, 196, 250, 84, "Portón o barrera", "relé 1", "door"))
a.add(box(902, 362, 250, 84, "Pulsador", "entrada 1", "bell"))
W = (605, 321)
# t1 HTTP
travel(a, (175, 218), W, 3, 11, "GET + clave", a.WHITE, a.BLUE, hold=2)
# t2 BLE
travel(a, (175, 324), W, 28, 36, "BLE", a.WHITE, a.BLUE, hold=2)
when(a, a.pill(605, 236, "en la lista", a.OK, a.OKBG, 15, 26, "middle"), 37, 47)
# t3 LPR
travel(a, (175, 430), W, 53, 61, "patente", a.WHITE, a.BLUE, hold=2)
when(a, a.pill(605, 236, "patente autorizada", a.OK, a.OKBG, 15, 26, "middle"), 62, 72, still=1)
# relé -> portón (t1, t2, t3)
for t in (13, 38, 63):
    travel(a, (750, 300), (895, 238), t, t + 5, None, bg=a.CYAN, dot=10, hold=0.5)
    when(a, f'<rect x="900" y="194" width="254" height="88" rx="17" fill="none" stroke="{a.OK}" stroke-width="3"/>'
         + a.pill(1027, 290, "abre", a.OK, a.OKBG, 15, 26, "middle"), t + 5, t + 11, still=1 if t == 63 else 0)
# t4 entrada
travel(a, (895, 404), (750, 342), 79, 86, "entrada 1", a.WHITE, a.CYAN, hold=2)
when(a, f'<rect x="900" y="360" width="254" height="88" rx="17" fill="none" stroke="{a.CYAN}" stroke-width="3"/>', 77, 88)

# registro
a.add(a.box(48, 492, 1104, 160, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, 524, "Registro del WR01", 18, a.INK, a.SANS, 600))
a.add(a.text(260, 524, "guarda hasta 100.000 registros", 15, a.GREY, a.MONO))
rows = [(14, "relé 1", "web / API", "usuario de la API"),
        (44, "relé 1", "Bluetooth", "usuario de la lista"),
        (69, "relé 1", "cámara LPR", "patente autorizada"),
        (87, "entrada 1", "pulsador", "")]
for i, (t, c1, c2, c3) in enumerate(rows):
    y = 556 + i * 25
    when(a, a.text(72, y, c1, 16, a.INK, a.MONO, 600) + a.text(210, y, c2, 16, a.INK, a.MONO, 600) + a.text(380, y, c3, 16, a.TXT, a.MONO),
         t, 100, still=1 if i < 3 else 0)

out(a, 34, 1, "WR01: tres caminos al relé, un solo registro",
    "Animación del WR01 con tres orígenes a la izquierda (web o API, celular, cámara LPR), un portón en el relé 1 y un pulsador en la entrada 1. "
    "Tiempo 1: llega un pedido HTTP con usuario y clave y el relé 1 abre el portón. "
    "Tiempo 2: un celular presenta su credencial por Bluetooth; el WR01 la encuentra en su lista de usuarios y abre. "
    "Tiempo 3: la cámara LPR manda una patente; está autorizada y el relé 1 abre. "
    "Tiempo 4: el camino inverso, el pulsador avisa al WR01 por la entrada 1. "
    "Abajo, el registro del WR01 suma una línea por cada evento.",
    [8, 42, 70, 92])
