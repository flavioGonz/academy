import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *


def loop(x, y, state, eol=True):
    """Lazo de zona NC: bornes Z y COM a la izquierda, contacto y resistencia a la derecha. Alto 150."""
    out = []
    out.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#CBD5DF" stroke="{INK3}" stroke-width="1.5"/>')
    out.append(f'<circle cx="{x}" cy="{y + 110}" r="9" fill="#CBD5DF" stroke="{INK3}" stroke-width="1.5"/>')
    out.append(text(x - 16, y + 6, "Z", 15, 700, INK, FM, anchor="end"))
    out.append(text(x - 16, y + 116, "COM", 15, 700, INK, FM, anchor="end"))
    cut = state == "open"
    out.append(f'<path d="M{x + 9} {y}H{x + 70}" stroke="{BLUE}" stroke-width="3" fill="none"/>')
    out.append(contact(x + 70, y, closed=not cut, w=70))
    out.append(f'<path d="M{x + 140} {y}H{x + 230}V{y + 30}" stroke="{BLUE}" stroke-width="3" fill="none"/>')
    if eol:
        out.append(resistor(x + 230, y + 30, y + 90, "1 kΩ", BLUE, vertical=True, body=44))
    else:
        out.append(f'<path d="M{x + 230} {y + 30}V{y + 90}" stroke="{BLUE}" stroke-width="3"/>')
    out.append(f'<path d="M{x + 230} {y + 90}V{y + 110}H{x + 9}" stroke="{BLUE}" stroke-width="3" fill="none"/>')
    if state == "short":
        out.append(f'<path d="M{x + 40} {y}V{y + 110}" stroke="{ALERT}" stroke-width="4"/>')
        out.append(f'<circle cx="{x + 40}" cy="{y}" r="5" fill="{ALERT}"/><circle cx="{x + 40}" cy="{y + 110}" r="5" fill="{ALERT}"/>')
        out.append(text(x + 48, y + 64, "corto", 15, 700, ALERT, FM))
    return "".join(out)


# ---------------------------------------------------------------- 3.svg: tres estados que ve la central
c = Canvas(K(), "Con 1 kΩ al final, la central ve tres estados")
c.add(NOLIG)
cols = [("Normal", "contacto cerrado", "normal", "ve 1 kΩ", "ok", "Zona cerrada, todo bien"),
        ("Abierta", "puerta abierta o cable cortado", "open", "ve circuito abierto", "warn", "Zona abierta: alarma si está armada"),
        ("En corto", "cables unidos o puenteados", "short", "ve 0 Ω", "alert", "Falla: TBL grupo 5, tamper y cableado")]
for i, (t, s, st, val, kd, res) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 124, 352, 352, t, kd, sub=s))
    c.add(loop(x + 70, 210, st))
    c.add(tag(x + 176, 382, val, kd, 16))
    svg_, _ = wrap(x + 20, 428, res, 312, 16, 600, INK)
    c.add(svg_)
