import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 8.svg: canal y ancho, después potencia
c = Canvas(K(), "Primero canal y ancho, después potencia")
c.add(panel(48, 124, 540, 380, "2.4 GHz: tres canales que no se pisan", "info"))
k = 470 / 84.0
X = lambda f: 78 + (f - 2400) * k
base, top = 400, 214
for n in range(1, 12):
    f = 2412 + 5 * (n - 1)
    if n not in (1, 6, 11):
        c.add(hump(X(f), 10 * k, base, top + 40, INK3, 1.2, 0.03))
for n, col in ((1, BLUE), (6, OK), (11, CYAN)):
    f = 2412 + 5 * (n - 1)
    c.add(hump(X(f), 10 * k, base, top, col, 3, 0.16))
c.add(hline(70, 566, base, INK3, 2))
for n in range(1, 12):
    f = 2412 + 5 * (n - 1)
    bold = n in (1, 6, 11)
    c.add(mid(X(f), base + 26, str(n), 16 if bold else 15, 700 if bold else 400, INK if bold else INK3, FM))
c.add(text(72, 470, "Solo 1, 6 y 11, siempre a 20 MHz.", 18, 600, INK, FB))
c.add(panel(612, 124, 540, 380, "5 GHz: el ancho según la interferencia", "info"))
modes = [("20 MHz", "Antiinterferencia", "mucha interferencia", "warn"),
         ("40 MHz", "Equilibrado", "buen valor de arranque", "ok"),
         ("80 MHz o más", "Alto ancho", "solo en ambiente limpio", "info")]
for i, (w_, t, d, kd) in enumerate(modes):
    y = 176 + i * 96
    c.add(panel(636, y, 492, 80, None, kd))
    c.add(text(660, y + 34, w_, 20, 600, INK, FM))
    c.add(text(660, y + 60, t, 15, 500, INK3, FB))
    c.add(text(1104, y + 47, d, 16, 500, INK2, FB, anchor="end"))
c.add(Note(48, 526, 1104, "Más potencia no es mejor: con EAP a menos de 12 m, bajala. El ejemplo oficial va de 28 a 25 dBm y prueba; 3 dB menos es la mitad de la potencia, y la celda se achica sin dejar huecos.", title="Recién ahí, potencia", kind="ok"))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso3: dos EAP con canales distintos
c = Canvas(K(3), "Dos EAP vecinos: canales distintos y potencia media")
c.add(rect(48, 124, 680, 420, WHITE, LINE2, rx=18))
c.add(text(72, 156, "Planta (EAP de techo, al centro del ambiente)", 15, 500, INK3, FM))
c.add(cell(250, 336, 175, BLUE, 0.07))
c.add(cell(526, 336, 175, OK, 0.07))
c.add(APNode(250, 320, "EAP 1", "", r=34))
c.add(APNode(526, 320, "EAP 2", "", r=34, led=OK))
c.add(f'<path d="M290 430H486" stroke="{INK3}" stroke-width="2" marker-start="url(#a-gray)" marker-end="url(#a-gray)"/>')
c.add(mid(388, 460, "10 a 12 m entre EAP", 16, 600, INK2, FB))
c.add(Step(48, 124, 3))
c.add(code(760, 124, 392, "Devices > (EAP) > Config > Radios", 14, h=40))
c.add(Table(760, 184, ["Radio", "EAP 1", "EAP 2"], [
    ["2.4 GHz", "1 · 20 MHz", "6 u 11 · 20"],
    ["5 GHz", "36 · 40 MHz", "44 o 149 · 40"],
    ["Potencia", "Medium", "Medium"],
], [110, 134, 148], row_h=46, mono_cols=(1, 2)))
c.add(Note(760, 382, 392, "Paso 4: región Uruguay en el sitio. Define qué canales y qué potencia son legales.", kind="info"))
c.add(Note(48, 566, 1104, "Canales distintos en cada vecino y la misma potencia media: cada celda se superpone apenas con la de al lado.", kind="ok"))
save(c, "8-paso3.svg")

