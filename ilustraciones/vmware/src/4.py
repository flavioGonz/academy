import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 4.svg: un vmk por tráfico
c = Canvas(K(), "Las IPs del propio host: un vmk por tipo de tráfico")
c.add(NOLIG)
c.add(host(48, 124, 560, 420, "Host ESXi", "adaptadores VMkernel"))
vmks = [("vmk0", "Gestión", "192.168.88.20", "Management Network", BLUE),
        ("vmk1", "Almacenamiento IP", "10.10.10.21 · MTU 9000", "Storage-VLAN30", CYAN),
        ("vmk2", "vMotion", "red privada solo de hosts", "VLAN propia", WARN)]
for i, (n, t, ip, pg, col) in enumerate(vmks):
    y = 200 + i * 108
    c.add(rect(72, y, 512, 90, "#0B3A66", col, rx=12, sw=2.5))
    c.add(rect(88, y + 22, 76, 46, col, col, rx=10))
    c.add(text(126, y + 52, n, 17, 700, WHITE, FM, anchor="middle"))
    c.add(text(184, y + 36, t, 18, 600, WHITE, FB))
    c.add(text(184, y + 60, ip, 15, 500, "#9FC3E3", FM))
    c.add(text(184, y + 80, pg, 13.5, 500, CYAN, FM))
# NAS y datastores
c.add(Server(700, 150, "NAS de prueba", "10.10.10.50"))
c.add(Cable((584, 353), (700, 192), "data", label="NFS", label_at=0.55))
c.add(cyl(700, 290, 200, 130, "nfs-lab", "NFS 3 o 4.1"))
c.add(cyl(940, 290, 212, 130, "datastore1", "VMFS"))
c.add(text(940, 456, "disco local o LUN", 15, 500, INK3, FB))
c.add(Note(640, 486, 512, "Tráfico de vMotion sin cifrar: lleva la memoria de la VM. Va en una red aislada, solo de hosts.", title="vmk2 aparte", kind="warn"))
c.add(Note(48, 566, 560, "Cada vmk con su VLAN, su subred y su prueba de vmkping.", kind="ok"))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso1: vmkping grande de punta a punta
c = Canvas(K(1), "vmkping de 8972 bytes: el MTU tiene que ser 9000 en todo")
c.add(NOLIG)
c.add(Step(48, 140, 1))
c.add(code(80, 122, 620, "vmkping -I vmk1 -d -s 8972 10.10.10.50"))
c.add(text(730, 148, "8972 + 28 de encabezados = 9000", 17, 600, INK, FM))
hops = ["vmk1", "vSwitch1", "Switch físico", "NAS"]


def fila(y, mtus, ok):
    out = [text(48, y - 14, "Todo en 9000: pasa" if ok else "Un salto en 1500: el paquete grande no pasa", 18, 600, OK if ok else ALERT, FD)]
    for i, (h, m) in enumerate(zip(hops, mtus)):
        x = 48 + i * 280
        bad = m != 9000
        out.append(rect(x, y, 220, 90, ALERT_BG if bad else WHITE, ALERT if bad else LINE2, rx=14, sw=2.5 if bad else 2))
        out.append(text(x + 20, y + 36, h, 18, 600, INK, FB))
        out.append(text(x + 20, y + 66, f"MTU {m}", 16, 700, ALERT if bad else OK, FM))
        if i < 3:
            out.append(Cable((x + 220, y + 45), (x + 280, y + 45), "ok" if ok else ("alert" if (bad or mtus[i + 1] != 9000) else "flow"), arrow=True).svg())
    return "".join(out)


c.add(fila(220, [9000, 9000, 9000, 9000], True))
c.add(fila(390, [9000, 9000, 1500, 9000], False))
c.add(Mark(1110, 265, True))
c.add(Mark(1110, 435, False))
c.add(Note(48, 510, 540, "-d prohíbe fragmentar: si algún salto tiene 1500, el ping grande se pierde y el normal anda.", title="Cómo se lee", kind="info"))
c.add(Note(612, 510, 540, "Cambiar el MTU de un vSwitch con VMs en producción puede cortar un instante: en ventana de mantenimiento.", kind="warn"))
save(c, "4-paso1.svg")

# ---------------------------------------------------------------- 4-t2: VMFS contra NFS
c = Canvas(K(), "Dos formas de datastore: VMFS y NFS")
c.add(NOLIG)


def lado(x, titulo, kind, quien, abajo, sub_abajo, conexion):
    out = [panel(x, 124, 540, 470, titulo, kind)]
    out.append(rect(x + 30, 180, 220, 70, DEEP, DEEP, rx=12))
    out.append(text(x + 50, 222, "Host ESXi", 17, 600, WHITE, FB))
    out.append(rect(x + 290, 180, 220, 70, DEEP, DEEP, rx=12))
    out.append(text(x + 310, 222, "Host ESXi", 17, 600, WHITE, FB))
    out.append(arrow((x + 140, 252), (x + 220, 318), "flow").svg())
    out.append(arrow((x + 400, 252), (x + 320, 318), "flow").svg())
    out.append(pill(x + 270, 302, conexion, BLUE, WHITE, 14))
    out.append(rect(x + 70, 324, 400, 60, SOFT, BLUE, rx=12))
    out.append(text(x + 270, 351, quien, 16, 600, INK, FB, anchor="middle"))
    out.append(text(x + 270, 373, "maneja el sistema de archivos", 14, 400, INK3, FB, anchor="middle"))
    out.append(cyl(x + 160, 400, 220, 104, abajo, sub_abajo))
    out.append(text(x + 30, 540, "Adentro, una carpeta por VM:", 15, 600, INK2, FB))
    out.append(text(x + 30, 566, ".vmx (configuración) · .vmdk y -flat.vmdk (disco)", 14.5, 500, INK, FM))
    return "".join(out)


c.add(lado(48, "VMFS: el host formatea el disco", "info", "VMFS, lo arma ESXi", "disco o LUN", "por bloques", "SAN, iSCSI o disco local"))
c.add(lado(612, "NFS: el NAS ya tiene el sistema", "info", "el NAS (su propio sistema)", "export NFS", "por archivos", "NFS 3 o 4.1 por un vmk"))
c.add(text(48, 628, "Si el datastore es compartido (LUN o NFS), varios hosts ven las mismas VMs: eso habilita vMotion y HA.", 16, 500, INK2, FB))
save(c, "4-t2.svg")
