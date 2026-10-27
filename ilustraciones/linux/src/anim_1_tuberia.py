"""Teoría lección 1: la tubería ps aux | grep "[s]shd" y por qué grep no se encuentra a sí mismo."""
from _alnx import *

a = new(20, "La tubería: la salida de uno entra al otro")
a.steps(["ps aux escribe la lista de procesos en su salida.",
         "La tubería | lleva esa salida a la entrada de grep.",
         "grep deja pasar solo las líneas que dicen sshd.",
         "La línea del propio grep dice [s]shd: no coincide."], still=3)

rows = [("1", "/sbin/init", 0), ("418", "/lib/systemd/systemd-journald", 0), ("612", "sshd: /usr/sbin/sshd -D", 1),
        ("1450", "sshd: tecnico [priv]", 1), ("1460", "-bash", 0), ("1502", "grep [s]shd", 2)]
# caja izquierda: ps aux
a.add(card(a, 48, 186, 470, 372))
a.add(mono(a, 70, 222, "$ ps aux", 18, a.INK, 700))
a.add(a.text(70, 250, "PID    COMANDO (columnas recortadas)", 14, a.GREY, a.MONO, 500))
Y0, LH = 290, 44
for i, (pid, cmd, kind) in enumerate(rows):
    y = Y0 + i * LH
    at(a, mono(a, 70, y, pid.ljust(6) + " " + cmd, 16, a.INK, 500), 1 + i * 3, 100, 1)
    if kind == 0:  # no coincide: se apaga
        at(a, a.box(60, y - 24, 446, 34, a.BG, None, rx=6, extra='fill-opacity="0.72"'), 52, 100, 1)
    elif kind == 1:  # coincide
        at(a, a.box(60, y - 24, 446, 34, "none", a.OK, rx=6, sw=2.5), 52, 100, 1)
    else:  # la del grep
        at(a, a.box(60, y - 24, 446, 34, a.BG, None, rx=6, extra='fill-opacity="0.72"'), 52, 100, 1)
        at(a, a.box(60, y - 24, 446, 34, "none", a.AMB, rx=6, sw=3), 76, 100, 1)

# tubería
at(a, a.box(538, 330, 116, 84, a.SLATE, a.LINE, rx=14), 0, 100, 1)
a.add(mono(a, 596, 386, "|", 44, a.BLUE, 700, "middle"))
a.add(a.text(596, 446, "tubería", 16, a.TXT, a.SANS, 600, "middle"))
at(a, a.box(538, 330, 116, 84, "none", a.CYAN, rx=14, sw=4), 25, 50, 0)
for k in range(6):
    t0 = 26 + k * 3.6
    mv = a.move([(0, 520, 372), (t0, 520, 372), (t0 + 6, 676, 372), (100, 676, 372)])
    op = a.keyframes([(0, 0), (t0, 0), (t0 + 0.4, 1), (t0 + 5.6, 1), (t0 + 6, 0), (100, 0)])
    a.add(a.group(dot(a, 0, 0, 9, a.CYAN), mv, op, still=0))

# caja derecha: grep
a.add(card(a, 676, 186, 476, 372))
a.add(mono(a, 698, 222, '$ grep "[s]shd"', 18, a.INK, 700))
a.add(a.text(698, 250, "lo que sale por pantalla", 14, a.GREY, a.MONO, 500))
at(a, mono(a, 698, 290, "612    sshd: /usr/sbin/sshd -D", 16, a.OK, 600), 54, 100, 1)
at(a, mono(a, 698, 334, "1450   sshd: tecnico [priv]", 16, a.OK, 600), 57, 100, 1)
expl = (a.box(698, 372, 432, 160, a.AMBBG, None, rx=12)
        + a.text(718, 404, "Patrón [s]shd = una s y después shd.", 16, a.AMB, a.SANS, 700)
        + a.text(718, 434, "Encuentra sshd en los procesos de SSH.", 16, a.INK, a.SANS, 500)
        + a.text(718, 464, "El texto grep [s]shd no tiene sshd", 16, a.INK, a.SANS, 500)
        + a.text(718, 490, "seguido: el propio grep queda afuera.", 16, a.INK, a.SANS, 500))
at(a, expl, 77, 100, 1)

caption(a, 612, [(0, 25, "Cada programa tiene una salida: normalmente la pantalla.", None),
                 (25, 50, "Con | esa salida no va a la pantalla: entra a grep.", None),
                 (50, 75, "grep filtra línea por línea y no modifica nada del sistema.", a.OK),
                 (75, 100, "Sin los corchetes, la línea del grep aparecería siempre en el resultado.", a.AMB)], still=3)
write(a, "1-t1.svg", "La tubería: la salida de uno entra al otro",
      "Animación en cuatro tiempos. 1: a la izquierda, ps aux lista seis procesos de ejemplo: init, journald, dos de sshd, una bash y el propio grep [s]shd. "
      "2: puntos de colores viajan por la tubería, del cuadro de ps al de grep. 3: las líneas que no dicen sshd se apagan, las dos de sshd quedan en verde y aparecen a la derecha como resultado. "
      "4: la línea del propio grep se marca en ámbar y una nota explica que el patrón [s]shd busca una s seguida de shd, y que el texto grep [s]shd no lo contiene, por eso no aparece. "
      "El cuadro fijo muestra el resultado final con la explicación.")
