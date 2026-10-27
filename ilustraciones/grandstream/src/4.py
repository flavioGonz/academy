import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 4.svg: tres tipos de troncal
c = Canvas(K(), "Register, Peer o Account: quién se registra en quién")
tipos = [("Register SIP Trunk", "ok", "Tu UCM se registra", "en el proveedor", ("UCM", "tu central"), ("Proveedor", "usuario y clave"), "REGISTER", "el de todos los días"),
         ("Peer SIP Trunk", "info", "Dos centrales se hablan", "por IP, sin registro", ("UCM", "casa central"), ("UCM", "sucursal"), "por IP", "para unir centrales"),
         ("Account SIP Trunk", "info", "Un equipo sin IP fija", "se registra en tu UCM", ("ATA o gateway", "sin IP fija"), ("UCM", "tu central"), "REGISTER", "lo contrario al Register")]
for i, (ttl, kd, l1, l2, a, b, lab, chip) in enumerate(tipos):
    x = 48 + i * 376
    c.add(panel(x, 130, 352, 420, ttl, kd, title_size=20))
    c.add(text(x + 20, 190, l1, 17, 500, INK, FB))
    c.add(text(x + 20, 214, l2, 17, 500, INK, FB))
    ga = Generic(x + 46, 250, a[0], a[1], icon="cloud" if a[0] == "Proveedor" else ("phone" if "ATA" in a[0] else "server"), w=260, dark=a[0] == "UCM")
    gb = Generic(x + 46, 410, b[0], b[1], icon="cloud" if b[0] == "Proveedor" else "server", w=260, dark=b[0] == "UCM")
    c.add(ga); c.add(gb)
    if lab == "por IP":
        c.add(Cable((x + 160, 340), (x + 160, 404), kind="logical", arrow=True))
        c.add(Cable((x + 192, 404), (x + 192, 340), kind="logical", arrow=True))
        c.add(pill(x + 268, 378, lab, INK3, WHITE, size=14))
    else:
        c.add(arrow((x + 176, 338), (x + 176, 404), kind="ok" if kd == "ok" else "flow", label=lab, label_dy=4))
    c.add(Chip(x + 20, 528, chip, "ok" if kd == "ok" else "gray", mono=False))
c.add(text(48, 600, "Proveedor con usuario y contraseña: Register. La UCM admite hasta 200 troncales SIP.", 17, 500, INK2, FB))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso1: el registro sale de la UCM
c = Canvas(K(1), "El registro sale de la UCM: no abras puertos")
xs = (170, 520, 900)
c.add(lifeline(xs[0], 130, 548, "UCM", "Proveedor_Lab", w=210))
c.add(lifeline(xs[1], 130, 548, "Router", "NAT del cliente", w=190))
c.add(lifeline(xs[2], 130, 548, "Proveedor", "sip.proveedor.example", w=250))
seq = [("REGISTER · usuario 21000000", 1, "flow"), ("401 · pedido de credenciales", -1, "logical"), ("REGISTER con la respuesta", 1, "flow"), ("200 OK · Registered", -1, "ok"), ("OPTIONS cada 60 s · heartbeat del paso 2", 1, "flow"), ("200 OK · sigue vivo", -1, "ok")]
for i, (s, d, k) in enumerate(seq):
    y = 236 + i * 54
    if d == 1:
        c.add(msg(xs[0], xs[2], y, s, k))
    else:
        c.add(msg(xs[2], xs[0], y, s, k))
c.add(f'<rect x="{xs[1] - 70}" y="210" width="140" height="350" rx="12" fill="{GROUND}" opacity=".0"/>')
c.add(Step(xs[0] - 105, 130, 1))
c.add(Note(48, 566, 1104, "La UCM inicia la charla y las respuestas vuelven por la misma sesión del router. Simtex sostiene que en el 99,9 % de los casos el troncal registrado no necesita reenvío de puertos.", kind="ok", size=15))
save(c, "4-paso1.svg")

# ---------------------------------------------------------------- 4-paso3: Registered o Rejected
c = Canvas(K(3), "Rejected es alcance o credenciales")
c.add(Window(48, 132, 520, 210, "UCM · web", path="System Status > Dashboard > Trunks", rows=[("Registered", "registró, listo"), ("Rejected", "no registró")], hl=1))
c.add(Step(48, 132, 3))
c.add(text(48, 386, "Si dice Rejected, dos preguntas:", 19, 600, INK, FD))
c.add(panel(48, 410, 520, 136, "1. ¿Llego al proveedor?", "info"))
lst, _ = bullet_list(68, 474, ["Desde una PC en la misma red de la central, el host del proveedor resuelve y responde."], 480, size=16, gap=4)
c.add(lst)
c.add(panel(612, 132, 540, 150, "2. ¿Las credenciales son las del proveedor?", "info", title_size=17))
lst, _ = bullet_list(632, 196, ["Usuario, Auth ID y contraseña copiados y pegados, no tipeados.", "Revisá los tres campos contra los datos del proveedor."], 500, size=16, gap=6)
c.add(lst)
c.add(Note(612, 310, 540, "El Dashboard muestra el estado de todos los troncales juntos: miralo antes de que llame el cliente.", kind="info", size=16))
c.add(Note(612, 420, 540, "Recién con Registered pasá a las cuatro pruebas del paso 4.", kind="ok", size=16))
save(c, "4-paso3.svg")

# ---------------------------------------------------------------- 4-paso4: las cuatro pruebas
c = Canvas(K(4), "Cuatro pruebas para dar el troncal por terminado")
pr = [("Sale", "Llamá a un celular desde una interna.", "phone"),
      ("Entra", "Desde un celular, llamá al número del troncal.", "phone"),
      ("Muestra bien el número", "El celular ve el caller ID que corresponde.", "user"),
      ("Pasa los tonos", "Dejá un mensaje en un buzón usando el teclado.", "bell")]
for i, (t, d, ic) in enumerate(pr):
    x = 48 + (i % 2) * 564
    y = 132 + (i // 2) * 186
    c.add(panel(x, y, 540, 162, None, "ok"))
    c.add(icon(x + 24, y + 30, ic, OK, 1.6))
    c.add(text(x + 80, y + 56, t, 22, 600, INK, FD))
    svg, _ = wrap(x + 80, y + 96, d, 430, 17, 400, INK2)
    c.add(svg)
    c.add(Mark(x + 500, y + 40, ok=True))
c.add(Step(48, 132, 4))
c.add(Note(48, 516, 1104, "El DTMF se prueba con algo que reaccione a las teclas, como el buzón. Si una de las cuatro falla, el troncal no está terminado aunque el Dashboard diga Registered.", kind="warn", size=16))
save(c, "4-paso4.svg")
