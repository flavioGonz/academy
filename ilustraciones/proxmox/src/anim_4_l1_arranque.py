#!/usr/bin/env python3
"""Lección 4 · Laboratorio, paso 3: el cambio de agente necesita un arranque nuevo desde Proxmox. qm set --agent 1
queda en la configuración, pero el proceso QEMU que ya corre se armó sin el canal del agente; un reboot desde
adentro reinicia el sistema invitado en el mismo proceso. Stop y Start crean un proceso nuevo, con el canal
/var/run/qemu-server/100.qga, y el ping responde.
Fuentes: guía de administración ("A fresh start of the VM is necessary"), wiki Qemu-guest-agent (socket .qga)."""
from _anim_pmx_red import *

a = new(24, "VM bien armada", "Por qué el agente pide apagar y prender", lab=True)
a.steps([
    "qm set 100 --agent 1: queda en la configuración, el QEMU que corre no cambia.",
    "Reboot desde adentro: rearranca el sistema, pero en el mismo proceso.",
    "Stop y Start desde Proxmox: proceso QEMU nuevo, ya con el canal.",
    "El agente arranca adentro y qm agent 100 ping responde.",
], still=2)

# configuración
a.add(a.box(48, 182, 330, 150, a.WHITE, a.LINE, rx=14))
a.add(a.text(66, 212, "/etc/pve/qemu-server/100.conf", 15, a.GREY, a.MONO))
a.add(a.text(66, 248, "scsihw: virtio-scsi-single", 15, a.TXT, a.MONO))
a.add(a.text(66, 276, "net0: virtio=...,bridge=vmbr0", 15, a.TXT, a.MONO))
at(a, a.box(56, 290, 314, 32, a.OKBG, rx=8) + a.text(66, 312, "agent: 1", 15, a.OK, a.MONO, 700), 4, 100, still=1)
go(a, "agent: 1", [(213, 160), (213, 306)], 1, 4, a.BLUE, hold=0.3)

# proceso QEMU
QX, QY, QW, QH = 420, 182, 380, 300


def qemu(pid, canal, st=0, t0=0, t1=100):
    s = a.box(QX, QY, QW, QH, a.INK, rx=16)
    s += a.text(QX + 22, QY + 34, "Proceso QEMU de la VM 100", 17, a.WHITE, a.SANS, 600)
    s += a.text(QX + 22, QY + 60, f"kvm -id 100 · PID {pid}", 15, SKY, a.MONO)
    s += a.box(QX + 22, QY + 84, QW - 44, 126, "#0B2E50", rx=12)
    s += a.text(QX + 40, QY + 112, "Debian adentro", 16, a.WHITE, a.SANS, 600)
    s += a.text(QX + 40, QY + 140, "qemu-guest-agent", 15, SKY, a.MONO)
    if canal:
        s += a.box(QX + 22, QY + 226, QW - 44, 52, "#0F3A2C", rx=10) + a.text(QX + 40, QY + 258, "canal del agente · 100.qga", 15, MINT, a.MONO, 600)
    else:
        s += a.box(QX + 22, QY + 226, QW - 44, 52, "#3A1F1A", rx=10) + a.text(QX + 40, QY + 258, "sin canal del agente", 15, CORAL, a.MONO, 600)
    at(a, s, t0, t1, still=st)


qemu(4123, False, 0, 0, 52)
qemu(5871, True, 1, 52, 100)
# servicio adentro
at(a, chip(a, QX + 40, QY + 156, "corre, sin canal", "amb" ), 0, 28)
at(a, chip(a, QX + 40, QY + 156, "reboot: reiniciando", "amb"), 28, 40)
at(a, chip(a, QX + 40, QY + 156, "corre, sin canal", "amb"), 40, 52)
at(a, chip(a, QX + 40, QY + 156, "arrancando", "amb"), 56, 76)
at(a, chip(a, QX + 40, QY + 156, "active (running)", "ok"), 76, 100, still=1)
# reboot interno: flecha circular
# stop / start
at(a, a.box(QX - 4, QY - 4, QW + 8, QH + 8, "none", a.BAD, rx=18, sw=3, extra='stroke-dasharray="10 8"') + chip(a, QX + QW / 2, QY + QH + 14, "Stop: el proceso termina", "bad", anchor="middle"), 50, 56)
at(a, chip(a, QX + QW / 2, QY + QH + 14, "Start: proceso nuevo con agent: 1", "ok", anchor="middle"), 56, 75, still=1)

