"""Teoría lección 3: el ciclo diario de unattended-upgrades y la marca de reinicio."""
from _alnx import *

a = new(20, "Un día de actualizaciones automáticas")
a.steps(["Un timer de systemd baja las listas, como apt update.",
         "Otro timer corre unattended-upgrades: solo seguridad.",
         "El kernel nuevo deja la marca /var/run/reboot-required.",
         "Automatic-Reboot decide: 04:30 o tu ventana acordada."], still=3)

# línea de 24 h
X0, X1, Y = 80, 1120, 300
a.add(line(a, f"M{X0} {Y}H{X1}", a.LINE, 6))
for h in range(0, 25, 3):
    x = X0 + (X1 - X0) * h / 24
    a.add(line(a, f"M{x} {Y - 10}V{Y + 10}", a.GREY, 2))
    a.add(mono(a, x, Y + 38, f"{h:02d}:00", 15, a.GREY, 500, "middle"))
def hx(h):
    return X0 + (X1 - X0) * h / 24
# cursor del día
mv = a.move([(0, hx(6), Y), (2, hx(6), Y), (22, hx(10), Y), (48, hx(15), Y), (70, hx(24), Y), (70.01, hx(0), Y), (85, hx(4.5), Y), (100, hx(4.5), Y)])
a.add(a.group(dot(a, 0, 0, 13, a.BLUE), mv, a.show(0, 99), still=0))
# eventos
ev = [(9, "apt-daily.timer", "baja las listas", 2, a.BLUE, "info"),
      (14, "apt-daily-upgrade.timer", "instala seguridad", 27, a.OK, "ok")]
for h, n, d, t0, col, k in ev:
    x = hx(h)
    at(a, line(a, f"M{x} {Y - 18}V{Y - 70}", col, 3) + chip(a, x, Y - 108, n, k, anchor="middle")
       + a.text(x, Y - 120, d, 15, col, a.SANS, 600, "middle"), t0, 100, 1)
# paquetes instalados
at(a, term(a, 300, 380, 600, [("Start-Date: ... · unattended-upgrades", T_COM), ("Upgrade: openssl, linux-image-...", "#FFFFFF")], "/var/log/apt/history.log", size=15, lh=26), 34, 100, 1)
# marca de reinicio
at(a, a.box(300, 500, 600, 52, a.AMBBG, a.AMB, rx=12, sw=2) + mono(a, 600, 533, "/var/run/reboot-required", 18, a.AMB, 700, "middle"), 52, 100, 1)
# reinicio
x = hx(4.5)
at(a, line(a, f"M{x} {Y - 18}V{Y - 70}", a.OK, 3) + chip(a, x, Y - 108, "04:30 reinicio", "ok", anchor="middle")
   + a.text(x, Y - 120, "Automatic-Reboot \"true\"", 15, a.OK, a.MONO, 600, "middle"), 80, 100, 1)
at(a, a.text(1100, 420, "con \"false\":", 16, a.AMB, a.SANS, 700, "end") + a.text(1100, 444, "espera tu ventana", 16, a.AMB, a.SANS, 600, "end"), 80, 100, 1)

caption(a, 620, [(0, 25, "Corre solo, una vez por día, con dos timers de systemd.", None),
                 (25, 50, "Lo que instaló queda en history.log y en el log de unattended-upgrades.", a.OK),
                 (50, 75, "Un kernel nuevo no se usa hasta reiniciar: por eso aparece la marca.", a.AMB),
                 (75, 100, "Reinicio de madrugada en equipos desatendidos; con gente de día, en ventana.", a.OK)], still=3)
write(a, "3-t1.svg", "Un día de actualizaciones automáticas",
      "Animación en cuatro tiempos sobre una línea de 24 horas, con un punto que recorre el día. 1: a media tarde, apt-daily.timer baja las listas de paquetes. "
      "2: más tarde, apt-daily-upgrade.timer corre unattended-upgrades e instala solo seguridad; aparece el registro en history.log con openssl y un kernel nuevo. "
      "3: aparece en ámbar la marca /var/run/reboot-required. 4: el punto llega a las 04:30 y, con Automatic-Reboot en true, el equipo reinicia; con false, espera la ventana acordada. Las horas de los timers son de ejemplo.")
