import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 7.svg: snapshot no es backup
c = Canvas(K(), "Un snapshot no es un backup: dónde vive cada uno")
c.add(NOLIG)
c.add(rect(48, 124, 520, 330, WHITE, LINE2, rx=18))
c.add(text(72, 162, "Disco del host · local-lvm", 20, 600, INK, FD))
c.add(vmcard(72, 186, 470, "VM 100", "su disco, en producción", "info"))
c.add(vmcard(72, 270, 470, "Snapshot de la VM 100", "mismo disco, mismo pool", "warn"))
c.add(rect(72, 362, 470, 70, ALERT_BG, ALERT, rx=12))
c.add(text(96, 394, "Si este disco muere, se pierden", 17, 700, ALERT, FB))
c.add(text(96, 418, "la VM y su snapshot juntos.", 16, 500, INK2, FB))
c.add(path("M568 230 H644", BLUE, 4, arrow=True))
c.add(pill(606, 214, "vzdump", BLUE, size=15))
c.add(rect(652, 124, 500, 210, OK_BG, OK, rx=18))
c.add(text(676, 162, "Otro almacenamiento", 20, 600, OK, FD))
c.add(text(676, 192, "local, NFS o Proxmox Backup Server", 15, 500, INK2, FM))
c.add(code(676, 212, 452, "vzdump-qemu-100-<fecha>.vma.zst", 15))
c.add(text(676, 290, "Copia completa: configuración y discos.", 16, 500, INK2, FB))
c.add(text(676, 314, "Sobrevive si el disco de la VM muere.", 16, 600, OK, FB))
c.add(path("M902 334 V372", OK, 4, arrow=True))
c.add(rect(652, 380, 500, 74, WHITE, OK, rx=14))
c.add(text(676, 412, "Restore de prueba a la VM 900", 17, 700, INK, FB))
c.add(text(676, 436, "nunca encima de la VM 100", 15, 500, INK2, FB))
c.add(Note(48, 480, 520, "Sirve para deshacer un cambio: antes de actualizar, un snapshot; si sale mal, rollback en minutos.", title="Para qué sí sirve el snapshot", kind="info"))
c.add(Note(612, 480, 540, "Un backup cuenta cuando lo restauraste en una VM nueva y arrancó. Anotá cuánto tardó.", title="Cuándo cuenta un backup", kind="ok"))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso1: vzdump y el archivo
c = Canvas(K(1), "vzdump: qué le pedís y qué archivo deja")
c.add(NOLIG)
c.add(Step(48, 124, 1))
parts = [("vzdump 100", "la VM a respaldar", BLUE), ("--mode snapshot", "sin apagarla; con el agente congela el disco", OK),
         ("--compress zstd", "compresión rápida", BLUE), ("--storage local", "destino: /var/lib/vz/dump", BLUE)]
for i, (p, d, col) in enumerate(parts):
    y = 132 + i * 64
    c.add(rect(80, y, 330, 48, "#03213C", "#03213C", rx=10))
    c.add(text(98, y + 31, p, 16, 600, "#7FE0B0" if col == OK else "#D9E9F8", FM))
    c.add(path(f"M418 {y + 24} H456", CYAN, 3, arrow=True))
    c.add(text(468, y + 31, d, 17, 500, INK, FB))
c.add(text(48, 418, "Lo que aparece en /var/lib/vz/dump/:", 18, 600, INK, FB))
segs = [("vzdump", "prefijo", INK2), ("-qemu", "qemu: VM · lxc: CT", BLUE), ("-100", "VMID", OK),
        ("-<fecha>", "fecha y hora", WARN), (".vma", "formato", BLUE), (".zst", "compresión", INK2)]
for i, (sg, lb, col) in enumerate(segs):
    xc = [110, 290, 450, 620, 800, 950][i]
    w = len(sg) * 13.2 + 28
    c.add(rect(xc - w / 2, 436, w, 46, WHITE, col, rx=10))
    c.add(text(xc, 467, sg, 22, 700, col, FM, anchor="middle"))
    c.add(text(xc, 510, lb, 15, 600, col, FB, anchor="middle"))
c.add(Note(48, 534, 1104, "En modo snapshot la VM sigue andando. El modo stop la apaga un momento y da la máxima consistencia: se elige cuando la consistencia manda.", kind="info"))
save(c, "7-paso1.svg")

# ---------------------------------------------------------------- 7-paso3: restore con la placa desconectada
c = Canvas(K(3), "Restore a la VM 900 con el cable virtual desenchufado")
c.add(NOLIG)
c.add(Step(48, 124, 3))
c.add(rect(400, 140, 400, 90, DEEP, DEEP, rx=16))
c.add(text(600, 180, "vmbr0", 22, 600, WHITE, FD, anchor="middle"))
c.add(text(600, 206, "la red del cliente", 15, 400, "#9FC3E3", FM, anchor="middle"))
c.add(vmcard(120, 330, 380, "VM 100 · original", "10.10.10.100 · en producción", "ok"))
c.add(vmcard(700, 330, 380, "VM 900 · restaurada", "misma IP y misma MAC adentro", "warn"))
c.add(path("M310 330 V270 H500 V230", BLUE, 4))
c.add(path("M890 330 V270 H700 V236", ALERT, 4, dash="8 7"))
c.add(Mark(795, 270, False))
c.add(tag(1010, 300, "link_down=1", "alert", 15))
sv, h = codebox(120, 440, 960, ["qm set 900 --net0 virtio,bridge=vmbr0,link_down=1", "qm start 900"], 16, 30, title="ANTES DE ARRANCARLA")
c.add(sv)
c.add(Note(120, 560, 960, "Si arranca conectada, la copia pelea la IP con la original. Probá por la consola: que el sistema y los datos estén, y anotá cuánto tardó.", kind="warn"))
save(c, "7-paso3.svg")
