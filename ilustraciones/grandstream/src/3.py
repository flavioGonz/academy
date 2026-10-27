import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 3.svg: dos caminos para que el teléfono encuentre la UCM
c = Canvas(K(), "Cómo encuentra el teléfono su configuración")
metodos = [("SIP SUBSCRIBE", "en cualquier modo de red", "info",
            [("SUBSCRIBE a multicast", "flow", 1), ("NOTIFY con la URL", "ok", -1), ("baja el XML", "flow", 1)]),
           ("DHCP opción 66", "solo con la UCM en Route", "info",
            [("DHCP DISCOVER", "flow", 1), ("OFFER + opción 66", "ok", -1), ("baja el XML", "flow", 1)])]
for j, (ttl, sub, kd, msgs) in enumerate(metodos):
    x0 = 48 + j * 564
    c.add(panel(x0, 128, 540, 380, ttl, kd, sub=sub, title_size=21))
    xa, xb = x0 + 120, x0 + 420
    c.add(lifeline(xa, 210, 480, "Teléfono", "recién reseteado", w=180))
    c.add(lifeline(xb, 210, 480, "UCM", "Zero Config", w=180))
    for i, (s, k, d) in enumerate(msgs):
        y = 320 + i * 58
        if d == 1:
            c.add(msg(xa, xb, y, s, k))
        else:
            c.add(msg(xb, xa, y, s, k))
c.add(Note(48, 530, 540, "El XML lo arma la UCM con las plantillas y viaja por TFTP, HTTP o HTTPS. El teléfono lo aplica y registra solo.", kind="ok", size=16))
c.add(Note(612, 530, 540, "En Route la UCM es el DHCP de su LAN y entrega la URL, por ejemplo https://192.168.2.1:8089/zccgi/", kind="info", size=16))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso2: escaneo por SIP Message a la dirección de broadcast
c = Canvas(K(2), "Si no aparece, escaneá con SIP Message a .255")
u = c.add(Generic(48, 250, "UCM", "192.168.88.20", icon="server", w=230, dark=True))
c.add(Zone(330, 140, 440, 460, "red 192.168.88.0/24", BLUE))
c.add(DeskPhone(370, 210, "GRP26xx", "reseteado"))
c.add(DeskPhone(575, 210, "GRP26xx", "reseteado"))
c.add(Generic(400, 470, "Otro equipo", "no Grandstream", icon="phone", w=300))
c.add(wire([(278, 280), (310, 280), (310, 180), (660, 180), (660, 204)], kind="flow", arrow=True))
c.add(wire([(310, 280), (362, 280)], kind="flow", arrow=True))
c.add(pill(200, 226, "SIP Message", BLUE, WHITE, size=14))
c.add(text(550, 436, "responden y aparecen en la lista", 15, 500, OK, FB, anchor="middle"))
c.add(text(550, 584, "no aparece: su OUI no está en la lista", 15, 500, INK3, FB, anchor="middle"))
c.add(Step(48, 250, 2))
c.add(Window(800, 140, 352, 230, "Auto Discover", path="Device Management > Zero Config", rows=[("Scan Method", "SIP Message"), ("Scan IP", "192.168.88.255"), ("Scan all MACs", "No")], hl=1))
c.add(Note(800, 396, 352, "Con .255 el mensaje va a toda la red. Con Scan all MACs en No, solo aparecen equipos con OUI de Grandstream.", kind="info", size=15))
c.add(Note(800, 526, 352, "Auto Assign Extension solo en una red de voz separada: puede tomar teléfonos ajenos.", kind="warn", size=15))
save(c, "3-paso2.svg")

# ---------------------------------------------------------------- 3-paso4: prioridad de plantillas
c = Canvas(K(4), "Qué plantilla gana cuando dos dicen distinto")
niveles = [("Model Template", "por modelo · la que gana", "Idioma del GRP: inglés", OK_BG, OK),
           ("Global Template", "varias, una por defecto", "(sin idioma)", WHITE, LINE2),
           ("Global Policy", "una sola · todos los equipos", "Idioma: español · Montevideo", SOFT, BLUE)]
for i, (n_, s, v, bg, fg) in enumerate(niveles):
    y = 136 + i * 108
    w = 560 - (2 - i) * 0
    c.add(f'<rect x="48" y="{y}" width="640" height="92" rx="14" fill="{bg}" stroke="{fg}" stroke-width="2"/>')
    c.add(text(72, y + 40, n_, 21, 600, INK, FD))
    c.add(text(72, y + 68, s, 15, 500, INK3, FM))
    c.add(text(664, y + 54, v, 16, 600, INK, FB, anchor="end"))
c.add(arrow((720, 438), (720, 150), kind="ok"))
c.add(text(740, 300, "más", 16, 600, OK, FB))
c.add(text(740, 322, "prioridad", 16, 600, OK, FB))
c.add(Step(48, 352, 4))
c.add(panel(860, 136, 292, 308, "Resultado", "ok"))
c.add(DeskPhone(920, 196, "GRP", "inglés · hora de Montevideo"))
c.add(text(880, 412, "el idioma lo pisó el Model", 15, 500, INK2, FB))
c.add(text(880, 432, "Template; la hora vino de abajo", 15, 500, INK2, FB))
c.add(Note(48, 474, 1104, "Lo que alguien tocó a mano en la web del teléfono no lo pisa ninguna plantilla. Por eso el teléfono que se aprovisiona no se toca: si quedó distinto, reset de fábrica y que lo tome Zero Config.", title="Por encima de todo, lo manual", kind="warn", size=16))
save(c, "3-paso4.svg")
