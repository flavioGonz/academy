import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *


def hump(xc, half, base, top, color, sw=2.5, op=0.12):
    xl, xr = xc - half, xc + half
    return (f'<path d="M{xl:.1f} {base}C{xl + half * 0.45:.1f} {top},{xr - half * 0.45:.1f} {top},{xr:.1f} {base}" '
            f'fill="{color}" fill-opacity="{op}" stroke="{color}" stroke-width="{sw}"/>')


# ---------------------------------------------------------------- 7.svg: canales angostos
c = Canvas(K(), "Canal angosto: menos ancho, menos choques")
c.add(panel(48, 124, 540, 410, "2.4 GHz: tres canales que no se pisan", "info"))
k = 470 / 84.0
X = lambda f: 78 + (f - 2400) * k
base, top = 420, 230
for n in range(1, 12):
    f = 2412 + 5 * (n - 1)
    if n not in (1, 6, 11):
        c.add(hump(X(f), 10 * k, base, top + 40, INK3, 1.2, 0.03))
for n, col in ((1, BLUE), (6, OK), (11, CYAN)):
    f = 2412 + 5 * (n - 1)
    c.add(hump(X(f), 10 * k, base, top, col, 3, 0.16))
c.add(hline(70, 566, base, INK3, 2))
for n in range(1, 12):
    f = 2412 + 5 * (n - 1)
    bold = n in (1, 6, 11)
    c.add(mid(X(f), base + 26, str(n), 16 if bold else 15, 700 if bold else 400, INK if bold else INK3, FM))
c.add(text(72, 488, "Siempre 20 MHz y solo 1, 6 u 11.", 18, 600, INK, FB))
c.add(text(72, 514, "Los canales del medio se pisan con dos de ellos.", 16, 400, INK2, FB))
c.add(panel(612, 124, 540, 410, "5 GHz: más ancho, menos canales", "info"))
chs = [36, 40, 44, 48]
cx0, cw = 650, 112
rows = [("20 MHz", [[36], [40], [44], [48]]), ("40 MHz", [[36, 40], [44, 48]]), ("80 MHz", [[36, 40, 44, 48]])]
for i, (lab, groups) in enumerate(rows):
    y = 204 + i * 84
    c.add(text(640, y - 8, lab, 15, 600, INK3, FM))
    for g in groups:
        x = cx0 + chs.index(g[0]) * cw
        w = len(g) * cw - 8
        c.add(rect(x, y, w, 46, SOFT, BLUE, rx=10, sw=2))
        c.add(mid(x + w / 2, y + 30, " + ".join(str(v) for v in g) if len(g) < 4 else "36 a 48, un solo canal", 15, 600, BLUE, FM))
c.add(text(640, 488, "Un canal de 80 ocupa lo que cuatro de 20.", 18, 600, INK, FB))
c.add(text(640, 514, "Con vecinos y muchos clientes, conviene angosto.", 16, 400, INK2, FB))
c.add(Note(48, 556, 1104, "Punto de partida en 5 GHz: 80 MHz en una casa, 40 MHz en una oficina, 20 MHz en alta densidad. El ancho se elige por clientes y vecinos, no por lo que dice la caja.", kind="ok"))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso1: mirar el entorno antes de elegir
c = Canvas(K(1), "Mirá qué canales usan los vecinos antes de elegir")
c.add(Window(48, 128, 700, 420, "UniFi Network", path="UniFi Devices > AP > AirView > Environment"))
c.add(Step(48, 128, 1))
bars = [(36, 210), (40, 230), (44, 190), (48, 220), (52, 60), (56, 40), (60, 70), (64, 30)]
for i, (ch, h) in enumerate(bars):
    x = 92 + i * 80
    col = ALERT if ch <= 48 else OK
    c.add(f'<rect x="{x}" y="{500 - h}" width="52" height="{h}" rx="6" fill="{col}" fill-opacity=".75"/>')
    c.add(mid(x + 26, 528, str(ch), 16, 600, INK, FM))
