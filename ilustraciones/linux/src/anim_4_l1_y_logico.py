#!/usr/bin/env python3
"""Lección 4 · Laboratorio, paso 3 (y el 4): sshd -t && ... El segundo comando corre solo si el primero terminó
con código 0. Con la configuración bien, sshd -t no dice nada y termina en 0; con un error, avisa archivo y línea y
termina con un código distinto de 0, y lo que va después de && no se ejecuta (el reload no corre y el servicio sigue
con la configuración anterior). Fuentes: manual de bash (listas con &&), sshd(8) (-t: modo de prueba) y la lección."""
from _anims_lnx_rl import *

a = nueva(24, "LINUX · VALIDAR · LABORATORIO", "&&: el segundo comando espera el visto bueno")
a.steps([
    "sshd -t lee la configuración, no dice nada y termina con código 0.",
    "&& deja pasar: echo \"config OK\" se ejecuta.",
    "Con yess, sshd -t avisa archivo y línea y termina distinto de 0.",
    "&& corta: el reload no corre y SSH sigue con lo anterior.",
], still=3)


def carril(y, titulo, cmd2, ok, t0):
    a.add(a.text(48, y - 66, titulo, 16, a.OK if ok else a.BAD, a.SANS, 700))
    a.add(a.box(48, y - 40, 250, 80, a.INK, None, rx=14) + mono(a, 70, y + 8, "sudo sshd -t", 17, "#FFFFFF", 700))
    a.add(a.box(860, y - 40, 292, 80, a.WHITE, "#C2D4E6", rx=14) + mono(a, 880, y + 8, cmd2, 16, a.INK, 700))
    a.add(linea(298, y, 560, y, a.LINE, 4) + linea(620, y, 860, y, a.LINE, 4))
    # compuerta
    a.add(a.box(560, y - 46, 60, 92, a.SLATE, "#C2D4E6", rx=12) + mono(a, 590, y + 7, "&&", 20, a.INK, 700, "middle"))
    code = "código 0" if ok else "código ≠ 0"
    col = a.OK if ok else a.BAD
    viaje(a, code, [(380, y), (500, y)], t0 + 4, t0 + 9, bg=col, size=14, hold=40)
    if ok:
        en(a, a.box(560, y - 46, 60, 92, a.OKBG, a.OK, rx=12, sw=3) + mono(a, 590, y + 7, "&&", 20, a.OK, 700, "middle"), t0 + 26, 100, still=1)
        viaje(a, "", [(620, y), (860, y)], t0 + 28, t0 + 32, inner=f'<circle r="10" fill="{a.OK}"/>', hold=0)
        en(a, a.box(860, y - 40, 292, 80, a.OKBG, a.OK, rx=14, sw=3) + mono(a, 880, y + 8, cmd2, 16, a.OK, 700), t0 + 32, 100, still=1)
        en(a, a.text(860, y + 66, "corre: imprime config OK", 15, a.OK, a.SANS, 700), t0 + 33, 100, still=1)
    else:
        en(a, a.box(560, y - 46, 60, 92, a.BADBG, a.BAD, rx=12, sw=3) + mono(a, 590, y + 7, "&&", 20, a.BAD, 700, "middle")
           + linea(572, y - 34, 608, y + 34, a.BAD, 4), t0 + 30, 100, still=1)
        en(a, a.box(860, y - 40, 292, 80, a.SLATE, None, rx=14) + mono(a, 880, y + 8, cmd2, 16, a.GREY, 700)
           + linea(870, y, 1142, y, a.BAD, 3), t0 + 32, 100, still=1)
        en(a, a.text(860, y + 66, "no corre: SSH sigue como estaba", 15, a.BAD, a.SANS, 700), t0 + 33, 100, still=1)
    fijo(a, place(pill_c(a, code, "#FFFFFF", col, 14), 500, y))


carril(282, "Configuración bien", 'echo "config OK"', True, 0)
carril(470, "Con PasswordAuthentication yess", "sudo systemctl reload ssh", False, 46)

# salidas de sshd -t
en(a, a.text(48, 350, "sshd -t: sin salida", 15, a.TXT, a.MONO, 600), 4, 100, still=1)
en(a, a.box(48, 528, 780, 34, a.BADBG, None, rx=8) + a.text(60, 551, '/etc/ssh/sshd_config.d/10-ies.conf line 2: unsupported option "yess".', 15, a.BAD, a.MONO, 600), 50, 100, still=1)

narr(a, [
    (0, 25, "Cada comando termina con un código: 0 es que salió bien.", None),
    (25, 50, "Con &&, lo de la derecha corre solo si lo de la izquierda dio 0.", a.OK),
    (50, 75, "El validador lee como el servicio: te dice el archivo y la línea del error.", a.BAD),
    (75, 100, "Corregís, validás otra vez, y recién con 0 se recarga.", a.OK),
], still_idx=3)

escribir(a, "4-l1", "&&: el segundo comando espera el visto bueno",
         "Animación en cuatro tiempos con dos carriles, cada uno con sudo sshd -t a la izquierda, una compuerta && en el medio y el comando siguiente a la derecha. "
         "Arriba, con la configuración bien: 1: sshd -t no dice nada y su código 0 viaja hasta la compuerta. 2: la compuerta se pone verde y echo \"config OK\" se ejecuta. "
         "Abajo, con PasswordAuthentication yess: 3: sshd -t imprime /etc/ssh/sshd_config.d/10-ies.conf line 2: unsupported option \"yess\" y su código distinto de 0 viaja hasta la compuerta. "
         "4: la compuerta se cierra en rojo, sudo systemctl reload ssh queda tachado, no corre, y SSH sigue con la configuración anterior.",
         [10, 36, 62, 92])
