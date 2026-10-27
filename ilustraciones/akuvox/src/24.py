import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 24.svg: las cuatro versiones del R29
c = Canvas("Akuvox · Lección 24", "Cuatro R29: la versión decide fuente y credenciales")
vers = [("R29S", 1, [("1 cámara", "gray"), ("sin Bluetooth", "gray")], ("PoE 802.3at", "ok"), "fuente: la tabla no la lista"),
        ("R29C", 2, [("2 cámaras", "gray"), ("Bluetooth", "cyan")], ("PoE at o 12 V 2,5 A", "ok"), ""),
        ("R29C-L", 2, [("2 cámaras", "gray"), ("LTE", "cyan")], ("sin PoE: 12 V 1,5 A", "alert"), "con el switch solo, no arranca"),
        ("R29C-T", 2, [("2 cámaras", "gray"), ("huella (sin QR)", "cyan")], ("PoE af o 12 V 1,5 A", "ok"), "")]
for i, (m, cams, chips, pw, note) in enumerate(vers):
    x = 48 + i * 280
    c.add(panel(x, 122, 264, 420, None, "alert" if m == "R29C-L" else "info"))
    c.add(text(x + 132, 156, m, 22, 700, INK, FM, anchor="middle"))
    c.add(portero(x + 82, 176, "pantalla", 0.66, cams=cams))
    for k, (s_, kd) in enumerate(chips):
        c.add(Chip(x + 132, 386 + k * 38, s_, kd, mono=False, anchor="middle"))
    c.add(Chip(x + 132, 476, pw[0], pw[1], mono=False, anchor="middle"))
    if note:
        c.add(text(x + 132, 518, note, 15, 500, ALERT if m == "R29C-L" else INK3, FB, anchor="middle"))
c.add(panel(48, 560, 1104, 64, None, "soft"))
c.add(text(600, 600, "Todas: tarjetas 13,56 y 125 kHz · relé 30 V 3 A · IP65 e IK06 · Android 7\"", 17, 600, INK, FB, anchor="middle"))
save(c, "24.svg")

# ---------------------------------------------------------------- 24-paso3: R29C-L sin PoE
c = Canvas("Akuvox · Lección 24 · Paso 3", "El R29C-L con LTE no arranca por PoE")
c.add(panel(48, 126, 540, 400, "Solo switch PoE", "alert"))
c.add(Router(76, 186, "Switch PoE", "802.3at", ports=["1", "2", "3"], hl={"1": CYAN}))
c.add(portero(420, 186, "pantalla", 0.62, "R29C-L", None, cams=2))
c.add(wire([(133, 356), (133, 390), (390, 390), (390, 240), (420, 240)], "data"))
c.add(check(80, 470, False) + text(104, 476, "no acepta PoE: queda apagado", 17, 600, ALERT, FB))
c.add(panel(612, 126, 540, 400, "Fuente 12 V 1,5 A", "ok"))
c.add(PSU(640, 196, "Fuente", "12 V 1,5 A", w=210))
c.add(portero(940, 186, "pantalla", 0.62, "R29C-L", None, cams=2))
c.add(wire([(850, 238), (940, 238)], "power+"))
c.add(Router(640, 330, "Switch", "solo datos", ports=["1", "2", "3"]) if False else "")
c.add(check(644, 470, True) + text(668, 476, "con su fuente, arranca", 17, 600, OK, FB))
c.add(Note(48, 548, 1104, "En la lista de obra, el R29C-L va con fuente de 12 V 1,5 A y con el soporte de pared R29C-L.", kind="info", size=16))
save(c, "24-paso3.svg")

# ---------------------------------------------------------------- 24-paso4: montaje y accesorios
c = Canvas("Akuvox · Lección 24 · Paso 4", "Elegí cubierta y soporte según el montaje")


def wall_section(x, y, embutido):
    out = [f'<rect x="{x}" y="{y}" width="70" height="300" fill="#E9E4DA" stroke="{INK3}" stroke-width="2"/>']
    for k in range(6):
        out.append(f'<path d="M{x} {y + 20 + k * 50}l70 -30" stroke="#CFC6B6" stroke-width="2"/>')
    if embutido:
        out.append(f'<rect x="{x + 20}" y="{y + 60}" width="50" height="180" fill="{WHITE}" stroke="{INK2}" stroke-width="2" stroke-dasharray="5 4"/>')
        out.append(f'<rect x="{x + 40}" y="{y + 70}" width="48" height="160" rx="8" fill="#26323F"/>')
        out.append(f'<path d="M{x + 36} {y + 46}h66l-8 22h-58z" fill="{BLUE}" opacity=".9"/>')
    else:
        out.append(f'<rect x="{x + 70}" y="{y + 64}" width="14" height="172" fill="{INK3}"/>')
        out.append(f'<rect x="{x + 84}" y="{y + 70}" width="48" height="160" rx="8" fill="#26323F"/>')
        out.append(f'<path d="M{x + 70} {y + 44}h74l-8 24h-66z" fill="{BLUE}" opacity=".9"/>')
    return "".join(out)


c.add(panel(48, 126, 540, 420, "De superficie (pared)", "info"))
c.add(wall_section(110, 190, False))
c.add(text(270, 250, "cubierta de lluvia", 16, 600, BLUE, FB))
c.add(arrow((266, 245), (232, 245), "flow", bend="straight"))
c.add(text(270, 330, "soporte de pared", 16, 600, INK2, FB))
c.add(arrow((266, 325), (196, 325), "flow", bend="straight"))
c.add(panel(612, 126, 540, 420, "Embutido", "info"))
c.add(wall_section(674, 190, True))
c.add(text(834, 250, "cubierta de lluvia", 16, 600, BLUE, FB))
c.add(arrow((830, 245), (780, 245), "flow", bend="straight"))
c.add(text(834, 470, "soporte para embutir", 16, 600, INK2, FB))
c.add(text(834, 492, "(caja en la pared)", 15, 400, INK3, FB))
c.add(arrow((830, 465), (748, 432), "flow", bend="straight"))
c.add(text(270, 420, "portero", 16, 600, INK, FB) + arrow((266, 415), (220, 400), "flow", bend="straight"))
c.add(text(834, 340, "portero", 16, 600, INK, FB) + arrow((830, 335), (768, 335), "flow", bend="straight"))
c.add(text(320, 520, "Dibujo genérico: la forma de cada accesorio está en la ficha del R29.", 15, 400, INK3, FB) if False else "")
c.add(Note(48, 562, 1104, "Dibujo genérico. Cubierta y soporte en negro o plata; el R29C-L lleva su soporte de pared propio. IK06: si el pliego pide más impacto, compará antes.", kind="info", size=15))
save(c, "24-paso4.svg")
