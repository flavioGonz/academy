"""Teoría lección 4: DORA con reserva por MAC en el DHCP de Windows Server."""
from _awin import *

a = new(20, "DHCP en cuatro mensajes, con reserva por MAC")
a.steps(["Discover: la cámara grita a toda la red que necesita IP.",
         "Offer: el servidor ve la MAC y ofrece la IP reservada.",
         "Request: la cámara pide esa IP.",
         "Ack: confirmada, con gateway y DNS del ámbito."], still=3)
XL, XR = 330, 870
a.add(card(a, 48, 186, 250, 110, "Cámara", "00-11-22-33-44-55"))
a.add(card(a, 902, 186, 250, 110, "Servidor DHCP", "10.10.10.20 · IP fija", dark=True))
a.add(line(a, f"M{XL} 200V540", a.LINE, 2, "6 6") + line(a, f"M{XR} 200V540", a.LINE, 2, "6 6"))
rows = [(250, "DISCOVER · broadcast · MAC …-55", a.AMB, False, 0),
        (330, "OFFER · 10.10.10.150 (reserva)", a.BLUE, True, 25),
        (410, "REQUEST · quiero 10.10.10.150", a.BLUE, False, 50),
        (490, "ACK · router .1 · DNS .20", a.OK, True, 75)]
for y, label, col, back, s in rows:
    x1, x2 = (XR, XL + 8) if back else (XL, XR - 8)
    at(a, a.arrow(f"M{x1} {y}H{x2}", col, 4) + a.text((XL + XR) / 2, y - 12, label, 16, col, a.MONO, 600, "middle"), s, 100, 1)
# la reserva, en el servidor
at(a, a.box(902, 320, 250, 92, "#E5F0FB", a.CYAN, rx=12, sw=2) + a.text(918, 348, "reserva por MAC", 15, a.GREY, a.SANS, 600)
   + a.text(918, 374, "…-55 → 10.10.10.150", 16, a.BLUE, a.MONO, 600) + a.text(918, 398, "ámbito 'Lab CCTV'", 15, a.GREY, a.MONO, 500), 22, 100, 1)
# la cámara configurada
at(a, a.box(48, 446, 250, 92, a.OKBG, a.OK, rx=12, sw=2) + a.text(64, 474, "10.10.10.150 /24", 16, a.OK, a.MONO, 600)
   + a.text(64, 500, "gw 10.10.10.1", 15, a.TXT, a.MONO, 500) + a.text(64, 524, "dns 10.10.10.20", 15, a.TXT, a.MONO, 500), 78, 100, 1)
caption(a, 610, [(0, 25, "La cámara todavía no tiene IP: por eso el primer mensaje va a todos (broadcast).", None),
                 (25, 50, "El servidor busca la MAC en sus reservas: si está, ofrece siempre la misma IP.", a.BLUE),
                 (50, 75, "Si hubiera dos DHCP en la red, acá la cámara elige una oferta: por eso el de laboratorio va aislado.", a.AMB),
                 (75, 100, "Con dominio, un DHCP de Windows no autorizado en AD no llega a responder.", None)], still=3)
write(a, "4-t1.svg", "DHCP en cuatro mensajes, con reserva por MAC",
      "Animación en cuatro tiempos entre una cámara con MAC 00-11-22-33-44-55 y un servidor DHCP de Windows Server con IP fija 10.10.10.20. "
      "1: Discover, la cámara sin IP manda un broadcast pidiendo dirección. 2: Offer, el servidor encuentra la MAC en sus reservas del ámbito Lab CCTV y ofrece 10.10.10.150. "
      "3: Request, la cámara pide esa IP. 4: Ack, el servidor confirma con el router 10.10.10.1 y el DNS 10.10.10.20, y la cámara queda configurada. "
      "Las notas de pie recuerdan que dos DHCP en la misma red compiten y que en un dominio el DHCP tiene que estar autorizado.")
