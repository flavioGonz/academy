import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 6.svg: la escalera
c = new(None, "La escalera de red: el primer escalón que falla")
steps = [("1", "Interfaz con IP", "ip -br addr|ip route", "cable, DHCP o IP fija"),
         ("2", "Gateway", "ping -c3 192.168.88.1", "VLAN, gateway mal cargado"),
         ("3", "IP pública", "ping -c3 1.1.1.1", "ruta o salida del router"),
         ("4", "Nombre (DNS)", "dig debian.org +short", "revisá los nameservers"),
         ("5", "Puerto y servicio", "ss -tlnp · curl -sI", "servicio caído o filtrado")]
W = 212
for i, (n, t, cmd, hint) in enumerate(steps):
    x = 48 + i * 222
    y = 500 - i * 80
    c.add(rect(x, y, W, 600 - y, SOFT if i % 2 == 0 else WHITE, CYAN if i == 3 else LINE2, rx=12))
    c.add(badge(x + 28, y + 30, n, CYAN, r=16, size=16))
    c.add(text(x + 54, y + 36, t, 18, 600, INK, FB))
    for j, part in enumerate(cmd.split("|")):
        c.add(text(x + 16, y + 64 + j * 22, part, 15, 600, BLUE, FM))
# pistas abajo de cada columna
for i, (n, t, cmd, hint) in enumerate(steps):
    x = 48 + i * 222
    svg, _ = wrap(x + 4, 628, "Si falla: " + hint, 210, 15, 500, ALERT if i == 3 else INK2)
    c.add(svg)
c.add(Note(48, 124, 520, "Subí de abajo hacia arriba y anotá cada escalón. Si la IP pública responde y el nombre no, es DNS.", title="Sin saltear escalones", kind="info"))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso1: leer ip y la traducción
c = new(1, "ip -br addr e ip route: interfaz, IP y salida")
svg, h = term(48, 124, 700, ["$ ip -br addr",
                             ("lo        UNKNOWN  127.0.0.1/8 ::1/128", T_OUT),
                             ("ens18     UP       192.168.88.50/24", "#FFFFFF"),
                             "$ ip route",
                             ("default via 192.168.88.1 dev ens18", "#FFFFFF"),
                             ("192.168.88.0/24 dev ens18 proto kernel scope link", T_OUT)], "TERMINAL · EJEMPLO", size=16, lh=30)
c.add(svg)
cw = 16 * 0.6
X = 64
def ly(k): return 124 + 32 + 4 + (k + 0.6) * 30
c.add(f'<rect x="{X - 3}" y="{ly(2) - 21}" width="{cw * 5 + 6}" height="29" rx="5" fill="none" stroke="{T_PR}" stroke-width="2"/>')
c.add(f'<rect x="{X + cw * 10 - 3}" y="{ly(2) - 21}" width="{cw * 2 + 6}" height="29" rx="5" fill="none" stroke="{T_OK}" stroke-width="2"/>')
c.add(f'<rect x="{X + cw * 19 - 3}" y="{ly(2) - 21}" width="{cw * 16 + 6}" height="29" rx="5" fill="none" stroke="{T_WARN}" stroke-width="2"/>')
c.add(f'<rect x="{X - 3}" y="{ly(4) - 21}" width="{cw * 24 + 6}" height="29" rx="5" fill="none" stroke="{T_OK}" stroke-width="2"/>')
yb = 124 + h
c.add(callout(X + cw * 2.5, yb, 70, yb + 80, "nombre real de la interfaz", "cyan"))
c.add(callout(X + cw * 11, yb, 190, yb + 40, "enlace arriba", "ok"))
c.add(callout(X + cw * 27, yb, 380, yb + 40, "IP y máscara", "warn"))
c.add(Note(776, 124, 376, "La línea default via dice por dónde sale todo lo que no es de la red local: si falta, no hay internet aunque la IP esté bien.", title="Ruta por defecto", kind="ok"))
c.add(Table(776, 330, ["Antes (net-tools)", "Ahora (iproute2)"], [["ifconfig", "ip addr"], ["route", "ip route"], ["arp", "ip neigh"], ["netstat", "ss"]],
            [188, 188], row_h=40, mono_cols=(0, 1)))
c.add(Note(48, 540, 700, "Usá el nombre que muestra ip -br addr (ens18, enp0s31f6): eth0 ya no es la norma.", kind="info"))
save(c, "6-paso1.svg")

# ---------------------------------------------------------------- 6-paso2: netplan anotado
c = new(2, "IP fija con netplan: YAML, permisos 600 y try")
rows = ["network:", "  version: 2", "  ethernets:", "    ens18:", "      dhcp4: false", "      addresses: [192.168.88.50/24]",
        "      routes:", "        - to: default", "          via: 192.168.88.1", "      nameservers:", "        addresses: [192.168.88.1, 1.1.1.1]"]
fb, fh = fileb(48, 124, 600, "/etc/netplan/90-ies.yaml", rows, size=16, lh=34, hl=(3, 5, 8, 10))
c.add(fb)
c.add(callout(220, 124 + 44 + 3.5 * 34, 690, 196, "la interfaz de ip -br addr", "cyan"))
c.add(callout(560, 124 + 44 + 5.5 * 34, 690, 262, "IP fija con máscara", "info"))
c.add(callout(420, 124 + 44 + 8.5 * 34, 690, 330, "ruta por defecto: el gateway", "info"))
c.add(callout(600, 124 + 44 + 10.5 * 34, 690, 398, "DNS: el escalón 4", "info"))
c.add(Note(48, 584, 600, "Dos espacios por nivel, nunca tabulaciones, y espacio después de los dos puntos.", kind="warn"))
svg, h = term(690, 432, 462, ["$ sudo chmod 600 /etc/netplan/90-ies.yaml", "$ sudo netplan generate", "$ sudo netplan try"], None, size=15, lh=28)
c.add(svg)
c.add(text(690, 432 + h + 30, "try: sin Enter en 120 s, vuelve atrás solo.", 16, 600, OK, FB))
save(c, "6-paso2.svg")
