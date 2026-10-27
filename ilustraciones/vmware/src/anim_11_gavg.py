"""Teoría lección 11: GAVG = KAVG + DAVG. Dónde se pierde el tiempo de una lectura."""
from _avmw import *

a = new(20, "GAVG = KAVG + DAVG: dónde se va el tiempo de un disco")
a.steps(["La VM pide una lectura: arranca el reloj de GAVG.",
         "Pasa por el VMkernel del host: eso es KAVG, debería ser casi cero.",
         "Llega al almacenamiento y vuelve: eso es DAVG.",
         "Si DAVG es el grande, el problema está en el storage, no en el host."], still=2)

a.add(vmbox(a, 48, 220, 260, 70, "VM", "pide una lectura"))
a.add(card(a, 420, 200, 300, 110, "VMkernel", "cola del host", dark=True))
a.add(card(a, 840, 200, 312, 110, "Almacenamiento", "SAN, iSCSI, NFS o disco"))
a.add(line(a, "M308 255H420", a.BLUE, 3) + line(a, "M720 255H840", a.BLUE, 3))
# viaje de la lectura
a.add(a.group('<circle r="12" fill="#FFB020" stroke="#fff" stroke-width="3"/>',
              a.move([(0, 290, 255), (4, 290, 255), (22, 570, 255), (30, 570, 255), (45, 1100, 282), (62, 1100, 282), (72, 570, 255), (80, 290, 255), (100, 290, 255)]),
              a.keyframes([(0, 0), (3, 0), (4, 1), (80, 1), (82, 0), (100, 0)]), still=0))
# barras de tiempo
Y = 380
a.add(a.text(48, Y - 14, "tiempo de la lectura", 16, a.GREY, a.MONO, 600))
a.add(a.box(48, Y, 1104, 44, a.WHITE, a.LINE, rx=10))
kav = a.box(48, Y, 60, 44, a.CYAN, None, rx=10) + a.text(78, Y + 28, "K", 15, "#FFFFFF", a.MONO, 700, "middle")
at(a, kav, 22, 100, 1)
dav = a.box(112, Y, 700, 44, a.AMB, None, rx=10) + a.text(462, Y + 28, "DAVG: almacenamiento", 16, "#FFFFFF", a.MONO, 700, "middle")
k = a.keyframes([(0, 0.0001), (40, 0.0001), (62, 1), (100, 1)], "transform", "scaleX({})")
a.add(a.group(dav, k, still=0, origin=f"112px {Y}px"))
a.add(a.group(dav, a.keyframes([(0, 0), (100, 0)]), still=1))
at(a, a.box(48, Y + 60, 764, 44, "none", a.INK, rx=10, sw=2.5) + a.text(830, Y + 89, "GAVG = KAVG + DAVG", 18, a.INK, a.MONO, 700), 62, 100, 1)
# diagnóstico
at(a, chip(a, 840, 330, "acá está la demora", "amb"), 75, 100, 0)
at(a, chip(a, 420, 330, "KAVG cerca de cero: host bien", "ok"), 75, 100, 0)
caption(a, 560, [(0, 25, "GAVG es lo que siente la VM: el total.", None),
                 (25, 50, "Si KAVG sube, hay encolamiento dentro del host.", None),
                 (50, 75, "DAVG mide al almacenamiento: controladora, red de storage, NAS o SAN.", a.AMB),
                 (75, 100, "Separar KAVG de DAVG evita culpar al host por un NAS lento.", a.OK)], still=2)
a.add(a.text(48, 620, "En esxtop: tecla u, columnas DAVG/cmd, KAVG/cmd y GAVG/cmd (en milisegundos).", 15, a.GREY, a.SANS, 500))
write(a, "11-t1.svg", "GAVG = KAVG + DAVG: dónde se va el tiempo de un disco",
      "Animación en cuatro tiempos con tres cajas en fila: la VM, el VMkernel del host y el almacenamiento, y abajo una barra con el tiempo de la lectura. "
      "1: la VM pide una lectura y arranca el reloj de GAVG. 2: la lectura pasa por la cola del VMkernel, un tramo corto llamado KAVG, que debería ser casi cero. "
      "3: llega al almacenamiento y vuelve; ese tramo, DAVG, es el más largo de la barra, y GAVG queda como la suma de KAVG y DAVG. "
      "4: como DAVG es el grande, la demora está en el almacenamiento y no en el host.")
