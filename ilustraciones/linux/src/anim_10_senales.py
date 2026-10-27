"""Teoría lección 10: SIGTERM (15) contra SIGKILL (9)."""
from _alnx import *

a = new(20, "kill pide, kill -9 arranca de raíz")
a.steps(["kill PID manda SIGTERM (15): un pedido de terminar.",
         "El programa lo atrapa: cierra el archivo y sale prolijo.",
         "kill -9 manda SIGKILL: el kernel lo saca sin avisarle.",
         "Lo que estaba a medio escribir queda a medio escribir."], still=1)

lanes = [(190, "kill 1502", "SIGTERM · 15", a.BLUE), (410, "kill -9 1502", "SIGKILL · 9", a.BAD)]
for y, cmd, sig, col in lanes:
    a.add(a.box(48, y, 1104, 190, a.WHITE, a.LINE, rx=16, sw=2))
    a.add(term(a, 72, y + 24, 250, [f"$ {cmd}"], size=17, lh=28))
    a.add(a.text(80, y + 120, sig, 17, col, a.MONO, 700))
    # proceso
    a.add(a.text(560, y + 40, "proceso 1502 · grabador", 16, a.GREY, a.MONO, 600, "middle"))
    a.add(a.text(920, y + 40, "archivo que escribe", 16, a.GREY, a.MONO, 600, "middle"))

def proc(y, fill, stroke, label, tc):
    return a.box(450, y + 58, 220, 92, fill, stroke, rx=14, sw=2.5) + a.text(560, y + 112, label, 19, tc, a.HEAD, 700, "middle")

def fil(y, pct, col, label, lc):
    w = 300
    return (a.box(770, y + 70, w, 40, a.SLATE, a.LINE, rx=8) + a.box(770, y + 70, w * pct, 40, col, None, rx=8)
            + a.text(770, y + 140, label, 16, lc, a.SANS, 600))

Y1, Y2 = 190, 410
# carril 1: SIGTERM
mv = a.move([(0, 330, Y1 + 104), (3, 330, Y1 + 104), (16, 440, Y1 + 104), (100, 440, Y1 + 104)])
a.add(a.group(pkt(a, "15", a.BLUE, 60), mv, a.show(2, 22), still=0))
at(a, proc(Y1, "#E5F0FB", a.BLUE, "corriendo", a.BLUE), 0, 30, 0)
at(a, proc(Y1, a.OKBG, a.OK, "cierra y guarda", a.OK), 30, 48, 1)
at(a, proc(Y1, a.SLATE, a.LINE, "terminó", a.GREY), 48, 100, 0)
at(a, fil(Y1, 0.62, a.CYAN, "video.mp4 · escribiendo", a.TXT), 0, 30, 0)
at(a, fil(Y1, 1, a.OK, "video.mp4 · cerrado completo", a.OK), 30, 100, 1)

# carril 2: SIGKILL
mv2 = a.move([(0, 330, Y2 + 104), (50, 330, Y2 + 104), (57, 440, Y2 + 104), (100, 440, Y2 + 104)])
a.add(a.group(pkt(a, "9", a.BAD, 60), mv2, a.show(51, 58), still=0))
at(a, proc(Y2, "#E5F0FB", a.BLUE, "corriendo", a.BLUE), 0, 58, 1)
at(a, a.box(450, Y2 + 58, 220, 92, a.BG, a.BAD, rx=14, sw=2.5, extra='stroke-dasharray="8 6"') + a.text(560, Y2 + 112, "eliminado", 19, a.BAD, a.HEAD, 700, "middle"), 58, 100, 0)
at(a, fil(Y2, 0.62, a.CYAN, "video.mp4 · escribiendo", a.TXT), 0, 75, 1)
at(a, fil(Y2, 0.62, a.BAD, "video.mp4 · cortado a la mitad", a.BAD), 75, 100, 0)

caption(a, 636, [(0, 25, "SIGTERM se puede atrapar: el programa decide cómo terminar.", None),
                 (25, 50, "Por eso kill sin número es lo primero que se prueba.", a.OK),
                 (50, 75, "SIGKILL no se puede atrapar ni ignorar: lo resuelve el kernel.", a.BAD),
                 (75, 100, "kill -9 va como último recurso; a un servicio, systemctl restart.", a.AMB)], still=1)
write(a, "10-t1.svg", "kill pide, kill -9 arranca de raíz",
      "Animación en cuatro tiempos con dos carriles, el mismo proceso grabador 1502 escribiendo video.mp4. Arriba, kill 1502: 1: viaja la señal 15, SIGTERM. "
      "2: el proceso la atrapa, pasa a cierra y guarda, y el archivo queda cerrado completo en verde. Abajo, kill -9 1502: 3: viaja la señal 9, SIGKILL, y el proceso aparece eliminado sin pasar por ningún cierre. "
      "4: el archivo queda en rojo, cortado a la mitad. El cuadro fijo muestra el tiempo 2: arriba el cierre prolijo, abajo el proceso todavía corriendo.")