# host / terminal
TX, TY, TW, TH = 840, 182, 312, 300
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 18, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
L = [TY + 62 + i * 26 for i in range(9)]
at(a, tline(a, TX + 18, L[0], "# qm set 100 --agent 1", MINT), 0, 100, still=1)
at(a, tline(a, TX + 18, L[1], "# qm agent 100 ping", MINT), 10, 50)
at(a, tline(a, TX + 18, L[2], "error: no hay canal", CORAL), 14, 50)
at(a, tline(a, TX + 18, L[3], "(adentro: reboot)", GOLD), 28, 50)
at(a, tline(a, TX + 18, L[4], "# qm agent 100 ping", MINT), 42, 50)
at(a, tline(a, TX + 18, L[5], "error: sigue sin canal", CORAL), 45, 50)
at(a, tline(a, TX + 18, L[1], "# qm stop 100", MINT), 50, 100, still=1)
at(a, tline(a, TX + 18, L[2], "# qm start 100", MINT), 55, 100, still=1)
at(a, tline(a, TX + 18, L[3], "# qm agent 100 ping", MINT), 78, 100)
at(a, tline(a, TX + 18, L[4], "sin salida ni error:", MINT), 84, 100)
at(a, tline(a, TX + 18, L[5], "el agente contestó", MINT), 84, 100)
# ping que viaja
go(a, "ping", [(TX, TY + 100), (QX + QW - 30, QY + 252)], 11, 14, a.BLUE, hold=0.5)
at(a, xmark(a, QX + QW - 40, QY + 252), 14, 25)
go(a, "ping", [(TX, TY + 160), (QX + QW - 30, QY + 252)], 42, 45, a.BLUE, hold=0.5)
at(a, xmark(a, QX + QW - 40, QY + 252), 45, 50)
go(a, "ping", [(TX, TY + 140), (QX + QW - 30, QY + 252)], 79, 82, a.BLUE, hold=0.3)
go(a, "OK", [(QX + QW - 30, QY + 252), (TX, TY + 160)], 82, 85, a.OK, hold=6)

# notas
at(a, note(a, 48, 360, 330, 122, "Dos mitades", ["agent: 1 del lado de Proxmox y el", "paquete qemu-guest-agent adentro.", "Sin una de las dos, no hay canal."], "info"), 0, 100, still=1)

status(a, 610, [
    (0, 25, "El hardware virtual se arma cuando arranca el proceso QEMU, no cuando cambiás la configuración.", a.INK, 0),
    (25, 50, "Un reboot del invitado no crea un proceso nuevo: el canal sigue sin existir.", a.AMB, 0),
    (50, 75, "Apagar y prender desde Proxmox arma la VM otra vez con todo lo que dice 100.conf.", a.OK, 1),
    (75, 100, "Recién ahí el ping llega al agente: qm agent 100 ping vuelve sin error.", a.OK, 0),
], size=17)

write(a, 4, "l1", "Por qué el agente pide apagar y prender",
      "Animación en cuatro tiempos con el archivo /etc/pve/qemu-server/100.conf, el proceso QEMU de la VM 100 con Debian adentro y la terminal de pve1. "
      "1: qm set 100 --agent 1 agrega agent: 1 a la configuración, pero el proceso QEMU que ya corre, con PID 4123, se armó sin el canal del agente; qm agent 100 ping falla porque no hay canal. "
      "2: un reboot desde adentro reinicia Debian dentro del mismo proceso QEMU; el servicio qemu-guest-agent corre, pero sigue sin canal y el ping vuelve a fallar. "
      "3: qm stop 100 termina el proceso y qm start 100 crea uno nuevo, con PID 5871, armado con agent: 1 y con el canal 100.qga. "
      "4: el servicio qemu-guest-agent arranca adentro en estado active (running) y qm agent 100 ping vuelve sin salida, sin error: el agente contestó. "
      "Hacen falta las dos mitades: agent: 1 del lado de Proxmox y el paquete qemu-guest-agent adentro.",
      [8, 36, 48, 62, 92])
