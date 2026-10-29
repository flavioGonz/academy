#!/usr/bin/env python3
"""Lección 11 · Laboratorio, paso 4: rsync -avn /srv/datos/ backup@10.10.10.20:/respaldos/servidor1/.
rsync compara cada archivo de origen y destino (por defecto, tamaño y fecha de modificación): los iguales se saltean,
los distintos o nuevos se copian. Con -n solo muestra la lista; sin -n copia solo eso. La barra final del origen
copia el contenido de la carpeta. Fuentes: rsync(1) (quick check por tamaño y fecha, -n/--dry-run, barra final del
origen), teoría y laboratorio de la lección. Archivos de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · BACKUP · LABORATORIO", "rsync -n: la lista de lo que copiaría, sin copiar")
a.steps([
    "rsync compara cada archivo: tamaño y fecha en origen y destino.",
    "Los iguales se saltean; los distintos o nuevos van a la lista.",
    "Con -n es un simulacro: muestra la lista y no copia nada.",
    "Sin -n copia solo esos dos; lo demás ya estaba.",
], still=2)

OX, DX, W = 48, 732, 420
a.add(a.box(OX, 170, W, 270, a.WHITE, "#C2D4E6", rx=16) + a.text(OX + 18, 200, "Origen", 17, a.INK, a.HEAD, 600) + mono(a, OX + 100, 200, "/srv/datos/", 15, a.BLUE, 700))
a.add(a.box(DX, 170, W, 270, a.INK, None, rx=16) + a.text(DX + 18, 200, "Destino", 17, "#FFFFFF", a.HEAD, 600) + mono(a, DX + 106, 200, "10.10.10.20:/respaldos/servidor1/", 14, LIGHT, 600))
F = [("planos/plano-a.pdf", "2,1M · 10/09", "2,1M · 10/09", "igual"), ("fotos/obra-01.jpg", "4,8M · 28/10", "4,6M · 21/10", "cambió"),
     ("informe.docx", "310K · 28/10", None, "nuevo"), ("notas.txt", "4K · 02/10", "4K · 02/10", "igual")]
for i, (n, so, de, st) in enumerate(F):
    y = 220 + i * 52
    a.add(a.box(OX + 14, y, W - 28, 42, a.SLATE, None, rx=8) + mono(a, OX + 28, y + 27, n, 15, a.INK, 700) + mono(a, OX + W - 28, y + 27, so, 14, a.GREY, 500, "end"))
    if de:
        a.add(a.box(DX + 14, y, W - 28, 42, "#0B3A66", None, rx=8) + mono(a, DX + 28, y + 27, n, 15, "#FFFFFF", 700) + mono(a, DX + W - 28, y + 27, de, 14, LIGHT, 500, "end"))
    else:
        en(a, a.box(DX + 14, y, W - 28, 42, "none", "#7FA6C9", rx=8, sw=2, extra='stroke-dasharray="6 5"') + a.text(DX + 28, y + 27, "no existe", 15, LIGHT, a.SANS, 600), 0, 82, still=1)
    # comparación
    t0 = 4 + i * 5
    viaje(a, "", [(OX + W + 6, y + 21), (DX - 6, y + 21)], t0, t0 + 3, inner=f'<circle r="7" fill="{a.CYAN}"/>', hold=0)
    ok = st == "igual"
    en(a, a.pill(600, y + 6, st if not ok else "igual: se saltea", a.OK if ok else a.AMB, a.OKBG if ok else a.AMBBG, 14, 30, "middle"), 26 + i * 2, 100, still=1)
    if not ok:
        en(a, a.box(OX + 10, y - 4, W - 20, 50, "none", a.AMB, rx=10, sw=2.5), 28, 100, still=1)
        viaje(a, n.split("/")[-1], [(OX + W - 30, y + 21), (DX + 120, y + 21)], 80 + i, 86 + i, bg=a.AMB, size=13, hold=1)
        en(a, a.box(DX + 14, y, W - 28, 42, "#0B3A66", MINT, rx=8, sw=2) + mono(a, DX + 28, y + 27, n, 15, MINT, 700) + mono(a, DX + W - 28, y + 27, so, 14, MINT, 500, "end"), 86 + i, 100)
en(a, a.text(600, 436, "comparando tamaño y fecha", 15, a.CYAN, a.SANS, 700, "middle"), 3, 25)
en(a, a.box(DX - 6, 164, W + 12, 282, "none", GOLD, rx=20, sw=3, extra='stroke-dasharray="8 6"') + a.text(600, 436, "-n: el destino no cambia", 15, a.AMB, a.SANS, 700, "middle"), 52, 75, still=1)

# terminal
TY = 458
a.add(tterm(a, 48, TY, 1104, 150))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 30 + i * 25, r, 14) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ rsync -avn /srv/datos/ backup@10.10.10.20:/respaldos/servidor1/", ("sending incremental file list", T_OUT)], 0, 50)
filas(["$ rsync -avn /srv/datos/ backup@10.10.10.20:/respaldos/servidor1/", ("sending incremental file list", T_OUT), ("fotos/obra-01.jpg", T_WARN), ("informe.docx", T_WARN),
       ("sent ... bytes  received ... bytes  ...  (DRY RUN)", T_COM)], 50, 75, still=1)
filas(["$ rsync -av /srv/datos/ backup@10.10.10.20:/respaldos/servidor1/", ("fotos/obra-01.jpg", T_OK), ("informe.docx", T_OK),
       ("# /srv/datos/ con barra: copia el contenido; sin barra, crearía servidor1/datos/", T_COM)], 75, 100)

narr(a, [
    (0, 25, "rsync no copia todo de nuevo: primero mira qué tiene cada lado.", None),
    (25, 50, "Lo que cambió y lo nuevo es lo único que va a viajar.", a.AMB),
    (50, 75, "El simulacro te deja ver la lista antes, sobre todo si el destino es importante.", a.OK),
    (75, 100, "Si la lista del -n es la esperada, la corrida real hace exactamente eso.", a.OK),
], y=640, still_idx=2)

escribir(a, "11-l1", "rsync -n: la lista de lo que copiaría, sin copiar",
         "Animación en cuatro tiempos con el origen /srv/datos/ a la izquierda y el destino 10.10.10.20:/respaldos/servidor1/ a la derecha, con cuatro archivos de ejemplo; abajo, la terminal. "
         "1: rsync compara cada archivo por tamaño y fecha. "
         "2: planos/plano-a.pdf y notas.txt son iguales y se saltean; fotos/obra-01.jpg cambió y informe.docx es nuevo, en ámbar. "
         "3: con rsync -avn, la salida lista fotos/obra-01.jpg e informe.docx con la marca DRY RUN y el destino no cambia. "
         "4: con rsync -av, sin la n, se copian solo esos dos; la barra final de /srv/datos/ copia el contenido de la carpeta, y sin barra crearía servidor1/datos/.",
         [10, 38, 64, 94])
