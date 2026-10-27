from _akv import *


def lock_with_terms(c, x, y, title, sub, w=250, hl=None):
    """Cerradura con bornes + arriba y - abajo. Devuelve (pos_mas, pos_menos)."""
    c.add(Lock(x, y, title, sub, w=w, hl=hl))
    pm, mn = (x + 60, y), (x + w - 60, y + 84)
    c.add(terminal(pm[0], pm[1], "+", RED, size=17, side="right", lcolor=RED))
    c.add(terminal(mn[0], mn[1], "−", BLACK, size=17, side="right", lcolor=BLACK))
    return pm, mn


def psu_with_terms(c, x, y, title="Fuente 12 V CC", sub="aparte del portero", w=250):
    c.add(PSU(x, y, title, sub, w=w))
    pp, pn = (x + 60, y), (x + w - 60, y + 84)
    c.add(terminal(pp[0], pp[1], "+", RED, size=17, side="right", lcolor=RED))
    c.add(terminal(pn[0], pn[1], "−", BLACK, size=17, side="right", lcolor=BLACK))
    return pp, pn


# ---------- 4.svg: fail-safe vs fail-secure
c = Canvas("Akuvox · Lección 4", "Sin luz, ¿la puerta queda libre o trabada?")
cases = [(48, "Fail-safe · COM + NC", "NC", "Electroimán", "libera sin 12 V", "ok", "SIN ENERGÍA: LIBRE", "salida de emergencia"),
         (620, "Fail-secure · COM + NO", "NO", "Cerradura", "abre con 12 V", "warn", "SIN ENERGÍA: TRABADA", "portón de calle, depósito")]
for x0, ttl, term, lk, lks, kd, state, uso in cases:
    c.add(panel(x0, 130, 532, 470, ttl, "info"))
    r = c.add(Relay(x0 + 24, 170, "Relé A", "del portero"))
    pp, pn = (x0 + 330, 190), (x0 + 450, 274)
    c.add(PSU(x0 + 290, 190, "Fuente 12 V", "aparte", w=210))
    c.add(terminal(x0 + 340, 190, "+", RED, size=17, side="right", lcolor=RED))
    c.add(terminal(x0 + 450, 274, "−", BLACK, size=17, side="left", lcolor=BLACK))
    c.add(Lock(x0 + 290, 400, lk, lks, w=210))
    c.add(terminal(x0 + 340, 400, "+", RED, size=17, side="right", lcolor=RED))
    c.add(terminal(x0 + 450, 484, "−", BLACK, size=17, side="left", lcolor=BLACK))
    com, sel = r.port("COM"), r.port(term)
    c.add(wire([(x0 + 340, 172), (x0 + 340, 150), (x0 + 270, 150), (x0 + 270, 316), (com[0], 316), com], "power+"))
    c.add(wire([sel, (sel[0], 350), (x0 + 340, 350), (x0 + 340, 382)], "relay"))
    c.add(wire([(x0 + 450, 292), (x0 + 450, 330), (x0 + 510, 330), (x0 + 510, 520), (x0 + 450, 520), (x0 + 450, 502)], "power-"))
    c.add(Chip(x0 + 24, 450, state, kd, anchor="start"))
    c.add(text(x0 + 24, 500, "Uso típico:", 15, 600, INK2))
    c.add(text(x0 + 24, 522, uso, 15, 400, INK3, FB))
    if term == "NC":
        c.add(text(x0 + 24, 572, "Electroimán: diodo sobre la bobina (paso 2)", 15, 500, INK2))
    else:
        c.add(text(x0 + 24, 572, "La cerradura solo recibe 12 V mientras el relé actúa", 15, 500, INK2))
save(c, "4.svg")

