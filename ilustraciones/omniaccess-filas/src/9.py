from _fil import *

# ---------- 9.svg: una alerta, varios avisos
c = Canvas("OmniAccess Filas · Lección 9", "Una alerta de aforo llega por cuatro lados")
src = c.add(Generic(48, 270, "Aforo ≥ umbral", "Fila Caja 1 · 9 / 8", icon="warn", w=300, hl=ALERT))
outs = [
    (150, "Recuadro en el panel", "Alerta de aforo · video", "laptop"),
    (260, "Supervisor", "Telegram o WhatsApp · foto o clip", "phone"),
    (370, "App de filas", "notificación push", "bell"),
    (480, "Escalamiento", "si sigue 5 min sobre el umbral", "shield"),
]
for y, t, s, ic in outs:
    b = c.add(Generic(660, y, t, s, icon=ic, w=492, hl=ALERT if t == "Escalamiento" else None))
    c.add(Arrow(src.right(), b.left(), kind="alert" if t == "Escalamiento" else "flow"))
c.add(Note(48, 420, 400, "Primero mirá la imagen: el carro abandonado o alguien agachado también suman.", title="Antes de actuar", kind="warn", size=15))
save(c, "9.svg")

# ---------- 9-paso2.svg: cómo atender
c = Canvas("OmniAccess Filas · Lección 9 · Paso 2", "Atender la alerta: mirar, decidir, registrar")
c.add(rect(48, 130, 360, 270, WHITE, ALERT, 3, rx=16))
c.add(rect(48, 130, 360, 44, ALERT_BG, ALERT_BG, 0, rx=16))
c.add(text(70, 160, "ALERTA DE AFORO", 16, 700, ALERT, FM, ls=1.2))
c.add(rect(68, 186, 320, 150, "#0B1A28", "#0B1A28", 0, rx=10))
c.add(Chip(300, 216, "Excede umbral", "alert", anchor="middle"))
c.add(text(370, 320, "9 / 8", 24, 700, ALERT, FM, anchor="end"))
c.add(text(68, 362, "Acción requerida: verificá en vivo", 15, 500, INK2, FB))
c.add(text(68, 384, "y abrí otra caja o despejá la zona.", 15, 500, INK2, FB))
c.add(Step(48, 130, 2))
q = c.add(Box(500, 200, 260, 80, "¿Cola real?", "mirá el video", hl=CYAN))
c.add(Arrow((408, 260), (500, 240), kind="flow"))
y1 = c.add(Box(860, 140, 292, 80, "Sí: abrir caja", "o reordenar la fila", hl=OK))
n1 = c.add(Box(860, 270, 292, 80, "No: anotar", "carro, reflejo → calibrar", hl=WARN))
c.add(Arrow(q.right(-14), y1.left(), kind="ok"))
c.add(Arrow(q.right(14), n1.left(), kind="flow"))
c.add(Box(500, 420, 652, 80, "Silenciar o descartar", "la cruz cierra el recuadro; vuelve si la fila baja y sube"))
c.add(Note(48, 430, 420, "Si llega una alerta de salud (cámara tapada, muy clara u oscura), el número no es confiable.", kind="alert", size=15))
save(c, "9-paso2.svg")

# ---------- 9-paso6.svg: el corte de cámara
c = Canvas("OmniAccess Filas · Lección 9 · Paso 6", "Un corte de cámara queda registrado con su duración")
ty = 300
c.add(line(80, ty, 1120, ty, INK3, 2))
pts = [(140, "sondeo ok", "ok"), (330, "falla 1", "warn"), (470, "falla 2", "alert"), (860, "vuelve", "ok")]
for x, s, k in pts:
    c.add(f'<circle cx="{x}" cy="{ty}" r="8" fill="{ {"ok": OK, "warn": WARN, "alert": ALERT}[k] }"/>')
    c.add(Chip(x, ty - 30, s, k, anchor="middle"))
c.add(rect(470, ty + 20, 390, 40, ALERT_BG, ALERT, 2, rx=10))
c.add(text(665, ty + 46, "corte abierto: guarda el último aforo", 15, 600, ALERT, FM, anchor="middle"))
c.add(rect(860, ty + 20, 260, 40, OK_BG, OK, 2, rx=10))
c.add(text(990, ty + 46, "cierra con la duración", 15, 600, OK, FM, anchor="middle"))
c.add(Step(48, 150, 6))
c.add(text(80, 200, "Desconectá la cámara unos 30 s y volvé a conectarla.", 18, 500, INK))
c.add(Note(48, 420, 540, "Monitor en Vivo: tocá la cámara y buscá la marca \"Corte de cámara\" en la curva de hoy.", kind="info", size=15))
c.add(Note(612, 420, 540, "Reportes: la tabla \"Cortes de conexión de cámara\" explica los huecos del período.", kind="info", size=15))
save(c, "9-paso6.svg")
