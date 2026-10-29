#!/usr/bin/env python3
"""Lección 9 · Laboratorio, pasos 5 y 6: el QDevice. corosync-qnetd en un tercer equipo, corosync-qdevice en los
nodos, pvecm qdevice setup copia la clave SSH del clúster y arma la conexión cifrada; cada nodo habla por TCP 5403 con
el qnetd y el clúster pasa a esperar 3 votos; con pve2 apagado, pve1 y el QDevice suman 2 de 3.
Fuentes: guía de administración (QDevice-Net Setup, puerto 5403, salida de pvecm status con Qdevice, flags A,V,NMW)."""
from _anim_pmx_red import *

a = new(24, "Tres votos", "QDevice: el tercer voto llega por TCP 5403", lab=True)
a.steps([
    "qnetd en el tercer equipo; corosync-qdevice en los dos nodos.",
    "pvecm qdevice setup: copia la clave del clúster y arma la conexión cifrada.",
    "Cada nodo habla con el qnetd por TCP 5403: el clúster espera 3 votos.",
    "Paso 6: apagás pve2 y pve1 con el QDevice suman 2 de 3. Hay quórum.",
], still=2)

P1, P2, Q = (48, 186), (48, 420), (440, 304)
a.add(dev(a, *P1, 300, 84, "pve1 · 10.10.10.11", "corosync-qdevice", icon="server", dark=True, tsize=18))
at(a, dev(a, *P2, 300, 84, "pve2 · 10.10.10.12", "corosync-qdevice", icon="server", dark=True, tsize=18), 0, 77, still=1)
at(a, a.box(*P2, 300, 84, a.SLATE, a.LINE, rx=14, sw=2, extra='stroke-dasharray="8 6"') + glyph(a, "server", 66, 438, a.GREY)
   + a.text(110, 454, "pve2 · apagado", 18, a.GREY, a.SANS, 600) + a.text(110, 478, "sin voto", 15, a.GREY, a.MONO), 77, 100)
a.add(dev(a, *Q, 300, 84, "Debian · 10.10.10.13", "corosync-qnetd", icon="server", tsize=18, stroke=a.CYAN, sw=2.5))
at(a, a.text(Q[0] + 150, Q[1] + 112, "no corre VMs: solo vota", 15, a.CYAN, a.SANS, 600, "middle"), 0, 100, still=1)
# enlaces
at(a, line(198, 270, 198, 420, a.BLUE, 4), 0, 77, still=1)
at(a, line(198, 270, 198, 420, a.LINE, 4, "8 8"), 77, 100)
a.add(path(f"M348 228 H394 V330 H{Q[0]}", a.LINE, 3, "6 6"))
a.add(path(f"M348 462 H394 V360 H{Q[0]}", a.LINE, 3, "6 6"))
at(a, path(f"M348 228 H394 V330 H{Q[0]}", a.CYAN, 3.5), 54, 100, still=1)
at(a, path(f"M348 462 H394 V360 H{Q[0]}", a.CYAN, 3.5), 54, 77, still=1)
at(a, chip(a, 400, 252, "TCP 5403", "cyan", h=28), 54, 100, still=1)
# paso 1: paquetes instalados
at(a, chip(a, Q[0], Q[1] - 40, "apt install corosync-qnetd", "info", h=28), 3, 25)
# paso 2: setup
go(a, "clave SSH", [(348, 228), (394, 228), (394, 330), (Q[0], 330)], 30, 35, a.BLUE, hold=0.5)
go(a, "certificados", [(Q[0], 330), (394, 330), (394, 228), (348, 228)], 37, 42, a.OK, hold=0.5)
go(a, "certificados", [(Q[0], 360), (394, 360), (394, 462), (348, 462)], 40, 45, a.OK, hold=0.5)
at(a, chip(a, Q[0], Q[1] - 40, "conexión cifrada", "ok", h=28), 44, 50)
# paso 3 y 4: votos
for t in (56, 62, 68, 80, 88):
    go(a, "voto", [(Q[0], 330), (394, 330), (394, 228), (348, 228)], t, t + 3, a.CYAN, hold=0.2)
