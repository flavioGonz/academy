import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 4.svg: tres caminos en otra subred
c = Canvas(K(), "Otra subred: alguien le dice al EAP dónde ir")
c.add(Zone(48, 132, 330, 160, "192.168.88.0/24"))
c.add(Generic(68, 170, "Controlador", "192.168.88.10", icon="server", w=290, dark=True))
c.add(Box(470, 170, 260, 84, "Router", "rutea entre subredes"))
c.add(Zone(822, 132, 330, 160, "VLAN 20 · 10.10.10.0/24"))
c.add(APNode(900, 204, "EAP", "10.10.10.x", r=32))
c.add(Cable((866, 212), (742, 212), kind="alert", arrow=True))
c.add(text(760, 196, "broadcast", 15, 600, ALERT, FM))
c.add(text(470, 284, "El broadcast no pasa el router.", 16, 600, ALERT, FB))
c.add(wire([(1060, 292), (1060, 326), (213, 326), (213, 258)], kind="ok", arrow=True))
c.add(tag(640, 332, "con la dirección, el EAP llama directo: Pending", "ok", mono=False))
cards = [("A", "Discovery Utility", ["Programa en una PC de la", "subred del equipo.", "Batch Setting con la IP."]),
         ("B", "Inform URL", ["En la web del equipo:", "System Tools >", "Controller Settings."]),
         ("C", "DHCP option 138", ["El DHCP entrega la IP", "del controlador. Actúa", "cuando el equipo renueva."])]
for i, (k, t, ls) in enumerate(cards):
    x = 48 + i * 376
    c.add(panel(x, 370, 352, 168, None, "info"))
    c.add(badge(x + 36, 408, k))
    c.add(text(x + 66, 415, t, 20, 600, INK, FD))
    c.add(lines(x + 26, 452, ls, 16, 26))
c.add(Note(48, 558, 540, "En Omada Central va la Site URL que copiás en Global View > Dashboard, no una IP.", kind="info"))
c.add(Note(612, 558, 540, "Con Docker Desktop (Windows o macOS), el camino práctico es la Inform URL.", kind="warn"))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso1: option 138 en hexadecimal
c = Canvas(K(1), "Option 138: la IP del controlador, byte por byte")
c.add(code(48, 124, 1104, "/ip dhcp-server option add name=omada138 code=138 value=0xC0A8580A", 16, h=44))
c.add(Step(48, 124, 1))
pairs = [("C0", "192"), ("A8", "168"), ("58", "88"), ("0A", "10")]
for i, (hx, dec) in enumerate(pairs):
    x = 150 + i * 180
    c.add(rect(x, 206, 140, 86, WHITE, BLUE, rx=14, sw=3))
    c.add(mid(x + 70, 262, hx, 34, 600, INK, FM))
    c.add(mid(x + 70, 326, dec, 22, 600, BLUE, FM))
c.add(f'<path d="M160 346v12H{150 + 3 * 180 + 130}v-12" fill="none" stroke="{BLUE}" stroke-width="2"/>')
c.add(mid(430, 388, "192.168.88.10, la IP del controlador", 18, 600, INK, FB))
c.add(mid(430, 414, "un byte por octeto, en hexadecimal", 15, 500, INK3, FM))
c.add(Note(860, 206, 292, "En el gateway Omada no hace falta el hex: Advanced DHCP Options, Option 138 = 192.168.88.10.", title="Con gateway Omada", kind="ok"))
c.add(code(48, 450, 1104, '/ip dhcp-server network set [find address="10.10.10.0/24"] dhcp-option=omada138', 15, h=44))
c.add(Note(48, 520, 1104, "La opción se entrega con la próxima concesión. Un EAP que ya tenía IP no se entera hasta renovar: por eso el paso 2 es desconectarlo y volver a conectarlo.", title="Recién al renovar", kind="warn"))
save(c, "4-paso1.svg")

# ---------------------------------------------------------------- 4-paso5: NAT y port forwarding
c = Canvas(K(5), "Con NAT: los mismos puertos de punta a punta")
c.add(APNode(110, 200, "EAP", "en la sucursal", r=32))
c.add(Internet(240, 158, "Internet", "", w=200))
c.add(Box(540, 158, 280, 84, "Router de la central", "port forwarding"))
c.add(Generic(900, 158, "Controlador", "192.168.88.10", icon="server", w=252, dark=True))
c.add(Cable((146, 200), (236, 200), kind="data"))
c.add(Cable((444, 200), (536, 200), kind="data"))
c.add(Cable((824, 200), (896, 200), kind="flow"))
c.add(code(48, 312, 1104, "TCP+UDP  29810-29817  ->  192.168.88.10  29810-29817   (mismo puerto origen y destino)", 16, h=46))
c.add(Step(48, 312, 5))
c.add(Note(48, 390, 352, "En descubrimiento, adopción y gestión, origen y destino iguales. Desde la 5.9, solo web y portal admiten otro puerto de origen.", title="Mismo puerto", kind="ok"))
c.add(Note(424, 390, 352, "En el controlador 6 se sumó el TCP 29817, para los datos de monitoreo. Tiene que estar abierto para que equipo y controlador se hablen bien.", title="El 29817", kind="info"))
c.add(Note(800, 390, 352, "Exponer la gestión a internet abre el controlador al mundo. Si podés, túnel VPN entre sedes y option 138 por adentro.", title="Mejor por VPN", kind="alert"))
c.add(text(48, 584, "Dos controladores detrás de una IP: uno pasa a 29820-29827 y web 18043, con el puerto en la Inform URL.", 16, 500, INK2, FB))
save(c, "4-paso5.svg")
