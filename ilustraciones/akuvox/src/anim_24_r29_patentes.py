#!/usr/bin/env python3
"""Lección 24 · teoría: desde el firmware 29.30.10.745 el R29 abre leyendo patentes de cámaras Hikvision y Dahua por la HTTP API."""
from _anim_akuvox_15_28 import *

a = new(20, "AKUVOX", "R29 y cámara de patentes: el firmware decide")
a.steps([
    "Llega un auto. La cámara de patentes (Hikvision o Dahua) lee la patente.",
    "La cámara manda la lectura al R29 por la HTTP API.",
    "Con firmware 29.30.10.745 o más, el R29 abre: su relé levanta la barrera.",
    "Con un firmware anterior, esa función no está: la barrera no se mueve.",
], still=2)

G = 500  # suelo
a.add(f'<path d="M48 {G} H1152" stroke="{I.LINE2}" stroke-width="3"/>')

# auto
car = (f'<path d="M0 0 H230 V-34 L196 -40 L160 -76 H70 L40 -40 L0 -34 Z" fill="{a.BLUE}" stroke="{a.INK}" stroke-width="2"/>'
       f'<path d="M78 -68 H152 L178 -42 H58 Z" fill="#CFE4F7"/>'
       f'<circle cx="52" cy="2" r="20" fill="{a.INK}"/><circle cx="182" cy="2" r="20" fill="{a.INK}"/>'
       f'<rect x="212" y="-30" width="26" height="18" rx="3" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="1.5"/>')
a.add(a.group(car, a.move([(0, -260, G - 20), (2, -260, G - 20), (14, 150, G - 20), (100, 150, G - 20)]), a.show(0, 15, 0.1), still=0))
a.add(at(a, f'<g transform="translate(150 {G - 20})">{car}</g>', 14, 100, still=1))
# cámara en poste
a.add(f'<path d="M470 {G} V300" stroke="{a.GREY}" stroke-width="6"/>')
a.add(f'<g transform="rotate(18 470 290)"><rect x="420" y="272" width="64" height="32" rx="6" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="2.5"/><rect x="408" y="278" width="14" height="20" rx="3" fill="{a.INK}"/></g>')
a.add(a.text(470, 250, "cámara de patentes", 15, a.INK, a.SANS, 600, "middle"))
beam = f'<path d="M414 296 L384 452 L372 476 Z" fill="{a.CYAN}" opacity=".35"/>'
a.add(at(a, beam, 14, 25, still=0))
a.add(at(a, a.box(290, 330, 110, 36, a.WHITE, a.CYAN, rx=8, sw=2) + a.text(345, 354, "patente", 15, a.BLUE, a.MONO, 600, "middle"), 16, 50, still=0))

# barrera
BX, BY = 590, 432
a.add(a.box(BX - 14, BY - 10, 28, G - BY + 10, a.INK, rx=6))
arm = f'<rect x="{BX}" y="{BY - 8}" width="210" height="16" rx="8" fill="{a.WHITE}" stroke="{a.BAD}" stroke-width="3" stroke-dasharray="22 14"/>'
rot = a.keyframes([(0, 0), (56, 0), (60, -78), (74, -78), (78, 0), (100, 0)], "transform", "rotate({}deg)")
a.add(a.group(arm, rot, a.show(0, 100), still=0, origin=f"{BX}px {BY}px"))
a.add(a.group(f'<g transform="rotate(-78 {BX} {BY})">{arm}</g>', a.keyframes([(0, 0), (100, 0)]), still=1))
a.add(a.text(BX, G + 30, "barrera", 15, a.GREY, a.SANS, 600, "middle"))

# R29
a.add(I.Intercom(960, 176, "R29", "Android 7\"", screen=True).svg())
a.add(at(a, a.text(1035, 236 + 50, "HTTP API", 15, "#9FC3E3", a.MONO, 600, "middle"), 30, 100, still=1))
# relé hacia la barrera
a.add(f'<path d="M960 400 H900 V{BY + 40} H{BX + 14}" fill="none" stroke="{a.LINE}" stroke-width="4"/>')
a.add(a.text(846, BY + 30, "relé", 15, a.GREY, a.MONO, 600))
a.add(at(a, f'<path d="M960 400 H900 V{BY + 40} H{BX + 14}" fill="none" stroke="{a.CYAN}" stroke-width="5"/>', 54, 75, still=1))
a.add(at(a, mark(720, BY + 40, False), 80, 100, still=0))

# lectura viaja por la red
a.add(f'<path d="M490 290 H950" stroke="{a.LINE}" stroke-width="3" stroke-dasharray="6 8"/>')
a.add(packet(a, "patente · HTTP API", (580, 290), (850, 290), 28, 44, hide=50))

# firmware
a.add(a.box(48, 556, 1104, 92, a.WHITE, a.LINE, rx=14))
a.add(a.text(70, 586, "Status > Basic > Product Information", 15, a.GREY, a.MONO, 600))
a.add(a.text(70, 622, "Firmware", 17, a.TXT, a.SANS, 600))
a.add(at(a, a.text(170, 622, "29.30.10.745 o más", 19, a.INK, a.MONO, 600) + mark(420, 616, True)
         + a.text(450, 622, "abre por patente", 17, a.OK, a.SANS, 600), 52, 75, still=1))
a.add(at(a, a.text(170, 622, "anterior a 29.30.10.745", 19, a.INK, a.MONO, 600) + mark(470, 616, False)
         + a.text(500, 622, "no abre por patente", 17, a.BAD, a.SANS, 600), 76, 100, still=0))
a.add(a.text(1130, 622, "29 = código del R29", 16, a.BLUE, a.MONO, 600, "end"))

a.write(*out(24)[:1], title="R29 que abre por patente según el firmware",
        desc=("Animación en cuatro tiempos. 1: llega un auto y una cámara de patentes Hikvision o Dahua lee la patente. "
              "2: la cámara manda la lectura al R29 por la HTTP API. "
              "3: con firmware 29.30.10.745 o más, el R29 abre y su relé levanta la barrera. "
              "4: con un firmware anterior esa función no está y la barrera no se mueve. "
              "Abajo, el firmware se lee en Status > Basic > Product Information; el primer bloque, 29, es el código del R29."),
        preview=[18, 40, 66, 92], prefix=out(24)[1])
