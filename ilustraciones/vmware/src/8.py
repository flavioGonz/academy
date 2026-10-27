import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 8.svg: permiso = quién + rol + dónde
c = Canvas(K(), "Un permiso son tres cosas: quién, qué rol y dónde")
c.add(NOLIG)
parts = [("Quién", "usuario o grupo", "tecnico.prueba", "user"),
         ("Qué rol", "conjunto de privilegios", "Soporte-Lectura", "key"),
         ("Dónde", "objeto del inventario", "carpeta o clúster", "server")]
for i, (t, s, v, ic) in enumerate(parts):
    x = 48 + i * 300
    c.add(panel(x, 128, 260, 170, None, "info"))
    c.add(icon(x + 22, 150, ic, BLUE, 1.3))
    c.add(text(x + 70, 176, t, 21, 600, INK, FD))
    c.add(text(x + 22, 218, s, 15, 400, INK3, FB))
    c.add(rect(x + 18, 236, 224, 42, SOFT, CYAN, rx=10, sw=1.5))
    c.add(text(x + 130, 263, v, 13.5 if len(v) > 22 else 15, 600, INK, FM, anchor="middle"))
    if i < 2:
        c.add(text(x + 280, 222, "+", 30, 700, INK3, FD, anchor="middle"))
c.add(arrow((948, 213), (996, 213), "flow"))
c.add(panel(1000, 128, 152, 170, "Permiso", "ok"))
sv, _ = wrap(1018, 190, "y con Propagate, también en los hijos", 120, 15, 400, INK2)
c.add(sv)
# vCenter y SSO
c.add(host(48, 330, 560, 170, "vCenter (VCSA)", "appliance · gestiona varios hosts"))
c.add(rect(72, 410, 250, 70, "#0B3A66", CYAN, rx=12))
c.add(text(92, 440, "Single Sign-On", 16, 600, WHITE, FB))
c.add(text(92, 464, "dominio vsphere.local", 14, 500, "#9FC3E3", FM))
c.add(rect(340, 410, 244, 70, "#0B3A66", "#4E7396", rx=12))
c.add(text(360, 440, "Clúster, vMotion,", 16, 600, WHITE, FB))
c.add(text(360, 464, "HA y DRS", 16, 600, WHITE, FB))
c.add(panel(640, 330, 512, 170, "administrator@vsphere.local", "alert", title_size=17))
sv, _ = wrap(660, 392, "La llave maestra: va al gestor de contraseñas de la empresa y no se usa para el día a día.", 470, 16, 400, INK2)
c.add(sv)
c.add(Note(48, 522, 540, "Cada técnico con su usuario: cada cambio queda a nombre de quien lo hizo.", kind="ok"))
c.add(Note(612, 522, 540, "En vSphere 8 el tamaño Tiny de la VCSA pide 14 GB de RAM.", kind="info"))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso2: clonar Read-only
c = Canvas(K(2), "Clonar Read-only y sumar un solo privilegio")
c.add(NOLIG)
c.add(Step(48, 140, 2))
c.add(text(80, 146, "Administration > Access Control > Roles", 17, 600, BLUE, FM))
c.add(panel(48, 176, 420, 250, "Read-only", "gray"))
sv, _ = wrap(68, 236, "Ver el inventario y su configuración, sin cambiar nada.", 380, 16, 400, INK2)
c.add(sv)
c.add(tag(68, 320, "rol de fábrica", "gray", anchor="start"))
c.add(arrow((470, 300), (560, 300), "flow", label="Clone", label_dy=-16))
c.add(panel(564, 176, 588, 250, "Soporte-Lectura", "ok"))
c.add(text(586, 236, "todo lo de Read-only", 16, 400, INK2, FB))
c.add(text(586, 274, "+ un privilegio:", 16, 600, OK, FB))
c.add(rect(586, 290, 544, 46, WHITE, OK, rx=10))
c.add(text(604, 320, "Virtual machine > Interaction > Console interaction", 14.5, 600, INK, FM))
c.add(text(586, 380, "puede abrir la consola de una VM", 15, 500, INK3, FB))
c.add(text(586, 404, "no puede apagar, borrar ni cambiar hardware", 15, 500, INK3, FB))
c.add(Note(48, 456, 540, "Se clona en vez de editar: los roles de fábrica quedan intactos y se sabe qué cambiaste.", title="Por qué clonar", kind="info"))
c.add(Note(612, 456, 540, "Cada privilegio que sumás es algo más que ese usuario puede romper: de a uno y con motivo.", kind="warn"))
save(c, "8-paso2.svg")

# ---------------------------------------------------------------- 8-paso3: Add Permission con propagación
c = Canvas(K(3), "Add Permission en la carpeta y Propagate to children")
c.add(NOLIG)
c.add(Step(48, 140, 3))
tree = [(0, "Datacenter", "server", None), (1, "Lab-Pruebas (carpeta)", "server", "set"), (2, "vm-prueba", "laptop", "hereda"),
        (2, "vm-prueba-2", "laptop", "hereda"), (1, "Produccion (carpeta)", "server", None), (2, "srv-video", "laptop", None)]
bottom = {}
for i, (lvl, name, ic, st) in enumerate(tree):
    y = 170 + i * 66
    x = 80 + lvl * 52
    if lvl:
        c.add(f'<path d="M{x - 30} {bottom[lvl - 1]}V{y + 25}H{x}" fill="none" stroke="{LINE2}" stroke-width="2"/>')
    bottom[lvl] = y + 50
    col = {"set": CYAN, "hereda": OK, None: LINE2}[st]
    bg = {"set": SOFT, "hereda": OK_BG, None: WHITE}[st]
    c.add(rect(x, y, 380 - lvl * 52, 50, bg, col, rx=10, sw=2 if st else 1.5))
    c.add(icon(x + 12, y + 12, ic, BLUE if st != "hereda" else OK, 1.05))
    c.add(text(x + 50, y + 31, name, 16, 600, INK, FB))
    if st == "set":
        c.add(tag(x + 400 - lvl * 52, y + 31, "permiso acá", "info", anchor="start"))
    elif st == "hereda":
        c.add(tag(x + 400 - lvl * 52, y + 31, "lo hereda", "ok", anchor="start"))
    elif name.startswith("srv"):
        c.add(tag(x + 400 - lvl * 52, y + 31, "no lo ve", "gray", anchor="start"))
c.add(Window(720, 160, 432, 176, "Add Permission", [("User", "tecnico.prueba"), ("Role", "Soporte-Lectura"), ("Propagate to children", "marcado")], hl=2))
c.add(Note(720, 366, 432, "Después cerrá sesión y entrá como tecnico.prueba@vsphere.local para ver qué ve y qué no (paso 4).", kind="info"))
save(c, "8-paso3.svg")
