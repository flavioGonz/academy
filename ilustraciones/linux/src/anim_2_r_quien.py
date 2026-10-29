#!/usr/bin/env python3
"""Lección 2 (Nunca 777), Resumen: la carpeta compartida de obra, antes y después. Con 777 cualquiera escribe en
/srv/obra, también un servicio como www-data, que puede borrar plano.txt (borrar necesita escritura en la carpeta).
Con root:tecnicos y 2770, tec1 y tec2 trabajan, lo nuevo hereda el grupo tecnicos por el setgid y el resto queda afuera.
Fuentes: teoría de la lección (dueño, grupo y resto; setgid; usermod -aG) y chmod(1)."""
from _anims_lnx_rl import *

a = nueva(26, "LINUX · PERMISOS · CÓMO SE VE", "777 o un grupo: quién puede tocar /srv/obra")
a.steps([
    "Con 777, tec1 crea plano.txt: anda, y parece resuelto.",
    "Pero el resto también escribe: www-data puede borrar plano.txt.",
    "La carpeta pasa a root:tecnicos con chmod 2770.",
    "tec1 y tec2 trabajan; www-data recibe Permission denied.",
], still=3)

ACT = [("tec1", "grupo tecnicos", 196), ("tec2", "grupo tecnicos", 306), ("www-data", "servicio web", 416)]
for n, g, y in ACT:
    a.add(dev(a, 48, y, 262, 84, n, g, "user", dark=(n == "www-data")))

# carpeta
FX, FY, FW, FH = 500, 180, 380, 330
a.add(a.box(FX, FY, FW, FH, a.WHITE, "#C2D4E6", rx=16))
a.add(mono(a, FX + 20, FY + 36, "/srv/obra", 19, a.INK, 700))
en(a, mono(a, FX + 20, FY + 68, "drwxrwxrwx root root", 16, a.BAD, 700) + a.pill(FX + 20, FY + 82, "777: todos rwx", a.BAD, a.BADBG, 14, 28), 0, 52)
en(a, mono(a, FX + 20, FY + 68, "drwxrws--- root tecnicos", 16, a.OK, 700) + a.pill(FX + 20, FY + 82, "2770: grupo rwx + setgid, resto nada", a.OK, a.OKBG, 14, 28), 52, 100, still=1)
a.add(linea(FX + 20, FY + 130, FX + FW - 20, FY + 130, a.LINE, 2))

# archivos
def archivo(y, nombre, dueño, color):
    return (a.box(FX + 20, y, FW - 40, 46, a.SLATE, None, rx=10) + mono(a, FX + 38, y + 29, nombre, 16, a.INK, 700)
            + mono(a, FX + FW - 38, y + 29, dueño, 15, color, 600, "end"))


en(a, archivo(FY + 150, "plano.txt", "tec1 tec1", a.GREY), 11, 37)
en(a, a.box(FX + 20, FY + 150, FW - 40, 46, "none", a.BAD, rx=10, sw=3) + marca(a, FX + FW - 20, FY + 150, False, 14), 33, 37)
en(a, mono(a, FX + 38, FY + 179, "plano.txt: borrado por www-data", 15, a.BAD, 700), 37, 52)
en(a, archivo(FY + 150, "plano.txt", "tec1 tecnicos", a.OK), 81, 100, still=1)
en(a, archivo(FY + 208, "fotos.zip", "tec2 tecnicos", a.OK), 87, 100, still=1)
en(a, a.text(FX + 20, FY + 292, "el grupo sale de la carpeta (setgid)", 15, a.OK, a.SANS, 600), 83, 100, still=1)

# pedidos
def pedido(lbl, y, t0, t1, ok, back=False):
    yy = y + 42
    c = a.OK if ok else a.BAD
    viaje(a, lbl, [(330 + len(lbl) * 4.6, yy), (FX - len(lbl) * 4.6 - 18, yy)], t0, t1, bg=a.BLUE, size=14, hold=0.6)
    if back:
        viaje(a, "Permission denied", [(FX - 110, yy + 30), (410, yy + 30)], t1 + 1, t1 + 5, bg=a.BAD, size=14, hold=10)


