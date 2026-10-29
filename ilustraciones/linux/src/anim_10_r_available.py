#!/usr/bin/env python3
"""Lección 10 (Available, no free), Resumen: la RAM de un servidor que lleva días prendido. free es poco porque
Linux usa la RAM que sobra como caché de disco; esa caché se suelta cuando un programa pide memoria, y available
estima cuánto se puede dar sin ir a swap. Lo que alarma es available bajo con swap en uso. Fuentes: teoría de la
lección (buff/cache, MemAvailable desde el kernel 3.14, el Server B de linuxblog.io) y free(1). Cifras de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · MEMORIA · CÓMO SE VE", "free bajo y anda perfecto: la caché se suelta")
a.steps([
    "free -h: free dice 312 Mi y parece poco; available dice 5,4 Gi.",
    "buff/cache es lo que Linux leyó del disco y guardó por si vuelve.",
    "Un programa pide 2 GB: el kernel suelta caché y se los da, sin swap.",
    "Lo que alarma es available bajo y swap en uso, no free.",
], still=2)

BX, BY, BW, BH = 48, 250, 1104, 64
G = BW / 7.7
a.add(a.text(BX, BY - 44, "RAM · 7,7 Gi en total (ejemplo)", 16, a.INK, a.HEAD, 600))


def barra(used, free, cache, t0, t1, still=0, warn=False):
    xs = BX
    s = ""
    for val, fill, fg, lbl in ((used, a.BLUE, "#FFFFFF", "used"), (cache, a.CYAN, "#FFFFFF", "buff/cache"), (free, "#C2D4E6", a.INK, "free")):
        w = val * G
        s += a.box(xs, BY, w, BH, fill, "#FFFFFF", rx=8, sw=2)
        if w > 90:
            s += a.text(xs + 14, BY + 28, lbl, 15, fg, a.MONO, 700) + a.text(xs + 14, BY + 50, f"{val:.1f} Gi".replace(".", ","), 15, fg, a.MONO, 500)
        xs += w
    if free * G <= 90:
        s += a.text(BX + BW - 4, BY - 10, "free", 15, a.GREY, a.MONO, 700, "end")
    # available
    av = cache + free - 0.2 if not warn else 0.2
    x0 = BX + used * G
    s += camino(f"M{x0 + 4} {BY + BH + 12} V{BY + BH + 24} H{BX + BW - 4} V{BY + BH + 12}", a.OK if not warn else a.BAD, 3)
    if warn:
        s += a.text(BX + BW - 4, BY + BH + 50, f"available ≈ {av:.1f} Gi".replace(".", ","), 16, a.BAD, a.MONO, 700, "end")
    else:
        s += a.text(x0 + 12, BY + BH + 50, f"available ≈ {av:.1f} Gi".replace(".", ","), 16, a.OK, a.MONO, 700)
    en(a, s, t0, t1, still)


barra(2.1, 0.3, 5.3, 0, 59.5)
barra(4.1, 0.3, 3.3, 59.5, 76, still=1)
barra(7.2, 0.1, 0.4, 78, 100, warn=True)
en(a, a.text(BX + 2.1 * G + 14, BY + BH + 74, "free + la caché que se puede soltar", 15, a.TXT, a.SANS, 500), 0, 26)

# paso 2: discos y caché
en(a, a.box(BX + 2.1 * G - 4, BY - 6, 5.3 * G + 8, BH + 12, "none", GOLD, rx=12, sw=3), 26, 50)
en(a, a.text(BX + 2.1 * G + 14, BY + BH + 74, "archivos que ya se leyeron: la próxima lectura no va al disco", 15, a.AMB, a.SANS, 600), 26, 52)
# paso 3: el programa entra
blk = a.box(-1 * G, -32, 2 * G, 64, a.NAVY2, "#FFFFFF", rx=10, sw=2) + a.text(0, 6, "grabador pide 2 GB", 16, "#FFFFFF", a.SANS, 700, "middle")
viaje(a, "", [(BX + 3.1 * G, 186), (BX + 3.1 * G, BY + 32)], 52, 59, inner=blk, hold=1.5)
en(a, a.text(BX + 4.1 * G + 14, BY + BH + 74, "la caché bajó 2 Gi; free casi no cambió", 15, a.OK, a.SANS, 600), 60, 76, still=1)

# terminal free -h
TY = 412
a.add(tterm(a, 48, TY, 1104, 110, "FREE -H · COLUMNAS RESUMIDAS"))
def filas(m, s, t0, t1, still=0, col=T_OUT):
    en(a, trow(a, 48, TY + 56, ("             total    used    free   buff/cache   available", T_COM), 15)
       + trow(a, 48, TY + 80, (m, col), 15) + trow(a, 48, TY + 102, (s, T_OUT), 15), t0, t1, still)


filas("Mem:         7.7Gi   2.1Gi   312Mi        5.3Gi       5.4Gi", "Swap:        2.0Gi      0B", 0, 52)
filas("Mem:         7.7Gi   4.1Gi   290Mi        3.3Gi       3.4Gi", "Swap:        2.0Gi      0B", 52, 76, still=1, col=T_OK)
filas("Mem:         7.7Gi   7.2Gi    98Mi        0.4Gi       0.2Gi", "Swap:        2.0Gi   1.5Gi   # ahora sí: falta RAM", 76, 100, col=T_ERR)

# swap
SY = 548
a.add(a.text(48, SY + 20, "swap", 15, a.GREY, a.MONO, 700) + a.box(120, SY, 400, 28, a.SLATE, None, rx=8))
en(a, a.box(120, SY, 300, 28, a.BAD, None, rx=8) + a.text(540, SY + 20, "en uso: el equipo se pone lento", 15, a.BAD, a.SANS, 700), 80, 100)
en(a, a.text(540, SY + 20, "sin usar", 15, a.OK, a.SANS, 600), 0, 78, still=1)

narr(a, [
    (0, 25, "Un servidor con días prendido casi no tiene free: es normal.", None),
    (25, 50, "Linux usa la RAM que sobra como caché de disco, y figura en buff/cache.", a.AMB),
    (50, 75, "Cuando un programa pide, esa caché se libera: por eso available es la cifra que importa.", a.OK),
    (75, 100, "Available cerca de cero y swap creciendo: ahí sí falta memoria.", a.BAD),
], still_idx=2)

escribir(a, "10-r1", "free bajo y anda perfecto: la caché se suelta",
         "Animación en cuatro tiempos con una barra de 7,7 Gi de RAM de ejemplo dividida en used, buff/cache y free, una llave que marca available y la salida de free -h abajo, con la swap. "
         "1: used 2,1 Gi, buff/cache 5,3 Gi y free 312 Mi; available dice 5,4 Gi, que es free más la caché que se puede soltar. "
         "2: se marca buff/cache: archivos que ya se leyeron y se guardan para que la próxima lectura no vaya al disco. "
         "3: un grabador pide 2 GB y entra en la barra: used sube a 4,1 Gi, la caché baja a 3,3 Gi, free casi no cambia y la swap sigue sin usar. "
         "4: otro caso, el que alarma: used 7,2 Gi, available 0,2 Gi y 1,5 Gi de swap en uso: ahí sí falta memoria.",
         [12, 38, 66, 90])
