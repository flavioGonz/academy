import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 6.svg: casa tipo, cada zona su definición
c = Canvas(K(), "El tipo de zona sale del recorrido de entrada")
c.add(NOLIG)
c.add(rect(48, 124, 640, 470, WHITE, LINE2, rx=18))
c.add(text(72, 156, "Casa tipo · planta", 15, 500, INK3, FM))
# paredes
c.add(f'<path d="M90 190H650V560H90Z" fill="{GROUND}" stroke="{INK3}" stroke-width="4"/>')
c.add(f'<path d="M370 190V380M370 440V560M90 380H90" stroke="{INK3}" stroke-width="3"/>')
c.add(text(150, 430, "Living y entrada", 17, 600, INK2, FB))
c.add(text(470, 300, "Dormitorio", 17, 600, INK2, FB))
# puerta principal abajo izquierda
c.add(f'<path d="M180 560H250" stroke="{GROUND}" stroke-width="6"/><path d="M180 560L230 520" stroke="{BLUE}" stroke-width="4"/>')
c.add(badge(214, 586, "1", BLUE, 16, 15))
# teclado en el hall
c.add(rect(296, 500, 40, 50, WHITE, INK2, rx=6)); c.add(text(316, 492, "teclado", 14, 600, INK2, FB, anchor="middle"))
# PIR del living que ve el teclado
c.add(f'<path d="M110 210L345 470L250 545Z" fill="{CYAN}" fill-opacity=".14" stroke="{CYAN}" stroke-dasharray="4 4"/>')
c.add(f'<circle cx="110" cy="210" r="10" fill="{CYAN}"/>'); c.add(badge(140, 206, "2", CYAN, 16, 15))
# ventanas
for (x1, y1, x2, y2) in [(430, 190, 520, 190), (650, 250, 650, 330)]:
    c.add(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{OK}" stroke-width="8"/>')
c.add(badge(475, 214, "3", OK, 16, 15)); c.add(badge(626, 290, "3", OK, 16, 15))
# caja de medidores (afuera)
c.add(rect(560, 572, 80, 16, WARN_BG, WARN, rx=4)); c.add(badge(540, 580, "4", WARN, 16, 15))
c.add(text(650, 612, "medidores", 14, 600, WARN, FB, anchor="end"))
rows = [("1", BLUE, "01", "Retardo de entrada 1", "Puerta principal: da tiempo a desarmar."),
        ("2", CYAN, "05", "Seguimiento", "PIR que ve el teclado: espera si abrió la puerta."),
        ("3", OK, "08", "Instantánea", "Ventanas y perímetro: dispara al instante."),
        ("4", WARN, "16", "Robo 24 h", "Tapa de medidores: armada siempre."),
        ("", ALERT, "11", "Fuego", "Normalmente abierta con EOL. No se puede anular.")]
for i, (n, col, code_, t, d) in enumerate(rows):
    y = 128 + i * 96
    c.add(rect(712, y, 440, 84, WHITE, LINE2, rx=14))
    if n:
        c.add(badge(742, y + 30, n, col, 16, 15))
    c.add(text(770, y + 36, code_, 20, 700, col, FM))
    c.add(text(812, y + 36, t, 18, 600, INK, FB))
    svg, _ = wrap(736, y + 64, d, 400, 15, 400, INK2)
    c.add(svg)
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso1: anatomía de la sección de zona
c = Canvas(K(1), "Cada zona es una sección: definición, partición, opciones")
c.add(NOLIG)
c.add(Step(48, 150, 1))
sv, _ = keys(80, 132, ["[001]", "+", "01", "1", "+", ("opciones 1 a 8",), "[ENTER]"], 22)
c.add(sv)
for x, lab, col in [(116, "zona 1", INK3), (228, "definición", BLUE), (262, "partición", OK)]:
    c.add(text(x, 206 if lab != "partición" else 228, lab, 16, 600, col, FB, anchor="middle"))
c.add(text(80, 260, "De fábrica vienen encendidas las opciones 1, 2, 3 y 8:", 17, 600, INK2, FB))
c.add(opts(80, 280, {1, 2, 3, 8}, size=40, gap=8))
c.add(text(80, 362, "Partición: 1, 2, o 3 para ambas. ENTER guarda y avanza a la zona siguiente.", 16, 500, INK2, FB))
c.add(Table(48, 400, ["Sección", "Dato", "Zona", "Tipo"], [
    ["[001]", "01 1", "puerta principal", "retardo de entrada 1"],
    ["[002]", "05 1", "PIR del living", "seguimiento"],
    ["[003]", "08 1", "ventanas", "instantánea"],
    ["[004]", "16 1", "tapa de medidores", "robo 24 h"],
], [180, 180, 340, 404], row_h=40, mono_cols=(0, 1)))
save(c, "6-paso1.svg")

# ---------------------------------------------------------------- 6-paso4: la prueba del recorrido
c = Canvas(K(4), "Probalo como el cliente: dos recorridos, dos resultados")
c.add(NOLIG)
def lane(y, title, evs, res, kd):
    c.add(text(48, y, title, 19, 600, INK, FD))
    x = 48
    for i, (t, s) in enumerate(evs):
        c.add(rect(x, y + 18, 236, 92, WHITE, LINE2, rx=12))
        c.add(text(x + 18, y + 54, t, 17, 600, INK, FB))
        c.add(text(x + 18, y + 82, s, 15, 400, INK3, FB))
        x += 236
        c.add(Arrow((x + 4, y + 64), (x + 30, y + 64)))
        x += 36
    bg, fg = KC[kd]
    c.add(rect(x, y + 18, 1152 - x, 92, bg, fg, rx=12))
    svg, _ = wrap(x + 18, y + 54, res, 1152 - x - 30, 17, 600, fg)
    c.add(svg)
lane(140, "Paso 3 · Entra por la puerta", [("Abre la puerta", "zona 1 · retardo 45 s"), ("Camina frente al PIR", "zona 2 · seguimiento: espera"), ("Desarma", "en el teclado, a tiempo")], "Sin alarma", "ok")
lane(320, "Paso 4 · El PIR primero, sin abrir la puerta", [("Armado", "la puerta sigue cerrada"), ("Se activa el PIR", "zona 2 · nadie abrió antes")], "Alarma al instante: alguien entró por otro lado", "alert")
c.add(Step(48, 340, 4))
c.add(Note(48, 500, 1104, "Si en una obra hay falsas alarmas en la entrada, la opción 7 de la zona 1 (retardo de transmisión) suena pero no reporta si se desarma a tiempo; el tiempo va en [833]. Con monitoreo, avisá antes de cada prueba.", kind="info", size=16))
save(c, "6-paso4.svg")
