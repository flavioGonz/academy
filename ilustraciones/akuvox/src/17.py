import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/akuvox/src")
from _cat import *

# ---------------------------------------------------------------- 17.svg: evento -> GET con variables reemplazadas
c = Canvas("Akuvox", "Cada evento del portero manda un GET a tu servidor")
c.add(portero(60, 170, "pantalla", 0.85, "Portero", "192.168.88.21"))
c.add(panel(930, 172, 222, 316, None, "info"))
c.add(icon(1020, 220, "server", BLUE, 1.5))
c.add(text(1041, 290, "Servidor", 20, 600, INK, FB, anchor="middle"))
c.add(text(1041, 316, "192.168.88.10", 15, 500, INK3, FM, anchor="middle"))
c.add(text(1041, 338, "puerto 8000", 15, 500, INK3, FM, anchor="middle"))
c.add(text(1041, 380, "registra cada", 15, 400, INK2, FB, anchor="middle"))
c.add(text(1041, 400, "línea que llega", 15, 400, INK2, FB, anchor="middle"))
c.add(text(330, 152, "EVENTO", 14, 600, INK3, FM, ls=1.5))
c.add(text(520, 152, "LO QUE CARGASTE → LO QUE LLEGA", 14, 600, INK3, FM, ls=1.5))
ev = [("Tarjeta válida", "/validcard=$card_sn", "/validcard=<n.º de tarjeta>"),
      ("Relé A se dispara", "/relaytrigger=$relay1status", "/relaytrigger=1"),
      ("Relé A cierra", "/relayclose=$relay1status", "/relayclose=0")]
for i, (e_, tpl, real) in enumerate(ev):
    y = 172 + i * 112
    c.add(f'<rect x="310" y="{y}" width="580" height="92" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
    c.add(text(330, y + 34, e_, 18, 600, INK, FB))
    c.add(text(520, y + 34, tpl, 15, 500, INK3, FM))
    c.add(text(520, y + 66, real, 16, 700, BLUE, FM))
    c.add(arrow((892, y + 46), (928, y + 46), "flow", bend="straight"))
c.add(arrow((205, 290), (310, 290), "logical"))
c.add(Note(48, 540, 540, "El equipo reemplaza cada $variable por el dato real antes de mandar: $relay1status vale 1 abierto y 0 cerrado.", kind="info", size=16))
c.add(Note(612, 540, 540, "Lo que abre por HTTP también avisa por HTTP, a un servidor de la misma red (la VLAN de porteros).", kind="ok", size=16))
save(c, "17.svg")

# ---------------------------------------------------------------- 17-paso2: campos de Action URL
c = Canvas("Akuvox · Paso 2", "Cargá una URL por evento en Action URL")
c.add(Window(48, 128, 1104, 296, "Portero · web", path="Device Management > Setting > Action URL",
             rows=[("Action URL", "Enabled ✓"),
                   ("Relay A Triggered", "http://<IP_SERVIDOR>:8000/relaytrigger=$relay1status"),
                   ("Relay A Closed", "http://<IP_SERVIDOR>:8000/relayclose=$relay1status"),
                   ("Valid Card Entered", "http://<IP_SERVIDOR>:8000/validcard=$card_sn"),
                   ("Setup Completed", "(vacío)")], hl=4))
c.add(Step(1152, 128, 2))
c.add(text(48, 462, "Variables que el equipo completa:", 17, 600, INK, FB))
c.add(Table(48, 476, ["Variable", "Qué trae"], [["$relay1status", "1 abierto · 0 cerrado"], ["$card_sn", "número de la tarjeta"], ["$code", "código ingresado"], ["$mac  $ip  $model", "quién avisa"]], [230, 300], mono_cols=(0,), row_h=36))
c.add(Note(640, 476, 512, "Setup Completed (arranque) no lo controla el interruptor de Action URL: si no lo usás, el campo queda vacío.", title="Atención", kind="warn", size=15))
c.add(Note(640, 590, 512, "El menú es el del R20A; los eventos cambian por modelo.", kind="info", size=15))
save(c, "17-paso2.svg")

# ---------------------------------------------------------------- 17-paso3: lo que se ve en la terminal
c = Canvas("Akuvox · Paso 3", "Pasá una tarjeta y mirá llegar las líneas")
dim = "#7FA6C9"
lines = [("$ python3 -m http.server 8000 --bind 192.168.88.10", "#D9E9F8"),
         ("Serving HTTP on 192.168.88.10 port 8000 ...", dim),
         ('192.168.88.21 - - [...] "GET /validcard=... HTTP/1.1" 404 -', "#7FD6F2"),
         ('192.168.88.21 - - [...] "GET /relaytrigger=1 HTTP/1.1" 404 -', "#7FD6F2"),
         ('192.168.88.21 - - [...] "GET /relayclose=0 HTTP/1.1" 404 -', "#7FD6F2")]
t = c.add(Terminal(48, 130, 760, lines, title="PC DE LABORATORIO · 192.168.88.10"))
lab = [("tarjeta válida", 2), ("el relé A abre", 3), ("el relé A cierra", 4)]
for s_, i in lab:
    y = 130 + 56 + i * 26 - 6
    c.add(arrow((1000, y), (822, y), "flow"))
    c.add(text(1012, y + 6, s_, 16, 600, INK, FB))
c.add(Note(48, 340, 540, "El 404 no importa: el servidor no tiene esa página, pero la línea demuestra que el portero avisó.", title="404 es normal", kind="ok", size=16))
c.add(Note(612, 340, 540, "Paso 4: sumá mac=$mac:ip=$ip:model=$model a una URL y fijate que llegan los datos del equipo.", kind="info", size=16))
c.add(Note(48, 470, 1104, "$card_sn y $code viajan dentro de la URL: el servidor va en la VLAN de porteros y no deja esos logs a la vista.", kind="warn", size=16))
save(c, "17-paso3.svg")
