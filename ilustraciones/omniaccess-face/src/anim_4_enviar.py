"""Teoría de Rostros al terminal: ID estable de 9 dígitos, usuario y foto; Memoria Flash lee lo que el equipo tiene."""
from _anim_face import *

caps = ["Del identificador interno sale un ID de 9 dígitos: siempre el mismo.",
        "Crea o actualiza la persona en el terminal: nombre, tarjetas y PIN.",
        "Manda la foto en base64: el terminal guarda una plantilla, o la rechaza.",
        "Un reenvío actualiza la misma fila. Memoria Flash lee lo que el equipo tiene."]
a = new(24, "Enviar rostro", "Enviar un rostro: un ID estable y dos pedidos", caps, still=3, size=17)
S = [sp[0] for sp in a.spans]

# ficha
FX, FY, FW, FH = 48, 178, 320, 290
a.add(a.box(FX, FY, FW, FH, a.WHITE, a.LINE))
a.add(a.text(FX + 20, FY + 32, "Ficha en OmniAccess", 17, a.INK, a.SANS, 600))
a.add(a.box(FX + 20, FY + 50, 80, 92, a.SLATE, rx=8) + person(a, FX + 60, FY + 82, .55, fill="#9DB2C6"))
a.add(a.text(FX + 116, FY + 76, "Ana Ejemplo", 18, a.INK, a.SANS, 600) + a.text(FX + 116, FY + 102, "Lote 12", 15, a.GREY, a.MONO))
a.add(a.text(FX + 116, FY + 126, "tarjeta · PIN", 15, a.GREY, a.MONO))
a.add(a.text(FX + 20, FY + 176, "identificador interno", 15, a.GREY, a.MONO, 600))
a.add(a.box(FX + 20, FY + 186, 280, 26, a.SLATE, rx=6) + a.text(FX + 32, FY + 205, "texto largo, único", 14, a.GREY, a.MONO))
vis(a, line(a, FX + 160, FY + 214, FX + 160, FY + 232, a.BLUE, 2.5) + a.box(FX + 20, FY + 236, 280, 40, "#E3EEF9", a.BLUE, rx=8)
    + a.text(FX + 34, FY + 262, "ID 000482193", 18, a.BLUE, a.MONO, 600), 0, 3, d0=4)
vis(a, a.text(FX + 20, FY + FH + 26, "mismo cálculo, mismo número", 15, a.BLUE, a.SANS, 600), 0, d0=8)

# terminal
TX, TW = 800, 352
a.add(a.box(TX, FY, TW, FH, a.WHITE, a.LINE))
a.add(a.text(TX + 20, FY + 32, "Portería peatonal · memoria", 17, a.INK, a.SANS, 600))
for k, h in enumerate(("ID", "NOMBRE", "ROSTRO")):
    a.add(a.text(TX + 20 + (0, 130, 268)[k], FY + 66, h, 14, a.GREY, a.MONO, 600))
a.add(a.text(TX + 20, FY + 104, "001937520", 15, a.TXT, a.MONO) + a.text(TX + 150, FY + 104, "Bruno Ejemplo", 15, a.TXT) + a.text(TX + 288, FY + 104, "✓", 16, a.OK, a.MONO, 600))
RY = FY + 144
vis(a, a.box(TX + 10, RY - 24, TW - 20, 36, a.OKBG, rx=8) + a.text(TX + 20, RY, "000482193", 15, a.INK, a.MONO, 600) + a.text(TX + 150, RY, "Ana Ejemplo", 15, a.INK, a.SANS, 600), 1, 3, d0=8)
vis(a, a.text(TX + 288, RY, "no", 15, a.GREY, a.MONO, 600), 1, d0=8)
vis(a, a.text(TX + 288, RY, "✓", 16, a.OK, a.MONO, 600), 2, 3, d0=10)
vis(a, a.text(TX + 20, FY + 200, "plantilla de rasgos guardada", 15, a.OK, a.SANS, 600)
    + a.text(TX + 20, FY + 230, "sin cara usable: rechazo y", 15, a.AMB, a.SANS, 600) + a.text(TX + 20, FY + 252, "error en el cajón de la ficha", 15, a.AMB, a.SANS, 600), 2, d0=12)
vis(a, a.box(TX + 10, RY + 16, TW - 20, 36, "none", a.BAD, rx=8, extra='stroke-dasharray="6 5"') + a.text(TX + 20, RY + 40, "000482193", 15, a.BAD, a.MONO)
    + a.text(TX + 150, RY + 40, "no se duplica", 15, a.BAD, a.SANS, 600), 3, d0=7)
vis(a, a.pill(TX + 20, FY + 214, "misma fila, actualizada", a.OK, a.OKBG, size=14), 3, d0=6)

# pedidos
mid = (FX + FW + TX) / 2
vis(a, line(a, FX + FW + 10, 300, TX - 10, 300, a.BLUE, 3) + a.text(mid, 288, "usuario: nombre, tarjetas, PIN", 15, a.BLUE, a.SANS, 600, "middle"), 1, 3, d0=2)
vis(a, line(a, FX + FW + 10, 350, TX - 10, 350, a.CYAN, 3) + a.text(mid, 338, "foto en base64 → rostros", 15, "#0B7FA3", a.SANS, 600, "middle"), 2, 3, d0=2)
token(a, "crear / actualizar", [(S[1] + 2, FX + FW + 90, 300), (S[1] + 8, TX - 90, 300), (S[1] + 9, TX - 90, 300)], bg=a.BLUE, size=13)
token(a, "JPG → base64", [(S[2] + 2, FX + FW + 90, 350), (S[2] + 9, TX - 90, 350), (S[2] + 10, TX - 90, 350)], size=13)
token(a, "reenvío · ID 000482193", [(S[3] + 1, FX + FW + 110, 300), (S[3] + 6, TX - 110, 300), (S[3] + 7, TX - 110, 300)], bg=a.BLUE, size=13)

# Memoria Flash
a.add(a.box(48, 516, 1104, 120, a.SLATE, None, rx=14))
a.add(a.text(72, 552, "Memoria Flash", 18, a.INK, a.SANS, 600))
a.add(a.text(72, 584, "hace el camino inverso: le pide al equipo sus usuarios y sus rostros, los cruza y muestra qué tiene cada ID.", 16, a.TXT))
vis(a, a.pill(72, 598, "solo en el equipo", a.AMB, a.AMBBG, size=14) + a.pill(260, 598, "sincronizado", a.OK, a.OKBG, size=14)
    + a.text(420, 618, "la verdad está en el terminal", 16, a.INK, a.SANS, 600), 3, d0=10)
write(a, "4-t1.svg", "Enviar un rostro al terminal", [12, 37, 62, 92])
