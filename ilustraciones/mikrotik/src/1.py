"""Lección 1 · Entrar sin romper: principal + pasos 1, 2 y 4."""
from _mt import *

K = "MikroTik · Lección 1"
PORTS = ["ether1", "ether2", "ether3", "ether4", "ether5"]

# ------------------------------------------------------------------ 1.svg principal
c = Canvas(K, "¿Por dónde entro a un MikroTik recién sacado de la caja?")
r = c.add(Router(48, 140, "Router de laboratorio", "RouterOS 7 · config de fábrica", ports=PORTS,
                 hl={"ether1": WARN, "ether2": CYAN}))
x1, yb = r.port("ether1")
x2, _ = r.port("ether2")
# llave LAN debajo de ether2..ether5
lx0, lx1 = r.port("ether2")[0] - 34, r.port("ether5")[0] + 34
c.add(f'<path d="M{lx0} {yb + 14}v10H{lx1}v-10" fill="none" stroke="{INK3}" stroke-width="2"/>')
c.add(pill(r.port("ether4")[0], yb + 58, "LAN · bridge", "gray"))
c.add(pill(x1, yb + 34, "WAN", "warn"))
# notebook mal ubicada en ether1
c.add(Cable((x1, yb + 54), (x1, 420), kind="alert", arrow=False))
c.add(mark(x1, 438, ok=False))
c.add(text(x1, 490, "ether1 no:", 16, 600, ALERT, FB, anchor="middle"))
c.add(text(x1, 512, "es la WAN", 16, 600, ALERT, FB, anchor="middle"))
# notebook bien
n = c.add(Laptop(232, 430, "Notebook", "WinBox", hl=CYAN, w=240))
c.add(Cable((n.x + 120, n.y), (x2 + 0.1, yb), kind="data"))
c.add(mark(n.x + 220, n.y, ok=True))
c.add(Label(232, 560, "Cualquier puerto LAN sirve (ether2 a ether5).", 16, 500, OK))

# dos caminos a la derecha
X = 600
c.add(caption(X, 160, "Dos caminos para entrar"))
c.add(card(X, 178, 552, 168, "Por IP · 192.168.88.1",
           "El DHCP de fábrica le da a la notebook una IP de esa red. Es el camino normal cuando el equipo tiene la config por defecto.",
           kind="info", icon="globe"))
c.add(card(X, 362, 552, 192, "Por MAC · Neighbors",
           "No necesita IP: WinBox habla con el equipo por la dirección física. Te salva si la IP no responde, figura 0.0.0.0 o el equipo no trae config (los CCR).",
           kind="ok", icon="key"))
c.add(Note(X, 572, 552, "La MAC no cruza routers: tenés que estar en el mismo segmento de red que el equipo.", kind="warn", size=15))
save(c, "1.svg")

# ------------------------------------------------------------------ 1-paso1.svg
c = Canvas(K + " · Paso 1", "Conectá la notebook a ether2 y entrá por la MAC")
r = c.add(Router(48, 140, "Router de laboratorio", "RouterOS 7", ports=PORTS, hl={"ether2": CYAN, "ether1": WARN}))
x1, yb = r.port("ether1")
c.add(pill(x1, yb + 40, "WAN", "warn"))
n = c.add(Laptop(150, 450, "Notebook", "WinBox", hl=CYAN, w=250))
c.add(Cable((n.x + 125, n.y), r.port("ether2"), kind="data", label="cable de red", label_at=.5, label_dy=6))
c.add(Step(r.port("ether2")[0] + 34, yb + 30, 1))
c.add(wrap(48, 580, "No hace falta configurar IP en la notebook para este paso.", 440, 16, 500, INK2)[0])

# ventana WinBox
WX, WY, WW, WH = 540, 128, 612, 500
c.add(rect(WX, WY, WW, WH, WHITE, LINE2, 2, 14))
c.add(f'<path d="M{WX} {WY + 14}a14 14 0 0 1 14 -14h{WW - 28}a14 14 0 0 1 14 14v26h-{WW}z" fill="{SOFT}"/>')
for i in range(3):
    c.add(f'<circle cx="{WX + 20 + 18 * i}" cy="{WY + 20}" r="5" fill="{LINE2}"/>')
c.add(text(WX + 76, WY + 26, "WinBox", 15, 600, INK2))
# formulario de login
fy = WY + 64
for i, (k, v, hl) in enumerate([("Connect To", "AA:BB:CC:00:11:22", True), ("Login", "admin", False), ("Password", "vacía o la de la etiqueta", False)]):
    yy = fy + i * 44
    c.add(text(WX + 24, yy + 22, k, 15, 500, INK2))
    c.add(rect(WX + 150, yy, WW - 290, 34, SOFT if hl else WHITE, CYAN if hl else LINE2, 2 if hl else 1.5, 8))
    c.add(text(WX + 164, yy + 22, v, 15, 500 if hl else 400, INK if hl else INK3, FM))
c.add(rect(WX + WW - 122, fy + 88, 100, 36, BLUE, BLUE, 0, 8))
c.add(text(WX + WW - 72, fy + 112, "Connect", 15, 600, WHITE, FB, anchor="middle"))
# pestaña Neighbors
ty = fy + 150
c.add(rect(WX + 18, ty, 120, 32, DEEP, DEEP, 0, 8))
c.add(text(WX + 78, ty + 21, "Neighbors", 14, 600, WHITE, FB, anchor="middle"))
c.add(line(WX + 18, ty + 32, WX + WW - 18, ty + 32, CYAN, 2))
c.add(Table(WX + 18, ty + 44, ["MAC Address", "IP Address", "Identity"],
            [["AA:BB:CC:00:11:22", "192.168.88.1", "MikroTik"]], [236, 178, 162], hl_row=0, mono_cols=(0, 1)))
