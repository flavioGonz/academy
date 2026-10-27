"""Teoría de Servidor a medida: un puerto, un proceso; el conflicto y cómo se resuelve."""
from _anim_hc import *

caps = ["Otro programa del servidor ya escucha en el puerto 80.",
        "El SYS arranca, pide el 80 y no lo consigue: queda en rojo.",
        "netstat da el PID 4321 y tasklist dice qué programa es.",
        "El SYS pasa al 81: queda en verde y se entra con :81."]
a = new(24, "Puertos", "Un puerto, un proceso: quién llegó primero", caps, still=3)

a.add(a.box(48, 186, 560, 330, a.WHITE, a.LINE, rx=18))
a.add(a.text(72, 222, "Servidor SYS · 192.168.88.10", 18, a.INK, a.SANS, 600))
for x, p in ((80, "80"), (340, "81")):
    a.add(a.box(x, 250, 236, 96, a.SLATE, a.LINE, rx=14, extra='stroke-dasharray="6 5"'))
    a.add(a.text(x + 16, 274, f"puerto {p}", 15, a.GREY, a.MONO, 600))
# ocupante del 80, desde el tiempo 1
vis(a, a.pill(198, 302, "otro-programa.exe", a.WHITE, a.AMB, anchor="middle"), 0, 3)
s0, s1 = ph(a, 0)
# SYS: espera abajo
vis(a, a.text(80, 430, "servicio del SYS", 15, a.GREY, a.MONO), 0, 2)
for k in (0, 2):
    vis(a, a.pill(198, 452, "SYS", a.WHITE, a.BLUE, anchor="middle"), k)
s0, s1 = ph(a, 1)
token(a, "SYS", [(s0 + 2, 198, 466), (s0 + 9, 198, 372), (s0 + 12, 198, 372), (s0 + 18, 198, 466)], bg=a.BLUE)
vis(a, a.text(330, 400, "ocupado", 16, a.BAD, a.SANS, 600), 1)
# tiempo 4: SYS en el 81
s0, s1 = ph(a, 3)
token(a, "SYS", [(s0 + 1, 198, 466), (s0 + 8, 458, 316)], bg=a.BLUE)
vis(a, a.pill(458, 302, "SYS", a.WHITE, a.BLUE, anchor="middle"), 3, still=1)

# Service Manager
a.add(a.box(650, 186, 502, 150, a.WHITE, a.LINE, rx=14))
a.add(a.box(650, 186, 502, 40, a.SLATE, rx=14))
a.add(a.text(670, 213, "Service Manager", 16, a.TXT, a.SANS, 600))
a.add(a.text(670, 280, "SYS", 18, a.INK, a.SANS, 600))
vis(a, a.pill(1130, 260, "esperando", a.GREY, a.SLATE, anchor="end"), 0)
vis(a, a.pill(1130, 260, "Exceptional · 80", a.BAD, a.BADBG, anchor="end"), 1, 2)
vis(a, a.pill(1130, 260, "Running · 81", a.OK, a.OKBG, anchor="end"), 3)

# terminal
a.add(a.box(650, 356, 502, 160, "#03213C", rx=14))
L = [("> netstat -ano | findstr :80", "#D9E9F8"), ("TCP 0.0.0.0:80 … LISTENING 4321", "#FFD28A"),
     ("> tasklist | findstr 4321", "#D9E9F8"), ("otro-programa.exe   4321", "#FFD28A")]
for i, (s, col) in enumerate(L):
    vis(a, a.text(670, 392 + i * 32, s, 15, col, a.MONO), 2, 3)

a.add(a.text(48, 572, "Un puerto lo escucha un solo proceso a la vez. Se cierra el otro programa, con permiso", 17, a.TXT))
a.add(a.text(48, 600, "del cliente, o se mueve el puerto del servicio y se entra con él en la URL.", 17, a.TXT))
vis(a, a.pill(48, 620, "http://192.168.88.10:81", a.OK, a.OKBG), 3)
write(a, "2-t1.svg", "Un puerto, un proceso", [12, 33, 60, 90])
