"""Lección 43 · Theme del monitor: ilustración principal y pasos 2 y 6.
Todo sale de card.md de la lección 43 y de research/notes/f.md (guías de pantalla de C319, C313, S567, IT88, S562 y X933;
fondo por AutoP; especificaciones de protector)."""
from _theme import *  # noqa
from _akv import code, panel, pill  # noqa

K = "Akuvox · Lección 43"

# ---------------------------------------------------------------- principal
c = Canvas(K, "Theme y áreas: dos capas de la misma pantalla")
c.add(mon_screen(60, 132, 360, 236, "default", hl_area=(3, WARN), title="Theme Default", sub="áreas con íconos"))
c.add(mon_screen(470, 132, 360, 236, "calllist", title="Theme Call List", sub="lista de contactos"))
cards = [
    ("1 · Theme", "Qué forma tiene el inicio: íconos o lista para llamar.", "info"),
    ("2 · Áreas", "Qué botón va en cada lugar: tipo, etiqueta e ícono.", "info"),
    ("3 · Aspecto", "Protector, fondo, logo de arranque e idioma de pantalla.", "info"),
]
for i, (t, b, k) in enumerate(cards):
    y0 = 132 + i * 92
    c.add(panel(880, y0, 270, 80, t, k, title_size=17))
    w_, _ = wrap(900, y0 + 52, b, 240, 15, 400, INK2)
    c.add(w_)
for yy, mod, path in [(440, "C319 · S567 · IT88 · X933 · S562", "Device > Display Setting > Theme  ->  Default | Call List"),
                      (490, "C313 (Linux)", "Device > Key/Display > Home Page Mode  ->  Classic | Call List Simple")]:
    c.add(code(60, yy, 1090, "", 15))
    c.add(text(76, yy + 25, mod, 15, 600, "#9FE3F7", FM))
    c.add(text(420, yy + 25, path, 15, 500, "#D9E9F8", FM))
c.add(Note(60, 556, 1090, "El ámbar marca el área con Arming (alarma). Ese botón no es parte del theme: se cambia el tipo del área en Device > Display Setting, y el theme queda como está.", title="El botón de alarma es un área, no un theme", kind="warn"))
save(c, "43.svg")

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "Cambiá el tipo del área: de Arming a Unlock")
rows_before = [["Área 1", "Intercom", "Llamar"], ["Área 2", "Message", "Mensajes"], ["Área 3", "DND", "DND"], ["Área 4", "Arming", "Alarma"]]
rows_after = [["Área 1", "Intercom", "Llamar"], ["Área 2", "Message", "Mensajes"], ["Área 3", "DND", "DND"], ["Área 4", "Unlock", "Portón"]]
c.add(Label(60, 140, "Device > Display Setting · Home Page Display", 17, 600, INK, FM))
c.add(Table(60, 160, ["Área", "Type", "Label"], rows_before, [110, 150, 170], hl_row=3, row_h=40, mono_cols=(1,)))
c.add(Table(640, 160, ["Área", "Type", "Label"], rows_after, [110, 150, 170], hl_row=3, row_h=40, mono_cols=(1,)))
c.add(Label(60, 386, "antes", 16, 600, WARN))
c.add(Label(640, 386, "después", 16, 600, OK))
c.add(Arrow((506, 260), (626, 260), "Type", kind="flow"))
c.add(mon_screen(60, 410, 360, 200, "default", hl_area=(3, WARN)))
c.add(mon_screen(610, 410, 360, 200, "default", areas=[("Llamar", "call"), ("Mensajes", "msg"), ("DND", "dnd"), ("Portón", "unlock")], hl_area=(3, OK)))
c.add(Note(990, 410, 170, "En S567 y X933, Value toma un Remote Relay HTTP (Botón del monitor).", kind="info", size=15))
c.add(Step(566, 300, 2))
save(c, "43-paso2.svg")

# ---------------------------------------------------------------- paso 6
c = Canvas(K + " · Paso 6", "Un fondo para todos: AutoP desde SmartPlus")
c.add(CloudBox(60, 160, "SmartPlus", "proyecto > AutoP", w=250))
c.add(Label(345, 150, "comandos AutoP para el equipo", 15, 600, INK3, FM))
c.add(code(340, 166, 500, "Config.Wallpaper.Url01 = URL del JPG", 15))
c.add(code(340, 214, 500, "Config.Settings.PICTURE.Wallpaper = 1", 15))
c.add(Arrow((310, 202), (334, 202)))
c.add(mon_screen(870, 130, 300, 200, "default", areas=[("Llamar", "call"), ("Mensajes", "msg"), ("DND", "dnd"), ("Portón", "unlock")], clock="10:24"))
c.add(Label(930, 368, "S562 · ejemplo de la guía", 15, 500, INK3, FM))
c.add(Arrow((846, 210), (864, 210)))
c.add(Server(60, 380, "Servidor de imágenes", "HTTPS · FTP · TFTP", w=300))
c.add(f'<path d="M360 422 H900 V340" fill="none" stroke="{BLUE}" stroke-width="4" marker-end="url(#a-blue)"/><circle cx="360" cy="422" r="5" fill="{BLUE}"/>')
c.add(pill(620, 460, "el monitor baja el JPG o PNG", BLUE, WHITE, 14))
c.add(Chip(930, 420, "cambia después del reinicio", "warn", mono=False))
c.add(Note(60, 500, 1090, "En las planillas AutoP oficiales, la pantalla de inicio (IdleStyle) vale 4 o 5 en el S567 y 0 o 1 en el S562 y el C313. Una línea copiada de otro modelo deja otra pantalla: revisá la planilla de tu modelo.", title="Ojo al copiar entre modelos", kind="warn"))
save(c, "43-paso6.svg")
