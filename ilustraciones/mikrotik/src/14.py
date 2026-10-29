"""Lección 14 · Cliente DHCP."""
from _comun_12_22 import *

K = "MikroTik"

# ---------------------------------------------------------------- principal
c = Canvas(K, "Qué instala el cliente DHCP cuando queda bound")
mod = c.add(Generic(48, 250, "Módem u otro router", "servidor DHCP", icon="server", w=290))
rt = c.add(Box(440, 210, 290, 160, "MikroTik", "dhcp-client en ether1", dark=True))
c.add(Chip(585, 346, "status: bound", "ok", anchor="middle"))
c.add(Cable(mod.right(), rt.left(), "data", label="ether1", label_dy=-14))
outs = [
    ("Dirección", "dinámica en ether1"),
    ("Ruta por defecto", "default-route-distance=1"),
    ("DNS", "use-peer-dns=yes"),
    ("NTP", "use-peer-ntp=yes"),
]
for i, (t, s) in enumerate(outs):
    y = 130 + i * 104
    c.add(panel(822, y, 330, 84, None, "info"))
    c.add(text(844, y + 36, t, 18, 600, INK))
    c.add(mono(844, y + 62, s, 15, BLUE, 500))
    c.add(Arrow((rt.x + rt.w + 6, rt.y + 70), (816, y + 42), kind="flow"))
c.add(Note(48, 572, 1104, "Al perder el lease o deshabilitar el cliente, se borran la dirección y las rutas dinámicas que había instalado.", kind="info", size=16))
save(c, "14.svg")

# ---------------------------------------------------------------- paso 2: distancia
c = Canvas(K + " · Paso 2", "La distancia decide qué ruta por defecto gana")
for j, (title, kind, d1, d2, act2, body) in enumerate([
        ("Distancia 1 y 1", "warn", "distance=1", "distance=1", True, "Las dos rutas activas: el tráfico se reparte (ECMP). No es un respaldo."),
        ("Distancia 1 y 2", "ok", "distance=1", "distance=2", False, "Gana la de menor distancia. La de 2 queda esperando: es el respaldo.")]):
    x = 48 + j * 574
    c.add(panel(x, 130, 530, 420, title, kind))
    r = f'<rect x="{x + 30}" y="300" width="130" height="70" rx="12" fill="{DEEP}"/>' + mono(x + 95, 342, "MikroTik", 16, WHITE, 600, anchor="middle")
    c.add(r)
    for k, (nm, dd, active) in enumerate([("WAN 1", d1, True), ("WAN 2", d2, act2)]):
        yy = 200 + k * 150
        c.add(Cable((x + 160, 335), (x + 330, yy + 30), "ok" if active else "logical", arrow=True))
        c.add(Generic(x + 336, yy, nm, dd, icon="globe", w=170))
        c.add(Chip(x + 336, yy + 112, "activa" if active else "en espera", "ok" if active else "gray", mono=False))
    c.add(para(x + 30, 506, body, 470, 17, INK, 500))
c.add(Terminal(48, 572, 1104, ["/ip/dhcp-client/set [find interface=ether1] default-route-distance=2"], title="SI ETHER1 ES EL RESPALDO"))
save(c, "14-paso2.svg")

# ---------------------------------------------------------------- paso 4: doble NAT
c = Canvas(K + " · Paso 4", "¿Hay otro NAT adelante? Compará dos direcciones")
net = c.add(Internet(48, 150, "Internet", "", w=200))
mod = c.add(Generic(330, 150, "Módem en modo router", "NAT 1", icon="server", w=290))
rt = c.add(Box(702, 140, 220, 104, "MikroTik", "NAT 2", dark=True))
lan = c.add(Generic(1000, 150, "LAN", "", icon="laptop", w=152))
c.add(Cable(net.right(), mod.left(), "data"))
c.add(Cable(mod.right(), rt.left(), "data"))
c.add(Cable(rt.right(), lan.left(), "data"))
c.add(Chip(475, 290, "public-address (IP Cloud)", "blue", anchor="middle"))
c.add(Chip(812, 290, "address del cliente DHCP", "cyan", anchor="middle"))
c.add(Table(48, 340, ["address del cliente DHCP", "qué significa"], [
    ["igual a public-address", "IP pública directa en ether1"],
    ["10.x · 172.16-31.x · 192.168.x", "doble NAT: módem en modo router"],
    ["100.64.0.0/10", "CGNAT del proveedor (lección 27)"],
], [470, 634], hl_row=None, row_h=52, mono_cols=(0,)))
c.add(Terminal(48, 560, 540, ["/ip/dhcp-client/print detail", "/ip/cloud/print"], title="COMPARÁ"))
c.add(Note(612, 560, 540, "Con doble NAT o CGNAT, no prometas acceso remoto por la IP: hace falta un túnel (lecciones 19 y 20).", kind="warn", size=16))
save(c, "14-paso4.svg")
