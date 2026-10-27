import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 16.svg: qué se hace y cada cuánto
c = Canvas(K(), "Qué se revisa, cada cuánto y dónde queda escrito")
X0, X1 = 260, 1120


def px(m): return X0 + (X1 - X0) * m / 60  # meses


c.add(hline(X0, X1, 160, LINE2, 3))
for y_ in range(6):
    c.add(f'<path d="M{px(y_ * 12)} 152V168" stroke="{INK3}" stroke-width="2"/>')
    c.add(mid(px(y_ * 12), 190, "obra" if y_ == 0 else f"año {y_}", 14, 500, INK3, FM))
rows = [("Bosch (mínimo)", BLUE, [(m, "") for m in (12, 24, 36, 48, 60)], "inspección visual y funcional, pantalla recalibrada, ventilaciones"),
        ("NFPA 72: visual", CYAN, [(m, "") for m in range(6, 61, 6)], "semestral"),
        ("NFPA 72: prueba", OK, [(m, "") for m in (12, 24, 36, 48, 60)], "completa, anual"),
        ("Sensibilidad", WARN, [(12, ""), (24, ""), (60, "")], "primer año, a los dos y luego hasta cada cinco"),
        ("Hora del panel", ALERT, [(m, "") for m in range(6, 61, 6)], "en cada visita")]
for i, (t, col, marks, s) in enumerate(rows):
    y = 240 + i * 66
    c.add(text(48, y + 6, t, 17, 600, INK))
    c.add(hline(X0, X1, y, LINE, 1.5))
    for m, _ in marks:
        c.add(f'<circle cx="{px(m):.1f}" cy="{y}" r="9" fill="{col}"/>')
    c.add(text(X0, y + 30, s, 15, 400, INK3))
c.add(Note(48, 572, 1104, "En Uruguay el propietario mantiene y una empresa registrada hace el mantenimiento; las frecuencias las fija el proyecto. NFPA 72 se usa como referencia.", title="Lo que no está registrado no se hizo", kind="info"))
save(c, "16.svg")

# ---------------------------------------------------------------- 16-t2: valor óptico de contaminación (teoría, fija)
c = Canvas("Bosch Incendio · Mantenimiento", "El valor óptico dice cuándo cambiar el detector")
W = 208
segs = [(OK, .45, "0 a 170", "nuevo"), (OK, .85, "hasta 350", "normal"), (WARN, .85, "350 a 450", "cambiar pronto"),
        (ALERT, .85, "450 a 510", "cambiar ya"), (BLACK, .85, "más de 511", "sensor desactivado")]
c.add(text(80, 180, "VALOR ÓPTICO DEL FAP-425 (LECTURA DE DIAGNÓSTICO) · TRAMOS, NO A ESCALA", 13, 600, INK3, FM, ls=1.5))
for k, (col, op, r, t) in enumerate(segs):
    x = 80 + k * W
    c.add(f'<rect x="{x}" y="200" width="{W - 4}" height="70" rx="8" fill="{col}" fill-opacity="{op}"/>')
    c.add(mid(x + W / 2 - 2, 242, r, 16, 700, WHITE, FM))
    c.add(mid(x + W / 2 - 2, 300, t, 16, 600, col if col != BLACK else INK))
xe = 80 + 3 * W + W / 2
c.add(f'<path d="M{xe} 380V316" stroke="{ALERT}" stroke-width="2.5" marker-end="url(#a-alert)"/>')
c.add(rect(xe - 200, 380, 400, 80, ALERT_BG, ALERT, rx=12, sw=1.5))
c.add(text(xe - 182, 412, "Ejemplo: 470", 17, 700, ALERT, FM))
c.add(text(xe - 182, 440, "cambiar ya, en esa misma visita", 15, 400, INK2))
c.add(Note(48, 500, 1104, "Arriba de 450, el detector se reemplaza en la visita o se deja documentado como pendiente urgente al cliente. La contaminación se informa como avería, no como falsa alarma.", title="Qué hacer con el número", kind="warn"))
save(c, "16-t2.svg")
