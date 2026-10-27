"""Teoría de Mapa AVENAR: en una red todos los nodos tienen la misma versión de firmware."""
from _anim_bi import *

caps = ["Tres paneles AVENAR en red corren 4.8.1.",
        "Se suma un FPA-5000: toda la red queda en el mismo 3.x.",
        "3.x quedó fuera de mantenimiento: con Ethernet, evaluación de riesgo.",
        "Controlador del FPA cambiado por uno AVENAR: la red vuelve a 4.x."]
a = new(24, "Firmware", "Una red, una sola versión de firmware", caps, still=3)

# red Ethernet
a.add(a.box(90, 386, 1030, 6, a.LINE, rx=3))
a.add(a.text(90, 418, "red de paneles (Ethernet)", 15, a.GREY, a.MONO))
X = [(90, "AVENAR 8000", "torre A"), (480, "AVENAR 8000", "torre B"), (870, "AVENAR 2000", "torre C")]
for x, t, s in X:
    a.add(a.box(x + 124, 340, 6, 50, a.LINE, rx=3))
    a.add(card(a, x, 220, 250, 120, t, s, dark=True))
# cuarto nodo (aparece en el tiempo 2)
vis(a, a.box(604, 392, 6, 58, a.LINE, rx=3), 1, 3)
vis(a, card(a, 480, 450, 250, 110, "FPA-5000", "torre D", stroke=a.AMB, sw=3), 1, 2)
vis(a, card(a, 480, 450, 250, 110, "AVENAR (ex FPA)", "torre D: solo cambió", stroke=a.OK, sw=3), 3)
vis(a, a.text(500, 590, "el controlador; el lazo LSN queda", 15, a.OK, a.SANS, 600), 3)
# versiones por tiempo
for x, _, _ in X:
    vis(a, a.pill(x + 236, 236, "4.8.1", a.OK, a.OKBG, anchor="end"), 0)
    vis(a, a.pill(x + 236, 236, "3.x", a.AMB, a.AMBBG, anchor="end"), 1, 2)
    vis(a, a.pill(x + 236, 236, "4.x", a.OK, a.OKBG, anchor="end"), 3)
vis(a, a.pill(716, 466, "3.x", a.AMB, a.AMBBG, anchor="end"), 1, 2)
vis(a, a.pill(716, 466, "4.x", a.OK, a.OKBG, anchor="end"), 3)
# aviso
vis(a, a.box(800, 450, 352, 110, a.BADBG, a.BAD, rx=14, sw=2), 2)
vis(a, a.text(820, 488, "Evaluación de riesgo", 19, a.BAD, a.SANS, 600), 2)
vis(a, a.text(820, 516, "3.x sin mantenimiento desde 2026", 15, a.TXT), 2)
vis(a, a.text(820, 540, "y el panel conectado a Ethernet", 15, a.TXT), 2)
vis(a, a.text(90, 500, "Un FPA en la red:", 17, a.AMB, a.SANS, 600), 1, 2)
vis(a, a.text(90, 526, "todos con la misma 3.x", 17, a.AMB, a.SANS, 600), 1, 2)
a.add(a.text(48, 640, "Paneles conectados: siempre la misma versión. Solo AVENAR: conviene la última 4.x.", 17, a.TXT))
write(a, "1-t1.svg", "Una red, una sola versión", [12, 37, 62, 90])
