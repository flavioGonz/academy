"""Teoría lección 7: qué arranca y cuándo, y cómo el administrador de servicios levanta un servicio caído."""
from _awin import *

a = new(24, "Del encendido al servicio que vuelve solo")
a.steps(["Windows arranca: suben los servicios en Automático.",
         "Un rato después, los de Automático retrasado.",
         "La tarea AtStartup corre como SYSTEM, sin sesión.",
         "El servicio se cae: 3 minutos y se reinicia solo."], still=3)
X0, X1 = 260, 1140
lanes = [(200, "Automático", "red, base local…"), (290, "Retrasado", "servicio del VMS"), (380, "Tarea al inicio", "AtStartup · SYSTEM"), (470, "Sesión", "nadie entró")]
for y, t, s in lanes:
    a.add(a.text(48, y + 6, t, 18, a.INK, a.HEAD, 600) + a.text(48, y + 30, s, 15, a.GREY, a.MONO, 500))
    a.add(line(a, f"M{X0} {y + 10}H{X1}", a.LINE, 2))
a.add(line(a, f"M{X0} 180V520", a.GREY, 2, "4 6") + a.text(X0, 548, "encendido", 15, a.GREY, a.MONO, 600, "middle"))


def bar(y, x1, x2, s, color, label, still=1, e=100):
    at(a, a.box(x1, y - 6, x2 - x1, 32, color, None, rx=16) + a.text(x1 + 14, y + 16, label, 15, "#FFFFFF", a.MONO, 600), s, e, still)


bar(200, 270, 1140, 2, a.BLUE, "corriendo")
bar(290, 470, 1140, 27, a.OK, "servicio del VMS corriendo", e=75)
bar(380, 330, 520, 52, a.CYAN, "arranque.ps1")
at(a, a.text(530, 414, "→ C:\\Lab\\arranque.log", 15, a.BLUE, a.MONO, 600), 54, 100, 1)
a.add(a.text(X1, 504, "sin sesión iniciada", 15, a.GREY, a.SANS, 500, "end"))
# 4: caída y recuperación
bar(290, 470, 760, 75, a.OK, "servicio del VMS", still=1)
at(a, a.box(760, 284, 160, 32, a.BADBG, a.BAD, rx=16, sw=2) + a.text(840, 306, "caído · 3 min", 15, a.BAD, a.MONO, 600, "middle"), 77, 100, 1)
bar(290, 920, 1140, 82, a.OK, "reiniciado", still=1)
caption(a, 600, [(0, 25, "El administrador de servicios levanta primero los que están en Automático.", None),
                 (25, 50, "Retrasado deja tiempo a que estén la red y la base de datos antes del VMS.", a.OK),
                 (50, 75, "La tarea no espera a nadie: corre al encender, como SYSTEM y en su carpeta.", None),
                 (75, 100, "La recuperación reinicia el servicio a los 3 minutos; el contador vuelve a 0 en 24 h.", a.OK)], still=3)
write(a, "7-t1.svg", "Del encendido al servicio que vuelve solo",
      "Animación en cuatro tiempos sobre una línea de tiempo desde el encendido, con cuatro carriles: servicios en Automático, servicio en Automático retrasado, tarea al inicio y sesión de usuario. "
      "1: al arrancar suben los servicios en Automático. 2: un rato después arranca el servicio del VMS, en Automático retrasado, cuando ya están la red y la base. "
      "3: la tarea programada AtStartup corre arranque.ps1 como SYSTEM y escribe C:\\Lab\\arranque.log sin que nadie haya iniciado sesión. "
      "4: el servicio del VMS se cae, queda 3 minutos caído y la recuperación lo reinicia solo. El carril de sesión dice todo el tiempo que nadie entró.", pcts=(12, 37, 62, 90))
