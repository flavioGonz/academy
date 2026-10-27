"""Teoría lección 9: vMotion copia la memoria en vivo, en pasadas, y cambia de host en un instante."""
from _avmw import *

a = new(20, "vMotion: la memoria viaja mientras la VM sigue andando")
a.steps(["Primera pasada: se copia toda la memoria por la red de vMotion.",
         "La VM sigue escribiendo: se copian de nuevo las páginas que cambiaron.",
         "Quedan pocas: pausa de un instante, se pasa el estado y arranca en el destino.",
         "La VM corre en esxi-lab02; el disco nunca se movió del datastore."], still=1)

for x, t in [(48, "esxi-lab01"), (700, "esxi-lab02")]:
    a.add(card(a, x, 170, 452, 270, t, "Cluster-Lab", dark=True))
# memoria origen y destino: 16 páginas cada una
def pages(x, y, fill, stroke):
    return "".join(a.box(x + (k % 8) * 48, y + (k // 8) * 48, 40, 40, fill, stroke, rx=5, sw=1.5) for k in range(16))

a.add(a.text(76, 250, "memoria de vm-prueba", 15, "#9FC3E3", a.MONO))
a.add(pages(76, 266, "#E5F0FB", a.BLUE))
a.add(a.text(728, 250, "memoria en el destino", 15, "#9FC3E3", a.MONO))
a.add(pages(728, 266, "#0B3A66", "#4E7396"))
# pasada 1: el destino se llena (excepto las que después cambian)
DIRTY = {3, 9, 12}
for k in range(16):
    t0 = 3 + k * 1.2
    at(a, a.box(728 + (k % 8) * 48, 266 + (k // 8) * 48, 40, 40, "#E5F0FB", a.BLUE, rx=5, sw=1.5), t0, 100, 1)
# páginas que cambian en el origen
for k in DIRTY:
    at(a, a.box(76 + (k % 8) * 48, 266 + (k // 8) * 48, 40, 40, "#FFB020", a.AMB, rx=5, sw=2), 28, 58, 1)
    at(a, a.box(728 + (k % 8) * 48, 266 + (k // 8) * 48, 40, 40, "#FFE3A3", a.AMB, rx=5, sw=2), 28, 48, 1)
    at(a, a.box(728 + (k % 8) * 48, 266 + (k // 8) * 48, 40, 40, "#E5F0FB", a.BLUE, rx=5, sw=1.5), 48, 100, 0)
# flujo
a.add(line(a, "M500 300H700", a.AMB, 4, "10 8"))
a.add(a.text(600, 290, "red de vMotion", 14, a.AMB, a.MONO, 600, "middle"))
for i in range(3):
    a.add(a.group('<rect x="-14" y="-10" width="28" height="20" rx="4" fill="#0A63B8"/>',
                  a.move([(0, 510, 320), (i * 8, 510, 320), (i * 8 + 8, 690, 320), (100, 690, 320)]),
                  a.keyframes([(0, 0), (i * 8, 0), (i * 8 + 0.5, 1), (i * 8 + 7.5, 1), (i * 8 + 8, 0), (100, 0)]), still=0))
# corte: pausa
at(a, chip(a, 600, 360, "pausa de un instante", "amb", anchor="middle"), 58, 75, 0)
# VM origen y destino
a.add(a.group(vmbox(a, 76, 380, 300, 50, "vm-prueba", "corriendo aquí"), a.show(0, 62), still=1))
a.add(a.group(vmbox(a, 728, 380, 300, 50, "vm-prueba", "corriendo aquí", stroke=a.OK), a.show(62, 100), still=0))
# datastore
a.add(a.box(326, 480, 548, 70, a.WHITE, a.BLUE, rx=14, sw=2.5) + a.text(600, 512, "datastore compartido", 17, a.INK, a.SANS, 600, "middle")
      + a.text(600, 536, "el disco de vm-prueba queda acá", 14, a.GREY, a.MONO, 400, "middle"))
a.add(line(a, "M274 440V480M926 440V480", a.BLUE, 3))
caption(a, 600, [(0, 25, "La VM no se apaga: la copia se hace con la VM corriendo.", None),
                 (25, 50, "Cada pasada es más chica que la anterior.", None),
                 (50, 75, "Si algo falla en el camino, la VM vuelve a su host de origen.", a.AMB),
                 (75, 100, "Un ping continuo pierde, como mucho, uno o dos paquetes.", a.OK)], still=1)
write(a, "9-t1.svg", "vMotion: la memoria viaja mientras la VM sigue andando",
      "Animación en cuatro tiempos con dos hosts, esxi-lab01 y esxi-lab02, la memoria de la VM en cada uno y un datastore compartido abajo. "
      "1: en una primera pasada toda la memoria se copia por la red de vMotion al destino. "
      "2: como la VM sigue escribiendo, tres páginas cambian en el origen y se vuelven a copiar. "
      "3: con pocas páginas pendientes, la VM se pausa un instante, se pasa el estado y arranca en el destino. "
      "4: la VM corre en esxi-lab02 y su disco nunca se movió del datastore compartido.")
