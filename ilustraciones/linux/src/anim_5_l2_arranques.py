#!/usr/bin/env python3
"""Lección 5 · Laboratorio, paso 4: journalctl -b -1 -p err. El journal guarda cada arranque por separado
(0 es el actual, -1 el anterior); un corte termina el arranque -1 y lo que se escribió hasta ahí queda.
-b -1 trae solo ese arranque y -p err deja las prioridades 0 a 3 (emerg, alert, crit, err).
Fuentes: journalctl(1) (-b, --list-boots, -p), teoría de la lección (prioridades de 0 a 7) y el laboratorio.
Las líneas de log son de ejemplo (el OOM del kernel se registra con prioridad err)."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · JOURNAL · LABORATORIO", "journalctl -b -1: lo que pasó antes del reinicio")
a.steps([
    "El journal guarda cada arranque por separado: el actual es el 0.",
    "Un corte termina el arranque -1: lo escrito hasta ahí queda guardado.",
    "-b -1 trae solo ese arranque; -p err deja los errores y lo más grave.",
    "Las prioridades van de 0 a 7: err es la 3 y -p err muestra de 0 a 3.",
], still=2)

Y0 = 176
SEG = [(48, 250, "arranque -2", "lunes"), (318, 520, "arranque -1", "martes, hasta el corte"), (858, 294, "arranque 0", "hoy, el actual")]
for x, w, t, s in SEG:
    a.add(a.box(x, Y0, w, 190, a.WHITE, "#C2D4E6", rx=14) + a.text(x + 18, Y0 + 30, t, 17, a.INK, a.HEAD, 600)
          + a.text(x + 18, Y0 + 52, s, 15, a.GREY, a.SANS, 500))
# marcas cortas en -2 y 0
import random
random.seed(5)
for x, w, _, _ in (SEG[0], SEG[2]):
    for i in range(5):
        c = a.BAD if (x == 48 and i == 3) else "#C2D4E6"
        a.add(a.box(x + 18, Y0 + 72 + i * 22, random.randint(int(w * 0.45), w - 40), 10, c, None, rx=5))
en(a, a.box(858, Y0, 294, 190, "none", a.BLUE, rx=14, sw=3), 0, 25)

# líneas del arranque -1
LX = 336
L = [("08:02  systemd[1]: Started ssh.service", "info", 6), ("08:03  app-obra[812]: conectado a la base", "info", 9),
     ("02:58  CRON[950]: (root) CMD (backup-etc.sh)", "info", 28), ("03:12  kernel: Out of memory: Killed process 812", "err", 33)]
for i, (s, p, t) in enumerate(L):
    y = Y0 + 84 + i * 26
    col = a.BAD if p == "err" else a.INK
    en(a, mono(a, LX, y, s, 14, col, 600 if p == "err" else 500), t, 100, still=1)
    if p != "err":
        en(a, a.box(LX - 6, y - 17, 504, 24, a.WHITE, None, rx=4, extra='opacity=".72"'), 52, 100, still=1)
en(a, glyph(a, "bolt", 812, Y0 + 14, a.BAD, 1.2, 2) + a.text(800, Y0 + 32, "corte 03:12", 15, a.BAD, a.MONO, 700, "end"), 36, 100, still=1)
en(a, a.box(318, Y0, 520, 190, "none", a.AMB, rx=14, sw=3), 50, 75, still=1)

# prioridades
PY = 392
a.add(a.text(48, PY + 20, "prioridad", 15, a.GREY, a.SANS, 600))
PR = ["0 emerg", "1 alert", "2 crit", "3 err", "4 warning", "5 notice", "6 info", "7 debug"]
px = 140
pos = []
for i, p in enumerate(PR):
    w = int(len(p) * 15 * 0.62 + 26)
    pos.append((px, w))
    a.add(a.pill(px, PY, p, a.BAD if i <= 3 else a.GREY, a.BADBG if i <= 3 else a.SLATE, 15, 30))
    px += w + 10
x0, x1 = pos[0][0] - 6, pos[3][0] + pos[3][1] + 6
en(a, a.box(x0, PY - 6, x1 - x0, 42, "none", a.BAD, rx=14, sw=3) + a.text((x0 + x1) / 2, PY + 62, "lo que deja -p err", 15, a.BAD, a.SANS, 700, "middle"), 76, 100)

# terminal
TY = 470
a.add(tterm(a, 48, TY, 1104, 130))
def filas(rows, t0, t1, still=0):
    s = "".join(trow(a, 48, TY + 32 + i * 26, r, 15) for i, r in enumerate(rows))
    en(a, s, t0, t1, still)


filas(["$ journalctl --list-boots", ("  -2  lunes   ·  -1  martes, hasta las 03:12  ·  0  hoy, desde las 07:40", T_OUT), ("  (resumido: la salida real trae el ID y la primera y última línea de cada uno)", T_COM)], 0, 25)
filas(["$ du -sh /var/log/journal", ("  el journal está en disco: sobrevive al reinicio", T_OUT)], 25, 50)
filas(["$ sudo journalctl -b -1 -p err", ("  03:12 srv kernel: Out of memory: Killed process 812 (app-obra)", T_ERR), ("  (líneas de ejemplo)", T_COM)], 50, 75, still=1)
filas(["$ sudo journalctl -b -1 -p warning", ("  suma la 4: más líneas, menos foco", T_OUT), ("  sin -p: todo el arranque, de 0 a 7", T_OUT)], 75, 100)

narr(a, [
    (0, 25, "Cada arranque tiene su número: 0 el actual, -1 el anterior, -2 el de antes.", None),
    (25, 50, "Lo que el equipo escribió hasta el corte está ahí, aunque haya reiniciado.", a.AMB),
    (50, 75, "Un filtro por arranque y otro por gravedad: de cientos de líneas quedan pocas.", a.OK),
    (75, 100, "Si no aparece nada con err, probá con warning antes de leer todo.", None),
], still_idx=2)

escribir(a, "5-l2", "journalctl -b -1: lo que pasó antes del reinicio",
         "Animación en cuatro tiempos con tres bloques del journal, uno por arranque: -2 el lunes, -1 el martes hasta el corte y 0 el actual; abajo, las prioridades de 0 a 7 y una terminal. "
         "1: journalctl --list-boots muestra los tres arranques y el actual se marca como 0. "
         "2: en el arranque -1 aparecen líneas de ejemplo: ssh arrancado, app-obra conectada, una tarea de cron y, a las 03:12, kernel: Out of memory: Killed process 812; después llega el corte de luz y el bloque termina ahí. El journal está en disco y sobrevive al reinicio. "
         "3: sudo journalctl -b -1 -p err marca solo ese arranque, apaga las líneas informativas y deja la del kernel. "
         "4: en la fila de prioridades se marcan 0 emerg, 1 alert, 2 crit y 3 err como lo que deja -p err; con warning se suma la 4 y sin -p sale todo.",
         [10, 40, 62, 90])
