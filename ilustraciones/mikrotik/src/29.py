"""Lección 29 · Diagnóstico por terminal: principal + pasos 2, 3 y 4.
Fuentes: class/29-diagnostico-terminal/card.md, research/notes/n29-32.md
(manual 7.25 Ping y Traceroute, foro 157966 y 80144).
Regenerar:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/29.py
  python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/mikrotik/29*.svg
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/mikrotik/src")
from _mt import *  # noqa
from _mt import text, wrap

K = "MikroTik"

# ------------------------------------------------------------ principal: la escalera
c = Canvas(K, "Escalera de pings: ¿en qué escalón falla?")
steps = [
    ("1", "LAN", "/ping 192.168.88.254", "cable, puerto, bridge o firewall del equipo"),
    ("2", "Gateway del ISP", "/ping 203.0.113.1", "WAN: cable al módem, IP o VLAN, PPPoE"),
    ("3", "IP de internet", "/ping 1.1.1.1", "ruta por defecto o el proveedor"),
    ("4", "Un nombre", "/ping mikrotik.com", "DNS: \"resolve failed\""),
]
base_y, dy, dx = 540, 100, 60
for i, (n, lbl, cmd, falla) in enumerate(steps):
    x = 48 + i * dx
    y = base_y - i * dy
    w = 560
    c.add(rect(x, y, w, 76, WHITE, LINE2, 2, 14))
    c.add(Step(x + 34, y + 38, n))
    c.add(text(x + 66, y + 32, lbl, 18, 600, INK, FD))
    c.add(text(x + 66, y + 58, cmd, 16, 500, BLUE, FM))
    # flecha hacia el diagnóstico
    ax = x + w + 14
    c.add(arrow((ax, y + 38), (ax + 46, y + 38), kind="alert"))
    c.add(rect(ax + 56, y + 8, 1100 - (ax + 56) + 52, 60, ALERT_BG, ALERT_BG, 0, 12))
    c.add(text(ax + 72, y + 32, "si falla acá", 14, 600, ALERT, FM))
    c.add(text(ax + 72, y + 55, falla, 15, 500, INK2, FB))
c.add(text(48, 150, "De adentro hacia afuera:", 17, 600, INK2, FB))
c.add(text(48, 174, "el primer escalón que no contesta dice dónde mirar.", 17, 400, INK2, FB))
c.add(Chip(48, 222, "anda la IP y no el nombre = DNS", "ok", mono=False))
save(c, "29.svg")

# ------------------------------------------------------------ paso 2: ARP ping
c = Canvas(K + " · Paso 2", "La notebook no contesta ping: probá con ARP")
r = c.add(Generic(60, 320, "MikroTik", "192.168.88.1 · bridge", icon="server", dark=True, w=280))
lp = c.add(Laptop(860, 320, "Notebook", "192.168.88.254", w=290))
c.add(Arrow((350, 335), (850, 335), kind="alert", label="ICMP echo: timeout", label_dy=-14))
c.add(rect(690, 348, 150, 28, ALERT_BG, ALERT_BG, 0, 8))
c.add(text(765, 367, "firewall Windows", 14, 600, ALERT, FM, anchor="middle"))
c.add(Arrow((350, 412), (850, 412), kind="ok", label="ARP: ¿quién tiene .254?", label_dy=-14))
c.add(Arrow((850, 448), (350, 448), kind="ok", label="respuesta con su MAC", label_dy=28))
c.add(Note(60, 128, 600, "El firewall de Windows suele frenar el ping. ARP no se puede frenar: sin ARP el equipo no hablaría con nadie de su red.", title="Por qué ARP sí contesta", kind="info"))
t, _ = code(60, 512, 700, ["/ping 192.168.88.254 arp-ping=yes interface=bridge count=2",
                           ("0  FE:14:80:BE:47:5B   386us", GREEN_T)], title="TERMINAL")
c.add(t)
c.add(Note(790, 512, 360, "Aparece una MAC: el equipo está vivo. Buscala en los leases del DHCP.", kind="ok"))
save(c, "29-paso2.svg")

# ------------------------------------------------------------ paso 3: leer traceroute
c = Canvas(K + " · Paso 3", "Traceroute: ¿pérdida real o router que no contesta?")
c.add(caption(48, 148, "caso A · el destino contesta", OK))
c.add(Table(48, 164, ["#", "address", "loss"], [
    ["1", "203.0.113.1", "0%"],
    ["2", "203.0.113.6", "90%"],
    ["3", "198.51.100.1", "0%"],
    ["4", "1.1.1.1", "0%"],
], [60, 250, 210], hl_row=1, mono_cols=(1, 2)))
c.add(Note(48, 372, 520, "La pérdida no sigue en los saltos siguientes: ese router limita sus respuestas ICMP. El tráfico pasa. No es falla.", title="Salto 2 con 90%", kind="ok"))
c.add(caption(632, 148, "caso B · se corta en el salto 3", ALERT))
c.add(Table(632, 164, ["#", "address", "loss"], [
    ["1", "203.0.113.1", "0%"],
    ["2", "203.0.113.6", "0%"],
    ["3", "", "100%  timeout"],
    ["4", "", "100%  timeout"],
], [60, 250, 210], hl_row=2, mono_cols=(1, 2)))
c.add(Note(632, 372, 520, "Nada contesta después del salto 2: el problema está después de 203.0.113.6 (enlace, ruta, ruta de vuelta o firewall).", title="Falla real", kind="alert"))
c.add(Note(48, 540, 1104, "La pérdida real empieza en un salto y se ve en todos los que siguen. Dos direcciones que se alternan son un lazo de ruteo.", title="La regla de la documentación", kind="info"))
save(c, "29-paso3.svg")

# ------------------------------------------------------------ paso 4: src-address
c = Canvas(K + " · Paso 4", "src-address: probá el camino de la LAN")
c.add(rect(48, 150, 250, 420, DEEP, DEEP, 2, 18))
c.add(text(173, 196, "MikroTik", 21, 600, WHITE, FD, anchor="middle"))
c.add(text(173, 224, "WAN 203.0.113.10", 15, 400, "#9FC3E3", FM, anchor="middle"))
c.add(text(173, 248, "LAN 192.168.88.1", 15, 400, "#9FC3E3", FM, anchor="middle"))
c.add(mini(930, 300, 222, 110, "Internet", "1.1.1.1", icon="globe"))
rows_ = [
    (300, "/ping 1.1.1.1", "sale con la IP de la WAN", "ok", True),
    (400, "/ping 1.1.1.1 src-address=192.168.88.1", "masquerade la cambia por 203.0.113.10", "ok", True),
    (500, "igual, con el masquerade apagado", "sale con 192.168.88.1: la respuesta no vuelve", "alert", False),
]
for y, cmd, lbl, kind, ok in rows_:
    c.add(arrow((310, y), (918, y), kind=kind))
    c.add(text(330, y - 34, cmd, 15, 600, INK, FM))
    c.add(text(330, y - 12, lbl, 15, 400, OK if ok else ALERT, FB))
    c.add(Mark(880, y - 26, ok))
c.add(Note(48, 590, 1104, "El ping normal anda y el de la LAN no: así se ve un masquerade roto. Con un túnel entre dos LAN se prueba igual, desde la IP de la LAN.", kind="warn"))
save(c, "29-paso4.svg")
