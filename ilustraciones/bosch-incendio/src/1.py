import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 1.svg: la familia
c = Canvas(K(), "¿Qué central tenés adelante?")
c.add(text(48, 140, "GENERACIÓN AVENAR (VIGENTE)", 13, 600, INK3, FM, ls=1.5))
cards = [("AVENAR panel 2000", ["6 módulos, hasta 4 lazos", "viene como kit en gabinete"], 48),
         ("AVENAR panel 8000", ["46 módulos, hasta 32 lazos", "módulos en riel, ampliable"], 420),
         ("AVENAR keypad 8000", ["FPE-8000-FMR", "opera a distancia o hace de", "controlador redundante del 8000"], 792)]
for t, ls, x in cards:
    c.add(rect(x, 156, 356, 150, DEEP, DEEP, rx=16))
    c.add(text(x + 22, 194, t, 21, 600, WHITE, FD))
    for i, s in enumerate(ls):
        c.add(text(x + 22, 228 + i * 25, s, 16, 400, "#C9DDF0", FB))
c.add(text(48, 346, "GENERACIÓN ANTERIOR (FPA)", 13, 600, INK3, FM, ls=1.5))
for t, ls, x in [("FPA-5000", ["red de hasta 32 paneles y teclados", "modular, controladores MPC"], 48),
                 ("FPA-1200", ["1 panel y hasta 3 teclados remotos", "sin controlador redundante"], 420)]:
    c.add(rect(x, 362, 356, 120, WHITE, LINE2, rx=16))
    c.add(text(x + 22, 400, t, 21, 600, INK, FD))
    for i, s in enumerate(ls):
        c.add(text(x + 22, 432 + i * 25, s, 16, 400, INK2, FB))
c.add(rect(792, 362, 356, 120, SOFT, CYAN, rx=16))
c.add(text(814, 400, "Todos hablan LSN", 21, 600, BLUE, FD))
c.add(text(814, 432, "el lazo y los detectores", 16, 400, INK2))
c.add(text(814, 457, "son la misma tecnología", 16, 400, INK2))
c.add(Note(48, 510, 540, "Standard o premium, grabada en el controlador. Premium suma BMS, UGM, voz y, en el 2000, la red.", title="Licencia: no se cambia", kind="warn"))
c.add(Note(612, 510, 536, "4.x solo en redes 100 % AVENAR (vigente 4.8.1). Con un FPA en la red, todos en el mismo 3.x.", title="Firmware: depende de la red", kind="info"))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso1: leer la etiqueta
c = Canvas(K(1), "La etiqueta dice modelo y licencia")
c.add(rect(48, 130, 560, 150, WHITE, LINE2, rx=16))
c.add(text(72, 164, "ETIQUETA DEL CONTROLADOR (EJEMPLO)", 13, 600, INK3, FM, ls=1.5))
c.add(text(72, 232, "FPE-2000-", 46, 600, INK, FM))
c.add(text(72 + 9 * 27.6, 232, "PPC", 46, 700, OK, FM))
c.add(f'<path d="M80 250H316" stroke="{BLUE}" stroke-width="3"/>')
c.add(text(198, 274, "familia y tamaño", 15, 600, BLUE, FB, anchor="middle"))
c.add(f'<path d="M330 250H410" stroke="{OK}" stroke-width="3"/>')
c.add(text(370, 274, "licencia", 15, 600, OK, FB, anchor="middle"))
c.add(Table(640, 130, ["Código", "Qué es"], [
    ["FPE-2000-SPC", "AVENAR panel 2000, standard"],
    ["FPE-2000-PPC", "AVENAR panel 2000, premium"],
    ["FPE-8000-SPC", "AVENAR panel 8000, standard"],
    ["FPE-8000-PPC", "AVENAR panel 8000, premium"],
    ["FPE-8000-FMR", "AVENAR keypad 8000"],
], [190, 322], hl_row=1, row_h=42, mono_cols=(0,)))
c.add(tag(130, 340, "SPC = standard", "gray"))
c.add(tag(330, 340, "PPC = premium", "ok"))
c.add(Note(48, 384, 560, "La licencia viene grabada: según el manual, no se puede modificar, revocar ni transportar. Si la obra necesita BMS o red y el panel es standard, no se arregla con un código.", title="Lo que no tiene arreglo en obra", kind="warn"))
c.add(Note(640, 384, 512, "Premium: interfaces a BMS (BIS, OPC, FSI), panel jerárquico UGM-2040 y evacuación por voz. En el 2000, además, trabajar en red.", title="Qué agrega premium", kind="info"))
save(c, "1-paso1.svg")

