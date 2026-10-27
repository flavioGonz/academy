"""Teoría de Recorrido de lectura: los cinco tramos de una lectura, con el cronómetro de 1 a 3 s."""
from _anim_lpr import *

caps = ["La cámara ve el auto en la línea de captura, lee la patente y arma el XML.",
        "Lo manda por HTTP: un POST multipart al puerto 10000 del servidor.",
        "El receptor separa XML e imágenes, reconoce la cámara y decide.",
        "La foto va al bucket lpr y el evento a la base de datos.",
        "El servidor empuja el evento en vivo al Monitor LPR."]
a = new(25, "Recorrido", "Una lectura, cinco tramos, un cronómetro", caps, still=4)

W, G, Y, H = 200, 26, 186, 84
names = [("Cámara ANPR", "lee a bordo"), ("Red", "HTTP"), ("Servidor", "puerto 10000"), ("Base y fotos", "bucket lpr"), ("Monitor LPR", "en vivo")]
cx = [48 + i * (W + G) + W / 2 for i in range(5)]
for i, (t, s) in enumerate(names):
    x = 48 + i * (W + G)
    a.add(card(a, x, Y, W, H, t, s, dark=(i == 2)))
    vis(a, a.box(x - 4, Y - 4, W + 8, H + 8, "none", a.CYAN, rx=17, sw=3.5), i)
# carril de la ficha
a.add(line(a, cx[0], 306, cx[4], 306, a.LINE, 2, "4 6", arrow=False))
for x in cx:
    a.add(f'<circle cx="{x}" cy="306" r="5" fill="{a.LINE}"/>')

# detalle de cada tramo (aparece en su tiempo y queda)
det = [["licensePlate", "confianza · MAC", "hora · 2 fotos"],
       ["POST multipart", "XML + imágenes"],
       ["separa el XML", "MAC, si no IP", "antirrebote", "decide"],
       ["foto → bucket lpr", "evento → base"],
       ["a los navegadores", "abiertos"]]
for i, rows in enumerate(det):
    x = 48 + i * (W + G)
    inner = "".join(a.text(x + 14, 360 + k * 24, r, 15, a.TXT, a.MONO) for k, r in enumerate(rows))
    vis(a, inner, i, 4)
vis(a, a.pill(48 + 2 * (W + G) + 14, 442, "Autorizado", a.OK, a.OKBG), 2, 4)
vis(a, a.box(48 + 4 * (W + G) + 14, 410, 172, 52, a.OKBG, a.OK, rx=10) + a.text(48 + 4 * (W + G) + 30, 443, "SBA 1234", 18, a.INK, a.MONO, 600), 4)

# la ficha que viaja
token(a, "SBA1234", [(2, cx[0], 306), (20, cx[0], 306), (28, cx[1], 306), (37, cx[2], 306), (60, cx[2], 306),
                     (68, cx[3], 306), (80, cx[3], 306), (88, cx[4], 306), (99, cx[4], 306)], size=14)
# en el fijo, la ficha queda en el monitor
a.add(a.group(a.pill(cx[4], 292, "SBA1234", a.WHITE, a.CYAN, anchor="middle"), a.keyframes([(0, 0), (100, 0)]), still=1))

# cronómetro 0..12 s
X0, X1, CY = 176, 1100, 528
px = (X1 - X0) / 12
a.add(a.text(48, CY + 6, "CRONÓMETRO", 14, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))
a.add(a.box(X0, CY - 12, X1 - X0, 24, a.SLATE, rx=12))
a.add(a.box(X0, CY - 12, 3 * px, 24, a.OKBG, rx=12))
a.add(a.box(X0 + 10 * px, CY - 12, 2 * px, 24, a.BADBG, rx=12))
for s, lab in ((0, "0 s"), (3, "3 s"), (10, "10 s")):
    a.add(a.text(X0 + s * px, CY + 40, lab, 15, a.GREY, a.MONO, 600, "middle"))
a.add(a.text(X1, CY - 22, "más de 10 s habituales: algún tramo degradado", 15, a.BAD, a.SANS, 600, "end"))
fill = a.keyframes([(0, 0), (2, 0), (98, 1), (100, 1)], "transform", "scaleX({})")
a.add(a.group(a.box(X0, CY - 8, 2.2 * px, 16, a.OK, rx=8), fill, still=1, origin=f"{X0}px {CY}px"))
vis(a, a.text(X0 + 2.2 * px + 16, CY + 6, "1 a 3 s: normal", 16, a.OK, a.SANS, 600), 4)

# el NVR, aparte
a.add(a.box(48, 586, 1104, 60, a.WHITE, a.LINE, rx=12))
a.add(a.text(70, 622, "NVR", 17, a.INK, a.SANS, 600))
a.add(a.text(120, 622, "graba aparte, todo el tiempo. El servidor le pide el video solo al tocar Grabación, Clip o Exportar.", 16, a.TXT))
write(a, "1-t1.svg", "Recorrido de una lectura", [12, 30, 50, 70, 92])
