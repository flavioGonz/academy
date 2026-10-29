import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 18.svg: cuatro clientes, un GET
c = Canvas("Akuvox", "Un mismo GET, cuatro sistemas, un usuario cada uno")
cl = [("PC con curl", "curl -u", "curl-lab", "laptop"),
      ("MikroTik", "/tool/fetch", "mk-porton", "server"),
      ("Home Assistant", "rest_command", "ha-porton", "server"),
      ("Asterisk / FreePBX", "CURL() en el dialplan", "usuario propio", "phone")]
for i, (t, sub, u, ic) in enumerate(cl):
    y = 132 + i * 104
    c.add(Generic(48, y, t, sub, ic, w=330))
    c.add(Chip(396, y + 50, u, "gray"))
    c.add(Cable((560, y + 42), (742, 300), kind="flow", arrow=True))
c.add(portero(752, 176, "pantalla", 0.8, "Portero", "<IP_PORTERO>"))
c.add(gate(960, 236, 190, 110, BLUE, "Portón"))
c.add(wire([(872, 290), (960, 290)], "relay"))
c.add(pill(916, 278, "relé B", CYAN, WHITE, 15))
c.add(text(48, 580, "Lo que mandan todos:", 16, 600, INK2, FB))
s, _ = code_parts(220, 556, [("<IP_PORTERO>", "#7FD6F2"), ("/fcgi/OpenDoor?action=OpenDoor&", "#D9E9F8"), ("DoorNum=2", "#F2C94C")], size=16)
c.add(s)
c.add(text(48, 640, "Si cambiás la clave de un sistema, los otros tres siguen andando.", 16, 500, OK, FB))
save(c, "18.svg")

# ---------------------------------------------------------------- 18-paso1: basic o digest
c = Canvas("Akuvox · Pasos 1 a 3", "¿Responde 401? Igualá basic o digest")
c.add(Laptop(48, 140, "curl", "192.168.88.10", w=230))
c.add(portero(980, 128, "pantalla", 0.62, None, None))
c.add(text(1026, 314, "Portero", 17, 600, INK, FB, anchor="middle"))
c.add(text(1026, 334, "192.168.88.21", 15, 400, INK3, FM, anchor="middle"))
c.add(arrow((290, 166), (960, 166), "flow", "curl -u (basic)", bend="straight", label_dy=-10))
c.add(arrow((960, 206), (290, 206), "alert", "401 Unauthorized", bend="straight", label_dy=-10))
c.add(arrow((290, 262), (960, 262), "ok", "curl --digest -u ...", bend="straight", label_dy=-10))
c.add(text(625, 300, "relé B abre", 16, 700, OK, FB, anchor="middle"))
c.add(Step(48, 140, 1))
c.add(text(48, 392, "Mismo cambio en cada cliente (basic es el valor por defecto):", 17, 600, INK, FB))
c.add(Table(48, 408, ["Cliente", "Basic", "Digest"],
            [["curl", "-u usuario:clave", "--digest -u usuario:clave"],
             ["MikroTik /tool/fetch", "user= password=", "http-auth-scheme=digest"],
             ["Home Assistant", "authentication: basic", "authentication: digest"]],
            [290, 360, 454], mono_cols=(1, 2), row_h=42))
c.add(Note(48, 590, 1104, "Un usuario distinto por sistema: curl-lab, mk-porton, ha-porton. Así cada credencial se cambia sin tocar las demás.", kind="info", size=15))
save(c, "18-paso1.svg")

# ---------------------------------------------------------------- 18-paso4: Asterisk abre con la extensión 7001
c = Canvas("Akuvox · Paso 4", "El interno marca 7001 y la central abre el portón")
c.add(Phone(48, 170, "Interno autorizado", "marca 7001", w=250))
c.add(Phone(48, 330, "Otro interno", "marca 7001", w=250))
c.add(Server(410, 230, "Asterisk / FreePBX", "extensión 7001", w=290))
c.add(portero(820, 160, "pantalla", 0.75, "Portero", "<IP_PORTERO>"))
c.add(gate(990, 220, 160, 100, BLUE, "Portón"))
c.add(wire([(932, 270), (990, 270)], "relay"))
c.add(arrow((298, 212), (410, 262), "ok"))
c.add(arrow((298, 372), (410, 296), "alert"))
c.add(Mark(352, 372, ok=False))
c.add(text(320, 420, "bloqueado en la central", 15, 600, ALERT, FB))
c.add(arrow((700, 272), (818, 272), "flow", "GET", bend="straight", label_dy=-12))
c.add(Step(410, 230, 4))
c.add(text(48, 500, "Dialplan de prueba:", 16, 600, INK2, FB))
c.add(code(48, 512, 1104, "exten => 7001,1,Set(RESP=${CURL(http://<USUARIO>:<CLAVE>@<IP_PORTERO>/fcgi/OpenDoor?action=OpenDoor&DoorNum=2)})", 14, h=40))
c.add(code(48, 556, 1104, " same => n,Hangup()", 14, h=40))
c.add(Note(48, 606, 1104, "La extensión 7001 abre el portón: restringila en la central a los internos que corresponda.", kind="warn", size=15))
save(c, "18-paso4.svg")