# ---------------------------------------------------------------- 1-paso2: frente del controlador
c = Canvas(K(2), "Tocá el logo de la pantalla y anotá el firmware")
s, an = controlador(300, 140, w=520, h=360, screen=["Pantalla de inicio", "", "", "", ""])
c.add(s)
# logo genérico (sin marca) en la pantalla
c.add(rect(600, 176, 180, 54, SOFT, CYAN, rx=10, sw=2, dash="5 4"))
c.add(mid(690, 209, "logo (tocar)", 15, 600, BLUE))
c.add(rect(392, 260, 300, 70, WHITE, OK, rx=10, sw=2))
c.add(text(408, 288, "Versión de firmware", 15, 600, OK, FB))
c.add(text(408, 314, "4.8.1  (ejemplo)", 16, 600, INK, FM))
c.add(callout(690, 176, 880, 160, "Logo en pantalla: muestra la versión", BLUE))
c.add(callout(334, 250, 140, 230, "18 LED de estado", INK2, anchor="end"))
c.add(callout(*an["fixed"], 470, 560, "6 botones fijos", INK2, anchor="end"))
c.add(callout(*an["fkeys"], 760, 560, "3 teclas de función", INK2))
c.add(Note(870, 252, 290, "Rojo: alarma. Amarillo titilando: falla. Amarillo fijo: algo deshabilitado. Verde: normal.", title="Cómo leer los LED", kind="info"))
c.add(Note(48, 300, 230, "Se apaga con su botón antes de quitar la alimentación.", title="Apagado", kind="warn"))
c.add(text(48, 640, "Esquema genérico del controlador AVENAR: ubicación de las piezas no a escala.", 15, 400, INK3))
save(c, "1-paso2.svg")

# ---------------------------------------------------------------- 1-paso3: contar módulos del riel
c = Canvas(K(3), "Contá los módulos del riel y anotá cuáles son de lazo")
mods = [("FPE-8000-BCM", "baterías", "warn"), ("LSN 1500 A", "lazo", "info"), ("LSN 1500 A", "lazo", "info"),
        ("LSN 0300 A", "lazo", "info"), ("IOS 0020 A", "otro", "gray"), ("", "libre", None)]
c.add(rect(48, 150, 1104, 230, "#E9EFF5", LINE2, rx=14))
c.add(text(70, 178, "RIEL DEL PANEL (EJEMPLO)", 13, 600, INK3, FM, ls=1.5))
for i, (m, k, kd) in enumerate(mods):
    x = 70 + i * 180
    if kd is None:
        c.add(rect(x, 196, 160, 160, "none", LINE2, rx=10, dash="6 6"))
        c.add(mid(x + 80, 282, "libre", 16, 500, INK3))
        continue
    col = {"warn": WARN, "info": BLUE, "gray": INK3}[kd]
    c.add(rect(x, 196, 160, 160, WHITE, col, rx=10, sw=2.5))
    c.add(rect(x + 14, 212, 132, 10, col, col, rx=5, sw=0))
    c.add(mid(x + 80, 268, m, 16, 600, INK, FM))
    c.add(mid(x + 80, 296, k, 15, 500, col))
    if kd == "info":
        c.add(badge(x + 80, 334, str([1, 1, 2, 3][i]), BLUE, r=15, size=15))
c.add(codebox(48, 410, 680, ["Módulos: LSN 0300 A x 1  LSN 1500 A x 2  BCM x 1", "         otros: IOS 0020 A", "Cada módulo LSN: un lazo o hasta dos ramales"], title="FICHA")[0])
c.add(Note(760, 410, 392, "En obra nueva desde el 02/05/2026 el módulo de baterías es el FPE-8000-BCM, que no se mezcla con el BCM-0000-B en un mismo panel.", title="El de baterías también cuenta", kind="info"))
save(c, "1-paso3.svg")
