"""Teoría de Grupos y horarios: el grupo documenta, la copia hace reconocer y el horario lo decide el terminal (y un reenvío lo pisa)."""
from _anim_face import *

caps = ["Grupo de Acceso: personas por equipos. Queda en OmniAccess y documenta.",
        "La copia lleva cara, nombre, tarjetas y PIN, con el horario siempre (1001).",
        "En el terminal le ponen a Ana L a V de 8 a 17: a las 7:30 no abre.",
        "Reenvío: crear falla porque ya existe, actualiza todo y el horario vuelve a siempre."]
a = new(24, "Horarios", "Grupo, copia y horario: cada cosa en su lugar", caps, still=3, size=17)
S = [sp[0] for sp in a.spans]

# OmniAccess
a.add(a.box(48, 178, 440, 300, "none", "#C2D4E6", rx=20, extra='stroke-dasharray="7 7"'))
a.add(a.text(70, 172, "OMNIACCESS", 14, a.BLUE, a.MONO, 600))
a.add(a.box(68, 196, 400, 124, a.WHITE, a.LINE) + a.text(88, 226, "Grupo de Acceso · Residentes", 17, a.INK, a.SANS, 600)
      + a.pill(88, 244, "Ana", a.INK, a.SLATE, size=14) + a.pill(150, 244, "Bruno", a.INK, a.SLATE, size=14)
      + a.text(240, 264, "×", 18, a.GREY, a.MONO, 600) + a.pill(262, 244, "Portería peatonal", a.INK, a.SLATE, size=14)
      + a.text(88, 302, "quién pasa por dónde", 15, a.GREY, a.MONO))
vis(a, a.box(64, 192, 408, 132, "none", a.CYAN, rx=16, sw=3) + a.text(270, 352, "no viaja al terminal: ordena y documenta", 15, a.BLUE, a.SANS, 600, "middle"), 0)
a.add(a.box(68, 372, 400, 92, a.WHITE, a.LINE) + a.text(88, 402, "Ficha de Ana · A qué equipos se manda", 16, a.INK, a.SANS, 600)
      + a.box(88, 420, 22, 22, a.BLUE, rx=5) + '<path d="M93 431 l5 5 l8 -10" fill="none" stroke="#fff" stroke-width="3"/>'
      + a.text(120, 437, "Portería peatonal", 16, a.INK, a.SANS))

# terminal
TX = 720
a.add(a.box(TX, 178, 432, 300, "none", "#C2D4E6", rx=20, extra='stroke-dasharray="7 7"'))
a.add(a.text(TX + 22, 172, "TERMINAL · PORTERÍA PEATONAL", 14, a.OK, a.MONO, 600))
a.add(a.box(TX + 20, 196, 392, 268, a.WHITE, a.LINE))
vis(a, a.text(TX + 40, 228, "Ana Ejemplo", 18, a.INK, a.SANS, 600) + a.text(TX + 40, 260, "cara · nombre · tarjetas · PIN", 15, a.GREY, a.MONO)
    + a.text(TX + 40, 306, "horario", 15, a.GREY, a.MONO, 600), 1, 3, d0=8)
vis(a, a.text(TX + 40, 228, "Ana todavía no está aquí", 17, a.GREY, a.SANS, 600), 0)
hor = [(1, "siempre (1001)", a.OK, a.OKBG), (2, "L a V · 8:00 a 17:00", a.AMB, a.AMBBG), (3, "siempre (1001)", a.OK, a.OKBG)]
for st, t, fg, bg in hor:
    vis(a, a.pill(TX + 40, 318, t, fg, bg, size=17, h=36), st, d0=(9 if st != 2 else 2))
vis(a, a.text(TX + 40, 392, "cargado a mano en la web del equipo", 15, a.AMB, a.SANS, 600), 2, d0=2)
vis(a, a.text(TX + 40, 392, "nadie lo tocó: lo pisó el reenvío", 15, a.BAD, a.SANS, 600), 3, d0=10)

# viaje
token(a, "copia · horario 1001", [(S[1] + 2, 520, 420), (S[1] + 8, 680, 300), (S[1] + 9, 680, 300)], size=13)
s3 = S[3]
token(a, "crear", [(s3 + 1, 520, 420), (s3 + 4, 660, 300), (s3 + 5, 660, 300)], bg=a.BLUE, size=13)
vis(a, a.pill(604, 236, "ya existe", a.BAD, a.BADBG, size=14, anchor="middle"), 3, d0=5)
token(a, "actualizar todo", [(s3 + 7, 520, 420), (s3 + 10, 660, 300), (s3 + 11, 660, 300)], size=13)

# prueba en la puerta
a.add(a.box(48, 510, 1104, 120, a.WHITE, a.LINE))
a.add(a.text(72, 546, "En la puerta, un lunes a las", 18, a.INK, a.SANS, 600) + a.text(332, 546, "7:30", 22, a.INK, a.MONO, 600))
vis(a, a.text(72, 586, "Sin cara en el terminal no hay reconocimiento: el grupo solo no alcanza.", 17, a.TXT), 0)
vis(a, a.text(72, 586, "Reconoce y abre: el horario es siempre.", 17, a.OK, a.SANS, 600), 1, d0=10)
vis(a, a.text(72, 586, "Reconoce, pero está fuera de su horario: el terminal no abre.", 17, a.BAD, a.SANS, 600), 2, d0=6)
vis(a, a.text(72, 586, "Vuelve a abrir a las 7:30, sin que nadie lo haya decidido.", 17, a.BAD, a.SANS, 600), 3, d0=12)
a.add(a.text(72, 614, "Anotá en la ficha de la obra quién tiene horario en el terminal y revisalo después de cada reenvío.", 15, a.GREY))
write(a, "5-t1.svg", "Grupo, copia y horario", [12, 40, 62, 92])