# ---------------------------------------------------------------- 8-paso5: medir después y corregir de a un AP
c = Canvas(K(5), "Medí en los mismos tres puntos y corregí de a un AP")
c.add(Table(48, 124, ["Punto", "Antes: canal, ancho, dBm", "Después: canal, ancho, dBm"], [
    ["Punto 1", "_____", "_____"], ["Punto 2", "_____", "_____"], ["Punto 3", "_____", "_____"]], [180, 462, 462], row_h=46, mono_cols=(1, 2)))
c.add(Step(48, 124, 5))
x0, x1 = 120, 1080
c.add(text(48, 372, "Señal en el punto medido", 17, 600, INK, FB))
scale = [(-40, ""), (-50, ""), (-60, ""), (-70, ""), (-80, ""), (-90, "")]
X = lambda d: x0 + (-40 - d) / 50 * (x1 - x0)
c.add(rect(x0, 396, X(-70) - x0, 40, OK_BG, OK, rx=10))
c.add(rect(X(-70), 396, x1 - X(-70), 40, WARN_BG, WARN, rx=10))
for d, _ in scale:
    c.add(mid(X(d), 464, f"{d} dBm", 15, 600, INK2, FM))
c.add(mid((x0 + X(-70)) / 2, 422, "mejor que -70: alcanza", 16, 600, OK, FB))
c.add(mid((X(-70) + x1) / 2, 422, "por debajo de -70: subí un escalón", 16, 600, WARN, FB))
c.add(Note(48, 494, 540, "Si un punto quedó por debajo de -70 dBm, subí un escalón la potencia solo del AP que cubre ese punto, y volvé a medir.", title="De a un AP", kind="ok"))
c.add(Note(612, 494, 540, "Subir todos a High trae de vuelta la interferencia y el cliente pegado al AP lejano.", title="No todos a máximo", kind="warn"))
save(c, "8-paso5.svg")

# ---------------------------------------------------------------- 8-paso6: WLAN Optimization de madrugada
c = Canvas(K(6), "WLAN Optimization de madrugada, lejos del reinicio")
c.add(code(48, 124, 1104, "Network Config > Network Settings > WLAN > WLAN Optimization", 15, h=42))
c.add(Step(48, 124, 6))
t0, t1, X0, X1 = 0, 6, 80, 1120
TX = lambda h: X0 + (h - t0) / (t1 - t0) * (X1 - X0)
c.add(hline(X0, X1, 300, INK3, 2))
for h in range(0, 7):
    c.add(f'<path d="M{TX(h):.1f} 292V308" stroke="{INK3}" stroke-width="2"/>')
    c.add(mid(TX(h), 334, f"{h}:00", 15, 500, INK3, FM))
c.add(rect(TX(3.5), 216, TX(4.0) - TX(3.5), 64, ALERT_BG, ALERT, rx=10))
c.add(mid(TX(3.75), 204, "3:30 optimización", 16, 600, ALERT, FB))
c.add(rect(TX(2.5), 228, TX(2.75) - TX(2.5), 52, SOFT, BLUE, rx=10))
c.add(mid(TX(2.6), 204, "reinicio de AP", 16, 600, BLUE, FB))
c.add(f'<path d="M{TX(2.75):.1f} 254H{TX(3.5):.1f}" stroke="{OK}" stroke-width="2.5" marker-start="url(#a-ok)" marker-end="url(#a-ok)"/>')
c.add(mid(TX(3.12), 246, "10 min o más", 15, 600, OK, FB))
c.add(text(80, 384, "Horarios de ejemplo: lo que importa es que no coincidan.", 15, 500, INK3, FM))
c.add(Note(48, 414, 352, "Mientras escanea, los clientes se quedan sin internet varios minutos. En horario de trabajo, nunca.", title="Corta el servicio", kind="alert"))
c.add(Note(424, 414, 352, "Los AP tienen que estar conectados durante la optimización: por eso, al menos 10 minutos del reinicio.", title="Separada del reinicio", kind="warn"))
c.add(Note(800, 414, 352, "Si el resultado no convence, Optimization Record Detail > Apply Previous Settings.", title="Volver atrás", kind="ok"))
save(c, "8-paso6.svg")
