"""Teoría de El terminal avisa: la Action URL es una plantilla; el servidor normaliza el evento y busca el equipo por la MAC."""
from _anim_face import *

caps = ["En el terminal, la Action URL es una plantilla con $variables.",
        "Al reconocer a alguien, reemplaza cada $variable por el dato real y la manda al 10000.",
        "El servidor lee el tipo de evento y lo normaliza.",
        "Busca el equipo por la MAC: sin equipo, no hay evento; con equipo, va por la foto."]
a = new(24, "Action URL", "De la plantilla al evento", caps, still=3, size=17)
S = [sp[0] for sp in a.spans]

a.add(a.box(48, 176, 1104, 150, a.INK, rx=16))
a.add(a.text(70, 206, "TERMINAL · ACTION URL DE «VALID FACE»", 14, DARK_SUB, a.MONO, 600, extra='letter-spacing="1.5"'))
CW = 12.3  # ancho de un carácter mono a 20 px
a.add(a.text(70, 248, "GET /api/webhooks/akuvox?event=face_valid", 20, a.WHITE, a.MONO, 600))
segs = [("&mac=", None, 17), (None, ("$mac", "00:00:5E:00:53:21"), 17), ("&user=", None, 6), (None, ("$user_name", "Ana%20Ejemplo"), 13),
        ("&userid=", None, 8), (None, ("$userid", "000482193"), 9), ("&...", None, 4)]
x = 70
for lit, var, n in segs:
    if lit:
        a.add(a.text(x, 292, lit, 20, a.WHITE, a.MONO, 600))
        x += len(lit) * CW
    else:
        ph_, val = var
        w = n * CW + 12
        vis(a, a.box(x - 4, 270, w, 32, "#3A2A0B", "#FFD28A", rx=6, sw=1.5) + a.text(x + 2, 292, ph_, 20, "#FFD28A", a.MONO, 600), 0)
        a.add(a.group(a.box(x - 4, 270, w, 32, "#0E3B2C", "#5BE0A5", rx=6, sw=1.5) + a.text(x + 2, 292, val, 20, "#5BE0A5", a.MONO, 600),
                      a.show(S[1] + 3, 100, .8), still=1))
        x += w + 8
# viaje al servidor
a.add(a.pill(1152, 340, "servidor · puerto 10000", a.WHITE, a.BLUE, size=14, anchor="end"))
token(a, "GET", [(S[1] + 8, 120, 354), (S[1] + 18, 900, 354), (S[1] + 20, 900, 354)], size=13)

# normalización
NX, NY, NW, NH = 48, 392, 520, 230
a.add(a.box(NX, NY, NW, NH, a.WHITE, a.LINE))
a.add(a.text(NX + 20, NY + 32, "1 · Tipo de evento, normalizado", 18, a.INK, a.SANS, 600))
rows = [("event=face_valid", "face_valid · rostro"), ("event=relay_open", "door_open · puerta abierta"), ("event=card&type=invalid", "card_invalid")]
for k, (i, o) in enumerate(rows):
    y = NY + 76 + k * 46
    a.add(a.text(NX + 20, y, i, 15, a.TXT, a.MONO, 600) + a.text(NX + 238, y, "→", 16, a.GREY, a.MONO) + a.text(NX + 260, y, o, 15, a.INK, a.MONO, 600))
    if k < 2:
        vis(a, a.box(NX + 10, y - 26, NW - 20, 38, "none", a.CYAN, rx=8, sw=2.5), 2, d0=2 + k * 8, fade=.6)
vis(a, a.box(NX + 10, NY + 50, NW - 20, 38, "none", a.CYAN, rx=8, sw=2.5), 3)

# equipo por MAC
MX, MW = 600, 552
a.add(a.box(MX, NY, MW, NH, a.WHITE, a.LINE))
a.add(a.text(MX + 20, NY + 32, "2 · Equipo por la MAC (Dispositivos)", 18, a.INK, a.SANS, 600))
devs = [("00:00:5E:00:53:21", "Portería peatonal"), ("00:00:5E:00:53:22", "Portería de servicio")]
for k, (m, n) in enumerate(devs):
    y = NY + 76 + k * 40
    a.add(a.text(MX + 20, y, m, 15, a.TXT, a.MONO, 600) + a.text(MX + 222, y, n, 16, a.INK, a.SANS, 600))
vis(a, a.box(MX + 10, NY + 50, MW - 20, 38, a.OKBG, a.OK, rx=8, sw=2) + a.text(MX + 20, NY + 76, devs[0][0], 15, a.OK, a.MONO, 600)
    + a.text(MX + 222, NY + 76, devs[0][1], 16, a.INK, a.SANS, 600) + check(a, MX + MW - 34, NY + 69, 13), 3, d0=2)
vis(a, a.text(MX + 20, NY + 168, "→ foto del registro del terminal → monitor", 16, a.OK, a.SANS, 600), 3, d0=6)
vis(a, a.text(MX + 20, NY + 204, "MAC 00:00:5E:00:53:99, no cargada: sin evento", 16, a.BAD, a.SANS, 600), 3, d0=12)
write(a, "3-t1.svg", "Action URL: de la plantilla al evento", [12, 40, 62, 92])
