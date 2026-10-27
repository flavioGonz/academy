import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *


def cabezal(cx, top, h=150, col=INK2, label=None):
    """Cabezal de prueba en pértiga, debajo de un detector de techo (cx, top = borde inferior del detector)."""
    out = [f'<path d="M{cx - 34} {top + 6}H{cx + 34}L{cx + 26} {top + 52}H{cx - 26}Z" fill="{SOFT}" stroke="{col}" stroke-width="2.5"/>',
           f'<path d="M{cx} {top + 52}V{top + h}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>']
    if label:
        out.append(text(cx + 44, top + 36, label, 15, 600, col, FB))
    return "".join(out)


# ---------------------------------------------------------------- 15.svg: cuatro formas de probar
c = Canvas(K(), "Cómo se prueba cada detector, y cuánto esperar")
cards = [("Modo revisión", "óptico con aerosol", "hasta 10 s", "El detector se prepara solo para la prueba al pasar la zona a revisión.", "info"),
         ("Walk test secuencial", "multisensor, un sensor por vez", "hasta 20 s", "Aerosol, calor y, en el DOTC, gas de CO de 0,5 a 1 s.", "info"),
         ("Walk test simultáneo", "herramienta multiestímulo", "todos o nada", "La alarma aparece solo si dispararon todos los sensores.", "ok"),
         ("Fuera de revisión", "con dependencia de 2 detectores", "hasta 1 min", "Aerosol en ráfagas: 1 s, esperás 30 s, otra ráfaga.", "warn")]
for i, (t, s, tm, d, kd) in enumerate(cards):
    x = 48 + (i % 2) * 564
    y = 130 + (i // 2) * 230
    c.add(panel(x, y, 540, 210, t, kd, title_size=20))
    c.add(text(x + 20, y + 64, s, 16, 500, INK3))
    c.add(tag(x + 520, y + 36, tm, kd if kd != "info" else "info", size=15, anchor="end"))
    c.add(wrap(x + 20, y + 110, d, 360, 16)[0])
    c.add(detector(x + 460, y + 132, 30))
    c.add(cabezal(x + 460, y + 162, 30, BLUE if kd == "info" else (OK if kd == "ok" else WARN)))
c.add(text(48, 625, "El cabezal queda arriba del detector hasta que dispare. Cada prueba se anota con método, segundos, resultado y hora.", 16, 500, INK2))
save(c, "15.svg")

# ---------------------------------------------------------------- 15-paso3: aerosol y contar segundos
c = Canvas(K(3), "Aerosol con el cabezal y contá hasta la alarma")
c.add(rect(48, 130, 560, 26, "#E9EFF5", LINE2, rx=6, sw=1.5)); c.add(text(60, 149, "techo", 14, 500, INK3, FM))
c.add(f'<path d="M300 156V176" stroke="{INK3}" stroke-width="3"/>')
c.add(detector(300, 206, 32, state="alarm"))
c.add(cabezal(300, 238, 300, BLUE, "cabezal con aerosol"))
c.add(text(330, 400, "queda arriba", 16, 600, BLUE)); c.add(text(330, 422, "hasta que dispare", 16, 600, BLUE))
c.add(text(352, 210, "LED en alarma", 15, 600, ALERT))
# reloj de segundos
X0, X1 = 660, 1140
c.add(text(X0, 170, "SEGUNDOS DESDE QUE APLICÁS", 13, 600, INK3, FM, ls=1.5))
c.add(hline(X0, X1, 230, LINE2, 6))
for s in range(0, 11, 2):
    x = X0 + (X1 - X0) * s / 10
    c.add(f'<path d="M{x} 222V238" stroke="{INK3}" stroke-width="2"/>'); c.add(mid(x, 262, f"{s}", 15, 500, INK3, FM))
c.add(f'<path d="M{X0} 230H{X1}" stroke="{BLUE}" stroke-width="6" stroke-opacity=".5"/>')
c.add(text(X1, 300, "hasta 10 s: el aerosol tarda en", 16, 600, BLUE, FB, anchor="end"))
c.add(text(X1, 324, "distribuirse dentro de la cámara", 16, 600, BLUE, FB, anchor="end"))
c.add(codebox(660, 380, 492, ["Dirección  3.1", "Modelo     FAP-425-O-R", "Modo       revisión · óptico", "Segundos   __   Resultado __   Hora __"], title="ANOTÁ")[0])
c.add(Note(48, 560, 1104, "Antes: zona en modo revisión, monitoreo avisado y salidas aisladas, como en Aislar y avisar, aunque sea en banco.", title="Paso 1 y 2", kind="info"))
save(c, "15-paso3.svg")

# ---------------------------------------------------------------- 15-paso4: secuencial en el multisensor
c = Canvas(K(4), "Multisensor, secuencial: un sensor por vez")
seq = [("Óptico", "aerosol de prueba", BLUE, "hasta 20 s en multisensor"), ("Térmico", "herramienta de calor", WARN, "anotá los segundos"), ("CO (solo DOTC)", "gas de prueba 0,5 a 1 s", OK, "anotá los segundos")]
for i, (t, s, col, foot) in enumerate(seq):
    x = 48 + i * 376
    c.add(rect(x, 140, 352, 250, WHITE, col, rx=16, sw=2.5))
    c.add(badge(x + 36, 178, str(i + 1), col))
    c.add(text(x + 66, 185, t, 20, 600, INK, FD))
    c.add(text(x + 24, 226, s, 16, 500, INK2))
    c.add(detector(x + 176, 296, 34))
    c.add(text(x + 24, 370, foot, 15, 600, col))
    if i < 2:
        c.add(arrow((x + 354, 265), (x + 374, 265)))
c.add(text(48, 420, "En el FAP-425-OT-R del laboratorio hay dos sensores: óptico y térmico. El de CO es del DOTC.", 15, 400, INK3))
c.add(Table(48, 446, ["Dirección", "Modelo", "Sensor", "Segundos", "Resultado"], [["3.2", "FAP-425-OT-R", "óptico", "__", "__"], ["3.2", "FAP-425-OT-R", "térmico", "__", "__"]], [150, 260, 220, 220, 254], row_h=44, mono_cols=(0, 1)))
save(c, "15-paso4.svg")
