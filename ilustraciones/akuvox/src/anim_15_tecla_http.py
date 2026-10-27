#!/usr/bin/env python3
"""Lección 15 · teoría: la tecla del monitor abre por HTTP, sin llamada (y el formato que exige la alta seguridad)."""
from _anim_akuvox_15_28 import *

a = new(20, "AKUVOX · LECCIÓN 15", "La tecla del monitor manda un GET, no un tono")
a.steps([
    "Tocás la tecla Portón en el monitor. No hace falta una llamada abierta.",
    "El monitor arma un GET con usuario, clave y DoorNum, y va directo al portero.",
    "El portero verifica la credencial y dispara el relé indicado: DoorNum=1 es el A.",
    "Con alta seguridad, la URL vieja /fcgi/do queda rechazada. Solo /fcgi/OpenDoor.",
], still=2)

# zona VLAN
a.add(zone(40, 180, 1112, 368, "VLAN de porteros · sin central"))

# monitor
a.add(I.Monitor(70, 240, "Monitor", "Remote Relay By HTTP").svg())
a.add(a.text(190, 290, "monitoreo · portón", 15, "#9FC3E3", a.MONO, 400, "middle"))
a.add(a.box(130, 320, 120, 34, a.BLUE, rx=8) + a.text(190, 343, "Portón", 16, a.WHITE, a.SANS, 600, "middle"))
a.add(tap(a, 225, 340, 6, 14))

# portero
a.add(I.Intercom(690, 226, "Portero portón", "192.168.88.22").svg())
a.add(a.text(765, 330, "Open Relay", 15, "#9FC3E3", a.MONO, 400, "middle"))
a.add(a.text(765, 348, "via HTTP", 15, "#9FC3E3", a.MONO, 400, "middle"))

# cable lógico monitor -> portero
a.add(f'<path d="M318 330 H680" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="6 8"/>')

# relés y portón
RX = 900
a.add(a.box(RX, 232, 230, 58, a.WHITE, a.LINE))
a.add(a.text(RX + 18, 258, "Relé B", 17, a.INK, a.SANS, 600) + a.text(RX + 18, 279, "DoorNum=2", 15, a.GREY, a.MONO))
a.add(a.text(RX + 212, 270, "en reposo", 15, a.GREY, a.MONO, 400, "end"))
a.add(a.box(RX, 302, 230, 58, a.WHITE, a.LINE))
a.add(a.text(RX + 18, 328, "Relé A", 17, a.INK, a.SANS, 600) + a.text(RX + 18, 349, "DoorNum=1", 15, a.GREY, a.MONO))
a.add(f'<path d="M842 261 H{RX - 6}" stroke="{a.LINE}" stroke-width="3"/>')
a.add(f'<path d="M842 331 H{RX - 6}" stroke="{a.LINE}" stroke-width="3"/>')
# relé A: reposo / activo
a.add(at(a, a.text(RX + 212, 340, "en reposo", 15, a.GREY, a.MONO, 400, "end"), 0, 55, still=0))
a.add(at(a, a.box(RX, 302, 230, 58, a.OKBG, a.OK, sw=3)
         + a.text(RX + 18, 328, "Relé A", 17, a.INK, a.SANS, 600) + a.text(RX + 18, 349, "DoorNum=1", 15, a.OK, a.MONO, 600)
         + a.pill(RX + 214, 316, "activado", a.OK, a.WHITE, 15, anchor="end")
         + f'<path d="M842 331 H{RX - 6}" stroke="{a.CYAN}" stroke-width="4"/>', 55, 75, still=1))
a.add(at(a, a.text(RX + 212, 340, "en reposo", 15, a.GREY, a.MONO, 400, "end"), 75, 100, still=0))
# portón
a.add(a.box(RX, 392, 230, 70, a.WHITE, a.LINE))
a.add(f'<g transform="translate({RX + 18} 410) scale(1.35)" fill="none" stroke="{a.BLUE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{I.ICON["lock"]}</g>')
a.add(a.text(RX + 64, 422, "Portón", 18, a.INK, a.SANS, 600))
a.add(at(a, a.text(RX + 64, 446, "cerrado", 15, a.GREY, a.MONO), 0, 57, still=0))
a.add(at(a, a.text(RX + 64, 446, "abre", 15, a.OK, a.MONO, 600), 57, 75, still=1))
a.add(at(a, a.text(RX + 64, 446, "cerrado", 15, a.GREY, a.MONO), 75, 100, still=0))
a.add(f'<path d="M{RX + 115} 360 V392" stroke="{a.LINE}" stroke-width="3"/>')
a.add(at(a, f'<path d="M{RX + 115} 360 V392" stroke="{a.CYAN}" stroke-width="4"/>', 56, 75, still=1))

