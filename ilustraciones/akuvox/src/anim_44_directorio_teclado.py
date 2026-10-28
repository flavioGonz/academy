#!/usr/bin/env python3
"""Lección 44 · Teoría · Del modo directorio al modo teclado, y el theme de nube sin nube.
Sale de teoria_md (Cómo funciona): dentro de Building, la página de inicio puede ser la de íconos, el directorio
o el teclado del PIN; Gate Mode muestra lo que hay en una comunidad de SmartPlus y en una obra local queda vacío.
Rutas y opciones: guías de pantalla del X915 y del R29, nota de themes por modelo."""
from _anim_akuvox_29_42 import new, out, when
from _theme import door_screen
import ilus

a = new(24, "PORTERO · PANTALLA", "Del directorio al teclado, y un theme que pide nube")
a.steps([
    "Building con Home Page: íconos y recuadro de rostro.",
    "Página de inicio en directorio: la visita toca un apartamento y llama.",
    "Página de inicio en PIN: arranca en el teclado; código correcto, abre.",
    "Gate Mode sin SmartPlus: no hay edificios para mostrar.",
], still=1)

DX, DY, DW, DH = 60, 160, 240, 410
a.add(door_screen(DX, DY, DW, DH, "building"))
when(a, door_screen(DX, DY, DW, DH, "building"), 0, 25, still=0)
when(a, door_screen(DX, DY, DW, DH, "directory"), 25, 50, still=1)
when(a, door_screen(DX, DY, DW, DH, "keypad"), 50, 75, still=0)
when(a, door_screen(DX, DY, DW, DH, "gate_empty", hl=ilus.WARN), 75, 100, still=0)

# tiempo 2: toque en 201 y llamada
sx, sy, sw = DX + 12, DY + 32, DW - 24
row_y = sy + 40 + 2 * 42
when(a, f'<rect x="{sx + 10}" y="{row_y}" width="{sw - 20}" height="34" rx="8" fill="none" stroke="{a.CYAN}" stroke-width="3"/>', 31, 50, still=1)
when(a, a.pill(DX + DW + 24, row_y + 2, "Llamando a 201", a.WHITE, a.BLUE, 15, 30), 35, 50, still=1)
# tiempo 3: código y relé
when(a, a.pill(DX + DW + 24, DY + 60, "código correcto", a.WHITE, a.BLUE, 15, 30), 58, 75, still=0)
when(a, a.pill(DX + DW + 24, DY + 104, "relé A: abre", a.OK, a.OKBG, 15, 30), 63, 75, still=0)

# panel de ajustes
PX, PW = 560, 590
a.add(a.box(PX, 160, PW, 300, a.WHITE, a.LINE, rx=18))
a.add(a.text(PX + 24, 196, "Lo que cambia en la web", 20, a.INK, a.HEAD, 600))
a.add(a.text(PX + 24, 236, "Setting > Key/Display > Theme", 15, a.GREY, a.MONO, 600))
when(a, a.pill(PX + 24, 248, "Building", a.INK, a.SLATE, 16, 30), 0, 75, still=1)
when(a, a.pill(PX + 24, 248, "Gate Mode", a.AMB, a.AMBBG, 16, 30), 75, 100, still=0)
a.add(a.text(PX + 24, 316, "Key In Homepage Of The Building Theme", 15, a.GREY, a.MONO, 600))
a.add(a.text(PX + 24, 337, "página de inicio (X915: Default Page · R29: Display Type)", 15, a.TXT, a.SANS, 600))
when(a, a.pill(PX + 24, 350, "Home Page", a.INK, a.SLATE, 16, 30), 0, 25, still=0)
when(a, a.pill(PX + 24, 350, "Tenants (directorio)", a.WHITE, a.BLUE, 16, 30), 25, 50, still=1)
when(a, a.pill(PX + 24, 350, "PIN (teclado)", a.WHITE, a.BLUE, 16, 30), 50, 75, still=0)
when(a, a.text(PX + 24, 372, "no aplica fuera de Building", 15, a.GREY, a.SANS, 600), 75, 100, still=0)
when(a, a.text(PX + 24, 428, "Edificio con visitas: directorio.", 17, a.OK, a.SANS, 600), 25, 50, still=1)
when(a, a.text(PX + 24, 428, "Acceso de personal: teclado.", 17, a.OK, a.SANS, 600), 50, 75, still=0)
when(a, a.text(PX + 24, 428, "Sin nube, este theme no tiene qué mostrar.", 17, a.BAD, a.SANS, 600), 75, 100, still=0)

# tiempo 4: el mismo theme con SmartPlus
when(a, a.box(PX, 480, PW, 120, a.OKBG, a.OK, rx=16) +
     a.text(PX + 24, 516, "Con SmartPlus: portero en el área pública de la comunidad.", 17, a.INK, a.SANS, 600) +
     a.text(PX + 24, 544, "Muestra los edificios y apartamentos cargados en la nube.", 16, a.TXT, a.SANS, 600) +
     a.text(PX + 24, 572, "En una obra local: Villa, Building o Default.", 16, a.TXT, a.SANS, 600), 78, 100, still=0)
when(a, a.text(PX, 530, "La página de inicio se elige dentro del theme Building, en la web del portero.", 17, a.INK, a.SANS, 600), 0, 78, still=1)

out(a, 44, 1, "Del directorio al teclado, y un theme que pide nube",
    "Animación con un portero táctil esquemático a la izquierda y, a la derecha, los ajustes de la web. "
    "Tiempo 1: theme Building con la página de inicio Home Page: recuadro de rostro y cuatro íconos (PIN, Llamar, Directorio y Recepción). "
    "Tiempo 2: la página de inicio pasa a Tenants y el portero arranca en el directorio; la visita toca el apartamento 201 y aparece Llamando a 201. "
    "Tiempo 3: la página de inicio pasa a PIN y el portero arranca en el teclado; con el código correcto, el relé A abre. "
    "Tiempo 4: el theme pasa a Gate Mode en una obra sin SmartPlus y la pantalla queda sin edificios para mostrar, marcada en ámbar; "
    "un recuadro verde explica que con el portero en el área pública de una comunidad de SmartPlus aparecen los edificios y apartamentos de la nube, y que en una obra local conviene Villa, Building o Default.",
    [12, 40, 65, 88])
