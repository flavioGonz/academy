#!/usr/bin/env python3
"""Lección 10 · Laboratorio, paso 1: uptime y nproc. La carga es el promedio de procesos corriendo o esperando
turno; se compara con la cantidad de núcleos. Con 4 núcleos, carga 2 deja núcleos libres; carga 6 es saturación.
Los tres números de uptime son promedios de 1, 5 y 15 minutos: sirven para ver si la carga es sostenida.
Fuentes: teoría y laboratorio de la lección (load average de 1, 5 y 15 minutos; carga sostenida por encima de nproc)."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · CARGA · LABORATORIO", "Carga contra núcleos: cuántos esperan turno")
a.steps([
    "nproc dice 4: hay cuatro núcleos para atender procesos.",
    "Carga 2: dos procesos corriendo, dos núcleos libres.",
    "Carga 6: cuatro corriendo y dos esperando turno. Saturación.",
    "Tres promedios, de 1, 5 y 15 minutos: ¿es sostenida o recién empieza?",
], still=2)

CX0, CY = 640, 236
cores = [(CX0 + i * 130, CY) for i in range(4)]
for i, (x, y) in enumerate(cores):
    a.add(a.box(x, y, 116, 110, a.WHITE, "#C2D4E6", rx=14) + a.text(x + 58, y + 26, f"núcleo {i}", 15, a.GREY, a.MONO, 600, "middle"))
a.add(a.text(CX0, CY - 18, "CPU · 4 núcleos (nproc)", 16, a.INK, a.HEAD, 600))
a.add(a.box(48, CY, 540, 110, a.SLATE, None, rx=14) + a.text(68, CY + 26, "esperando turno", 15, a.GREY, a.MONO, 600))
en(a, a.box(CX0 - 8, CY - 8, 4 * 130 + 2, 126, "none", a.BLUE, rx=16, sw=3), 4, 25)

PR = ["nginx", "postgres", "backup", "ffmpeg", "php-fpm", "rsync"]


def proc(n, x, y, col):
    return place(pill_c(a, n, "#FFFFFF", col, 15, 34), x, y)


# fase 2: dos corriendo
for i in range(2):
    x, y = cores[i]
    viaje(a, "", [(x + 58, CY - 50), (x + 58, y + 72)], 26 + i * 2, 29 + i * 2, inner=pill_c(a, PR[i], "#FFFFFF", a.OK, 15, 34), hold=19)
for i in (2, 3):
    x, y = cores[i]
    en(a, a.text(x + 58, y + 78, "libre", 16, a.OK, a.SANS, 700, "middle"), 30, 50)
# fase 3 y 4: cuatro corriendo, dos esperando
for i in range(4):
    x, y = cores[i]
    en(a, proc(PR[i], x + 58, y + 72, a.BLUE), 50, 100, still=1)
for j, n in enumerate(PR[4:]):
    qx = 440 - j * 150
    viaje(a, "", [(qx - 220, CY + 72), (qx, CY + 72)], 53 + j * 3, 57 + j * 3, inner=pill_c(a, n, "#FFFFFF", a.AMB, 15, 34), hold=60)
    fijo(a, proc(n, qx, CY + 72, a.AMB))
en(a, a.box(40, CY - 8, 556, 126, "none", a.AMB, rx=16, sw=3), 58, 75, still=1)

# medidor de carga
MX, MY = 48, 380
a.add(a.text(MX, MY + 22, "carga", 16, a.INK, a.HEAD, 600))
a.add(a.box(MX + 80, MY + 4, 600, 24, a.SLATE, None, rx=12))
a.add(linea(MX + 80 + 400, MY - 4, MX + 80 + 400, MY + 36, a.INK, 2.5, "5 4") + a.text(MX + 80 + 400, MY + 56, "4 = nproc", 15, a.INK, a.MONO, 700, "middle"))
en(a, a.box(MX + 80, MY + 4, 200, 24, a.OK, None, rx=12) + a.text(MX + 700, MY + 22, "2,00 · sobra", 16, a.OK, a.MONO, 700), 28, 50)
en(a, a.box(MX + 80, MY + 4, 600, 24, a.BAD, None, rx=12) + a.text(MX + 700, MY + 22, "6,10 · satura", 16, a.BAD, a.MONO, 700), 54, 100, still=1)

# terminal
TY = 460
a.add(tterm(a, 48, TY, 1104, 140))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 34 + i * 27, r, 15) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ nproc", ("4", T_OK)], 0, 25)
filas(["$ uptime", (" 10:42:01 up 153 days,  2:11,  1 user,  load average: 2.00, 1.90, 1.80", T_OK)], 25, 50)
filas(["$ uptime", (" 10:58:15 up 153 days,  2:27,  1 user,  load average: 6.10, 5.82, 2.31", T_ERR)], 50, 75, still=1)
filas(["$ uptime", ("  load average: 6.10, 5.82, 2.31   # 1 y 5 min altos, 15 min bajo: empezó hace poco", T_WARN),
       ("  load average: 6.10, 6.04, 5.97   # los tres altos: sostenida, buscá quién con top", T_ERR),
       ("  (cifras de ejemplo)", T_COM)], 75, 100)

narr(a, [
    (0, 25, "La carga se lee contra la cantidad de núcleos: el mismo número no dice lo mismo en todos los equipos.", None),
    (25, 50, "Por debajo de nproc, cada proceso encuentra un núcleo libre.", a.OK),
    (50, 75, "Por encima, la diferencia es la fila: procesos listos que esperan.", a.BAD),
    (75, 100, "Un pico de un minuto pasa; sostenida en los tres, toca buscar el consumo.", a.AMB),
], y=640, size=16, still_idx=2)

escribir(a, "10-l1", "Carga contra núcleos: cuántos esperan turno",
         "Animación en cuatro tiempos con cuatro núcleos de CPU a la derecha, una fila de espera a la izquierda, un medidor de carga con una marca en 4, igual a nproc, y una terminal abajo. "
         "1: nproc responde 4 y se marcan los cuatro núcleos. "
         "2: con carga 2,00, nginx y postgres ocupan dos núcleos y los otros dos quedan libres; uptime muestra load average 2.00, 1.90, 1.80. "
         "3: con carga 6,10, cuatro procesos corren y php-fpm y rsync esperan turno en la fila: el medidor pasa la marca de 4 en rojo y es saturación. "
         "4: los tres números de uptime son promedios de 1, 5 y 15 minutos: 6.10, 5.82, 2.31 indica que empezó hace poco; 6.10, 6.04, 5.97 indica carga sostenida y hay que buscar quién consume con top. Cifras de ejemplo.",
         [12, 38, 64, 90])
