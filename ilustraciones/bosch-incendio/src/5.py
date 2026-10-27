import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *


def V(L, n, i):
    I = n * i + 0.012 + 0.018
    return 30 - I * (2 * L * 0.0178 / 0.503 + n * 0.35)


def meter(x, y, val, ok=True, label=""):
    col = OK if ok else ALERT
    return (rect(x, y, 150, 74, WHITE, col, rx=14, sw=2.5) + text(x + 75, y + 44, val, 26, 700, col, FM, anchor="middle")
            + text(x + 75, y + 66, label, 14, 500, INK3, FB, anchor="middle"))


# ---------------------------------------------------------------- 5.svg: peor caso
c = Canvas(K(), "Al último elemento tienen que llegarle 15 V")
c.add(rect(48, 200, 200, 180, DEEP, DEEP, rx=14))
c.add(text(70, 240, "Módulo LSN", 19, 600, WHITE, FD))
c.add(text(70, 266, "en bornes", 15, 400, "#9FC3E3", FM))
c.add(meter(73, 282, "30 V", True, "sale"))
c.add(f'<path d="M248 250H860" stroke="{BLUE}" stroke-width="4"/><path d="M248 300H860" stroke="{BLACK}" stroke-width="3"/>')
c.add(mid(554, 236, "cable de ida y vuelta: resta en cada metro", 16, 600, BLUE))
c.add(mid(554, 330, "0,8 mm (0,503 mm²) · cobre", 15, 500, INK3, FM))
c.add(rect(860, 170, 292, 220, SOFT, CYAN, rx=16, sw=2))
c.add(text(880, 200, "Todos los elementos al final", 16, 600, BLUE))
for k in range(3):
    for j in range(2):
        c.add(detector(910 + k * 70, 245 + j * 60, 22))
c.add(text(1060, 380, "cálculo pesimista", 14, 500, INK3, FB, anchor="middle"))
c.add(meter(930, 404, "≥ 15 V", True, "tiene que llegar"))
c.add(text(48, 440, "QUÉ RESTA TENSIÓN", 13, 600, INK3, FM, ls=1.5))
c.add(bullet_list(48, 474, ["El largo del cable (ida y vuelta)", "La cantidad de elementos y su consumo", "Sirenas y módulos, que consumen más"], 520)[0])
c.add(box(612, 500, 540, 120, "Límites que no se negocian", ["1600 m con LSN 0300 A · 3000 m con LSN 1500 A", "cable no aislado (entradas, NAC, indicadores): 500 m"], kind="warn", size=16))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso2: la cuenta resuelta
c = Canvas(K(2), "La cuenta con 600 m, 60 elementos y 0,5 mA")
s, h = codebox(48, 130, 700, [
    "R_cable = 2 x 600 x 0,0178 / 0,503  = 42,5 ohm",
    "R_equip = 60 x 0,35                 = 21,0 ohm",
    "I_total = 60 x 0,0005 + 0,012 + 0,018 = 0,060 A",
    "Caída   = 0,060 x (42,5 + 21,0)      =  3,8 V",
    ("Queda   = 30 - 3,8                    = 26,2 V", "#7FE0B0"),
], size=16, lh=34, title="PLANILLA")
c.add(s)
c.add(meter(800, 150, "26,2 V", True, "al final del lazo"))
c.add(Mark(980, 187, True)); c.add(text(1008, 194, "más de 15 V", 17, 600, OK))
c.add(box(800, 260, 352, 150, "De dónde sale cada número", ["2 x L: el par va y vuelve", "0,35 ohm por elemento improved", "0,012 A transmisión + 0,018 A destello"], size=15))
c.add(Note(48, 360, 700, "La planilla es la cuenta de banco del manual, siempre pesimista. Sirve para ver si un lazo está en el límite antes de tirar cable; el cálculo de la obra se hace en Safety Systems Designer.", title="Para qué sirve", kind="info"))
c.add(Note(48, 500, 700, "Con 2 mA por elemento (paso 3) la misma cuenta deja unos 20,5 V: el margen se achica rápido.", title="Lo que viene", kind="warn"))
save(c, "5-paso2.svg")

# ---------------------------------------------------------------- 5-paso4: dónde cruza los 15 V
c = Canvas(K(4), "¿Dónde cae a 15 V? Con 2 mA, cerca de 1100 m")
X0, X1, Y0, Y1 = 130, 860, 560, 160   # 0..1600 m, 0..30 V


def px(L): return X0 + (X1 - X0) * L / 1600


def py(v): return Y0 - (Y0 - Y1) * v / 30


c.add(f'<rect x="{X0}" y="{py(15)}" width="{X1 - X0}" height="{Y0 - py(15)}" fill="{ALERT_BG}" opacity=".7"/>')
for v in (0, 15, 30):
    c.add(hline(X0, X1, py(v), LINE2 if v != 15 else ALERT, 1.5 if v != 15 else 2.5))
    c.add(text(X0 - 12, py(v) + 5, f"{v} V", 15, 600, ALERT if v == 15 else INK3, FM, anchor="end"))
for L in (0, 400, 800, 1200, 1600):
    c.add(text(px(L), Y0 + 26, f"{L} m", 15, 500, INK3, FM, anchor="middle"))
c.add(text(X0 + 10, py(15) + 26, "zona de avería: menos de 15 V", 15, 600, ALERT))
for i, col, lab in [(0.0005, OK, "0,5 mA"), (0.002, WARN, "2 mA")]:
    pts = " ".join(f"{px(L):.1f},{py(max(V(L, 60, i), 0)):.1f}" for L in range(0, 1601, 50))
    c.add(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="4"/>')
    c.add(text(px(1600) + 10, py(V(1600, 60, i)) + 5, lab, 16, 700, col, FM))
c.add(f'<circle cx="{px(1116):.1f}" cy="{py(15):.1f}" r="8" fill="{WARN}"/>')
c.add(text(px(1116) - 14, py(15) + 34, "unos 1116 m", 16, 700, WARN, FM, anchor="end"))
c.add(f'<path d="M{px(1600)} {Y1}V{Y0}" stroke="{INK3}" stroke-width="2" stroke-dasharray="6 6"/>')
c.add(text(px(1600) - 8, Y1 - 10, "largo máximo LSN 0300 A", 14, 600, INK3, FB, anchor="end"))
c.add(box(960, 160, 192, 150, "0,5 mA", ["no llega a 15 V", "antes de 1600 m:", "manda el largo"], kind="ok", size=15))
c.add(box(960, 330, 192, 150, "2 mA", ["cruza 15 V a", "unos 1116 m:", "manda la tensión"], kind="warn", size=15))
c.add(text(48, 630, "60 elementos, cuenta de banco. Si da más largo que el gráfico del manual, confiá en el gráfico y en SSD.", 16, 500, INK2))
save(c, "5-paso4.svg")
