"""Teoría lección 5: thin permite sobreasignar; si el datastore se llena con la VM corriendo, la VM se detiene."""
from _avmw import *

a = new(20, "Thin: prometés más espacio del que tenés")
a.steps(["Tres VMs thin de 500 GB cada una en un datastore de 1 TB.",
         "Al principio ocupan poco: entra todo y sobra.",
         "Las grabaciones y las bases crecen: el datastore llega al 100 %.",
         "Sin espacio para escribir, las VMs se detienen."], still=2)

a.add(a.text(48, 200, "Provisionado: 3 × 500 GB = 1,5 TB", 20, a.INK, a.MONO, 600))
a.add(a.text(48, 232, "Datastore real: 1 TB", 20, a.INK, a.MONO, 600))
# datastore
DX, DY, DW, DH = 48, 270, 1104, 90
a.add(a.box(DX, DY, DW, DH, a.WHITE, a.GREY, rx=14, sw=2.5))
a.add(a.text(DX, DY + DH + 28, "datastore1 · 1 TB", 16, a.GREY, a.MONO, 600))
cols = [a.BLUE, a.CYAN, "#5B8DEF"]
names = ["VM video", "VM acceso", "VM ERP"]
# ocupación por tiempo: (pct ciclo, ancho de cada una)
w0, w1, w2 = 80, 220, DW / 3
for i, (col, n) in enumerate(zip(cols, names)):
    k = a.keyframes([(0, 0.0001), (25, w0 / DW), (50, w1 / DW), (68, w2 / DW), (100, w2 / DW)], "transform", "scaleX({})")
    xi = DX + i * DW / 3
    bar = f'<rect x="{xi}" y="{DY + 6}" width="{DW}" height="{DH - 12}" rx="10" fill="{col}"/>'
    a.add(a.group(bar, k, still=0, origin=f"{xi}px {DY}px"))
    # rótulos en las VMs
    a.add(vmbox(a, 48 + i * 376, 420, 352, 64, n, "thin · 500 GB"))
# cuadro fijo: el datastore lleno
full = "".join(f'<rect x="{DX + i * DW / 3 + 4}" y="{DY + 6}" width="{DW / 3 - 8}" height="{DH - 12}" rx="10" fill="{c}"/>' for i, c in enumerate(cols))
a.add(a.group(full, a.keyframes([(0, 0), (100, 0)]), still=1))
at(a, chip(a, 1152, 384, "100 % ocupado", "bad", anchor="end"), 66, 100, 1)
for i in range(3):
    at(a, a.box(48 + i * 376, 420, 352, 64, a.BADBG, a.BAD, rx=12, sw=3) + a.text(48 + i * 376 + 48, 446, names[i], 16, a.BAD, a.SANS, 600)
       + a.text(48 + i * 376 + 48, 468, "detenida: sin espacio", 14, a.BAD, a.MONO, 600), 75, 100, 0)
caption(a, 560, [(0, 25, "Thin reserva solo lo escrito: por eso se puede prometer más de lo que hay.", None),
                 (25, 50, "Con espacio de sobra nadie lo nota.", a.OK),
                 (50, 75, "Nadie avisa hasta que el datastore se llena.", a.AMB),
                 (75, 100, "Por eso: sumar lo que puede crecer y compararlo con el libre.", a.BAD)], still=2)
write(a, "5-t1.svg", "Thin: prometés más espacio del que tenés",
      "Animación en cuatro tiempos. Tres VMs con disco thin de 500 GB cada una, 1,5 TB provisionados, en un datastore de 1 TB. "
      "1: se muestran los números: 1,5 TB prometidos contra 1 TB real. 2: al principio las tres ocupan poco y sobra espacio. "
      "3: los datos crecen y la barra del datastore llega al 100 por ciento. 4: sin espacio para escribir, las tres VMs quedan detenidas, marcadas en rojo.")
