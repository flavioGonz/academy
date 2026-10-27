from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Punto de emergencia: voz a la central, video al NVR")
p = c.add(Intercom(70, 170, "E21", "extensión 801"))
sw = c.add(Router(330, 150, "Switch PoE", "802.3af", ports=["1", "2", "3"], hl={"1": CYAN}))
c.add(Wire([p.port("eth"), (290, p.port("eth")[1]), (290, 360), (sw.port("1")[0], 360), sw.port("1")], kind="data", label="PoE", at=(290, 300)))
cen = c.add(Server(780, 150, "Central IP", "interno 200 guardia", w=260))
nvr = c.add(Server(780, 300, "NVR", "graba la cámara", w=260))
c.add(Arrow(sw.right(-30), cen.left(), kind="logical", label="SIP", label_at=0.45))
c.add(Arrow(sw.right(10), nvr.left(), kind="logical", label="ONVIF o RTSP", label_at=0.5, label_dy=18))
c.add(Label(70, 548, "Lo que trae el E21 (guía de selección y tablas):", 16, 600, INK))
c.add(chips_row(70, 592, ["acero inoxidable", "cámara · ONVIF", "IP65", "relé 30 V 3 A"]))
c.add(chips_row(70, 636, ["sin pantalla", "sin PIN, tarjeta ni Wiegand", "sin salida de 12 V"], kind="warn"))
c.add(Note(780, 430, 370, "El E20S también va por PoE 802.3af, pero no está en la guía de selección: cámara y protección no se afirman.", title="¿Y el E20S?", kind="info"))
c.save(out("29.svg"))

# ---------------------------------------------------------------- paso 1
c = Canvas(K + " · Paso 1", "Conectá el E21 a PoE y escuchá su IP")
sw = c.add(Router(330, 140, "Switch PoE", "puerto 802.3af", ports=["1", "2", "3", "4"], hl={"2": CYAN}))
p = c.add(Intercom(80, 300, "E21", "PoE 802.3af o 12 V 1 A"))
c.add(Wire([p.port("eth"), (sw.port("2")[0], p.port("eth")[1]), sw.port("2")], kind="data", label="cable de red", at=(330, p.port("eth")[1] - 14)))
c.add(Step(sw.port("2")[0] + 34, sw.port("2")[1] + 28, 1))
bx, by = p.x + 75, p.y + 196
c.add(f'<circle cx="{bx}" cy="{by}" r="34" fill="none" stroke="{CYAN}" stroke-width="3" stroke-dasharray="5 6"/>')
c.add(bubble(270, 470, 330, "Mantené el pulsador 5 s: el E21 dice su IP en voz alta.", tail="left"))
c.add(Chip(270, 600, "anotala: la vas a usar en el paso 2", "gray", mono=False))
c.add(Note(760, 150, 390, "El E20S no anuncia la IP. Alimentalo, dejá que tome IP por DHCP y buscala con IP Scanner o en la tabla del DHCP.", title="Si es un E20S", kind="warn"))
c.add(Note(760, 360, 390, "El E21 no da 12 V para una cerradura. Si maneja una, la cerradura lleva su propia fuente.", title="Alimentación", kind="info"))
c.save(out("29-paso1.svg"))

# ---------------------------------------------------------------- paso 4
c = Canvas(K + " · Paso 4", "Si nadie atiende en 20 s, llama al respaldo")
b = c.add(Generic(40, 280, "Botón del E21", "extensión 801", icon="bell", w=250))
cen = c.add(Server(350, 280, "Central IP", "regla de desvío", w=230))
g = c.add(Generic(760, 150, "Interno 200", "guardia", icon="user", w=250))
r = c.add(Generic(760, 410, "Cola o celular", "de guardia", icon="phone", w=250))
c.add(Arrow(b.right(), cen.left(), label="llamada", label_at=0.5, label_dy=-16))
bx = 660
c.add(Wire([cen.right(-14), (bx, cen.right(-14)[1]), (bx, g.left()[1]), (g.left()[0] - 4, g.left()[1])], kind="ok", arrow=True, label="1º: suena acá", at=(bx, 250)))
c.add(Wire([cen.right(14), (bx, cen.right(14)[1]), (bx, r.left()[1]), (r.left()[0] - 4, r.left()[1])], kind="alert", arrow=True, label="2º: sin respuesta en 20 s", at=(bx, 400)))
c.add(Mark(1060, 192, True))
c.add(Label(1088, 198, "atiende", 16, 600, OK))
c.add(Mark(1060, 452, False))
c.add(Label(1088, 446, "nadie", 16, 600, ALERT))
c.add(Label(1088, 466, "atiende", 16, 600, ALERT))
c.add(Note(40, 470, 560, "Probá los dos casos: apretá y atendé en el 200; después apretá y no atiendas. Si a los 20 s no suena el respaldo, el punto de emergencia no está terminado.", title="Cómo se prueba", kind="ok"))
c.save(out("29-paso4.svg"))
