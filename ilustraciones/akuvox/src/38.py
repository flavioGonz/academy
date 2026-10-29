from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Escritorio de guardia: el R49G atiende el portero")
po = c.add(Generic(50, 330, "Portero", "extensión SIP", icon="bell", w=230))
sw = c.add(Router(360, 130, "Switch PoE", "red de porteros", ports=["1", "2", "3"], hl={"1": CYAN, "2": CYAN}))
cen = c.add(Server(860, 150, "Central IP", "lección 6", w=260))
r49 = c.add(Generic(470, 440, "R49G", "teléfono de video · 7\"", icon="phone", w=300))
pc = c.add(Laptop(870, 440, "PC del guardia", "navega por el R49G", w=270))
c.add(Wire([po.top(), (po.top()[0], 330 - 20), (sw.port("1")[0], 330 - 20), sw.port("1")], kind="data", dots=True))
c.add(Wire([sw.port("2"), (sw.port("2")[0], r49.y)], kind="data", label="PoE", at=(sw.port("2")[0] + 36, 380)))
c.add(Cable(r49.right(), pc.left(), kind="data", label="puerto 2", label_at=0.5))
c.add(Arrow(sw.right(-30), cen.left(), kind="logical", label="SIP", label_at=0.45))
c.add(chips_row(50, 600, ["Android 9", "2 Gigabit conmutados", "PoE · Wi-Fi", "Bluetooth · USB"]))
c.save(out("38.svg"))

# ---------------------------------------------------------------- paso 1
c = Canvas(K + " · Paso 1", "PoE al puerto 1 del R49G, la PC al puerto 2")
sw = c.add(Router(60, 140, "Switch PoE", "con respaldo de energía", ports=["1", "2", "3", "4"], hl={"2": CYAN}))
r = c.add(Router(520, 330, "R49G", "2 puertos conmutados", ports=["puerto 1", "puerto 2"], hl={"puerto 1": CYAN, "puerto 2": BLUE}, dark=False))
p1, p2 = r.port("puerto 1"), r.port("puerto 2")
s2 = sw.port("2")
c.add(Wire([s2, (s2[0], 590), (p1[0], 590), p1], kind="data", label="PoE", at=(s2[0] + 120, 590)))
pc = c.add(Laptop(860, 560, "PC del guardia", "", w=270))
c.add(Wire([p2, (p2[0], pc.left()[1]), pc.left()], kind="data"))
c.add(Step(p1[0] - 44, p1[1] + 26, 1))
c.add(Note(880, 140, 270, "Si se corta el PoE del R49G, la PC también queda sin red.", title="Un solo cable para dos", kind="warn"))
c.add(Label(860, 350, "Verificá que la PC navegue", 17, 600, INK))
c.add(Label(860, 376, "antes de seguir con el paso 2.", 17, 500, INK2))
c.save(out("38-paso1.svg"))

# ---------------------------------------------------------------- paso 3
c = Canvas(K + " · Paso 3", "Lo que sé de cada equipo y lo que pido")
rows = [
    ["R49G", "7\", Android 9, 2 x Gigabit, PoE", "____"],
    ["SP-R50P", "teléfono IP (menú)", "ficha completa"],
    ["HCP-R15P", "teléfono IP, cuidado de mayores", "ficha completa"],
    ["VC50B/VC50T", "cámara IP, firmware 650", "resolución, lente, grado IP"],
    ["MR01 / MR03", "radares, MR01 firmware 301", "ficha completa"],
]
c.add(Table(60, 150, ["Equipo", "Sé (página leída)", "Falta pedir"], rows, [200, 470, 410], row_h=56))
c.add(Note(60, 520, 1080, "De un equipo sin ficha leída digo que existe y pido la ficha. Resolución, lente o protección no se inventan.", kind="warn"))
c.save(out("38-paso3.svg"))
