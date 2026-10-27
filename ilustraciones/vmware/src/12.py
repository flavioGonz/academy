import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 12.svg: renovar o migrar, con números
c = Canvas(K(), "¿Renovar o migrar? Tres preguntas con números")
c.add(NOLIG)
qs = [("1", "Núcleos", "físicos contra licenciables: ¿cuánto pagás de más por el mínimo de 16?"),
      ("2", "Funciones", "¿usa de verdad vSAN, NSX o DRS, o solo el hipervisor?"),
      ("3", "Piloto", "un host no crítico, 2 o 3 VMs, backup y restauración probados")]
for i, (n, t, s) in enumerate(qs):
    x = 48 + i * 376
    c.add(panel(x, 124, 352, 160, None, "info"))
    c.add(badge(x + 38, 164, n, BLUE, 20, 18))
    c.add(text(x + 70, 171, t, 21, 600, INK, FD))
    sv, _ = wrap(x + 22, 214, s, 312, 16, 400, INK2)
    c.add(sv)
c.add(panel(48, 312, 540, 190, "Renovar tiene sentido si…", "ok"))
c.add(bullet_list(68, 372, [("la relación físicos y licenciables está cerca de 1 a 1", "ok"), ("se usa el stack: vSAN, NSX, DRS", "ok"), ("hay apps certificadas solo para vSphere", "ok")], 500, 16, 8)[0])
c.add(panel(612, 312, 540, 190, "Conviene cotizar alternativa si…", "warn"))
c.add(bullet_list(632, 372, [("son 2 a 10 hosts con CPUs de menos de 16 núcleos", "warn"), ("solo se usa el hipervisor", "warn"), ("el costo subió y no hay funciones nuevas que lo paguen", "warn")], 500, 16, 8)[0])
c.add(rect(48, 526, 1104, 104, DEEP, DEEP, rx=16))
c.add(text(76, 568, "Ninguna migración arranca sin:", 19, 600, WHITE, FD))
for i, s in enumerate(["piloto", "backup verificado", "vuelta atrás"]):
    c.add(tag(400 + i * 230, 570, s, "cyan", anchor="start"))
c.add(text(76, 604, "Broadcom recomienda VCF 9 o VVF 9; Introserv y Redress dicen que en clientes chicos la cuenta suele no cerrar.", 15, 400, "#9FC3E3", FB))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso2: storage ESXi en Proxmox
c = Canvas(K(2), "En Proxmox: Datacenter > Storage > Add > ESXi")
c.add(NOLIG)
c.add(Step(48, 140, 2))
c.add(Window(48, 164, 560, 330, "Add: ESXi", [("ID", "esxi-lab"), ("Server", "192.168.88.20"), ("Username", "root"), ("Password", "la del root del ESXi"), ("Skip Certificate Verification", "marcado")], hl=4))
c.add(Server(700, 180, "Proxmox VE", "8 o 9 de laboratorio", w=260))
c.add(Server(700, 380, "ESXi de laboratorio", "192.168.88.20", w=260))
c.add(arrow((820, 266), (820, 376), "flow", label="directo al host", label_dy=0, label_at=0.5))
c.add(Note(980, 164, 172, "Contra el host, no contra vCenter: mucho más rápido.", kind="ok", size=15))
c.add(Note(980, 380, 172, "Marcalo solo si el ESXi usa certificado autofirmado.", kind="warn", size=15))
c.add(Note(48, 520, 1104, "Después aparece esxi-lab en el árbol: elegís la VM apagada, Import, storage de destino y bridge vmbr0 (paso 3).", kind="info"))
save(c, "12-paso2.svg")

# ---------------------------------------------------------------- 12-paso4: disco y drivers al arrancar
c = Canvas(K(4), "Si no arranca: el controlador de disco")
c.add(NOLIG)
c.add(Step(48, 140, 4))


def flujo(x, titulo, pasos, kind):
    out = [panel(x, 164, 540, 340, titulo, kind)]
    for i, (s, k) in enumerate(pasos):
        y = 220 + i * 98
        bg, fg = {"info": (SOFT, BLUE), "ok": (OK_BG, OK), "warn": (WARN_BG, WARN)}[k]
        out.append(rect(x + 24, y, 492, 74, bg, fg, rx=12, sw=1.8))
        sv, _ = wrap(x + 44, y + 32, s, 452, 16, 500, INK)
        out.append(sv)
        if i < len(pasos) - 1:
            out.append(arrow((x + 270, y + 76), (x + 270, y + 96), "flow").svg())
    return "".join(out)


c.add(flujo(48, "Linux", [("Arrancá con el disco en VirtIO SCSI", "info"), ("¿No bootea? Probá el disco en SATA", "warn"), ("Reconfigurá la IP si la placa cambió de nombre e instalá el agente QEMU", "ok")], "info"))
c.add(flujo(612, "Windows", [("Arrancá con el disco en SATA", "info"), ("Instalá los drivers VirtIO desde adentro", "warn"), ("Cambiá a VirtIO, reconfigurá la IP e instalá el agente QEMU", "ok")], "info"))
c.add(text(48, 560, "Verificá desde la consola de la VM: ip a y ping -c 3 192.168.88.1 (paso 5).", 17, 600, BLUE, FB))
save(c, "12-paso4.svg")
