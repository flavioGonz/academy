import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

PORTS = ["1", "2", "3", "4", "5"]

# ---------------------------------------------------------------- 6.svg: las tres patas de una VLAN
c = Canvas(K(), "Una VLAN tiene tres patas: gateway, uplink y puerto")
c.add(Generic(48, 150, "Gateway ER", "VLAN 20 · 10.10.20.1/24 · DHCP", icon="server", w=420, dark=True))
c.add(badge(48 + 420 - 4, 150, "1"))
sw = c.add(Router(640, 128, "Switch JetStream", "adoptado en el sitio", ports=PORTS, hl={"1": BLUE, "5": CYAN}))
p1, p5 = sw.port("1"), sw.port("5")
c.add(wire([(258, 234), (258, 368), (p1[0], 368), p1], kind="data"))
c.add(tag(440, 400, "uplink: perfil All, VLAN 20 tagueada", "info", mono=False))
c.add(badge(250, 400, "2"))
cam = c.add(Camera(920, 440, "Cámara", "toma 10.10.20.x", w=232))
c.add(wire([p5, (p5[0], 440)], kind="data"))
c.add(tag(1020, 392, "perfil CCTV: VLAN 20 nativa", "info", mono=False, anchor="end"))
c.add(badge(758, 386, "3"))
c.add(Note(48, 470, 540, "La VLAN solo en el switch no da IP. Hacen falta las tres: red y DHCP en el gateway, uplink tagueado y puerto con la VLAN nativa.", title="Por qué la cámara no agarra IP", kind="warn"))
c.add(Note(612, 470, 284, "Si no agarra IP, revisá en ese orden: 1, 2 y 3.", title="Orden", kind="ok"))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso1: crear la red
c = Canvas(K(1), "Creá la red: interfaz, VLAN y DHCP en un formulario")
c.add(Window(48, 124, 600, 290, "Omada · sitio", path="Network Config > Network Settings > LAN > Add", rows=[
    ("Name", "CCTV"), ("VLAN", "20"), ("Gateway/Subnet", "10.10.20.1/24"), ("DHCP Server", "activado"), ("Rango", "10.10.20.100 - 10.10.20.200")], hl=1))
c.add(Step(48, 124, 1))
c.add(Note(684, 124, 468, "Al crear la red, el controlador crea su perfil de puerto, CCTV, listo para asignar en el paso 3.", title="Perfil automático", kind="ok"))
c.add(Note(684, 266, 468, "Si la VLAN la rutea otro equipo, la red se crea con DHCP Server Device en None: la interfaz y el DHCP los da ese router.", title="Con router de terceros", kind="info"))
c.add(Note(684, 430, 468, "La red por defecto queda como VLAN de gestión de los equipos Omada. Moverla es engorroso: conviene dejarla así.", title="Red de gestión", kind="warn"))
save(c, "6-paso1.svg")

# ---------------------------------------------------------------- 6-paso3: perfiles en los puertos
c = Canvas(K(3), "Uplink en All, puerto de la cámara en CCTV")
sw = c.add(Router(48, 124, "Switch JetStream", "Devices > (switch) > Ports", ports=PORTS, hl={"1": BLUE, "5": CYAN}))
c.add(Step(48, 124, 3))
c.add(Table(48, 352, ["Puerto", "Perfil", "Qué lleva"], [
    ["1 · al gateway", "All", "Red por defecto nativa, VLAN 20 tagueada"],
    ["5 · cámara o notebook", "CCTV", "VLAN 20 nativa, sin tag"],
], [250, 140, 714], row_h=48, mono_cols=(1,)))
c.add(Note(552, 124, 600, "Verificá que el uplink al gateway siga en All (trunk): así la VLAN 20 sube tagueada.", title="Paso 2", kind="info"))
c.add(Note(552, 234, 600, "No cambies el perfil del puerto por donde el switch habla con el controlador: lo podés dejar sin gestión.", title="Cuidado", kind="alert"))
c.add(code(48, 516, 520, "ipconfig /renew", 16))
c.add(code(48, 568, 520, "ipconfig | findstr IPv4   ->  10.10.20.x", 16))
c.add(Note(612, 516, 540, "Notebook en el puerto 5: si muestra 10.10.20.x, las tres patas están bien.", title="Prueba (paso 4)", kind="ok"))
save(c, "6-paso3.svg")
