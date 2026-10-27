"""Teoría lección 8: evento, PGM, relé y pulso de portón."""
from _apdx import *

a = new(20, "Del botón B al portón: evento, PGM, relé, pulso")
a.steps(["Llega el evento de activación: botón B de un control (08/99/99).",
         "La PGM1 se activa y energiza la bobina del relé.",
         "El contacto seco COM y NO se cierra: la placa del portón ve un pulsador.",
         "Pasan los 2 s de [281]: la PGM vuelve sola y el contacto se abre."], still=2)
a.add(card(a, 48, 220, 230, 110, "Control", "botón B"))
a.add(card(a, 340, 220, 230, 110, "PGM1", "100 a 150 mA", dark=True))
a.add(card(a, 632, 200, 230, 150, "Relé", "bobina 12 V"))
a.add(card(a, 924, 220, 228, 110, "Portón", "entrada pulsador"))
a.add(line(a, "M278 275H340", a.GREY, 3, "6 6"))
a.add(line(a, "M570 275H632", a.CYAN, 4))
# contacto del relé
a.add(f'<circle cx="680" cy="310" r="6" fill="#fff" stroke="{a.INK}" stroke-width="3"/><circle cx="760" cy="310" r="6" fill="#fff" stroke="{a.INK}" stroke-width="3"/>')
a.add(a.text(680, 340, "COM", 14, a.GREY, a.MONO, 600, "middle") + a.text(760, 340, "NO", 14, a.GREY, a.MONO, 600, "middle"))
at(a, line(a, "M686 310L752 284", a.INK, 4), 0, 50, 0)
at(a, line(a, "M686 310L754 306", a.OK, 4), 50, 75, 1)
at(a, line(a, "M686 310L752 284", a.INK, 4), 75, 100, 0)
a.add(line(a, "M862 275H924", a.CYAN, 4))
# señal
mv = a.move([(0, 120, 275), (5, 120, 275), (22, 330, 275), (100, 330, 275)])
op = a.keyframes([(0, 0), (5, 1), (22, 1), (24, 0), (100, 0)])
a.add(a.group(f'<circle cx="0" cy="0" r="10" fill="{a.CYAN}" stroke="#fff" stroke-width="3"/>', mv, op, still=0))
at(a, a.box(340, 220, 230, 110, "none", a.CYAN, rx=14, sw=5), 25, 75, 1)
at(a, a.box(632, 200, 230, 150, "none", a.CYAN, rx=14, sw=5), 25, 75, 1)
at(a, a.box(924, 220, 228, 110, a.OKBG, a.OK, rx=14, sw=3) + a.text(944, 254, "Portón", 19, a.OK, a.HEAD, 600) + a.text(944, 280, "abre", 15, a.OK, a.MONO, 700), 50, 75, 1)
# temporizador
a.add(card(a, 340, 400, 520, 120, "[281] = 002 · pulso de 2 s", None))
a.add(a.box(364, 456, 472, 30, a.SLATE, None, rx=15))
bar = a.keyframes([(0, 0), (25, 0), (75, 1), (76, 0), (100, 0)], "transform", "scaleX({})")
a.add(a.group(a.box(364, 456, 472, 30, a.CYAN, None, rx=15), bar, still=1, origin="364px 471px"))
caption(a, 600, [(0, 25, "La PGM espera su evento: grupo, subgrupo y partición.", None),
                 (25, 50, "La PGM solo mueve la bobina: por eso alcanza con 100 a 150 mA.", None),
                 (50, 75, "El motor del portón se alimenta de su propia placa, no de la central.", a.OK),
                 (75, 100, "Sin tiempo ([281] en 000), la PGM esperaría su evento de desactivación.", None)], still=2)
write(a, "8-t1.svg", "Del botón B al portón: evento, PGM, relé, pulso",
      "Animación en cuatro tiempos de izquierda a derecha: control, PGM1, relé y placa del portón. 1: llega el evento de activación, botón B de cualquier control, 08/99/99. "
      "2: la PGM1 se activa y energiza la bobina del relé. 3: el contacto seco entre COM y NO se cierra y la placa del portón lo ve como su pulsador: abre. "
      "4: termina el pulso de 2 segundos de la sección 281, la PGM vuelve sola y el contacto se abre.")
