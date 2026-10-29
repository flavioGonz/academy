#!/usr/bin/env python3
"""IVR que solo anuncia · Laboratorio, paso 3: 20-l1.svg.
El 5 que el IVR recoge: en el banco lo marcás en la 1001 y llega como evento RFC 4733; en la obra lo
inventa el detector del FXO con ruido o eco que parece 770 + 1336 Hz (la tecla 5). Con Dial Other Extensions
prendido, el IVR espera el Digit Timeout (3 s de fábrica), busca el interno 5, no existe y suena el
Invalid Input Prompt; con repeticiones en 3, es la vuelta 1 de 3.
"""
from _anim_gs_red import R

g = R(T=26, fix=90, kicker="GRANDSTREAM · IVR QUE SOLO ANUNCIA · PASO 3", title="Un 5 en medio de la bienvenida")
g.steps([
    "En el banco: marcás 5 en la 1001 y viaja como evento RFC 4733 hasta el IVR.",
    "En la obra, el 5 lo inventa el FXO: ruido o eco que parece 770 + 1336 Hz.",
    "Con Dial Other Extensions prendido, espera más dígitos: Digit Timeout, 3 s.",
    "El interno 5 no existe: Invalid Input Prompt, vuelta 1 de 3.",
], size=17)

B, OK, BAD, AMB, GREY, INK = g.BLUE, g.OK, g.BAD, g.AMB, g.GREY, g.INK
XA, XI, XF = 150, 420, 690
g.lane(XA, 170, 500, "Interna 1001", "en el banco", w=220)
g.lane(XI, 170, 500, "IVR 7000", "bienvenida", w=220)
g.lane(XF, 170, 500, "FXO1 · línea", "en la obra", w=220)

# 1 · RFC 4733 desde la 1001
g.msg(XA, XI, 270, "RFC 4733 · evento 5", B, 3, 10, hold=25, tok="5", still=0)
# 2 · el FXO inventa el 5
g.appear(g.pillc(XF, 300, "ruido · eco", AMB, g.AMBBG, 14, 28), 27, 50, still=0)
g.appear(g.pillc(XF, 340, "770 + 1336 Hz", AMB, g.AMBBG, 14, 28), 31, 50, still=0)
g.msg(XF, XI, 396, "detector del FXO: 5", AMB, 36, 42, hold=100, tok="5")
# 4 · el aviso vuelve a quien llama
g.msg(XI, XF, 456, "«Lo siento, no lo entiendo»", BAD, 80, 86, hold=100)

# panel: lo que hace el IVR
PX, PY, PW = 832, 176, 320
g.add(g.box(PX, PY, PW, 324, g.WHITE, g.LINE, rx=14))
g.add(g.text(PX + 20, PY + 32, "Lo que hace el IVR", 17, INK, g.SANS, 600))
rows = [("Dial Other Extensions", "Extension, Ring Group", AMB, 0, 100),
        ("dígitos recibidos", "5", INK, 10, 100),
        ("Digit Timeout", "", INK, 0, 100),
        ("busca el interno 5", "no existe", BAD, 66, 100),
        ("Invalid Input Prompt", "vuelta 1 de 3", BAD, 78, 100)]
for i, (lab, val, col, t0, t1) in enumerate(rows):
    y = PY + 66 + i * 52
    g.add(g.text(PX + 20, y, lab, 14, GREY, g.SANS, 400))
    if val:
        g.appear(g.text(PX + 20, y + 22, val, 16, col, g.MONO, 600), t0, t1)
# Digit Timeout: barra de 3 s
DY = PY + 66 + 2 * 52 + 8
g.add(g.box(PX + 20, DY, 200, 18, g.SLATE, rx=6))
g.bar(PX + 20, DY, 200, 18, 52, 66, GREY)
g.appear(g.text(PX + 232, DY + 15, "3 s", 15, INK, g.MONO, 600), 66, 100)
g.appear(g.box(PX + 10, PY + 66 + 3 * 52 - 20, PW - 20, 50, "none", BAD, rx=10, sw=2.5), 66, 78, still=0)

# abajo
g.add(g.box(48, 534, 1104, 92, g.WHITE, g.LINE, rx=14))
g.add(g.text(72, 572, "En el banco el 5 lo marcás vos; en la obra lo inventa la línea.", 17, INK, g.SANS, 600))
g.add(g.text(72, 604, "El IVR no distingue uno del otro: los dos terminan en el aviso de inválido.", 17, BAD, g.SANS, 600))

g.done(20, "l1", "Un 5 en medio de la bienvenida",
       "Animación en cuatro tiempos con tres columnas: la interna 1001 en el banco, el IVR 7000 y el FXO1 con la línea en la obra; a la derecha, lo que hace el IVR. "
       "1: en el banco, marcás 5 en la 1001 durante la bienvenida y la tecla viaja como evento RFC 4733 hasta el IVR. "
       "2: en la obra, el 5 lo inventa el detector del FXO: ruido o eco de la línea que parece la mezcla de 770 y 1336 hercios, los tonos de la tecla 5, y el FXO se lo pasa al IVR. "
       "3: con Dial Other Extensions en Extension y Ring Group, el IVR guarda el 5 y espera más dígitos durante el Digit Timeout de 3 segundos. "
       "4: busca el interno 5, no existe, y le manda a quien llama el Invalid Input Prompt, Lo siento, no lo entiendo; con repeticiones en 3, es la vuelta 1 de 3. "
       "Abajo: en el banco el 5 lo marcás vos y en la obra lo inventa la línea, pero el IVR no distingue uno del otro.",
       [7, 22, 38, 46, 60, 72, 84, 95])
