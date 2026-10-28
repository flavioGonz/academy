"""Lección 44 · Theme del portero: ilustración principal y pasos 3 y 6.
Todo sale de card.md de la lección 44 y de research/notes/f.md (nota de themes por modelo, guías de pantalla
de R29, X915, S539 y E18, especificaciones de protector)."""
from _theme import *  # noqa
from _akv import code, panel, pill  # noqa

K = "Akuvox · Lección 44"

# ---------------------------------------------------------------- principal
c = Canvas(K, "Un theme por tipo de acceso")
c.add(door_screen(50, 128, 230, 320, "villa", title="Villa", sub="una casa"))
c.add(door_screen(300, 128, 230, 320, "building", hl=CYAN, title="Building", sub="edificio · de fábrica"))
c.add(door_screen(550, 128, 230, 320, "office", title="Office", sub="oficinas"))
c.add(panel(810, 128, 340, 214, "Dónde se elige", "info", title_size=18))
rutas = [("S539 · S538 · S535 · S532", "Setting > Key/Display > Theme"), ("X915 · X912 · R29", "Setting > Key/Display > Theme"),
         ("X916", "Intercom > Key/Display > Theme"), ("E18 · E16", "Device > LCD > Theme")]
for i, (m, p) in enumerate(rutas):
    y0 = 186 + i * 38
    c.add(text(830, y0, m, 15, 600, INK, FB))
    c.add(text(830, y0 + 18, p, 15, 500, BLUE, FM))
c.add(panel(810, 360, 340, 136, "Necesitan la nube", "warn", title_size=18))
c.add(wrap(830, 414, "Gate Mode y Parking Lot: portero en el área pública de una comunidad en SmartPlus. Office del S539: Smart Access Cloud.", 300, 15, 400, INK2)[0])
c.add(Note(60, 530, 1090, "La lista exacta depende del modelo y del firmware: la nota de themes de junio de 2026 da cuatro al R29 y su guía de septiembre suma Parking Lot. Manda lo que muestra la web de tu equipo.", title="Antes de prometer un theme, mirá la web del portero", kind="info"))
save(c, "44.svg")

# ---------------------------------------------------------------- paso 3
c = Canvas(K + " · Paso 3", "Building: elegí con qué pantalla arranca")
c.add(code(60, 118, 760, "Setting > Key/Display > Key In Homepage Of The Building Theme", 15))
opts = [("building", "Home Page", "íconos y rostro"), ("directory", "Tenants / Contacts", "directorio"), ("keypad", "PIN", "teclado")]
for i, (mode, opt, sub) in enumerate(opts):
    x0 = 80 + i * 290
    c.add(pill(x0 + 115, 206, opt, BLUE if i else CYAN, WHITE, 15))
    c.add(door_screen(x0, 220, 230, 330, mode, title=sub))
c.add(Note(960, 220, 200, "X915: Default Page. R29: Display Type, con Dial, Delivery o Temp Key además.", kind="info", size=15))
c.add(Note(960, 420, 200, "Directorio para edificios con visita; teclado para un acceso de personal.", kind="ok", size=15))
c.add(Step(60, 206, 3))
save(c, "44-paso3.svg")

# ---------------------------------------------------------------- paso 6
c = Canvas(K + " · Paso 6", "Protector del R29: reposo, imágenes y despertar")
c.add(door_screen(40, 130, 220, 290, "building", title="en uso"))
c.add(door_screen(380, 130, 220, 290, "saver", hl=CYAN, title="protector"))
c.add(door_screen(720, 130, 220, 290, "building", title="despierta"))
c.add(Arrow((268, 275), (372, 275), "Sleep 30 s"))
c.add(Arrow((608, 275), (712, 275), "IR Detection", label_dy=-30))
for i in range(5):
    c.add(f'<rect x="{400 + i * 42}" y="{472}" width="34" height="30" rx="6" fill="{SOFT if i else CYAN}" stroke="{BLUE}" stroke-width="1.5"/>')
    c.add(text(417 + i * 42, 493, str(i + 1), 15, 600, INK if i else WHITE, FM, anchor="middle"))
c.add(Label(400, 524, "hasta 5 imágenes · Play Time 0 a 120 s", 15, 500, INK3, FM))
c.add(code(60, 560, 640, "Device > LCD > Standby Interface Display", 15))
c.add(code(60, 610, 640, "Device > Import/Export > Upload Screensaver Picture", 15))
c.add(Note(965, 130, 200, "JPG hasta 2 MP, 800x1280 recomendado (R29).", kind="info", size=15))
c.add(Note(965, 290, 200, "X915: Device > LCD > Upload Screensaver, con video sin sonido.", kind="info", size=15))
save(c, "44-paso6.svg")
