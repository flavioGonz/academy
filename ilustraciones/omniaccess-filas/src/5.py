from _fil import *


def chart(x0, y0, w, h, series, ymax=5, xlabels=()):
    out = [rect(x0, y0, w, h, WHITE, LINE2, 1.5, rx=12)]
    for v in range(0, ymax + 1):
        yy = y0 + h - 30 - (h - 80) * v / ymax
        out.append(line(x0 + 50, yy, x0 + w - 20, yy, LINE, 1))
        out.append(text(x0 + 38, yy + 5, str(v), 14, 500, INK3, FM, anchor="end"))
    for col, vals, sw, dash in series:
        n = len(vals)
        pts = []
        for i, v in enumerate(vals):
            px = x0 + 60 + (w - 90) * i / (n - 1)
            py = y0 + h - 30 - (h - 80) * v / ymax
            if pts:
                pts.append((px, pts[-1][1]))
            pts.append((px, py))
        out.append(poly(pts, stroke=col, sw=sw, dash=dash))
    return "".join(out)


# ---------- 5.svg: crudo vs estabilizado
c = Canvas("OmniAccess Filas · Lección 5", "Del aforo que parpadea al aforo estable")
raw = [2, 3, 2, 3, 3, 4, 3, 4, 2, 3, 3, 4, 3, 3, 4, 3, 3, 2, 3, 3, 4, 4, 3, 4, 4]
stable = [2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4]
c.add(chart(48, 130, 760, 360, [(WARN, raw, 3, None), (BLUE, stable, 4, None)]))
c.add(text(118, 160, "Aforo · últimos 30 min", 15, 600, INK2, FM))
c.add(rect(840, 130, 312, 360, WHITE, LINE2, 1.5, rx=12))
c.add(line(864, 172, 900, 172, WARN, 4))
c.add(text(912, 178, "Crudo (cámara)", 16, 600, WARN))
c.add(line(864, 212, 900, 212, BLUE, 4))
c.add(text(912, 218, "Estabilizado", 16, 600, BLUE))
c.add(Table(864, 250, ["Medida", "Valor"], [["Cambios por minuto", "12"], ["Rebote sugerido", "2 s"]], [190, 74], row_h=44))
c.add(text(864, 420, "más de 8 por minuto:", 15, 600, WARN, FM))
c.add(text(864, 444, "parpadea de más", 15, 600, WARN, FM))
c.add(Note(48, 520, 1104, "Calibración → Señal del aforo mide el ruido y sugiere el rebote; el rebote se escribe en la cámara desde \"Zona y rebote en la cámara\".", kind="info", size=15))
save(c, "5.svg")

# ---------- 5-paso5.svg: rebote y ventana anti doble conteo
c = Canvas("OmniAccess Filas · Lección 5 · Paso 5", "Rebote y ventana anti doble conteo, en una línea de tiempo")
# rebote
c.add(panel(48, 130, 1104, 190, "Rebote de la zona · 1 s", kind="info"))
c.add(line(100, 250, 1100, 250, INK3, 2))
c.add(rect(160, 228, 90, 44, ALERT_BG, ALERT, 2, rx=8))
c.add(text(205, 300, "0,5 s adentro", 15, 600, ALERT, FM, anchor="middle"))
c.add(text(205, 218, "no suma", 15, 600, ALERT, FM, anchor="middle"))
c.add(rect(520, 228, 420, 44, OK_BG, OK, 2, rx=8))
c.add(line(700, 228, 700, 272, OK, 3))
c.add(text(730, 300, "pasado 1 s adentro: suma 1", 15, 600, OK, FM))
c.add(text(610, 218, "persona en la zona", 15, 500, INK3, FM))
# ventana
c.add(panel(48, 345, 1104, 200, "Ventana anti doble conteo · 20 s", kind="info"))
c.add(line(100, 470, 1100, 470, INK3, 2))
for x, s, k in [(180, "entra", "ok"), (480, "sale", "gray"), (720, "vuelve a los 10 s", "warn")]:
    c.add(Chip(x, 440, s, k, anchor="middle"))
    c.add(f'<circle cx="{x}" cy="470" r="7" fill="{INK2}"/>')
c.add(rect(180, 486, 820, 20, CYAN, CYAN, 0, rx=6, opacity=.25))
c.add(text(590, 530, "dentro de la ventana: cuenta una sola entrada", 15, 600, BLUE, FM, anchor="middle"))
c.add(Step(48, 130, 5))
c.add(Note(48, 565, 1104, "Rebote alto: más estable pero más lento. Rebote bajo: más sensible pero más ruidoso. Empezá por el sugerido.", kind="warn", size=15))
save(c, "5-paso5.svg")

# ---------- 5-paso6.svg: guardar con backup y verificación
c = Canvas("OmniAccess Filas · Lección 5 · Paso 6", "Guardar en la cámara: backup, escribir, releer")
steps = [("leer la cámara", "blue"), ("guardar backup", "cyan"), ("escribir", "blue"), ("releer y comparar", "blue")]
xs = [150, 400, 640, 900]
for i, ((s_, k), x) in enumerate(zip(steps, xs)):
    c.add(Chip(x, 220, s_, k, anchor="middle"))
    if i < 3:
        w0 = len(s_) * 9.2 + 26
        w1 = len(steps[i + 1][0]) * 9.2 + 26
        c.add(Arrow((x + w0 / 2 + 8, 211), (xs[i + 1] - w1 / 2 - 10, 211), kind="flow"))
c.add(Step(48, 150, 6))
c.add(Arrow((900, 240), (700, 330), kind="ok", label="coincide", label_dy=-6))
c.add(Arrow((960, 240), (1010, 330), kind="alert", label="no coincide", label_dy=-6))
c.add(panel(450, 340, 400, 120, "Analíticas guardadas", kind="ok", sub="la cámara reinicia sus contadores"))
c.add(panel(880, 340, 272, 120, "Se restaura", kind="alert", sub="el backup anterior"))
c.add(Note(48, 340, 370, "Solo un usuario ADMIN puede guardar. Cada backup queda en \"Backups de la cámara\" (hasta 15).", kind="info", size=15))
c.add(Note(48, 500, 1104, "Guardar reinicia los contadores de la cámara: hacelo con el local tranquilo y avisá al supervisor.", kind="warn", size=15))
save(c, "5-paso6.svg")
