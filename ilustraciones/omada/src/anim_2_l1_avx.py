#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 1: el chequeo de AVX. Con AVX, imagen 6.x; sin AVX, el MongoDB del 6.x
no arranca, el contenedor se cae y restart: unless-stopped lo vuelve a levantar una y otra vez."""
from _anim_om_red import *

a = nueva(24, "HOST DEDICADO", "Antes del compose: ¿la CPU tiene AVX?", "l")
F = a.steps([
    "En la VM, grep busca la bandera avx entre las que la CPU declara en /proc/cpuinfo.",
    "Imprime avx: la CPU la tiene. Imagen mbentley/omada-controller:6.2 y seguís.",
    "No imprime nada: el echo avisa SIN AVX. El MongoDB del controlador 6.x la necesita.",
    "Si igual levantás la 6.x: MongoDB no arranca, el contenedor cae y vuelve a caer.",
], still=3)

# terminal
TX, TY, TW = 48, 186, 560
a.add(a.box(TX, TY, TW, 250, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 32, "VM Linux · terminal", 15, SKY, a.MONO))
a.add(a.text(TX + 20, TY + 72, "$ grep -o -m1 avx /proc/cpuinfo \\", 15, a.WHITE, a.MONO))
a.add(a.text(TX + 20, TY + 96, '    || echo "SIN AVX: usar', 15, a.WHITE, a.MONO))
a.add(a.text(TX + 20, TY + 120, '    mbentley/omada-controller:5"', 15, a.WHITE, a.MONO))
at(a, a.text(TX + 20, TY + 168, "avx", 17, MINT, a.MONO, 600), 28, 50)
at(a, a.text(TX + 20, TY + 168, "SIN AVX: usar mbentley/omada-controller:5", 15, GOLD, a.MONO, 600), 53, 100, still=1)
# cursor de lectura en fase 1
at(a, a.box(TX + 20, TY + 186, 300, 34, "#0B3A66", rx=8) + a.text(TX + 34, TY + 209, "flags: fpu vme ... sse4_2 ...", 15, SKY, a.MONO), 3, 25)

# CPU y resultado
a.add(dev(a, 660, 186, 230, 92, "CPU de la VM", "/proc/cpuinfo", icon="bolt"))
at(a, chip(a, 775, 292, "tiene AVX", a.OK, a.OKBG, anchor="middle", stroke=a.OK), 27, 50)
at(a, chip(a, 775, 292, "sin AVX", a.BAD, a.BADBG, anchor="middle", stroke=a.BAD), 52, 100, still=1)
travel(a, dot(a, a.CYAN), [(608, 260), (660, 232)], 5, 9, hold=0.5)
for t0 in (12, 18):
    travel(a, dot(a, SKY, 7), [(660, 240), (608, 290)], t0, t0 + 3, hold=0.3)

# camino OK (fase 2)
OKP = (dev(a, 930, 186, 222, 92, "Imagen 6.2", "compose", icon="server", dark=True)
       + a.arrow("M890 232 H924", a.OK, 3))
at(a, OKP, 27, 50)
at(a, note(a, 660, 340, 492, 96, "Seguí con el paso 2", ["El 6.x arranca con unos 1,9 GB de RAM:", "conviene dejarle 4 GB libres."], "ok"), 30, 50)

# camino sin AVX (fases 3 y 4)
at(a, note(a, 660, 340, 492, 96, "Dos caminos", ["La imagen de la rama 5, o un equipo más", "nuevo (mini PC Intel de 6.ª generación o más)."], "amb"), 54, 75)
# bucle de reinicio
LY = 470
LOOP = (dev(a, 48, LY, 330, 92, "omada-controller:6.2", "restart: unless-stopped", icon="server")
        + dev(a, 430, LY, 300, 92, "MongoDB", "pide AVX", icon="server", dark=True))
at(a, LOOP, 76, 100, still=1)
at(a, a.arrow("M378 500 H424", a.BLUE, 3), 78, 100, still=1)
at(a, a.arrow("M430 548 C 400 600, 260 600, 220 568", a.BAD, 3), 82, 100, still=1)
at(a, a.text(320, 616, "no arranca, se cae", 15, a.BAD, a.SANS, 600, "middle"), 82, 100, still=1)
at(a, a.arrow("M120 562 C 80 610, 40 560, 70 470", a.AMB, 3, "6 5"), 86, 100, still=1)
at(a, a.text(116, 616, "lo vuelve a levantar", 15, a.AMB, a.SANS, 600, "middle"), 86, 100, still=1)
at(a, xmark(a, 704, 470, 13), 82, 100, still=1)
at(a, note(a, 770, LY, 382, 120, "En una VM", ["El hipervisor tiene que pasarle AVX al", "invitado: si la VM no la ve, el grep", "tampoco, aunque el servidor la tenga."], "info"), 78, 100, still=1)
for t0 in (79, 89):
    travel(a, dot(a, a.BLUE, 7), [(378, 500), (430, 500)], t0, t0 + 2, hold=0.2)

write(a, 2, "l1", "El chequeo de AVX antes de levantar el controlador 6.x",
      "Animación en cuatro tiempos con la terminal de la VM, la CPU y el contenedor. "
      "1: grep -o -m1 avx /proc/cpuinfo busca la bandera avx entre las que declara la CPU; si no la encuentra, el echo avisa que hay que usar la imagen de la rama 5. "
      "2: imprime avx, la CPU la tiene y se sigue con mbentley/omada-controller:6.2 y el compose del paso 2; el 6.x arranca con unos 1,9 GB de RAM y conviene dejarle 4 GB libres. "
      "3: no imprime nada y el echo avisa SIN AVX; quedan dos caminos: la imagen de la rama 5 o un equipo más nuevo, como una mini PC Intel de sexta generación o posterior. "
      "4: si igual se levanta la 6.x, el MongoDB que pide AVX no arranca, el contenedor se cae y restart: unless-stopped lo vuelve a levantar una y otra vez. "
      "En una VM, el hipervisor tiene que pasarle AVX al invitado.",
      [8, 36, 62, 92])
