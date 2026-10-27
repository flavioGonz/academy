import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 2.svg: permisos en números
c = new(None, "755, 644, 600: cómo se leen los permisos")
# calculadora
c.add(panel(48, 124, 470, 300, "Cada letra vale un número"))
for i, (l, v, d) in enumerate([("r", "4", "leer"), ("w", "2", "escribir"), ("x", "1", "ejecutar o entrar")]):
    y = 178 + i * 56
    c.add(rect(72, y, 52, 44, SOFT, CYAN, rx=10))
    c.add(mid(98, y + 30, l, 22, 700, BLUE, FM))
    c.add(text(140, y + 30, "=", 20, 600, INK3, FM))
    c.add(mid(178, y + 30, v, 22, 700, INK, FM))
    c.add(text(214, y + 29, d, 17, 500, INK2, FB))
c.add(hline(72, 494, 352))
for i, (a1, a2) in enumerate([("rwx = 4+2+1 = 7", "r-x = 4+1 = 5"), ("rw- = 4+2 = 6", "r-- = 4")]):
    c.add(text(72, 388 + i * 24, a1, 17, 600, INK, FM))
    c.add(text(300, 388 + i * 24, a2, 17, 600, INK, FM))
# tres categorías
c.add(panel(48, 446, 470, 160, "Tres cifras, tres categorías"))
for i, (n, lb, col) in enumerate([("7", "dueño (u)", BLUE), ("5", "grupo (g)", OK), ("5", "resto (o)", WARN)]):
    x = 80 + i * 146
    c.add(rect(x, 498, 110, 56, WHITE, col, rx=12))
    c.add(mid(x + 55, 536, n, 28, 700, col, FM))
    c.add(mid(x + 55, 584, lb, 15, 600, col, FB))
# tabla de valores típicos
rows = [("755", "rwxr-xr-x", "directorios y programas", "ok"), ("644", "rw-r--r--", "archivos de datos", "ok"),
        ("600", "rw-------", "secretos: llaves, claves", "ok"), ("2770", "rwxrws---", "carpeta compartida de un grupo", "ok"),
        ("777", "rwxrwxrwx", "cualquiera escribe: nunca", "alert")]
c.add(panel(546, 124, 606, 482, "Los que vas a ver siempre"))
for i, (n, p, d, k) in enumerate(rows):
    y = 176 + i * 82
    col = ALERT if k == "alert" else INK
    c.add(rect(570, y, 558, 66, ALERT_BG if k == "alert" else GROUND, ALERT if k == "alert" else LINE2, rx=12))
    c.add(text(590, y + 42, n, 24, 700, ALERT if k == "alert" else BLUE, FM))
    c.add(text(678, y + 42, p, 19, 600, col, FM))
    c.add(text(870, y + 41, d, 16, 500, ALERT if k == "alert" else INK2, FB))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso2: carpeta compartida con setgid
c = new(2, "Carpeta del grupo, con setgid: lo nuevo hereda el grupo")
svg, h = term(48, 124, 700, ["$ sudo chown root:tecnicos /srv/obra", "$ sudo chmod 2770 /srv/obra", "$ ls -ld /srv/obra",
                             ("drwxrws--- 2 root tecnicos 4096 ... /srv/obra", "#FFFFFF")], "TERMINAL", size=16, lh=28)
c.add(svg)
X0, Y = 64, 124 + 32 + 4 + 3.6 * 28
cw = 16 * 0.6
c.add(f'<rect x="{X0 + cw * 6 - 2}" y="{Y - 21}" width="{cw + 4}" height="28" rx="5" fill="none" stroke="{T_WARN}" stroke-width="2.5"/>')
c.add(callout(X0 + cw * 6.5, 124 + h, 140, 124 + h + 40, "s en el grupo: setgid activo", "warn"))
c.add(Note(776, 124, 376, "2770 = setgid (2) + dueño rwx (7) + grupo rwx (7) + resto nada (0).", title="Cómo se lee 2770", kind="info"))
# escena
y = 380
c.add(Person(48, y, "tec1", "grupo tecnicos", w=260))
c.add(Person(48, y + 120, "nobody", "fuera del grupo", w=260))
c.add(rect(470, y - 6, 300, 220, SOFT, CYAN, rx=16))
c.add(text(494, y + 28, "/srv/obra", 22, 700, BLUE, FM))
c.add(text(494, y + 54, "root : tecnicos", 15, 500, INK3, FM))
c.add(rect(494, y + 76, 252, 46, WHITE, OK, rx=10))
c.add(text(512, y + 105, "plano.txt", 17, 600, INK, FM))
c.add(text(632, y + 105, "tecnicos", 15, 700, OK, FM))
c.add(text(494, y + 160, "creado por tec1, del grupo", 15, 500, INK2, FB))
c.add(text(494, y + 182, "de la carpeta", 15, 500, INK2, FB))
c.add(arrow((308, y + 42), (470, y + 42), "ok", label="touch plano.txt"))
c.add(arrow((308, y + 162), (470, y + 162), "alert", label="ls"))
c.add(Mark(820, y + 42, True))
c.add(text(850, y + 49, "entra y escribe", 17, 600, OK, FB))
c.add(Mark(820, y + 162, False))
c.add(text(850, y + 169, "Permission denied", 17, 600, ALERT, FM))
save(c, "2-paso2.svg")

# ---------------------------------------------------------------- 2-paso4: recursivo sin volver ejecutable todo
c = new(4, "Permisos recursivos: directorios por un lado, archivos por otro")
def tree(x, y, items, title, kind):
    out = [panel(x, y, 540, 322, title, kind)]
    for i, (name, perm, bad) in enumerate(items):
        yy = y + 104 + i * 48
        ind = 24 if name.startswith("  ") else 0
        out.append(text(x + 28 + ind, yy, name.strip(), 18, 600, INK, FM))
        out.append(text(x + 512, yy, perm, 18, 700, ALERT if bad else OK, FM, anchor="end"))
    return "".join(out)
items_bad = [("obra/", "rwxr-xr-x", False), ("  planos/", "rwxr-xr-x", False), ("  plano.txt", "rwxr-xr-x", True),
             ("  fotos.zip", "rwxr-xr-x", True), ("  notas.txt", "rwxr-xr-x", True)]
items_ok = [("obra/", "rwxrws---", False), ("  planos/", "rwxrws---", False), ("  plano.txt", "rw-rw----", False),
            ("  fotos.zip", "rw-rw----", False), ("  notas.txt", "rw-rw----", False)]
c.add(tree(48, 124, items_bad, "chmod -R 755 obra", "alert"))
c.add(tree(612, 124, items_ok, "find por tipo", "ok"))
c.add(text(76, 182, "todo queda ejecutable", 15, 500, ALERT, FB))
c.add(text(640, 182, "cada tipo con lo suyo", 15, 500, OK, FB))
svg, h = term(612, 470, 540, ["$ sudo find /srv/obra -type d -exec chmod 2770 {} \\;",
                              "$ sudo find /srv/obra -type f -exec chmod 660 {} \\;"], None, size=14, lh=26)
c.add(svg)
c.add(Note(48, 470, 540, "Con -R, un solo número va a directorios y archivos por igual: los archivos de datos quedan ejecutables. find -type d y -type f los separa.", kind="warn"))
save(c, "2-paso4.svg")
