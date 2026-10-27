import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 6.svg: dos pasos
c = Canvas(K(), "Elegí en dos pasos y dejá escrito el porqué")
cols = [("1", "Riesgo de fuego", ["fuego latente, con humo", "fuego rápido, con llama", "combustión con poco humo"], "info"),
        ("2", "Lo que no es fuego", ["vapor de ducha o cocina", "polvo", "aerosoles"], "warn"),
        ("3", "Modelo y porqué", ["el detector que ve ese fuego", "y no confunde ese fenómeno", "queda escrito en la tabla"], "ok")]
for i, (n, t, ls, kd) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 130, 352, 220, None, kd))
    c.add(badge(x + 36, 168, n, {"info": BLUE, "warn": WARN, "ok": OK}[kd]))
    c.add(text(x + 66, 175, t, 20, 600, INK, FD))
    c.add(bullet_list(x + 24, 222, ls, 310, 16)[0])
    if i < 2:
        c.add(arrow((x + 354, 240), (x + 374, 240)))
c.add(text(48, 392, "EJEMPLO DEL LABORATORIO", 13, 600, INK3, FM, ls=1.5))
c.add(Table(48, 404, ["Ambiente", "Riesgo", "Engañoso", "Detector", "Porqué"],
            [["Habitación hotel", "latente (tapizados)", "vapor, aerosol", "FAP-425-DOTC-R", "CO rechaza vapor"]],
            [200, 210, 180, 200, 314], row_h=46, mono_cols=(3,)))
c.add(Note(48, 520, 540, "El firmware 4.8 es el último que soporta la serie 400 (O400, OT400, OC410, OTC410, T400): relevá antes de actualizar.", title="Serie vieja", kind="warn"))
c.add(Note(612, 520, 540, "La línea vigente es AVENAR detector 4000, con nueve variantes. Un \"AVENAR detector 5000\" no aparece en las fuentes de Bosch.", title="Ojo con los nombres", kind="info"))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-t2: nueve variantes y sus sensores (teoría, fija)
c = Canvas("Bosch Incendio · Detectores", "Nueve variantes: qué sensores trae cada una")
S = ["Óptico", "Doble óptico", "Térmico", "Químico (CO)"]
rows = [("FAH-425-T-R", "térmico", (0, 0, 1, 0)), ("FAP-425-O", "óptico", (1, 0, 0, 0)), ("FAP-425-O-R", "óptico", (1, 0, 0, 0)),
        ("FAP-425-DO-R", "doble óptico", (0, 1, 0, 0)), ("FAP-425-OT", "multisensor", (1, 0, 1, 0)), ("FAP-425-OT-R", "multisensor", (1, 0, 1, 0)),
        ("FAP-425-DOT-R", "multisensor", (0, 1, 1, 0)), ("FAP-425-DOTC-R", "multisensor", (0, 1, 1, 1)), ("FAP-425-DOTCO-R", "multisensor", (0, 1, 1, 1))]
x0, y0, rh = 48, 136, 46
c.add(rect(x0, y0, 1104, rh * 10, WHITE, LINE2, rx=12))
c.add(text(x0 + 18, y0 + 30, "MODELO", 13, 600, INK3, FM, ls=1.2))
for j, s in enumerate(S):
    c.add(mid(560 + j * 150, y0 + 30, s, 15, 600, INK2))
for i, (m, k, f) in enumerate(rows):
    y = y0 + rh * (i + 1)
    c.add(hline(x0 + 12, x0 + 1092, y, LINE))
    c.add(text(x0 + 18, y + 30, m, 16, 600, INK, FM))
    c.add(text(x0 + 240, y + 30, k, 15, 400, INK3))
    for j, on in enumerate(f):
        cx = 560 + j * 150
        if on:
            col = [BLUE, CYAN, WARN, OK][j]
            c.add(f'<circle cx="{cx}" cy="{y + 24}" r="11" fill="{col}"/>')
        else:
            c.add(f'<circle cx="{cx}" cy="{y + 24}" r="5" fill="{LINE}"/>')
c.add(text(x0 + 980, y0 + rh * 9 + 30, "CO 10 años", 14, 600, OK, FB))
c.add(text(48, 625, "-R: con perillas de dirección. Doble óptico: LED infrarrojo y azul. Todos traen aislador.", 16, 500, INK2))
save(c, "6-t2.svg")
