from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "IP o 2 hilos: la misma función, otro cable")
c.add(Zone(40, 150, 500, 420, "IP · cable UTP nuevo", BLUE))
sw = c.add(Generic(160, 195, "Switch PoE", "un UTP por equipo", icon="server", w=260))
pi = c.add(Generic(70, 400, "Portero IP", "PoE", icon="bell", w=210))
mi = c.add(Generic(305, 400, "Monitor IP", "PoE", icon="laptop", w=210))
c.add(Cable(sw.bottom(-60), pi.top(), kind="data", label="UTP", label_at=0.5, label_dy=0))
c.add(Cable(sw.bottom(60), mi.top(), kind="data", label="UTP", label_at=0.5, label_dy=0))
c.add(Zone(580, 150, 580, 420, "2 hilos · par existente", CYAN))
ps = c.add(PSU(610, 195, "Fuente 48 V DC", "1,25 A por portero", w=250))
p2 = c.add(Generic(610, 340, "R20A-2 / R20K-2", "portero, sin PoE", icon="bell", w=250))
c.add(Wire([ps.bottom(), p2.top()], kind="power+", label="48 V", at=(735, 312)))
ns = c.add(Generic(880, 195, "NS-2", "alimenta al C313-2", icon="server", w=255))
m2 = c.add(Generic(880, 340, "Monitor de 2 hilos", "C313W-2 / S562W-2", icon="laptop", w=255))
bus_y = 500
c.add(f'<path d="M620 {bus_y - 5}H1140M620 {bus_y + 5}H1140" stroke="{CYAN}" stroke-width="3"/>')
c.add(Label(625, bus_y + 40, "par del edificio (2 hilos)", 15, 600, CYAN, FM))
c.add(Wire([p2.bottom(), (p2.bottom()[0], bus_y - 6)], kind="relay"))
c.add(Wire([m2.bottom(), (m2.bottom()[0], bus_y - 6)], kind="relay"))
c.add(Wire([ns.right(), (1150, ns.right()[1]), (1150, bus_y - 6)], kind="logical", arrow=False))
c.add(Note(40, 590, 1120, "NC-2 y NX-2 también son de la línea, pero su rol exacto no está en lo leído: se confirman con el distribuidor.", kind="warn"))
c.save(out("37.svg"))

# ---------------------------------------------------------------- paso 1
c = Canvas(K + " · Paso 1", "Relevá el par existente y medilo antes de reutilizar")
bx, by, bw = 70, 150, 360
c.add(f'<path d="M{bx} {by + 40}L{bx + bw / 2} {by}L{bx + bw} {by + 40}V{by + 470}H{bx}Z" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
for i, lbl in enumerate(["Apto 301", "Apto 201", "Apto 101"]):
    fy = by + 60 + i * 120
    c.add(f'<rect x="{bx + 150}" y="{fy}" width="190" height="80" rx="10" fill="{SOFT}" stroke="{LINE2}"/>')
    c.add(text(bx + 245, fy + 34, lbl, 16, 600, INK, FB, anchor="middle"))
    c.add(text(bx + 245, fy + 58, "monitor viejo", 15, 400, INK3, FM, anchor="middle"))
    c.add(f'<path d="M{bx + 100} {fy + 40}H{bx + 150}" stroke="{CYAN}" stroke-width="3"/>')
    if i < 2:
        c.add(f'<path d="M{bx} {fy + 100}H{bx + bw}" stroke="{LINE}" stroke-width="2"/>')
c.add(f'<rect x="{bx + 20}" y="{by + 420}" width="110" height="40" rx="8" fill="#26323F"/>')
c.add(text(bx + 75, by + 446, "portero", 15, 600, WHITE, FB, anchor="middle"))
c.add(f'<path d="M{bx + 95} {by + 100}V{by + 420}M{bx + 105} {by + 100}V{by + 420}" stroke="{CYAN}" stroke-width="3"/>')
c.add(Chip(bx + 180, by + 445, "montante: par", "cyan"))
c.add(Step(bx + 60, by + 100, 1))
w = c.add(Window(500, 150, 640, 230, "Relevamiento", rows=[("Apartamentos", "____"), ("Par disponible hasta el portero", "____"), ("Par hasta cada apartamento", "____"), ("Accesos (portones)", "____")]))
c.add(Note(500, 410, 640, "Medí aislación y continuidad de cada par antes de reutilizarlo. Un par en mal estado no lo arregla ningún equipo.", title="Antes de cotizar", kind="warn"))
c.save(out("37-paso1.svg"))

# ---------------------------------------------------------------- paso 3
c = Canvas(K + " · Paso 3", "Lo que no sale de una página leída, en rojo")
ok = ["R20A-2 y R20K-2: 48 V DC 1,25 A", "R20A-2: tarjetas 13,56 y 125 kHz, sin PIN", "R20K-2: PIN y tarjetas", "C313-2: se alimenta del NS-2 o de 48 V", "C313W-2: RS485, relé, timbre y un RJ45", "Relé 30 V 2 A en R20-2 y C313-2"]
bad = ["Rol de NC-2 y NX-2", "Cantidades de NS-2, NC-2 y NX-2", "Ficha propia de cada equipo", "Largo máximo del par", "Datos de S562W-2 y E12S-2"]
c.add(Label(60, 160, "Sale de una página leída", 18, 600, OK))
for i, s in enumerate(ok):
    y = 210 + i * 58
    c.add(Mark(80, y, True))
    c.add(Label(112, y + 6, s, 17, 500, INK))
c.add(Label(700, 160, "A confirmar por escrito", 18, 600, ALERT))
for i, s in enumerate(bad):
    y = 210 + i * 58
    c.add(Mark(720, y, False))
    c.add(Label(752, y + 6, s, 17, 500, INK))
c.add(Note(60, 580, 1080, "Pedí al distribuidor la confirmación por escrito antes de pasar la cotización.", kind="info"))
c.save(out("37-paso3.svg"))
