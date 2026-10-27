import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 5.svg: de la imagen cloud a los clones
c = Canvas(K(), "De una imagen cloud a VMs listas en minutos")
c.add(NOLIG)
stages = [("Imagen cloud", "debian-13-generic", "cloud-amd64.qcow2", "gray"),
          ("VM 9000", "disco importado", "+ unidad cloud-init", "info"),
          ("Plantilla", "qm template 9000", "ya no arranca", "dark")]
for i, (t, s1, s2, kd) in enumerate(stages):
    x = 48 + i * 300
    dark = kd == "dark"
    c.add(rect(x, 140, 252, 150, DEEP if dark else (GROUND if kd == "gray" else WHITE), DEEP if dark else (LINE2 if kd == "gray" else BLUE), rx=16))
    c.add(text(x + 20, 180, t, 22, 600, WHITE if dark else INK, FD))
    c.add(text(x + 20, 214, s1, 15, 500, "#9FC3E3" if dark else INK2, FM))
    c.add(text(x + 20, 238, s2, 15, 500, "#9FC3E3" if dark else INK2, FM))
    if i < 2:
        c.add(path(f"M{x + 258} 215 H{x + 294}", BLUE, 4, arrow=True))
c.add(rect(948, 140, 204, 150, OK_BG, OK, rx=16))
c.add(text(968, 180, "Clones", 22, 600, OK, FD))
c.add(text(968, 214, "201, 202, 203…", 15, 500, INK2, FM))
c.add(text(968, 238, "full clone", 15, 700, OK, FM))
c.add(path("M906 215 H942", OK, 4, arrow=True))
# lo que recibe cada clon
c.add(text(48, 342, "Cada clon recibe desde Proxmox, por cloud-init, en el primer arranque:", 18, 600, INK, FB))
for i, (k, v) in enumerate([("usuario", "tecnico"), ("clave SSH", "id_ed25519.pub"), ("IP", "10.10.10.201/24"), ("gateway", "10.10.10.1")]):
    x = 48 + i * 278
    c.add(rect(x, 362, 262, 76, WHITE, LINE2, rx=12))
    c.add(text(x + 18, 392, k, 15, 600, INK3, FB))
    c.add(text(x + 18, 420, v, 17, 600, BLUE, FM))
c.add(Note(48, 468, 540, "Instalar desde ISO lleva unos veinte minutos; clonar una plantilla, menos de uno. Y todas quedan iguales.", title="Por qué plantilla", kind="ok"))
c.add(Note(612, 468, 540, "Un linked clone depende de la plantilla: si la plantilla se borra, se rompe. Para producción, full clone.", title="Full o linked", kind="warn"))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso2: qué deja cada comando en la VM 9000
c = Canvas(K(2), "Qué deja cada comando en la VM 9000")
c.add(NOLIG)
c.add(Step(48, 124, 2))
rows = [("qm create 9000 … --scsihw virtio-scsi-single --agent 1", "VM vacía: CPU, RAM, red VirtIO y agente"),
        ("qm set 9000 --scsi0 local-lvm:0,import-from=…qcow2", "scsi0: el disco de la imagen cloud"),
        ("qm set 9000 --ide2 local-lvm:cloudinit", "ide2: el CD de cloud-init"),
        ("qm set 9000 --boot order=scsi0", "arranca del disco importado"),
        ("qm set 9000 --serial0 socket --vga serial0", "consola serie: la piden las imágenes cloud"),
        ("qm template 9000", "la convierte en plantilla")]
for i, (cmd, res) in enumerate(rows):
    y = 128 + i * 74
    c.add(code(80, y, 620, cmd, 15, h=48))
    c.add(path(f"M708 {y + 24} H748", CYAN, 3, arrow=True))
    c.add(rect(756, y, 396, 48, OK_BG if i == 5 else WHITE, OK if i == 5 else LINE2, rx=10))
    c.add(text(774, y + 30, res, 16, 600, OK if i == 5 else INK, FB))
c.add(text(80, 608, "Los … son las mismas opciones del laboratorio, abreviadas para que entren en la imagen.", 15, 500, INK3, FB))
save(c, "5-paso2.svg")

# ---------------------------------------------------------------- 5-paso3: clon con cloud-init
c = Canvas(K(3), "Clon full, cloud-init y la VM nace con su IP")
c.add(NOLIG)
c.add(Step(48, 124, 3))
c.add(rect(48, 124, 300, 130, DEEP, DEEP, rx=16))
c.add(text(68, 162, "Plantilla 9000", 20, 600, WHITE, FD))
c.add(text(68, 190, "debian13-tpl", 15, 400, "#9FC3E3", FM))
c.add(path("M348 189 H420", BLUE, 4, arrow=True))
c.add(pill(388, 158, "--full 1", BLUE, size=15))
c.add(rect(428, 124, 300, 130, WHITE, BLUE, rx=16))
c.add(text(448, 162, "VM 201 · prueba-ci", 20, 600, INK, FD))
c.add(text(448, 190, "copia independiente", 15, 400, INK3, FM))
c.add(text(448, 216, "qm resize 201 scsi0 +10G", 15, 500, BLUE, FM))
sv, h = codebox(48, 284, 680, ["qm set 201 --ciuser tecnico", "  --sshkeys /root/.ssh/id_ed25519.pub", "  --ipconfig0 ip=10.10.10.201/24,gw=10.10.10.1"], 15, 28, title="LO QUE VA AL CD DE CLOUD-INIT")
c.add(sv)
c.add(path("M728 340 H800", CYAN, 4, arrow=True))
c.add(rect(808, 124, 344, 300, OK_BG, OK, rx=16))
c.add(text(828, 162, "Primer arranque", 20, 600, OK, FD))
for j, s in enumerate(["crea el usuario tecnico", "copia la clave SSH", "pone 10.10.10.201/24", "y el gateway 10.10.10.1"]):
    c.add(Mark(846, 206 + j * 46, True))
    c.add(text(876, 212 + j * 46, s, 17, 500, INK, FB))
c.add(text(48, 470, "Mirá el arranque en xterm.js y entrá:", 17, 600, INK, FB))
c.add(code(48, 486, 420, "ssh tecnico@10.10.10.201", 16))
c.add(Note(500, 456, 652, "Si cambiás algo de cloud-init después del primer arranque, regenerá el CD con qm cloudinit update 201. Claves SSH mejor que contraseña: la contraseña queda guardada en los datos de cloud-init.", kind="info"))
save(c, "5-paso3.svg")
