import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 1.svg: un solo árbol
c = new(None, "Un solo árbol: dónde vive cada cosa")
c.add(rect(48, 300, 92, 64, DEEP, DEEP, rx=14))
c.add(mid(94, 343, "/", 34, 700, WHITE, FM))
c.add(mid(94, 392, "la raíz", 15, 500, INK3, FB))
rows = [
    ("/etc", "configuración del sistema", "ssh/sshd_config · netplan/ · fstab", "info"),
    ("/var", "lo que cambia con el uso", "log/journal · cache/apt · lib/docker", "info"),
    ("/home", "carpetas de los usuarios", "/home/tecnico", "info"),
    ("/root", "carpeta personal del administrador", "no es la raíz del sistema", "warn"),
    ("/srv", "datos que sirve el equipo", "/srv/obra · /srv/backup", "info"),
    ("/tmp", "temporales", "se vacía; en Ubuntu 26.04 vive en RAM", "info"),
]
y0 = 132
for i, (p, d, ex, k) in enumerate(rows):
    y = y0 + i * 78
    c.add(f'<path d="M140 332C176 332 170 {y + 31} 206 {y + 31}" fill="none" stroke="{LINE2}" stroke-width="2.5"/>')
    fg = WARN if k == "warn" else BLUE
    c.add(rect(206, y, 128, 62, WARN_BG if k == "warn" else SOFT, fg, rx=12))
    c.add(mid(270, y + 39, p, 20, 700, fg, FM))
    c.add(text(354, y + 26, d, 18, 600, WARN if k == "warn" else INK, FB))
    c.add(text(354, y + 50, ex, 15, 500, INK3, FM))
# columna derecha: leer sin tocar
c.add(panel(800, 132, 352, 318, "Leer sin tocar nada", "ok"))
cmds = [("pwd", "dónde estoy"), ("ls -la", "qué hay, con dueños"), ("less", "leer un archivo"),
        ("find", "buscar por nombre"), ("grep -rn", "buscar texto adentro"), ("|", "encadenar comandos")]
for i, (cm, d) in enumerate(cmds):
    y = 196 + i * 42
    c.add(tag(822, y, cm, "dark", 15, anchor="start"))
    c.add(text(960, y - 1, d, 16, 500, INK2, FB))
c.add(Note(800, 474, 352, "Todo es /algo: no hay disco C ni D. Un disco extra se monta en una carpeta, como /srv/datos.", kind="info"))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso1: leer una línea de ls -la
c = new(1, "Cómo se lee una línea de ls -la")
svg, h = term(48, 124, 1104, ["$ ls -la /etc | less"], "TERMINAL · USUARIO COMÚN", size=17, lh=30)
c.add(svg)
# línea grande
L = "drwxr-xr-x  4  root  root  4096  oct 12 09:30  ssh"
L2 = "-rw-r--r--  1  root  root   711  oct  3 18:02  fstab"
X0, Y1, Y2, CW = 70, 272, 316, 19.2
c.add(rect(48, 232, 1104, 104, WHITE, LINE2, rx=14))
c.add(text(X0, Y1, L.replace("  ", "  "), 32, 600, INK, FM))
c.add(text(X0, Y2, L2.replace("  ", "  "), 32, 600, INK2, FM))
cw = 32 * 0.6
def cx(col):
    return X0 + col * cw