c.add(hline(80, 730, 502, INK3, 1.5))
c.add(text(92, 228, "uso de vecinos (ilustrativo)", 15, 500, INK3, FM))
c.add(tag(400, 230, "36 a 48 saturados", "alert", mono=False, anchor="start"))
c.add(tag(560, 400, "52 a 64: DFS, más limpios", "ok", mono=False))
c.add(Note(776, 128, 376, "Full recorre todos los canales pero desconecta a los clientes de esa radio. Hacelo fuera de horario.", title="Escaneo Full", kind="warn"))
c.add(Note(776, 300, 376, "Si el AP no tiene análisis en tiempo real, corré un Airtime Scan. Quick revisa canales del mismo ancho.", title="Sin análisis en vivo", kind="info"))
c.add(Note(776, 448, 376, "El patrón es el del caso de std.rocks: oficina con unos 300 equipos y 10 AP.", kind="info"))
save(c, "7-paso1.svg")

# ---------------------------------------------------------------- 7-paso2: el ancho por banda
c = Canvas(K(2), "Fijá el ancho por banda antes de Channel AI")
c.add(Window(48, 128, 520, 250, "UniFi Network", path="Settings > WiFi > Default WiFi Speeds > Custom", rows=[("2.4 GHz", "20 MHz"), ("5 GHz", "según el lugar"), ("6 GHz", "160 MHz")], hl=1))
c.add(Step(48, 128, 2))
cards = [("80 MHz", "Casa, pocos vecinos", "info"), ("40 MHz", "Oficina", "ok"), ("20 MHz", "Más de 30 clientes por AP", "warn")]
for i, (w_, lab, kd) in enumerate(cards):
    y = 128 + i * 84
    c.add(panel(612, y, 540, 70, None, kd))
    c.add(text(636, y + 44, w_, 24, 600, INK, FM))
    c.add(text(790, y + 43, lab, 18, 500, INK2, FB))
c.add(text(612, 396, "5 GHz: cuanto más denso, más angosto", 17, 600, INK, FB))
c.add(Note(48, 430, 520, "Después, Apply to All APs y Apply Changes (paso 3).", kind="info"))
c.add(Note(612, 430, 540, "Channel AI cambia canales, no anchos. Si fijás el ancho después, el plan de canales queda armado para otro ancho.", title="Por qué antes", kind="warn"))
save(c, "7-paso2.svg")

# ---------------------------------------------------------------- 7-paso5: DFS
c = Canvas(K(5), "DFS: canales limpios que se dejan ante un radar")
c.add(text(48, 150, "Canales de 5 GHz (según el caso de std.rocks)", 17, 600, INK, FB))
groups = [("36 a 48", "sin DFS", "warn", 260), ("52 a 64", "DFS", "ok", 260), ("100 a 140", "DFS", "ok", 480)]
x = 48
for lab, sub, kd, w in groups:
    bg, fg = {"warn": (WARN_BG, WARN), "ok": (OK_BG, OK)}[kd]
    c.add(rect(x, 170, w, 70, bg, fg, rx=12))
    c.add(text(x + 20, 204, lab, 19, 600, INK, FM))
    c.add(text(x + 20, 228, sub, 15, 500, fg, FM))
    x += w + 18
seq = [("AP en canal DFS", "canal 64 limpio", "ok"), ("Aparece un radar", "meteorológico, militar", "alert"), ("El AP deja el canal", "en el acto", "warn"), ("Clientes se cortan", "y reconectan", "alert")]
for i, (a, b, kd) in enumerate(seq):
    xx = 48 + i * 280
    c.add(panel(xx, 290, 250, 110, None, kd))
    c.add(text(xx + 20, 334, a, 19, 600, INK, FD))
    c.add(text(xx + 20, 362, b, 15, 400, INK3, FM))
    if i < 3:
        c.add(arrow((xx + 254, 345), (xx + 276, 345)))
c.add(Step(48, 290, 5))
c.add(Note(48, 430, 540, "Si 36 a 48 están saturados y el registro no muestra eventos de radar, activá Extended 5 GHz Spectrum (DFS) y probá.", title="Cuándo sí", kind="ok"))
c.add(Note(612, 430, 540, "Al día siguiente, AirView > Radios > Time Machine. Si ves cambios de canal por radar, volvé a los canales bajos.", title="Cuándo no", kind="alert"))
save(c, "7-paso5.svg")
