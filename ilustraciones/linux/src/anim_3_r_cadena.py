#!/usr/bin/env python3
"""Lección 3 (Actualizar con método), Resumen: lo que viaja entre el servidor y el repositorio.
apt update baja InRelease (el índice firmado) y verifica la firma con la llave de Signed-By; baja las listas
Packages, cuya suma SHA256 figura en InRelease; apt upgrade baja cada .deb y lo compara con la suma de Packages,
dpkg lo instala y todo queda en /var/log/apt/history.log. Fuentes: teoría de la lección (listas firmadas,
Signed-By, history.log) y la documentación de APT sobre repositorios firmados (InRelease, sumas de Packages)."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · APT · EN LA RED", "apt update y upgrade: una cadena de confianza")
a.steps([
    "apt update pide InRelease: el índice firmado del repositorio.",
    "Verifica la firma con la llave de Signed-By: si no coincide, no sigue.",
    "Baja las listas Packages: su SHA256 tiene que ser el que dice InRelease.",
    "apt upgrade baja cada .deb, lo compara con Packages y dpkg lo instala.",
], still=3)

S, R = 440, 1030
a.add(dev(a, S - 130, 166, 260, 72, "Servidor", "apt · Debian 13", "server", dark=True))
a.add(dev(a, R - 122, 166, 244, 72, "deb.debian.org", "repositorio", "globe"))
a.add(lifeline(a, S, 238, 520))
a.add(lifeline(a, R, 238, 520))

msg(a, S, R, 268, "GET trixie/InRelease", 3, still=1, lsize=15)
msg(a, R, S, 298, "InRelease · firmado", 9, color=a.CYAN, still=1, lsize=15)
msg(a, S, R, 386, "GET .../Packages.xz", 51, still=1, lsize=15)
msg(a, R, S, 416, "Packages.xz", 56, color=a.CYAN, still=1, lsize=15)
msg(a, S, R, 476, "GET openssl_..._amd64.deb", 76, still=1, lsize=15)
msg(a, R, S, 506, ".deb", 81, color=a.CYAN, still=1, lsize=15)

# panel de verificación (cadena)
PX, PW = 48, 340
a.add(a.box(PX, 252, PW, 268, a.WHITE, a.LINE, rx=16) + a.text(PX + 20, 284, "Qué comprueba apt", 17, a.INK, a.HEAD, 600))
ROWS = [(300, "1 · firma de InRelease", "con la llave de Signed-By", 30), (370, "2 · SHA256 de Packages", "contra lo que dice InRelease", 60), (440, "3 · SHA256 del .deb", "contra lo que dice Packages", 85)]
for y, t, s, t0 in ROWS:
    a.add(a.box(PX + 16, y, PW - 32, 60, a.SLATE, None, rx=10) + a.text(PX + 32, y + 26, t, 15, a.INK, a.MONO, 700)
          + a.text(PX + 32, y + 48, s, 15, a.TXT, a.SANS, 500))
    en(a, a.box(PX + 16, y, PW - 32, 60, a.OKBG, a.OK, rx=10, sw=2) + a.text(PX + 32, y + 26, t, 15, a.OK, a.MONO, 700)
       + a.text(PX + 32, y + 48, s, 15, a.INK, a.SANS, 500) + marca(a, PX + PW - 40, y + 30, True, 13), t0, 100, still=1)
# llave (paso 2)
en(a, a.box(S + 24, 312, 470, 42, a.OKBG, a.OK, rx=10) + glyph(a, "key", S + 36, 317, a.OK, 1.3)
   + a.text(S + 76, 339, "Signed-By: debian-archive-keyring.gpg", 15, a.OK, a.MONO, 700), 27, 100, still=1)
en(a, a.text(S + 24, 440, "suma igual a la de InRelease", 15, a.OK, a.SANS, 700), 60, 100, still=1)
en(a, a.text(S + 24, 530, "suma igual a la de Packages → dpkg instala", 15, a.OK, a.SANS, 700), 86, 100, still=1)

# terminal
TY = 548
a.add(tterm(a, 48, TY, 1104, 58))
def cmd(s, t0, t1, still=0, com=None, col=None):
    inner = trow(a, 48, TY + 36, s if col is None else (s, col), 15)
    if com:
        inner += a.text(1136, TY + 36, com, 15, T_COM, a.MONO, 500, "end")
    en(a, inner, t0, t1, still)


cmd("$ sudo apt update", 0, 25, 0, "Get: ... trixie InRelease")
cmd("$ sudo apt update", 25, 50, 0, "sin firma válida: error, no sigue")
cmd("$ apt-get -s upgrade | grep ^Inst", 50, 75, 0, "-s simula: lista lo que instalaría")
cmd("history.log · Upgrade: openssl:amd64 (versión vieja, versión nueva)", 75, 100, 1, col=T_OK)

narr(a, [
    (0, 25, "update no instala nada: solo actualiza lo que el equipo sabe que existe.", None),
    (25, 50, "La firma prueba que el índice viene del repositorio y nadie lo cambió.", a.OK),
    (50, 75, "Cada eslabón lleva la suma del siguiente: alcanza con confiar en una llave.", a.OK),
    (75, 100, "Lo instalado queda en /var/log/apt/history.log: qué, cuándo y con qué comando.", None),
], y=642, still_idx=3)

escribir(a, "3-r1", "apt update y upgrade: una cadena de confianza",
         "Animación en cuatro tiempos en forma de diagrama de secuencia entre el servidor con apt, Debian 13, y el repositorio deb.debian.org; a la izquierda, un panel con lo que comprueba apt y, abajo, una terminal. "
         "1: apt update pide trixie/InRelease y el repositorio devuelve el índice firmado. "
         "2: apt verifica la firma con la llave de Signed-By, debian-archive-keyring.gpg, y se marca en verde el eslabón 1; sin firma válida da error y no sigue. "
         "3: pide Packages.xz y su suma SHA256 coincide con la que figura en InRelease, eslabón 2. "
         "4: apt upgrade pide el .deb de openssl, su SHA256 coincide con la de Packages, eslabón 3, dpkg lo instala y history.log registra el Upgrade de openssl.",
         [10, 38, 66, 92])
