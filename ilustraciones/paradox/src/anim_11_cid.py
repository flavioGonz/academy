"""Teoría lección 11: un mensaje Contact ID, campo por campo, hasta el operador."""
from _apdx import *

a = new(22, "Un evento en Contact ID, campo por campo")
a.steps(["Central armada: se abre la ventana de la zona 3.",
         "La central arma el mensaje: abonado, tipo, evento, partición y zona.",
         "El mensaje viaja a la receptora, que confirma que lo recibió.",
         "El operador ve abonado 1A01, robo, partición 1, zona 3."], still=1)
fields = [("1A01", "abonado", a.BLUE), ("18", "tipo", a.GREY), ("1", "nuevo", a.AMB), ("130", "robo", a.BAD), ("01", "partición", a.OK), ("003", "zona", a.CYAN)]
x = 140
for i, (v, lab, col) in enumerate(fields):
    w = len(v) * 22 + 40
    at(a, a.box(x, 220, w, 64, "#03213C", None, rx=10) + a.text(x + w / 2, 262, v, 28, "#fff", a.MONO, 700, "middle")
       + a.text(x + w / 2, 312, lab, 15, col, a.SANS, 700, "middle"), 25 + i * 3, 100, 1)
    x += w + 16
at(a, a.text(x + 4, 262, "+ control", 15, a.GREY, a.SANS, 600), 45, 100, 1)
at(a, card(a, 48, 210, 1104, 90, "Zona 3 · ventana", "armada: instantánea, dispara") , 0, 25, 0)
# viaje
a.add(card(a, 48, 380, 240, 110, "Central", "abonado 1A01", dark=True))
a.add(card(a, 470, 380, 260, 110, "Receptora", "IPR512 o IPC10"))
a.add(card(a, 912, 380, 240, 110, "Operador", "software de monitoreo"))
mv = a.move([(0, 300, 435), (50, 300, 435), (62, 460, 435), (100, 460, 435)])
op = a.keyframes([(0, 0), (50, 0), (51, 1), (62, 1), (63, 0), (100, 0)])
a.add(a.group(f'<rect x="-50" y="-14" width="100" height="28" rx="14" fill="{a.CYAN}"/><text x="0" y="5" font-family="{a.MONO}" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">mensaje</text>', mv, op, still=0))
at(a, a.arrow("M466 470H294", a.OK, 3) + a.text(380, 520, "recibido", 15, a.OK, a.MONO, 700, "middle"), 62, 100, 0)
at(a, a.arrow("M730 435H906", a.BLUE, 3), 75, 100, 0)
at(a, a.box(912, 380, 240, 110, a.BADBG, a.BAD, rx=14, sw=3) + a.text(932, 414, "ROBO · 1A01", 18, a.BAD, a.MONO, 700)
   + a.text(932, 446, "partición 1", 15, a.INK, a.SANS, 600) + a.text(932, 470, "zona 3 · ventana", 15, a.INK, a.SANS, 600), 77, 100, 0)
caption(a, 600, [(0, 25, "En [810], el 4 es Contact ID. Por IP o GPRS, es el formato que va.", None),
                 (25, 50, "Calificador 1 = evento nuevo; 3 = restauración. 130 es robo en la tabla de Contact ID.", None),
                 (50, 75, "Si la receptora no confirma, la central vuelve a intentar.", None),
                 (75, 100, "El abonado de cada partición es lo que convierte un número en un cliente.", a.OK)], still=1)
write(a, "11-t1.svg", "Un evento en Contact ID, campo por campo",
      "Animación en cuatro tiempos. 1: con la central armada se abre la ventana de la zona 3. 2: la central arma el mensaje Contact ID campo por campo: abonado 1A01, tipo 18, calificador 1 de evento nuevo, código 130 de robo, partición 01, zona 003 y un dígito de control. "
      "3: el mensaje viaja a la receptora, que confirma la recepción. 4: el operador ve en su software robo en el abonado 1A01, partición 1, zona 3.")
