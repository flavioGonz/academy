"""Lección 26 · Asignar IP."""
from _mt import *  # noqa

K = "MikroTik · Lección 26"

# ---------------------------------------------------------------- principal
c = Canvas(K, "Una IP: dirección, máscara e interfaz")
c.add(rect(48, 130, 640, 110, WHITE, LINE2, 2, 16))
c.add(text(72, 168, "/ip/address/add", 17, 500, BLUE, FM))
c.add(text(72, 214, "address=10.10.20.1/24 interface=ether5", 22, 600, INK, FM))
c.add(caption(48, 286, "Lo que RouterOS calcula solo"))
t, h = ctable(48, 304, ["qué", "valor"], [
    ["red", "10.10.20.0"],
    ["hosts", "10.10.20.1 a 10.10.20.254"],
    ["broadcast", "10.10.20.255"],
    ["ruta conectada", ("DAc 10.10.20.0/24 ether5", "pill:cyan")],
], [210, 430], row_h=46, col_fonts=[FB, FM])
c.add(t)
c.add(caption(740, 146, "¿Dónde va la IP?"))
items = [("En el bridge", True, "la LAN de la defconf: 192.168.88.1/24"),
         ("En una interfaz VLAN", True, "vlan20-cctv sobre el bridge"),
         ("En un puerto ruteado", True, "ether5 fuera del bridge"),
         ("En un puerto dentro del bridge", False, "es esclavo: termina en el bridge")]
for i, (tt, ok, sub) in enumerate(items):
    y = 180 + i * 92
    c.add(rect(740, y, 412, 78, OK_BG if ok else ALERT_BG, OK_BG if ok else ALERT_BG, 1.5, 14))
    c.add(mark(774, y + 39, ok))
    c.add(text(806, y + 34, tt, 17, 600, INK, FB))
    c.add(text(806, y + 58, sub, 14, 400, INK2, FM))
c.add(Label(48, 560, "Una interfaz puede tener varias IP, o ninguna.", 17, 500, INK2))
save(c, "26.svg")

# ---------------------------------------------------------------- paso 2: segunda IP temporal
c = Canvas(K + " · Paso 2", "Dos IP en el bridge para llegar a un equipo de fábrica")
r = c.add(Box(420, 125, 360, 175, "MikroTik · bridge", "", dark=True))
c.add(pill(510, 262, "192.168.88.1/24", "cyan"))
c.add(pill(690, 262, "192.168.1.254/24", "warn"))
nb = c.add(Laptop(60, 400, "Notebook", "192.168.88.254", w=270))
eq = c.add(Generic(860, 400, "Equipo de fábrica", "192.168.1.x", icon="camera", w=290))
c.add(Cable(nb.top(), (510, 300), "data"))
c.add(Cable(eq.top(), (690, 300), "data"))
c.add(Note(380, 350, 440, "Dos rutas conectadas, una por cada red. Desde la notebook entrás al equipo a través del router.", kind="info", size=15))
c.add(Note(60, 540, 1090, "Temporal: cuando el equipo ya tiene su IP definitiva, /ip/address/remove [find comment=\"lab temporal\"].", title="Comentala y borrala al terminar", kind="warn", size=15))
save(c, "26-paso2.svg")

# ---------------------------------------------------------------- paso 4: DHCP en cuatro piezas
c = Canvas(K + " · Paso 4", "El servidor DHCP son cuatro piezas")
pieces = [("1 · IP en la interfaz", "ether5", "10.10.20.1/24"),
          ("2 · Pool", "pool-cctv", ".100 a .199"),
          ("3 · Red", "gateway y DNS", "10.10.20.1"),
          ("4 · Servidor", "dhcp-cctv", "ether5 + pool")]
W, G, X0, Y0 = 250, 34, 48, 150
for i, (tt, a, b) in enumerate(pieces):
    x = X0 + i * (W + G)
    c.add(rect(x, Y0, W, 130, WHITE if i < 3 else DEEP, LINE2 if i < 3 else DEEP, 2, 16))
    col = INK if i < 3 else WHITE
    c.add(text(x + 18, Y0 + 38, tt, 18, 600, col, FD))
    c.add(text(x + 18, Y0 + 76, a, 15, 500, BLUE if i < 3 else CYAN, FM))
    c.add(text(x + 18, Y0 + 104, b, 15, 400, INK2 if i < 3 else "#9FC3E3", FM))
    if i < 3:
        c.add(arrow((x + W + 4, Y0 + 65), (x + W + G - 4, Y0 + 65)))
cam = c.add(Camera(700, 400, "Cámara en ether5", "recibe 10.10.20.100", w=300))
c.add(arrow((X0 + 3 * (W + G) + W / 2, Y0 + 130), cam.top(), "ok", bend="straight"))
c.add(Note(48, 360, 600, "El pool no incluye la IP del router. Del .2 al .99 queda libre para IP fijas.", title="Pool con lugar para las fijas", kind="ok", size=15))
c.add(Note(48, 510, 600, "Si un equipo tiene que tener siempre la misma IP: make-static sobre su lease.", title="Reserva", kind="info", size=15))
save(c, "26-paso4.svg")
