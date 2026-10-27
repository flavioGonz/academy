import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 2.svg: tres condiciones para adoptar
c = Canvas(K(), "Tres condiciones para que un equipo adopte")
c.add(APNode(118, 268, "AP nuevo", "o reseteado"))
gates = [
    ("1", "Libre de otro", "controlador", ["Reset de fábrica y, si", "estaba adoptado, borrado", "del controlador viejo."]),
    ("2", "Firmware", "compatible", ["Desfase entre equipo y", "controlador: la falla", "más común (LazyAdmin)."]),
    ("3", "Llega al", "controlador", ["En L2: misma red y", "un solo servidor DHCP.", "En L3: inform (lección aparte)."]),
]
for i, (n_, a, b, lines) in enumerate(gates):
    x = 222 + i * 272
    c.add(panel(x, 140, 248, 256, None, "info"))
    c.add(f'<circle cx="{x + 36}" cy="{176}" r="18" fill="{CYAN}"/>' + mid(x + 36, 182, n_, 18, 700, WHITE, FD))
    c.add(text(x + 66, 174, a, 20, 600, INK, FD))
    c.add(text(x + 66, 198, b, 20, 600, INK, FD))
    c.add(hline(x + 20, x + 228, 222))
    for k, s in enumerate(lines):
        c.add(text(x + 20, 256 + k * 26, s, 16, 400, INK2, FB))
    c.add(arrow((x - 22, 268), (x - 4, 268)))
c.add(arrow((1042, 268), (1066, 268), kind="ok"))
c.add(f'<circle cx="1104" cy="268" r="34" fill="{OK_BG}" stroke="{OK}" stroke-width="2"/>')
c.add(icon(1086, 250, "check", OK, 1.5, 2.6))
c.add(mid(1104, 330, "Adopt", 17, 600, OK, FM))
c.add(Note(48, 430, 1104, "Reset, misma red que el controlador, firmware, y recién ahí sospechás del controlador. Ese orden ahorra la primera hora de cada obra.", title="El orden en obra", kind="ok"))
c.add(Note(48, 548, 1104, "Si el equipo estaba adoptado en otro controlador, borralo primero ahí: si no, sigue buscando a su host viejo.", kind="warn"))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso2: misma red, un solo DHCP
c = Canvas(K(2), "El AP en el mismo switch y red que el controlador")
sw = c.add(Router(250, 128, "Switch del laboratorio", "una sola VLAN", ports=["1", "2", "3", "4", "5"], hl={"1": BLUE, "3": CYAN, "5": BLUE}))
ctl = c.add(Generic(70, 420, "Controlador", "misma red", icon="server", w=240))
ap = c.add(APNode(475, 455, "AP", "PoE desde el switch"))
rt = c.add(Generic(600, 420, "Router de laboratorio", "DHCP 192.168.88.0/24", icon="server", w=290))
c.add(Cable(sw.port("1"), ctl.top(), kind="data"))
c.add(Cable(sw.port("3"), (475, 413), kind="data", label="PoE", label_at=0.55, label_dy=0))
c.add(Cable(sw.port("5"), rt.top(-40), kind="data"))
c.add(Step(sw.port("3")[0] + 30, sw.port("3")[1] + 26, 2))
c.add(panel(930, 128, 222, 250, None, "alert"))
c.add(Mark(966, 166, ok=False))
c.add(text(994, 172, "Segundo DHCP", 18, 600, ALERT, FD))
lst, _ = bullet_list(950, 214, ["Módem o router del cliente repartiendo IP en la misma red.", "El AP toma IP de otro rango y no ve al controlador."], 186, size=15)
c.add(lst)
c.add(Note(930, 400, 222, "Uno solo: el del laboratorio.", kind="ok", size=15))
c.add(Note(70, 580, 820, "En capa 2 el controlador descubre al AP sin configurar nada. Conectarlo al mismo switch que el controlador descarta la red como sospechosa.", kind="info", size=16))
save(c, "2-paso2.svg")

# ---------------------------------------------------------------- 2-paso3: SSH e info
c = Canvas(K(3), "Entrá por SSH y leé info antes de adoptar")
c.add(Terminal(48, 130, 610, [("$ ssh ubnt@192.168.88.20", "#9FE3B5"), "  usuario y clave de fábrica: ubnt / ubnt", ("# info", "#9FE3B5"), "", "Model:       <modelo de tu AP>", "Version:     <firmware>", "IP Address:  192.168.88.20", "Status:      Not Adopted", "             (http://unifi:8080/inform)"], title="SSH AL AP RESETEADO"))
rows = [(290, "¿es el equipo que pensás?"), (316, "firmware: compará con el controlador"), (342, "¿quedó en la red del controlador?"), (368, "estado y URL de inform a la que apunta")]
for y, s in rows:
    c.add(f'<path d="M664 {y - 5}H694" stroke="{CYAN}" stroke-width="2" stroke-dasharray="4 4"/>')
    c.add(text(704, y, s, 16, 500, INK2, FB))
c.add(Note(48, 470, 610, "La IP la sacás de la lista de leases del DHCP o con WiFiman. Si ya entrás por SSH, set-default resetea igual que el botón de 10 segundos.", kind="info"))
c.add(Note(700, 470, 452, "El firmware que ves en Version es el primer sospechoso si después no adopta.", title="Desfase de firmware", kind="warn"))
save(c, "2-paso3.svg")

# ---------------------------------------------------------------- 2-paso5: estados y salidas
c = Canvas(K(5), "Qué hacer según el estado que muestra Devices")
rows = [
    ("Pending Adoption", "info", "Adopt", "ok", "queda adoptado y conectado"),
    ("Pending Adoption (Update Required)", "warn", "Adopt and Upgrade", "info", "si no actualiza solo: upgrade por SSH"),
    ("Adopta y pasa a offline", "alert", "Firewall de la PC", "info", "controlador en una PC: revisá su firewall"),
]
for i, (st, kd, act, ka, res) in enumerate(rows):
    y = 140 + i * 132
    c.add(panel(48, y, 400, 100, None, kd))
    svg_, hh = wrap(70, 0, st, 360, 19, 600, {"info": INK, "warn": WARN, "alert": ALERT}[kd], FM)
    c.add(f'<g transform="translate(0 {y + 50 - hh / 2 + 15:.1f})">{svg_}</g>')
    c.add(arrow((456, y + 50), (500, y + 50)))
    c.add(panel(508, y, 270, 100, None, ka))
    c.add(text(530, y + 58, act, 19, 600, INK, FD))
    c.add(arrow((786, y + 50), (830, y + 50)))
    svg_, hh = wrap(842, 0, res, 310, 17, 400, INK2)
    c.add(f'<g transform="translate(0 {y + 50 - hh / 2 + 13:.1f})">{svg_}</g>')
c.add(Step(48, 272, 5))
c.add(code(508, 560, 644, "upgrade <url-del-firmware-para-tu-modelo>"))
c.add(text(48, 586, "Firmware de tu modelo, desde la página", 16, 400, INK2, FB))
c.add(text(48, 610, "de descargas de Ubiquiti, por SSH:", 16, 400, INK2, FB))
save(c, "2-paso5.svg")
