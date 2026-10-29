#!/usr/bin/env python3
"""Lección 11 (Backup que restaura), Resumen: el backup que se va con el disco y el que sobrevive.
El timer corre tar a las 02:30 y el archivo queda en /srv/backup, en el mismo disco; rsync lo copia a otro equipo,
10.10.10.20, mandando solo lo que cambió; se rompe el disco del servidor y lo local se pierde; desde el otro equipo
se restaura a una carpeta aparte y diff lo confirma. Fuentes: teoría y laboratorio de la lección (tar czf con
hostname y fecha, timer OnCalendar 02:30, rsync a otro equipo, otro lugar físico, restaurar a /tmp y diff)."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · BACKUP · CÓMO SE VE", "El backup que se va con el disco y el que queda")
a.steps([
    "02:30: el timer corre tar y el archivo queda en /srv/backup.",
    "rsync lo copia a 10.10.10.20, otro equipo: solo lo que cambió.",
    "La prueba: se restaura un archivo de la copia a /tmp y diff confirma.",
    "Se rompe el disco: lo local se pierde; la copia remota ya está probada.",
], still=3)

# servidor
SX, SY, SW, SH = 48, 172, 500, 300
a.add(a.box(SX, SY, SW, SH, a.WHITE, "#C2D4E6", rx=16) + glyph(a, "server", SX + 18, SY + 16, a.BLUE) + a.text(SX + 62, SY + 38, "srv1 · 192.168.88.50", 18, a.INK, a.HEAD, 600))
a.add(a.box(SX + 18, SY + 62, SW - 36, 216, a.SLATE, None, rx=12) + a.text(SX + 34, SY + 88, "disco del sistema (sda)", 15, a.GREY, a.SANS, 600))
ROWS = [("/etc", "configuración"), ("/srv/datos", "datos de la obra"), ("/srv/backup", "")]
for i, (p, d) in enumerate(ROWS):
    y = SY + 104 + i * 54
    a.add(a.box(SX + 34, y, SW - 68, 42, a.WHITE, a.LINE, rx=8) + mono(a, SX + 50, y + 27, p, 15, a.INK, 700) + a.text(SX + 200, y + 27, d, 15, a.GREY, a.SANS, 500))
en(a, mono(a, SX + 200, SY + 239, "srv1-etc-2026-10-28.tar.gz", 14, a.OK, 700), 9, 100, still=0)
viaje(a, "tar czf", [(SX + 100, SY + 125), (SX + 100, SY + 222)], 4, 9, bg=a.BLUE, size=14, hold=1)
en(a, a.pill(SX + 300, SY + 22, "timer · 02:30", a.BLUE, "#E5F0FB", 14, 28), 2, 25)
# disco roto
en(a, a.box(SX + 18, SY + 62, SW - 36, 216, a.BADBG, a.BAD, rx=12, sw=3)
   + marca(a, SX + SW / 2, SY + 150, False, 26) + a.text(SX + SW / 2, SY + 210, "el disco no arranca", 18, a.BAD, a.SANS, 700, "middle")
   + a.text(SX + SW / 2, SY + 236, "/etc, /srv/datos y /srv/backup: perdidos", 15, a.INK, a.SANS, 600, "middle"), 77, 100, still=1)

# equipo de respaldo
BX = 700
a.add(a.box(BX, SY, 452, SH, a.INK, None, rx=16) + glyph(a, "server", BX + 18, SY + 16, a.CYAN) + a.text(BX + 62, SY + 38, "Respaldo · 10.10.10.20", 18, "#FFFFFF", a.HEAD, 600))
a.add(a.text(BX + 62, SY + 62, "otro equipo, en otra sala", 15, LIGHT, a.SANS, 500))
a.add(a.box(BX + 18, SY + 82, 416, 120, "#0B3A66", None, rx=10) + mono(a, BX + 34, SY + 108, "/respaldos/srv1/", 15, "#FFFFFF", 700))
en(a, mono(a, BX + 34, SY + 140, "srv1-etc-2026-10-27.tar.gz", 14, LIGHT, 600), 0, 100, still=1)
en(a, mono(a, BX + 34, SY + 166, "srv1-etc-2026-10-28.tar.gz", 14, MINT, 700), 36, 100, still=1)
en(a, a.text(BX + 34, SY + 192, "el del 27 ya estaba: no se manda de nuevo", 14, LIGHT, a.SANS, 600), 36, 75)
a.add(camino(f"M{SX + SW} 330 H{BX}", "#C2D4E6", 4, "8 6"))
viaje(a, "tar xzf -C /tmp", [(BX - 20, 296), (SX + SW + 20, 296)], 53, 58, bg=a.OK, size=14, hold=1)
viaje(a, "rsync -a", [(SX + SW + 20, 318), (BX - 20, 318)], 28, 36, bg=a.CYAN, size=14, hold=1)
en(a, a.text((SX + SW + BX) / 2, 352, "solo lo nuevo", 15, a.CYAN, a.SANS, 700, "middle"), 30, 50)
# restauración
en(a, a.box(BX + 18, SY + 214, 416, 72, a.OKBG, a.OK, rx=10) + mono(a, BX + 34, SY + 240, "probado: hostname restaurado", 14, a.OK, 700)
   + a.text(BX + 34, SY + 266, "en /tmp, y diff contra el original: igual", 15, a.INK, a.SANS, 600), 58, 100, still=1)

# terminal
TY = 488
a.add(tterm(a, 48, TY, 1104, 118))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 32 + i * 26, r, 15) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ journalctl -u backup-etc.service -n 3", ("backup-etc.service: Deactivated successfully.   # corrió a las 02:30", T_OK)], 0, 25)
filas(["$ rsync -av /srv/backup/ backup@10.10.10.20:/respaldos/srv1/", ("srv1-etc-2026-10-28.tar.gz", T_OUT), ("sent ... bytes   (solo el archivo nuevo)", T_COM)], 25, 50)
filas(["$ sudo tar xzf srv1-etc-2026-10-28.tar.gz -C /tmp etc/hostname     # traído de 10.10.10.20",
       "$ diff /tmp/etc/hostname /etc/hostname && echo \"restaurado OK\"", ("restaurado OK", T_OK)], 50, 75)
filas([("# el servidor no arranca: lo que estaba en su disco se perdió", T_ERR), ("# la copia de 10.10.10.20 sigue entera, y ya sabés que restaura", T_OK)], 75, 100, still=1)

narr(a, [
    (0, 25, "Que el timer corra no prueba nada todavía: el archivo está en el mismo disco.", None),
    (25, 50, "Otro lugar físico: otro equipo, mejor en otra sala.", a.OK),
    (50, 75, "El backup existe recién cuando restauraste un archivo de él.", a.OK),
    (75, 100, "Un backup en el mismo disco se pierde con el disco; el otro te salva.", a.BAD),
], y=642, still_idx=3)

escribir(a, "11-r1", "El backup que se va con el disco y el que queda",
         "Animación en cuatro tiempos. A la izquierda, el servidor srv1 con su disco del sistema y las carpetas /etc, /srv/datos y /srv/backup; a la derecha, el equipo de respaldo 10.10.10.20, en otra sala, con /respaldos/srv1/; abajo, una terminal. "
         "1: a las 02:30 el timer corre tar czf y srv1-etc-2026-10-28.tar.gz queda en /srv/backup, en el mismo disco; el journal muestra que corrió. "
         "2: rsync -av copia /srv/backup/ a 10.10.10.20 y solo manda el archivo nuevo: el del 27 ya estaba. "
         "3: la prueba: con el archivo traído de 10.10.10.20, tar xzf con -C /tmp restaura etc/hostname aparte y diff contra el original responde restaurado OK. "
         "4: el disco del servidor se rompe y /etc, /srv/datos y /srv/backup se pierden; la copia de 10.10.10.20 sigue entera y ya está probada.",
         [10, 38, 64, 92])
