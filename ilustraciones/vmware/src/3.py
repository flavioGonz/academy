import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 3.svg: vSwitch, port groups y uplinks
c = Canvas(K(), "Adentro del host: vSwitch, port groups y uplinks")
c.add(NOLIG)
c.add(host(48, 124, 790, 372, "Host ESXi", "esxi-lab01"))
# vSwitch0: gestión
c.add(rect(72, 200, 250, 92, "#0B3A66", "#4E7396", rx=12))
c.add(text(90, 230, "Management Network", 16, 600, WHITE, FB))
c.add(text(90, 254, "vmk0 · 192.168.88.20", 14, 500, "#9FC3E3", FM))
c.add(text(90, 278, "VLAN 0 (sin etiqueta)", 14, 500, CYAN, FM))
c.add(rect(72, 330, 250, 50, "#0E4A80", CYAN, rx=10))
c.add(text(197, 362, "vSwitch0", 17, 700, WHITE, FM, anchor="middle"))
c.add(f'<path d="M197 292V330" stroke="{CYAN}" stroke-width="3"/>')
c.add(nicport(149, 420, "vmnic0"))
c.add(f'<path d="M197 380V420" stroke="{CYAN}" stroke-width="3"/>')
# vSwitch1: VMs en VLAN 20
c.add(vm(370, 158, 196, 58, "VM video", "srv-video", dark=True))
c.add(vm(610, 158, 196, 58, "VM acceso", "srv-acceso", dark=True))
c.add(rect(370, 236, 436, 56, "#0B3A66", CYAN, rx=12))
c.add(text(390, 270, "Port group VM-VLAN20", 16, 600, WHITE, FB))
c.add(text(788, 270, "VLAN 20", 15, 700, CYAN, FM, anchor="end"))
c.add(f'<path d="M468 216V236M708 216V236" stroke="{CYAN}" stroke-width="3"/>')
c.add(rect(370, 330, 436, 50, "#0E4A80", CYAN, rx=10))
c.add(text(588, 362, "vSwitch1", 17, 700, WHITE, FM, anchor="middle"))
c.add(f'<path d="M588 292V330" stroke="{CYAN}" stroke-width="3"/>')
c.add(nicport(430, 420, "vmnic2"))
c.add(nicport(650, 420, "vmnic3"))
c.add(f'<path d="M478 380V420M698 380V420" stroke="{CYAN}" stroke-width="3"/>')
# switch físico
c.add(rect(48, 548, 790, 92, WHITE, LINE2, rx=16))
c.add(text(68, 580, "Switch físico", 18, 600, INK, FD))
for x, lab, kind in [(149, "acceso", "gray"), (430, "troncal", "info"), (650, "troncal", "info")]:
    c.add(rect(x, 590, 96, 38, SOFT if kind == "info" else GROUND, BLUE if kind == "info" else LINE2, rx=8))
    c.add(mid(x + 48, 615, lab, 14, 600, BLUE if kind == "info" else INK3, FM))
for x in (197, 478, 698):
    c.add(Cable((x, 460), (x, 590), "data"))
c.add(Note(866, 124, 286, "Un enchufe virtual con su VLAN ID. Las VMs y los vmk se conectan ahí, no al vSwitch directo.", title="Port group", kind="info"))
c.add(Note(866, 300, 286, "Dos placas a dos bocas: si se suelta un cable, el tráfico sigue por la otra.", title="Dos uplinks", kind="ok"))
c.add(Note(866, 450, 286, "La VLAN de Management Network se cambia solo con iLO, iDRAC o la pantalla abierta.", title="Ojo con gestión", kind="warn"))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso1: troncal y prueba de failover
c = Canvas(K(1), "Troncal en el switch, ping y un cable afuera")
c.add(NOLIG)
c.add(Step(48, 140, 1))


def lado(x, cortado):
    out = [panel(x, 160, 540, 330, "Desenchufás vmnic3" if cortado else "Con los dos cables", "warn" if cortado else "info")]
    out.append(vm(x + 30, 210, 210, 60, "VM de prueba", "VM-VLAN20"))
    out.append(rect(x + 30, 300, 480, 46, DEEP, DEEP, rx=10))
    out.append(text(x + 270, 330, "vSwitch1", 16, 700, WHITE, FM, anchor="middle"))
    out.append(f'<path d="M{x + 135} 270V300" stroke="{BLUE}" stroke-width="3"/>')
    out.append(nicport(x + 90, 372, "vmnic2"))
    out.append(nicport(x + 330, 372, "vmnic3", ALERT if cortado else None))
    out.append(f'<path d="M{x + 138} 346V372M{x + 378} 346V372" stroke="{BLUE}" stroke-width="3"/>')
    out.append(Cable((x + 138, 412), (x + 138, 470), "data").svg())
    if cortado:
        out.append(f'<path d="M{x + 378} 412V432" stroke="{BLUE}" stroke-width="4"/><path d="M{x + 378} 452V470" stroke="{BLUE}" stroke-width="4"/>')
        out.append(Mark(x + 430, 442, False))
    else:
        out.append(Cable((x + 378, 412), (x + 378, 470), "data").svg())
    out.append(rect(x + 30, 470, 480, 4, LINE2, LINE2, rx=2))
    out.append(tag(x + 400, 252, "ping 0 % perdido" if not cortado else "ping sigue", "ok"))
    return "".join(out)


c.add(lado(48, False))
c.add(lado(612, True))
c.add(text(48, 520, "Puertos del switch: troncal con la VLAN 20 permitida", 17, 600, INK, FB))
c.add(code(48, 538, 700, "esxcli network vswitch standard policy failover get -v vSwitch1"))
c.add(text(48, 612, "Antes de desenchufar, revisá que los dos uplinks figuren como activos.", 16, 400, INK2, FB))
c.add(Note(790, 520, 362, "Si al desenchufar se corta el ping, falta permitir la VLAN 20 en esa boca.", kind="warn"))
save(c, "3-paso1.svg")
