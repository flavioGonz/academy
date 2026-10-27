import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 6.svg: sin área no hay vivo
c = Canvas(K(), "Sin área, la cámara existe pero nadie la puede usar")
for i, ok in enumerate([False, True]):
    x = 48 + i * 564
    c.add(panel(x, 124, 540, 380, "Agregada sin importar a un área" if not ok else "Canales importados a un área", "alert" if not ok else "ok"))
    n = c.add(Generic(x + 24, 180, "NVR del depósito", "online en Device", icon="server", w=250))
    if ok:
        c.add(rect(x + 300, 172, 216, 100, WHITE, OK, rx=14))
        c.add(text(x + 318, 202, "Área Nave 1", 16, 600, OK, FM))
        c.add(text(x + 318, 230, "CAM-01 a CAM-04", 15, 400, INK2, FM))
        c.add(text(x + 318, 254, "Puerta N1", 15, 400, INK2, FM))
        c.add(Arrow(n.right(), (x + 298, 222), kind="ok"))
    else:
        c.add(rect(x + 300, 172, 216, 100, WHITE, ALERT, rx=14, dash="6 5"))
        c.add(text(x + 318, 214, "ningún área", 16, 600, ALERT, FM))
        c.add(text(x + 318, 244, "canales sin ubicar", 15, 400, INK3))
    for j, s in enumerate(["Vivo", "Reproducción", "Eventos y alarmas"]):
        y = 320 + j * 52
        c.add(Mark(x + 44, y, ok))
        c.add(text(x + 76, y + 7, s + (": sí" if ok else ": no"), 18, 600, OK if ok else ALERT))
c.add(text(48, 548, "En el alta, activá Add Resource to Area. Si te lo olvidaste, importá los canales desde el área.", 17, 500, INK2))
c.add(text(48, 588, "El árbol de áreas se diseña antes de dar de alta el primer equipo.", 18, 600, BLUE, FD))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso5: área madre e hijas
c = Canvas(K(5), "Las cámaras de las hijas no aparecen en la madre")
c.add(rect(48, 132, 520, 440, WHITE, LINE2, rx=16))
c.add(text(72, 170, "ÁRBOL DE ÁREAS", 13, 600, INK3, FM, ls=1.5))
tree = [(0, "Sitio Ejemplo", ""), (1, "Depósito", "sin cámaras propias"), (2, "Nave 1", "CAM-01..04"), (2, "Nave 2", "CAM-05..08"), (1, "Oficinas", "CAM-09..10")]
for i, (lv, t, d) in enumerate(tree):
    y = 214 + i * 66
    x = 80 + lv * 52
    if lv:
        c.add(f'<path d="M{x - 30} {y - 46}V{y - 8}H{x - 8}" fill="none" stroke="{LINE2}" stroke-width="2"/>')
    hl = t == "Depósito"
    c.add(rect(x, y - 30, 200, 44, SOFT if hl else WHITE, CYAN if hl else LINE2, rx=10, sw=3 if hl else 2))
    c.add(text(x + 16, y - 2, t, 17, 600, INK))
    if d:
        c.add(text(x + 216, y - 2, d, 15, 500, INK3 if not hl else WARN, FM))
c.add(panel(612, 132, 540, 200, "Doble clic en Depósito", "warn"))
c.add(code(636, 196, 492, "There is no camera in this area", 16, color="#FFD28A", h=48))
c.add(text(636, 290, "Las 8 cámaras están en Nave 1 y Nave 2.", 17, 500, INK2))
c.add(panel(612, 356, 540, 216, "Doble clic en Nave 1", "ok"))
for k in range(4):
    c.add(rect(636 + (k % 2) * 124, 400 + (k // 2) * 78, 112, 66, DEEP, DEEP, rx=8))
    c.add(mid(636 + (k % 2) * 124 + 56, 440 + (k // 2) * 78, f"CAM-0{k + 1}", 15, 600, "#9FC3E3", FM))
c.add(text(900, 440, "Vivo de las cuatro", 17, 600, OK))
c.add(text(900, 470, "cámaras de la nave.", 17, 500, INK2))
c.add(text(48, 620, "Cada recurso va en el área donde el operador lo busca, no en la de arriba.", 17, 600, INK))
save(c, "6-paso5.svg")

# ---------------------------------------------------------------- 6-paso6: E-map y GIS
c = Canvas(K(6), "E-map para un plano fijo, GIS para un mapa vivo")
c.add(panel(48, 124, 540, 400, "E-map", "info", sub="imagen estática: el plano de la planta"))
c.add(rect(72, 200, 492, 230, SOFT, LINE2, rx=10))
c.add(f'<path d="M92 220H544V410H92Z M300 220V330 M300 330H544 M92 330H220" fill="none" stroke="{INK3}" stroke-width="3"/>')
c.add(text(110, 252, "Nave 1", 15, 600, INK3, FM))
c.add(text(320, 252, "Nave 2", 15, 600, INK3, FM))
c.add(text(110, 362, "Oficinas", 15, 600, INK3, FM))
for (px, py, l) in [(180, 290, "CAM-01"), (260, 300, "CAM-02"), (420, 290, "CAM-05"), (160, 390, "CAM-09")]:
    c.add(f'<circle cx="{px}" cy="{py}" r="12" fill="{CYAN}" stroke="{WHITE}" stroke-width="3"/>')
c.add(text(72, 466, "Cargás un JPG del plano y ubicás cada cámara", 16, 400, INK2))
c.add(text(72, 490, "como punto caliente (hot spot).", 16, 400, INK2))
c.add(panel(612, 124, 540, 400, "GIS", "info", sub="mapa geográfico con datos en tiempo real"))
c.add(rect(636, 200, 492, 230, "#EAF4EC", LINE2, rx=10))
c.add(f'<path d="M650 400 C720 330,800 360,870 300 S1020 240,1110 220" fill="none" stroke="{WHITE}" stroke-width="10"/>')
c.add(f'<path d="M700 220 L760 420" fill="none" stroke="{WHITE}" stroke-width="8"/>')
for (px, py) in [(740, 345), (900, 290), (1040, 250)]:
    c.add(f'<circle cx="{px}" cy="{py}" r="12" fill="{CYAN}" stroke="{WHITE}" stroke-width="3"/>')
c.add(text(636, 466, "Para sitios repartidos en una ciudad o una ruta:", 16, 400, INK2))
c.add(text(636, 490, "dónde está cada sede, cada cámara y cada alarma.", 16, 400, INK2))
c.add(Note(48, 548, 1104, "Una cámara entra una sola vez en cada mapa y puede ser punto caliente en hasta 6 mapas (FAQ V2.5.500).", kind="info"))
save(c, "6-paso6.svg")
