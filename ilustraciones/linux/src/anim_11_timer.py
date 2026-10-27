"""Teoría lección 11: un timer con Persistent=true recupera la ejecución perdida; después, la prueba de restauración."""
from _alnx import *

a = new(20, "Persistent=true: el backup que no se pierde")
a.steps(["Lunes 02:30: el timer dispara backup-etc.service.",
         "Martes 02:30: el equipo está apagado por un corte.",
         "Martes 07:10 arranca: Persistent corre lo que faltó.",
         "Recién con la restauración a /tmp hay backup."], still=2)

X0, X1, Y = 80, 1120, 300
def hx(day, h):
    return X0 + (X1 - X0) * (day * 24 + h) / 48
a.add(line(a, f"M{X0} {Y}H{X1}", a.LINE, 8))
for d, lab in [(0, "lunes"), (1, "martes")]:
    x = hx(d, 0)
    a.add(line(a, f"M{x} {Y - 14}V{Y + 14}", a.GREY, 2))
    a.add(a.text(x + 8, Y + 44, lab + " 00:00", 15, a.GREY, a.MONO, 500))
# apagado martes 01:00 a 07:10
at(a, a.box(hx(1, 1), Y - 22, hx(1, 7.17) - hx(1, 1), 44, a.BADBG, a.BAD, rx=8, sw=2)
   + a.text((hx(1, 1) + hx(1, 7.17)) / 2, Y + 6, "apagado", 15, a.BAD, a.SANS, 700, "middle"), 26, 100, 1)
# disparo lunes
x = hx(0, 2.5)
at(a, line(a, f"M{x} {Y - 26}V{Y - 80}", a.OK, 3) + chip(a, x, Y - 118, "02:30 backup OK", "ok", anchor="middle"), 3, 100, 1)
# martes 02:30 perdido
x2 = hx(1, 2.5)
at(a, line(a, f"M{x2} {Y - 26}V{Y - 80}", a.BAD, 3, "6 5") + chip(a, x2, Y - 118, "02:30 sin correr", "bad", anchor="middle"), 30, 100, 1)
# recupera
x3 = hx(1, 7.17)
at(a, line(a, f"M{x3} {Y + 26}V{Y + 70}", a.OK, 3) + chip(a, x3, Y + 78, "07:10 Persistent: corre ahora", "ok", anchor="middle"), 54, 100, 1)
at(a, term(a, 240, 430, 720, ["$ journalctl -u backup-etc.service -n 2", ("mar 07:10 systemd[1]: Starting backup-etc.service - Backup de /etc...", T_OUT),
                              ("mar 07:11 systemd[1]: Finished backup-etc.service - Backup de /etc.", T_OK)], size=15, lh=26), 58, 100, 1)
# restauración
at(a, a.box(240, 560, 720, 46, a.OKBG, a.OK, rx=12, sw=2) + mono(a, 600, 590, "tar xzf ... -C /tmp etc/hostname  +  diff  ->  restaurado OK", 15, a.OK, 700, "middle"), 77, 100, 0)
# cursor
mv = a.move([(0, hx(0, 1), Y), (5, hx(0, 3), Y), (25, hx(0, 22), Y), (45, hx(1, 4), Y), (55, hx(1, 7.3), Y), (75, hx(1, 12), Y), (100, hx(1, 20), Y)])
a.add(a.group(dot(a, 0, 0, 12, a.BLUE), mv, a.show(0, 99), still=0))

caption(a, 640, [(0, 25, "El .timer dice cuándo; el .service, qué. El log queda en el journal.", None),
                 (25, 50, "Con cron, la ejecución de esa noche simplemente no pasa.", a.BAD),
                 (50, 75, "Persistent=true la recupera apenas el equipo arranca.", a.OK),
                 (75, 100, "Que corra no prueba nada: la prueba es restaurar un archivo y compararlo.", a.OK)], still=2)
write(a, "11-t1.svg", "Persistent=true: el backup que no se pierde",
      "Animación en cuatro tiempos sobre una línea de dos días, lunes y martes. 1: el lunes a las 02:30 el timer dispara el backup, marcado en verde. "
      "2: el martes un corte deja el equipo apagado de la 01:00 a las 07:10, y el backup de las 02:30 queda sin correr, en rojo. "
      "3: el equipo arranca a las 07:10 y, por Persistent=true, el backup corre en ese momento; el journal de backup-etc.service muestra Starting y Finished a las 07:10. "
      "4: aparece la prueba que importa, restaurar etc/hostname a /tmp con tar y compararlo con diff: restaurado OK.")
