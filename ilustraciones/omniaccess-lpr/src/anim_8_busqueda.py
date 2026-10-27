"""Teoría de Investigar matrícula: la Búsqueda inteligente traduce la frase a filtros; la búsqueda por imagen va al NVR."""
from _anim_lpr import *

caps = ["Escribís como hablás, en modo Accesos.",
        "Un analizador, sin IA ni internet, traduce cada palabra a un filtro.",
        "Los filtros corren sobre los eventos propios: al instante, portones incluidos.",
        "La búsqueda por imagen es otra: la hace el NVR, solo con cámaras de contexto."]
a = new(22, "Búsqueda", "Búsqueda inteligente: de la frase a los filtros", caps, still=2)

# caja de búsqueda con tipeo
a.add(a.box(48, 178, 720, 58, a.WHITE, a.BLUE, rx=12, sw=2.5))
a.add(a.pill(630, 193, "Accesos", a.OK, a.OKBG, size=14))
words = [("camioneta", 72), ("blanca", 187), ("ayer", 264), ("a la tarde", 318)]
s0 = ph(a, 0)[0]
for k, (w, x) in enumerate(words):
    a.add(a.group(a.text(x, 214, w, 20, a.INK, a.MONO, 600), a.show(s0 + 2 + k * 4, 100, 0.4), still=1))
# chips
chips = [("camioneta", "→ tipo", 48), ("color blanco", "→ color", 228), ("ayer", "→ fecha", 408), ("tarde (12–20 h)", "→ hora del día", 556)]
s0 = ph(a, 1)[0]
for k, ((c, sub, x), (w, wx)) in enumerate(zip(chips, words)):
    t = s0 + 2 + k * 4
    a.add(a.group(line(a, wx + len(w) * 6, 242, x + 60, 266, a.OK, 2), a.show(t, ph(a, 1)[1], 0.6), still=0))
    a.add(a.group(a.pill(x, 270, c, a.OK, a.OKBG, size=15, h=30) + a.text(x + 4, 322, sub, 15, a.GREY, a.MONO), a.show(t + 1, 100, 0.6), still=1))

# tabla de eventos propios
TX, TY, TW = 48, 350, 720
a.add(a.box(TX, TY, TW, 268, a.WHITE, a.LINE))
cols = [("HORA", 20), ("MATRÍCULA", 160), ("TIPO", 300), ("COLOR", 448), ("ACCESO", 580)]
for c, dx in cols:
    a.add(a.text(TX + dx, TY + 30, c, 14, a.GREY, a.MONO, 600))
rows = [("ayer 09:12", "SBA1234", "auto", "gris", "P1", False),
        ("ayer 14:05", "SCD5678", "camioneta", "blanco", "P2", True),
        ("ayer 16:40", "SBB4321", "camioneta", "blanco", "P5 portón", True),
        ("ayer 17:22", "SAC1010", "camioneta", "negro", "P1", False),
        ("ayer 18:47", "SDE9090", "camioneta", "blanco", "P1", True),
        ("hoy 15:10", "SBA9876", "camioneta", "blanco", "P2", False)]
s0, s1 = ph(a, 2)
for k, (h, p, t, c, acc, hit) in enumerate(rows):
    y = TY + 46 + k * 36
    cells = "".join(a.text(TX + dx, y + 24, v, 16, a.INK, a.MONO, 600 if i == 1 else 400) for i, ((_, dx), v) in enumerate(zip(cols, (h, p, t, c, acc))))
    if hit:
        a.add(a.group(a.box(TX + 8, y, TW - 16, 34, a.OKBG, rx=8), a.show(s0 + 4, s1, 0.8), still=1))
        a.add(cells)
    else:
        a.add(a.group(cells, a.keyframes([(0, 1), (s0 + 3, 1), (s0 + 5, .22), (s1 - 1, .22), (s1, 1), (100, 1)]), still=.22))
vis(a, a.text(48, 650, "3 eventos coinciden, en menos de un segundo, incluido el portón P5.", 17, a.OK, a.SANS, 600), 2, d0=5)

# panel derecho: fuentes / búsqueda por imagen
RX, RW = 800, 352
vis(a, a.box(RX, 178, RW, 440, a.SLATE, None, rx=16)
    + a.text(RX + 22, 214, "De dónde salen los datos", 18, a.INK, a.SANS, 600)
    + a.text(RX + 22, 254, "Lo que reportó la cámara:", 16, a.TXT, a.SANS, 600)
    + a.text(RX + 22, 280, "color, tipo, marca", 16, a.BLUE, a.MONO, 600)
    + a.text(RX + 22, 326, "Lo que sabe el sistema:", 16, a.TXT, a.SANS, 600)
    + a.text(RX + 22, 352, "acceso, sentido,", 16, a.BLUE, a.MONO, 600)
    + a.text(RX + 22, 376, "decisión, hora", 16, a.BLUE, a.MONO, 600)
    + a.text(RX + 22, 430, "Todo en la base propia:", 16, a.TXT)
    + a.text(RX + 22, 454, "no sale del predio.", 16, a.TXT), 0, 2)
s0 = ph(a, 3)[0]
nvr = (a.box(RX, 178, RW, 440, a.WHITE, a.LINE, rx=16)
       + a.text(RX + 22, 214, "Búsqueda por imagen", 18, a.INK, a.SANS, 600)
       + card(a, RX + 60, 250, 232, 74, "NVR", "índice de analítica", dark=True, tsize=18)
       + card(a, RX + 22, 438, 150, 74, "Contexto", "cámara", tsize=17)
       + card(a, RX + 186, 438, 150, 74, "Matrícula", "cámara LPR", tsize=17)
       + line(a, RX + 97, 432, RX + 140, 332, a.OK, 3)
       + line(a, RX + 261, 432, RX + 218, 332, a.BAD, 3, "7 5")
       + f'<g transform="translate({RX + 240},{382})"><circle r="15" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2"/><path d="M-6 -6 L6 6 M6 -6 L-6 6" stroke="{a.BAD}" stroke-width="3"/></g>'
       + a.text(RX + 22, 548, "La cámara de matrícula no", 16, a.TXT)
       + a.text(RX + 22, 572, "alimenta ese índice: es un", 16, a.TXT)
       + a.text(RX + 22, 596, "límite del hardware.", 16, a.TXT))
vis(a, nvr, 3)
token(a, "foto", [(s0 + 3, RX + 176, 240), (s0 + 7, RX + 176, 260), (s0 + 9, RX + 176, 260)], bg=a.BLUE, size=13)
write(a, "8-t1.svg", "Búsqueda inteligente", [12, 37, 62, 90])
