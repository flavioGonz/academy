from _akv import *

# ---------- 2.svg: leer A.B.C.D
c = Canvas("Akuvox · Lección 2", "¿Qué dice el número de firmware?")
segs = [("216", BLUE), (".", INK3), ("30", CYAN), (".", INK3), ("10", WARN), (".", INK3), ("121", OK)]
size, k = 72, 72 * 0.6
total = sum(len(s) for s, _ in segs) * k
x0 = 600 - total / 2
c.add(f'<rect x="{x0 - 30:.0f}" y="150" width="{total + 60:.0f}" height="110" rx="20" fill="#03213C"/>')
cx, centers = x0, []
for s, col in segs:
    c.add(text(cx, 230, s, size, 600, col if col != INK3 else "#7FA6C9", FM))
    if s != ".":
        centers.append((cx + len(s) * k / 2, col))
    cx += len(s) * k
cards = [("A · modelo", "216 = E16 V2", "29 = R29 · 915 = X915", BLUE),
         ("B · OEM", "30 = logo Akuvox", "31 = sin logo", CYAN),
         ("C · rama", "10 o más", "rama con alta seguridad", WARN),
         ("D · versión", "mayor = más nueva", "mismo modelo, OEM y rama", OK)]
for i, ((ttl, big, small, col), (mx, _)) in enumerate(zip(cards, centers)):
    bx = 48 + i * 282
    c.add(f'<path d="M{mx:.0f} 266V300H{bx + 133}V340" fill="none" stroke="{col}" stroke-width="3"/>')
    c.add(f'<rect x="{bx}" y="340" width="266" height="130" rx="16" fill="{WHITE}" stroke="{col}" stroke-width="2.5"/>')
    c.add(text(bx + 20, 374, ttl.upper(), 14, 600, col, FM, ls=1.5))
    c.add(text(bx + 20, 410, big, 21, 600, INK, FD))
    c.add(text(bx + 20, 442, small, 15, 400, INK3, FM))
c.add(Note(48, 500, 1104, "Varios modelos tienen dos o tres versiones de hardware y cada una lleva su archivo de firmware. Antes de bajar nada: modelo, hardware y rama.", title="El número no alcanza solo", kind="warn"))
save(c, "2.svg")

# ---------- 2-paso1.svg: dónde se lee
c = Canvas("Akuvox · Lección 2 · Paso 1", "Anotá firmware y hardware antes de tocar nada")
c.add(Window(48, 140, 560, 250, "Web del portero", path="Status > Basic > Product Information",
             rows=[("Model", "E16"), ("Firmware Version", "216.30.10.121"), ("Hardware Version", "(anotala tal cual)")], hl=1))
c.add(Step(48, 140, 1))
# etiqueta trasera del R20A
c.add(f'<rect x="700" y="150" width="450" height="200" rx="14" fill="{WHITE}" stroke="{WARN}" stroke-width="2.5" stroke-dasharray="8 6"/>')
c.add(text(724, 186, "ETIQUETA TRASERA · R20A", 14, 600, WARN, FM, ls=1.5))
c.add(Table(724, 206, ["Etiqueta dice", "Hardware real"], [["V3.0", "hardware 2"], ["V5.0", "hardware 3"]], [200, 200], row_h=40, mono_cols=(0, 1)))
c.add(Note(48, 430, 560, "En la web el dato sale limpio. Copialo a la ficha: con eso elegís el archivo correcto y soporte no rebota el ticket.", kind="info"))
c.add(Note(700, 380, 450, "En el R20A la etiqueta engaña: si dudás, mandá lo que dice la web, no lo que dice el sticker.", title="La etiqueta no es la versión", kind="warn"))
save(c, "2-paso1.svg")

# ---------- 2-paso5.svg: orden seguro de la actualización
c = Canvas("Akuvox · Lección 2 · Paso 5", "Backup, archivo correcto, subir y no tocar")
steps = [(3, "Backup", "exportar la config", "info"), (4, "Archivo", ".rom Linux · .zip Android", "info"),
         (5, "Subir", "System > Basic > Upgrade", "warn"), (6, "Verificar", "versión nueva en la ficha", "ok")]
for i, (n, ttl, sub, kd) in enumerate(steps):
    x = 48 + i * 282
    bg, fg = KC[kd]
    c.add(f'<rect x="{x}" y="160" width="250" height="150" rx="16" fill="{bg}" stroke="{fg if kd != "info" else LINE2}" stroke-width="2"/>')
    c.add(Step(x + 36, 196, n, CYAN if kd == "info" else fg))
    c.add(text(x + 66, 203, ttl, 21, 600, INK, FD))
    svg, _ = wrap(x + 22, 250, sub, 216, 15, 500, INK2, FM)
    c.add(svg)
    if i < 3:
        c.add(Arrow((x + 254, 235), (x + 278, 235)))
c.add(Window(48, 350, 640, 200, "Web del portero · Upgrade", path="System > Basic > Select File > Upgrade",
             rows=[("Archivo", "216.30.10.xxx.rom"), ("Mientras sube", "no cierres ni refresques")], hl=1))
c.add(Note(720, 350, 432, "La guía de Akuvox pide no cerrar ni refrescar la ventana hasta que termine. En obra: fuera de horario, con backup hecho y alguien del lado de la puerta.", title="Mientras sube, manos quietas", kind="alert"))
save(c, "2-paso5.svg")
