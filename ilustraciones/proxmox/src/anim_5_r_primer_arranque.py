#!/usr/bin/env python3
"""Lección 5 · Resumen, "Cómo se ve en la red": un servidor nuevo en un minuto. Full clone de la plantilla 9000 a la
VM 201, datos de cloud-init en la configuración, Proxmox genera el CD (formato nocloud: user, network, meta), en el
primer arranque cloud-init crea el usuario, copia la clave, configura la IP y agranda el disco, y el host entra por
SSH con la clave.
Fuentes: wiki Cloud-Init_Support (ISO generado por Proxmox, nocloud para Linux, user/network/meta, clave SSH
antes que contraseña), tarjeta de la lección (comandos del paso 3)."""
from _anim_pmx_red import *

a = new(24, "Plantilla y clon", "De la plantilla a un servidor con usuario, IP y SSH")
a.steps([
    "qm clone 9000 201 --full 1: copia completa, sin usuario ni red.",
    "Los datos de cloud-init van a la VM; al arrancar, Proxmox arma el CD.",
    "Primer arranque: cloud-init lee el CD y aplica usuario, clave e IP.",
    "Desde pve1: ssh tecnico@10.10.10.201 entra con la clave, sin contraseña.",
], still=2)

# plantilla y clon
a.add(dev(a, 48, 180, 250, 86, "Plantilla 9000", "debian13-tpl", icon="server", sub2="solo lectura", tsize=18))
a.add(during(a, dev(a, 48, 300, 250, 86, "VM 201", "prueba-ci", icon="server", sub2="full clone", tsize=18, stroke=a.BLUE), 8, 100, still=1))
for i in range(4):
    a.add(travel(a, a.box(-12, -9, 24, 18, a.CYAN, rx=4), [(173, 266), (173, 300)], 2 + i * 1.4, 4 + i * 1.4, hold=0.2, fade=0.3))
at(a, chip(a, 48, 398, "sin usuario · sin red", "grey"), 9, 25)
at(a, chip(a, 48, 398, "tecnico · 10.10.10.201", "ok"), 62, 100, still=1)

# datos de cloud-init y CD
CX, CY, CW, CH = 340, 180, 390, 370
a.add(a.box(CX, CY, CW, CH, a.WHITE, a.LINE, rx=16))
a.add(glyph(a, "card", CX + 18, CY + 16))
a.add(a.text(CX + 60, CY + 36, "CD cloud-init · ide2", 18, a.INK, a.SANS, 600))
a.add(a.text(CX + 60, CY + 60, "nocloud · lo genera Proxmox", 15, a.GREY, a.MONO))
files = [("user", ["hostname: prueba-ci", "user: tecnico", "ssh key: id_ed25519.pub"], 0, CY + 82),
         ("network", ["ip: 10.10.10.201/24", "gw: 10.10.10.1"], 1, CY + 188),
         ("meta", ["instance-id: ..."], 2, CY + 270)]
for name, lines, i, y in files:
    body = a.box(CX + 18, y, CW - 36, 24 * len(lines) + 24, a.SLATE, rx=10)
    body += a.text(CX + 34, y + 26, name, 15, a.BLUE, a.MONO, 700)
    for k, ln in enumerate(lines):
        body += a.text(CX + 130, y + 26 + k * 24, ln, 15, a.INK, a.MONO)
    a.add(during(a, body, 30 + i * 3, 100, still=1))
at(a, a.text(CX + 18, CY + CH - 14, "contraseña: mejor no, va guardada en estos datos", 15, a.AMB, a.SANS, 600), 38, 75, still=1)

