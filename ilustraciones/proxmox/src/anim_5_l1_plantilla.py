#!/usr/bin/env python3
"""Lección 5 · Laboratorio, paso 2: cómo se arma la plantilla 9000. qm create arma el hardware, import-from copia la
imagen qcow2 a local-lvm como scsi0, ide2 agrega la unidad cloud-init, boot y serial0 dejan el arranque y la consola,
y qm template congela la VM: el disco pasa a base-9000-disk-0, de solo lectura.
Fuentes: wiki Cloud-Init_Support (pasos), guía de administración (nombres de volumen vm-/base-, plantilla de solo
lectura), tarjeta de la lección (comandos del paso 2)."""
from _anim_pmx_red import *

a = new(24, "Plantilla y clon", "Cuatro piezas y la VM queda de molde", lab=True)
a.steps([
    "qm create 9000: solo el hardware, todavía sin disco.",
    "import-from: la imagen qcow2 se copia a local-lvm como scsi0.",
    "ide2 cloudinit, boot order=scsi0 y consola serie.",
    "qm template 9000: el disco pasa a base-9000, de solo lectura.",
], still=3)

# imagen en /root
a.add(dev(a, 48, 182, 300, 96, "Imagen cloud", "/root/debian-13-", icon="card", sub2="genericcloud-amd64.qcow2", tsize=18, ssize=15))
at(a, a.text(48, 306, "sistema instalado, sin usuario ni red", 15, a.GREY, a.SANS), 0, 100, still=1)

# configuración de la VM 9000
CX, CY, CW, CH = 380, 182, 400, 300
a.add(a.box(CX, CY, CW, CH, a.WHITE, a.LINE, rx=14))
a.add(a.text(CX + 18, CY + 30, "VM 9000 · debian13-tpl", 17, a.INK, a.SANS, 600))
at(a, chip(a, CX + CW - 18, CY + 12, "template", "dark", anchor="end", h=28), 80, 100, still=1)
rows = [
    (0, "memory: 2048 · cores: 2", 3),
    (1, "net0: virtio,bridge=vmbr0", 3),
    (2, "scsihw: virtio-scsi-single", 3),
    (3, "agent: 1", 3),
    (4, "scsi0: local-lvm:vm-9000-disk-0", 34),
    (5, "ide2: local-lvm:vm-9000-cloudinit", 54),
    (6, "boot: order=scsi0", 58),
    (7, "serial0: socket · vga: serial0", 62),
]
for i, txt, t in rows:
    y = CY + 62 + i * 28
    col = a.TXT if i < 4 else (a.BLUE if i == 4 else a.CYAN)
    a.add(during(a, a.text(CX + 18, y, txt, 15, col, a.MONO, 600 if i >= 4 else 400), t, 100, still=1))
# en el paso 4, scsi0 cambia de nombre
a.add(during(a, a.box(CX + 10, CY + 62 + 4 * 28 - 19, CW - 20, 26, a.WHITE, rx=4) + a.text(CX + 18, CY + 62 + 4 * 28, "scsi0: local-lvm:base-9000-disk-0", 15, a.INK, a.MONO, 700), 82, 100, still=1))

# local-lvm
SX, SY, SW, SH = 812, 182, 340, 300
a.add(a.box(SX, SY, SW, SH, a.SLATE, a.LINE, rx=14))
a.add(glyph(a, "server", SX + 18, SY + 16))
a.add(a.text(SX + 60, SY + 36, "local-lvm · thin pool", 17, a.INK, a.SANS, 600))
vol1 = a.box(SX + 18, SY + 64, SW - 36, 52, a.WHITE, a.BLUE, rx=10, sw=2) + a.text(SX + 34, SY + 96, "vm-9000-disk-0", 15, a.BLUE, a.MONO, 700)
a.add(during(a, vol1, 32, 84))
vol1b = a.box(SX + 18, SY + 64, SW - 36, 52, a.INK, rx=10) + a.text(SX + 34, SY + 96, "base-9000-disk-0", 15, a.WHITE, a.MONO, 700) + glyph(a, "lock", SX + SW - 54, SY + 76, GOLD, 1.0)
a.add(during(a, vol1b, 82, 100, still=1))
vol2 = a.box(SX + 18, SY + 132, SW - 36, 52, a.WHITE, a.CYAN, rx=10, sw=2) + a.text(SX + 34, SY + 164, "vm-9000-cloudinit", 15, a.CYAN, a.MONO, 700)
a.add(during(a, vol2, 54, 100, still=1))
at(a, a.text(SX + 18, SY + 220, "solo lectura: se clona,", 15, a.INK, a.SANS, 600) + a.text(SX + 18, SY + 244, "no se arranca ni se modifica", 15, a.INK, a.SANS, 600), 84, 100, still=1)
# copia de la imagen
for i in range(5):
    a.add(travel(a, a.box(-14, -10, 28, 20, a.BLUE, rx=4), [(198, 278), (198, 520), (SX + 170, 520), (SX + 170, SY + SH)], 27 + i * 1.5, 33 + i * 1.5, hold=0.1, fade=0.3))
a.add(path(f"M198 318 V520 H{SX + 170} V{SY + SH}", a.LINE, 2.5, "6 6"))

# terminal
TX, TY, TW, TH = 48, 540, 1104, 60
a.add(a.box(TX, TY, TW, TH, a.INK, rx=12))
cmds = [
    (0, 25, "# qm create 9000 --name debian13-tpl --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0 --scsihw ... --agent 1"),
    (25, 50, "# qm set 9000 --scsi0 local-lvm:0,import-from=/root/debian-13-genericcloud-amd64.qcow2"),
    (50, 75, "# qm set 9000 --ide2 local-lvm:cloudinit · --boot order=scsi0 · --serial0 socket --vga serial0"),
    (75, 100, "# qm template 9000"),
]
for t0, t1, c in cmds:
    at(a, tline(a, TX + 18, TY + 37, c, MINT), t0, t1, still=1 if t0 == 75 else 0)

status(a, 640, [
    (0, 25, "El hardware se elige una vez: VirtIO, agente y la placa en vmbr0 quedan en el molde.", a.INK, 0),
    (25, 50, "import-from copia la imagen al almacenamiento: el qcow2 de /root/ ya no se usa.", a.BLUE, 0),
    (50, 75, "La unidad cloud-init es un CD que Proxmox arma con los datos de cada clon.", a.CYAN, 0),
    (75, 100, "La plantilla no arranca más: es el molde de donde salen los clones.", a.INK, 1),
])

write(a, 5, "l1", "Cuatro piezas y la VM queda de molde",
      "Animación en cuatro tiempos con la imagen /root/debian-13-genericcloud-amd64.qcow2, la configuración de la VM 9000 debian13-tpl, el almacenamiento local-lvm y la terminal. "
      "1: qm create 9000 arma solo el hardware: memory 2048, cores 2, net0 virtio en vmbr0, scsihw virtio-scsi-single y agent 1, todavía sin disco. "
      "2: qm set 9000 --scsi0 local-lvm:0,import-from=/root/... copia la imagen, que ya trae el sistema instalado sin usuario ni red, al thin pool como vm-9000-disk-0, y aparece la línea scsi0. "
      "3: --ide2 local-lvm:cloudinit agrega la unidad cloud-init, el volumen vm-9000-cloudinit; boot order=scsi0 arranca directo del disco y serial0 con vga serial0 deja la consola serie. "
      "4: qm template 9000 convierte la VM en plantilla: el disco pasa a llamarse base-9000-disk-0, queda de solo lectura y la VM ya no se arranca ni se modifica, solo se clona.",
      [10, 34, 60, 70, 92])
