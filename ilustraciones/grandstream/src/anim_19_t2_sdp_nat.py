#!/usr/bin/env python3
"""Lección 19 · Troncal SIP de Antel · teoría: con NAT en el medio, el SDP queda con la IP privada (19-t2.svg).
El router traduce la IP del paquete pero no la del contenido SIP; Antel manda el audio a una IP que no existe
en su red. Arreglo: la troncal directo a la central, o External Host con la IP de Antel si hay firewall.
Datos de ejemplo: UCM 192.168.88.20 detrás del router, IP de cliente de Antel 198.51.100.2, servidor 203.0.113.10.
"""
from _anim_grandstream import G, SITE, PREV

g = G(T=24, fix=90, kicker="GRANDSTREAM · TRONCAL SIP DE ANTEL", title="Con NAT en el medio, el SDP queda con la IP privada")
g.steps([
    "La UCM, detrás de un router, manda el INVITE con c=192.168.88.20 en el SDP.",
    "El router cambia la IP del paquete a 198.51.100.2, pero no la del SDP.",
    "Antel manda el audio a 192.168.88.20, que no existe en su red: audio de un lado.",
    "Troncal directo a la central (o External Host 198.51.100.2): el SDP dice la verdad.",
], size=17)

B, OK, BAD, GREY, INK, CY = g.BLUE, g.OK, g.BAD, g.GREY, g.INK, g.CYAN
Y = 300
g.add(g.node(48, Y - 50, 250, 100, "UCM", "192.168.88.20", dark=True))
g.add(g.node(475, Y - 50, 250, 100, "Router con NAT", "sale como 198.51.100.2"))
g.add(g.node(902, Y - 50, 250, 100, "Antel", "203.0.113.10"))
g.add(f'<path d="M298 {Y} H475 M725 {Y} H902" stroke="{g.LINE}" stroke-width="5"/>')
g.appear(g.pill(600, Y - 92, "SIP ALG o firewall sin SIP", g.AMB, g.AMBBG, 14, 28, ), 0, 75, still=0)

def pkt(ip, sdp, ip_col=INK, sdp_col=INK):
    return (g.box(-122, -34, 244, 68, g.WHITE, g.LINE, rx=10, sw=2)
            + g.text(-108, -8, f"IP  {ip}", 14, ip_col, g.MONO, 600)
            + g.text(-108, 20, f"SDP c={sdp}", 14, sdp_col, g.MONO, 600))

# 1 y 2 · el INVITE atraviesa el router
g.token([(173, Y + 130), (600, Y + 130)], 3, 18, pkt("192.168.88.20", "192.168.88.20"), hold=26)
g.token([(600, Y + 130), (1027, Y + 130)], 30, 44, pkt("198.51.100.2", "192.168.88.20", OK, BAD), hold=50)
g.appear(g.text(600, Y + 196, "cambia la IP del paquete", 15, OK, g.SANS, 600, "middle"), 27, 50)
g.appear(g.text(600, Y + 218, "el SDP sigue con la privada", 15, BAD, g.SANS, 600, "middle"), 27, 50)
# 3 · el audio va a una IP que no existe para Antel
g.token([(902, Y + 74), (760, Y + 74)], 53, 62, g.chip("RTP → 192.168.88.20", bg=BAD, size=13, h=24), hold=75)
g.appear(g.mark(648, Y + 74, False, 15), 62, 75)
g.appear(g.note(48, 520, 1104, "Audio de un lado", ["La UCM manda su audio y Antel lo recibe, pero la respuesta va a una IP privada que no existe del otro lado. Es el mismo mecanismo de Audio de un lado."], "bad"), 55, 75)
# 4 · el arreglo
g.appear(g.node(48, Y - 50, 250, 100, "UCM · LAN1", "198.51.100.2", dark=True), 78, 100)
g.appear(g.box(475, Y - 50, 250, 100, g.OKBG, g.OK, rx=14, sw=3) + g.text(600, Y - 4, "Sin NAT", 20, OK, g.HEAD, 600, "middle")
         + g.text(600, Y + 22, "cable directo a la central", 15, OK, g.SANS, 600, "middle"), 78, 100)
g.token([(173, Y + 130), (1027, Y + 130)], 79, 88, pkt("198.51.100.2", "198.51.100.2", OK, OK), hold=100)
g.token([(902, Y + 74), (420, Y + 74)], 89, 96, g.chip("RTP → 198.51.100.2", bg=OK, size=13, h=24), hold=100, still=1)
g.appear(g.note(48, 520, 1104, "Dos formas de que el SDP diga la verdad", ["Troncal directo a la central en modo Dual: no hay NAT. Con un firewall en el medio: External Host 198.51.100.2 y el ALG apagado."], "ok"), 78, 100)
g.fijo_only(f'<g transform="translate(1027 {Y + 130})">' + pkt("198.51.100.2", "198.51.100.2", OK, OK) + "</g>")

PCTS = [8, 22, 40, 58, 70, 84, 96]
name = "19-t2.svg"
out = SITE / name
g.save(str(out), "Con NAT en el medio, el SDP queda con la IP privada",
       "Animación en cuatro tiempos con la UCM 192.168.88.20, un router con NAT que sale como 198.51.100.2 y Antel con su servidor 203.0.113.10. Debajo, el paquete con dos datos: la IP del paquete y la línea c= del SDP. "
       "1: la UCM, detrás del router, manda el INVITE con IP 192.168.88.20 y c=192.168.88.20 en el SDP. "
       "2: el router traduce la IP del paquete a 198.51.100.2 pero no toca el SDP, que sigue con la privada; un SIP ALG o un firewall sin soporte de SIP hace lo mismo o lo reescribe mal. "
       "3: Antel manda el audio RTP a 192.168.88.20, que no existe en su red, y se pierde: audio de un lado, el mismo mecanismo de la lección Audio de un lado. "
       "4: con la troncal conectada directo a la central en modo Dual no hay NAT, y con un firewall en el medio se carga External Host 198.51.100.2 y se apaga el ALG: el SDP lleva 198.51.100.2 y el audio vuelve. Datos de ejemplo.")
for old in PREV.glob("_rev-19-t2-*.png"):
    old.unlink()
g._last = out
g.preview(PCTS, str(PREV / "_rev-19-t2"))
kb = out.stat().st_size / 1024
print(f"{name}: {kb:.0f} KB")
assert kb < 120
