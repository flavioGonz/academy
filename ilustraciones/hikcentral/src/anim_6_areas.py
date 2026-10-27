"""Teoría de Áreas primero: importar canales a un área es lo que los hace visibles."""
from _anim_hc import *

caps = ["El NVR queda agregado y online, con sus 8 canales sin área.",
        "Se importan los canales 1 a 4 a Nave 1 y del 5 al 8 a Nave 2.",
        "El operador de Nave 1 abre su vista: aparecen sus cuatro cámaras.",
        "Abre Depósito, el área madre: There is no camera in this area."]
a = new(26, "Áreas", "Un canal existe para el operador cuando está en un área", caps, still=2)

# NVR
a.add(card(a, 48, 186, 330, 80, "NVR del depósito", "online en Device"))
CH = [(60 + (k % 4) * 78, 290 + (k // 4) * 52) for k in range(8)]
for k, (x, y) in enumerate(CH):
    a.add(a.box(x, y, 66, 38, a.SLATE, a.LINE, rx=10))
    a.add(a.text(x + 33, y + 25, f"ch{k + 1}", 15, a.GREY, a.MONO, 600, "middle"))
vis(a, a.text(60, 420, "sin área: ni vivo, ni reproducción, ni eventos", 15, a.BAD, a.SANS, 600), 0)
vis(a, a.text(60, 420, "importados: cada canal en su área", 15, a.OK, a.SANS, 600), 1, 3)

# árbol de áreas
a.add(a.box(420, 186, 340, 64, a.WHITE, a.LINE, rx=12))
a.add(a.text(440, 225, "Depósito", 18, a.INK, a.SANS, 600))
a.add(a.text(740, 225, "área madre", 14, a.GREY, a.MONO, anchor="end"))
vis(a, a.box(420, 186, 340, 64, "none", a.AMB, rx=12, sw=3), 3)
for j, (nm, y) in enumerate((("Nave 1", 290), ("Nave 2", 410))):
    a.add(f'<path d="M440 250 V{y + 30} H470" fill="none" stroke="#C2D4E6" stroke-width="2"/>')
    a.add(a.box(470, y, 290, 100, a.WHITE, a.LINE, rx=12))
    a.add(a.text(490, y + 30, nm, 17, a.INK, a.SANS, 600))
    for k in range(4):
        kk = j * 4 + k
        a.add(a.group(a.pill(490 + k * 66, y + 50, f"{kk + 1:02d}", a.WHITE, a.CYAN, size=13), a.show(ph(a, 1)[0] + 9 + kk * 1.6, 100), still=1))
vis(a, a.box(470, 290, 290, 100, "none", a.CYAN, rx=12, sw=3), 2)

s0, s1 = ph(a, 1)
for k in range(8):
    x, y = CH[k]
    tx, ty = (490 + (k % 4) * 66 + 22, (340 if k < 4 else 460) + 14)
    token(a, f"ch{k + 1}", [(s0 + 1 + k * 1.6, x + 33, y + 19), (s0 + 9 + k * 1.6, tx, ty)], bg=a.CYAN, size=13)

# vista del operador
a.add(a.box(800, 186, 352, 330, a.WHITE, a.LINE, rx=16))
a.add(a.text(820, 218, "Control Client · operador Nave 1", 15, a.TXT, a.SANS, 600))
for k in range(4):
    x, y = 820 + (k % 2) * 160, 240 + (k // 2) * 118
    a.add(a.box(x, y, 150, 108, a.SLATE, rx=8))
    vis(a, a.box(x, y, 150, 108, a.INK, rx=8) + a.text(x + 75, y + 60, f"CAM-0{k + 1}", 15, DARK_SUB, a.MONO, 600, "middle"), 2)
vis(a, a.box(820, 330, 312, 64, "#FFF3DC", "#B26A00", rx=10) + a.text(976, 368, "There is no camera in this area", 14, "#B26A00", a.MONO, 600, "middle"), 3)

a.add(a.text(48, 572, "El equipo puede estar online y aun así no existir para el operador. Las cámaras de un", 17, a.TXT))
a.add(a.text(48, 600, "área hija no aparecen en la madre: cada recurso va donde el operador lo busca.", 17, a.TXT))
write(a, "6-t1.svg", "Importar canales a un área", [10, 38, 62, 90])
