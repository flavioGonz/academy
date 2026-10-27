from _akx2941 import *

K = "Akuvox"


def panel(x, y, floors, active):
    """Botonera genérica de ascensor: devuelve (svg, {piso: (x, y) del borde izquierdo del botón})."""
    h = 60 + len(floors) * 66
    o = [f'<rect x="{x}" y="{y}" width="200" height="{h}" rx="18" fill="#E9EEF3" stroke="{LINE2}" stroke-width="2"/>',
         text(x + 100, y + 34, "botonera", 15, 600, INK3, FM, anchor="middle")]
    pos = {}
    for i, f in enumerate(floors):
        cy = y + 82 + i * 66
        on = f == active
        o.append(f'<circle cx="{x + 60}" cy="{cy}" r="24" fill="{OK_BG if on else WHITE}" stroke="{OK if on else LINE2}" stroke-width="{3 if on else 2}"/>')
        o.append(text(x + 60, cy + 6, f, 17, 700, OK if on else INK3, FM, anchor="middle"))
        o.append(text(x + 100, cy + 6, "habilitado" if on else "bloqueado", 15, 600 if on else 400, OK if on else INK3, FB))
        pos[f] = (x, cy)
    return "".join(o), pos


# ---------------------------------------------------------------- figura principal
c = Canvas(K, "La tarjeta habilita solo el piso del usuario")
t = c.add(Generic(50, 300, "Terminal", "A08 o portero", icon="card", w=250))
c.add(Chip(50, 270, "usuario: piso 3", "cyan", mono=False))
ec = c.add(Generic(450, 300, "EC33", "32 relés · hasta 64", icon="elevator", w=280, dark=True))
c.add(Arrow(t.right(), ec.left(), kind="logical", label="HTTP", label_at=0.5))
svg, pos = panel(900, 130, ["4", "3", "2", "1", "PB", "-1"], "3")
c.add(svg)
c.add(Wire([ec.right(), (820, ec.right()[1]), (820, pos["3"][1]), (pos["3"][0] + 34, pos["3"][1])], kind="relay", label="relé del piso 3", at=(780, 230)))
c.add(Label(450, 450, "Los demás relés no se mueven:", 16, 600, INK))
c.add(Label(450, 474, "esa tarjeta no llega a otro piso.", 16, 500, INK2))
c.add(Note(50, 520, 690, "EC33 (ficha): Wiegand 26/34, 20.000 tarjetas, 100.000 registros, TCP/IP y RS485. Lo integran todos los porteros y terminales de Akuvox salvo A094 y E20.", kind="info"))
c.save(out("36.svg"))

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "El terminal le habla al EC33 con su usuario")
w1 = c.add(Window(50, 140, 545, 330, "Terminal · web", path="Device > Lift Control",
                  rows=[("Lift Control List", "Akuvox"), ("Server 1 (Unlock) IP", "192.168.88.40"), ("Usuario / clave", "ec33-lab / Ejemplo-Lift-2026"), ("Floor Starts From", "-1"), ("Device Location", "planta baja")], hl=2))
w2 = c.add(Window(705, 140, 450, 250, "EC33 · web", path="Device > Relay",
                  rows=[("Open Relay via HTTP", "Enabled"), ("Usuario", "ec33-lab"), ("Clave", "Ejemplo-Lift-2026")], hl=1))
c.add(Step(w2.x + w2.w - 10, w2.y - 6, 1))
c.add(Step(w1.x + w1.w - 10, w1.y - 6, 2))
c.add(Arrow((w1.x + w1.w + 6, 311), (w2.x - 8, 273), kind="logical"))
c.add(Label(650, 340, "mismo", 15, 600, INK3, FM, "middle"))
c.add(Label(650, 360, "usuario", 15, 600, INK3, FM, "middle"))
c.add(Note(50, 500, 545, "-1 si el edificio tiene un subsuelo. Si hay planta baja entre -1 y 1, configurala en Ground Floor.", title="Floor Starts From", kind="info"))
c.add(Note(705, 420, 450, "Server 1 (Unlock) libera pisos. Server 2 (Execute) solo si un segundo EC33 llama al ascensor.", title="Dos EC33 posibles", kind="info"))
c.save(out("36-paso2.svg"))

# ---------------------------------------------------------------- paso 5
c = Canvas(K + " · Paso 5", "¿Paralelo o serie? Acordalo con el ascensorista")
c.add(Zone(40, 150, 540, 400, "PARALELO · directo al piso", BLUE))
A, B = 90, 530
for y, lbl in [(270, "botón del piso"), (420, "relé EC33")]:
    c.add(Wire([(A, y), (225, y)], kind="relay", dots=False))
    c.add(contact(225, y, lbl, w=190))
    c.add(Wire([(415, y), (B, y)], kind="relay", dots=False))
c.add(Wire([(A, 270), (A, 420)], kind="relay", dots=False))
c.add(Wire([(B, 270), (B, 420)], kind="relay", dots=False))
c.add(Label(60, 505, "Cierra cualquiera de los dos: el relé marca el piso", 16, 500, INK2))
c.add(Label(60, 528, "aunque nadie apriete el botón.", 16, 500, INK2))
c.add(Zone(620, 150, 540, 400, "SERIE · liberar botones", CYAN))
y = 340
c.add(Wire([(650, y), (680, y)], kind="relay", dots=False))
c.add(contact(680, y, "relé EC33", w=190))
c.add(Wire([(870, y), (905, y)], kind="relay", dots=False))
c.add(contact(905, y, "común del botón", w=200))
c.add(Wire([(1105, y), (1130, y)], kind="relay", dots=False))
c.add(Label(650, 505, "El botón funciona solo mientras el relé está", 16, 500, INK2))
c.add(Label(650, 528, "cerrado: después de validar la credencial.", 16, 500, INK2))
c.add(Note(40, 580, 1120, "En el ascensor real lo cablea o lo autoriza la empresa de mantenimiento del ascensor.", kind="warn"))
c.save(out("36-paso5.svg"))
