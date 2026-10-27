"""Teoría lección 12: importación en frío con el importador ESXi de Proxmox VE."""
from _avmw import *

a = new(24, "Importar en frío: de ESXi a Proxmox, nunca las dos prendidas")
a.steps(["En el ESXi: VM apagada, sin VMware Tools y con la red anotada.",
         "Proxmox se conecta al host ESXi como storage, no a vCenter.",
         "Copia los discos: de a pocos, no más de cuatro a la vez.",
         "La VM arranca en Proxmox; en ESXi queda apagada como vuelta atrás."], still=2)

a.add(card(a, 48, 180, 470, 340, "ESXi de laboratorio", "192.168.88.20", dark=True))
a.add(card(a, 682, 180, 470, 340, "Proxmox VE", "storage esxi-lab", dark=True))
# VM en ESXi
a.add(vmbox(a, 76, 260, 414, 64, "vm-prueba", "apagada · sin Tools", fill=a.SLATE))
a.add(a.box(76, 344, 414, 46, a.NAVY2, "#4E7396", rx=10) + a.text(96, 373, "IP, máscara, gateway y DNS anotados", 14, "#9FC3E3", a.MONO))
# discos
for k in range(3):
    a.add(a.box(96 + k * 130, 420, 110, 70, "#E5F0FB", a.BLUE, rx=10) + a.text(151 + k * 130, 462, f"disco {k + 1}", 15, a.INK, a.MONO, 600, "middle"))
# conexión
at(a, line(a, "M518 300H682", a.CYAN, 4, "8 6") + chip(a, 600, 256, "API del host ESXi", "cyan", anchor="middle"), 25, 100, 1)
at(a, chip(a, 600, 536, "vCenter: mucho más lento", "bad", anchor="middle"), 25, 50, 0)
# copia de discos
for k in range(3):
    t0 = 52 + k * 5
    a.add(a.group(a.box(-55, -35, 110, 70, "#FFB020", a.AMB, rx=10) + a.text(0, 7, f"disco {k + 1}", 15, a.INK, a.MONO, 700, "middle"),
                  a.move([(0, 151 + k * 130, 455), (t0, 151 + k * 130, 455), (t0 + 8, 785 + k * 130, 455), (100, 785 + k * 130, 455)]),
                  a.keyframes([(0, 0), (t0 - 1, 0), (t0, 1), (100, 1)]), still=0))
a.add(a.group("".join(a.box(730 + k * 130, 420, 110, 70, "#FFB020", a.AMB, rx=10) + a.text(785 + k * 130, 462, f"disco {k + 1}", 15, a.INK, a.MONO, 700, "middle") for k in range(3)),
              a.keyframes([(0, 0), (100, 0)]), still=1))
# VM en Proxmox
at(a, vmbox(a, 710, 260, 414, 64, "vm-prueba", "corriendo · VirtIO o SATA", stroke=a.OK), 75, 100, 0)
at(a, a.box(710, 344, 414, 46, a.NAVY2, a.OK, rx=10) + a.text(730, 373, "bridge vmbr0 · agente QEMU", 14, "#9FE3F7", a.MONO), 75, 100, 0)
at(a, chip(a, 76, 196 + 340, "queda apagada: vuelta atrás", "ok"), 75, 100, 0)
caption(a, 600, [(0, 25, "Tools se desinstala antes; el vTPM no se migra: claves de BitLocker a mano.", None),
                 (25, 50, "El importador habla con el host ESXi; no depende del VDDK que Broadcom retiró.", None),
                 (50, 75, "En frío: si algo falla, no se pierde nada de lo escrito.", a.OK),
                 (75, 100, "Nunca encendida en los dos lados a la vez: misma IP, mismo nombre.", a.BAD)], still=2)
write(a, "12-t1.svg", "Importar en frío: de ESXi a Proxmox, nunca las dos prendidas",
      "Animación en cuatro tiempos con un ESXi de laboratorio a la izquierda y un Proxmox VE a la derecha. "
      "1: en el ESXi, la VM vm-prueba está apagada, sin VMware Tools y con su configuración de red anotada; tiene tres discos. "
      "2: Proxmox se conecta al host ESXi por su API como storage esxi-lab; pasar por vCenter sería mucho más lento. "
      "3: los discos se copian de a pocos, no más de cuatro a la vez, con la VM apagada. "
      "4: la VM arranca en Proxmox en el bridge vmbr0 con el agente QEMU, y en el ESXi queda apagada como vuelta atrás; nunca encendida en los dos lados a la vez.")
