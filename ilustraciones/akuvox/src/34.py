from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Carga lejos del portero: un WR01 al lado de la carga")
sw = c.add(Router(400, 120, "Switch PoE+", "VLAN de porteros", ports=["1", "2", "3"], hl={"3": CYAN}))
c.add(Zone(440, 345, 340, 170, "gabinete cerrado", INK3))
wr = c.add(Generic(480, 385, "WR01", "2 relés · 2 entradas", icon="bolt", w=260, dark=True))
c.add(Wire([sw.port("3"), (sw.port("3")[0], wr.y)], kind="data", label="red", at=(sw.port("3")[0] + 44, 326)))
cam = c.add(Camera(60, 300, "Cámara LPR", "lee la patente", w=270))
c.add(Arrow(cam.right(), (wr.x - 6, wr.y + 30), kind="logical", label="patente", label_at=0.45))
ph = c.add(Phone(60, 470, "Celular", "credencial BLE", w=270))
c.add(Cable(ph.right(), (wr.x - 6, wr.y + 62), kind="wifi", label="Bluetooth", label_at=0.45, label_dy=24, arrow=False))
gate = c.add(Generic(880, 300, "Portón o barrera", "relé 1", icon="door", w=270))
btn = c.add(Generic(880, 470, "Pulsador", "entrada 1", icon="bell", w=270))
c.add(Cable(wr.right(-14), gate.left(), kind="relay"))
c.add(Cable(btn.left(), wr.right(14), kind="relay"))
c.add(Label(450, 560, "Sin lector propio: abre por web, API, Bluetooth o patente.", 16, 500, INK2))
c.add(Label(450, 586, "Patentes desde el firmware 1401.30.11.221.", 16, 500, INK3, FM))
c.save(out("34.svg"))

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "Relé 1 a una lámpara y entrada 1 a un pulsador")
st = c.add(Strip(340, 140, "WR01", ["IN1", "GND", "12V", "R1·a", "R1·b"], sub="bornes genéricos: ubicalos en su guía", tw=96, w=540))
p = {t: st.port(t) for t in st.terms}
c.add(Wire([p["12V"], (p["12V"][0], 335), (p["R1·a"][0], 335), p["R1·a"]], kind="power+", label="puente", at=(648, 335)))
lamp = c.add(Lamp(930, 430, "Lámpara 12 V", "de banco"))
c.add(Wire([p["R1·b"], (p["R1·b"][0], 430), lamp.port("a")], kind="relay"))
c.add(Wire([lamp.port("b"), (1040, 430), (1040, 600), (p["GND"][0], 600), p["GND"]], kind="power-", label="vuelve a GND", at=(780, 600)))
pb = c.add(Generic(60, 400, "Pulsador", "de banco", icon="bell", w=220))
c.add(Wire([pb.right(-14), (p["IN1"][0], pb.right(-14)[1]), p["IN1"]], kind="relay"))
c.add(Wire([pb.right(14), (p["GND"][0], pb.right(14)[1])], kind="power-"))
c.add(Chip(p["12V"][0] + 52, 386, "12 V: máx. 500 mA", "warn", anchor="middle"))
c.add(Step(st.x + st.w + 30, st.y + 30, 2))
c.add(Note(60, 530, 400, "Probá: activá el relé 1 desde la web y mirá el registro; después apretá el pulsador.", kind="ok"))
c.save(out("34-paso2.svg"))

# ---------------------------------------------------------------- paso 6
c = Canvas(K + " · Paso 6", "A15: de la pantalla a la IP en tres toques")
c.add(card(60, 160, 330, 170, "Mantené la pantalla 5 s", "En el A15 instalado en el marco de la puerta.", n="a"))
c.add(card(435, 160, 330, 170, "PIN o tarjeta de administrador", "Validá como administrador para abrir el menú.", n="b"))
c.add(card(810, 160, 330, 170, "Setting > System Info > Network", "Ahí está la IP para entrar a la web.", n="c"))
c.add(Arrow((392, 245), (433, 245), kind="flow"))
c.add(Arrow((767, 245), (808, 245), kind="flow"))
c.add(Table(60, 400, ["Alimentación del A15", "Borne de 12 V"], [["PoE 802.3at", "hasta 500 mA"], ["Fuente 12 V 2 A", "hasta 1 A"]], [330, 250], row_h=46, mono_cols=(1,)))
c.add(Note(740, 400, 400, "Terminal facial de 4,59\" para marco angosto: PIN, 13,56 MHz, rostro, Bluetooth y QR.", title="A15", kind="info"))
c.save(out("34-paso6.svg"))
