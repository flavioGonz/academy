from _oai import *

# ---------- 9.svg: el orden
c = Canvas("OmniAccess Intrusión · Lección 9", "Bajá las falsas en este orden")
lv = [("1", "Instalación", "horizonte y calle fuera del cuadro, vidrio limpio, sin telarañas"),
      ("2", "Regla", "línea lejos del árbol, un sentido, zona chica, sensibilidad 40 a 60"),
      ("3", "Objetivo", "Persona o Vehículo, si la cámara clasifica"),
      ("4", "Medir", "% de falsas y ritmo en el Análisis, una semana")]
for i, (n, t, d) in enumerate(lv):
    x = 48 + i * 150
    y = 420 - i * 80
    w = 1104 - i * 150
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
    c.add(f'<circle cx="{x + 34}" cy="{y + 35}" r="17" fill="{CYAN}"/>')
    c.add(text(x + 34, y + 41, n, 17, 700, WHITE, FD, anchor="middle"))
    c.add(text(x + 64, y + 42, t, 19, 600, INK, FD))
    c.add(text(x + 190, y + 42, d, 15, 500, INK2, FB))
c.add(Note(48, 520, 540, "Un cambio por vez y probado caminando de noche: si la persona deja de disparar, te pasaste.", title="El otro error", kind="alert", size=15))
c.add(Note(612, 520, 540, "Sin clasificación, ni porcentaje ni sensibilidad frenan gatos y pájaros: gana la geometría.", title="Cámara que no clasifica", kind="warn", size=15))
c.add(text(48, 215, "de abajo hacia arriba ↑", 15, 600, INK3, FM))
save(c, "9.svg")

# ---------- 9-paso4.svg: causa → cambio
c = Canvas("OmniAccess Intrusión · Lección 9 · Paso 4", "Mirá la foto falsa y elegí un solo cambio")
c.add(Table(48, 150, ["Lo que se ve en la foto", "El cambio", "Dónde"],
            [["Telaraña o vidrio sucio", "Limpiar, sin tocar la regla", "en la cámara"],
             ["Faros o calle en el cuadro", "Línea más adentro o sentido A→B", "calibrador"],
             ["Perros, gatos, pájaros", "Objetivo: Persona", "calibrador"],
             ["Árbol o arbustos", "Zona más chica, línea lejos; sensibilidad 40", "calibrador"]],
            [360, 470, 274], row_h=56))
c.add(Step(48, 150, 4))
c.add(Note(48, 450, 1104, "Anotá la fecha del cambio: en una semana comparás el porcentaje de falsas de esa cámara.", kind="info", size=16))
save(c, "9-paso4.svg")

# ---------- 9-paso6.svg: medir
c = Canvas("OmniAccess Intrusión · Lección 9 · Paso 6", "Una semana después, compará el porcentaje")
base = 470
for i, (lab, pct, col) in enumerate([("Antes del cambio", 82, ALERT), ("Una semana después", 35, OK)]):
    x = 200 + i * 360
    h = pct * 3
    c.add(f'<rect x="{x}" y="{base - h}" width="160" height="{h}" rx="12" fill="{col}"/>')
    c.add(text(x + 80, base - h - 14, f"{pct} %", 28, 700, INK, FD, anchor="middle"))
    c.add(text(x + 80, base + 32, lab, 17, 600, INK2, FB, anchor="middle"))
c.add(f'<path d="M150 {base}H760" stroke="{LINE2}" stroke-width="2"/>')
c.add(text(150, 170, "% de falsas de las últimas revisadas · ejemplo", 15, 600, INK3, FM))
c.add(Note(820, 200, 332, "El Análisis lo calcula con las últimas 50 revisadas de la cámara, desde 5.", title="De dónde sale", kind="info", size=15))
c.add(Note(820, 360, 332, "Si bajó y la persona sigue disparando en la prueba de noche, el cambio quedó.", title="Cuándo dejarlo", kind="ok", size=15))
c.add(Step(150, 210, 6))
save(c, "9-paso6.svg")
