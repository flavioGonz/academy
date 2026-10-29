#!/usr/bin/env python3
"""Lección 9 · Laboratorio, paso 1: df -h y df -i. Cada archivo usa un inodo, pese lo que pese; en ext4 la cantidad
de inodos se fija al crear el sistema de archivos. Millones de archivos chicos los agotan y aparece "No space left on
device" con espacio libre; df -i lo muestra (IUse% 100%) y du --inodes encuentra la carpeta. Fuentes: teoría de la
lección (cada archivo usa uno, df -i), df(1), du(1) (--inodes) y la documentación de ext4. Cifras de ejemplo."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · DISCO · LABORATORIO", "Lleno con espacio libre: se acabaron los inodos")
a.steps([
    "df -h mide bloques: quedan 12 GB libres en /.",
    "Cada archivo usa un inodo, aunque pese 2 KB; en ext4 son un número fijo.",
    "Millones de archivos chicos agotan los inodos: No space left on device.",
    "df -i lo muestra con IUse% 100%; du --inodes dice qué carpeta es.",
], still=2)

# carpeta que se llena de archivos chicos
CX, CY, CW, CH = 48, 176, 520, 280
a.add(a.box(CX, CY, CW, CH, a.WHITE, "#C2D4E6", rx=16) + mono(a, CX + 18, CY + 30, "/var/cache/app-obra/miniaturas/", 15, a.INK, 700))
a.add(a.text(CX + 18, CY + 54, "una miniatura por evento, 2 KB cada una (ejemplo)", 15, a.GREY, a.SANS, 500))
N = 0
for r in range(6):
    for c in range(20):
        x, y = CX + 20 + c * 24.5, CY + 72 + r * 28
        t0 = 26 + (r * 20 + c) * 0.17
        en(a, a.box(x, y, 18, 22, a.CYAN, None, rx=3), t0, 100, still=1)
        N += 1
en(a, a.text(CX + 18, CY + CH - 10, "cada cuadrito: miles de archivos", 14, a.GREY, a.SANS, 500), 26, 100, still=1)

# medidores
MX, MW = 620, 532


def medidor(y, titulo, cmd):
    a.add(a.text(MX, y, titulo, 17, a.INK, a.HEAD, 600) + mono(a, MX + MW, y, cmd, 15, a.BLUE, 600, "end"))
    a.add(a.box(MX, y + 14, MW, 34, a.SLATE, None, rx=10))


medidor(210, "Bloques (espacio)", "df -h /")
en(a, a.box(MX, 224, MW * 0.6, 34, a.BLUE, None, rx=10) + a.text(MX, 284, "19G de 31G usados · 12G libres", 15, a.OK, a.MONO, 700), 0, 100, still=1)
en(a, a.box(MX, 224, MW * 0.62, 34, a.BLUE, None, rx=10), 50, 100, still=1)
medidor(330, "Inodos (cantidad de archivos)", "df -i /")
k = a.keyframes([(0, 0.25), (26, 0.25), (50, 1), (100, 1)], "transform", "scaleX({})")
a.add(a.group(a.group(a.box(MX, 344, MW, 34, a.BAD, None, rx=10), k, still=None, origin=f"{MX}px 344px"), a.show(0, 100), still=0))
fijo(a, a.box(MX, 344, MW, 34, a.BAD, None, rx=10))
en(a, a.text(MX, 404, "500 mil de 2,0 M usados", 15, a.TXT, a.MONO, 700), 0, 26)
en(a, a.text(MX, 404, "2,0 M de 2,0 M: no queda ninguno", 15, a.BAD, a.MONO, 700), 50, 100, still=1)
en(a, a.text(MX, 430, "en ext4, la cantidad se fija al formatear", 15, a.GREY, a.SANS, 600), 26, 100, still=1)

# error
en(a, a.box(MX, 444, MW, 40, a.BADBG, a.BAD, rx=10) + mono(a, MX + 16, 470, "No space left on device", 16, a.BAD, 700)
   + a.text(MX + MW - 16, 470, "con 12G libres", 15, a.INK, a.SANS, 600, "end"), 54, 100, still=1)

# terminal
TY = 498
a.add(tterm(a, 48, TY, 1104, 110))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 30 + i * 25, r, 14) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ df -h /", ("Filesystem  Size  Used Avail Use% Mounted on", T_COM), ("/dev/sda2    31G   19G   12G  62% /", T_OK)], 0, 50)
filas(["$ touch /var/cache/app-obra/prueba", ("touch: cannot touch '/var/cache/app-obra/prueba': No space left on device", T_ERR)], 50, 75, still=1)
filas(["$ df -i /", ("Filesystem   Inodes  IUsed IFree IUse% Mounted on", T_COM), ("/dev/sda2      2.0M   2.0M     0  100% /", T_ERR),
       "$ sudo du --inodes -xd1 /var | sort -n | tail -3      # la carpeta con más archivos"], 75, 100)

narr(a, [
    (0, 25, "df -h solo cuenta espacio: no dice cuántos archivos entran.", None),
    (25, 50, "Un archivo de 2 KB ocupa poco espacio, pero un inodo entero.", a.AMB),
    (50, 75, "Sin inodos libres no se crea ningún archivo, aunque sobre espacio.", a.BAD),
    (75, 100, "La salida: borrar o rotar esos archivos chicos, no agrandar el disco.", a.OK),
], y=642, still_idx=2)

escribir(a, "9-l1", "Lleno con espacio libre: se acabaron los inodos",
         "Animación en cuatro tiempos. A la izquierda, la carpeta de ejemplo /var/cache/app-obra/miniaturas, que se llena de archivos de 2 KB; a la derecha, dos medidores, bloques con df -h / e inodos con df -i /, y abajo una terminal. "
         "1: df -h muestra 19G de 31G usados y 12G libres. "
         "2: cada archivo usa un inodo aunque pese poco, y en ext4 la cantidad de inodos se fija al formatear; la carpeta empieza a llenarse. "
         "3: el medidor de inodos llega al tope, 2,0 millones de 2,0 millones, mientras el de espacio casi no se mueve, y touch falla con No space left on device con 12G libres. "
         "4: df -i muestra IUse% 100% y du --inodes -xd1 /var ordenado encuentra la carpeta con más archivos.",
         [10, 38, 64, 90])
