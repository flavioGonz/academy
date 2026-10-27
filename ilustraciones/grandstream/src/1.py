import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 1.svg: los tres modos de red
c = Canvas(K(), "Elegí el modo de red antes de configurar nada")
modos = [
    ("Switch", "por defecto", "gray", "WAN: subida a la red", "LAN: puente, para una PC", ["Sirve si la red ya tiene", "DHCP y router propios."], None),
    ("Route", "la central rutea", "ok", "WAN: subida a la red", "LAN: router con su DHCP", ["Habilita DHCP opción 66", "y Dynamic Defense."], "opción 66 · Dynamic Defense"),
    ("Dual", "dos salidas", "gray", "WAN (LAN2): subida 1", "LAN (LAN1): subida 2", ["Dos redes independientes;", "elegís Default Interface."], None),
]
for i, (nm, sub, kd, wan, lan, why, chip) in enumerate(modos):
    x = 48 + i * 376
    c.add(panel(x, 130, 352, 400, None, "ok" if kd == "ok" else "info"))
    c.add(text(x + 24, 172, nm, 26, 600, INK, FD))
    c.add(text(x + 24, 198, sub, 15, 500, INK3, FM))
    # equipo mini
    c.add(f'<rect x="{x + 24}" y="222" width="304" height="78" rx="12" fill="{DEEP}"/>')
    c.add(text(x + 40, 250, "UCM6300", 16, 600, WHITE, FD))
    for k, p in enumerate(["WAN", "LAN"]):
        px = x + 150 + k * 90
        c.add(f'<rect x="{px}" y="236" width="76" height="50" rx="8" fill="#0B3A66" stroke="#4E7396" stroke-width="2"/>')
        c.add(text(px + 38, 278, p, 14, 600, WHITE, FM, anchor="middle"))
    # qué hace cada puerto
    c.add(text(x + 24, 340, wan, 16, 500, INK, FM))
    c.add(text(x + 24, 368, lan, 16, 500, INK, FM))
    c.add(f'<path d="M{x + 24} 392H{x + 328}" stroke="{LINE}" stroke-width="1.5"/>')
    for k, s in enumerate(why):
        c.add(text(x + 24, 424 + k * 24, s, 17, 400, INK2, FB))
    if chip:
        c.add(Chip(x + 24, 504, chip, "ok", mono=False))
c.add(Note(48, 556, 1104, "Decidilo con la central vacía. Cambiar el modo en producción corta la web y los teléfonos: hacelo en ventana de mantenimiento y con el LCD o la consola a mano.", title="Antes que nada", kind="warn", size=16))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso1: conectar por WAN y leer la IP
c = Canvas(K(1), "Conectá la UCM por WAN y leé su IP")
u = c.add(UCMBox(60, 140, 520, "UCM6300", "botón Home: muestra la IP", hl={"WAN": CYAN}, lcd="192.168.88.20"))
r = c.add(Generic(60, 430, "Router de laboratorio", "DHCP 192.168.88.0/24", icon="server", w=330))
n = c.add(Laptop(430, 430, "Notebook", "192.168.88.10", w=250))
c.add(Cable(u.port("WAN"), r.top(-60), kind="data", label="cable al WAN", label_at=0.5, label_dy=0))
c.add(Cable(n.left(), r.right(), kind="data"))
c.add(Step(u.port("WAN")[0] + 56, u.port("WAN")[1] + 20, 1))
w = c.add(Window(740, 140, 412, 210, "Router · DHCP", rows=[("UCM6300", "192.168.88.20"), ("Notebook", "192.168.88.10")], hl=0, path="Leases asignados"))
c.add(text(740, 384, "Dos lugares para leer la IP:", 17, 600, INK, FB))
lst, _ = bullet_list(740, 418, ["En el LCD de la central, con el botón Home.", "En la lista de DHCP del router de laboratorio."], 412, size=16)
c.add(lst)
c.add(Note(740, 500, 412, "El puerto LAN queda libre: lo que hace depende del modo de red que elijas en el paso 3.", kind="info", size=16))
save(c, "1-paso1.svg")

