"""Lección 25 · Un solo bridge."""
from _mt import *  # noqa

K = "MikroTik"

# ---------------------------------------------------------------- principal
c = Canvas(K, "Un bridge: el switch que vive dentro del router")
r = c.add(Router(330, 130, "hAP / hEX", "configuración por defecto",
                 ports=["ether1", "ether2", "ether3", "ether4", "ether5"],
                 hl={"ether1": BLUE, "ether2": CYAN, "ether3": CYAN, "ether4": CYAN, "ether5": CYAN}))
net = c.add(Internet(48, 470, "Internet", "WAN · cliente DHCP", w=240))
c.add(Cable(r.port("ether1"), net.top(), "data"))
# chips H bajo los puertos del bridge
for p in ["ether2", "ether3", "ether4", "ether5"]:
    x, y = r.port(p)
    c.add(pill(x, y + 34, "H", "ok"))
br = c.add(Box(430, 440, 330, 96, "bridge", "192.168.88.1/24 · DHCP · VLAN", dark=True))
for p in ["ether2", "ether3", "ether4", "ether5"]:
    x, y = r.port(p)
    c.add(line(x, y + 46, x, 440, CYAN, 3))
c.add(Label(595, 572, "Los puertos son esclavos: la IP va en el bridge", 16, 600, INK2, FB, anchor="middle"))
c.add(Note(812, 130, 340, "El switch chip conmuta a velocidad de cable y la CPU queda libre para rutear.", title="H = hardware offloading", kind="ok", size=15))
c.add(Note(812, 300, 340, "Fuera de los CRS1xx/2xx, solo un bridge por switch chip tiene H. El segundo bridge va por la CPU.", title="¿Un segundo bridge? No", kind="alert", size=15))
c.add(Note(812, 482, 340, "Cámaras, oficina e invitados: un bridge y VLAN para separar.", title="Para separar redes", kind="info", size=15))
save(c, "25.svg")

# ---------------------------------------------------------------- paso 3: ether5 fuera del bridge
c = Canvas(K + " · Paso 3", "Sacá ether5 del bridge y dale su propia red")
s1, a1, w1 = port_router(48, 150, ["ether1", "ether2", "ether3", "ether4", "ether5"],
                         {"ether2": CYAN, "ether3": CYAN, "ether4": CYAN, "ether5": CYAN}, "Antes", "")
c.add(s1)
c.add(caption(48, 330, "ether2 a ether5 en el bridge"))
s2, a2, w2 = port_router(640, 150, ["ether1", "ether2", "ether3", "ether4", "ether5"],
                         {"ether2": CYAN, "ether3": CYAN, "ether4": CYAN, "ether5": WARN}, "Después", "")
c.add(s2)
c.add(arrow((48 + w1 + 14, 215), (626, 215), "flow"))
c.add(caption(640, 330, "ether5 fuera del bridge"))
ex, ey = a2["ether5"]
c.add(pill(ex, ey + 30, "10.10.50.1/24", "warn"))
nb = c.add(Laptop(860, 390, "Notebook", "10.10.50.2/24", w=260))
c.add(Cable((ex, ey + 46), nb.top(), "data"))
c.add(mark(80, 430, True))
c.add(Label(112, 437, "ping 10.10.50.1 contesta: la defconf acepta ICMP", 17, 600, OK, FB))
c.add(mark(80, 492, False))
c.add(Label(112, 499, "WinBox a 10.10.50.1 no entra", 17, 600, ALERT, FB))
c.add(Note(48, 540, 760, "ether5 no está en la lista LAN y la configuración por defecto corta en input todo lo que no viene de LAN.", kind="warn", size=15))
save(c, "25-paso3.svg")

# ---------------------------------------------------------------- paso 4: ether1 como WAN
c = Canvas(K + " · Paso 4", "¿ether1 quedó dentro del bridge? Así vuelve a ser WAN")
t, h = ctable(48, 140, ["configuración", "equipos", "ether1"], [
    ["AP Router", "hAP, hEX, RB4011", ("afuera: ya es WAN", "pill:ok")],
    ["Switch", "CRS sin WiFi", ("adentro del bridge", "pill:warn")],
    ["IP Only", "CCR, RB1100", ("192.168.88.1 en ether1", "pill:gray")],
], [220, 260, 340], row_h=50)
c.add(t)
code_svg, ch = code(48, 360, 820, [
    "/interface/bridge/port/remove [find interface=ether1]",
    "/interface/list/member/add list=WAN interface=ether1",
    "/ip/dhcp-client/add interface=ether1 disabled=no",
], title="1 SACAR · 2 LISTA WAN · 3 CLIENTE DHCP", lh=40)
c.add(code_svg)
for i in range(3):
    c.add(Step(892, 411 + i * 40, i + 1))
c.add(Note(930, 140, 222, "Si no existe la lista WAN: /interface/list/add name=WAN", kind="info", size=15))
c.add(Note(930, 330, 222, "Antes de enchufar internet a un CRS: firewall (lección de cerrar puertas).", kind="warn", size=15))
c.add(Note(48, 560, 820, "Hacelo desde otro puerto y en Safe Mode: si sacás del bridge el puerto por donde entrás, te cortás.", kind="alert", size=15))
save(c, "25-paso4.svg")
