import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 4.svg: de dónde viene y a dónde va la energía
c = Canvas(K(), "Energía: lo que entra, lo que cuelga y lo que aguanta")
c.add(NOLIG)
tr = c.add(Generic(48, 140, "Transformador", "16,5 Vac · 40 VA mín.", icon="bolt", w=290))
bt = c.add(Generic(48, 290, "Batería", "12 V · 7 Ah (4 Ah en SP+)", icon="bolt", w=340))
ce = c.add(Box(470, 180, 250, 190, "Central", "SP+ o MG", dark=True, icon=ICON["shield"]))
au = c.add(Generic(822, 140, "AUX", "teclados, módulos y sensores", icon="bolt", w=330))
be = c.add(Generic(822, 290, "BELL", "sirena 12 V o 1 kΩ", icon="bell", w=330))
c.add(Cable(tr.right(), ce.left(-40), kind="power+", label="AC"))
c.add(Cable(bt.right(), ce.left(40), kind="power+", label="BAT"))
c.add(Cable(ce.right(-40), au.left(), kind="power+"))
c.add(Cable(ce.right(40), be.left(), kind="power+"))
c.add(text(48, 254, "en un toma sin llave", 15, 600, WARN, FB))
c.add(text(48, 404, "al revés, quema el fusible", 15, 600, ALERT, FB))
c.add(text(822, 254, "SP5500+: hasta 700 mA en total", 15, 600, WARN, FB))
c.add(text(822, 404, "corta si pasa de 3 A", 15, 500, INK3, FB))
# escala de batería
c.add(text(48, 470, "BATERÍA EN SP+ (sin red)", 14, 600, INK3, FM, ls=1.5))
x0, x1 = 120, 1100
V = lambda v: x0 + (12.5 - v) / (12.5 - 8.0) * (x1 - x0)
c.add(f'<rect x="{x0}" y="490" width="{V(10.5) - x0:.0f}" height="26" rx="6" fill="{OK_BG}" stroke="{OK}"/>')
c.add(f'<rect x="{V(10.5):.0f}" y="490" width="{V(8.5) - V(10.5):.0f}" height="26" fill="{WARN_BG}" stroke="{WARN}"/>')
c.add(f'<rect x="{V(8.5):.0f}" y="490" width="{x1 - V(8.5):.0f}" height="26" rx="6" fill="{ALERT_BG}" stroke="{ALERT}"/>')
for v, lab, col in [(10.5, "10,5 V · falla de batería", WARN), (9.1, "9,1 V · desconexión de protección", WARN), (8.5, "8,5 V · se apaga", ALERT)]:
    x = V(v)
    c.add(vline(x, 482, 540, col, 3))
    c.add(text(x, 562, lab, 15, 600, col, FB, anchor="middle" if v != 8.5 else "start"))
c.add(text(x0, 510, "12 V", 15, 600, OK, FM))
c.add(text(48, 620, "Si AUX corta por sobrecarga: sacá todas las cargas al menos 10 segundos antes de reconectar.", 16, 500, INK2, FB))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso2: la suma del auxiliar
c = Canvas(K(2), "Sumá el auxiliar antes de energizar")
c.add(NOLIG)
items = [("K32LCD+ × 2", 172, BLUE), ("TM70 + zumbador", 330, CYAN), ("ZX8", 31, INK3), ("IP150+", 100, NAVY)]
X0, W, MAX = 60, 1000, 800
px = lambda ma: X0 + ma / MAX * W
x = X0
c.add(text(60, 150, "Ejemplo con la tabla de consumos máximos de la guía SP+", 17, 600, INK2, FB))
for name, ma, col in items:
    w = ma / MAX * W
    c.add(f'<rect x="{x:.1f}" y="180" width="{w:.1f}" height="64" fill="{col}" stroke="{WHITE}" stroke-width="2"/>')
    if w > 80:
        c.add(mid(x + w / 2, 208, name, 15, 600, WHITE, FB))
        c.add(mid(x + w / 2, 232, f"{ma} mA", 15, 600, WHITE, FM))
    x += w
