"""Teoría de Mapa de capas: el Streaming Gateway toma un flujo de la cámara y lo reparte."""
from _anim_hc import *

caps = ["El Control Client inicia sesión en el SYS.",
        "Un operador pide el vivo: el gateway abre un flujo contra la cámara.",
        "El gateway reenvía ese flujo al primer cliente.",
        "Un segundo cliente pide la misma cámara: recibe el mismo flujo."]
a = new(24, "Arquitectura", "Un flujo desde la cámara, repartido por el gateway", caps, still=3)

# fijos
a.add(card(a, 60, 318, 250, 84, "Cámara", "CAM-01"))
a.add(a.box(420, 196, 360, 330, a.INK, a.INK, rx=18))
a.add(a.text(444, 236, "SYS", 22, a.WHITE, a.HEAD, 600))
a.add(a.text(444, 262, "gestión, usuarios, base", 15, DARK_SUB, a.MONO))
a.add(a.box(444, 318, 312, 84, a.NAVY2, a.CYAN, rx=14))
a.add(a.text(464, 354, "Streaming Gateway", 19, a.WHITE, a.SANS, 600))
a.add(a.text(464, 380, "dentro del SYS", 15, DARK_SUB, a.MONO))
a.add(card(a, 890, 226, 262, 84, "Control Client A", "puesto 1"))
a.add(card(a, 890, 420, 262, 84, "Control Client B", "puesto 2"))

# 1: login
s0, s1 = ph(a, 0)
token(a, "login", [(s0 + 3, 880, 252), (s0 + 14, 790, 252), (s1 - 2, 790, 252)], bg=a.BLUE)
vis(a, a.text(1021, 212, "usuario y clave", 15, a.BLUE, a.MONO, 600, "middle"), 0)
# 2: pedido y flujo de la cámara
s0, s1 = ph(a, 1)
token(a, "pedir vivo CAM-01", [(s0 + 2, 880, 290), (s0 + 12, 840, 360), (s0 + 20, 840, 360)], bg=a.BLUE)
vis(a, line(a, 312, 360, 440, 360, a.CYAN, 4, arrow=False), 1, 3)
vis(a, a.text(376, 340, "RTSP 554", 14, a.CYAN, a.MONO, 600, "middle"), 1, 3)
stream(a, 312, 360, 440, 360, s0 + 8, 100, a.CYAN)
vis(a, a.pill(185, 420, "1 flujo desde la cámara", a.CYAN, a.SLATE, anchor="middle"), 1, 3)
# 3: reenvío al cliente A
s0, s1 = ph(a, 2)
vis(a, line(a, 758, 344, 888, 270, a.CYAN, 4, arrow=False), 2, 3)
stream(a, 758, 344, 888, 270, s0 + 2, 100, a.CYAN)
# 4: cliente B pide la misma cámara
s0, s1 = ph(a, 3)
token(a, "pedir vivo CAM-01", [(s0 + 1, 880, 450), (s0 + 8, 840, 400), (s0 + 12, 840, 400)], bg=a.BLUE)
vis(a, line(a, 758, 380, 888, 460, a.CYAN, 4, arrow=False), 3)
stream(a, 758, 380, 888, 460, s0 + 8, 100, a.CYAN)
vis(a, a.pill(1152, 540, "2 clientes, la cámara sigue con 1 flujo", a.OK, a.OKBG, anchor="end"), 3)

a.add(a.text(48, 610, "Según el FAQ, el gateway alcanza hasta 200 cámaras reenviadas;", 17, a.TXT))
a.add(a.text(48, 638, "por encima se instala un Streaming Server, siempre en otra máquina que el SYS.", 17, a.TXT))
write(a, "1-t1.svg", "El Streaming Gateway reparte un flujo", [12, 35, 60, 90])
