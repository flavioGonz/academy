import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 26.svg: los cuatro R20
c = Canvas("Akuvox", "Cuatro R20: cambia cómo se entra a la puerta")
vs = [("R20A", "boton", [("un botón", "gray"), ("tarjetas 13,56 y 125", "cyan"), ("QR desde 320.30.12.19", "cyan")], ("sin PIN", "alert")),
      ("R20K", "teclado", [("teclado", "gray"), ("PIN", "cyan"), ("tarjetas 13,56 y 125", "cyan")], None),
      ("R20K-L", "teclado", [("teclado + LTE", "gray"), ("PIN", "cyan"), ("solo 13,56 MHz", "cyan")], None),
      ("R20B", "botones", [("varios botones", "gray"), ("tarjetas", "cyan"), ("+ MD06 / MD12", "gray")], ("sin PIN", "alert"))]
for i, (m, k, chips, bad) in enumerate(vs):
    x = 48 + i * 280
    c.add(panel(x, 122, 264, 430, None, "info"))
    c.add(text(x + 132, 156, m, 22, 700, INK, FM, anchor="middle"))
    c.add(portero(x + 82, 176, k, 0.66))
    for j, (s_, kd) in enumerate(chips):
        c.add(Chip(x + 132, 386 + j * 38, s_, kd, mono=False, anchor="middle"))
    if bad:
        c.add(Chip(x + 132, 386 + 3 * 38, bad[0], bad[1], mono=False, anchor="middle"))
c.add(panel(48, 568, 1104, 60, None, "soft"))
c.add(text(600, 605, "Todos: Linux · aluminio · sin pantalla · IP65 · PoE 802.3af o 12 V 1 A · relé 30 V 2 A", 17, 600, INK, FB, anchor="middle"))
save(c, "26.svg")

# ---------------------------------------------------------------- 26-paso2: la etiqueta engaña
c = Canvas("Akuvox · Paso 2", "La etiqueta engaña: leé el hardware en la web")
c.add(f'<rect x="60" y="150" width="260" height="120" rx="10" fill="{WHITE}" stroke="{INK3}" stroke-width="2" stroke-dasharray="4 4"/>')
c.add(text(80, 186, "ETIQUETA", 14, 600, INK3, FM, ls=1.5))
c.add(text(80, 228, "R20A V3.0", 26, 700, INK, FM))
c.add(arrow((330, 210), (420, 210), "flow", bend="straight"))
c.add(Window(430, 140, 400, 150, "Portero · web", path="Status > Basic > Product Information", rows=[("Hardware Version", "220.x")], hl=0))
c.add(arrow((840, 210), (920, 210), "flow", bend="straight"))
c.add(panel(930, 150, 222, 120, None, "warn"))
c.add(text(1041, 200, "hardware 2", 22, 700, WARN, FB, anchor="middle"))
c.add(text(1041, 232, "no 3", 17, 600, INK2, FB, anchor="middle"))
c.add(Step(430, 140, 2))
c.add(Table(48, 340, ["Empieza con", "Hardware", "Ejemplos"],
            [["20.x", "hardware 1", ""], ["220.x", "hardware 2", "R20A con etiqueta V3.0"], ["320.x", "hardware 3", "R20A V5.0 · R20K V3.0"]],
            [220, 220, 664], hl_row=1, mono_cols=(0,), row_h=46))
c.add(Note(48, 540, 1104, "Cada versión de hardware lleva su propio archivo de firmware: se baja el de la versión real, no el de la etiqueta.", kind="warn", size=16))
save(c, "26-paso2.svg")

# ---------------------------------------------------------------- 26-paso3: decidir la cerradura
c = Canvas("Akuvox · Paso 3", "¿Puede el R20 alimentar la cerradura?")
rows = [("hardware 3 (o R20B V2.0)", "+ fuente 12 V 1,2 A o más", "12 V 500 mA por el relé", "ok"),
        ("hardware 3", "+ PoE + firmware 320.30.11.42 o más", "12 V 500 mA, afectada por el volumen", "warn"),
        ("hardware viejo", "(sin salida de 12 V)", "fuente propia para la cerradura", "alert")]
for i, (hw, cond, res, kd) in enumerate(rows):
    y = 140 + i * 128
    c.add(box(48, y, 300, 100, hw, None, "dark", None, 18))
    c.add(text(366, y + 56, cond, 16, 600, INK2, FM))
    c.add(arrow((738, y + 50), (794, y + 50), "flow", bend="straight"))
    bg, fg = KC[kd]
    c.add(f'<rect x="800" y="{y}" width="352" height="100" rx="14" fill="{bg}" stroke="{fg}" stroke-width="2"/>')
    c.add(wrap(820, y + (44 if len(res) > 34 else 57), res, 320, 18, 600, fg)[0])
c.add(Note(48, 540, 1104, "R20K V3.0, R20A V5.0 y R20B V2.0 tienen salida; las versiones viejas no. Anotá hardware, firmware y decisión en la planilla (paso 4).", kind="info", size=16))
save(c, "26-paso3.svg")