c.add(text(px(31 + 172 + 330 + 100) - 70, 272, "ZX8 31", 14, 600, INK3, FM))
c.add(f'<rect x="{x:.1f}" y="180" width="{px(700) - x:.1f}" height="64" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2" stroke-dasharray="6 4"/>')
c.add(vline(px(700), 160, 300, ALERT, 3))
c.add(text(px(700) + 8, 176, "700 mA", 16, 700, ALERT, FM))
c.add(text(px(700) + 8, 196, "SP5500+", 15, 500, ALERT, FB))
c.add(text(60, 330, "Suma sin detectores: 633 mA. Quedan 67 mA para 6 detectores: unos 11 mA cada uno.", 18, 600, INK, FB))
c.add(Step(44, 180, 2))
c.add(Note(48, 370, 540, "Si los detectores consumen más de lo que queda, parte de las cargas va a una fuente auxiliar aparte. Lo que alimenta una fuente externa no cuenta en el AUX.", title="Si te pasás", kind="warn"))
c.add(Note(612, 370, 540, "Cada placa tiene su máximo de auxiliar: la guía lista 1000\u00a0mA para la SP6000+ y 1500\u00a0mA para la SP7000+. Los sensores, de la hoja de su fabricante.", title="Mirá tu central", kind="info"))
c.add(text(48, 540, "Las PGM alimentadas del AUX y los teclados con zumbador también entran en la cuenta.", 16, 500, INK2, FB))
save(c, "4-paso2.svg")

# ---------------------------------------------------------------- 4-paso3: autonomía
c = Canvas(K(3), "¿Cuántas horas aguanta sin red?")
c.add(NOLIG)
c.add(Step(48, 140, 3))
c.add(rect(80, 140, 1072, 120, WHITE, LINE2, rx=16))
c.add(text(110, 214, "horas  =  Ah de la batería  ÷  ( central + suma AUX, en amperes )", 24, 600, INK, FM))
ex = [("Ejemplo EVOHD+", "7 Ah ÷ (0,100 + 0,130 A)", "≈ 30 h", "ok"), ("Tabla del manual EVOHD+", "17 Ah ÷ (0,100 + 0,470 A)", "≈ 30 h", "ok")]
for i, (t, f, r, kd) in enumerate(ex):
    x = 48 + i * 564
    c.add(panel(x, 300, 540, 170, t, "info"))
    c.add(text(x + 24, 384, f, 20, 600, INK2, FM))
    c.add(text(x + 24, 444, r, 32, 700, OK, FD))
c.add(Note(48, 500, 1104, "Es una cuenta aproximada: la batería pierde capacidad con los años y el consumo sube cuando suena todo. Si la cuenta da corta, batería más grande o menos carga en el AUX.", title="Margen", kind="warn"))
save(c, "4-paso3.svg")

# ---------------------------------------------------------------- 4-paso4: 1 kΩ en BELL
c = Canvas(K(4), "Sin sirena, 1 kΩ entre BELL+ y BELL−")
c.add(NOLIG)
sv, an = strip(80, 150, ["BELL+", "BELL−"], pitch=110, title="CENTRAL · SALIDA DE CAMPANA", hl={"BELL+": RED, "BELL−": BLACK})
c.add(sv)
(x1, y1), (x2, y2) = an["BELL+"], an["BELL−"]
c.add(f'<path d="M{x1} {y1}V{y1 + 90}H{x1 + 20}" stroke="{INK}" stroke-width="3" fill="none"/>')
c.add(resistor(x1 + 20, y1 + 90, x2 - 20, "1 kΩ", INK, lab_dy=36, body=50))
c.add(f'<path d="M{x2 - 20} {y1 + 90}H{x2}V{y2}" stroke="{INK}" stroke-width="3" fill="none"/>')
c.add(f'<circle cx="{x1}" cy="{y1}" r="5" fill="{INK}"/><circle cx="{x2}" cy="{y2}" r="5" fill="{INK}"/>')
c.add(Step(64, 240, 4))
c.add(panel(420, 140, 340, 150, "Sin nada en BELL", "warn"))
c.add(tag(470, 238, "TBL 3", "warn", 17)); c.add(text(530, 238, "campana desconectada", 16, 600, INK, FB))
c.add(panel(812, 140, 340, 150, "Con 1 kΩ", "ok"))
c.add(text(836, 238, "la falla de campana desaparece", 16, 600, OK, FB))
c.add(Arrow((764, 215), (808, 215), kind="ok"))
c.add(Note(48, 380, 540, "Con sirena: + al BELL+ y − al BELL−. La salida da 12 V en alarma: una sirena de 30 W o dos de 20 W, y corta si pasa de 3 A.", title="Cuando hay sirena", kind="info"))
c.add(Note(612, 380, 540, "Con la central en batería, medí con el tester: menos de 10,5 V es falla y a 8,5 V se apaga (paso 5). Y antes de cerrar, polaridad de la batería.", title="Después, medí la batería", kind="warn"))
save(c, "4-paso4.svg")
