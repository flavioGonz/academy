#!/usr/bin/env python3
"""Lección 1 · Laboratorio, paso 2: find /etc -name "*sshd*" 2>/dev/null. Lo que coincide sale por la salida
estándar (canal 1); el aviso de una carpeta que no se puede leer sale por el canal de errores (canal 2).
Sin redirección los dos llegan a la pantalla; con 2>/dev/null el canal 2 va al descarte.
Fuentes: teoría de la lección (tres canales, 2>/dev/null descarta los errores) y la documentación de GNU find."""
from _anims_lnx_rl import *

a = nueva(24, "LINUX · CANALES · LABORATORIO", "Resultados por un canal, errores por otro")
a.steps([
    "find recorre /etc: lo que coincide sale por el canal 1, a la pantalla.",
    "Una carpeta protegida no se puede leer: el aviso sale por el canal 2.",
    "Sin redirección, los dos canales terminan mezclados en la pantalla.",
    "Con 2>/dev/null, el canal 2 va al descarte: quedan los resultados.",
], still=3)

# ---- carpetas que recorre
a.add(a.text(48, 190, "lo que recorre (usuario común)", 15, a.GREY, a.SANS, 600))
DIRS = [("/etc/pam.d", True, 4), ("/etc/ssh", True, 12), ("/etc/ssl/private", False, 28), ("/etc/sudoers.d", False, 38)]
for i, (d, ok, t) in enumerate(DIRS):
    y = 206 + i * 58
    a.add(a.box(48, y, 270, 46, a.WHITE, a.LINE, rx=10) + mono(a, 66, y + 29, d, 15, a.INK, 600))
    a.add(marca(a, 294, y + 23, ok, 13))
    for t0 in ((t, t + 9), (t * 0.4 + 76, t * 0.4 + 82)):
        en(a, a.box(48, y, 270, 46, "none", a.OK if ok else a.BAD, rx=10, sw=3), t0[0], t0[1])
a.add(a.text(48, 460, "sin permiso de lectura:", 15, a.GREY, a.SANS, 500) + a.text(48, 482, "find no puede entrar", 15, a.GREY, a.SANS, 500))

# ---- proceso find
a.add(dev(a, 360, 246, 190, 120, "find", "salida y errores", None, dark=True, sub2="por separado"))
a.add(a.pill(560, 262, "1 salida", a.BLUE, "#E5F0FB", 14, 26))
a.add(a.pill(560, 334, "2 errores", a.BAD, a.BADBG, 14, 26))

# caminos
C1 = [(600, 290), (660, 290)]
C2s = [(600, 362), (640, 362), (640, 420), (660, 420)]
C2n = [(600, 362), (640, 362), (640, 560), (742, 560)]
a.add(camino("M650 290 H664", a.BLUE, 3))
en(a, camino("M640 362 V420 H664", a.BAD, 3, "7 5"), 26, 75)
en(a, camino("M640 362 V560 H742", a.BAD, 3, "7 5"), 75, 100, still=1)
a.add(camino("M600 362 H640", a.BAD, 3, "7 5"))

# ---- pantalla
TX, TY, TW, TH = 664, 176, 488, 300
a.add(tterm(a, TX, TY, TW, TH, "PANTALLA"))
en(a, trow(a, TX, TY + 54, '$ find /etc -name "*sshd*"', 15), 0, 75)
en(a, trow(a, TX, TY + 54, '$ find /etc -name "*sshd*" 2>/dev/null', 15), 75, 100, still=1)
R = [("/etc/pam.d/sshd", T_OUT, 8), ("/etc/ssh/sshd_config", T_OUT, 16), ("/etc/ssh/sshd_config.d", T_OUT, 22),
     ("find: ‘/etc/ssl/private’: Permission denied", T_ERR, 33), ("find: ‘/etc/sudoers.d’: Permission denied", T_ERR, 43)]
for i, (s, c, t) in enumerate(R):
    en(a, trow(a, TX, TY + 90 + i * 30, (s, c), 15), t, 75)
for i, (s, c, t) in enumerate(R[:3]):
    en(a, trow(a, TX, TY + 90 + i * 30, (s, c), 15), 77 + i * 3, 100, still=1)
en(a, a.box(TX + 8, TY + 160, TW - 16, 62, "none", GOLD, rx=8, sw=2), 52, 75)
a.add(a.text(TX, TY + TH + 24, "ejemplo: el orden depende de cómo find encuentra las carpetas", 15, a.GREY, a.SANS, 500))

# ---- /dev/null
a.add(a.box(742, 530, 220, 60, a.SLATE, "#C2D4E6", rx=12) + mono(a, 762, 566, "/dev/null", 17, a.INK, 700))
a.add(a.text(980, 556, "lo que entra", 15, a.GREY, a.SANS, 500) + a.text(980, 578, "se descarta", 15, a.GREY, a.SANS, 500))

# ---- viajes
for s, c, t in R[:3]:
    viaje(a, "", C1, t - 3.5, t - 0.5, inner=f'<circle r="9" fill="{a.BLUE}"/>', hold=0)
for s, c, t in R[3:]:
    viaje(a, "", C2s, t - 4, t - 0.5, inner=f'<circle r="9" fill="{a.BAD}"/>', hold=0)
for i in range(3):
    viaje(a, "", C1, 74.5 + i * 3, 76.8 + i * 3, inner=f'<circle r="9" fill="{a.BLUE}"/>', hold=0)
for t in (86, 92):
    viaje(a, "", C2n, t - 4, t, inner=f'<circle r="9" fill="{a.BAD}"/>', hold=0.5)
fijo(a, f'<circle cx="742" cy="560" r="9" fill="{a.BAD}"/>')

narr(a, [
    (0, 25, "Cada resultado es una línea con la ruta completa.", None),
    (25, 50, "Permission denied no es una falla del comando: es una carpeta que tu usuario no puede leer.", a.AMB),
    (50, 75, "Con muchas carpetas protegidas, los resultados se pierden entre los avisos.", a.BAD),
    (75, 100, "2> redirige solo el canal 2: los resultados siguen llegando a la pantalla.", a.OK),
], still_idx=3)

escribir(a, "1-l1", "Resultados por un canal, errores por otro",
         "Animación en cuatro tiempos. A la izquierda, cuatro carpetas que find recorre como usuario común: /etc/pam.d y /etc/ssh, que se pueden leer, y /etc/ssl/private y /etc/sudoers.d, que no. "
         "En el medio, el proceso find con dos salidas: canal 1, salida, y canal 2, errores. A la derecha, la pantalla y, abajo, /dev/null. "
         "1: los resultados /etc/pam.d/sshd, /etc/ssh/sshd_config y /etc/ssh/sshd_config.d viajan por el canal 1 y aparecen en la pantalla. "
         "2: al llegar a las carpetas protegidas, find: Permission denied viaja por el canal 2. "
         "3: sin redirección, los dos avisos quedan mezclados con los resultados en la pantalla. "
         "4: con 2>/dev/null en el comando, los avisos viajan a /dev/null y la pantalla muestra solo las tres rutas.",
         [9, 36, 62, 92])
