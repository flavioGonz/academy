"""Teoría lección 4: qué es una VM en Proxmox (KVM + QEMU) y por qué VirtIO."""
from _apmx import *

a = new(20, "KVM y QEMU: qué es una VM por dentro")
a.steps(["El CPU con VT-x o AMD-V sabe correr una VM.",
         "El kernel de Proxmox carga KVM: cada VM es un proceso QEMU.",
         "Adentro corre otro kernel, directo sobre el CPU real.",
         "Disco y red: con VirtIO, sin imitar hardware viejo."], still=2)
# pila
a.add(a.box(48, 516, 600, 60, a.SLATE, a.LINE, rx=12) + a.text(348, 552, "Hardware · CPU con VT-x o AMD-V", 18, a.INK, a.SANS, 600, "middle"))
a.add(a.box(48, 440, 600, 60, a.INK, None, rx=12) + a.text(348, 470, "Kernel Linux de Proxmox VE", 18, "#FFFFFF", a.SANS, 600, "middle")
      + a.text(348, 491, "con el módulo KVM", 15, "#9FC3E3", a.MONO, 400, "middle"))
at(a, a.box(46, 514, 604, 64, "none", a.CYAN, rx=13, sw=4), 0, 25, 0)
for i, (vm, os_) in enumerate([("VM 100", "kernel Windows"), ("VM 101", "kernel Linux")]):
    x = 48 + i * 308
    g = a.box(x, 180, 292, 244, "#FFFFFF", a.BLUE, rx=14, sw=2) + a.text(x + 18, 210, "proceso QEMU · " + vm, 17, a.BLUE, a.MONO, 700)
    at(a, g, 25, 100, 1)
    inner = (a.box(x + 16, 228, 260, 54, "#E5F0FB", a.LINE, rx=10) + a.text(x + 146, 261, "aplicaciones", 16, a.INK, a.SANS, 600, "middle")
             + a.box(x + 16, 292, 260, 54, a.NAVY2, None, rx=10) + a.text(x + 146, 325, os_, 16, "#FFFFFF", a.SANS, 600, "middle"))
    at(a, inner, 50, 100, 1)
    at(a, a.box(x + 16, 356, 260, 52, a.AMBBG, a.AMB, rx=10, sw=2) + a.text(x + 146, 388, "disco y placa virtuales", 15, a.AMB, a.SANS, 700, "middle"), 75, 100, 0)
# flecha vCPU directa
at(a, a.arrow("M162 346 V 512", a.OK, 4) + chip(a, 174, 362, "vCPU", "ok"), 50, 75, 1)
# panel derecho
PX = 690
for s, e, t, body, col, st in [
    (0, 25, "La base", ["Las extensiones de virtualización", "del procesador dejan correr el código", "de la VM sin traducirlo."], None, 0),
    (25, 50, "Una VM, un proceso", ["Para el host, cada VM es un proceso", "QEMU: lo ves con su VMID y se", "mata, migra o respalda como tal."], None, 0),
    (50, 75, "Kernel propio", ["La VM arranca su propio kernel.", "Por eso corre Windows o cualquier", "Linux, y aísla más que un contenedor."], a.OK, 1)]:
    g = a.text(PX, 214, t, 22, col or a.INK, a.HEAD, 600)
    for j, ln in enumerate(body):
        g += a.text(PX, 254 + j * 28, ln, 17, a.TXT, a.SANS, 500)
    at(a, g, s, e, st)
g4 = a.text(PX, 214, "Dos formas de dar un disco", 22, a.INK, a.HEAD, 600)
g4 += a.box(PX, 236, 462, 104, a.AMBBG, a.AMB, rx=12) + a.text(PX + 18, 268, "Emulado (IDE)", 17, a.AMB, a.SANS, 700)
g4 += a.text(PX + 18, 294, "QEMU imita un disco real y traduce", 15, a.TXT, a.SANS, 500) + a.text(PX + 18, 316, "cada acceso: anda en todo, rinde poco.", 15, a.TXT, a.SANS, 500)
g4 += a.box(PX, 352, 462, 104, a.OKBG, a.OK, rx=12) + a.text(PX + 18, 384, "VirtIO (paravirtual)", 17, a.OK, a.SANS, 700)
g4 += a.text(PX + 18, 410, "El invitado sabe que es virtual y deja", 15, a.TXT, a.SANS, 500) + a.text(PX + 18, 432, "los pedidos en colas compartidas.", 15, a.TXT, a.SANS, 500)
at(a, g4, 75, 100, 0)
caption(a, 626, [(0, 25, "Sin VT-x o AMD-V en el BIOS, Proxmox no puede usar KVM: primero se habilita ahí.", None),
                 (25, 50, "KVM está en el kernel del host; QEMU pone el resto: memoria, discos, placas y consola.", None),
                 (50, 75, "Las instrucciones del invitado corren en el CPU real: casi sin pérdida de velocidad.", a.OK),
                 (75, 100, "Windows no trae los drivers VirtIO: por eso el ISO virtio-win en la instalación.", a.AMB)], still=2)
write(a, "4-t1.svg", "KVM y QEMU: qué es una VM por dentro",
      "Animación en cuatro tiempos de la pila de virtualización de Proxmox VE. 1: abajo, el hardware con un CPU que tiene VT-x o AMD-V. "
      "2: encima, el kernel Linux de Proxmox con el módulo KVM; cada VM aparece como un proceso QEMU, uno para la VM 100 y otro para la VM 101. "
      "3: dentro de cada proceso corre el kernel propio del invitado, Windows o Linux, con sus aplicaciones, y las vCPU ejecutan directo sobre el CPU real. "
      "4: disco y placa son virtuales: emulados como IDE, QEMU imita un disco real y traduce cada acceso; con VirtIO el invitado sabe que es virtual y usa colas compartidas, y en Windows eso pide los drivers virtio-win.")
