import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 8.svg: evento, PGM, relé, carga
c = Canvas(K(), "La PGM manda, el relé carga")
c.add(NOLIG)
ev = c.add(Box(48, 150, 300, 110, "Evento", "grupo, subgrupo, part.", icon=ICON["bell"]))
pg = c.add(Box(420, 150, 220, 110, "PGM de la placa", "100 a 150 mA", dark=True, icon=ICON["bolt"]))
rl = c.add(Relay(706, 150, "Relé externo", "bobina 12 V"))
ld = c.add(Generic(950, 160, "Carga", "portón o luz", icon="door", w=202))
c.add(Arrow(ev.right(), pg.left(), label="activa"))
c.add(Cable(pg.right(), rl.left(), kind="relay", label="bobina"))
c.add(Cable(rl.right(), ld.left(), kind="relay"))
c.add(panel(48, 300, 540, 190, "Se apaga de dos formas", "info"))
c.add(bullet_list(72, 364, [("Evento de desactivación: por ejemplo, la falla de AC que se restaura.", "info"),
                             ("Tiempo: [281] a [296], 5 s de fábrica. Un pulso para el portón.", "info")], 496, 16)[0])
c.add(panel(612, 300, 540, 190, "De fábrica", "info"))
c.add(bullet_list(636, 364, [("PGM1: botón B de cualquier control (08/99/99).", "info"), ("PGM2: botón C.", "info"),
                              ("Partición 01, 02 o 99 para ambas.", "info")], 496, 16)[0])
c.add(Note(48, 514, 1104, "La PGM solo mueve la bobina de un relé. Un portón, una luz o una sirena extra van por el contacto del relé, nunca directo a la placa.", title="Baja corriente", kind="warn"))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso1: cableado del portón
c = Canvas(K(1), "PGM1 a la bobina, contacto seco al pulsador del portón")
c.add(NOLIG)
sv, an = strip(60, 140, ["AUX+", "PGM1"], pitch=100, title="CENTRAL", hl={"AUX+": RED})
c.add(sv)
rl = c.add(Relay(440, 300, "Relé 12 V", "bobina < 100 mA"))
c.add(rect(840, 300, 312, 150, WHITE, LINE2, rx=14))
c.add(text(860, 332, "Placa del portón", 18, 600, INK))
c.add(text(860, 356, "bornes del pulsador (según la placa)", 15, 400, INK3, FB))
sv, an2 = strip(880, 368, ["puls.", "puls. "], pitch=90, above=False)
c.add(sv)
(ax, ay), (px, py) = an["AUX+"], an["PGM1"]
c.add(wire([(ax, ay), (ax, 270), (500, 270), (500, 300)], "power+"))
c.add(wire([(px, py), (px, 250), (600, 250), (600, 300)], "relay"))
c.add(text(470, 292, "+", 16, 700, RED, FM)); c.add(text(608, 292, "PGM", 14, 600, CYAN, FM))
(cx_, cy_), (nx, ny) = rl.port("COM"), rl.port("NO")
c.add(wire([(cx_, cy_), (cx_, 500), (an2[1][0], 500), (an2[1][0], an2[1][1])], "relay"))
c.add(wire([(nx, ny), (nx, 480), (an2[0][0], 480), (an2[0][0], an2[0][1])], "relay"))
c.add(text(700, 470, "contacto seco: COM y NO", 15, 600, CYAN, FB, anchor="middle"))
c.add(Step(44, 210, 1))
c.add(Note(48, 300, 360, "El puente PGM de la placa elige si la PGM da negativo o +12 V. Dibujo con PGM a negativo y bobina al AUX+: mirá tu placa.", kind="warn", size=15))
c.add(code(48, 540, 520, "[281] 002   PGM1: pulso de 2 s", 16, h=42))
c.add(code(612, 540, 540, "[220] 06 08 01   prueba con tecla de utilidad 1", 16, h=42))
c.add(text(48, 620, "Probalo con el motor desconectado: un portón que abre por la alarma es un riesgo físico.", 16, 600, ALERT, FB))
save(c, "8-paso1.svg")

# ---------------------------------------------------------------- 8-paso2: luz de falla de AC
c = Canvas(K(2), "Luz de falla de AC: se prende con un evento, se apaga con otro")
c.add(NOLIG)
X0, X1, Y = 80, 1120, 300
c.add(f'<path d="M{X0} {Y}H{X1}" stroke="{INK3}" stroke-width="3" marker-end="url(#a-gray)"/>')
evs = [(110, "Corte de red", "TBL 2.2 ya se ve", INK2), (420, "Pasa el retardo [839]", "15 min de fábrica · 1 en el banco", WARN),
       (720, "Vuelve la red", "falla restaurada", INK2)]
for x, t, s, col in evs:
    c.add(f'<circle cx="{x}" cy="{Y}" r="9" fill="{col}"/>')
    c.add(text(x, Y - 48, t, 17, 600, INK, FB, anchor="middle" if x > 110 else "start"))
    c.add(text(x, Y - 24, s, 15, 500, col, FB, anchor="middle" if x > 110 else "start"))
c.add(f'<rect x="420" y="{Y + 30}" width="300" height="44" rx="10" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/>')
c.add(mid(570, Y + 58, "PGM2 encendida: luz prendida", 16, 700, WARN, FB))
c.add(f'<rect x="110" y="{Y + 30}" width="300" height="44" rx="10" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(mid(260, Y + 58, "luz apagada", 16, 600, INK3, FB))
c.add(f'<rect x="730" y="{Y + 30}" width="390" height="44" rx="10" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(mid(925, Y + 58, "luz apagada, sola", 16, 600, OK, FB))
c.add(code(48, 140, 520, "[222] 44 01 99   activación: nueva falla, AC", 15, h=40))
c.add(code(612, 140, 540, "[223] 45 01 99   desactivación: AC restaurada", 15, h=40))
c.add(Step(48, 140, 2))
c.add(Note(48, 420, 540, "Con [282] en 000, la PGM2 no tiene tiempo: queda prendida hasta el evento de desactivación.", title="Sin temporizador", kind="info"))
c.add(Note(612, 420, 540, "Bajá [839] a 001 solo para probar. Al terminar, devolvelo al valor acordado con la empresa de monitoreo (paso 5).", title="El retardo, de vuelta", kind="warn"))
save(c, "8-paso2.svg")
