import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _fxo import *

# ---------------------------------------------------------------- 13.svg: quién da qué en la línea
c = Canvas(K(), "Antel da tensión y timbre; la UCM descuelga por FXO")
c.add(dev(48, 140, "Central de Antel", "hace de FXS", icon="central", w=270, dark=True))
j = c.add(Jack(520, 132, "Roseta", "RJ11"))
c.add(par([(318, 182), (520, 182)], "par de cobre", dy=-14))
# lo que da la línea
c.add(panel(712, 132, 440, 196, "Lo que da la línea (FXS)", "info", title_size=18))
lst, _ = bullet_list(732, 196, ["Tensión en reposo (continua)", "Timbre (alterna) cuando entra una llamada",
                                "Tono de invitación a marcar al descolgar", "Número del que llama, si está contratado"], 400, size=16, gap=8)
c.add(lst)
# UCM con FXO1
u = c.add(UCMAnalog(520, 392, w=632, top=True, state={"FXO1": "libre"}, hl={"FXO1": CYAN}))
fx = u.port("FXO1")
c.add(par([j.port("rj"), (595, 352), (fx[0], 352), (fx[0], fx[1])], "cable RJ11", dy=-12, at=0.6))
c.add(text(1128, 518, "El FXO hace de teléfono:", 16, 600, WHITE, FB, anchor="end"))
c.add(text(1128, 540, "descuelga y cuelga.", 16, 500, "#9FC3E3", FB, anchor="end"))
# equipos en paralelo
for i, (t, s, ic) in enumerate([("Alarma", "reporta por la línea", "alarma"), ("Posnet", "autoriza por la línea", "posnet"), ("Teléfono", "en otro ambiente", "tel")]):
    y = 292 + i * 92
    c.add(dev(48, y, t, s, icon=ic, w=290, h=76))
    c.add(par([(420, 182), (420, y + 38), (338, y + 38)], color=INK3, w=2))
c.add(pill(420, 268, "mismo par", INK3, WHITE, size=14, mono=False))
c.add(Note(48, 588, 1104, "Antel no publica tensiones ni frecuencias de su línea: se miden antes de enchufar, y todo lo que cuelga del par también descuelga.", kind="warn", size=16))
save(c, "13.svg")

# ---------------------------------------------------------------- 13-paso1: medir reposo y descolgado
c = Canvas(K(1), "Medí el par con la central desconectada")
# frente de la ficha RJ11 (6 posiciones, se usan 3 y 4)
c.add(panel(48, 132, 420, 230, "Ficha RJ11: se usan los contactos 3 y 4", "info", title_size=17))
c.add(f'<rect x="118" y="180" width="280" height="150" rx="10" fill="#0B1A28"/>')
pins = {}
for i in range(6):
    px = 150 + i * 44
    used = i in (2, 3)
    c.add(text(px, 210, str(i + 1), 15, 600, "#E7C66A" if used else "#7FA6C9", FM, anchor="middle"))
    c.add(f'<rect x="{px - 8}" y="224" width="16" height="48" rx="3" fill="{"#E7C66A" if used else "#3A4A5C"}"/>')
    pins[i + 1] = (px, 272)
m = c.add(Meter(170, 400, "__ V", "V CC", w=176, h=200))
c.add(probe(m.port("rojo"), (pins[3][0], pins[3][1]), RED))
c.add(probe(m.port("negro"), (pins[4][0], pins[4][1]), BLACK))
c.add(Step(48, 132, 1))
# lecturas
c.add(panel(520, 132, 632, 150, "Reposo, todo colgado", "info"))
c.add(text(540, 204, "Anotá: ____ V", 22, 600, INK, FM))
svg, _ = wrap(540, 240, "Referencia de las fuentes: de 24 a 70 V; muchas líneas andan cerca de 48 V.", 590, 16, 400, INK2)
c.add(svg)
c.add(panel(520, 300, 632, 150, "Descolgado, con el teléfono de prueba", "info"))
c.add(text(540, 372, "Anotá: ____ V", 22, 600, INK, FM))
svg, _ = wrap(540, 408, "Cae a pocos voltios: entre 4 y 18 V según la distancia a la central (Sandman).", 590, 16, 400, INK2)
c.add(svg)
c.add(Note(520, 470, 632, "Si en reposo ya da valores de descolgado, algo en paralelo tiene tomada la línea.", kind="warn", size=16))
c.add(Note(520, 560, 632, "Con la línea sonando hay unos 70 V de alterna: no toques los contactos.", kind="alert", size=16))
save(c, "13-paso1.svg")

# ---------------------------------------------------------------- 13-paso5: lo que cuelga del par
c = Canvas(K(5), "Todo lo que cuelga del par también descuelga")
c.add(dev(48, 290, "Línea de Antel", "par de la roseta", icon="central", w=280, dark=True))
eq = [("Panel de alarma", "llama para reportar", "alarma"), ("Posnet", "autoriza por la línea", "posnet"),
      ("Fax", "puede atender solo", "fax"), ("Teléfono", "olvidado en el depósito", "tel")]
for i, (t, s, ic) in enumerate(eq):
    y = 140 + i * 100
    c.add(dev(560, y, t, s, icon=ic, w=330, h=80, hl=WARN))
    c.add(par([(328, 332), (440, 332), (440, y + 40), (560, y + 40)], color=INK3, w=2))
    c.add(Chip(910, y + 50, "anotalo", "warn", mono=False))
c.add(Step(48, 140, 5))
c.add(Note(48, 158, 360, "Cualquiera de estos equipos puede tomar la línea sin avisar: la central la ve ocupada o la tensión baja.", kind="info", size=16))
c.add(Note(48, 552, 1104, "Para probar la línea: una línea, un equipo. Desconectá el resto y medí de nuevo; después se vuelve a conectar lo que haga falta.", kind="ok", size=16))
save(c, "13-paso5.svg")

# ---------------------------------------------------------------- 13-paso7: enchufar al FXO1
c = Canvas(K(7), "Enchufá la línea al FXO1 y mirá el Dashboard")
j = c.add(Jack(110, 140, "Roseta", "línea 1"))
u = c.add(UCMAnalog(48, 380, w=632, top=True, state={"FXO1": "gris"}, hl={"FXO1": CYAN}))
fx = u.port("FXO1")
c.add(par([j.port("rj"), (185, 330), (fx[0], 330), (fx[0], fx[1])], "cable RJ11", dy=-12, at=0.55))
c.add(Step(fx[0] + 30, fx[1] - 50, 7))
c.add(Window(724, 140, 428, 250, "UCM · web", path="System Status > Dashboard", rows=[("Interface Status", ""), ("FXO 1", "gris"), ("quiere decir", "conectado, sin troncal"), ("FXO 2 a 4", "sin línea todavía")], hl=1))
c.add(Note(724, 420, 428, "Gris en el FXO1 es lo esperado: la central ve la línea pero todavía no tiene troncal. Eso es la lección siguiente.", kind="ok", size=16))
c.add(Note(48, 588, 1104, "Lifeline: con un corte de luz, el FXS1 queda conectado al FXO1 y el FXS2 al FXO2. Un teléfono analógico en el FXS1 sigue andando por la línea 1.", kind="info", size=16))
save(c, "13-paso7.svg")
