#!/usr/bin/env python3
"""Lección 16 · teoría: el SR01 adentro por RS485; si arrancan el frente, solo encuentran un bus de datos."""
from _anim_akuvox_15_28 import *

a = new(20, "AKUVOX · LECCIÓN 16", "El frente pide, el SR01 de adentro decide")
a.steps([
    "Llega un pedido de apertura al portero: por HTTP, DoorNum=SB.",
    "El portero manda la orden por RS485. El SR01 cierra su contacto: Hold Delay 5 s.",
    "Alguien arranca el frente y puentea los cables que encuentra.",
    "Solo hay un bus de datos: ningún par alimenta la cerradura. Sigue cerrada.",
], still=3)

# zonas y pared
a.add(zone(40, 180, 470, 380, "CALLE"))
a.add(zone(566, 180, 594, 380, "ADENTRO"))
a.add(a.box(527, 172, 22, 396, "#D5DFE9", rx=4))

# portero
a.add(I.Intercom(150, 232, "Portero", "Security Relay B").svg())
# bus RS485 (dos hilos)
for dy, col in ((-8, a.BLUE), (8, a.NAVY2)):
    a.add(f'<path d="M300 {330 + dy} H640" stroke="{col}" stroke-width="3.5"/>')
a.add(a.pill(420, 286, "RS485 · datos", a.BLUE, a.WHITE, 15, anchor="middle"))

# SR01
a.add(I.Box(640, 288, 220, 84, "SR01", "relé de seguridad", icon=I.ICON["shield"]).svg())
# cerradura y fuente
a.add(I.Lock(920, 206, "Cerradura", " ", w=212).svg())
a.add(I.PSU(920, 432, "Fuente", "de la cerradura", w=212).svg())
a.add(f'<path d="M1026 516 V540 H1148 V248 H1132" fill="none" stroke="#2B2B2B" stroke-width="3"/>')
a.add(f'<path d="M920 474 H896 V350 H860" fill="none" stroke="{a.BAD}" stroke-width="3.5"/>')
a.add(f'<path d="M860 310 H896 V248 H920" fill="none" stroke="{a.LINE}" stroke-width="3.5"/>')
a.add(at(a, f'<path d="M860 310 H896 V248 H920" fill="none" stroke="{a.CYAN}" stroke-width="4.5"/>', 28, 47, still=0))
a.add(a.text(904, 300, "contacto", 15, a.GREY, a.MONO))

# estados de la cerradura
a.add(at(a, a.text(984, 267, "trabada", 15, a.GREY, a.MONO), 0, 28, still=0))
a.add(at(a, a.text(984, 267, "libera", 15, a.OK, a.MONO, 600), 28, 47, still=0))
a.add(at(a, a.text(984, 267, "trabada", 15, a.GREY, a.MONO), 47, 75, still=0))
a.add(at(a, a.text(984, 267, "sigue cerrada", 15, a.OK, a.MONO, 600) + mark(1112, 200, True), 75, 100, still=1))

# paso 1: pedido HTTP
a.add(packet(a, "HTTP · DoorNum=SB", (330, 208), (250, 208), 3, 18, hide=25, size=15))
# paso 2: orden por el bus y Hold Delay 5 s
a.add(packet(a, "abrir", (330, 330), (610, 330), 26, 30, color=a.BLUE, hide=31, size=15))
a.add(a.text(600, 404, "Trigger Delay 0 · Hold Delay 5", 15, a.GREY, a.MONO))
for i in range(5):
    t = 28 + i * 3.8
    a.add(at(a, a.box(600 + i * 44, 416, 40, 15, a.CYAN, rx=4), t, 47, still=0))
a.add(at(a, a.text(600, 452, "relé activado", 15, a.CYAN, a.MONO, 600), 28, 47, still=0))
a.add(at(a, a.text(600, 452, "vuelve al reposo", 15, a.GREY, a.MONO, 600), 47, 52, still=0))

# paso 3 y 4: ataque al frente
atk = (f'<rect x="138" y="220" width="174" height="284" rx="24" fill="none" stroke="{a.BAD}" stroke-width="3" stroke-dasharray="9 7"/>'
       + f'<path d="M318 322 C334 322 334 338 318 338" fill="none" stroke="{a.BAD}" stroke-width="4"/>'
       + f'<circle cx="318" cy="322" r="5" fill="{a.BAD}"/><circle cx="318" cy="338" r="5" fill="{a.BAD}"/>'
       + a.text(60, 214, "frente arrancado", 16, a.BAD, a.SANS, 600)
       + a.text(352, 380, "puente en los cables", 15, a.BAD, a.MONO, 600))
a.add(at(a, atk, 51, 100, still=1))
a.add(at(a, a.box(586, 476, 300, 66, a.OKBG, a.OK, rx=12, sw=1.5)
         + a.text(602, 503, "por el bus solo viajan datos:", 15, a.OK, a.SANS, 600)
         + a.text(602, 526, "la cerradura no recibe energía", 15, a.OK, a.SANS, 600), 76, 100, still=1))

a.write(*out(16)[:1], title="SR01 por RS485 contra un ataque al frente",
        desc=("Animación en cuatro tiempos. Del lado de la calle está el portero; del lado de adentro, el SR01, la cerradura y su fuente, unidos al portero solo por el bus RS485. "
              "1: llega al portero un pedido HTTP con DoorNum=SB. 2: el portero manda la orden por RS485; el SR01 cierra su propio contacto, la cerradura libera durante el Hold Delay de 5 segundos (Trigger Delay 0) y después vuelve al reposo. "
              "3: alguien arranca el frente y puentea los cables que encuentra. 4: solo hay un bus de datos, ningún par alimenta la cerradura, y la puerta sigue cerrada."),
        preview=[10, 38, 62, 90], prefix=out(16)[1])
