import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *


def cam_view(c, x, y, w, h, zone, line_y, title="Calibrar ANPR · en vivo", zone_ok=True, extra=None):
    """Vista esquemática de la cámara: calzada en perspectiva, zona de lectura y línea de captura."""
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#14222F"/>')
    c.add(text(x + 16, y + 28, title, 14, 600, "#9FC3E3", FM, ls=1.2))
    # calzada en perspectiva
    c.add(f'<path d="M{x + w * 0.38} {y + 50} L{x + w * 0.62} {y + 50} L{x + w * 0.95} {y + h} L{x + w * 0.05} {y + h} Z" fill="#2E4052"/>')
    c.add(f'<path d="M{x + w * 0.5} {y + 60} L{x + w * 0.5} {y + h}" stroke="#C2D4E6" stroke-width="3" stroke-dasharray="16 14"/>')
    if extra:
        c.add(extra)
    col = CYAN if zone_ok else ALERT
    pts = " ".join(f"{px:.0f},{py:.0f}" for px, py in zone)
    c.add(f'<polygon points="{pts}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="3" stroke-dasharray="10 6"/>')
    for px, py in zone:
        c.add(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="{WHITE}" stroke="{col}" stroke-width="3"/>')
    c.add(f'<path d="M{zone[3][0]:.0f} {line_y}H{zone[2][0]:.0f}" stroke="{OK}" stroke-width="4"/>')


# ---------------------------------------------------------------- 6.svg: zona, línea y perfil
c = Canvas(K(), "Zona sobre el carril, línea de captura y perfil nocturno")
X, Y, W, H = 48, 132, 600, 440
zone = [(X + 300, Y + 150), (X + 420, Y + 150), (X + 520, Y + 410), (X + 300, Y + 410)]
cam_view(c, X, Y, W, H, zone, Y + 330)
c.add(plate(X + 410, Y + 290, "SBA 1234", w=110, size=17))
c.add(pill(X + 160, Y + 214, "Carril 1", fg=CYAN, bg="#14222F"))
c.add(pill(X + 150, Y + 336, "Línea de captura", fg=OK, bg="#14222F"))
c.add(panel(680, 132, 472, 440, "Perfil ANPR barrio-noche", "dark", sub="20 a 30 km/h, faros de frente"))
perfil = [("Obturador", "1/500"), ("Anti-brillo de patente", "60"), ("WDR", "apagado"), ("HLC", "apagado"), ("Ganancia máxima", "40"), ("Filtro IR", "automático"), ("Iluminador IR", "auto"), ("Foco", "semiautomático")]
for i, (k, v) in enumerate(perfil):
    yy = 230 + i * 40
    c.add(text(704, yy, k, 17, 500, WHITE, FB))
    c.add(text(1128, yy, v, 17, 600, CYAN, FM, anchor="end"))
c.add(text(704, 552, "Solo Hikvision · reversible", 15, 500, "#9FC3E3", FM))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso1: la tasa por hora
c = Canvas(K(1), "Mirá la tasa de lectura por hora, no el promedio")
vals = [62, 60, 58, 64, 70, 84, 93, 97, 98, 98, 99, 98, 98, 97, 98, 98, 97, 96, 93, 88, 86, 80, 72, 66]
labels = [f"{h:02d}h" for h in range(24)]
c.add(text(48, 150, "Tasa de lectura ANPR · P1 - Entrada (21) · últimos 7 días", 17, 600, INK, FB))
c.add(bars(60, 180, 760, 300, vals, labels, label_every=3))
c.add(text(830, 186, "100 %", 14, 500, INK3, FM))
c.add(text(830, 200 + 300 * 0.05, "95 %", 14, 600, OK, FM))
c.add(text(830, 180 + 300 * 0.15 + 4, "85 %", 14, 600, ALERT, FM))
c.add(panel(900, 140, 252, 210, "Tasa global", "info"))
c.add(text(920, 236, "91 %", 44, 700, INK, FD))
c.add(text(920, 270, "parece aceptable...", 16, 500, INK2, FB))
c.add(text(920, 300, "de 00 a 04 h: ~60 %", 16, 600, ALERT, FM))
c.add(Note(900, 372, 252, "Dónde está: Dispositivos → vista Cámaras LPR → Tasa de lectura.", kind="info", size=15))
c.add(text(60, 560, "Verde: más de 95 % · ámbar: 85 a 95 % · rojo: menos de 85 % (emplazamiento o luz)", 16, 500, INK2, FB))
save(c, "6-paso1.svg")

# ---------------------------------------------------------------- 6-paso2: zona de más contra zona justa
c = Canvas(K(2), "Achicá la zona de lectura al carril real")
X1, Y1, W1, H1 = 48, 140, 540, 380
big = [(X1 + 30, Y1 + 70), (X1 + 510, Y1 + 70), (X1 + 520, Y1 + 360), (X1 + 20, Y1 + 360)]
cartel = f'<rect x="{X1 + 40}" y="{Y1 + 90}" width="110" height="46" rx="4" fill="#C2D4E6"/>' + text(X1 + 95, Y1 + 120, "CAUTION", 15, 700, INK, FM, anchor="middle")
cam_view(c, X1, Y1, W1, H1, big, Y1 + 300, title="ZONA DE MÁS", zone_ok=False, extra=cartel)
X2 = 612
small = [(X2 + 287, Y1 + 120), (X2 + 345, Y1 + 120), (X2 + 460, Y1 + 340), (X2 + 292, Y1 + 340)]
cam_view(c, X2, Y1, W1, H1, small, Y1 + 280, title="ZONA JUSTA", zone_ok=True)
c.add(tag(48, 566, "lee carteles y autos de la calle", "alert", size=16))
c.add(tag(612, 566, "solo el carril: menos lecturas falsas", "ok", size=16))
c.add(text(48, 620, "Arrastrá los puntos, dejá la línea donde la patente se ve derecha y tocá Guardar línea de captura → Sí, guardar.", 16, 500, INK2, FB))
save(c, "6-paso2.svg")
