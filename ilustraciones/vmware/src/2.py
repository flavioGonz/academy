import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 2.svg: requisitos de ESXi 8
c = Canvas(K(), "Lo que el servidor tiene que cumplir para ESXi 8")
c.add(NOLIG)
cards = [
    ("CPU", ["2 núcleos como mínimo", "en la Compatibility Guide"], "cpu", "info"),
    ("BIOS", ["VT-x o AMD-V habilitado", "NX/XD habilitado · UEFI"], "bolt", "info"),
    ("Memoria", ["8 GB como mínimo", "12 GB para producción"], "server", "info"),
    ("Red", ["una NIC gigabit soportada", "mejor dos (lección 3)"], "globe", "info"),
    ("Disco de arranque", ["persistente: 32 GB mínimo", "128 GB óptimo, en RAID 1"], "check", "ok"),
    ("SD o USB", ["solo para arranque, en retirada", "no sirven para OSDATA"], "x", "alert"),
]
for i, (t, ls, ic, k) in enumerate(cards):
    col, row = i % 3, i // 3
    x, y = 48 + col * 376, 128 + row * 196
    bg, fg = KC[k]
    c.add(panel(x, y, 352, 176, None, k))
    c.add(f'<circle cx="{x + 42}" cy="{y + 44}" r="24" fill="{WHITE if k == "info" else bg}" stroke="{fg}" stroke-width="2"/>')
    if ic == "cpu":
        c.add(f'<g fill="none" stroke="{fg}" stroke-width="2"><rect x="{x + 31}" y="{y + 33}" width="22" height="22" rx="3"/><path d="M{x + 36} {y + 28}v5M{x + 42} {y + 28}v5M{x + 48} {y + 28}v5M{x + 36} {y + 55}v5M{x + 42} {y + 55}v5M{x + 48} {y + 55}v5"/></g>')
    else:
        c.add(icon(x + 28, y + 30, ic, fg, 1.15, 2))
    c.add(text(x + 80, y + 52, t, 20, 600, fg if k != "info" else INK, FD))
    for j, s in enumerate(ls):
        c.add(text(x + 26, y + 104 + j * 30, s, 16, 500 if j == 0 else 400, INK if j == 0 else INK2, FB))
c.add(Note(48, 540, 540, "Primero el modelo: CPU, NIC y controladora en la Broadcom Compatibility Guide (la ex HCL). Si no está, no hay soporte.", title="Antes de todo", kind="info"))
c.add(Note(612, 540, 540, "ESXi 9 deja afuera CPUs Skylake y anteriores: si el cliente piensa actualizar, chequeá también la 9.0.", title="Mirando adelante", kind="warn"))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso3: bootear el instalador sin instalar
c = Canvas(K(3), "Booteá el instalador para ver qué detecta, sin instalar")
c.add(NOLIG)
c.add(Step(48, 140, 3))
c.add(Laptop(48, 190, "Notebook", "consola remota"))
c.add(rect(48, 330, 230, 84, WHITE, LINE2, rx=16))
c.add(icon(66, 356, "card", BLUE, 1.35))
c.add(text(112, 366, "USB con el", 17, 600, INK, FB))
c.add(text(112, 390, "instalador ESXi 8", 15, 400, INK3, FM))
c.add(host(460, 170, 300, 300, "Servidor", "iLO o iDRAC"))
for i, s in enumerate(["CPU", "NICs", "Controladora"]):
    c.add(rect(480, 250 + i * 62, 260, 48, "#0B3A66", "#4E7396", rx=10))
    c.add(text(500, 280 + i * 62, s, 16, 600, WHITE, FB))
    c.add(text(724, 280 + i * 62, "¿la ve?", 15, 600, CYAN, FM, anchor="end"))
c.add(arrow((280, 232), (456, 232), "logical", label="medios virtuales", label_dy=-16))
c.add(arrow((280, 372), (456, 372), "flow", label="o USB", label_dy=-16))
c.add(arrow((762, 260), (826, 200), "ok"))
c.add(arrow((762, 400), (826, 452), "alert"))
c.add(panel(830, 128, 322, 160, "Detecta todo", "ok"))
sv, _ = wrap(850, 194, "Cancelás o seguís con la instalación en un disco persistente (paso 4).", 284, 16, 400, INK2)
c.add(sv)
c.add(panel(830, 370, 322, 180, "Avisa algo no soportado", "alert"))
sv, _ = wrap(850, 436, "El instalador lo advierte: frenás, revisás la Compatibility Guide y no instalás en un cliente.", 284, 16, 400, INK2)
c.add(sv)
c.add(Note(48, 500, 712, "Así chequeás compatibilidad sin tocar los discos del servidor: nada se escribe hasta que confirmás la instalación.", kind="info"))
save(c, "2-paso3.svg")

# ---------------------------------------------------------------- 2-paso4: DCUI, Configure Management Network
c = Canvas(K(4), "En la DCUI: IP fija, DNS y nombre del host")
c.add(NOLIG)
c.add(Step(48, 140, 4))
c.add(rect(48, 162, 640, 420, "#2E2E2E", "#2E2E2E", rx=14))
c.add(rect(48, 162, 640, 44, "#C9A227", "#C9A227", rx=14))
c.add(rect(48, 190, 640, 16, "#C9A227", "#C9A227", rx=0))
c.add(text(68, 191, "Configure Management Network", 17, 700, "#1E1E1E", FM))
menu = ["Network Adapters", "VLAN (optional)", "IPv4 Configuration", "IPv6 Configuration", "DNS Configuration", "Custom DNS Suffixes"]
for i, s in enumerate(menu):
    y = 236 + i * 46
    hl = s in ("IPv4 Configuration", "DNS Configuration")
    if hl:
        c.add(rect(60, y - 4, 616, 38, "#C9A227", "#C9A227", rx=6))
    c.add(text(80, y + 21, s, 17, 600 if hl else 500, "#1E1E1E" if hl else "#E8E8E8", FM))
c.add(text(68, 556, "<Enter> elegir    <Esc> salir", 15, 500, "#BDBDBD", FM))
c.add(arrow((690, 284), (742, 220), "flow"))
c.add(arrow((690, 422), (742, 398), "flow"))
c.add(Window(744, 128, 408, 214, "IPv4 Configuration", [("Modo", "Static"), ("IP", "192.168.88.20"), ("Máscara", "255.255.255.0"), ("Gateway", "192.168.88.1")], hl=0))
c.add(Window(744, 362, 408, 138, "DNS Configuration", [("DNS", "192.168.88.1"), ("Hostname", "esxi-lab01")]))
c.add(rect(744, 520, 408, 62, OK_BG, OK, rx=12))
c.add(text(764, 558, "Esc > Y: reinicia la red de gestión", 16, 600, OK, FM))
c.add(text(48, 625, "Después: https://192.168.88.20/ui y entrás con root al Host Client (paso 5).", 17, 500, INK2, FB))
save(c, "2-paso4.svg")