# paquetes
a.add(packet(a, "GET /fcgi/OpenDoor", (440, 330), (560, 330), 28, 46, hide=50))
a.add(at(a, a.pill(500, 284, "usuario · clave · DoorNum", a.BLUE, a.WHITE, 15, anchor="middle"), 27, 50, still=0))
a.add(packet(a, "GET /fcgi/do", (420, 330), (580, 330), 79, 89, color=a.AMB, hide=100))

# verificación en el portero
a.add(at(a, mark(660, 272, True) + a.text(632, 278, "credencial ok", 16, a.OK, a.MONO, 600, "end"), 51, 75, still=1))
a.add(at(a, mark(660, 272, False) + a.text(632, 278, "rechazada", 16, a.BAD, a.MONO, 600, "end"), 89, 100, still=0))
a.add(at(a, a.box(450, 392, 220, 96, a.AMBBG, a.AMB, rx=12, sw=1.5)
         + a.text(466, 418, "alta seguridad:", 15, a.AMB, a.MONO, 600)
         + a.text(466, 442, "firmware 3er bloque", 15, a.AMB, a.MONO, 400)
         + a.text(466, 466, "≥ 10 y modo encendido", 15, a.AMB, a.MONO, 400), 76, 100, still=0))

# URL abajo
new_url, sp = code(a, 48, 592, [("http://monitor-porton:clave@192.168.88.22", "#D9E9F8"), ("/fcgi/OpenDoor", "#7FE0FF"),
                                   ("?action=OpenDoor&", "#D9E9F8"), ("DoorNum=1", "#FFD28A")], size=16)
a.add(at(a, a.text(48, 582, "Lo que manda la tecla", 15, a.GREY, a.SANS, 600) + new_url, 26, 75, still=1))
x0, x1 = sp[3]
a.add(at(a, f'<rect x="{x0 - 4:.0f}" y="596" width="{x1 - x0 + 8:.0f}" height="36" rx="6" fill="none" stroke="#FFD28A" stroke-width="2"/>'
         + a.text((x0 + x1) / 2, 658, "relé A", 15, a.AMB, a.MONO, 600, "middle"), 53, 75, still=1))
old_url, sp2 = code(a, 48, 592, [("http://192.168.88.22", "#D9E9F8"), ("/fcgi/do", "#FFB4A6"), ("?…usuario y clave en la consulta", "#D9E9F8")], size=16)
a.add(at(a, a.text(48, 582, "Formato viejo", 15, a.BAD, a.SANS, 600) + old_url
         + f'<path d="M{sp2[1][0]:.0f} 614 H{sp2[1][1]:.0f}" stroke="{a.BAD}" stroke-width="3"/>'
         + a.text(sp2[2][1] + 36, 620, "el portero no lo acepta", 16, a.BAD, a.SANS, 600), 76, 100, still=0))
a.add(at(a, a.text(48, 620, "Sin llamada en curso: la tecla no depende de DTMF.", 17, a.TXT, a.SANS, 600), 0, 25, still=0))

a.write(*out(15)[:1], title="Tecla del monitor que abre por HTTP",
        desc=("Animación en cuatro tiempos. 1: en el monitor, en la pantalla de monitoreo del portón, tocás la tecla Portón; no hay llamada abierta. "
              "2: el monitor arma un pedido HTTP GET a /fcgi/OpenDoor con usuario, clave y DoorNum, y lo manda directo al portero 192.168.88.22 por la VLAN de porteros, sin central. "
              "3: el portero verifica la credencial y dispara el relé indicado; DoorNum=1 es el relé A y el portón abre, el relé B queda en reposo. "
              "4: si el portero tiene alta seguridad (tercer bloque del firmware 10 o más y el modo encendido), un pedido con la URL vieja /fcgi/do y usuario y clave en la consulta queda rechazado."),
        preview=[12, 40, 62, 92], prefix=out(15)[1])
