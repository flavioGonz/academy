"""Teoría lección 2: hipervisor tipo 2 contra tipo 1, y por qué ESXi pide hardware de la lista."""
from _avmw import *

a = new(20, "Hipervisor tipo 1: ESXi va directo sobre el hierro")
a.steps(["Tipo 2: la VM pasa por el hipervisor y por el sistema operativo de la PC.",
         "Tipo 1: la VM pasa solo por ESXi, que está instalado sobre el servidor.",
         "Con VT-x o AMD-V, el código de la VM corre en la CPU real.",
         "ESXi trae sus propios drivers: por eso NIC y controladora van en la lista."], still=1)


def stack(x, layers, title, hi=None):
    s = a.text(x, 196, title, 20, a.INK, a.HEAD, 600)
    y = 214
    for name, sub, kind in layers:
        fill, stroke, tc = {"vm": (a.WHITE, a.LINE, a.INK), "hv": (a.INK, a.INK, "#FFFFFF"), "os": (a.SLATE, a.LINE, a.INK), "hw": ("#E5F0FB", a.BLUE, a.INK)}[kind]
        s += a.box(x, y, 500, 74, fill, stroke, rx=12)
        s += a.text(x + 20, y + 32, name, 18, tc, a.SANS, 600) + a.text(x + 20, y + 56, sub, 14, "#9FC3E3" if kind == "hv" else a.GREY, a.MONO)
        y += 86
    return s


T2 = [("VM", "Windows o Linux invitado", "vm"), ("Hipervisor tipo 2", "programa, ej. Workstation", "hv"), ("Sistema operativo de la PC", "Windows, macOS o Linux", "os"), ("Hardware", "CPU · RAM · disco · NIC", "hw")]
T1 = [("VM", "servidor de video, ERP…", "vm"), ("ESXi (VMkernel)", "hipervisor tipo 1", "hv"), ("Hardware del servidor", "CPU · RAM · controladora · NIC", "hw")]
a.add(stack(48, T2, "Tipo 2 (PC de escritorio)"))
a.add(stack(652, T1, "Tipo 1 (servidor)"))
# paquete tipo 2
mv = a.move([(0, 400, 250), (3, 400, 250), (8, 400, 336), (14, 400, 422), (20, 400, 508), (25, 400, 508), (100, 400, 508)])
op = a.keyframes([(0, 0), (2, 0), (3, 1), (23, 1), (25, 0), (100, 0)])
a.add(a.group(f'<circle cx="0" cy="0" r="12" fill="#FFB020" stroke="#fff" stroke-width="3"/>', mv, op, still=0))
# paquete tipo 1
mv = a.move([(0, 1000, 250), (28, 1000, 250), (35, 1000, 336), (43, 1000, 422), (50, 1000, 422), (100, 1000, 422)])
op = a.keyframes([(0, 0), (27, 0), (28, 1), (48, 1), (50, 0), (100, 0)])
a.add(a.group(f'<circle cx="0" cy="0" r="12" fill="#FFB020" stroke="#fff" stroke-width="3"/>', mv, op, still=0))
at(a, chip(a, 48, 572, "3 capas hasta el hardware", "amb"), 0, 25, 0)
at(a, chip(a, 652, 486, "1 capa hasta el hardware", "ok"), 25, 50, 1)
# VT-x: atajo directo a la CPU, trampa al VMkernel
vt = a.arrow("M1110 262 C1170 300 1170 380 1112 420", a.OK, 4)
vt += chip(a, 652, 486, "código normal: directo a la CPU", "ok")
vt += a.arrow("M650 250 C606 270 606 320 646 338", a.AMB, 3, "6 5")
vt += chip(a, 652, 530, "instrucción sensible: trampa a ESXi", "amb")
at(a, vt, 50, 75, 0)
# drivers
drv = a.box(652, 310, 500, 74, a.INK, a.CYAN, rx=12, sw=4) + a.text(672, 342, "ESXi (VMkernel)", 18, "#FFFFFF", a.SANS, 600) + a.text(672, 366, "drivers propios de NIC y controladora", 14, "#9FE3F7", a.MONO, 600)
drv += chip(a, 652, 486, "driver no incluido = la placa no aparece", "bad")
at(a, drv, 75, 100, 0)
caption(a, 630, [(0, 25, "Sirve en la notebook del técnico, no en el servidor de un cliente.", None),
                 (25, 50, "No hay Windows ni Linux debajo de ESXi: menos capas, menos cosas que se rompen.", a.OK),
                 (50, 75, "Por eso el BIOS tiene que tener VT-x o AMD-V y NX/XD habilitados.", None),
                 (75, 100, "La Compatibility Guide dice qué CPU, NIC y controladora tienen driver y soporte.", a.BAD)], still=1)
write(a, "2-t1.svg", "Hipervisor tipo 1: ESXi va directo sobre el hierro",
      "Animación en cuatro tiempos con dos pilas de capas. A la izquierda, tipo 2: VM, hipervisor tipo 2 como Workstation, sistema operativo de la PC y hardware. "
      "A la derecha, tipo 1: VM, ESXi (VMkernel) y hardware del servidor. 1: un pedido de la VM baja tres capas hasta el hardware en el tipo 2. "
      "2: en el tipo 1 baja una sola capa. 3: con VT-x o AMD-V el código normal de la VM corre directo en la CPU y las instrucciones sensibles saltan como trampa a ESXi. "
      "4: ESXi trae sus propios drivers de NIC y controladora; si un driver no está incluido, la placa no aparece, y por eso se mira la Compatibility Guide.")
