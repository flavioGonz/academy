import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 6.svg: VM contra LXC
c = Canvas(K(), "VM o contenedor: quién tiene kernel propio")
c.add(NOLIG)
for x, t, kd in [(48, "Máquina virtual (KVM)", "info"), (612, "Contenedor (LXC)", "ok")]:
    c.add(text(x, 140, t, 22, 600, INK, FD))
# VM
c.add(layer(48, 162, 540, 54, "aplicaciones", fill=SOFT, stroke=LINE2, size=17))
c.add(layer(48, 224, 540, 54, "kernel propio del invitado", fill="#0B3A66", stroke="#0B3A66", color=WHITE, size=17))
c.add(layer(48, 286, 540, 54, "hardware virtual (QEMU)", fill=WHITE, stroke=BLUE, color=BLUE, size=17))
c.add(layer(48, 348, 540, 54, "kernel del host · KVM", fill=DEEP, stroke=DEEP, color=WHITE, size=17))
c.add(layer(48, 410, 540, 46, "hardware", fill=GROUND, stroke=LINE2, size=16))
# LXC
c.add(layer(612, 162, 540, 54, "aplicaciones", fill=SOFT, stroke=LINE2, size=17))
c.add(layer(612, 224, 540, 116, "", fill=OK_BG, stroke=OK))
c.add(text(882, 268, "sistema de archivos y procesos aislados", 17, 600, OK, FB, anchor="middle"))
c.add(text(882, 296, "sin kernel propio", 16, 500, INK2, FB, anchor="middle"))
c.add(layer(612, 348, 540, 54, "kernel del host · compartido", fill=DEEP, stroke=CYAN, color=WHITE, size=17))
c.add(layer(612, 410, 540, 46, "hardware", fill=GROUND, stroke=LINE2, size=16))
for x, items in [(48, [("Aísla más: otro kernel", True), ("Windows o cualquier Linux", True), ("Docker y lo expuesto a internet", True)]),
                 (612, [("Arranca en segundos, gasta poco", True), ("Solo Linux, mismo kernel del host", False), ("Si el kernel se compromete, afecta al host", False)])]:
    for j, (s, ok) in enumerate(items):
        c.add(check(x + 18, 490 + j * 42, s, ok, 17) if ok else
              f'<circle cx="{x + 18}" cy="{490 + j * 42}" r="18" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/>' + text(x + 18, 496 + j * 42, "!", 18, 700, WARN, FD, anchor="middle") + text(x + 48, 496 + j * 42, s, 17, 500, INK, FB))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso3: anatomía de pct create
c = Canvas(K(3), "pct create: qué define cada opción")
c.add(NOLIG)
c.add(Step(48, 124, 3))
opts = [("300", "el CTID, como el VMID de una VM"), ("local:vztmpl/<plantilla>", "la plantilla Debian que bajaste con pveam"),
        ("--hostname ct-prueba", "nombre del contenedor"), ("--unprivileged 1", "no privilegiado: el default y lo seguro"),
        ("--memory 512", "MB de RAM"), ("--rootfs local-lvm:8", "disco raíz de 8 GB en local-lvm"),
        ("--net0 name=eth0,bridge=vmbr0,ip=dhcp", "placa eth0 en vmbr0, IP por DHCP"), ("--password '…'", "clave de root de ejemplo: cambiala")]
for i, (o, d) in enumerate(opts):
    y = 132 + i * 60
    hl = o.startswith("--unprivileged")
    c.add(rect(80, y, 470, 46, OK_BG if hl else "#03213C", OK if hl else "#03213C", rx=10))
    c.add(text(98, y + 29, o, 15, 600, OK if hl else "#D9E9F8", FM))
    c.add(path(f"M558 {y + 23} H596", CYAN, 3, arrow=True))
    c.add(text(608, y + 29, d, 17, 600 if hl else 500, OK if hl else INK, FB))
c.add(text(80, 630, "Después: pct start 300 y pct enter 300 para entrar.", 16, 500, INK3, FB))
save(c, "6-paso3.svg")

# ---------------------------------------------------------------- 6-paso4: uid_map
c = Canvas(K(4), "cat /proc/self/uid_map: el root de adentro no es root")
c.add(NOLIG)
c.add(Step(48, 124, 4))
sv, h = codebox(48, 124, 560, ["# cat /proc/self/uid_map", ("         0     100000      65536", "#7FE0B0")], 18, 34, title="ADENTRO DEL CT 300")
c.add(sv)
for i, (v, lab) in enumerate([("0", "uid adentro del contenedor"), ("100000", "el uid que le corresponde en el host"), ("65536", "cuántos uid se mapean en fila")]):
    c.add(text(640, 152 + i * 34, v, 18, 700, OK, FM))
    c.add(text(740, 152 + i * 34, lab, 17, 500, INK2, FB))
c.add(rect(48, 290, 500, 220, OK_BG, OK, rx=16))
c.add(text(72, 326, "Contenedor 300", 20, 600, OK, FD))
c.add(text(72, 372, "root", 30, 700, INK, FM))
c.add(text(72, 402, "uid 0", 17, 600, INK2, FM))
c.add(text(72, 470, "uid 1 → 100001 … uid 65535 → 165535", 15, 500, INK2, FM))
c.add(path("M548 386 H640", OK, 5, arrow=True))
c.add(rect(648, 290, 504, 220, DEEP, DEEP, rx=16))
c.add(text(672, 326, "Host Proxmox", 20, 600, WHITE, FD))
c.add(text(672, 372, "uid 100000", 30, 700, WHITE, FM))
c.add(text(672, 402, "un usuario sin privilegios", 17, 500, "#9FC3E3", FB))
c.add(text(672, 470, "no puede tocar archivos del host", 16, 600, "#7FE0B0", FB))
c.add(Note(48, 534, 1104, "En el host, pct config 300 | grep unprivileged tiene que mostrar unprivileged: 1. En un contenedor privilegiado, el root de adentro sería el root del host.", kind="info"))
save(c, "6-paso4.svg")