c.add(arrow((WX + 140, ty + 92), (WX + 300, fy + 40), kind="logical"))
c.add(text(WX + 316, ty - 2, "clic en la MAC", 15, 600, INK3, FM))
c.add(Note(WX + 18, ty + 140, WW - 36, "Si la IP no contesta o figura 0.0.0.0, la MAC igual entra: WinBox habla con el equipo en capa 2.", kind="info", size=15))
save(c, "1-paso1.svg")

# ------------------------------------------------------------------ 1-paso2.svg
c = Canvas(K + " · Paso 2", "Leé qué trae de fábrica antes de tocar nada")
cols = [
    ("/interface/list/member/print", "Listas de interfaces", ["WAN  →  ether1", "LAN  →  bridge"], "Las reglas apuntan a las listas, no a los puertos."),
    ("/ip/firewall/filter/print", "Firewall de fábrica", ["defconf: drop all not", "  coming from LAN", "defconf: drop all from", "  WAN not DSTNATed"], "Protegen al router y a la LAN de lo que llega por WAN."),
    ("/ip/address/print", "Direcciones IP", ["192.168.88.1/24", "  en bridge"], "La IP de gestión vive en el bridge, no en un puerto."),
]
for i, (cmd, ttl, res, foot) in enumerate(cols):
    x = 48 + i * 376
    c.add(rect(x, 132, 352, 46, "#03213C", "#03213C", 0, 10))
    c.add(text(x + 16, 161, cmd, 14.5 if len(cmd) > 26 else 15, 500, CYAN_T, FM))
    c.add(arrow((x + 176, 182), (x + 176, 212), kind="flow"))
    c.add(rect(x, 216, 352, 216, WHITE, LINE2, 2, 14))
    c.add(text(x + 18, 248, ttl, 18, 600, INK, FD))
    for j, s in enumerate(res):
        c.add(text(x + 18, 284 + j * 24, s, 15, 500, BLUE if not s.startswith("  ") else INK2, FM))
    c.add(wrap(x + 18, 390 - (0 if len(res) > 2 else 0), foot, 316, 15, 400, INK3)[0] if len(res) <= 2 else wrap(x + 18, 392, foot, 316, 15, 400, INK3)[0])
# router resumido abajo
svg, anc, w = port_router(250, 456, PORTS, colors={"ether1": WARN, "ether2": BLUE, "ether3": BLUE, "ether4": BLUE, "ether5": BLUE},
                          name="Así queda el equipo", sub="config de fábrica")
c.add(svg)
c.add(pill(anc["ether1"][0], 632, "WAN", "warn"))
c.add(f'<path d="M{anc["ether2"][0] - 30} 596v8H{anc["ether5"][0] + 30}v-8" fill="none" stroke="{INK3}" stroke-width="2"/>')
c.add(pill((anc["ether2"][0] + anc["ether5"][0]) / 2, 632, "LAN · bridge · 192.168.88.1", "gray"))
c.add(Note(820, 456, 332, "Los CCR pueden venir sin nada de esto: ahí bridge, IP y DHCP se arman a mano.", kind="warn", size=15))
save(c, "1-paso2.svg")

# ------------------------------------------------------------------ 1-paso4.svg (Safe Mode)
c = Canvas(K + " · Paso 4", "Safe Mode: si la sesión se cae, el router deshace")
steps = [("Ctrl+X", "Entrás a Safe Mode", "[admin@MikroTik] <SAFE>"),
         ("cambio", "Agregás la regla", 'comment="prueba-safe"'),
         ("Ctrl+D", "Salís sin confirmar", "o se corta el cable"),
         ("undo", "El router deshace", "la regla desaparece")]
for i, (tag, t, s) in enumerate(steps):
    x = 48 + i * 282
    hl = CYAN if i < 2 else (WARN if i == 2 else OK)
    c.add(rect(x, 150, 252, 140, WHITE, hl, 2.5, 16))
    c.add(pill(x + 20, 186, tag, "dark", anchor="start"))
    c.add(text(x + 20, 236, t, 18, 600, INK, FD))
    c.add(text(x + 20, 266, s, 14 if len(s) > 22 else 15, 500, INK3, FM))
    if i < 3:
        c.add(arrow((x + 256, 225), (x + 278, 225), kind="flow"))
# dos salidas
c.add(card(48, 330, 540, 130, "¿Querés que el cambio quede?",
           "Apretá Ctrl+X otra vez antes de salir: dejás Safe Mode y los cambios se guardan.", kind="ok", icon="check"))
c.add(card(612, 330, 540, 130, "¿Te cortaste el acceso?",
           "No hagas nada: cuando la sesión muere, el router vuelve solo a como estaba antes de Ctrl+X.", kind="info", icon="shield"))
c.add(Note(48, 494, 1104, "Safe Mode recuerda hasta 100 acciones. Si pegás un script largo y se pasa, sale solo del modo seguro y ya no deshace nada: trabajá de a pasos chicos.", title="Ojo con los scripts largos", kind="warn", size=16))
save(c, "1-paso4.svg")