# ---------- 4-paso2.svg: cableado en NO con fuente aparte y diodo
c = Canvas("Akuvox · Lección 4 · Paso 2", "Cableá la cerradura al relé con fuente aparte")
r = c.add(Relay(470, 140, "Relé A del portero", "contacto seco", hl=CYAN))
c.add(Step(470, 140, 2))
pp, pn = psu_with_terms(c, 60, 400)
lp, ln = lock_with_terms(c, 720, 400, "Cerradura de prueba", "o lámpara de 12 V", w=290)
com, no, nc = r.port("COM"), r.port("NO"), r.port("NC")
c.add(wire([pp, (pp[0], 320), (com[0], 320), com], "power+"))
c.add(wire([no, (no[0], 300), (lp[0], 300), lp], "relay"))
c.add(wire([pn, (pn[0], 600), (ln[0], 600), ln], "power-"))
# diodo en antiparalelo sobre la bobina
dx = 1110
c.add(f'<circle cx="{lp[0]}" cy="345" r="5" fill="{CYAN}"/>')
c.add(f'<path d="M{lp[0]} 345H{dx}V412" fill="none" stroke="{INK}" stroke-width="2.5"/>')
c.add(diode_v(dx, 442, 60))
c.add(f'<path d="M{dx} 472V600H{ln[0]}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
c.add(f'<circle cx="{ln[0]}" cy="600" r="5" fill="{BLACK}"/>')
c.add(text(1095, 532, "diodo en", 15, 600, INK, FB, anchor="end"))
c.add(text(1095, 552, "antiparalelo", 15, 600, INK, FB, anchor="end"))
c.add(text(1095, 574, "cátodo al +", 14, 500, INK3, FM, anchor="end"))
c.add(pill(330, 312, "+12 V → COM", RED))
c.add(pill(820, 292, "NO → + cerradura", CYAN))
c.add(pill(560, 592, "− cerradura → −12 V", BLACK))
c.add(text(nc[0] + 60, nc[1] - 30, "NC: libre", 15, 500, INK3, FM))
c.add(Note(60, 140, 360, "El relé solo cierra un contacto (30\u00a0V\u00a02\u00a0A en E16 y R20): la corriente la pone la fuente de la cerradura, nunca el portero.", title="Contacto seco", kind="info", size=15))
c.add(Note(800, 140, 350, "El diodo frena el pico de tensión que larga la bobina al cortarse: cuida el contacto del relé.", title="Electroimán o bobina", kind="warn", size=15))
save(c, "4-paso2.svg")

# ---------- 4-paso5.svg: botón de salida y alarmas
c = Canvas("Akuvox · Lección 4 · Paso 5", "El botón de salida va a una entrada, no al relé")
b = c.add(Generic(60, 170, "Pulsador de salida", "NA · del lado de adentro", icon="door", w=300))
c.add(f'<rect x="60" y="330" width="300" height="120" rx="16" fill="#26323F"/>')
c.add(text(80, 362, "Portero · bornera", 17, 600, WHITE))
c.add(terminal(130, 410, "entrada", CYAN, side="right", lcolor=WHITE))
c.add(terminal(290, 410, "común", CYAN, side="left", lcolor=WHITE))
c.add(text(210, 480, "nombres de borne según el modelo", 14, 500, INK3, FM, anchor="middle"))
c.add(wire([b.bottom(-80), (130, 300), (130, 401)], "relay"))
c.add(wire([b.bottom(80), (290, 300), (290, 401)], "relay"))
c.add(Step(60, 330, 5))
c.add(Window(430, 140, 720, 300, "Web del portero", path="Access Control > Input",
             rows=[("Enabled", "activada"), ("Trigger Electrical Level", "Low o High"), ("Execute Relay", "Relay A"),
                   ("Door Opened Timeout", "alarma si queda abierta"), ("Break-in Intrusion", "alarma si la fuerzan")], hl=2))
c.add(Note(430, 470, 340, "Apretar el botón dispara el relé elegido: la puerta abre igual que con un PIN.", title="Qué hace", kind="ok", size=15))
c.add(Note(800, 470, 350, "Door Opened Timeout avisa si la puerta queda abierta. Probala dejando la entrada accionada (paso 6).", title="Alarma gratis", kind="warn", size=15))
save(c, "4-paso5.svg")
