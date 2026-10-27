"""Teoría de Enrolar en portería: el orden del alta, con la bifurcación del consentimiento."""
from _anim_face import *

caps = ["Se informa con un texto corto y se deja constancia: quién, cuándo, quién leyó.",
        "Si acepta: foto de frente, una sola cara, luz pareja.",
        "Ficha con unidad y terminal; prueba: pasa y sale Permitido con su nombre.",
        "Si no acepta: tarjeta, PIN o portería, sin castigo."]
a = new(24, "Consentimiento", "Alta en portería: el consentimiento va primero", caps, still=2, size=17)
S = [sp[0] for sp in a.spans]

Y = 236
nodes = {
    "A": (48, Y, 150, 84, "Persona", "nueva"),
    "B": (226, Y, 200, 84, "Informar", "y anotar"),
    "C": (600, 186, 160, 84, "Foto", "de frente"),
    "D": (790, 186, 170, 84, "Ficha", "y envío"),
    "E": (990, 186, 162, 84, "Prueba", "Permitido"),
    "F": (600, 330, 552, 84, "Alternativa", "tarjeta · PIN · portería"),
}
for k, (x, y, w, h, t, s) in nodes.items():
    a.add(card(a, x, y, w, h, t, s, tsize=18))
DX, DY = 512, Y + 42
a.add(f'<path d="M{DX} {DY - 50} L{DX + 56} {DY} L{DX} {DY + 50} L{DX - 56} {DY} Z" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="2"/>')
a.add(a.text(DX, DY + 6, "¿Acepta?", 16, a.INK, a.SANS, 600, "middle"))
a.add(line(a, 198, Y + 42, 222, Y + 42, a.GREY, 2.5) + line(a, 426, Y + 42, DX - 60, Y + 42, a.GREY, 2.5))
a.add(f'<path d="M{DX} {DY - 50} V228 H594" fill="none" stroke="{a.OK}" stroke-width="2.5" marker-end="url(#{a._marker(a.OK)})"/>' + a.text(DX + 10, 214, "sí", 15, a.OK, a.MONO, 600))
a.add(f'<path d="M{DX} {DY + 50} V372 H594" fill="none" stroke="{a.AMB}" stroke-width="2.5" marker-end="url(#{a._marker(a.AMB)})"/>' + a.text(DX + 10, 362, "no", 15, a.AMB, a.MONO, 600))
a.add(line(a, 760, 228, 786, 228, a.GREY, 2.5) + line(a, 960, 228, 986, 228, a.GREY, 2.5))

hl = lambda k, c: a.box(nodes[k][0] - 4, nodes[k][1] - 4, nodes[k][2] + 8, nodes[k][3] + 8, "none", c, rx=17, sw=3.5)
vis(a, hl("B", a.CYAN), 0, d0=4)
vis(a, a.box(226, Y + 100, 200, 96, a.WHITE, a.LINE, rx=10) + a.text(242, Y + 128, "constancia", 15, a.GREY, a.MONO, 600)
    + a.text(242, Y + 152, "quién · cuándo", 15, a.INK, a.MONO) + a.text(242, Y + 176, "quién leyó", 15, a.INK, a.MONO), 0, 3, d0=7)
vis(a, hl("C", a.CYAN), 1, d0=8)
vis(a, a.text(600, 296, "una cara · luz pareja", 15, a.TXT, a.SANS, 600), 1, 3, d0=9)
vis(a, hl("D", a.CYAN), 2, d0=3)
vis(a, hl("E", a.OK), 2, d0=10)
vis(a, a.text(790, 296, "unidad · A qué equipos se manda", 15, a.TXT, a.SANS, 600), 2, 3, d0=3)
vis(a, hl("F", a.AMB), 3, d0=7)
vis(a, a.text(600, 440, "sin castigo y igual de cómoda", 15, a.AMB, a.SANS, 600), 3, d0=8)
token(a, "persona", [(S[0] + 1, 123, Y + 20), (S[0] + 5, 326, Y + 20), (S[0] + 7, 326, Y + 20)], bg=a.INK, size=13)
token(a, "acepta", [(S[1] + 1, DX, DY - 60), (S[1] + 6, 680, 176), (S[1] + 8, 680, 176)], bg=a.OK, size=13)
token(a, "foto ok", [(S[2] + 1, 680, 176), (S[2] + 4, 875, 176), (S[2] + 8, 1071, 176), (S[2] + 10, 1071, 176)], bg=a.OK, size=13)
token(a, "no acepta", [(S[3] + 1, DX, DY + 62), (S[3] + 6, 690, 330), (S[3] + 8, 690, 330)], bg=a.AMB, size=13)

a.add(a.box(48, 486, 540, 150, a.SLATE, None, rx=14))
a.add(a.text(70, 520, "Técnico y guardia", 18, a.INK, a.SANS, 600))
for k, t in enumerate(("que el consentimiento quede registrado", "que exista la alternativa", "que la foto se use solo para lo dicho")):
    a.add(a.text(70, 552 + k * 26, "· " + t, 16, a.TXT))
a.add(a.box(612, 486, 540, 150, a.SLATE, None, rx=14))
a.add(a.text(634, 520, "Responsable de la base (administración)", 18, a.INK, a.SANS, 600))
for k, t in enumerate(("evaluación de impacto (art. 18 bis)", "inscripción de la base", "texto definitivo, con su asesor")):
    a.add(a.text(634, 552 + k * 26, "· " + t, 16, a.TXT))
write(a, "7-t1.svg", "Alta con consentimiento", [12, 37, 62, 90])