c.add(Note(48, 498, 540, "Sin resistencia, un corto se ve igual que una zona cerrada: alguien puentea el cable y la central nunca se entera.", title="Sin EOL, el corto es invisible", kind="alert"))
c.add(Note(612, 498, 540, "En Paradox la EOL es de 1 kΩ y se activa para toda la central en [706] opción 2. Los 5,6 kΩ de otras marcas no aplican.", title="Paradox: 1 kΩ", kind="info"))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso2: la resistencia en el extremo del detector
c = Canvas(K(2), "La resistencia va en el detector, no en la central")
c.add(NOLIG)
sv, an = strip(60, 160, ["Z1", "COM"], pitch=90, title="CENTRAL · ZONA 1")
c.add(sv)
c.add(Step(44, 250, 2))
c.add(rect(700, 140, 452, 280, WHITE, LINE2, rx=16))
c.add(text(724, 176, "Contacto magnético (NC)", 18, 600, INK))
c.add(text(724, 200, "en la puerta, a varios metros", 15, 400, INK3, FB))
zx, zy = an["Z1"]; cx_, cy_ = an["COM"]
c.add(wire([(zx, zy), (zx, 300), (760, 300)], "data"))
c.add(contact(760, 300, True, None, 90))
c.add(f'<path d="M850 300H930" stroke="{BLUE}" stroke-width="3"/>')
c.add(resistor(930, 300, 1110, "1 kΩ", BLUE, body=70))
c.add(f'<path d="M1110 300V370H{cx_}V{cy_}" stroke="{BLUE}" stroke-width="3" fill="none"/>')
c.add(f'<circle cx="{cx_}" cy="{cy_}" r="5" fill="{BLUE}"/><circle cx="{zx}" cy="{zy}" r="5" fill="{BLUE}"/>')
c.add(text(1020, 344, "en serie con el contacto", 15, 600, WARN, FB, anchor="middle"))
c.add(pill(420, 292, "cable de zona", BLUE, WHITE, 14))
c.add(Note(48, 446, 540, "Así el cable entero queda vigilado: un corto en cualquier punto del recorrido le saca la resistencia a la central. Si la resistencia queda en la bornera, el cable no está supervisado.", title="Por qué en el extremo", kind="ok"))
c.add(Note(612, 446, 540, "Medí la resistencia con el tester antes de usarla (paso 1). La guía muestra este y otros dibujos en la figura Single Zone Input Connections.", title="Antes de cablear", kind="info"))
save(c, "3-paso2.svg")

# ---------------------------------------------------------------- 3-paso4: ATZ, dos detectores por entrada
c = Canvas(K(4), "ATZ: dos detectores en el mismo par, dos valores")
c.add(NOLIG)
sv, an = strip(60, 160, ["Z1", "COM"], pitch=90, title="CENTRAL · ENTRADA")
c.add(sv)
c.add(Step(44, 250, 4))
c.add(rect(560, 130, 592, 300, WHITE, LINE2, rx=16, dash="8 6"))
c.add(text(584, 164, "Lazo ATZ · según la figura Double Zone Connections", 16, 600, INK2, FB))
for i, (n, r) in enumerate([("Detector 1", "1 kΩ"), ("Detector 2", "2,2 kΩ")]):
    y = 200 + i * 110
    c.add(rect(600, y, 240, 84, SOFT, LINE2, rx=12))
    c.add(text(620, y + 34, n, 18, 600, INK))
    c.add(text(620, y + 60, "contacto NC", 15, 400, INK3, FM))
    c.add(f'<rect x="900" y="{y + 26}" width="120" height="32" rx="6" fill="#FFF7E0" stroke="{WARN}" stroke-width="2.5"/>')
    c.add(mid(960, y + 48, r, 17, 700, WARN, FM))
    c.add(f'<path d="M840 {y + 42}H900" stroke="{INK3}" stroke-width="2"/>')
zx, zy = an["Z1"]; cx_, cy_ = an["COM"]
c.add(wire([(zx, zy), (zx, 290), (560, 290)], "data"))
c.add(wire([(cx_, cy_), (cx_, 330), (560, 330)], "data"))
c.add(text(380, 370, "un solo par de cables", 15, 600, BLUE, FB, anchor="middle"))
sv, _ = keys(60, 470, ["[ENTER]", "+", "0000", "+", "[705]", "[1]", "[ENTER]"], 17, hl=(5,))
c.add(sv)
c.add(lines(60, 548, ["Opción 1 = ATZ encendido.", "Opción 2 encendida = paralelo; apagada = serie (fábrica)."], 16, 26))
c.add(Note(612, 456, 540, "En la serie plus, solo la SP6000+. La central reconoce cada detector por el valor de su resistencia y le da un número de zona propio: anotalo en la planilla (paso 5).", title="Solo SP6000+ o EVO", kind="warn"))
save(c, "3-paso4.svg")
