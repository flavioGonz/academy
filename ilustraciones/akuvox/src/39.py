from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "El pedido sale de la ficha del modelo exacto")
c.add(Intercom(70, 170, "Portero", "ej. R29C", screen=True))
items = [
    ("Frente", "Versión exacta: R29S, R29C, R29C-L o R29C-T."),
    ("Montaje", "Caja o soporte de embutir o de superficie del modelo."),
    ("Cubierta de lluvia", "La del modelo y su color (R29: negro o plata)."),
    ("Alimentación", "PoE del tipo que pide, o la fuente de la tabla."),
    ("Cerradura", "Desde el portero si su salida alcanza; si no, fuente propia."),
    ("Módulos", "SR01, lector o Bkey, si la obra los pide."),
]
for i, (t, b) in enumerate(items):
    x = 300 + (i % 2) * 430
    y = 140 + (i // 2) * 160
    c.add(card(x, y, 400, 140, t, b))
c.add(Label(300, 640, "R29C-L (con LTE) lleva su propio soporte y no admite PoE.", 16, 500, INK3))
c.save(out("39.svg"))

# ---------------------------------------------------------------- paso 1
c = Canvas(K + " · Paso 1", "Módulo SR01: el relé que abre queda adentro")
c.add(f'<rect x="560" y="140" width="40" height="470" rx="6" fill="#D5DEE8" stroke="{LINE2}"/>')
c.add(Label(300, 160, "CALLE", 15, 600, INK3, FM, "middle"))
c.add(Label(880, 160, "ADENTRO", 15, 600, INK3, FM, "middle"))
po = c.add(Intercom(220, 200, "Portero", "frente a la calle", keypad=True))
sr = c.add(Generic(680, 250, "SR01", "relé de seguridad · 30 V 2 A", icon="shield", w=380))
lk = c.add(Lock(680, 440, "Cerradura", "la mueve el SR01", w=380))
c.add(Wire([po.port("relayA"), (640, po.port("relayA")[1]), (640, sr.left()[1]), sr.left()], kind="relay", label="12 V o RS485", at=(470, po.port("relayA")[1] - 14)))
c.add(Wire([sr.bottom(), lk.top()], kind="relay"))
c.add(Note(60, 560, 470, "Si rompen el portero, la puerta no se abre: el contacto que mueve la cerradura está del lado de adentro.", kind="ok"))
c.add(Label(680, 590, "Por la salida de 12 V: Security Relay A.", 16, 500, INK2))
c.add(Label(680, 616, "Por RS485: Security Relay B.", 16, 500, INK2))
c.save(out("39-paso1.svg"))

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "Cerradura NC o NO desde la salida de 12 V")
for x, kind, lock_t, lock_s, term, mode, col in [
    (40, "NC: abre al cortar", "Cerradura NC", "con 12 V queda trabada", "NC", "Always", BLUE),
    (620, "NO: abre al dar 12 V", "Cerradura NO", "sin 12 V queda trabada", "NO", "Triggered by Open Relay", CYAN),
]:
    c.add(Zone(x, 150, 540, 460, kind, col))
    st = c.add(Strip(x + 70, 190, "Portero", ["GND", "NO", "NC"], sub="12 V por el relé A", tw=110, w=400, hl={term: CYAN}))
    lk = c.add(Lock(x + 130, 450, lock_t, lock_s, w=290))
    g, t = st.port("GND"), st.port(term)
    c.add(Wire([g, (g[0], 400), (lk.x + 40, 400), (lk.x + 40, lk.y)], kind="power-"))
    c.add(Wire([t, (t[0], 420), (lk.x + 250, 420), (lk.x + 250, lk.y)], kind="power+"))
    c.add(Chip(x + 270, 580, mode, "dark", anchor="middle"))
c.add(Step(600, 640 - 10, 2))
c.save(out("39-paso2.svg"))
