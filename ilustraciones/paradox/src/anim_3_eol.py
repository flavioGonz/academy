"""Teoría lección 3: la central mide la resistencia del lazo (normal, abierta, corto)."""
from _apdx import *

a = new(20, "Lo que mide la central en una zona con EOL")
a.steps(["Normal: contacto cerrado y 1 kΩ al final. La central mide 1 kΩ.",
         "Se abre la puerta: el lazo queda abierto. Si está armada, alarma.",
         "Alguien une los cables: 0 Ω. La central lo ve como falla y tamper.",
         "Sin EOL, ese mismo corto se ve como una zona cerrada: invisible."], still=0)
# lazo
X, Y = 140, 260
a.add(a.text(X - 20, Y + 6, "Z", 18, a.INK, a.MONO, 700, "end"))
a.add(a.text(X - 20, Y + 166, "COM", 18, a.INK, a.MONO, 700, "end"))
a.add(f'<circle cx="{X}" cy="{Y}" r="10" fill="#CBD5DF" stroke="{a.GREY}" stroke-width="2"/><circle cx="{X}" cy="{Y + 160}" r="10" fill="#CBD5DF" stroke="{a.GREY}" stroke-width="2"/>')
a.add(line(a, f"M{X + 10} {Y}H{X + 220}"))
a.add(line(a, f"M{X + 320} {Y}H{X + 480}V{Y + 40}"))
a.add(line(a, f"M{X + 480} {Y + 120}V{Y + 160}H{X + 10}"))
# contacto: cerrado / abierto
a.add(f'<circle cx="{X + 226}" cy="{Y}" r="6" fill="#fff" stroke="{a.INK}" stroke-width="3"/><circle cx="{X + 314}" cy="{Y}" r="6" fill="#fff" stroke="{a.INK}" stroke-width="3"/>')
at(a, line(a, f"M{X + 232} {Y}L{X + 308} {Y - 6}", a.INK, 4), 0, 25, 1)
at(a, line(a, f"M{X + 232} {Y}L{X + 300} {Y - 40}", a.INK, 4), 25, 50, 0)
at(a, line(a, f"M{X + 232} {Y}L{X + 308} {Y - 6}", a.INK, 4), 50, 100, 0)
a.add(a.text(X + 270, Y - 56, "contacto NC", 15, a.GREY, a.MONO, 600, "middle"))
# resistencia (desaparece en el tramo 4)
at(a, a.box(X + 466, Y + 40, 28, 80, "#FFF7E0", a.AMB, rx=4, sw=3) + a.text(X + 510, Y + 86, "1 kΩ", 18, a.AMB, a.MONO, 700), 0, 75, 1)
at(a, line(a, f"M{X + 480} {Y + 40}V{Y + 120}") + a.text(X + 500, Y + 86, "sin resistencia", 16, a.GREY, a.SANS, 600), 75, 100, 0)
# puente de corto
at(a, line(a, f"M{X + 120} {Y}V{Y + 160}", a.BAD, 5) + dot(a, X + 120, Y, 6, a.BAD) + dot(a, X + 120, Y + 160, 6, a.BAD)
   + a.text(X + 132, Y + 86, "puente", 16, a.BAD, a.MONO, 700), 50, 100, 0)
# medidor de la central
MX, MY = 790, 200
a.add(card(a, MX, MY, 362, 300, "La central mide", None, dark=True))
for s, e, val, verdict, col, still in [(0, 25, "1 kΩ", "normal", a.OK, 1), (25, 50, "abierto", "zona abierta · alarma", a.AMB, 0),
                                       (50, 75, "0 Ω", "falla · TBL grupo 5", a.BAD, 0), (75, 100, "0 Ω", "parece cerrada", a.AMB, 0)]:
    at(a, a.text(MX + 181, MY + 150, val, 54, "#FFFFFF", a.MONO, 700, "middle")
       + a.box(MX + 30, MY + 200, 302, 52, col, None, rx=26) + a.text(MX + 181, MY + 233, verdict, 18, "#FFFFFF", a.SANS, 700, "middle"), s, e, still)
caption(a, 600, [(0, 25, "Con EOL, la central espera ver justo 1 kΩ: es la firma de un lazo sano.", None),
                 (25, 50, "Lazo abierto: puede ser la puerta o un cable cortado. Para la central es lo mismo.", a.AMB),
                 (50, 75, "El corto le saca la resistencia: la central sabe que alguien tocó el cable.", a.BAD),
                 (75, 100, "Sin resistencia no hay diferencia entre cerrado y puenteado: por eso existe la EOL.", a.AMB)])
write(a, "3-t1.svg", "Lo que mide la central en una zona con EOL",
      "Animación en cuatro tiempos de un lazo de zona con contacto normalmente cerrado y resistencia de 1 kΩ al final. "
      "1: contacto cerrado, la central mide 1 kΩ y la zona está normal. 2: se abre la puerta, el lazo queda abierto y, armada, es alarma. "
      "3: un puente une los cables, la central mide 0 Ω y muestra falla de tamper y cableado de zona, grupo 5 de TBL. "
      "4: sin resistencia, el mismo puente se ve como una zona cerrada y el sabotaje pasa inadvertido.")
