import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 12.svg: Swan o IP estática, y el monitoreo aparte
c = Canvas(K(), "La app llega por Swan o por IP estática")
c.add(NOLIG)
ph = c.add(Phone(48, 270, "BlueEye", "celular del cliente", w=250))
sw = c.add(CloudBox(430, 140, "Swan", "servidor de Paradox", w=270))
rt = c.add(Generic(430, 400, "Router", "port forward", icon="globe", w=270))
md = c.add(Box(860, 270, 292, 84, "Módulo IP", "en la central", icon=ICON["server"]))
c.add(Arrow(ph.right(-20), sw.left(), kind="flow"))
c.add(Arrow(sw.right(), md.left(-20), kind="flow"))
c.add(Arrow(ph.right(20), rt.left(), kind="logical"))
c.add(Arrow(rt.right(), md.left(20), kind="logical"))
c.add(tag(565, 252, "con suscripción", "ok", 15))
c.add(tag(565, 510, "solo módulos legado", "warn", 15))
c.add(Note(860, 130, 292, "El módulo sale a internet y se conecta a Swan; el sitio tiene días de suscripción y fecha de renovación.", kind="info", size=15))
c.add(Note(860, 400, 292, "Sin Swan, directo al módulo. Con IP150 1.xx o 4.0.4 pide la clave de fábrica: no lo expongas así.", kind="warn", size=15))
c.add(rect(48, 572, 1104, 52, OK_BG, OK, rx=12))
c.add(text(72, 605, "El monitoreo va por su propio canal a la receptora: no depende de la app ni de la suscripción.", 17, 600, OK, FB))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso2: crear el sitio Swan
c = Canvas(K(2), "Crear el sitio Swan desde el menú instalador")
c.add(NOLIG)
x0 = 84
path = ["Menú", "Entorno instalador", "My Other Paradox Systems", "⋮", "Create Swan System"]
x = x0
for i, p in enumerate(path):
    w = len(p) * 9.4 + 30
    c.add(rect(x, 140, w, 46, SOFT if i < 4 else CYAN, CYAN, rx=10))
    c.add(mid(x + w / 2, 170, p, 16, 600, INK if i < 4 else WHITE, FM))
    x += w + 10
    if i < 4:
        c.add(text(x - 4, 170, "›", 20, 700, INK3, FB))
        x += 12
c.add(Step(48, 140, 2))
c.add(Window(48, 230, 520, 230, "Create Swan System", rows=[("Número de serie", "el de la central"), ("Nombre del sitio", "la obra"), ("Correo", "el del sitio")], hl=0))
c.add(panel(612, 230, 540, 230, "Antes de crear", "warn"))
c.add(bullet_list(636, 290, [("Módulo conectado a la central y a internet: sin eso, no se crea.", "warn"),
                             ("Cuenta de instalador de paradox.com aprobada por el distribuidor.", "info"),
                             ("Borrar el sitio de la app no lo borra del servidor Swan.", "info")], 496, 16)[0])
c.add(Note(48, 490, 1104, "Después entrás con el código de PC (paso 3) y anotás en la ficha los días de suscripción, la fecha de renovación y quién paga (pasos 4 y 6).", kind="info", size=16))
save(c, "12-paso2.svg")

# ---------------------------------------------------------------- 12-paso3: el código de PC en BlueEye
c = Canvas(K(3), "El código de PC en BlueEye: cada 0 se escribe A")
c.add(NOLIG)
c.add(Step(48, 150, 3))
def digits(x, y, ds, hl=()):
    for i, d in enumerate(ds):
        col = WARN if i in hl else BLUE
        c.add(rect(x + i * 70, y, 58, 76, WARN_BG if i in hl else SOFT, col, rx=10))
        c.add(mid(x + i * 70 + 29, y + 51, d, 32, 700, col, FM))
c.add(text(90, 168, "En BabyWare ([911])", 17, 600, INK3, FB))
digits(90, 186, "6089", hl=(1,))
c.add(Arrow((400, 224), (520, 224)))
c.add(text(560, 168, "En BlueEye (MG/SP)", 17, 600, INK3, FB))
digits(560, 186, "6A89", hl=(1,))
c.add(text(90, 320, "Es el mismo código de PC de BabyWare. En MG y SP, cada 0 se escribe A.", 18, 600, INK, FB))
c.add(Note(48, 370, 540, "Si el código no entra, revisá los ceros antes que nada: cada uno va como A.", title="Si no entra", kind="warn"))
c.add(Note(612, 370, 540, "Es la misma llave que protege BabyWare: si quedó de fábrica, también la app queda abierta.", title="Misma llave", kind="info"))
save(c, "12-paso3.svg")
