import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *


def reliability(x, y, w, h, vals, low, labels=None):
    """Gráfico genérico de índice de confiabilidad (1 a 10) por día."""
    out = [rect(x, y, w, h, WHITE, LINE2, rx=12)]
    n = len(vals)
    cw = (w - 60) / n
    for k in (1, 5, 10):
        yy = y + 20 + (10 - k) / 9 * (h - 80)
        out.append(hline(x + 40, x + w - 16, yy, LINE, 1))
        out.append(text(x + 30, yy + 5, str(k), 14, 500, INK3, FM, anchor="end"))
    pts = []
    for i, v in enumerate(vals):
        cx = x + 48 + cw * (i + 0.5)
        pts.append((cx, y + 20 + (10 - v) / 9 * (h - 80)))
        if i == low:
            out.append(f'<rect x="{cx - cw / 2 + 2:.0f}" y="{y + 8}" width="{cw - 4:.0f}" height="{h - 16}" rx="8" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/>')
        if labels:
            out.append(text(cx, y + h - 22, labels[i], 13, 500, INK3, FM, anchor="middle"))
    d = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
    for px, py in pts:
        out.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="4.5" fill="{BLUE}"/>')
    return "".join(out), pts


# ---------------------------------------------------------------- 9.svg: qué cambió, quién reinició
c = Canvas(K(), "Ante una falla: primero qué cambió, después quién")
c.add(NOLIG)
c.add(text(48, 146, "Monitor de confiabilidad · perfmon /rel", 17, 600, INK, FM))
sv, pts = reliability(48, 160, 640, 250, [10, 10, 9.6, 9.8, 3.2, 3.8, 4.5], 4, ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"])
c.add(sv)
c.add(text(48, 440, "Ese día, en la misma columna:", 16, 600, INK2, FB))
c.add(tag(48, 476, "instalación: aplicación nueva", "info", anchor="start", mono=False))
c.add(tag(330, 476, "falla de aplicación", "alert", anchor="start", mono=False))
c.add(text(48, 516, "Dibujo genérico: el índice va de 1 a 10 por día.", 15, 400, INK3, FB))
c.add(panel(720, 128, 432, 190, None, "info"))
c.add(text(744, 172, "1074", 30, 700, BLUE, FM))
c.add(text(840, 168, "quién pidió el reinicio", 17, 600, INK, FB))
svg, _ = wrap(744, 210, "Un usuario, el servicio de Windows Update como SYSTEM o un programa: queda escrito con fecha y hora.", 390, 16, 400, INK2)
c.add(svg)
c.add(panel(720, 336, 432, 190, None, "alert"))
c.add(text(744, 380, "6008", 30, 700, ALERT, FM))
c.add(text(840, 376, "apagado inesperado", 17, 600, ALERT, FB))
svg, _ = wrap(744, 418, "Nadie lo pidió: corte de luz o pantallazo azul. Se lee junto con lo que pasó antes.", 390, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 552, 1104, "Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} filtra en el origen: mucho más rápido que traer todo y filtrar con Where-Object.", kind="ok"))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso1: dónde mirar en Confiabilidad
c = Canvas(K(1), "Buscá el día con el índice más bajo y qué se instaló")
c.add(NOLIG)
c.add(Step(65, 141, 1))
c.add(text(94, 147, "Win+R · perfmon /rel · vista por semanas", 17, 600, INK2, FM))
c.add(rect(48, 172, 1104, 450, WHITE, LINE2, rx=14))
c.add(f'<path d="M48 186a14 14 0 0 1 14 -14h1076a14 14 0 0 1 14 14v26h-1104z" fill="{SOFT}"/>')
c.add(text(68, 200, "Monitor de confiabilidad (dibujo genérico)", 15, 600, INK2, FB))
for i, t in enumerate(["Días", "Semanas"]):
    c.add(rect(880 + i * 130, 182, 120, 26, CYAN if i else WHITE, CYAN if i else LINE2, rx=13, sw=1.5))
    c.add(mid(940 + i * 130, 200, t, 14, 600, WHITE if i else INK2, FB))
sv, pts = reliability(68, 228, 760, 200, [9.8, 10, 9.4, 3.1, 4.2, 5.0, 5.8, 6.4], 3, ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"])
c.add(sv)
rows = [("Fallas de aplicaciones", 3, "alert"), ("Fallas de Windows", None, None), ("Información: instalaciones y actualizaciones", 3, "info")]
cw = (760 - 60) / 8
for i, (t, col, kd) in enumerate(rows):
    y = 452 + i * 40
    c.add(hline(68, 828, y + 14, LINE, 1))
    c.add(text(68, y + 6, t, 15, 500, INK2, FB))
    if col is not None:
        cx = 68 + 48 + cw * (col + 0.5)
        if kd == "alert":
            c.add(Mark(cx, y, ok=False))
        else:
            c.add(f'<circle cx="{cx:.0f}" cy="{y}" r="14" fill="{SOFT}" stroke="{BLUE}" stroke-width="2"/>' + text(cx, y + 6, "i", 17, 700, BLUE, FD, anchor="middle"))
c.add(Note(856, 232, 276, "La semana donde el índice se desploma, mirá qué se instaló: ahí suele estar el cambio.", title="Qué buscar", kind="warn"))
c.add(Note(856, 430, 276, "Guardar historial de confiabilidad: el XML va adjunto al informe (paso 6).", kind="info"))
save(c, "9-paso1.svg")

# ---------------------------------------------------------------- 9-paso4: anatomía del filtro
c = Canvas(K(4), "Un filtro dice qué log, qué nivel y desde cuándo")
c.add(NOLIG)
c.add(Step(65, 141, 4))
c.add(text(94, 147, "Errores y críticos del log Sistema de las últimas 24 horas", 17, 600, INK2, FB))
c.add(code(48, 176, 1104, "Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddHours(-24)}", 15, h=50))
parts = [(250, "LogName='System'", "qué log", "System, Application…"), (520, "Level=1,2", "qué nivel", "1 crítico · 2 error"), (850, "StartTime=…", "desde cuándo", "las últimas 24 horas")]
for x, p, t, s in parts:
    c.add(arrow((x, 230), (x, 280), "flow"))
    c.add(panel(x - 125, 284, 250, 116, None, "info"))
    c.add(text(x - 105, 318, p, 16, 600, BLUE, FM))
    c.add(text(x - 105, 348, t, 17, 600, INK, FD))
    c.add(text(x - 105, 376, s, 15, 400, INK3, FB))
c.add(panel(48, 428, 540, 130, None, "ok"))
c.add(text(72, 466, "FilterHashtable", 18, 600, OK, FM))
svg, _ = wrap(72, 500, "El servicio de registro devuelve solo lo que coincide: rápido aunque el log sea grande.", 490, 16, 400, INK2)
c.add(svg)
c.add(panel(612, 428, 540, 130, None, "warn"))
c.add(text(636, 466, "… | Where-Object", 18, 600, WARN, FM))
svg, _ = wrap(636, 500, "Trae todos los eventos a PowerShell y recién ahí filtra: con logs grandes tarda mucho más.", 490, 16, 400, INK2)
c.add(svg)
save(c, "9-paso4.svg")
