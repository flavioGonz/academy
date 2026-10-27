from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Serie X: PoE+ para el grande, 24 V 1 A de techo al chico")
for x, name, sub, rows in [
    (70, "X937", "15,6\" · Android 14", [("PoE+ 802.3at o 12 V 2 A", "blue"), ("2 relés · 30 V 2 A", "gray"), ("2 RJ45 extra", "gray"), ("aluminio", "gray")]),
    (640, "X933", "7\" · Android", [("PoE o 12 V 1 A", "gray"), ("2 relés · 24 V 1 A", "warn"), ("plástico", "gray")]),
]:
    c.add(Monitor(x, 140, name, sub))
    for j, (s, k) in enumerate(rows):
        c.add(Chip(x + 270, 172 + j * 44, s, k, mono=False))
c.add(Label(70, 400, "Los dos traen 1 RS485 y 1 entrada de timbre.", 17, 500, INK2))
c.add(Note(70, 440, 520, "Pide PoE+ 802.3at en el puerto del switch. En un puerto 802.3af no hay energía suficiente: switch PoE+ o fuente de 12 V 2 A.", title="X937", kind="info"))
c.add(Note(640, 440, 500, "Sus relés aguantan hasta 24 V 1 A. Un portón, una cerradura de más consumo o cualquier cosa de más de 24 V o 1 A va con relé auxiliar.", title="X933", kind="warn"))
c.save(out("32.svg"))

# ---------------------------------------------------------------- paso 1
c = Canvas(K + " · Paso 1", "Revisá el puerto antes de colgar el X937")
sw = c.add(Router(330, 130, "Switch PoE", "un puerto at, otro af", ports=["802.3at", "802.3af", "3", "4"], hl={"802.3at": OK, "802.3af": WARN}))
m1 = c.add(Monitor(90, 390, "X937", "en puerto 802.3at", hl=OK))
m2 = c.add(Monitor(520, 390, "X937", "en puerto 802.3af", hl=ALERT))
c.add(Cable(sw.port("802.3at"), m1.top(), kind="data", label="PoE+", label_at=0.5, label_dy=-6))
c.add(Cable(sw.port("802.3af"), m2.top(), kind="alert", label="no alcanza", label_at=0.55, label_dy=-6, arrow=False))
c.add(Mark(m1.x + m1.w - 6, m1.y + 8, True))
c.add(Mark(m2.x + m2.w - 6, m2.y + 8, False))
c.add(Step(sw.x - 30, sw.y + 120, 1))
c.add(Note(860, 150, 300, "Sin switch PoE+, el X937 va con fuente de 12 V 2 A.", title="Plan B", kind="info"))
c.add(Note(860, 330, 300, "El X933 anda con PoE o con fuente de 12 V 1 A.", title="X933", kind="ok"))
c.save(out("32-paso1.svg"))

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "Más de 24 V o 1 A en el X933: relé auxiliar")
c.add(Label(60, 150, "El X933 solo mueve la bobina (poca corriente)", 18, 600, INK))
y1 = 250
c.add(Chip(60, y1 + 6, "+12 V", "alert"))
c.add(Wire([(140, y1), (250, y1)], kind="power+"))
c.add(contact(250, y1, "relé X933", sub="máx. 24 V 1 A", closed=True, w=170))
c.add(Wire([(420, y1), (560, y1)], kind="relay"))
c.add(coil(560, y1, "bobina", sub="relé auxiliar", w=170))
c.add(Wire([(730, y1), (850, y1)], kind="power-"))
c.add(Chip(860, y1 + 6, "−", "dark"))
c.add(Label(60, 380, "El relé auxiliar maneja la carga grande", 18, 600, INK))
y2 = 480
c.add(Chip(60, y2 + 6, "fuente de la carga", "gray", mono=False))
c.add(Wire([(232, y2), (560, y2)], kind="power+"))
c.add(contact(560, y2, "contacto aux.", sub="para la carga", closed=True, w=170))
c.add(Wire([(730, y2), (850, y2)], kind="relay"))
c.add(Generic(850, y2 - 42, "Carga", "más de 24 V o 1 A", icon="bolt", w=300))
c.add(Cable((645, y1 + 36), (645, y2 - 86), kind="logical", label="mueve", label_at=0.5, label_dy=6))
c.add(Step(490, 144, 2))
c.add(Note(60, 560, 500, "Anotá en la ficha: relé 1 del X933 → bobina del auxiliar; auxiliar → la carga.", kind="info", size=16))
c.save(out("32-paso2.svg"))
