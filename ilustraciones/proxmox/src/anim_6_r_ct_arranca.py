#!/usr/bin/env python3
"""Lección 6 · Resumen, "Cómo se ve en la red": pct start 300. Sin BIOS ni kernel propio: el kernel del host crea los
namespaces y el cgroup y arranca el init del contenedor; la red es un par veth (eth0 adentro, veth300i0 en vmbr0);
con ip=dhcp el contenedor pide su dirección al router de la LAN; en el host sus procesos son procesos comunes.
Fuentes: guía de administración (pct, net0 name=eth0,bridge=vmbr0,ip=dhcp, veth), tarjeta de la lección
(namespaces, cgroups, no privilegiado 0 → 100000), RFC 2131 (DORA)."""
from _anim_pmx_red import *

a = new(24, "Contenedor sin privilegios", "pct start 300: un contenedor arranca en segundos")
a.steps([
    "El kernel del host crea los namespaces y el cgroup y arranca el init.",
    "La red es un par veth: eth0 adentro, veth300i0 enchufado en vmbr0.",
    "ip=dhcp: el contenedor pide su dirección al router de la LAN.",
    "En el host, sus procesos son procesos comunes, con uid 100000.",
], still=1)

# host
HX, HY, HW, HH = 48, 178, 790, 400
a.add(a.box(HX, HY, HW, HH, a.WHITE, a.LINE, rx=18))
a.add(glyph(a, "server", HX + 18, HY + 16))
a.add(a.text(HX + 60, HY + 36, "pve1", 19, a.INK, a.SANS, 600))
# kernel
KY = HY + HH - 82
a.add(a.box(HX + 20, KY, HW - 40, 62, a.INK, rx=12))
a.add(a.text(HX + 40, KY + 26, "kernel Linux del host · uno solo", 16, a.WHITE, a.SANS, 600))
a.add(a.text(HX + 40, KY + 48, "namespaces · cgroups", 15, SKY, a.MONO))
# contenedor
CX, CY, CW, CH = HX + 20, HY + 60, 380, 228
a.add(during(a, a.box(CX, CY, CW, CH, a.WHITE, a.BLUE, rx=14, sw=2.5, extra='stroke-dasharray="9 6"'), 3, 100, still=1))
a.add(during(a, a.text(CX + 18, CY + 30, "CT 300 · ct-prueba", 17, a.INK, a.SANS, 600), 3, 100, still=1))
for i, (lab, t) in enumerate([("pid · su árbol de procesos", 6), ("net · su eth0", 8), ("mnt · su sistema de archivos", 10), ("user · root = 100000 afuera", 12)]):
    a.add(during(a, chip(a, CX + 18, CY + 46 + i * 36, lab, "info", h=28), t, 100, still=1))
a.add(during(a, a.text(CX + 18, CY + 208, "cgroup: memoria 512 MB", 15, a.AMB, a.MONO, 600), 14, 100, still=1))
a.add(during(a, a.text(CX + CW - 18, CY + 30, "init", 15, a.OK, a.MONO, 700, "end"), 16, 100, still=1))
# del kernel al contenedor
for i in range(3):
    a.add(travel(a, f'<circle r="7" fill="{a.CYAN}"/>', [(CX + 190 + i * 40, KY), (CX + 190 + i * 40, CY + CH)], 4 + i * 2, 8 + i * 2, hold=0.2, fade=0.3))
