#!/usr/bin/env python3
"""Lección 3 · Laboratorio, paso 2: qué toma unattended-upgrades. En Ubuntu, 50unattended-upgrades trae
Allowed-Origins con el pocket del release y -security habilitados y -updates comentado; un repositorio agregado
a mano no entra si no se suma su origen. 20auto-upgrades con dos "1" lo activa una vez por día.
Fuentes: teoría de la lección (aplica solo seguridad; 20auto-upgrades y 50unattended-upgrades; un repositorio
agregado a mano no entra si no sumás su origen) y el 50unattended-upgrades de Ubuntu (Allowed-Origins)."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · ACTUALIZACIONES · LABORATORIO", "unattended-upgrades: qué toma y qué deja")
a.steps([
    "Hay tres actualizaciones pendientes, de tres orígenes distintos.",
    "50unattended-upgrades dice qué orígenes se aplican solos.",
    "openssl, de -security, se instala; las otras dos esperan.",
    "20auto-upgrades con dos \"1\" lo corre una vez por día; el log lo cuenta.",
], still=2)

CARDS = [("openssl", "${distro_codename}-security", a.OK, 190), ("nano", "${distro_codename}-updates", a.AMB, 290), ("app-terceros", "repositorio agregado a mano", a.AMB, 390)]
for n, o, c, y in CARDS:
    a.add(a.box(48, y, 360, 80, a.WHITE, "#C2D4E6", rx=14) + mono(a, 68, y + 34, n, 17, a.INK, 700) + mono(a, 68, y + 60, o, 14, a.GREY, 500))
en(a, a.box(40, 182, 376, 296, "none", a.BLUE, rx=18, sw=3), 3, 25)
a.add(a.text(48, 176 - 10, "pendientes (ejemplo, Ubuntu)", 15, a.GREY, a.SANS, 600))

# filtro
FX, FY, FW, FH = 430, 190, 408, 280
a.add(a.box(FX, FY, FW, FH, a.INK, None, rx=16) + a.text(FX + 20, FY + 32, "50unattended-upgrades", 17, "#FFFFFF", a.HEAD, 600))
a.add(mono(a, FX + 20, FY + 64, "Allowed-Origins {", 14, LIGHT, 500))
OL = [('"${distro_id}:${distro_codename}";', "#FFFFFF"), ('"${distro_id}:${distro_codename}-security";', MINT),
      ('//"${distro_id}:${distro_codename}-updates";', "#7FA6C9"), ("};   (resumido)", LIGHT)]
for i, (s, c) in enumerate(OL):
    a.add(mono(a, FX + 18 if i < 3 else FX + 14, FY + 92 + i * 26, s, 14, c, 600))
en(a, a.box(FX + 8, FY + 99, FW - 16, 27, "none", GOLD, rx=6, sw=2) + a.box(FX + 8, FY + 125, FW - 16, 27, "none", GOLD, rx=6, sw=2, extra='stroke-dasharray="5 4"'), 27, 50)
en(a, a.text(FX + 20, FY + 220, "// = comentado: no se aplica", 15, GOLD, a.SANS, 700)
   + a.text(FX + 20, FY + 244, "lo que no figura, tampoco", 15, LIGHT, a.SANS, 500), 30, 100, still=1)

# resultados
RX, RW = 852, 300
a.add(a.box(RX, 190, RW, 120, a.OKBG, a.OK, rx=14, sw=2) + a.text(RX + 18, 218, "se instala solo", 17, a.OK, a.HEAD, 600))
a.add(a.box(RX, 330, RW, 140, a.AMBBG, a.AMB, rx=14, sw=2) + a.text(RX + 18, 358, "espera a que lo hagas vos", 17, a.AMB, a.HEAD, 600))
for i, (n, o, c, y) in enumerate(CARDS):
    dest = (RX + RW / 2, 270) if c == a.OK else (RX + RW / 2, 400 + (i - 1) * 40)
    t0 = 52 + i * 6
    viaje(a, "", [(410, y + 40), (FX - 10, y + 40), (FX + FW + 10, dest[1]), dest], t0, t0 + 6,
          inner=pill_c(a, n, "#FFFFFF", c, 15, 32), hold=100)
    fijo(a, place(pill_c(a, n, "#FFFFFF", c, 15, 32), *dest))

# terminal
TY = 492
a.add(tterm(a, 48, TY, 1104, 110))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 32 + i * 26, r, 15) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ apt list --upgradable", ("openssl/...-security   nano/...-updates   app-terceros/...   (resumido)", T_OUT)], 0, 50)
filas([("# lo que se instala solo es lo de -security; el resto, en una ventana tuya", T_COM), ("# un repositorio agregado a mano entra solo si sumás su origen a la lista", T_COM)], 50, 75, still=1)
filas(["$ cat /etc/apt/apt.conf.d/20auto-upgrades", ('APT::Periodic::Update-Package-Lists "1";   APT::Periodic::Unattended-Upgrade "1";', T_OK),
       ("unattended-upgrades.log: Packages that will be upgraded: openssl ...", T_OUT)], 75, 100)

narr(a, [
    (0, 25, "No todas las actualizaciones pesan lo mismo: el origen dice qué son.", None),
    (25, 50, "La lista de orígenes es la que decide; en Ubuntu viene con seguridad.", a.AMB),
    (50, 75, "Seguridad se aplica sola; lo demás queda para hacerlo con método.", a.OK),
    (75, 100, "Si un paquete molesta, se bloquea ese paquete; no se apaga todo.", None),
], y=640, still_idx=2)

escribir(a, "3-l1", "unattended-upgrades: qué toma y qué deja",
         "Animación en cuatro tiempos. A la izquierda, tres actualizaciones pendientes de ejemplo en Ubuntu: openssl de ${distro_codename}-security, nano de ${distro_codename}-updates y app-terceros de un repositorio agregado a mano. "
         "En el medio, el archivo 50unattended-upgrades con Allowed-Origins resumido: el pocket del release, -security habilitado y -updates comentado con //. A la derecha, se instala solo y espera a que lo hagas vos. "
         "1: se marcan las tres pendientes. 2: se marcan las líneas de -security y la de -updates comentada; lo comentado no se aplica y lo que no figura tampoco. "
         "3: openssl pasa el filtro y cae en se instala solo; nano y app-terceros caen en espera; un repositorio agregado a mano entra solo si se suma su origen. "
         "4: 20auto-upgrades tiene Update-Package-Lists y Unattended-Upgrade en 1, y el log de unattended-upgrades dice Packages that will be upgraded: openssl.",
         [10, 38, 66, 90])
