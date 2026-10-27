"""Teoría lección 7: backup en modo snapshot (fsfreeze + copy-before-write)."""
from _apmx import *

a = new(24, "Backup en modo snapshot: la VM no se detiene")
a.steps(["Arranca vzdump: el guest agent congela el disco un instante.",
         "Se descongela: la VM sigue y el backup copia bloque por bloque.",
         "La VM pisa un bloque sin copiar: antes, el viejo va al backup.",
         "Terminó: el archivo es la foto del instante en que arrancó."], still=2)
BX, S, G = 300, 84, 14
DY, KY = 250, 470
cx = [BX + i * (S + G) + S / 2 for i in range(8)]


def blk(i, y, lab, fill, st, col, dash=False):
    x = BX + i * (S + G)
    d = 'stroke-dasharray="6 5"' if dash else ""
    return a.box(x, y, S, S, fill, st, rx=10, sw=2.5, extra=d) + a.text(x + S / 2, y + S / 2 + 8, lab, 22, col, a.MONO, 700, "middle")


a.add(a.text(48, DY + 38, "Disco de", 18, a.INK, a.SANS, 600) + a.text(48, DY + 62, "la VM 100", 18, a.INK, a.SANS, 600))
a.add(a.text(48, KY + 38, "Archivo", 18, a.INK, a.SANS, 600) + a.text(48, KY + 62, "de backup", 18, a.INK, a.SANS, 600))
for i in range(8):
    a.add(blk(i, DY, str(i + 1), "#E5F0FB", a.BLUE, a.INK))
    a.add(blk(i, KY, "", "#FFFFFF", a.LINE, a.GREY, True))
# congelado (tiempo 1)
at(a, a.box(BX - 8, DY - 8, 8 * (S + G) - G + 16, S + 16, "none", a.CYAN, rx=14, sw=4) + chip(a, BX, DY - 52, "fsfreeze: escrituras en pausa", "cyan"), 0, 25, 0)
at(a, chip(a, BX, DY - 52, "VM 100 corriendo", "ok"), 25, 100, 1)
# copias normales
times = {0: 28, 1: 33, 2: 38, 3: 43, 5: 58, 4: 66, 6: 78, 7: 84}
for i, t in times.items():
    at(a, blk(i, KY, str(i + 1), a.OKBG, a.OK, a.OK), t, 100, 1 if t < 75 else 0)
# tiempo 3: escritura sobre el bloque 6 (índice 5)
at(a, a.arrow(f"M{cx[5]} {DY + S + 6} V{KY - 8}", a.OK, 4) + a.text(cx[5] + 14, DY + S + 70, "primero el viejo", 16, a.OK, a.SANS, 700), 56, 75, 1)
at(a, chip(a, cx[5] - 30, DY - 52, "escritura nueva en espera", "amb"), 52, 62, 0)
at(a, blk(5, DY, "6'", a.AMBBG, a.AMB, a.AMB) + a.text(cx[5], DY - 10, "dato nuevo", 15, a.AMB, a.SANS, 700, "middle"), 62, 100, 1)
at(a, chip(a, cx[0] - 40, KY + S + 18, "foto del instante en que arrancó: con el 6 viejo", "ok"), 88, 100, 0)
caption(a, 626, [(0, 25, "Con agent: 1 y el agente corriendo, Proxmox congela el sistema de archivos para no copiar algo a medio escribir.", None),
                 (25, 50, "QEMU pone un filtro copy-before-write en el disco y lo descongela: la VM no se entera del backup.", a.OK),
                 (50, 75, "Si la VM escribe un bloque que falta copiar, el viejo sale primero: la escritura espera al destino del backup.", a.AMB),
                 (75, 100, "Por eso el backup es consistente aunque la VM nunca se haya apagado. Lo que cambió va en el próximo.", a.OK)], still=2)
write(a, "7-t1.svg", "Backup en modo snapshot: la VM no se detiene",
      "Animación en cuatro tiempos de un backup de vzdump en modo snapshot de la VM 100, con ocho bloques de disco y un archivo de backup vacío. "
      "1: al arrancar, el guest agent congela el sistema de archivos un instante y las escrituras quedan en pausa. "
      "2: QEMU instala un filtro copy-before-write, descongela y la VM sigue corriendo mientras el backup copia los bloques 1 a 4. "
      "3: la VM quiere escribir el bloque 6, que todavía no se copió: primero el bloque 6 viejo va al backup y recién después se escribe el dato nuevo. "
      "4: se copian los bloques que faltan y el archivo queda como la foto del instante en que arrancó, con el bloque 6 viejo.", pcts=(12, 37, 62, 92))
