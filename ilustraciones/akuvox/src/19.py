import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 19.svg: qué familia va en cada entrada
c = Canvas("Akuvox · Lección 19", "¿Qué familia de portero va en cada entrada?")
cols = [("Casa u oficina chica", "boton", "un botón: un destino", ["E13S · E12", "X910", "R20A · R25A"], "house"),
        ("Edificio con varios destinos", "teclado", "teclado o botones", ["R20K · R20K-L", "R20B + MD06/MD12", "R28"], "building"),
        ("Acceso con pantalla y rostro", "pantalla", "pantalla táctil, rostro", ["R29 · S535", "X912", "E18 · E16"], "building"),
        ("Acceso principal grande", "pantalla_grande", "Android grande", ["S539 · S538", "X916 · X915", ""], "tall")]
for i, (t, kind, crit, models, pic) in enumerate(cols):
    x = 48 + i * 280
    c.add(panel(x, 122, 262, 440, None, "info"))
    c.add(text(x + 131, 154, t, 17, 600, INK, FB, anchor="middle"))
    if pic == "house":
        c.add(house(x + 20, 190, 120, 100, BLUE))
    else:
        c.add(building(x + 20, 176 if pic == "tall" else 196, 110, 114 if pic == "tall" else 94, 4 if pic == "tall" else 3, BLUE))
    c.add(portero(x + 160, 172, kind, 0.46))
    c.add(pill(x + 131, 352, crit, BLUE, SOFT, 15, False))
    for k, m in enumerate(models):
        if m:
            c.add(text(x + 131, 402 + k * 34, m, 18, 600, INK, FM, anchor="middle"))
c.add(text(48 + 3 * 280 + 131, 470, "(edificio de categoría)", 15, 400, INK3, FB, anchor="middle"))
c.add(Note(48, 578, 640, "Orientación para arrancar la cotización: la decisión final sale de la obra y de la ficha de la versión.", kind="info", size=15))
c.add(Note(708, 578, 444, "Portón con cámara de patentes Hikvision: R29 o X912 (lección 18).", kind="ok", size=15))
save(c, "19.svg")

# ---------------------------------------------------------------- 19-paso2: la planilla y de dónde sale cada columna
c = Canvas("Akuvox · Lección 19 · Pasos 2 y 3", "Cada columna de la planilla tiene su fuente")
srcs = [(553, "tabla de alimentación"), (733, "tabla de relé"), (933, "menú de akuvox.com")]
for x, s in srcs:
    c.add(pill(x, 160, s, BLUE, WHITE, 15, False))
    c.add(arrow((x, 168), (x, 222), "flow", bend="straight"))
c.add(Table(48, 230, ["Modelo", "Tipo", "Serie", "Sistema", "PoE (tabla)", "Relé (tabla)", "En el menú hoy"],
            [["R29", "Portero", "R", "Android", "802.3at", "30 V 3 A", "sí"],
             ["E16C", "Portero", "E", "Linux", "802.3af", "30 V 2 A", "sí"],
             ["C315", "Monitor", "C", "(ver)", "(ver)", "30 V 2 A", "no"]],
            [110, 120, 80, 110, 170, 190, 210], hl_row=2, mono_cols=(4, 5), row_h=46))
c.add(Note(48, 440, 540, "Si un dato no aparece en la tabla, escribí \"sin dato\". Suponerlo es la forma más rápida de cotizar mal.", title="Paso 3", kind="warn", size=15))
c.add(Note(612, 440, 540, "\"No está en el menú\" no es \"sin soporte\": antes de decírselo al cliente, consultá al distribuidor.", title="C315: parque instalado", kind="info", size=15))
save(c, "19-paso2.svg")

# ---------------------------------------------------------------- 19-paso4: sufijos que cambian funciones
c = Canvas("Akuvox · Lección 19 · Paso 4", "El sufijo cambia funciones: marcá cada versión")
rows = [("R29S", "una cámara, sin Bluetooth", "gray"),
        ("R29C-L", "LTE · no acepta PoE", "warn"),
        ("R29C-T", "lector de huella", "cyan"),
        ("R20K-L", "LTE", "warn"),
        ("X915P · E16P", "venas de la palma", "cyan"),
        ("X915 HID iClass / Prox", "lector HID", "cyan")]
for i, (m, what, k) in enumerate(rows):
    col, row = i % 2, i // 2
    x, y = 48 + col * 564, 140 + row * 118
    c.add(panel(x, y, 540, 96, None, "info"))
    c.add(text(x + 24, y + 42, m, 21, 700, INK, FM))
    c.add(Chip(x + 24, y + 78, what, k, mono=False))
c.add(Note(48, 510, 1104, "Mismo modelo, distinta versión: cambian la fuente o las credenciales. En la planilla, cada versión con sufijo va en otro color.", kind="info", size=16))
save(c, "19-paso4.svg")
