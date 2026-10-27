import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *


def scene(c, x, y, w, h, r, ok, cid):
    """Dos AP con sus celdas y un celular cerca del AP 2."""
    c.add(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/></clipPath>')
    a1, a2 = (x + 110, y + h / 2), (x + w - 110, y + h / 2)
    col = OK if ok else ALERT
    op = 0.05 if r > 180 else 0.1
    c.add(f'<g clip-path="url(#{cid})">' + cell(a1[0], a1[1], r, BLUE, op, "10 6") + cell(a2[0], a2[1], r, CYAN, op, "10 6") + "</g>")
    c.add(APNode(a1[0], a1[1], "AP 1", "", r=32))
    c.add(APNode(a2[0], a2[1], "AP 2", "", r=32))
    px, py = a2[0] - 70, a2[1] + 80
    tgt = a2 if ok else a1
    c.add(f'<path d="M{px} {py - 18}L{tgt[0] + (30 if not ok else -10)} {tgt[1] + 26}" stroke="{col}" stroke-width="3"' + ("" if ok else ' stroke-dasharray="8 6"') + "/>")
    c.add(f'<rect x="{px - 13}" y="{py - 22}" width="26" height="44" rx="6" fill="{WHITE}" stroke="{col}" stroke-width="2.5"/>')
    c.add(mid(px, py + 44, "celular", 15, 600, col))


# ---------------------------------------------------------------- 8.svg: potencia alta contra potencia baja
c = Canvas(K(), "Potencia alta: el celular se queda en el AP lejano")
c.add(panel(48, 124, 540, 330, None, "alert"))
scene(c, 48, 160, 540, 290, 230, False, "s1")
c.add(text(68, 152, "Todo al máximo", 18, 600, ALERT, FD))
c.add(panel(612, 124, 540, 330, None, "ok"))
scene(c, 612, 160, 540, 290, 140, True, "s2")
c.add(text(632, 152, "Potencia baja, celdas chicas", 18, 600, OK, FD))
c.add(text(68, 438, "cada AP llega a todo el local", 15, 600, INK2, FB))
c.add(text(632, 438, "celdas que apenas se solapan", 15, 600, INK2, FB))
c.add(Note(48, 474, 540, "El celular ve fuerte al AP 1 y no busca otro. El AP llega lejos pero el celular no le contesta bien: reintentos, velocidad baja y airtime gastado para todos.", title="Cliente pegajoso", kind="alert"))
c.add(Note(612, 474, 540, "Al acercarse al AP 2, el AP 1 se debilita y el celular se pasa. Si queda un rincón débil, un AP más antes que subirle a todos.", title="Cada uno en su AP", kind="ok"))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso1: la caminata con WiFiman
c = Canvas(K(1), "Tres puntos, una caminata y una tabla")
c.add(rect(48, 130, 640, 360, WHITE, INK3, rx=8, sw=3))
c.add(text(68, 160, "planta del local", 15, 500, INK3, FM))
c.add(APNode(170, 300, "AP 1", "", r=30))
c.add(APNode(566, 300, "AP 2", "", r=30))
pts = [("A", 250, "cerca del AP 1"), ("B", 368, "entre los dos"), ("C", 486, "cerca del AP 2")]
c.add(f'<path d="M250 430H486" stroke="{INK3}" stroke-width="2.5" stroke-dasharray="6 8" marker-end="url(#a-gray)"/>')
for p, x, lab in pts:
    c.add(f'<circle cx="{x}" cy="410" r="18" fill="{CYAN}" stroke="{WHITE}" stroke-width="3"/>' + mid(x, 416, p, 17, 700, WHITE, FD))
    c.add(mid(x, 466, lab, 15, 500, INK2))
c.add(Step(48, 130, 1))
c.add(Table(724, 130, ["Punto", "Señal", "AP"], [["A", "__ dBm", "AP __"], ["B", "__ dBm", "AP __"], ["C", "__ dBm", "AP __"]], [120, 160, 148], mono_cols=(1, 2), row_h=46))
c.add(Phone(724, 340, "WiFiman", "en el celular", w=428))
c.add(Note(48, 516, 1104, "Anotá la señal y a qué AP estás conectado en cada punto, antes de tocar nada. Es tu línea de base para comparar después del cambio (paso 4).", kind="info"))
save(c, "8-paso1.svg")

# ---------------------------------------------------------------- 8-paso2: valores de partida por banda
c = Canvas(K(2), "Punto de partida con varios AP: baja, media, alta")
c.add(Window(48, 130, 560, 290, "UniFi Network", path="AirView > Radios", rows=[("2.4 GHz", "Low"), ("5 GHz", "Medium"), ("", "Low si hay un AP por ambiente"), ("6 GHz", "High")], hl=0))
c.add(Step(48, 130, 2))
why = [("2.4 GHz, baja", "Atraviesa más paredes. Purple: en diseños enterprise suele ir 3 a 6 dB por debajo de 5 GHz.", "info"),
       ("5 GHz, entre baja y media", "Media si un AP cubre varios ambientes; baja si hay uno por ambiente.", "info"),
       ("6 GHz, alta", "Alcanza menos que las otras dos: arranca alta.", "info")]
y = 130
for a, b, kd in why:
    c.add(text(640, y + 24, a, 18, 600, INK, FD))
    svg_, hh = wrap(640, y + 52, b, 500, 16, 400, INK2)
    c.add(svg_)
    y += 46 + hh + 18
c.add(Note(48, 450, 560, "Con un solo AP, potencia alta: no hay otro AP al que pasarse.", title="La excepción", kind="warn"))
c.add(Note(640, 450, 512, "Son puntos de partida (WunderTech, LazyAdmin, std.rocks). Se ajustan AP por AP, caminando.", kind="info"))
save(c, "8-paso2.svg")

# ---------------------------------------------------------------- 8-paso4: leer el resultado
c = Canvas(K(4), "Repetí la caminata y leé la señal en cada punto")
x0, x1 = 80, 1120
vals = [-50, -55, -60, -65, -70, -75, -80]
X = lambda v: x0 + (-50 - v) / 30 * (x1 - x0)
c.add(f'<rect x="{X(-50)}" y="170" width="{X(-65) - X(-50)}" height="44" rx="10" fill="{OK_BG}" stroke="{OK}" stroke-width="2"/>')
c.add(f'<rect x="{X(-65)}" y="170" width="{X(-70) - X(-65)}" height="44" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/>')
c.add(f'<rect x="{X(-70)}" y="170" width="{X(-80) - X(-70)}" height="44" rx="10" fill="{ALERT_BG}" stroke="{ALERT}" stroke-width="2"/>')
c.add(mid((X(-50) + X(-65)) / 2, 198, "-65 dBm o mejor: recomendado", 16, 600, OK))
c.add(mid((X(-65) + X(-70)) / 2, 198, "hasta el mínimo", 16, 600, WARN))
c.add(mid((X(-70) + X(-80)) / 2, 198, "por debajo de -70", 16, 600, ALERT))
for v in vals:
    c.add(mid(X(v), 244, f"{v}", 15, 500, INK3, FM))
c.add(text(80, 150, "Señal del celular (dBm)", 16, 600, INK, FB))
rows = [("A", "AP 1", "sigue en el AP 1", "ok"), ("B", "AP 1 o AP 2", "zona de traspaso", "ok"), ("C", "AP 2", "ya pasó al AP 2, con -65 o mejor", "ok")]
for i, (p, ap, s, kd) in enumerate(rows):
    y = 290 + i * 62
    c.add(f'<circle cx="98" cy="{y + 22}" r="18" fill="{CYAN}" stroke="{WHITE}" stroke-width="3"/>' + mid(98, y + 28, p, 17, 700, WHITE, FD))
    c.add(text(134, y + 29, ap, 18, 600, INK, FM))
    c.add(text(330, y + 29, s, 17, 400, INK2, FB))
c.add(Step(48, 290, 4))
c.add(Note(720, 290, 432, "Un punto por debajo de -70 dBm: candidato a un AP más, o subí un nivel solo ese AP.", title="Si queda débil", kind="alert"))
c.add(Note(48, 494, 1104, "Bajá la potencia AP por AP y caminando: en producción, un cambio de golpe puede dejar rincones sin cobertura. Ubiquiti trata -70 dBm como mínimo y recomienda -65 o mejor (según WunderTech).", kind="warn"))
save(c, "8-paso4.svg")
