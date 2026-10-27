import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 4.svg: el orden antes de tocar el servidor
c = Canvas(K(), "Antes de tocar el servidor: backup afuera y licencia libre")
st = [("1", "Backup ahora", "Back Up Now"), ("2", "Copia afuera", "otra máquina, verificada"),
      ("3", "Desactivar licencia", "online u offline"), ("4", "Cambiar o migrar", "disco, servidor, VM"),
      ("5", "Reactivar y revisar", "licencia y servicios")]
for i, (n, t, d) in enumerate(st):
    x = 48 + i * 224
    c.add(rect(x, 132, 206, 140, DEEP if i == 3 else WHITE, DEEP if i == 3 else LINE2, rx=14))
    c.add(badge(x + 32, 166, n, CYAN))
    c.add(text(x + 20, 214, t, 18, 600, WHITE if i == 3 else INK))
    c.add(text(x + 20, 244, d, 15, 400, "#9FC3E3" if i == 3 else INK3, FB))
    if i < 4:
        c.add(Arrow((x + 208, 202), (x + 222, 202), bend="straight"))
c.add(panel(48, 304, 540, 236, "Si cambiás hardware sin desactivar", "alert"))
c.add(bullet_list(72, 380, [("En máquina física la licencia queda atada al hardware: se invalida.", "alert"),
                            ("El SYS alterna entre Starting y Stopped en Service Manager.", "alert"),
                            ("En el servidor nuevo, el código da 1108: ya está usado en otro SYS.", "alert")], 492, 16)[0])
c.add(panel(612, 304, 540, 236, "Si el backup quedó solo en el SYS", "alert"))
c.add(bullet_list(636, 380, [("El backup programado se guarda en el propio servidor SYS.", "alert"),
                             ("Si muere el disco, se lleva el sistema y sus backups.", "alert"),
                             ("Por eso se copia a otra máquina y se prueba que abra.", "ok")], 492, 16)[0])
c.add(text(48, 586, "Migrar la VM del SYS con vMotion o similar también rompe la verificación de licencia.", 17, 500, INK2))
c.add(text(48, 622, "Antes de tocar el servidor: backup afuera y licencia desactivada. Siempre.", 18, 600, BLUE, FD))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso2: backup programado con 5 copias
c = Canvas(K(2), "Backup semanal: cinco copias que rotan solas")
w = c.add(Window(48, 124, 520, 380, "Back Up and Restore System Data · Back Up", rows=[
    ("Type", "config · imágenes · eventos · pasadas"), ("How Often", "Weekly"), ("When", "domingo 03:00"),
    ("Max. Number of Backups", "5"), ("Botón", "Save and Back Up Now")], hl=3))
c.add(text(48, 532, "Ruta del manual V2.6.1: en V3.x el menú puede llamarse distinto.", 16, 400, WARN))
c.add(text(612, 150, "CADA DOMINGO A LAS 03:00", 14, 600, INK3, FM, ls=1.5))
weeks = ["sem 1", "sem 2", "sem 3", "sem 4", "sem 5"]
for i, s in enumerate(weeks):
    x = 612 + i * 106
    c.add(rect(x, 172, 94, 74, OK_BG, OK, rx=12))
    c.add(mid(x + 47, 216, s, 16, 600, OK, FM))
c.add(text(612, 290, "Sale la sexta: la más vieja se borra.", 17, 600, INK))
for i, s in enumerate(["sem 2", "sem 3", "sem 4", "sem 5", "sem 6"]):
    x = 612 + i * 106
    c.add(rect(x, 312, 94, 74, OK_BG if i < 4 else SOFT, OK if i < 4 else CYAN, rx=12, sw=2 if i < 4 else 3))
    c.add(mid(x + 47, 356, s, 16, 600, OK if i < 4 else BLUE, FM))
c.add(rect(612, 404, 94, 40, ALERT_BG, ALERT, rx=10, dash="5 4"))
c.add(mid(659, 430, "sem 1", 15, 600, ALERT, FM))
c.add(text(722, 430, "se borra", 16, 500, ALERT))
c.add(Note(612, 466, 540, "Las cinco copias viven en el servidor SYS. Sirven para volver atrás una semana, no para sobrevivir a un disco muerto.", kind="warn"))
save(c, "4-paso2.svg")

# ---------------------------------------------------------------- 4-paso3: copia fuera del SYS
c = Canvas(K(3), "Copiá los backups a otra máquina")
s = c.add(Generic(48, 170, "SYS", "D:\\HikCentral\\Backup", icon="server", w=330, dark=True))
d = c.add(Generic(822, 170, "Otra máquina", "\\\\192.168.88.20\\backups\\hcp", icon="server", w=330))
c.add(Arrow(s.right(), d.left(), label="robocopy por la red"))
c.add(code(48, 300, 1104, 'robocopy "D:\\HikCentral\\Backup" "\\\\192.168.88.20\\backups\\hcp" /E /R:2 /W:5', 16, h=50))
c.add(Table(48, 378, ["Opción", "Qué hace"], [["/E", "copia las subcarpetas, incluidas las vacías"], ["/R:2", "reintenta 2 veces si un archivo falla"], ["/W:5", "espera 5 segundos entre reintentos"]], [160, 944], row_h=40, mono_cols=(0,)))
c.add(text(48, 572, "La ruta de origen es de ejemplo: usá la que muestra la pestaña Back Up de tu servidor.", 16, 400, INK3))
c.add(text(48, 612, "Después, abrí la carpeta de destino y fijate que estén los archivos con fecha de hoy.", 17, 600, INK))
save(c, "4-paso3.svg")
