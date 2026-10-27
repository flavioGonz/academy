from _fil import *

# ---------- 8.svg: ley de Little aplicada a la fila
c = Canvas("OmniAccess Filas · Lección 8", "Espera = personas en la fila ÷ ritmo de salida")
c.add(panel(48, 130, 700, 300, "La fila ahora", kind="info", sub="aforo actual (canal Aforo)"))
for i in range(8):
    c.add(person(110 + i * 62, 300, BLUE, 17))
c.add(Arrow((620, 290), (700, 290), kind="ok"))
c.add(rect(696, 240, 36, 110, OK_BG, OK, 2, rx=8))
c.add(text(714, 380, "caja", 15, 600, OK, FM, anchor="middle"))
c.add(text(330, 400, "L = 8 personas", 20, 700, INK, FM, anchor="middle"))
c.add(panel(780, 130, 372, 300, "Últimos 15 minutos", kind="ok", sub="salidas (canal Salida)"))
c.add(text(966, 250, "20 salidas", 26, 700, OK, FM, anchor="middle"))
c.add(text(966, 300, "λ = 20 / 15", 18, 600, INK2, FM, anchor="middle"))
c.add(text(966, 330, "≈ 1,33 por minuto", 18, 600, INK2, FM, anchor="middle"))
c.add(rect(48, 460, 1104, 90, DEEP, DEEP, 0, rx=16))
c.add(text(600, 518, "W = L ÷ λ = 8 ÷ 1,33 ≈ 6 minutos", 28, 700, WHITE, FM, anchor="middle"))
c.add(Note(48, 572, 540, "Sin salidas en 15 minutos no hay ritmo: el kiosko muestra un guion.", kind="warn", size=15))
c.add(Note(612, 572, 540, "Vale con la fila estable; si entra más gente de la que sale, se queda corta.", kind="warn", size=15))
save(c, "8.svg")

# ---------- 8-paso2.svg: la línea de tiempo de una cámara
c = Canvas("OmniAccess Filas · Lección 8 · Paso 2", "La curva del día: cortes marcados y capturas")
x0, y0, w, h = 48, 130, 1104, 360
c.add(rect(x0, y0, w, h, WHITE, LINE2, 1.5, rx=14))
for k, lab in enumerate(["1h", "3h", "6h", "12h", "Hoy"]):
    c.add(Chip(x0 + 40 + k * 76, y0 + 42, lab, "cyan" if lab == "Hoy" else "gray", anchor="middle"))
vals = [1, 1, 2, 3, 3, 5, 6, 7, 6, 5, 4, 4, 0, 0, 3, 5, 8, 9, 7, 6, 4, 3, 2, 2]
pts = []
for i, v in enumerate(vals):
    px = x0 + 40 + (w - 80) * i / (len(vals) - 1)
    py = y0 + h - 40 - (h - 120) * v / 10
    pts.append((px, py))
seg1, seg2 = pts[:12], pts[14:]
c.add(poly(seg1, stroke=BLUE, sw=4))
c.add(poly(seg2, stroke=BLUE, sw=4))
cx0, cx1 = pts[11][0] + 10, pts[14][0] - 10
c.add(rect(cx0, y0 + 70, cx1 - cx0, h - 110, ALERT_BG, ALERT, 1.5, rx=8, opacity=.9))
c.add(text((cx0 + cx1) / 2, y0 + 100, "Corte", 15, 600, ALERT, FM, anchor="middle"))
c.add(text((cx0 + cx1) / 2, y0 + 122, "de cámara", 15, 600, ALERT, FM, anchor="middle"))
px, py = pts[17]
c.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="10" fill="{CYAN}" stroke="{WHITE}" stroke-width="3"/>')
c.add(rect(px + 24, py - 30, 220, 74, "#0B1A28", "#0B1A28", 0, rx=10))
c.add(text(px + 40, py, "captura fijada", 15, 600, WHITE, FM))
c.add(text(px + 40, py + 26, "9 personas", 15, 500, "#9FC3E3", FM))
c.add(Step(48, 130, 2))
c.add(Note(48, 510, 1104, "Tocá un punto de la curva para fijar su captura. El hueco rojo no es \"no vino nadie\": la cámara estuvo sin conexión.", kind="info", size=15))
save(c, "8-paso2.svg")

# ---------- 8-paso3.svg: el kiosko de sala
c = Canvas("OmniAccess Filas · Lección 8 · Paso 3", "El cartel de sala cambia con el límite de la fila")
cards = [("PASE", "Hay lugar disponible", OK, OK_BG, "menos del 70 %"), ("AGUARDE", "Fila moderada", WARN, WARN_BG, "desde el 70 %"), ("AFORO COMPLETO", "Por favor espere su turno", ALERT, ALERT_BG, "desde el 100 %")]
for i, (t, s, col, bg, cond) in enumerate(cards):
    x = 48 + i * 376
    c.add(rect(x, 140, 352, 300, bg, col, 3, rx=18))
    c.add(text(x + 176, 250, t, 30 if len(t) < 10 else 26, 700, col, FD, anchor="middle"))
    c.add(text(x + 176, 290, s, 17, 500, INK2, FB, anchor="middle"))
    c.add(line(x + 30, 330, x + 322, 330, col, 1))
    c.add(text(x + 30, 370, "Personas en fila", 15, 500, INK3, FM))
    c.add(text(x + 30, 410, "Espera estimada", 15, 500, INK3, FM))
    c.add(text(x + 322, 370, ["3 / 8", "6 / 8", "8 / 8"][i], 17, 700, INK, FM, anchor="end"))
    c.add(text(x + 322, 410, ["~2 min", "~5 min", "~7 min"][i], 17, 700, INK, FM, anchor="end"))
    c.add(Chip(x + 176, 480, cond, "gray", anchor="middle"))
c.add(Step(48, 140, 3))
c.add(Note(48, 520, 1104, "Con varias filas, el botón de lista elige cuál mostrar y la dirección queda con ?device= y el id. Se actualiza cada 5 s.", kind="info", size=15))
save(c, "8-paso3.svg")