# terminal pve1 (comandos)
TX, TY, TW, TH = 760, 180, 392, 200
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 18, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
T = [TY + 60 + i * 25 for i in range(6)]
at(a, tline(a, TX + 18, T[0], "# qm clone 9000 201 --full 1", MINT), 0, 75, still=1)
at(a, tline(a, TX + 18, T[1], "# qm set 201 --ciuser tecnico", MINT), 26, 75, still=1)
at(a, tline(a, TX + 18, T[2], "  --sshkeys ...id_ed25519.pub", MINT), 26, 75, still=1)
at(a, tline(a, TX + 18, T[3], "  --ipconfig0 ip=10.10.10.201/24", MINT), 26, 75, still=1)
at(a, tline(a, TX + 18, T[4], "# qm resize 201 scsi0 +10G", MINT), 28, 75, still=1)
at(a, tline(a, TX + 18, T[5], "# qm start 201", MINT), 30, 75, still=1)
at(a, tline(a, TX + 18, T[0], "# ssh tecnico@10.10.10.201", MINT), 75, 100)
at(a, tline(a, TX + 18, T[1], "(entra con la clave)", SKY), 86, 100)
at(a, tline(a, TX + 18, T[2], "tecnico@prueba-ci:~$", a.WHITE), 88, 100)
go(a, "datos", [(TX, TY + 120), (CX + CW, CY + 120)], 27, 30, a.BLUE, hold=0.3)

# consola del primer arranque
KX, KY, KW, KH = 760, 400, 392, 186
a.add(a.box(KX, KY, KW, KH, a.INK, rx=14))
a.add(a.text(KX + 18, KY + 28, "CONSOLA XTERM.JS · VM 201", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
K = [KY + 58 + i * 24 for i in range(5)]
at(a, tline(a, KX + 18, K[0], "cloud-init: lee el CD (nocloud)", SKY), 52, 100, still=1)
at(a, tline(a, KX + 18, K[1], "crea el usuario tecnico", a.WHITE), 55, 100, still=1)
at(a, tline(a, KX + 18, K[2], "copia la clave en authorized_keys", a.WHITE), 58, 100, still=1)
at(a, tline(a, KX + 18, K[3], "eth0 10.10.10.201/24 gw .1", a.WHITE), 61, 100, still=1)
at(a, tline(a, KX + 18, K[4], "agranda la partición: +10G", a.WHITE), 64, 100, still=1)
# el CD entra a la VM
go(a, "CD", [(CX + CW / 2, CY + CH), (CX + CW / 2, 568), (KX, 568)], 50, 54, a.CYAN, hold=0.4)
go(a, "CD", [(CX + 18, CY + 160), (298, 343)], 50, 54, a.CYAN, hold=0.6)
# ssh
go(a, "SSH · clave", [(TX + 40, TY + TH), (TX + 40, KY)], 78, 82, a.OK, hold=0.4)
go(a, "SSH · clave", [(TX + 40, TY + TH), (TX + 40, KY)], 82, 86, a.OK, hold=0.4)
at(a, check(a, KX + KW - 30, KY + 26), 86, 100)

status(a, 628, [
    (0, 25, "El clon nace igual a la plantilla: un disco listo, sin nombre, usuario ni IP.", a.INK, 0),
    (25, 50, "Cada VM lleva sus propios datos de cloud-init; el CD se arma con ellos.", a.BLUE, 0),
    (50, 75, "Nadie pasa por un instalador: cloud-init aplica todo en el primer arranque.", a.OK, 1),
    (75, 100, "La clave pública ya está adentro: el SSH entra sin contraseña.", a.OK, 0),
])

write(a, 5, "r1", "De la plantilla a un servidor con usuario, IP y SSH",
      "Animación en cuatro tiempos con la plantilla 9000 (debian13-tpl, solo lectura), la VM 201, el CD de cloud-init en ide2, la terminal de pve1 y la consola xterm.js de la VM. "
      "1: qm clone 9000 201 --full 1 copia completa la plantilla en la VM 201, que nace sin usuario y sin red. "
      "2: qm set 201 con --ciuser tecnico, --sshkeys con la clave pública id_ed25519.pub e --ipconfig0 ip=10.10.10.201/24 deja los datos en la VM; qm resize agrega 10 GB y qm start la arranca; "
      "Proxmox genera el CD en formato nocloud con tres partes: user (hostname prueba-ci, usuario tecnico y la clave), network (10.10.10.201/24, gateway 10.10.10.1) y meta (el identificador de la instancia). "
      "3: en el primer arranque cloud-init lee el CD, crea el usuario tecnico, copia la clave en authorized_keys, configura eth0 con 10.10.10.201 y agranda la partición. "
      "4: desde pve1, ssh tecnico@10.10.10.201 entra con la clave, sin contraseña, y aparece el prompt tecnico@prueba-ci.",
      [6, 36, 56, 68, 92])