# veth
EX, EY = CX + CW - 26, CY + 120
a.add(during(a, a.box(EX, EY - 18, 52, 36, a.OKBG, a.OK, rx=8, sw=2) + a.text(EX + 26, EY + 6, "eth0", 15, a.OK, a.MONO, 700, "middle"), 25, 100, still=1))
VX = CX + CW + 56
a.add(during(a, line(EX + 52, EY, VX, EY, a.OK, 4) + a.box(VX, EY - 18, 106, 36, a.OKBG, a.OK, rx=8, sw=2) + a.text(VX + 53, EY + 6, "veth300i0", 15, a.OK, a.MONO, 700, "middle"), 28, 100, still=1))
at(a, a.text((EX + 52 + VX) / 2, EY - 28, "par veth", 15, a.OK, a.SANS, 600, "middle"), 28, 50, still=1)
BX = VX + 140
a.add(a.box(BX, HY + 60, 96, 228, a.NAVY2, rx=12) + a.text(BX + 48, HY + 88, "vmbr0", 15, a.WHITE, a.MONO, 600, "middle"))
a.add(during(a, line(VX + 106, EY, BX, EY, a.OK, 4), 30, 100, still=1))
a.add(a.box(BX + 104, EY + 50, 68, 34, a.SLATE, rx=8) + a.text(BX + 138, EY + 73, "eno1", 15, a.INK, a.MONO, 600, "middle"))
a.add(line(BX + 96, EY + 67, BX + 104, EY + 67, a.BLUE, 3))
# router
RX, RY = 880, EY + 67 - 48
a.add(dev(a, RX, RY, 272, 96, "Router de la LAN", "servidor DHCP", icon="globe", sub2="10.10.10.1", tsize=18))
a.add(line(BX + 172, EY + 67, RX, EY + 67, a.BLUE, 3))
P = [(EX + 26, EY), (VX + 53, EY), (BX + 48, EY), (BX + 48, EY + 67), (RX, EY + 67)]
R = list(reversed(P))
go(a, "Discover", P, 53, 58, a.BLUE, hold=0.2)
go(a, "Offer", R, 59, 64, a.OK, hold=0.2)
go(a, "Request", P, 65, 69, a.BLUE, hold=0.2)
go(a, "Ack", R, 70, 74, a.OK, hold=1)
at(a, chip(a, EX + 60, EY + 28, "eth0: 10.10.10.150/24", "ok"), 74, 100)

# panel derecho de abajo: ps en el host / tiempos
TX, TY, TW, TH = 880, 178, 272, 180
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
at(a, tline(a, TX + 16, TY + 32, "# pct start 300", MINT) + tline(a, TX + 16, TY + 58, "sin BIOS, sin kernel", SKY) + tline(a, TX + 16, TY + 82, "propio: arranca en", SKY) + tline(a, TX + 16, TY + 106, "segundos", SKY), 0, 50, still=1)
at(a, tline(a, TX + 16, TY + 32, "esperando la IP...", SKY), 50, 75)
at(a, tline(a, TX + 16, TY + 32, "# ps -eo user,cmd", MINT) + tline(a, TX + 16, TY + 60, "100000 /sbin/init", GOLD) + tline(a, TX + 16, TY + 84, "100000 sshd", GOLD) + tline(a, TX + 16, TY + 108, "root   pvedaemon", a.WHITE) + tline(a, TX + 16, TY + 140, "afuera no es root", SKY), 75, 100)

status(a, 632, [
    (0, 25, "Para el contenedor es una máquina; para el host, procesos con su propia vista del sistema.", a.INK, 0),
    (25, 50, "Lo que sale por eth0 aparece en veth300i0, ya dentro del bridge, como una placa más.", a.OK, 1),
    (50, 75, "En la red, el contenedor es un equipo más: pide IP y contesta como cualquier otro.", a.BLUE, 0),
    (75, 100, "No privilegiado: el root de adentro, en el host, es el usuario 100000.", a.AMB, 0),
])

write(a, 6, "r1", "pct start 300: un contenedor arranca en segundos",
      "Animación en cuatro tiempos con el host pve1, su kernel Linux compartido, el contenedor 300 ct-prueba, el bridge vmbr0, la placa eno1 y el router de la LAN con DHCP en 10.10.10.1. "
      "1: pct start 300 no tiene BIOS ni kernel propio: el kernel del host crea los namespaces (pid, su árbol de procesos; net, su eth0; mnt, su sistema de archivos; user, donde root es 100000 afuera) y el cgroup con 512 MB de memoria, y arranca el init del contenedor en segundos. "
      "2: la red es un par veth: eth0 adentro del contenedor y veth300i0 afuera, enchufado en vmbr0 como una placa más. "
      "3: con ip=dhcp el contenedor manda Discover, el router contesta Offer, el contenedor pide Request y recibe Ack con 10.10.10.150/24. "
      "4: en el host, ps muestra los procesos del contenedor, /sbin/init y sshd, como procesos comunes del usuario 100000: afuera no es root.",
      [10, 36, 62, 76, 92])
