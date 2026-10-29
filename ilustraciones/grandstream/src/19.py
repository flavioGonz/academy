"""Lección 19 · Troncal SIP de Antel: ilustración principal y pasos 1, 2 y 7.

Datos de ejemplo (rangos de documentación): IP del cliente 198.51.100.2/30, gateway de Antel 198.51.100.1,
servidor SIP 203.0.113.10, redes de Antel 203.0.113.0/24, números 2900 1001 a 2900 1008 de ejemplo.
"""
import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 19.svg: la troncal llega por IP, a su propio puerto
c = Canvas(K(), "La troncal de Antel llega por IP, a su propio puerto")
c.add(Zone(36, 132, 290, 304, "red privada de Antel", CYAN))
c.add(CloudBox(60, 160, "Servidor SIP", "203.0.113.10", w=240))
c.add(Generic(60, 318, "Equipo de Antel", "RJ45 de la troncal", icon="server", w=240))
c.add(Cable((180, 244), (180, 318), kind="logical", arrow=False))
c.add(text(198, 290, "no es internet", 15, 500, INK3, FM))

u = c.add(UCMBox(430, 150, w=340, name="UCM6300", sub="modo Dual", ports=("LAN", "WAN"), hl={"LAN": CYAN}))
lx, wx = u.port("LAN")[0], u.port("WAN")[0]
c.add(wire([(lx, 300), (lx, 360), (300, 360)], "data"))
c.add(pill(410, 352, "198.51.100.2/30", CYAN, WHITE, size=14))
c.add(text(424, 394, "LAN1 · sin gateway", 15, 500, INK3, FM, anchor="middle"))

c.add(Generic(890, 318, "Router del cliente", "192.168.88.1", icon="globe", w=262))
c.add(wire([(wx, 300), (wx, 360), (890, 360)], "data"))
c.add(pill(740, 352, "192.168.88.20", BLUE, WHITE, size=14))
c.add(text(740, 394, "LAN2 · con gateway", 15, 500, INK3, FM, anchor="middle"))
c.add(text(1021, 430, "teléfonos, web e internet", 15, 500, INK3, FB, anchor="middle"))

c.add(panel(860, 132, 292, 160, "Lo que entrega Antel", "soft", title_size=17))
lst, _ = bullet_list(880, 192, ["IP de cliente, máscara y gateway", "IP del servidor SIP", "números y canales del plan", "sin usuario ni contraseña"], 262, size=15, gap=3)
c.add(lst)

cards = [("Peer SIP Trunk", "Host Name: la IP del servidor de Antel. Sin registro.", "info"),
         ("OPTIONS de Antel", "Antel pregunta si la central vive; la UCM contesta 200 OK.", "ok"),
         ("Caller ID de la troncal", "Toda saliente con un número de la troncal, o Antel la rechaza.", "warn")]
for i, (t, d, k) in enumerate(cards):
    x = 48 + i * 372
    c.add(panel(x, 470, 352, 142, t, k, title_size=19))
    svg, _ = wrap(x + 20, 534, d, 312, 16, 400, INK2)
    c.add(svg)
c.add(text(48, 642, "Datos de ejemplo. Los reales salen de la planilla de Antel.", 15, 400, INK3, FB))
save(c, "19.svg")

# ---------------------------------------------------------------- 19-paso1: la planilla
c = Canvas(K(1), "La planilla que se le pide a Antel antes de la obra")
rows = [["Número de servicio", "P00000 (de ejemplo)"],
        ["Plan y canales", "TSIP8 · 8 simultáneas"],
        ["IP del cliente y máscara", "198.51.100.2 / 255.255.255.252"],
        ["Gateway de Antel", "198.51.100.1"],
        ["Servidor SIP y puerto", "203.0.113.10 · 5060 UDP"],
        ["Redes a rutear (SIP y audio)", "203.0.113.0/24"],
        ["Números de la troncal", "2900 1001 a 2900 1008"],
        ["Número por defecto", "2900 1001"],
        ["Codecs y DTMF", "G.711, T.38 · RFC 2833 o inband"],
        ["Formato entrante y saliente", "8 cifras, 598 o 09: a confirmar"]]
