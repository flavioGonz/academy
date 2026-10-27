#!/usr/bin/env python3
"""Lección 29 · Teoría (2) · El registro es la clave del mantenimiento.
Sale de teoria_md (Cómo funciona): si el E21 pierde el registro, la central lo muestra como no disponible,
y eso se puede revisar o monitorear antes de que alguien lo necesite de verdad. Extensión 801 (laboratorio)."""
from _anim_akuvox_29_42 import new, out, box, travel, when

a = new(20, "PUNTO DE EMERGENCIA · REGISTRO", "El registro avisa antes de la emergencia")
a.steps([
    "El E21 se registra en la central: la extensión 801 queda disponible.",
    "Cada tanto renueva el registro, aunque nadie apriete el botón.",
    "Se corta el cable o la energía: el registro no se renueva.",
    "La central muestra el 801 no disponible: se revisa antes de una emergencia.",
], still=3)

Y = 330
a.add(f'<path d="M290 {Y} H700" stroke="{a.BLUE}" stroke-width="4"/>')
a.add(box(48, 288, 242, 84, "E21", "extensión 801", "bell"))
a.add(box(700, 288, 240, 84, "Central IP", "registros", "server", dark=True))

# panel de estado
a.add(a.box(700, 404, 452, 140, a.WHITE, a.LINE, rx=16))
a.add(a.text(724, 440, "Estado en la central", 17, a.INK, a.SANS, 600))
a.add(a.text(724, 486, "801", 22, a.INK, a.MONO, 600))
a.add(a.text(724, 518, "E21 estacionamiento", 15, a.GREY, a.MONO))
when(a, a.pill(800, 464, "disponible", a.OK, a.OKBG, 16, 32), 10, 52)
when(a, a.pill(800, 464, "sin renovar", a.AMB, a.AMBBG, 16, 32), 52, 76)
when(a, a.pill(800, 464, "no disponible", a.BAD, a.BADBG, 16, 32), 76, 100, still=1)

# registros
for t in (3, 28):
    travel(a, (320, Y - 22), (660, Y - 22), t, t + 6, "REGISTER", a.WHITE, a.BLUE, hold=1)
    travel(a, (660, Y + 26), (320, Y + 26), t + 8, t + 13, "200 OK", a.WHITE, a.OK, hold=1)
when(a, a.text(495, 270, "renueva cada tanto", 15, a.GREY, a.MONO, 600, "middle"), 27, 50)
# corte
when(a, f'<circle cx="495" cy="{Y}" r="18" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2"/>'
     f'<path d="M488 {Y - 7} l14 14 M502 {Y - 7} l-14 14" stroke="{a.BAD}" stroke-width="3" stroke-linecap="round"/>'
     + a.pill(495, 248, "corte de cable o energía", a.BAD, a.BADBG, 15, 28, "middle"), 51, 100, still=1)
travel(a, (320, Y - 22), (470, Y - 22), 56, 62, "REGISTER", a.WHITE, a.GREY, hold=8)
# aviso
when(a, a.pill(1152, 216, "monitoreo: revisar el 801", a.BAD, a.BADBG, 15, 30, "end"), 78, 100, still=1)

a.add(a.text(48, 600, "Revisar o monitorear el registro: la falla aparece en la central antes de que alguien apriete el botón.", 17, a.TXT, a.SANS, 600))

out(a, 29, 2, "El registro avisa antes de la emergencia",
    "Animación del registro SIP del E21 en la central. "
    "Tiempo 1: el E21 manda REGISTER, la central responde 200 OK y la extensión 801 queda disponible. "
    "Tiempo 2: el E21 renueva el registro cada tanto, aunque nadie use el botón. "
    "Tiempo 3: se corta el cable o la energía; el REGISTER no llega y el registro queda sin renovar. "
    "Tiempo 4: la central muestra el 801 como no disponible y el monitoreo avisa que hay que revisarlo, antes de que alguien lo necesite.",
    [12, 38, 62, 90])
