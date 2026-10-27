import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 1.svg: la configuración vive en cada controlador
c = Canvas(K(), "La configuración vive en el controlador de cada sitio")
sm = c.add(CloudBox(430, 120, "Site Manager", "unifi.ui.com", w=340))
c.add(tag(800, 152, "la puerta, no el cerebro", "info", mono=False, anchor="start"))
c.add(text(806, 190, "conecta, no guarda configuración", 15, 500, INK3, FM))
cols = [
    (48, "Sitio A · un local", "Cloud Gateway", "UCG o UDM", ["El gateway es el controlador.", "Switches y AP: host = UCG."]),
    (430, "Sitio B · consola aparte", "CloudKey", "controlador del sitio", ["Switches y AP del sitio:", "host = CloudKey."]),
    (812, "Sucursales · server central", "UniFi OS Server", "VM 10.10.10.5", ["Gateway del sitio: UXG", "o de terceros."]),
]
for x, zt, ct, cs, lines in cols:
    c.add(Zone(x, 262, 340, 232, zt))
    b = c.add(Generic(x + 20, 292, ct, cs, icon="server", w=300, dark=True))
    for i, s in enumerate(lines):
        c.add(text(x + 28, 416 + i * 26, s, 16, 400, INK2, FB))
    c.add(wire([(600, 204), (600, 236), (x + 300, 236), (x + 300, 286)], kind="logical", arrow=True))
c.add(Note(48, 520, 540, "Si cae internet en el cliente, el sitio se sigue gestionando en local, desde la red del sitio.", title="Cae internet", kind="ok"))
c.add(Note(612, 520, 540, "Los equipos siguen andando con la última configuración. Lo que perdés es cambiar, adoptar y ver estadísticas.", title="Cae el controlador", kind="warn"))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso3: entrar a UniFi OS Server
c = Canvas(K(3), "Entrá a la dirección que te da el instalador")
n = c.add(Laptop(48, 150, "Notebook", "navegador", w=250))
vm = c.add(Generic(48, 400, "VM Ubuntu 24.04", "UniFi OS Server", icon="server", w=300, dark=True))
c.add(Cable((173, 234), (173, 400), kind="data", label="https", label_at=0.5, label_dy=0))
c.add(text(48, 520, "IP de ejemplo de la VM: 10.10.10.5", 16, 500, INK2, FM))
c.add(text(48, 546, "2 vCPU · 2 GB RAM · 10 GB libres", 16, 500, INK2, FM))
flow = [("a", "Leé la dirección al final", "https, IP de la VM y el puerto", "que indica el instalador", "info"),
        ("b", "Creá el admin local", "usuario y contraseña propios,", "anotados en la ficha", "info"),
        ("c", "Entrá a UniFi Network", "y anotá dos versiones:", "UniFi OS y Network", "ok")]
for i, (k, a, b, d, kd) in enumerate(flow):
    y = 128 + i * 128
    c.add(panel(420, y, 732, 108, None, kd))
    c.add(f'<circle cx="462" cy="{y + 54}" r="20" fill="{CYAN if kd == "info" else OK}"/>' + mid(462, y + 61, k, 19, 700, WHITE, FD))
    c.add(text(500, y + 42, a, 21, 600, INK, FD))
    c.add(text(500, y + 72, b, 16, 400, INK2, FB))
    c.add(text(500, y + 94, d, 16, 400, INK2, FB))
c.add(Step(420, 128, 3))
c.add(Note(420, 520, 732, "Network 11 pide UniFi OS 6.0 o superior. Por eso se anotan las dos versiones: la de UniFi OS dice hasta dónde puede subir Network.", kind="info"))
save(c, "1-paso3.svg")

# ---------------------------------------------------------------- 1-paso4: un equipo, un solo host
c = Canvas(K(4), "Un equipo, un solo host: anotá quién manda")
c.add(text(48, 150, "Con UniFi OS Server central", 20, 600, INK, FD))
c.add(Table(48, 168, ["Equipo", "Host"], [["Gateway", "UXG, o uno de terceros"], ["Switches", "UniFi OS Server 10.10.10.5"], ["AP", "UniFi OS Server 10.10.10.5"]], [150, 380], mono_cols=(1,)))
c.add(text(624, 150, "Con Cloud Gateway en el sitio", 20, 600, INK, FD))
c.add(Table(624, 168, ["Equipo", "Host"], [["Gateway", "UCG: es el controlador"], ["Switches", "UCG"], ["AP", "UCG"]], [150, 378], mono_cols=(1,)))
c.add(Mark(72, 372, ok=False))
c.add(text(104, 366, "UDM o UCG manejado por un UniFi OS Server externo", 17, 600, ALERT, FB))
c.add(text(104, 392, "No se puede: el gateway corre su propio Network.", 16, 400, INK2, FB))
c.add(Mark(72, 446, ok=False))
c.add(text(104, 440, "El mismo AP en dos controladores a la vez", 17, 600, ALERT, FB))
c.add(text(104, 466, "Un CloudKey con Protect no gestiona los equipos que ya maneja el server.", 16, 400, INK2, FB))
c.add(Note(48, 510, 1104, "Escribí esta tabla antes de cotizar. Elegir mal el host obliga a migrar a los seis meses, y no clones la VM del server para otro cliente: los clones comparten los tokens de acceso remoto de Site Manager.", title="En la planilla del sitio", kind="warn"))
save(c, "1-paso4.svg")
