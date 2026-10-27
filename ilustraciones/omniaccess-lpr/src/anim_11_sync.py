"""Teoría de Padrón y reportes: la sincronización incremental aplica solo diferencias; Reemplazo total vacía y recarga."""
from _anim_lpr import *

caps = ["Analizar compara, cámara por cámara, la base con lo que tiene la cámara.",
        "Incremental agrega lo que falta y quita lo que sobra.",
        "Lo que está en lista negra pasa a la lista de bloqueo.",
        "Reemplazo total vacía y recarga todo: mientras tanto, la cámara no abre sola."]
a = new(24, "Sincronizar", "Sincronizar matrículas: solo las diferencias", caps, still=2)
S = [sp[0] for sp in a.spans]

# base
BX, BY, BW = 48, 176, 340
a.add(a.box(BX, BY, BW, 360, a.WHITE, a.LINE))
a.add(a.text(BX + 20, BY + 34, "Base · padrón", 18, a.INK, a.SANS, 600))
base = [("SBA1234", ""), ("SCD5678", ""), ("SBB4321", ""), ("SAC1010", "nueva"), ("SAB2024", "lista negra")]
ry = lambda i: BY + 74 + i * 52
for i, (p, tag) in enumerate(base):
    a.add(a.box(BX + 16, ry(i) - 22, BW - 32, 40, a.SLATE, rx=8) + a.text(BX + 32, ry(i) + 5, p, 17, a.INK, a.MONO, 600))
    if tag:
        fg, bg = (a.BAD, a.BADBG) if tag == "lista negra" else (a.BLUE, "#E3EEF9")
        a.add(a.pill(BX + BW - 26, ry(i) - 16, tag, fg, bg, size=13, h=26, anchor="end"))

# cámara
CX, CY, CW = 648, 176, 504
a.add(a.box(CX, CY, CW, 360, a.WHITE, a.LINE))
a.add(a.text(CX + 20, CY + 34, "Cámara P1 · sus listas", 18, a.INK, a.SANS, 600))
a.add(a.box(CX + 14, CY + 52, 230, 292, a.OKBG, None, rx=10) + a.text(CX + 28, CY + 76, "lista blanca", 15, a.OK, a.MONO, 600))
a.add(a.box(CX + 258, CY + 52, 232, 292, a.BADBG, None, rx=10) + a.text(CX + 272, CY + 76, "bloqueo", 15, a.BAD, a.MONO, 600))
cy = lambda i: CY + 112 + i * 46
WX, KX = CX + 129, CX + 374


def chip_at(x, y, p, fg=None, bg=None):
    return a.pill(x, y - 15, p, fg or a.WHITE, bg or a.INK, size=15, h=30, anchor="middle")


def kf(points):
    return a.keyframes(points)


R0 = S[3] + 2  # vacía
for i, p in enumerate(["SBA1234", "SCD5678", "SBB4321"]):
    back = S[3] + 10 + i * 2
    a.add(a.group(chip_at(WX, cy(i), p), kf([(0, 1), (R0, 1), (R0 + .8, 0), (back, 0), (back + .8, 1), (100, 1)]), still=1))
# SDE9090: sobra
a.add(a.group(chip_at(WX, cy(3), "SDE9090"), kf([(0, 1), (S[1] + 6, 1), (S[1] + 7.5, 0), (100, 0)]), still=0))
vis(a, a.box(WX - 70, cy(3) - 19, 140, 38, "none", a.AMB, rx=19, sw=3), 0, d0=4)
vis(a, a.box(WX - 70, cy(4) - 19, 140, 38, "none", a.BAD, rx=19, sw=3), 0, d0=6)
# SAC1010: falta → viaja desde la base
mover(a, chip_at(0, 0, "SAC1010", a.WHITE, a.BLUE), [(S[1] + 8, BX + BW - 110, ry(3)), (S[1] + 14, WX, cy(3)), (S[1] + 15, WX, cy(3))])
back = S[3] + 16
a.add(a.group(chip_at(WX, cy(3), "SAC1010"), kf([(0, 0), (S[1] + 15, 0), (S[1] + 15.5, 1), (R0, 1), (R0 + .8, 0), (back, 0), (back + .8, 1), (100, 1)]), still=1))
# SAB2024: blanca → bloqueo
a.add(a.group(chip_at(WX, cy(4), "SAB2024"), kf([(0, 1), (S[2] + 5, 1), (S[2] + 5.5, 0), (100, 0)]), still=0))
mover(a, chip_at(0, 0, "SAB2024", a.WHITE, a.BAD), [(S[2] + 5, WX, cy(4)), (S[2] + 11, KX, cy(0)), (S[2] + 12, KX, cy(0))])
back = S[3] + 18
a.add(a.group(chip_at(KX, cy(0), "SAB2024", a.WHITE, a.BAD), kf([(0, 0), (S[2] + 12, 0), (S[2] + 12.5, 1), (R0, 1), (R0 + .8, 0), (back, 0), (back + .8, 1), (100, 1)]), still=1))
a.add(a.group(a.text(CX + CW / 2, CY + 210, "vacía: la cámara no abre sola", 19, a.BAD, a.SANS, 600, "middle"), a.show(S[3] + 3, S[3] + 9.5, 0.6), still=0))

# panel del medio
MX, MW = 408, 220
a.add(a.box(MX, 176, MW, 360, a.SLATE, None, rx=14))
vis(a, a.text(MX + 16, 210, "Analizar", 18, a.INK, a.SANS, 600), 0, 2)
diffs = [("+ SAC1010", "a agregar", a.BLUE, 1, 8), ("− SDE9090", "a quitar", a.AMB, 1, 7), ("→ SAB2024", "a bloqueo", a.BAD, 2, 12)]
for k, (p, lab, c, st, dd) in enumerate(diffs):
    y = 256 + k * 74
    vis(a, a.text(MX + 16, y, p, 18, c, a.MONO, 600) + a.text(MX + 16, y + 24, lab, 15, a.GREY, a.MONO), 0, 2, d0=3 + k * 2)
    vis(a, f'<path d="M{MX + 180} {y - 6} l6 7 l12 -14" fill="none" stroke="{a.OK}" stroke-width="3.5"/>', st, 2, d0=dd)
vis(a, a.text(MX + 16, 210, "Reemplazo total", 18, a.BAD, a.SANS, 600)
    + a.text(MX + 16, 250, "borra la lista", 16, a.TXT) + a.text(MX + 16, 274, "y recarga todo", 16, a.TXT)
    + a.text(MX + 16, 324, "solo para reparar,", 16, a.TXT) + a.text(MX + 16, 348, "fuera del horario", 16, a.TXT) + a.text(MX + 16, 372, "de más tránsito", 16, a.TXT), 3)

a.add(a.text(48, 580, "Incremental compara y aplica solo diferencias: la cámara sigue abriendo a los de siempre mientras tanto.", 17, a.TXT))
a.add(a.text(48, 612, "Dispositivos → vista Cámaras LPR → Sincronizar matrículas a las cámaras → Analizar", 16, a.BLUE, a.MONO, 600))
write(a, "11-t1.svg", "Sincronización incremental", [12, 40, 62, 80, 96])
