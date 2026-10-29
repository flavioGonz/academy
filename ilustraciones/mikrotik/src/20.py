"""Lección 20 · Concentrador CHR."""
from _comun_12_22 import *

K = "MikroTik"

# ---------------------------------------------------------------- principal
c = Canvas(K, "Concentrador CHR: los sitios llaman al VPS")
c.add(Zone(380, 132, 440, 190, "VPS con IP pública"))
hub = c.add(Box(410, 160, 380, 146, "CHR · wg-hub", "198.51.100.20 · UDP 13231", dark=True))
c.add(Chip(600, 288, "túnel 10.10.10.1/24", "cyan", anchor="middle"))
nb = c.add(Laptop(880, 186, "Notebook", "peer propio", w=272))
c.add(Arrow(nb.left(), (hub.x + hub.w + 6, hub.y + 62), kind="flow", bend="straight"))
c.add(Zone(48, 400, 560, 190, "sitios detrás de NAT o CGNAT"))
s1 = c.add(Generic(68, 446, "sitio-lab", "10.10.10.2", icon="server", w=250))
s2 = c.add(Generic(338, 446, "otro sitio", "10.10.10.x", icon="server", w=250))
c.add(Arrow(s1.top(), (hub.x + 80, hub.y + hub.h + 6), "túnel saliente", kind="flow", label_at=.45, label_dy=0))
c.add(Arrow(s2.top(), (hub.x + 200, hub.y + hub.h + 6), kind="flow"))
c.add(Note(640, 380, 512, "El túnel lo abre el sitio hacia afuera: el CGNAT del cliente deja de importar. Desde la notebook, WinBox a 10.10.10.2 a través del hub. Sirve también para MikroTik MIPS sin Back To Home.", title="Por qué funciona", kind="ok", size=15))
c.add(Note(640, 560, 512, "Licencia Free: 1 Mbps de subida por interfaz. Alcanza para WinBox y monitoreo, no para video.", kind="warn", size=15))
save(c, "20.svg")

# ---------------------------------------------------------------- paso 1: endurecer
c = Canvas(K + " · Paso 1", "El CHR arranca con admin sin contraseña: endurecelo")
items = [
    ("Creá tu usuario", "/user/add name=tecnico-lucia group=full", "info"),
    ("Entrá con ese usuario y probá", "recién ahí seguí", "warn"),
    ("Deshabilitá admin", "/user/disable admin", "info"),
    ("Apagá servicios que no usás", "telnet, ftp, www, api, api-ssl", "info"),
    ("WinBox y SSH solo desde la oficina y el túnel", "available-from=203.0.113.50/32,10.10.10.0/24", "info"),
    ("MAC server, discovery y DNS remoto", "en none / allow-remote-requests=no", "info"),
]
for i, (t, s, k) in enumerate(items):
    y = 136 + i * 74
    c.add(panel(48, y, 700, 62, None, k))
    c.add(badge(84, y + 31, i + 1, WARN if k == "warn" else CYAN))
    c.add(text(116, y + 27, t, 17, 600, INK))
    c.add(mono(116, y + 50, s, 14, INK3, 500))
c.add(Note(784, 136, 368, "Arranca en una IP pública con admin y sin contraseña: endurecerlo es el primer paso, no el último.", title="Día uno", kind="alert"))
c.add(Note(784, 330, 368, "Si deshabilitás admin antes de probar tu usuario, te podés quedar afuera del VPS.", title="El orden importa", kind="warn"))
c.add(Note(784, 494, 368, "Después, el firewall de input (paso 2): lista WAN creada a mano y drop del resto.", kind="info", size=15))
save(c, "20-paso1.svg")

# ---------------------------------------------------------------- paso 5: el sitio llama
c = Canvas(K + " · Paso 5", "El sitio abre el túnel y lo mantiene con keepalive")
site = c.add(Box(48, 180, 300, 124, "Router del sitio", "wg-central · 10.10.10.2", dark=True))
cg = c.add(Generic(450, 200, "NAT o CGNAT", "del proveedor", icon="shield", w=250))
hub = c.add(Box(852, 180, 300, 124, "CHR", "wg-hub · 10.10.10.1", dark=True))
c.add(Cable(site.right(), cg.left(), "data"))
c.add(Cable(cg.right(), hub.left(), "data"))
c.add(Arrow((site.x + 150, 158), (hub.x + 150, 158), "sale hacia 198.51.100.20:13231", kind="ok", bend="straight", label_dy=-10))
c.add(Arrow((site.x + 150, 334), (hub.x + 150, 334), "keepalive cada 25 s: el NAT queda abierto", kind="logical", bend="straight", label_dy=-10))
c.add(Table(48, 384, ["en el peer", "router del sitio", "CHR (hub)"], [
    ["endpoint-address", "198.51.100.20", "no lleva"],
    ["persistent-keepalive", "25s", "no lleva"],
    ["allowed-address", "10.10.10.0/24", "10.10.10.2/32"],
], [368, 368, 368], mono_cols=(0, 1, 2), row_h=46))
c.add(Note(48, 584, 1104, "Sin keepalive, el NAT del proveedor olvida la conexión y el hub ya no puede llegar al sitio hasta que el sitio vuelva a hablar.", kind="info", size=15))
save(c, "20-paso5.svg")