# tipo
c.add(f'<rect x="{cx(0) - 4}" y="{Y1 - 30}" width="{cw + 5}" height="{Y2 - Y1 + 42}" rx="6" fill="none" stroke="{CYAN}" stroke-width="2.5"/>')
c.add(f'<rect x="{cx(1) + 3}" y="{Y1 - 30}" width="{cw * 9 + 3}" height="{Y2 - Y1 + 42}" rx="6" fill="none" stroke="{OK}" stroke-width="2.5"/>')
c.add(f'<rect x="{cx(15) - 3}" y="{Y1 - 30}" width="{cw * 10 + 6}" height="{Y2 - Y1 + 42}" rx="6" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
c.add(f'<rect x="{cx(47) - 4}" y="{Y1 - 30}" width="{cw * 5 + 8}" height="{Y2 - Y1 + 42}" rx="6" fill="none" stroke="{WARN}" stroke-width="2.5"/>')
# rótulos debajo
c.add(callout(cx(0.5), 338, 60, 392, "tipo: d directorio, - archivo", "cyan"))
c.add(callout(cx(5.5), 338, 330, 430, "permisos: dueño · grupo · resto", "ok"))
c.add(callout(cx(20), 338, 520, 392, "dueño y grupo", "info"))
c.add(callout(cx(49.5), 338, 1040, 392, "nombre", "warn"))
c.add(callout(cx(36), 338, 760, 430, "tamaño y fecha", "gray"))
# less
c.add(text(48, 500, "Dentro de less", 18, 600, INK, FB))
from_x = 48
for k, d in [("/", "buscar"), ("n", "repite la búsqueda"), ("q", "sale sin cambiar nada")]:
    c.add(rect(from_x, 516, 48, 44, WHITE, LINE2, rx=9))
    c.add(mid(from_x + 24, 545, k, 19, 700, INK, FM))
    c.add(text(from_x + 62, 545, d, 16, 500, INK2, FB))
    from_x += 62 + len(d) * 8.6 + 40
c.add(Note(48, 584, 1104, "El usuario común puede leer casi todo /etc: si algo dice Permission denied, es un archivo protegido, no un error tuyo.", kind="info"))
save(c, "1-paso1.svg")

# ---------------------------------------------------------------- 1-paso3: salida de grep -rn
c = new(3, "grep -rn: archivo, línea y texto encontrado")
svg, h = term(48, 124, 1104, ["$ grep -rn \"Port\" /etc/ssh 2>/dev/null",
                               ("/etc/ssh/sshd_config:14:#Port 22", "#FFFFFF"),
                               ("/etc/ssh/ssh_config:41:#   Port 22", "#FFFFFF")], "TERMINAL · EJEMPLO", size=20, lh=40)
c.add(svg)
cw = 20 * 0.6
X = 64
yb = 124 + h
# rótulos para la primera línea de salida
c.add(f'<rect x="{X - 2}" y="{124 + 32 + 4 + 40 * 1.6 - 26}" width="{cw * 20 + 4}" height="34" rx="6" fill="none" stroke="{CYAN}" stroke-width="2.5"/>')
c.add(f'<rect x="{X + cw * 21 - 2}" y="{124 + 32 + 4 + 40 * 1.6 - 26}" width="{cw * 2 + 4}" height="34" rx="6" fill="none" stroke="{OK}" stroke-width="2.5"/>')
c.add(f'<rect x="{X + cw * 24 - 2}" y="{124 + 32 + 4 + 40 * 1.6 - 26}" width="{cw * 8 + 4}" height="34" rx="6" fill="none" stroke="{T_WARN}" stroke-width="2.5"/>')
c.add(callout(X + cw * 10, yb + 2, 120, yb + 50, "archivo", "cyan"))
c.add(callout(X + cw * 22, yb + 2, 360, yb + 50, "número de línea", "ok"))
c.add(callout(X + cw * 28, yb + 2, 620, yb + 50, "la línea encontrada", "warn"))
y = yb + 96
c.add(box(48, y, 352, 178, "-r y -n", ["-r recorre la carpeta entera,", "con sus subcarpetas.", "-n agrega el número de línea", "para ir directo con less."]))
c.add(box(424, y, 352, 178, "# al principio", ["La línea está comentada:", "no cuenta. Vale el valor", "por defecto de SSH,", "que es el puerto 22."], kind="warn"))
c.add(box(800, y, 352, 178, "2>/dev/null", ["Descarta los mensajes de", "error, como Permission", "denied, y deja en pantalla", "solo lo encontrado."], kind="ok"))
save(c, "1-paso3.svg")
