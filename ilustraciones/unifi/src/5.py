import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 5.svg: red plana contra una red por función
c = Canvas(K(), "Red plana o una red por función")
c.add(panel(48, 128, 400, 404, "Red plana", "alert", sub="todo en 192.168.1.0/24"))
c.add(Generic(78, 210, "PCs y NVR", "oficina", icon="laptop", w=340))
c.add(Camera(78, 316, "Cámaras", "estacionamiento", w=340))
c.add(Phone(78, 422, "Celular invitado", "WiFi del café", w=340))
c.add(wire([(430, 464), (440, 464), (440, 252), (430, 252)], kind="alert", arrow=True))
c.add(text(78, 526, "el invitado llega a las PCs y al NVR", 15, 600, ALERT, FB))
c.add(panel(476, 128, 676, 404, "Una red por función", "ok", sub="cada una con su VLAN, su DHCP y su zona"))
g = c.add(Generic(664, 204, "Gateway UniFi", "DHCP por red · zonas", icon="server", w=300, dark=True))
nets = [("Staff", "VLAN 10", "10.10.10.0/24", "Internal", "info"),
        ("Invitados", "VLAN 20", "192.168.20.0/24", "Hotspot", "warn"),
        ("CCTV", "VLAN 30", "192.168.30.0/24", "Internal o CCTV", "info")]
for i, (nm, vl, sn, zn, kd) in enumerate(nets):
    x = 500 + i * 218
    c.add(rect(x, 344, 200, 170, WHITE, LINE2, rx=14))
    c.add(text(x + 16, 376, nm, 20, 600, INK, FD))
    c.add(text(x + 16, 402, vl, 16, 600, BLUE, FM))
    c.add(text(x + 16, 428, sn, 15, 500, INK2, FM))
    c.add(tag(x + 100, 484, zn, kd, size=15, mono=False))
    c.add(wire([(814, 288), (814, 316), (x + 100, 316), (x + 100, 340)], kind="logical", arrow=True))
c.add(Note(48, 552, 1104, "Desde Network 11.0 todos los sitios pasan al firewall por zonas. Cada red va a una zona y la Zone Matrix muestra qué puede hablar con qué: un celular de invitado o una cámara comprometida ya no llegan a las PCs ni al NVR.", kind="info"))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso1: crear las tres redes
c = Canvas(K(1), "Tres redes, cada una con nombre, VLAN, DHCP y zona")
c.add(Window(48, 130, 540, 330, "UniFi Network", path="Settings > Networks > Create New", rows=[("Name", "CCTV"), ("Router", "gateway UniFi"), ("Zone", "Internal o CCTV"), ("VLAN ID", "30"), ("Subred", "192.168.30.0/24"), ("DHCP", "del gateway, activo")], hl=2))
c.add(Step(48, 130, 1))
c.add(text(620, 150, "Repetilo tres veces", 20, 600, INK, FD))
c.add(Table(620, 168, ["Nombre", "VLAN", "Subred", "Zona"], [["Staff", "10", "10.10.10.0/24", "Internal"], ["Invitados", "20", "192.168.20.0/24", "Hotspot"], ["CCTV", "30", "192.168.30.0/24", "propia"]], [130, 70, 190, 142], mono_cols=(1, 2)))
c.add(Note(620, 340, 532, "Una VLAN sin DHCP es de los errores típicos: la red existe pero el cliente no recibe IP y no conecta.", title="DHCP en cada una", kind="warn"))
c.add(Note(48, 488, 1104, "Si el formulario no muestra Zone, el sitio sigue en el firewall clásico: en Settings buscá la opción de actualizar al firewall por zonas (Policy Engine). Ese es el paso 2.", kind="info"))
save(c, "5-paso1.svg")

# ---------------------------------------------------------------- 5-paso3: leer la Zone Matrix
c = Canvas(K(3), "Leé la Zone Matrix: fila origen, columna destino")
cols = ["Internal", "Gateway", "DMZ", "Hotspot"]
x0, y0, cw, rh = 250, 150, 220, 70
c.add(text(x0 - 20, y0 + 40, "origen ↓  destino →", 15, 500, INK3, FM, anchor="end"))
for j, col in enumerate(cols):
    c.add(rect(x0 + j * cw + 4, y0, cw - 8, 56, SOFT, SOFT, rx=10))
    c.add(mid(x0 + j * cw + cw / 2, y0 + 35, col, 18, 600, INK, FM))
rows = [("Hotspot", [("Allow Return", "ok"), ("Allow Return", "ok"), ("Block All", "alert"), ("Block All", "alert")]),
        ("Internal", [("", None), ("", None), ("", None), ("Allow All", "info")])]
for i, (rn, cells) in enumerate(rows):
    y = y0 + 70 + i * (rh + 14)
    c.add(rect(48, y, 186, rh, DEEP, DEEP, rx=12))
    c.add(text(68, y + 43, rn, 19, 600, WHITE, FM))
    for j, (v, kd) in enumerate(cells):
        x = x0 + j * cw
        if kd:
            bg, fg = {"ok": (OK_BG, OK), "alert": (ALERT_BG, ALERT), "info": (SOFT, BLUE)}[kd]
            c.add(rect(x + 4, y, cw - 8, rh, bg, fg, rx=12))
            c.add(mid(x + cw / 2, y + 43, v, 18, 600, fg, FM))
        else:
            c.add(rect(x + 4, y, cw - 8, rh, WHITE, LINE, rx=12, dash="5 5"))
c.add(Step(48, 220, 3))
c.add(text(250, 400, "En blanco: lo que no cubre esta lección; miralo en tu sitio.", 15, 400, INK3, FB))
c.add(Note(48, 420, 540, "El equipo de esa zona solo puede responder a conexiones que empezaron del otro lado. Un invitado contesta, pero no inicia nada hacia Internal.", title="Allow Return", kind="ok"))
c.add(Note(612, 420, 540, "Según WunderTech, una zona creada por vos llega libre al gateway y no a las otras zonas, salvo que escribas políticas. Para CCTV, una política: solo del NVR a las cámaras.", title="Tu zona CCTV", kind="info"))
save(c, "5-paso3.svg")
