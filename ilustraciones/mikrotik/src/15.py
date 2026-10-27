"""Lección 15 · PPPoE con Antel."""
from _comun_12_22 import *

K = "MikroTik · Lección 15"

# ---------------------------------------------------------------- principal: capas de la WAN PPPoE
c = Canvas(K, "Con PPPoE, la WAN pasa a ser pppoe-antel")
net = c.add(Internet(48, 150, "Antel", "internet", w=230))
ont = c.add(Generic(48, 330, "ONT de Antel", "modo puente", icon="server", w=230, hl=CYAN))
c.add(Cable(net.bottom(), ont.top(), "data"))
c.add(Note(48, 460, 300, "El modo puente se pide a Antel (MiAntel o 121); en fibra lo cambia el proveedor de forma remota.", kind="info", size=15))

# router con capas
RX, RY, RW, RH = 440, 130, 712, 420
c.add(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="22" fill="{DEEP}"/>')
c.add(text(RX + 28, RY + 40, "MikroTik · RouterOS 7", 21, 600, WHITE, FD))
c.add(text(RX + 28, RY + 64, "cada capa se apoya en la de abajo", 15, 400, "#9FC3E3", FM))
LX, LW = RX + 28, RW - 56
# capa 4: lo que usa la WAN
c.add(pill(LX, RY + 90, LW, 52, "lista WAN · masquerade · reglas  →  apuntan a pppoe-antel", "#0B3A66", WHITE, 15, FM, 600, stroke="#4E7396"))
# capa 3: pppoe
c.add(f'<rect x="{LX}" y="{RY + 160}" width="{LW}" height="78" rx="12" fill="{CYAN}"/>')
c.add(text(LX + 20, RY + 192, "pppoe-antel  (interfaz lógica)", 17, 600, WHITE, FM))
c.add(text(LX + 20, RY + 220, "usuario y contraseña · IP, ruta y DNS · MTU/MRU 1492", 15, 500, WHITE, FB))
# capa 2: vlan a confirmar
c.add(f'<rect x="{LX}" y="{RY + 256}" width="{LW}" height="62" rx="12" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2.5" stroke-dasharray="8 6"/>')
c.add(text(LX + 20, RY + 293, "vlan-wan · a confirmar con Antel (solo si la piden)", 16, 600, WARN, FM))
# capa 1: ether1
c.add(f'<rect x="{LX}" y="{RY + 336}" width="{LW}" height="56" rx="12" fill="#0B3A66" stroke="#4E7396" stroke-width="2"/>')
c.add(text(LX + 20, RY + 370, "ether1 · puerto físico, sin IP ni cliente DHCP", 16, 600, WHITE, FM))
c.add(Cable(ont.right(), (RX, RY + 364), "data", label="cable", label_dy=-14))
c.add(para(RX, 590, "Ninguna fuente leída confirma VLAN con el ONT en puente: probá primero sin VLAN (pppoe-client/scan) y confirmalo con Antel.", RW, 16, WARN, 500))
save(c, "15.svg")

# ---------------------------------------------------------------- paso 1: conexión y scan
c = Canvas(K + " · Paso 1", "ONT a ether1, y buscá el concentrador PPPoE")
ont = c.add(Generic(48, 150, "ONT de Antel", "puerto LAN · en puente", icon="server", w=300, hl=CYAN))
r = c.add(Router(470, 130, "RouterBOARD", "RouterOS 7", ports=["ether1", "ether2", "ether3", "ether4", "ether5"], hl={"ether1": CYAN}))
c.add(Cable(ont.bottom(), r.port("ether1"), "data", label="cable de red", label_at=0.55, label_dy=0))
c.add(Step(r.port("ether1")[0] + 30, r.port("ether1")[1] + 24, 1))
nb = c.add(Laptop(860, 340, "Notebook", "WinBox", w=260))
c.add(Cable(r.port("ether2"), nb.top(-60), "data", label="config", label_at=0.5, label_dy=0))
c.add(Chip(r.port("ether1")[0], 366, "WAN", "warn", anchor="middle"))
c.add(Terminal(48, 396, 640, ["/ip/dhcp-client/disable [find interface=ether1]", "/interface/pppoe-client/scan interface=ether1"], title="PASO 1 · TERMINAL"))
c.add(panel(48, 530, 540, 120, "Aparece un ac-name", "ok"))
c.add(para(68, 594, "El PPPoE responde sin VLAN: seguí con el paso 2.", 500, 16, INK, 500))
c.add(panel(612, 530, 540, 120, "No aparece nada", "warn"))
c.add(para(632, 594, "Pedile a Antel el dato de VLAN antes de seguir.", 500, 16, INK, 500))
save(c, "15-paso1.svg")

# ---------------------------------------------------------------- paso 5: MTU y MSS
c = Canvas(K + " · Paso 5", "PPPoE ocupa 8 bytes: MTU 1492 y MSS ajustado")
c.add(Label(48, 158, "LO QUE ENTRA EN UNA TRAMA ETHERNET (1500 BYTES DE CARGA)", 14, 600, INK3, FM))
X0, W = 48, 1104
sc = W / 1500
hdr = 8 * sc * 12  # cabecera exagerada para que se vea; la etiqueta da el número real
c.add(f'<rect x="{X0}" y="180" width="{W}" height="76" rx="12" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(f'<rect x="{X0}" y="180" width="{hdr:.0f}" height="76" rx="12" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/>')
c.add(text(X0 + hdr / 2, 214, "PPPoE 6", 15, 600, WARN, FM, anchor="middle"))
c.add(text(X0 + hdr / 2, 238, "+ PPP 2", 15, 600, WARN, FM, anchor="middle"))
c.add(f'<rect x="{X0 + hdr + 8:.0f}" y="188" width="{W - hdr - 16:.0f}" height="60" rx="10" fill="{SOFT}" stroke="{BLUE}" stroke-width="2"/>')
c.add(text(X0 + hdr + (W - hdr) / 2, 225, "paquete IP: hasta 1492 bytes", 18, 600, BLUE, FM, anchor="middle"))
c.add(Label(48, 296, "Por eso: max-mtu=1492 max-mru=1492 en el cliente PPPoE.", 17, 500, INK2))

c.add(panel(48, 330, 530, 170, "Sin MSS ajustado", "alert"))
c.add(para(68, 394, "Muchos routers no avisan que el paquete es grande (ICMP) y muchos firewalls lo bloquean: páginas que cargan a medias.", 490, 17, INK, 500))
c.add(panel(622, 330, 530, 170, "Con change-mss", "ok"))
c.add(para(642, 394, "El router corrige el MSS en el SYN de cada conexión TCP que sale por pppoe-antel: los equipos negocian segmentos que entran.", 490, 17, INK, 500))
c.add(Terminal(48, 526, 1104, ["/ip/firewall/mangle/add chain=forward out-interface=pppoe-antel protocol=tcp", "  tcp-flags=syn action=change-mss new-mss=clamp-to-pmtu passthrough=yes comment=\"MSS PPPoE\""], title="SI EL PERFIL PPP NO LO HACE (change-tcp-mss)"))
save(c, "15-paso5.svg")