pedido("touch plano.txt", 196, 4, 10, True)
pedido("rm plano.txt", 416, 27, 33, True)
a.add(a.text(FX + 20, FY + FH + 28, "chown root:tecnicos /srv/obra · chmod 2770 /srv/obra", 15, a.GREY, a.MONO, 500))
en(a, a.box(FX + 8, FY + FH + 6, 500, 34, "none", a.BLUE, rx=8, sw=2), 52, 75)
pedido("touch plano.txt", 196, 77, 81, True)
pedido("touch fotos.zip", 306, 82, 86, True)
pedido("rm plano.txt", 416, 88, 92, False, back=True)
fijo(a, place(pill_c(a, "Permission denied", "#FFFFFF", a.BAD, 14), 420, 488))

# panel derecho: qué categoría aplica
PX = 912
a.add(a.box(PX, 180, 240, 330, a.WHITE, a.LINE, rx=16) + a.text(PX + 20, 214, "Qué categoría aplica", 17, a.INK, a.HEAD, 600))
def panel(t0, t1, lines, still=0):
    s = ""
    for i, (txt, c) in enumerate(lines):
        s += a.text(PX + 20, 250 + i * 26, txt, 15, c, a.SANS, 600)
    en(a, s, t0, t1, still)


panel(0, 25, [("tec1 no es el dueño (root)", a.TXT), ("ni está en el grupo root:", a.TXT), ("cae en el resto.", a.TXT), ("resto: rwx → crea", a.OK)])
panel(25, 52, [("www-data tampoco es dueño", a.TXT), ("ni del grupo: resto.", a.TXT), ("resto: rwx → borra", a.BAD), ("", a.TXT), ("borrar un archivo pide", a.TXT), ("escritura en la carpeta.", a.TXT)])
panel(52, 75, [("dueño: root", a.TXT), ("grupo: tecnicos (rws)", a.OK), ("resto: ---", a.BAD), ("", a.TXT), ("los técnicos entran", a.TXT), ("por el grupo, no por 777.", a.TXT)])
panel(75, 100, [("tec1, tec2: grupo → rwx", a.OK), ("www-data: resto → ---", a.BAD), ("", a.TXT), ("sumar un técnico:", a.TXT), ("usermod -aG tecnicos", a.BLUE)], still=1)

narr(a, [
    (0, 25, "777 da todo a dueño, grupo y resto: el resto es cualquier usuario del equipo.", None),
    (25, 52, "Un servicio comprometido entra por el resto y se lleva lo que la carpeta permite.", a.BAD),
    (52, 75, "El acceso compartido se da con un grupo; el resto se queda sin nada.", None),
    (75, 100, "Lo nuevo nace con grupo tecnicos y el que no está en el grupo no entra.", a.OK),
], still_idx=3)

escribir(a, "2-r1", "777 o un grupo: quién puede tocar /srv/obra",
         "Animación en cuatro tiempos con tres usuarios a la izquierda, tec1 y tec2 del grupo tecnicos y www-data, el servicio web, y la carpeta /srv/obra en el medio. "
         "1: con drwxrwxrwx root root, 777, tec1 crea plano.txt y anda; el panel explica que tec1 no es el dueño ni está en el grupo root y entra por el resto, con rwx. "
         "2: www-data también cae en el resto con rwx y borra plano.txt, porque borrar un archivo pide escritura en la carpeta. "
         "3: la carpeta pasa a root:tecnicos con chmod 2770: grupo rwx con setgid y resto sin nada. "
         "4: tec1 crea plano.txt y tec2 crea fotos.zip, los dos con grupo tecnicos heredado de la carpeta; www-data intenta borrar y recibe Permission denied. Para sumar un técnico, usermod -aG tecnicos.",
         [8, 34, 62, 94])
