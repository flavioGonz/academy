import sys, math; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *


def side_view(c, x0, ground, H, h, D, m=90, angle_ok=True, show_dims=True, car_w=230):
    """Vista de costado: poste con cámara a H m, patente a h m y D m de distancia (escala m px/m)."""
    cy = ground - H * m
    px, py = x0 + D * m, ground - h * m
    c.add(f'<path d="M{x0 - 60} {ground}H{px + car_w + 20}" stroke="{INK3}" stroke-width="2"/>')
    c.add(f'<rect x="{x0 - 6}" y="{cy - 6}" width="12" height="{ground - cy + 6}" fill="{INK3}"/>')
    c.add(cam_icon(x0 - 4, cy, 0.9))
    c.add(car_side(px, ground, w=car_w))
    c.add(f'<rect x="{px - 8}" y="{py - 14}" width="10" height="28" rx="2" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>')
    col = OK if angle_ok else ALERT
    c.add(f'<path d="M{x0 + 70} {cy}L{px - 8} {py}" stroke="{col}" stroke-width="3" stroke-dasharray="9 7"/>')
    ang = math.degrees(math.atan((H - h) / D))
    r = 150 if m >= 80 else 95
    a = math.radians(ang)
    c.add(f'<path d="M{x0 + 70 + r} {cy} A{r} {r} 0 0 1 {x0 + 70 + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}" fill="none" stroke="{col}" stroke-width="2.5"/>')
    c.add(f'<path d="M{x0 + 70} {cy}H{x0 + 70 + r + 30}" stroke="{INK3}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    if show_dims:
        c.add(f'<path d="M{x0 - 34} {cy}V{ground}" stroke="{BLUE}" stroke-width="2" marker-end="url(#a-blue)" marker-start="url(#a-blue)"/>')
        c.add(text(x0 - 44, (cy + ground) / 2, f"H {H:g} m".replace(".", ","), 16, 600, BLUE, FM, anchor="end"))
        c.add(f'<path d="M{x0} {ground + 26}H{px - 8}" stroke="{BLUE}" stroke-width="2" marker-end="url(#a-blue)" marker-start="url(#a-blue)"/>')
        c.add(text((x0 + px) / 2, ground + 52, f"D {D:g} m".replace(".", ","), 16, 600, BLUE, FM, anchor="middle"))
    return ang, (x0 + 70 + r + 14, cy + 34)


# ---------------------------------------------------------------- 3.svg: la geometría de una cámara bien parada
c = Canvas(K(), "Hasta 30°, 4 a 8 m y la patente de 130 a 300 px")
ang, pos = side_view(c, 150, 540, 2.5, 0.5, 5.0, m=90)
c.add(text(pos[0], pos[1], f"{ang:.0f}° (máx. 30°)", 17, 700, OK, FM))
c.add(text(560, 600, "punto donde el auto frena", 15, 500, INK2, FB, anchor="middle"))
c.add(panel(860, 130, 292, 250, "Vista de arriba", "info"))
c.add(f'<rect x="900" y="200" width="212" height="110" rx="4" fill="#E6EEF6" stroke="{INK3}" stroke-width="1.5"/>')
c.add(f'<path d="M900 255H1112" stroke="{WHITE}" stroke-width="3" stroke-dasharray="14 10"/>')
c.add(f'<circle cx="884" cy="214" r="9" fill="{DEEP}"/>')
c.add(f'<path d="M884 214L1060 226" stroke="{OK}" stroke-width="2.5" stroke-dasharray="7 6"/>')
c.add(f'<path d="M884 214L1112 214" stroke="{INK3}" stroke-width="1.5" stroke-dasharray="4 4"/>')
c.add(text(1006, 344, "un carril por cámara", 16, 600, INK, FB, anchor="middle"))
c.add(text(1006, 366, "ángulo horizontal ≤ 30°", 15, 500, INK2, FM, anchor="middle"))
c.add(Note(860, 404, 292, "Patente de 130 a 300 px de ancho; lo ideal, 150 a 200.", kind="ok", size=16))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso2: dos cálculos, uno bien y otro pasado
c = Canvas(K(2), "Calculá el ángulo con la cinta antes de fijar")
c.add(panel(48, 126, 540, 430, "Cámara a 2,5 m · auto a 5 m", "ok"))
c.add(panel(612, 126, 540, 430, "Cámara a 3 m · auto a 4 m", "alert"))
side_view(c, 120, 440, 2.5, 0.5, 5.0, m=58, angle_ok=True, show_dims=False, car_w=140)
side_view(c, 690, 440, 3.0, 0.5, 4.0, m=58, angle_ok=False, show_dims=False, car_w=140)
c.add(code(70, 470, 496, "arctan((2,5 - 0,5) / 5) = 22°", size=16, color="#7EE2B8"))
c.add(code(634, 470, 496, "arctan((3,0 - 0,5) / 4) = 32°", size=16, color="#FFB4A6"))
c.add(text(318, 534, "Bien: queda debajo de 30°", 16, 600, OK, FB, anchor="middle"))
c.add(text(882, 534, "Se pasa: alejar el punto o bajar la cámara", 16, 600, ALERT, FB, anchor="middle"))
c.add(text(600, 610, "ángulo vertical = arctan((H - h) / D)   ·   h = altura de la patente, casi siempre 0,4 a 0,6 m", 16, 500, INK2, FM, anchor="middle"))
save(c, "3-paso2.svg")

# ---------------------------------------------------------------- 3-paso4: medir la patente en píxeles
c = Canvas(K(4), "Medí la patente en píxeles sobre una captura real")
c.add(Window(48, 126, 620, 420, "Editor de imágenes · captura.jpg"))
c.add(f'<rect x="64" y="174" width="588" height="356" rx="6" fill="#1B2A38"/>')
c.add(f'<path d="M120 520 Q360 300 600 520" fill="#2E4052"/>')
c.add(plate(358, 400, "SBA 1234", w=150, size=22))
c.add(f'<rect x="283" y="400" width="150" height="50" fill="none" stroke="{CYAN}" stroke-width="2.5" stroke-dasharray="6 4"/>')
c.add(f'<path d="M283 470H433" stroke="{CYAN}" stroke-width="2.5" marker-end="url(#a-cyan)" marker-start="url(#a-cyan)"/>')
c.add(pill(358, 500, "150 px", fg=CYAN, bg="#1B2A38"))
# escala de decisión
y = 260
segs = [(720, 860, ALERT_BG, ALERT, "< 130 px", "acercar"), (860, 1040, OK_BG, OK, "130 a 300 px", "bien"), (1040, 1152, ALERT_BG, ALERT, "> 300 px", "abrir zoom")]
for x1, x2, bg, fg, lbl, act in segs:
    c.add(f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="56" fill="{bg}" stroke="{fg}" stroke-width="1.5"/>')
    c.add(text((x1 + x2) / 2, y + 24, lbl, 15, 700, fg, FM, anchor="middle"))
    c.add(text((x1 + x2) / 2, y + 46, act, 15, 500, INK2, FB, anchor="middle"))
c.add(text(720, 236, "Qué hacer según el ancho medido", 18, 600, INK, FB))
c.add(Note(720, 360, 432, "Con el auto quieto en el punto de lectura. DTK y el manual aceptan desde 100 px; Hikvision pide 130 y recomienda 150 a 200.", kind="info", size=16))
save(c, "3-paso4.svg")
