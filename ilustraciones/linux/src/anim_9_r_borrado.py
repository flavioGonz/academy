#!/usr/bin/env python3
"""Lección 9 (Disco lleno), Resumen: borraste el log y el disco sigue lleno. El nombre de /var/log apunta a un
inodo y sus bloques; el proceso que escribe tiene el archivo abierto. rm borra el nombre, pero mientras el proceso
lo tenga abierto el espacio no se libera: df lo cuenta y du no lo encuentra. lsof +L1 lo muestra como (deleted);
al reiniciar el servicio se cierra y el espacio vuelve. Fuentes: teoría de la lección (archivo borrado que un proceso
sigue teniendo abierto, lsof), unlink(2) y lsof(8) (+L1, NLINK 0). Nombres y tamaños de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · DISCO · POR DENTRO", "Borraste el log y el disco sigue lleno")
a.steps([
    "app-obra escribe su log: el nombre apunta al inodo y a sus bloques.",
    "rm borra el nombre; el proceso lo sigue teniendo abierto.",
    "df dice lleno y du no lo encuentra: lsof +L1 lo muestra (deleted).",
    "Reiniciar el servicio cierra el archivo y el espacio vuelve.",
], still=2)

# proceso
en(a, dev(a, 48, 186, 270, 90, "app-obra", "PID 812 · fd 3 → escribe", None, dark=True, ssize=14), 0, 76, still=1)
en(a, dev(a, 48, 186, 270, 90, "app-obra", "PID 1733 · reiniciado", None, dark=True, ssize=14), 76, 100)
# directorio
a.add(a.box(380, 176, 330, 110, a.WHITE, "#C2D4E6", rx=14) + mono(a, 398, 206, "/var/log/", 16, a.INK, 700))
en(a, a.box(398, 222, 294, 44, a.SLATE, None, rx=8) + mono(a, 412, 250, "app-obra.log → inodo 1234", 15, a.INK, 600), 0, 30)
en(a, a.box(398, 222, 294, 44, "none", a.BAD, rx=8, sw=2, extra='stroke-dasharray="6 5"') + mono(a, 412, 250, "(sin nombre: lo borró rm)", 15, a.BAD, 600), 30, 100, still=1)
# inodo + bloques
IX = 770
a.add(a.box(IX, 176, 382, 230, a.WHITE, "#C2D4E6", rx=14) + mono(a, IX + 18, 206, "inodo 1234", 16, a.INK, 700))
en(a, mono(a, IX + 200, 206, "enlaces: 1", 15, a.GREY, 600), 0, 30)
en(a, mono(a, IX + 200, 206, "enlaces: 0", 15, a.BAD, 700), 30, 82, still=1)
for r in range(4):
    for c in range(10):
        bx, by = IX + 18 + c * 35, 226 + r * 40
        en(a, a.box(bx, by, 30, 32, a.BLUE, None, rx=5), 0, 82, still=1)
        en(a, a.box(bx, by, 30, 32, a.SLATE, None, rx=5), 82, 100)
a.add(a.text(IX + 18, 396, "bloques de datos · 6,5 GB (ejemplo)", 14, a.GREY, a.SANS, 600))
en(a, mono(a, IX + 200, 206, "liberados", 15, a.OK, 700), 84, 100)

# enlaces
en(a, camino("M692 244 H770", a.INK, 3), 0, 30)
en(a, camino("M318 254 C 340 330, 640 340, 770 340", a.CYAN, 3), 0, 82, still=1)
en(a, a.text(440, 366, "fd 3: el archivo sigue abierto", 15, a.CYAN, a.SANS, 700), 30, 82, still=1)
viaje(a, "", [(328, 270), (480, 334), (760, 340)], 3, 10, inner=f'<circle r="8" fill="{a.CYAN}"/>', hold=0)
viaje(a, "", [(328, 270), (480, 334), (760, 340)], 33, 40, inner=f'<circle r="8" fill="{a.CYAN}"/>', hold=0)
viaje(a, "rm", [(545, 176), (545, 236)], 26, 30, bg=a.BAD, size=14, hold=1)

# df y du
BY = 430
a.add(a.text(48, BY + 20, "df -h /", 15, a.INK, a.MONO, 700) + a.box(170, BY, 560, 26, a.SLATE, None, rx=8))
en(a, a.box(170, BY, 540, 26, a.BAD, None, rx=8) + a.text(750, BY + 20, "30G de 31G: lleno", 15, a.BAD, a.MONO, 700), 0, 82, still=1)
en(a, a.box(170, BY, 420, 26, a.OK, None, rx=8) + a.text(750, BY + 20, "23G de 31G", 15, a.OK, a.MONO, 700), 82, 100)
a.add(a.text(48, BY + 58, "du -xsh /var/log", 15, a.INK, a.MONO, 700))
en(a, a.text(220, BY + 58, "6,8G", 15, a.INK, a.MONO, 700), 0, 30)
en(a, a.text(220, BY + 58, "300M   el borrado ya no tiene nombre: du no lo ve", 15, a.AMB, a.MONO, 700), 30, 100, still=1)

# terminal
TY = 508
a.add(tterm(a, 48, TY, 1104, 100))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 30 + i * 25, r, 14) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ ls -l /var/log/app-obra.log", ("-rw-r----- 1 root adm 6,5G ... /var/log/app-obra.log", T_OUT)], 0, 25)
filas(["$ sudo rm /var/log/app-obra.log && df -h /", ("/dev/sda2   31G   30G  1,0G  97% /      # sigue lleno", T_ERR)], 25, 50)
filas(["$ sudo lsof +L1", ("COMMAND   PID USER FD  TYPE  SIZE/OFF NLINK  NODE NAME", T_COM),
       ("app-obra  812 root 3w  REG  6979321856     0  1234 /var/log/app-obra.log (deleted)", T_WARN)], 50, 75, still=1)
filas(["$ sudo systemctl restart app-obra && df -h /", ("/dev/sda2   31G   23G  7,5G  76% /      # el espacio volvió", T_OK)], 75, 100)

narr(a, [
    (0, 25, "Un archivo es un inodo con sus bloques; el nombre en la carpeta solo apunta.", None),
    (25, 50, "Mientras un proceso lo tenga abierto, el kernel no suelta los bloques.", a.BAD),
    (50, 75, "Si df y du no coinciden, buscá archivos borrados abiertos.", a.AMB),
    (75, 100, "Para un log grande, mejor vaciar o rotar con logrotate que borrar en caliente.", a.OK),
], y=642, still_idx=2)

escribir(a, "9-r1", "Borraste el log y el disco sigue lleno",
         "Animación en cuatro tiempos. A la izquierda, el proceso app-obra, PID 812, con el descriptor 3 abierto; en el medio, la carpeta /var/log con el nombre app-obra.log que apunta al inodo 1234; a la derecha, el inodo y sus bloques de datos, 6,5 GB de ejemplo. Abajo, df, du y una terminal. "
         "1: app-obra escribe su log y df -h / marca 30G de 31G. "
         "2: rm borra el nombre, el inodo queda con 0 enlaces, pero el proceso lo sigue teniendo abierto y los bloques siguen ocupados: df sigue lleno. "
         "3: du sobre /var/log ya no lo cuenta porque no tiene nombre; sudo lsof +L1 muestra app-obra, PID 812, descriptor 3w, NLINK 0, /var/log/app-obra.log (deleted). "
         "4: systemctl restart app-obra cierra el archivo, los bloques se liberan y df -h / baja a 23G.",
         [10, 38, 62, 92])
