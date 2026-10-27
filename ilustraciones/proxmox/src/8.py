import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 8.svg: la noche del PBS
c = Canvas(K(), "La noche del PBS: prune, backup, verify y GC")
c.add(NOLIG)
X0, X1, Y = 80, 1120, 214
c.add(path(f"M{X0} {Y} H{X1}", LINE2, 4))
c.add(text(48, 140, "Horario de ejemplo, de la guía de Hake Hardware", 15, 500, INK3, FB))
ev = [("21:30", "Prune", "Borra el índice de los backups que la retención no guarda. Todavía no libera espacio.", BLUE),
      ("22:00", "Backup", "Proxmox VE manda los backups nuevos al datastore.", OK),
      ("01:00", "Verify", "Relee y compara checksums. Si un ransomware cifra backups, falla y avisa.", BLUE),
      ("dom 02:00", "Garbage collection", "Borra los trozos que ya nadie usa, con un día de gracia. Ahí se libera.", WARN)]
for i, (hh, name, d, col) in enumerate(ev):
    x = 48 + i * 280
    c.add(f'<circle cx="{x + 24}" cy="{Y}" r="12" fill="{col}"/>')
    c.add(text(x + 8, Y - 26, hh, 18, 700, col, FM))
    c.add(rect(x, Y + 30, 264, 200, WHITE, LINE2, rx=14))
    c.add(text(x + 20, Y + 66, name, 20, 700, INK, FB))
    svg, _ = wrap(x + 20, Y + 98, d, 226, 16, 400, INK2)
    c.add(svg)
c.add(Note(48, 462, 1104, "Retención generosa al principio: siempre se puede achicar, pero no se recrean backups del pasado. Y una copia fuera del sitio con un sync job (regla 3-2-1).", kind="info"))
c.add(rect(48, 548, 1104, 74, OK_BG, OK, rx=14))
c.add(Mark(88, 585, True))
c.add(text(120, 578, "Usuario con rol DatastoreBackup: puede crear backups, no borrarlos", 18, 700, OK, FB))
c.add(text(120, 604, "Si alguien toma el host Proxmox VE, no puede borrar las copias del PBS.", 16, 400, INK2, FB))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso3: usuario, token y permiso
c = Canvas(K(3), "Usuario, token y permiso: escribir sí, borrar no")
c.add(NOLIG)
c.add(Step(48, 124, 3))
chain = [("Usuario", "backup@pbs", "user create"), ("Token", "backup@pbs!pve", "user generate-token"), ("Permiso", "DatastoreBackup", "acl update")]
for i, (t, v, cmd) in enumerate(chain):
    x = 80 + i * 360
    c.add(rect(x, 140, 320, 130, DEEP if i == 2 else WHITE, DEEP if i == 2 else BLUE, rx=16))
    c.add(text(x + 20, 176, t, 17, 600, "#9FC3E3" if i == 2 else INK3, FB))
    c.add(text(x + 20, 212, v, 20, 700, WHITE if i == 2 else BLUE, FM))
    c.add(text(x + 20, 246, cmd, 15, 500, "#9FC3E3" if i == 2 else INK3, FM))
    if i < 2:
        c.add(path(f"M{x + 324} 205 H{x + 354}", BLUE, 4, arrow=True))
c.add(text(800, 300, "sobre /datastore/main", 15, 600, INK3, FM))
c.add(text(80, 300, "Los tres con proxmox-backup-manager, en el PBS", 15, 600, INK3, FB))
c.add(text(48, 352, "Lo que puede hacer Proxmox VE con ese token:", 18, 600, INK, FB))
for i, (s, ok) in enumerate([("crear backups nuevos", True), ("leerlos para restaurar", True), ("borrar backups", False), ("cambiar la retención", False)]):
    x, y = 72 + (i // 2) * 420, 400 + (i % 2) * 52
    c.add(check(x, y, s, ok, 18))
c.add(Note(48, 500, 540, "PBS muestra el secreto del token una sola vez. Guardalo en el gestor de contraseñas apenas lo generás.", title="El secreto", kind="warn"))
c.add(Note(612, 500, 540, "Hay guías que conectan con root@pam. Funciona, pero un host tomado podría borrar todo el datastore.", title="Por qué no root", kind="info"))
save(c, "8-paso3.svg")

# ---------------------------------------------------------------- 8-paso4: agregar el PBS en Proxmox VE
c = Canvas(K(4), "En Proxmox VE: Add → Proxmox Backup Server")
c.add(NOLIG)
c.add(Step(48, 124, 4))
w = Window(48, 124, 600, 340, "Add: Proxmox Backup Server", rows=[("ID", "pbs-main"), ("Server", "IP del PBS"), ("Username", "backup@pbs!pve"),
           ("Password", "secreto del token"), ("Datastore", "main"), ("Fingerprint", "AA:BB:… del dashboard")], hl=2,
           path="Datacenter → Storage → Add")
c.add(w)
for y, s_, kd in [(140, "Username lleva el token completo: usuario, ! y nombre del token.", "info"),
                  (256, "En Password va el secreto que PBS mostró una vez, no la clave del usuario.", "warn"),
                  (372, "El fingerprint se copia del dashboard del PBS (web en el puerto 8007).", "info")]:
    c.add(Note(684, y, 468, s_, kind=kd))
c.add(text(48, 520, "Después lanzá un backup de prueba y mirá en PBS, Content, que aparezca.", 17, 600, INK, FB))
save(c, "8-paso4.svg")
