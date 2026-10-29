#!/usr/bin/env python3
"""Lección 12 · Resumen, "Cómo se ve en la red": la llamada de "la VM no arranca" y el orden de diagnóstico.
Quórum (pvecm status), logs del arranque (journalctl -b -u corosync / pve-cluster), locks (lock: en la
configuración, con las tareas del nodo vacías), qm unlock y la VM arranca; almacenamiento y firewall quedan
para después si hiciera falta.
Fuentes: tarjeta de la lección (orden de diagnóstico, lock de VM, qm unlock solo sin tareas en curso)."""
from _anim_pmx_red import *

a = new(24, "Upgrade y rescate", "La VM no arranca: el orden que ahorra la mañana")
a.steps([
    "Primero el quórum: sin él no funciona nada más. Quorate: Yes.",
    "Logs del arranque de corosync y pve-cluster: limpios.",
    "Locks: la VM quedó con lock: backup de anoche, sin tareas en curso.",
    "qm unlock 100 y la VM arranca. Storage y firewall, si hiciera falta.",
], still=2)

# lista de control
LX, LY = 48, 182
items = [("1", "Quórum", "pvecm status"), ("2", "Logs", "journalctl -b -u ..."), ("3", "Locks", "lock: en la config"),
         ("4", "Almacenamiento", "pvesm status"), ("5", "Firewall", "si hay sospecha")]
for i, (n, t, c) in enumerate(items):
    y = LY + i * 78
    a.add(a.box(LX, y, 360, 66, a.WHITE, a.LINE, rx=12))
    a.add(a.box(LX + 14, y + 15, 36, 36, a.SLATE, rx=18) + a.text(LX + 32, y + 39, n, 16, a.GREY, a.MONO, 700, "middle"))
    a.add(a.text(LX + 66, y + 30, t, 17, a.INK, a.SANS, 600))
    a.add(a.text(LX + 66, y + 52, c, 15, a.GREY, a.MONO))
# avance por la lista
marks = [(0, 0, 25), (1, 25, 50), (2, 50, 75)]
for idx, t0, t1 in marks:
    y = LY + idx * 78
    at(a, a.box(LX - 3, y - 3, 366, 72, "none", a.BLUE, rx=14, sw=3), t0, t1, still=1 if idx == 2 else 0)
    if idx < 2:
        at(a, check(a, LX + 330, y + 33, 14), t0 + 10, 100, still=1)
at(a, a.box(LX - 3, LY + 2 * 78 - 3, 366, 72, "none", a.AMB, rx=14, sw=3) + a.text(LX + 340, LY + 2 * 78 + 39, "acá está", 15, a.AMB, a.SANS, 700, "end"), 62, 100, still=1)
at(a, a.text(LX + 340, LY + 3 * 78 + 39, "no hizo falta", 15, a.GREY, a.SANS, 600, "end") + a.text(LX + 340, LY + 4 * 78 + 39, "no hizo falta", 15, a.GREY, a.SANS, 600, "end"), 82, 100)

# VM
at(a, dev(a, 440, 182, 300, 76, "VM 100 · mutualista", "no arranca · locked", icon="server", tsize=18, stroke=a.BAD, sw=2.5), 0, 86, still=1)
at(a, dev(a, 440, 182, 300, 76, "VM 100 · mutualista", "running", icon="server", tsize=18, stroke=a.OK, sw=2.5), 86, 100)
at(a, xmark(a, 712, 208, 13), 0, 86, still=1)
at(a, check(a, 712, 208, 13), 88, 100)

# terminal
TX, TY, TW, TH = 440, 280, 712, 312
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 18, TY + 28, "TERMINAL DEL NODO", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
L = [TY + 60 + i * 26 for i in range(10)]
at(a, tline(a, TX + 18, L[0], "# pvecm status", MINT) + tline(a, TX + 18, L[1], "Quorate:          Yes", MINT)
   + tline(a, TX + 18, L[2], "Total votes:      3 · Quorum: 2") + tline(a, TX + 18, L[4], "el clúster acepta escrituras: seguimos", SKY), 4, 25)
at(a, tline(a, TX + 18, L[0], "# journalctl -b -u corosync | tail -20", MINT) + tline(a, TX + 18, L[1], "... sin errores, sin cambios de membresía", a.WHITE)
   + tline(a, TX + 18, L[2], "# journalctl -b -u pve-cluster | tail -20", MINT) + tline(a, TX + 18, L[3], "... sin errores", a.WHITE)
   + tline(a, TX + 18, L[5], "la base del clúster está sana: seguimos", SKY), 27, 50)
at(a, tline(a, TX + 18, L[0], "# grep -l '^lock:' /etc/pve/qemu-server/*.conf", MINT) + tline(a, TX + 18, L[1], "/etc/pve/qemu-server/100.conf", GOLD)
   + tline(a, TX + 18, L[2], "lock: backup", GOLD) + tline(a, TX + 18, L[4], "Tareas del nodo: ninguna en curso", a.WHITE)
   + tline(a, TX + 18, L[5], "el backup se cortó con la luz de anoche", SKY), 52, 75, still=1)
at(a, tline(a, TX + 18, L[0], "# qm unlock 100", MINT) + tline(a, TX + 18, L[1], "# qm start 100", MINT)
   + tline(a, TX + 18, L[3], "VM 100: running", MINT) + tline(a, TX + 18, L[5], "unlock solo sin backup, snapshot ni", SKY)
   + tline(a, TX + 18, L[6], "migración en curso sobre esa VM", SKY), 77, 100)

status(a, 628, [
    (0, 25, "Si no hay quórum, todo lo demás falla igual: por eso se mira primero.", a.INK, 0),
    (25, 50, "Los logs del arranque cuentan si corosync o pmxcfs tuvieron problemas.", a.BLUE, 0),
    (50, 75, "Un lock que quedó de una tarea cortada traba solo a esa VM.", a.AMB, 1),
    (75, 100, "Siempre el mismo orden: de lo general a lo particular.", a.OK, 0),
])

write(a, 12, "r1", "La VM no arranca: el orden que ahorra la mañana",
      "Animación en cuatro tiempos con la lista de diagnóstico (1 quórum con pvecm status, 2 logs con journalctl -b -u, 3 locks en la configuración, 4 almacenamiento con pvesm status, 5 firewall si hay sospecha), la VM 100 de una mutualista que no arranca y la terminal del nodo. "
      "1: primero el quórum: pvecm status muestra Quorate: Yes, Total votes 3 y Quorum 2; el clúster acepta escrituras. "
      "2: los logs del último arranque de corosync y de pve-cluster no muestran errores ni cambios de membresía. "
      "3: grep -l '^lock:' encuentra /etc/pve/qemu-server/100.conf con lock: backup, de un backup que se cortó con la luz de anoche; las tareas del nodo no muestran nada en curso. "
      "4: qm unlock 100 y qm start 100: la VM queda running. Almacenamiento y firewall no hicieron falta. qm unlock va solo cuando no hay backup, snapshot ni migración en curso sobre esa VM.",
      [8, 36, 62, 66, 92])
