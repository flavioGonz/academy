"""Teoría lección 12: upgrade mayor de un clúster, un nodo por vez."""
from _apmx import *

a = new(24, "Upgrade de 8 a 9 en un clúster: un nodo por vez")
a.steps(["Vaciás pve1: sus VMs migran en vivo a pve2 y pve3.",
         "pve1 sin VMs: pve8to9 --full, upgrade, reinicio y control.",
         "Las VMs de pve2 van a pve1 (de 8 a 9 siempre anda).",
         "Lo mismo con pve3. Nunca dos nodos a la vez."], still=3)
NX = [48, 432, 816]
for i, x in enumerate(NX):
    a.add(card(a, x, 180, 336, 290, f"pve{i + 1}", None, dark=True))


def ver(i, s, e, label, kind, still=0):
    at(a, chip(a, NX[i] + 316, 196, label, kind, 16, anchor="end", h=32), s, e, still)


ver(0, 0, 25, "8.4", "grey"); ver(0, 25, 40, "actualizando", "amb"); ver(0, 40, 100, "9", "ok", 1)
ver(1, 0, 62, "8.4", "grey"); ver(1, 62, 70, "actualizando", "amb"); ver(1, 70, 100, "9", "ok", 1)
ver(2, 0, 87, "8.4", "grey"); ver(2, 87, 94, "actualizando", "amb"); ver(2, 94, 100, "9", "ok", 1)
SL = lambda n, k: (NX[n] + 168, 290 + k * 64)


def vm(name, path):
    pts = []
    for t, n, k in path:
        x, y = SL(n, k)
        pts.append((t, x, y))
    inner = a.box(-120, -24, 240, 48, "#E5F0FB", a.BLUE, rx=10, sw=2) + a.text(0, 7, name, 17, a.INK, a.MONO, 700, "middle")
    # en movimiento no se ve en el cuadro fijo; el fijo muestra la posición final (tiempo 4)
    fx, fy = pts[-1][1], pts[-1][2]
    final = f'<g transform="translate({fx} {fy})">{inner}</g>'
    return a.group(inner, a.move(pts), still=0) + a.group(final, a.keyframes([(0, 0), (100, 0)]), still=1)


a.add(vm("VM A", [(0, 0, 0), (5, 0, 0), (20, 1, 1), (52, 1, 1), (62, 0, 0), (100, 0, 0)]))
a.add(vm("VM B", [(0, 0, 1), (5, 0, 1), (20, 2, 1), (77, 2, 1), (87, 1, 0), (100, 1, 0)]))
a.add(vm("VM C", [(0, 1, 0), (52, 1, 0), (62, 0, 1), (100, 0, 1)]))
a.add(vm("VM D", [(0, 2, 0), (77, 2, 0), (87, 1, 1), (100, 1, 1)]))
at(a, chip(a, NX[0] + 168, 420, "vacío: listo para actualizar", "amb", anchor="middle"), 20, 40, 0)
at(a, chip(a, NX[1] + 168, 420, "vacío: se actualiza", "amb", anchor="middle"), 62, 75, 0)
at(a, chip(a, NX[2] + 168, 420, "vacío: se actualiza", "amb", anchor="middle"), 87, 100, 1)
at(a, a.text(600, 520, "de 9 a 8.4: no soportado", 17, a.BAD, a.SANS, 700, "middle"), 50, 75, 0)
caption(a, 604, [(0, 25, "Antes de empezar: backup probado de todo y pve8to9 --full limpio en cada nodo.", None),
                 (25, 50, "Por SSH con tmux o por IPMI: la consola de la GUI se corta en medio del upgrade.", a.AMB),
                 (50, 75, "Migrar de una versión vieja a una nueva siempre funciona; al revés, no está garantizado.", a.OK),
                 (75, 100, "Un nodo por vez y verificando cada uno: el clúster nunca pierde más de un voto.", a.OK)], still=3)
write(a, "12-t1.svg", "Upgrade de 8 a 9 en un clúster: un nodo por vez",
      "Animación en cuatro tiempos de un clúster de tres nodos en Proxmox VE 8.4 con cuatro VM. "
      "1: las VM A y B migran en vivo de pve1 a pve2 y pve3, y pve1 queda vacío. "
      "2: pve1 se actualiza a la 9 con pve8to9 --full antes, durante y después, se reinicia y se controla. "
      "3: las VM A y C, que estaban en pve2, migran a pve1, porque de 8.4 a 9 siempre funciona; pve2 queda vacío y se actualiza. Migrar de 9 a 8.4 no está soportado. "
      "4: las VM B y D pasan de pve3 a pve2 y pve3 se actualiza. Al final los tres nodos están en la 9 y nunca hubo dos actualizándose a la vez.", pcts=(10, 37, 62, 96))
