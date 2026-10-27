import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *


def site(x, y, name, chips, w=250):
    out = [panel(x, y, w, 128, name, "soft")]
    cx = x + 20
    for ch in chips:
        wd = len(ch) * 9.2 + 26
        out.append(Chip(cx, y + 92, ch, "blue").svg())
        cx += wd + 10
    return "".join(out)


# ---------------------------------------------------------------- 5.svg: clientes, sitios y equipos
c = Canvas(K(), "Un sitio por sede con gateway, un usuario por persona")
c.add(Generic(420, 120, "Controlador", "Software o Central Standard, MSP", icon="server", w=360, dark=True))
for cx, name in ((345, "Cliente A"), (905, "Cliente B")):
    c.add(rect(cx - 110, 238, 220, 50, WHITE, BLUE, rx=25, sw=2))
    c.add(mid(cx, 270, name, 18, 600, INK, FD))
    c.add(wire([(600, 204), (600, 220), (cx, 220), (cx, 238)], kind="logical"))
c.add(site(80, 332, "Sitio Central", ["ER", "SW", "EAP"]))
c.add(site(360, 332, "Sitio Sucursal", ["ER", "EAP"]))
c.add(site(780, 332, "Sitio Local", ["ER", "SW", "EAP"]))
for sx in (205, 485):
    c.add(wire([(345, 288), (345, 310), (sx, 310), (sx, 332)], kind="logical"))
c.add(wire([(905, 288), (905, 332)], kind="logical"))
c.add(text(1056, 380, "Un gateway", 15, 600, INK3, FB))
c.add(text(1056, 402, "por sitio", 15, 600, INK3, FB))
c.add(Note(48, 490, 352, "Los perfiles WiFi y el roaming son por sitio: dos sitios no hacen roaming entre sí.", title="WiFi y roaming", kind="info"))
c.add(Note(424, 490, 352, "Auto IPsec une sitios del mismo controlador, cada uno con su gateway.", title="VPN entre sitios", kind="ok"))
c.add(Note(800, 490, 352, "MSP en Software Controller y Central Standard; no en Essentials ni en los OC.", title="Modo MSP", kind="warn"))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso1: Site List con dos sitios
c = Canvas(K(1), "Site List: un sitio para cada sede con su gateway")
c.add(Window(48, 124, 560, 176, "Omada · Global View", path="Dashboard > Site List", rows=[("Central", "Uruguay · America/Montevideo"), ("Sucursal", "Uruguay · America/Montevideo")], hl=1))
c.add(Step(48, 124, 1))
c.add(panel(648, 124, 504, 150, "Un sitio, dos gateways", "alert"))
c.add(Chip(672, 214, "ER central", "blue"))
c.add(Chip(812, 214, "ER sucursal", "blue"))
c.add(Mark(1100, 206, ok=False))
c.add(text(672, 256, "Un sitio adopta un solo gateway.", 16, 500, INK2, FB))
c.add(panel(648, 296, 504, 150, "Dos sitios, uno cada uno", "ok"))
c.add(Chip(672, 386, "Central: ER", "blue"))
c.add(Chip(822, 386, "Sucursal: ER", "blue"))
c.add(Mark(1100, 378, ok=True))
c.add(text(672, 428, "Cada sede con router es un sitio.", 16, 500, INK2, FB))
c.add(Note(48, 328, 560, "Región Uruguay y zona horaria America/Montevideo en cada sitio: definen canales legales y la hora de los horarios programados.", title="Al crear cada sitio", kind="info"))
c.add(Note(48, 500, 1104, "Con todo en el sitio Default funciona hasta que llega el segundo gateway: ahí hay que rehacer. Conviene arrancar con un sitio por sede.", kind="warn"))
save(c, "5-paso1.svg")

# ---------------------------------------------------------------- 5-paso2: roles y un usuario de solo lectura
c = Canvas(K(2), "Un usuario por persona, con el rol justo")
c.add(Table(48, 124, ["Rol", "Para quién", "Qué puede"], [
    ["Main Administrator", "La empresa", "Todo en su vista"],
    ["Administrator", "Cada técnico", "Casi todo; no migra clientes ni hace backups automáticos"],
    ["Viewer", "El cliente", "Mirar estado y ajustes, sin cambiar"],
], [250, 200, 654], row_h=48, hl_row=2))
c.add(Step(48, 124, 2))
c.add(panel(48, 344, 540, 170, "viewer-sucursal", "soft"))
c.add(lines(72, 410, [("Rol: Viewer", INK), "Sitios: solo Sucursal", "Clave de ejemplo: Visor-Lab-2026"], 16, 30))
c.add(Note(612, 344, 540, "Entrá con ese usuario: tiene que ver solo Sucursal y no poder cambiar nada. Si ve Central o puede editar, revisá el rol.", title="Prueba (paso 3)", kind="ok"))
c.add(Note(612, 490, 540, "Con MSP hay dos niveles: rol MSP para la vista MSP y rol Customer para la vista Global y la del sitio.", title="Dos niveles en MSP", kind="info"))
save(c, "5-paso2.svg")
