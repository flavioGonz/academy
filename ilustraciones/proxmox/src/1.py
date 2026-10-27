import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 1.svg: tres repositorios, uno habilitado
c = Canvas(K(), "Un host, un repositorio de Proxmox elegido a conciencia")
c.add(NOLIG)
cols = [
    ("pve-enterprise", "ok", "Con suscripción", ["Producción y soporte", "Paquetes más validados", "Viene habilitado de fábrica"],
     ("Sin suscripción: error 401", "alert")),
    ("pve-no-subscription", "warn", "Gratis, sin clave", ["Pruebas y uso no productivo", "Paquetes menos validados", "Producción: decide el cliente"],
     ("Con backups probados", "warn")),
    ("pve-test", "gray", "Lo que viene", ["Para desarrolladores", "Funciones nuevas sin pulir", "Nunca en un cliente"],
     ("Solo en el banco", "gray")),
]
for i, (name, kd, sub, items, (tg, tk)) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 122, 352, 290, None, "info"))
    c.add(text(x + 22, 162, name, 21, 700, {"ok": OK, "warn": WARN, "gray": INK3}[kd], FM))
    c.add(text(x + 22, 190, sub, 17, 600, INK, FB))
    c.add(hline(x + 18, x + 334, 208))
    for j, it in enumerate(items):
        c.add(f'<circle cx="{x + 28}" cy="{238 + j * 34 - 5}" r="4.5" fill="{CYAN}"/>')
        c.add(text(x + 44, 238 + j * 34, it, 17, 400, INK2, FB))
    c.add(tag(x + 22, 384, tg, tk, 15, mono=False, anchor="start"))
sv, h = codebox(48, 436, 640, ["Types: deb", "URIs: http://download.proxmox.com/debian/pve", "Suites: trixie",
                               ("Components: pve-no-subscription", "#7FE0B0")], 15, 26,
                title="/ETC/APT/SOURCES.LIST.D/PROXMOX.SOURCES")
c.add(sv)
c.add(Note(712, 436, 440, "Además de uno de Proxmox, el host siempre necesita los repositorios base de Debian. Desde Debian 13 van en formato deb822, archivos .sources.", title="Lo que no se toca", kind="info"))
c.add(text(712, 598, "Y para actualizar, siempre:", 17, 600, INK, FB))
c.add(code(712, 612, 300, "apt full-upgrade", 16))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso3: deshabilitar enterprise y agregar no-subscription
c = Canvas(K(3), "Sin suscripción: apagá enterprise y sumá no-subscription")
c.add(NOLIG)
w = Window(48, 124, 700, 300, "pve1 · Updates · Repositories", rows=[], path="Node → Updates → Repositories")
c.add(w)
hdr_y = 214
c.add(text(68, hdr_y, "ARCHIVO", 13, 600, INK3, FM, ls=1.2))
c.add(text(330, hdr_y, "COMPONENTE", 13, 600, INK3, FM, ls=1.2))
c.add(text(600, hdr_y, "ESTADO", 13, 600, INK3, FM, ls=1.2))
rows = [("pve-enterprise.sources", "pve-enterprise", "Disabled", ALERT, False),
        ("proxmox.sources", "pve-no-subscription", "Enabled", OK, True),
        ("debian.sources", "main", "Enabled", OK, False)]
for i, (f, comp, st, col, hl) in enumerate(rows):
    y = 236 + i * 48
    if hl:
        c.add(rect(58, y - 6, 680, 42, SOFT, CYAN, rx=8))
    c.add(text(68, y + 21, f, 15, 500, INK, FM))
    c.add(text(330, y + 21, comp, 15, 500, INK2, FM))
    c.add(tag(600, y + 21, st, "ok" if col == OK else "alert", 15, anchor="start"))
c.add(badge(778, 262, "a", CYAN))
c.add(text(806, 268, "Seleccioná pve-enterprise", 18, 600, INK, FB))
c.add(text(806, 294, "y tocá Disable", 17, 400, INK2, FB))
c.add(badge(778, 330, "b", CYAN))
c.add(text(806, 336, "Add → No-Subscription", 18, 600, INK, FM))
c.add(text(806, 362, "queda en proxmox.sources", 17, 400, INK2, FB))
c.add(Step(48, 124, 3))
sv, h = codebox(48, 452, 560, ["# pve-enterprise.sources", "Components: pve-enterprise", ("Enabled: no", "#FFB4A6")], 15, 26, title="ASÍ QUEDA DESHABILITADO")
c.add(sv)
c.add(Note(640, 452, 512, "Sin clave de suscripción, enterprise responde 401 Unauthorized en cada apt update. Deshabilitarlo saca el error; no-subscription trae los paquetes.", title="Por qué los dos pasos", kind="warn"))
save(c, "1-paso3.svg")
