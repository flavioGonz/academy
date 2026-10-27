from _akv import *

# ---------- 10.svg: qué sigue andando sin internet
c = Canvas("Akuvox · Lección 10", "Se corta internet: ¿qué sigue andando?")
c.add(Zone(48, 140, 640, 470, "Red local del edificio", OK))
p = c.add(Generic(80, 190, "Portero", "PIN · tarjeta", icon="bell", w=230))
m = c.add(Generic(420, 190, "Monitor", "atiende y abre", icon="laptop", w=230))
r = c.add(Generic(420, 420, "Router", "salida WAN", icon="globe", w=230))
c.add(Arrow(p.right(-10), m.left(-10), kind="ok", label="llamada", label_dy=-12))
c.add(Arrow(m.left(14), p.right(14), kind="ok"))
c.add(text(365, 282, "apertura", 15, 600, OK, FM, anchor="middle"))
c.add(wire([p.bottom(), (p.bottom()[0], r.left()[1]), r.left()], "data"))
c.add(Chip(215, 350, "PIN y tarjeta: local", "ok", mono=False))
c.add(Zone(740, 140, 412, 470, "Internet", ALERT))
cl = c.add(CloudBox(790, 190, "SmartPlus", "nube de Akuvox", w=320))
ph = c.add(Phone(790, 420, "App SmartPlus", "llamada · llave temporal", w=320))
c.add(Cable(r.right(), cl.left(), kind="alert", arrow=False))
c.add(Mark(712, 432, ok=False))
c.add(text(712, 480, "WAN", 15, 600, ALERT, FM, anchor="middle"))
c.add(Cable(cl.bottom(), ph.top(), kind="alert"))
c.add(Note(80, 520, 580, "Sin internet: el monitor atiende y la puerta abre. Lo que se pierde es la app.", kind="ok", size=16))
c.add(text(950, 580, "sin internet: no llega", 15, 600, ALERT, FB, anchor="middle"))
save(c, "10.svg")

# ---------- 10-paso2.svg: cuenta 1 y cuenta 2
c = Canvas("Akuvox · Lección 10 · Paso 2", "Mirá qué cuenta usa SmartPlus y cuál la central")
c.add(Window(48, 150, 530, 190, "Account > Basic · Account 1", rows=[("Uso", "SmartPlus (nube)"), ("Register Name", "número SIP de SmartPlus"), ("Estado", "registrada en la nube")], hl=0))
c.add(Window(622, 150, 530, 190, "Account > Basic · Account 2", rows=[("Uso", "central local"), ("Register Name", "201"), ("Server Address", "192.168.88.10")], hl=0))
c.add(Step(48, 150, 2))
c.add(Note(48, 380, 1104, "Con SmartPlus activo, la cuenta 1 queda tomada por la nube. La central del edificio va en la cuenta 2 y sigue registrada aunque internet se caiga.", title="Dos cuentas, dos caminos", kind="info"))
save(c, "10-paso2.svg")

# ---------- 10-paso4.svg: la tabla de entrega
c = Canvas("Akuvox · Lección 10 · Paso 4", "Probá fila por fila con el WAN desconectado")
rows = [["Llamada portero → monitor", "local", "no"], ["Apertura desde el monitor", "local", "no"], ["PIN / tarjeta en el portero", "local", "no"],
        ["Llamada a la app SmartPlus", "—", "sí"], ["Llave temporal nueva", "—", "sí"]]
c.add(Table(48, 150, ["Función", "Local", "Necesita internet"], rows, [440, 200, 300], row_h=52))
for i, rr in enumerate(rows):
    c.add(Mark(1040, 150 + 52 * (i + 1) + 26, ok=rr[2] == "no"))
c.add(Note(48, 480, 1104, "Esto es lo esperado según la lección. Anotá lo que realmente pase en tu banco y pasalo a la ficha de entrega: el cliente sabe de antemano que la app es un extra.", kind="warn"))
c.add(Step(48, 150, 4))
save(c, "10-paso4.svg")