c.add(Table(48, 126, ["Dato", "Ejemplo"], rows, [330, 400], hl_row=5, row_h=44, mono_cols=(1,)))
c.add(Step(48, 126, 1))
c.add(panel(818, 126, 334, 200, "Lo que casi nunca viene", "warn", title_size=18))
lst, _ = bullet_list(838, 190, [("Todas las IP desde las que Antel manda señalización y audio", "warn"),
                                ("El formato del número que llega en las entrantes", "warn"),
                                ("Si el servidor contesta los OPTIONS de la central", "warn")], 300, size=15, gap=6)
c.add(lst)
c.add(Note(818, 348, 334, "El número de servicio, una P y cinco cifras, es el que pide el 0800 2599 para un reclamo. No es un número de teléfono.", kind="info", size=15))
c.add(text(48, 642, "Todos los valores son de ejemplo.", 15, 400, INK3, FB))
save(c, "19-paso1.svg")

# ---------------------------------------------------------------- 19-paso2: qué cable va a qué puerto
c = Canvas(K(2), "Modo Dual: Antel en LAN, la red del cliente en WAN")
u = c.add(UCMBox(400, 136, w=400, name="UCM6300", sub="Method: Dual", ports=("LAN", "WAN"), hl={"LAN": CYAN, "WAN": BLUE}))
c.add(Generic(48, 330, "Equipo de Antel", "RJ45 de la troncal", icon="server", w=270))
c.add(Generic(882, 330, "Switch del cliente", "red 192.168.88.0/24", icon="server", w=270))
c.add(wire([(u.port("LAN")[0], 286), (u.port("LAN")[0], 372), (318, 372)], "data"))
c.add(wire([(u.port("WAN")[0], 286), (u.port("WAN")[0], 372), (882, 372)], "data"))
c.add(pill(380, 364, "LAN1", CYAN, WHITE, size=14))
c.add(pill(780, 364, "LAN2", BLUE, WHITE, size=14))
c.add(Step(400, 136, 2))
c.add(panel(48, 448, 540, 150, "LAN1 · puerto LAN · troncal", "cyan", title_size=18))
lst, _ = bullet_list(68, 510, ["Static 198.51.100.2 / 255.255.255.252", "Sin gateway: a Antel se llega con la ruta estática del paso 3", "Nada más colgado de este puerto"], 500, size=15, gap=4)
c.add(lst)
c.add(panel(612, 448, 540, 150, "LAN2 · puerto WAN · red del cliente", "info", title_size=18))
lst, _ = bullet_list(632, 510, ["IP de la central en la red del cliente", "Default Interface: LAN2, con su gateway", "Teléfonos, web, internet y GDMS por acá"], 500, size=15, gap=4)
c.add(lst)
c.add(Note(848, 132, 304, "Cambiar el modo reinicia la central: backup antes y hacelo en sitio.", kind="warn", size=15))
save(c, "19-paso2.svg")

# ---------------------------------------------------------------- 19-paso7: la salida con el plan de Uruguay
c = Canvas(K(7), "La salida con el plan de numeración de Uruguay")
rows = [["_2XXXXXXX", "fijos de Montevideo y área metropolitana", "ruta Uruguay"],
        ["_4XXXXXXX", "fijos del interior", "ruta Uruguay"],
        ["_09XXXXXXX", "celulares: 0 más el número", "ruta Uruguay"],
        ["_0800XXXX", "sin cargo para el que llama", "ruta Uruguay"],
        ["_911  _10X", "emergencias: 911, 104, 105, 109", "sin PIN, Internal"],
        ["_00.", "internacional", "otra ruta, PIN"],
        ["_090XXXXX", "0900 a 0908, valor agregado", "PIN o sin ruta"]]
c.add(Table(48, 126, ["Patrón", "Qué es", "Ruta"], rows, [200, 430, 230], row_h=46, mono_cols=(0,)))
c.add(Step(48, 126, 7))
c.add(panel(926, 126, 226, 368, "Cómo sale", "info", title_size=18))
svg, hh = wrap(946, 186, "El número sale como se marcó: 8 cifras los fijos, 09 y 7 cifras los celulares.", 192, 15, 400, INK2)
c.add(svg)
svg, _ = wrap(946, 200 + hh, "Si Antel contesta 404 o 484, no es el formato que espera: miralo en el Request-URI de la captura y ajustá con Prepend o Strip.", 192, 15, 400, INK2)
c.add(svg)
c.add(Note(48, 520, 1104, "Emergencias: el 911 no se prueba llamando. Se revisa que el patrón exista, que no pida PIN y que salga por la troncal de Antel.", kind="alert", size=16))
save(c, "19-paso7.svg")
