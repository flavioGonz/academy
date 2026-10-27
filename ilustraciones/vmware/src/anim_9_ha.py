"""Teoría lección 9: HA detecta la caída de un host y reinicia sus VMs en otro: hay corte de minutos."""
from _avmw import *

a = new(24, "HA: se cae un host y sus VMs arrancan en otro")
a.steps(["Tres hosts en el clúster se vigilan entre sí.",
         "esxi-lab02 se apaga de golpe: sus VMs se caen con él.",
         "HA detecta la falla y arranca esas VMs en los otros hosts.",
         "Vuelven a andar: el corte fue lo que tardaron en arrancar."], still=2)

HX = [48, 418, 788]
for i, x in enumerate(HX):
    a.add(card(a, x, 180, 364, 300, f"esxi-lab0{i + 1}", "Cluster-Lab", dark=True))
# latidos entre hosts
a.add(a.group(line(a, "M230 452 H970", a.CYAN, 3, "4 8"), a.show(0, 25), still=0))
at(a, chip(a, 600, 400, "latidos entre hosts", "cyan", anchor="middle"), 0, 25, 0)
# VMs fijas en 1 y 3
a.add(vmbox(a, 72, 260, 316, 52, "VM ERP"))
a.add(vmbox(a, 812, 260, 316, 52, "VM acceso"))
# VMs del host 2
a.add(a.group(vmbox(a, 442, 260, 316, 52, "VM video") + vmbox(a, 442, 324, 316, 52, "VM telefonía"), a.show(0, 27), still=0))
# host 2 caído
at(a, a.box(418, 180, 364, 300, a.BADBG, a.BAD, rx=14, sw=3) + a.text(438, 214, "esxi-lab02", 19, a.BAD, a.HEAD, 600)
   + a.text(600, 340, "sin energía", 22, a.BAD, a.MONO, 700, "middle"), 25, 100, 1)
at(a, chip(a, 600, 400, "VMs caídas", "bad", anchor="middle"), 26, 50, 0)
# reinicio en 1 y 3
at(a, vmbox(a, 72, 324, 316, 52, "VM video", "arrancando…", fill=a.AMBBG, stroke=a.AMB), 52, 75, 1)
at(a, vmbox(a, 812, 324, 316, 52, "VM telefonía", "arrancando…", fill=a.AMBBG, stroke=a.AMB), 54, 75, 1)
at(a, vmbox(a, 72, 324, 316, 52, "VM video", "corriendo", stroke=a.OK), 75, 100, 0)
at(a, vmbox(a, 812, 324, 316, 52, "VM telefonía", "corriendo", stroke=a.OK), 75, 100, 0)
at(a, a.arrow("M600 300 C500 300 420 330 392 345", a.AMB, 3, "8 6") + a.arrow("M600 300 C700 300 780 330 808 345", a.AMB, 3, "8 6"), 50, 75, 1)
# reloj del corte
a.add(a.box(48, 510, 1104, 46, a.WHITE, a.LINE, rx=12))
a.add(a.text(68, 540, "servicio de VM video", 15, a.GREY, a.MONO, 600))
a.add(a.box(280, 520, 852, 26, a.OKBG, None, rx=8))
k = a.keyframes([(0, 0.0001), (25, 0.0001), (27, 0.02), (75, 0.45), (100, 0.45)], "transform", "scaleX({})")
a.add(a.group(a.box(500, 520, 852, 26, a.BAD, None, rx=8), k, still=0, origin="500px 520px"))
a.add(a.group(a.box(500, 520, 383, 26, a.BAD, None, rx=8), a.keyframes([(0, 0), (100, 0)]), still=1))
at(a, a.text(700, 539, "minutos sin servicio", 14, "#FFFFFF", a.MONO, 700, "middle"), 50, 100, 1)
caption(a, 610, [(0, 25, "HA es una configuración del clúster: activarla depende de la licencia.", None),
                 (25, 50, "No hay magia: lo que corría en ese host se cae con él.", a.BAD),
                 (50, 75, "Esto lo hacen los hosts: funciona aunque vCenter esté caído.", a.AMB),
                 (75, 100, "HA reinicia en otro host. No evita el corte: lo acorta.", a.OK)], still=2)
write(a, "9-t2.svg", "HA: se cae un host y sus VMs arrancan en otro",
      "Animación en cuatro tiempos con tres hosts de un clúster: esxi-lab01 con la VM ERP, esxi-lab02 con VM video y VM telefonía, esxi-lab03 con VM acceso. "
      "1: los hosts se vigilan entre sí con latidos. 2: esxi-lab02 se queda sin energía y sus dos VMs se caen. "
      "3: HA detecta la falla y arranca VM video en esxi-lab01 y VM telefonía en esxi-lab03, aunque vCenter esté caído. "
      "4: las VMs vuelven a andar; una barra abajo muestra los minutos sin servicio: HA no evita el corte, lo acorta.")
