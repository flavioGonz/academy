#!/usr/bin/env python3
"""Lección 8 · Laboratorio, paso 2: qué hace el verify job. Relee cada trozo de los backups, recalcula su SHA-256 y
lo compara con el que tiene registrado; si un trozo se degradó o lo cifró un ransomware, no coincide y el backup
queda con la verificación fallida. --ignore-verified true --outdated-after 30 saltea lo verificado hace menos de 30
días. Fuentes: documentación de PBS (verify, SHA-256, reverificar al menos mensual, bit rot, ransomware),
tarjeta de la lección (comando del paso 2)."""
from _anim_pmx_red import *

a = new(24, "PBS sin sorpresas", "verify: releer cada trozo y comparar su hash", lab=True)
a.steps([
    "A la 01:00 corre verif-main: relee los trozos de cada backup.",
    "El SHA-256 coincide con el registrado: el backup queda verificado.",
    "Un trozo se degradó en el disco: el hash no coincide y el job falla.",
    "Lo verificado hace menos de 30 días se saltea; lo demás se relee.",
], still=2)

# trozos en el datastore
DX, DY, DW, DH = 48, 182, 330, 330
a.add(a.box(DX, DY, DW, DH, a.WHITE, a.LINE, rx=14))
a.add(glyph(a, "server", DX + 18, DY + 16))
a.add(a.text(DX + 60, DY + 36, "datastore main", 17, a.INK, a.SANS, 600))
a.add(a.text(DX + 60, DY + 60, ".chunks/ · por su hash", 15, a.GREY, a.MONO))
CH = [("3f9a…", "ok"), ("a71c…", "ok"), ("c02e…", "bad"), ("e5b8…", "ok")]
CY0 = DY + 84
for i, (h, st) in enumerate(CH):
    y = CY0 + i * 56
    a.add(a.box(DX + 18, y, DW - 36, 46, a.SLATE, rx=8) + a.text(DX + 34, y + 29, f"trozo {h}", 15, a.INK, a.MONO, 600))
    if st == "bad":
        a.add(during(a, a.box(DX + 18, y, DW - 36, 46, a.BADBG, a.BAD, rx=8, sw=2) + a.text(DX + 34, y + 29, f"trozo {h}", 15, a.BAD, a.MONO, 700)
                     + a.text(DX + DW - 34, y + 29, "bit rot", 15, a.BAD, a.MONO, 700, "end"), 50, 100, still=1))

# proceso de verificación
VX, VY, VW, VH = 420, 230, 330, 210
a.add(a.box(VX, VY, VW, VH, a.INK, rx=16))
a.add(a.text(VX + 22, VY + 34, "verify · SHA-256", 18, a.WHITE, a.SANS, 600))
rows = [  # (t0, t1, trozo, resultado, ok, still)
    (6, 25, "3f9a…", "3f9a… = 3f9a…", True, 0),
    (28, 50, "a71c…", "a71c… = a71c…", True, 0),
    (53, 75, "c02e…", "9b41… ≠ c02e…", False, 1),
    (78, 100, "e5b8…", "hace 3 días", None, 0),
]
for t0, t1, tz, res, ok, st in rows:
    if ok is None:
        s = a.text(VX + 22, VY + 74, "backup vm/101 · lunes", 15, SKY, a.MONO)
        s += a.text(VX + 22, VY + 112, "última verificación:", 15, SKY, a.MONO)
    else:
        s = a.text(VX + 22, VY + 74, f"relee trozo {tz}", 15, SKY, a.MONO)
        s += a.text(VX + 22, VY + 112, "calcula y compara:", 15, SKY, a.MONO)
    col = MINT if ok else (CORAL if ok is False else GOLD)
    s += a.text(VX + 22, VY + 146, res, 17, col, a.MONO, 700)
    lab = "coincide" if ok else ("no coincide" if ok is False else "menos de 30: se saltea")
    s += a.text(VX + 22, VY + 182, lab, 15, col, a.SANS, 600)
    at(a, s, t0, t1, still=st)
# trozos que viajan al verificador
for i, t in enumerate((3, 26, 51)):
    y = CY0 + i * 56 + 23
    go(a, "lee", [(DX + DW - 10, y), (VX + 10, VY + 70)], t, t + 3, a.CYAN if i < 2 else a.BAD, hold=0.3)