# ---------------------------------------------------------------- 1-paso2: login con la etiqueta y contraseña nueva
c = Canvas(K(2), "Entrá con la contraseña de la etiqueta y cambiala")
c.add(Window(48, 132, 470, 250, "Navegador", path="https://192.168.88.20:8089", rows=[("Usuario", "admin"), ("Contraseña", "la de la etiqueta"), ("Puerto", "8089 · HTTPS")], hl=1))
# etiqueta trasera
c.add(f'<rect x="48" y="412" width="300" height="130" rx="10" fill="{WHITE}" stroke="{INK3}" stroke-width="1.5" stroke-dasharray="5 4"/>')
c.add(text(68, 444, "ETIQUETA TRASERA", 13, 600, INK3, FM, ls=1.5))
c.add(text(68, 476, "Password:", 15, 500, INK2, FM))
c.add(text(68, 504, "única de cada equipo", 15, 600, INK, FM))
c.add(text(68, 528, "(desde enero de 2017)", 14, 400, INK3, FM))
c.add(Mark(370, 476, ok=False))
c.add(text(398, 470, "admin / admin", 16, 600, ALERT, FM))
c.add(text(398, 494, "lo citan guías viejas", 15, 400, INK3, FB))
c.add(text(398, 516, "de proveedores", 15, 400, INK3, FB))
c.add(arrow((528, 256), (600, 256)))
c.add(Window(612, 132, 540, 250, "UCM · web", path="Maintenance > Login Settings > Change Password", rows=[("Nueva contraseña", "10 a 30 caracteres"), ("Debe tener", "Aa · 0-9 · especial"), ("Guardala en", "la ficha del cliente")], hl=0))
c.add(Step(612, 132, 2))
c.add(Note(612, 412, 540, "Dejar la clave de fábrica es de las causas más comunes de centrales comprometidas. La UCM6510 con firmware hasta 1.0.20.52 ni siquiera limitaba los intentos de login (CVE-2025-28172).", title="Por qué en el primer ingreso", kind="alert", size=16))
save(c, "1-paso2.svg")

# ---------------------------------------------------------------- 1-paso4: backup antes de actualizar
c = Canvas(K(4), "Backup a tu notebook antes de tocar el firmware")
flow = [("1", "Anotá la versión", "Maintenance > Upgrade", "botón Detect", "info"),
        ("2", "Bajá el backup", "Maintenance > Backup", "archivo .tar a la notebook", "ok"),
        ("3", "Recién ahí, upgrade", "Maintenance > Upgrade", "paso 5, con el .tar a salvo", "info")]
for i, (n_, a, b, d, kd) in enumerate(flow):
    x = 48 + i * 376
    c.add(panel(x, 140, 340, 170, None, kd))
    c.add(text(x + 24, 184, a, 21, 600, INK, FD))
    c.add(text(x + 24, 220, b, 15, 500, BLUE, FM))
    c.add(text(x + 24, 260, d, 16, 400, INK2, FB))
    c.add(text(x + 316, 184, ("primero", "después", "al final")[i], 14, 600, INK3, FM, anchor="end"))
    if i == 1:
        c.add(Step(x, 140, 4))
    if i < 2:
        c.add(arrow((x + 344, 225), (x + 372, 225)))
c.add(Laptop(424, 360, "Notebook del técnico", "backup-cliente.tar", hl=OK, w=340))
c.add(arrow((594, 314), (594, 356), kind="ok"))
c.add(Note(800, 340, 352, "Para restaurar, el archivo va en .tar o .tgz, pesa menos de 100 MB y su nombre no lleva caracteres especiales. Guardalo fuera de la central: si la central muere, el backup no puede morir con ella.", title="El punto de vuelta atrás", kind="ok", size=16))
c.add(Note(48, 360, 340, "Después conviene programar backups automáticos a USB, SD, SFTP, NAS o S3 (Maintenance > Backup).", kind="info", size=16))
save(c, "1-paso4.svg")
