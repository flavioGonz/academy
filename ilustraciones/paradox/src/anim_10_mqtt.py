"""Teoría lección 10: el módulo MQTT abre la conexión de salida y todo viaja por ahí."""
from _apdx import *

a = new(20, "MQTT: el módulo sale, nadie entra")
a.steps(["El módulo abre una conexión de salida, TCP 8883, hacia el servidor.",
         "La conexión queda abierta. No hace falta abrir puertos de entrada.",
         "Un evento sale por esa conexión al IPC10, que lo pasa al monitoreo.",
         "La app BlueEye llega por Swan, por la misma conexión saliente."], still=1)
a.add(card(a, 48, 180, 240, 110, "Central", "SP+ o MG", dark=True))
a.add(card(a, 48, 330, 240, 110, "IP180", "módulo MQTT"))
a.add(line(a, "M168 290V330", a.BLUE, 4))
a.add(a.box(380, 170, 26, 300, "#03213C", None, rx=8) + a.text(393, 500, "firewall", 15, a.GREY, a.MONO, 600, "middle"))
a.add(card(a, 520, 190, 300, 110, "Swan", "servidor de Paradox"))
a.add(card(a, 520, 360, 300, 110, "IPC10", "conversor de la receptora"))
a.add(card(a, 912, 360, 240, 110, "Monitoreo", "software"))
a.add(card(a, 912, 190, 240, 110, "BlueEye", "app del cliente"))
# túneles salientes
at(a, a.arrow("M288 385H514", a.BLUE, 4) + a.arrow("M288 370C380 300 420 250 514 245", a.BLUE, 4)
   + a.text(424, 414, "TCP 8883", 15, a.BLUE, a.MONO, 700), 0, 25, 0)
at(a, line(a, "M288 385H520", a.OK, 10) + line(a, "M288 370C380 300 420 250 520 245", a.OK, 10)
   + a.text(424, 414, "abierta", 15, a.OK, a.MONO, 700), 25, 100, 1)
at(a, chip(a, 393, 540, "entrada cerrada", "grey", anchor="middle"), 25, 100, 1)
# evento
mv = a.move([(0, 300, 350), (50, 300, 350), (60, 470, 350), (100, 470, 350)])
op = a.keyframes([(0, 0), (50, 0), (51, 1), (60, 1), (61, 0), (100, 0)])
a.add(a.group(f'<rect x="-34" y="-14" width="68" height="28" rx="14" fill="{a.BAD}"/><text x="0" y="5" font-family="{a.MONO}" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">evento</text>', mv, op, still=0))
at(a, a.arrow("M820 415H906", a.BAD, 3) + a.text(866, 400, "CID", 14, a.BAD, a.MONO, 700, "middle") + a.box(912, 360, 240, 110, "none", a.BAD, rx=14, sw=3), 60, 75, 0)
at(a, a.arrow("M906 245H826", a.CYAN, 4) + a.box(520, 190, 300, 110, "none", a.CYAN, rx=14, sw=3), 75, 100, 0)
caption(a, 600, [(0, 25, "Salida que piden IP180 e IP150M: TCP 8883 y 443, UDP 53, 123 y 5683, y el correo.", None),
                 (25, 50, "La conexión la inicia el módulo: por eso no hay port forward ni IP estática.", a.OK),
                 (50, 75, "Con módulos MQTT, el reporte es solo Contact ID y solo a IPC10 o VIPC20.", None),
                 (75, 100, "Legado (TURN) y MQTT no conviven en la misma central.", a.AMB)], still=1)
write(a, "10-t1.svg", "MQTT: el módulo sale, nadie entra",
      "Animación en cuatro tiempos. 1: el módulo IP180 abre conexiones de salida por TCP 8883 hacia Swan y hacia el IPC10, atravesando el firewall. "
      "2: las conexiones quedan abiertas y la entrada del firewall sigue cerrada. 3: un evento sale por la conexión al IPC10, que lo pasa en Contact ID al software de monitoreo. "
      "4: la app BlueEye llega a través de Swan, por la misma conexión que abrió el módulo.")