# backups (snapshots)
SX, SY, SW, SH = 790, 182, 362, 330
a.add(a.box(SX, SY, SW, SH, a.WHITE, a.LINE, rx=14))
a.add(a.text(SX + 18, SY + 32, "Content · estado de verificación", 16, a.INK, a.SANS, 600))
SN = [("vm/100 · martes", 25, "ok", 0), ("vm/101 · martes", 48, "ok", 0), ("vm/100 · miércoles", 73, "bad", 1), ("vm/101 · lunes", 98, "skip", 0)]
for i, (n, t, st, stl) in enumerate(SN):
    y = SY + 56 + i * 66
    a.add(a.box(SX + 18, y, SW - 36, 54, a.SLATE, rx=8) + a.text(SX + 34, y + 33, n, 15, a.INK, a.MONO, 600))
    if st == "ok":
        at(a, check(a, SX + SW - 44, y + 27, 13) + a.text(SX + SW - 66, y + 33, "OK", 15, a.OK, a.MONO, 700, "end"), t - 4 if t > 4 else 0, 100, still=1)
    elif st == "bad":
        at(a, xmark(a, SX + SW - 44, y + 27, 13) + a.text(SX + SW - 66, y + 33, "failed", 15, a.BAD, a.MONO, 700, "end"), 58, 100, still=1)
        at(a, a.box(SX + 14, y - 4, SW - 28, 62, "none", a.BAD, rx=10, sw=2.5), 58, 75, still=1)
    else:
        at(a, a.text(SX + SW - 34, y + 33, "ya verificado", 15, a.AMB, a.MONO, 700, "end"), 80, 100)
        at(a, a.text(SX + SW - 34, y + 33, "pendiente", 15, a.GREY, a.MONO, 400, "end"), 0, 80, still=1)
at(a, chip(a, VX, VY + VH + 16, "el job falla y avisa", "bad"), 58, 75, still=1)

# terminal
TX, TY, TW, TH = 48, 548, 1104, 52
a.add(a.box(TX, TY, TW, TH, a.INK, rx=12))
a.add(tline(a, TX + 18, TY + 33, "# proxmox-backup-manager verify-job create verif-main --store main --schedule '01:00'", MINT))
a.add(during(a, a.box(TX, TY, TW, TH, a.INK, rx=12) + tline(a, TX + 18, TY + 33, "# ... verify-job create verif-main --store main --schedule '01:00' --ignore-verified true --outdated-after 30", GOLD), 75, 100))

status(a, 636, [
    (0, 25, "Cada trozo se guarda con su hash: releerlo y recalcularlo dice si sigue igual.", a.INK, 0),
    (25, 50, "Un backup verificado se puede restaurar sin sorpresas.", a.OK, 0),
    (50, 75, "Un disco que se degrada o un ransomware que cifra el datastore: el hash lo delata.", a.BAD, 1),
    (75, 100, "Diario lo nuevo y, como mínimo una vez al mes, todo otra vez.", a.AMB, 0),
])

write(a, 8, "l1", "verify: releer cada trozo y comparar su hash",
      "Animación en cuatro tiempos con el datastore main y sus trozos guardados en .chunks por su hash, el proceso de verificación con SHA-256 y la lista Content con el estado de cada backup. "
      "1: a la 01:00 corre el verify job verif-main y relee el trozo 3f9a; recalcula su SHA-256, coincide, y el backup vm/100 del martes queda OK. "
      "2: relee el trozo a71c, el hash coincide con el registrado y vm/101 del martes queda verificado. "
      "3: el trozo c02e se degradó en el disco por bit rot; el hash recalculado, 9b41, no coincide con c02e, el backup vm/100 del miércoles queda con la verificación fallida y el job falla y avisa. Lo mismo pasaría si un ransomware cifrara el datastore. "
      "4: con --ignore-verified true --outdated-after 30, vm/101 del lunes, verificado hace 3 días, se saltea; lo verificado hace más de 30 días se vuelve a leer. Conviene verificar diario lo nuevo y todo, como mínimo, una vez al mes.",
      [10, 36, 62, 66, 90])