for t in (58, 64, 70):
    go(a, "voto", [(Q[0], 360), (394, 360), (394, 462), (348, 462)], t, t + 3, a.CYAN, hold=0.2)

# terminal
TX, TY, TW, TH = 780, 182, 372, 412
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 18, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
L = [TY + 60 + i * 25 for i in range(14)]
at(a, tline(a, TX + 18, L[0], "# apt install corosync-qdevice", MINT) + tline(a, TX + 18, L[1], "(también en pve2)", SKY), 0, 25)
at(a, tline(a, TX + 18, L[0], "# pvecm qdevice setup 10.10.10.13", MINT) + tline(a, TX + 18, L[2], "... Done", a.WHITE), 25, 50)
p3 = (tline(a, TX + 18, L[0], "# pvecm status", MINT)
      + tline(a, TX + 18, L[1], "Expected votes:   3")
      + tline(a, TX + 18, L[2], "Highest expected: 3")
      + tline(a, TX + 18, L[4], "Quorum:           2")
      + tline(a, TX + 18, L[6], "Membership information", SKY)
      + tline(a, TX + 18, L[7], "Nodeid  Votes Qdevice Name", SKY))
at(a, p3, 50, 100, still=1)
at(a, tline(a, TX + 18, L[3], "Total votes:      3") + tline(a, TX + 18, L[5], "Flags: Quorate Qdevice", MINT)
   + tline(a, TX + 18, L[8], "0x1       1  A,V,NMW .11", a.WHITE) + tline(a, TX + 18, L[9], "0x2       1  A,V,NMW .12", a.WHITE)
   + tline(a, TX + 18, L[10], "0x0       1          Qdevice", MINT), 50, 77, still=1)
at(a, tline(a, TX + 18, L[3], "Total votes:      2", GOLD) + tline(a, TX + 18, L[5], "Flags: Quorate Qdevice", MINT)
   + tline(a, TX + 18, L[8], "0x1       1  A,V,NMW .11", a.WHITE) + tline(a, TX + 18, L[10], "0x0       1          Qdevice", MINT)
   + tline(a, TX + 18, L[12], "2 de 3: Quorate: Yes", MINT), 77, 100)

status(a, 632, [
    (0, 25, "El tercer voto no necesita un servidor: alcanza un Debian chico, incluso en otra sede.", a.INK, 0),
    (25, 50, "La conexión entre el qnetd y el clúster va cifrada: setup deja las claves y certificados.", a.BLUE, 0),
    (50, 75, "El QDevice va por TCP y no tiene la exigencia de latencia de corosync.", a.CYAN, 1),
    (75, 100, "Con tres votos esperados, perder un nodo deja mayoría: el clúster sigue escribiendo.", a.OK, 0),
])

write(a, 9, "l2", "QDevice: el tercer voto llega por TCP 5403",
      "Animación en cuatro tiempos con pve1 (10.10.10.11) y pve2 (10.10.10.12) con corosync-qdevice, un tercer equipo Debian (10.10.10.13) con corosync-qnetd, que no corre VMs y solo vota, y la terminal de pve1. "
      "1: se instala corosync-qnetd en el tercer equipo y corosync-qdevice en los dos nodos. "
      "2: pvecm qdevice setup 10.10.10.13 copia la clave SSH del clúster al tercer equipo y arma certificados para que la conexión vaya cifrada; termina con Done. "
      "3: cada nodo habla con el qnetd por TCP 5403 y el QDevice aporta un voto: pvecm status muestra Expected votes 3, Total votes 3, Quorum 2, Flags Quorate Qdevice, y en Membership information los dos nodos con A,V,NMW y una fila Qdevice con 1 voto. "
      "4: en el paso 6 se apaga pve2; pve1 y el QDevice suman 2 de 3 votos, Total votes 2, y el clúster sigue con Quorate: Yes.",
      [8, 38, 62, 66, 92])
