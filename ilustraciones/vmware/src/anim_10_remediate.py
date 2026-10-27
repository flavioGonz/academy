"""Teoría lección 10: stage primero en todos, después remediar de a un host con sus VMs movidas."""
from _avmw import *

a = new(24, "Remediar un clúster: de a un host, sin cortar las VMs")
a.steps(["Stage: los paquetes bajan a los tres hosts, todavía sin aplicar.",
         "esxi-lab01 entra en mantenimiento: sus VMs se mueven con vMotion.",
         "Sin VMs encima, se aplica el parche y el host reinicia.",
         "Vuelve actualizado y sale de mantenimiento; sigue el próximo host."], still=1)

HX = [48, 418, 788]
for i, x in enumerate(HX):
    a.add(card(a, x, 180, 364, 300, f"esxi-lab0{i + 1}", None, dark=True))
    a.add(a.text(x + 20, 236, "8.0 U3", 15, "#9FC3E3", a.MONO))
# versión nueva en host 1
at(a, a.box(60, 220, 200, 26, "#0B3A66", None, rx=6) + a.text(68, 238, "8.0 U3 + parche", 15, "#9FE3F7", a.MONO, 700), 80, 100, 0)
# paquetes stage
for i, x in enumerate(HX):
    pk = a.box(x + 236, 196, 108, 30, "#FFB020", None, rx=8) + a.text(x + 290, 216, "paquetes", 14, a.INK, a.MONO, 700, "middle")
    a.add(a.group(pk, a.move([(0, 0, -24), (3 + i * 4, 0, -24), (9 + i * 4, 0, 0), (100, 0, 0)]), a.keyframes([(0, 0), (3 + i * 4, 0), (4 + i * 4, 1), (100, 1)]), still=0))
    a.add(a.group(pk, a.keyframes([(0, 0), (100, 0)]), still=1))
# VMs: dos en host 1 que se mueven a 2 y 3
a.add(vmbox(a, 442, 270, 316, 52, "VM acceso"))
a.add(vmbox(a, 812, 270, 316, 52, "VM telefonía"))
a.add(a.group(vmbox(a, 0, 0, 316, 52, "VM video"), a.move([(0, 72, 270), (28, 72, 270), (40, 442, 336), (100, 442, 336)]), still=1))
a.add(a.group(vmbox(a, 0, 0, 316, 52, "VM ERP"), a.move([(0, 72, 336), (31, 72, 336), (44, 812, 336), (100, 812, 336)]), still=1))
# mantenimiento
at(a, a.box(48, 180, 364, 300, "none", a.AMB, rx=14, sw=4) + chip(a, 72, 420, "modo mantenimiento", "amb"), 26, 84, 1)
at(a, a.text(230, 330, "aplicando parche", 18, "#FFD27A", a.MONO, 700, "middle") + a.text(230, 360, "reinicio", 18, "#FFD27A", a.MONO, 700, "middle"), 52, 78, 0)
at(a, chip(a, 72, 420, "actualizado", "ok"), 84, 100, 0)
at(a, a.box(418, 180, 364, 300, "none", a.CYAN, rx=14, sw=3, extra='stroke-dasharray="8 6"') + chip(a, 442, 420, "el próximo", "cyan"), 84, 100, 0)
caption(a, 540, [(0, 25, "El staging no corta nada: por eso se hace antes y en todos.", None),
                 (25, 50, "Con DRS el movimiento es automático; sin DRS, se mueven a mano o se apagan.", None),
                 (50, 75, "Las VMs siguen andando en los otros hosts mientras este reinicia.", a.OK),
                 (75, 100, "Un host por vez: siempre queda capacidad para las VMs.", a.OK)], still=1)
a.add(a.box(48, 580, 1104, 52, a.BADBG, a.BAD, rx=12))
a.add(a.text(70, 612, "Antes de empezar: backup del vCenter, de la configuración de cada host y de las VMs críticas.", 16, a.BAD, a.SANS, 600))
write(a, "10-t1.svg", "Remediar un clúster: de a un host, sin cortar las VMs",
      "Animación en cuatro tiempos con tres hosts en 8.0 U3. 1: en el staging, los paquetes bajan a los tres hosts sin aplicarse. "
      "2: esxi-lab01 entra en modo mantenimiento y sus dos VMs, video y ERP, se mueven con vMotion a los otros hosts. "
      "3: sin VMs encima se aplica el parche y el host reinicia, mientras las VMs siguen andando en los otros. "
      "4: el host vuelve actualizado, sale de mantenimiento y el siguiente host queda marcado como el próximo. Abajo, el recordatorio de hacer backup antes de empezar.")
