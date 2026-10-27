"""Lección 13 · IP fija."""
from _comun_12_22 import *

K = "MikroTik · Lección 13"

# ---------------------------------------------------------------- principal
c = Canvas(K, "IP fija: cuatro datos del proveedor, tres comandos")
isp = c.add(Generic(48, 140, "Equipo del proveedor", "gateway 203.0.113.9", icon="globe", w=330))
rt = c.add(Box(822, 130, 330, 104, "MikroTik", "ether1 · 203.0.113.10/29", dark=True))
c.add(Cable(isp.right(), rt.left(), "data", label="cable a ether1", label_dy=-14))

rows = [
    ("Dirección y máscara", "203.0.113.10/29", "/ip/address/add address=203.0.113.10/29", "interface=ether1"),
    ("Gateway", "203.0.113.9", "/ip/route/add dst-address=0.0.0.0/0", "gateway=203.0.113.9"),
    ("DNS", "1.1.1.1 · 9.9.9.9", "/ip/dns/set servers=1.1.1.1,9.9.9.9", ""),
]
y = 282
c.add(Label(48, y - 14, "DATO QUE ENTREGA EL PROVEEDOR", 14, 600, INK3, FM))
c.add(Label(560, y - 14, "COMANDO EN ROUTEROS 7", 14, 600, INK3, FM))
for i, (k, v, cmd1, cmd2) in enumerate(rows):
    yy = y + i * 104
    c.add(panel(48, yy, 420, 84, None, "info"))
    c.add(text(70, yy + 36, k, 18, 600, INK))
    c.add(mono(70, yy + 64, v, 16, BLUE, 600))
    c.add(Arrow((478, yy + 42), (548, yy + 42), bend="straight"))
    c.add(f'<rect x="560" y="{yy}" width="592" height="84" rx="14" fill="#03213C"/>')
    c.add(mono(582, yy + (36 if cmd2 else 49), cmd1, 15, "#D9E9F8", 400))
    if cmd2:
        c.add(mono(582, yy + 62, "  " + cmd2, 15, "#D9E9F8", 400))
c.add(Note(48, 596, 1104, "Antes de cargarla, deshabilitá el cliente DHCP de ether1 para que no compitan por la interfaz.", kind="warn", size=16))
save(c, "13.svg")

# ---------------------------------------------------------------- paso 2: DHCP vs fija
c = Canvas(K + " · Paso 2", "Apagá el cliente DHCP antes de cargar la IP fija")
for j, (title, kind, dh, dhk, ok) in enumerate([
        ("Si los dejás juntos", "alert", "dhcp-client · activo", "alert", False),
        ("Como tiene que quedar", "ok", "dhcp-client · disabled", "gray", True)]):
    x = 48 + j * 574
    c.add(panel(x, 140, 530, 340, title, kind))
    c.add(Mark(x + 490, 174, ok))
    c.add(f'<rect x="{x + 30}" y="{210}" width="150" height="70" rx="12" fill="{DEEP}"/>')
    c.add(mono(x + 105, 252, "ether1", 18, WHITE, 600, anchor="middle"))
    c.add(Cable((x + 180, 245), (x + 250, 210), "logical", arrow=False))
    c.add(Cable((x + 180, 245), (x + 250, 300), "logical", arrow=False))
    c.add(Chip(x + 256, 216, dh, dhk))
    c.add(Chip(x + 256, 306, "203.0.113.10/29 · fija", "blue" if ok else "warn"))
txt_bad = "El cliente DHCP y la IP fija compiten por la misma interfaz: dos direcciones y dos rutas por defecto posibles en ether1."
txt_ok = "Una sola fuente: dirección, ruta y DNS cargados a mano, con comment=\"WAN fija\" para encontrarlos después."
c.add(para(78, 380, txt_bad, 470, 17, INK, 500))
c.add(para(652, 380, txt_ok, 470, 17, INK, 500))
c.add(Terminal(48, 520, 1104, ["/ip/dhcp-client/disable [find interface=ether1]"], title="PRIMERO ESTO"))
save(c, "13-paso2.svg")

# ---------------------------------------------------------------- paso 3: verificar por capas
c = Canvas(K + " · Paso 3", "Verificá por capas: cada falla apunta a otra cosa")
xs = [48, 340, 632, 924]
nodes = [("MikroTik", "203.0.113.10", "server", True), ("Gateway", "203.0.113.9", "globe", False),
         ("Internet", "1.1.1.1", "globe", False), ("Nombre", "mikrotik.com", "cloud", False)]
bx = []
for x, (t, s, ic, dk) in zip(xs, nodes):
    bx.append(c.add(Generic(x, 140, t, s, icon=ic, w=228, dark=dk)))
tests = [
    ("/ping 203.0.113.9", "cable, máscara o VLAN"),
    ("/ping 1.1.1.1", "ruta o proveedor"),
    (":put [:resolve mikrotik.com]", "DNS"),
]
for i, (cmd, cause) in enumerate(tests):
    y = 290 + i * 100
    x_end = xs[i + 1] + 114
    c.add(Arrow((162, y), (x_end, y), bend="straight", kind="flow"))
    c.add(line(x_end, 224, x_end, y - 12, LINE2, 2, "4 6"))
    c.add(badge(162, y, i + 1))
    c.add(mono(196, y - 14, cmd, 15, INK, 600))
    c.add(Chip(x_end + 20, y + 34, "si falla: " + cause, "alert", mono=False, anchor="start") if x_end + 20 + (len(cause) + 10) * 8.4 + 26 < 1160 else Chip(x_end - 10 - ((len(cause) + 10) * 8.4 + 26), y + 34, "si falla: " + cause, "alert", mono=False))
c.add(Note(48, 596, 1104, "Si las tres pasan, mirá /ip/route/print where dst-address=0.0.0.0/0: la ruta por defecto tiene que estar activa.", kind="ok", size=16))
save(c, "13-paso3.svg")
