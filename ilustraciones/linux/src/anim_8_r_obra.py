#!/usr/bin/env python3
"""Lección 8 (Deny por defecto), Resumen: el servidor de la obra con ufw en deny entrante, allow saliente y SSH
solo desde la red de gestión. SSH desde 10.10.10.25 pasa; desde una PC de la LAN cae en deny y no recibe nada;
la respuesta de un apt update vuelve por established; postgres en 127.0.0.1 no se alcanza desde la red.
Fuentes: teoría y laboratorio de la lección (ufw default deny incoming, allow from 10.10.10.0/24 to any port 22,
established,related, ss -tlnp y 127.0.0.1). Direcciones de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · FIREWALL · EN LA RED", "Deny por defecto: qué pasa con cada conexión")
a.steps([
    "SSH desde la red de gestión, 10.10.10.25: la regla lo deja pasar.",
    "Una PC de la LAN prueba el 22: cae en deny y no recibe nada.",
    "El servidor sale a actualizar y la respuesta vuelve por established.",
    "postgres escucha en 127.0.0.1: desde la red no hay nada que alcanzar.",
], still=1)

a.add(dev(a, 48, 196, 260, 84, "Notebook gestión", "10.10.10.25", "laptop"))
a.add(dev(a, 48, 410, 260, 84, "PC de la LAN", "192.168.88.30", "laptop"))
a.add(dev(a, 920, 300, 232, 84, "Repositorio", "deb.debian.org", "globe"))
# servidor
SX, SY, SW, SH = 420, 172, 400, 350
a.add(a.box(SX, SY, SW, SH, a.WHITE, "#C2D4E6", rx=18) + a.text(SX + 70, SY + 32, "Servidor 192.168.88.50", 17, a.INK, a.HEAD, 600))
# barra del firewall
a.add(a.box(SX + 14, SY + 14, 40, SH - 28, a.NAVY2, None, rx=10))
a.add(f'<text x="{SX + 40}" y="{SY + SH / 2}" font-family="{a.MONO}" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 {SX + 40} {SY + SH / 2})">ufw · deny entrante</text>')
# reglas
a.add(a.box(SX + 70, SY + 48, 310, 82, a.SLATE, None, rx=10) + mono(a, SX + 84, SY + 72, "22/tcp ALLOW IN 10.10.10.0/24", 14, a.OK, 700)
      + mono(a, SX + 84, SY + 96, "default: deny (incoming)", 14, a.BAD, 600) + mono(a, SX + 84, SY + 118, "         allow (outgoing)", 14, a.OK, 600))
# servicios
a.add(a.box(SX + 70, SY + 150, 310, 50, a.WHITE, a.LINE, rx=10) + mono(a, SX + 86, SY + 181, "sshd   0.0.0.0:22", 15, a.INK, 700))
a.add(a.box(SX + 70, SY + 214, 310, 50, a.WHITE, a.LINE, rx=10) + mono(a, SX + 86, SY + 245, "apt    (sale a internet)", 15, a.INK, 700))
a.add(a.box(SX + 70, SY + 278, 310, 50, a.WHITE, a.LINE, rx=10) + mono(a, SX + 86, SY + 309, "postgres 127.0.0.1:5432", 15, a.INK, 700))

FW = SX + 34
# 1 SSH gestión
a.add(camino(f"M308 238 C 360 238, 380 347, {FW} 347", "#C2D4E6", 3))
viaje(a, "SYN :22", [(320, 238), (370, 300), (FW - 30, 347)], 3, 9, bg=a.BLUE, size=13, hold=0.5)
viaje(a, "", [(FW - 4, 347), (SX + 70, 347)], 9.5, 11.5, inner=f'<circle r="9" fill="{a.OK}"/>', hold=0.2)
en(a, a.box(SX + 66, SY + 146, 318, 58, "none", a.OK, rx=12, sw=3), 11, 25)
viaje(a, "SYN-ACK", [(FW - 30, 347), (370, 300), (320, 238)], 13, 19, bg=a.OK, size=13, hold=1)
en(a, marca(a, SX - 2, 330, True, 14), 9, 25)
en(a, a.text(48, 306, "regla 22 desde 10.10.10.0/24: entra", 15, a.OK, a.SANS, 700), 11, 25)
# 2 PC LAN
a.add(camino(f"M308 452 C 360 452, 380 400, {FW} 400", "#C2D4E6", 3))
viaje(a, "SYN :22", [(300, 452), (340, 420), (360, 402)], 28, 34, bg=a.BLUE, size=13, hold=16)
en(a, marca(a, SX - 2, 400, False, 14), 34, 50, still=1)
en(a, a.text(48, 524, "nada coincide: deny, y no vuelve nada", 15, a.BAD, a.SANS, 700) + a.text(48, 546, "ssh espera hasta el timeout", 15, a.TXT, a.SANS, 500), 35, 50, still=1)
fijo(a, place(pill_c(a, "SYN :22", "#FFFFFF", a.BLUE, 13), 360, 402))
# 3 apt
a.add(camino(f"M{SX + SW} 418 C 860 418, 870 342, 920 342", "#C2D4E6", 3))
viaje(a, "", [(SX + 380, SY + 239), (SX + SW + 10, 418), (870, 360), (912, 342)], 53, 58, inner=pill_c(a, "GET (sale)", "#FFFFFF", a.BLUE, 13), hold=0.5)
viaje(a, "", [(912, 342), (870, 360), (SX + SW + 10, 418)], 60, 65, inner=pill_c(a, "respuesta", "#FFFFFF", a.OK, 13), hold=0.5)
en(a, a.text(SX + SW + 20, 470, "established: vuelve", 15, a.OK, a.SANS, 700) + a.text(SX + SW + 20, 492, "porque la pidió él", 15, a.TXT, a.SANS, 500), 62, 75)
en(a, a.box(SX + 66, SY + 210, 318, 58, "none", a.OK, rx=12, sw=3), 56, 75)
# 4 postgres
en(a, a.box(SX + 66, SY + 274, 318, 58, "none", a.AMB, rx=12, sw=3) + a.text(SX + 70, SY + SH + 26, "127.0.0.1 = solo el propio equipo", 15, a.AMB, a.SANS, 700), 76, 100)
en(a, nota(a, 870, 410, 282, 110, "Desde la red, el 5432", ["no tiene nada escuchando en", "192.168.88.50, con o sin", "firewall: no escuchar > filtrar"], "ok", 16, 15), 78, 100)

narr(a, [
    (0, 25, "Lo que el equipo sirve se abre con nombre y origen: SSH, solo desde gestión.", a.OK),
    (25, 50, "Un deny no contesta: del otro lado se ve un timeout, no un rechazo.", a.BAD),
    (50, 75, "El saliente queda permitido y las respuestas entran por la primera regla.", a.OK),
    (75, 100, "La primera capa es no escuchar donde no hace falta; el firewall es la segunda.", None),
], y=640, still_idx=1)

escribir(a, "8-r1", "Deny por defecto: qué pasa con cada conexión",
         "Animación en cuatro tiempos con el servidor 192.168.88.50 en el medio, con ufw en deny entrante, la regla 22/tcp ALLOW IN 10.10.10.0/24, el saliente permitido, y tres servicios: sshd en 0.0.0.0:22, apt y postgres en 127.0.0.1:5432. "
         "A la izquierda, la notebook de gestión 10.10.10.25 y una PC de la LAN 192.168.88.30; a la derecha, el repositorio. "
         "1: el SYN al 22 desde 10.10.10.25 coincide con la regla, entra a sshd y vuelve el SYN-ACK. "
         "2: el SYN al 22 desde la PC de la LAN no coincide con nada, cae en deny y no vuelve nada: ssh espera hasta el timeout. "
         "3: apt sale al repositorio, el saliente está permitido, y la respuesta vuelve por established porque la pidió el servidor. "
         "4: postgres escucha solo en 127.0.0.1: desde la red no hay nada escuchando en 192.168.88.50:5432, con o sin firewall.",
         [10, 40, 62, 90])
