#!/usr/bin/env python3
"""Lección 19 · Troncal SIP de Antel · teoría: una entrante de Antel de punta a punta (19-t1.svg).
OPTIONS de Antel y 200 OK, INVITE al número de la troncal, ruta entrante By DID, 180 y 200 OK con SDP,
ACK, RTP por el puerto de la troncal, refresco de sesión a mitad del intervalo y BYE.
Datos de ejemplo: servidor 203.0.113.10, UCM 198.51.100.2 (LAN1), número 2900 1001, interna 1001.
"""
from _anim_grandstream import G, SITE, PREV

g = G(T=28, fix=97, kicker="GRANDSTREAM · TRONCAL SIP DE ANTEL", title="Una entrante de Antel, de punta a punta")
g.steps([
    "Antel pregunta si la central vive: OPTIONS desde el Host Name y 200 OK de la UCM.",
    "INVITE al 2900 1001: la ruta entrante By DID con Strip 4 lo lleva a la 1001.",
    "Suena la 1001 y atiende: en el SDP la UCM pone su IP del lado de Antel.",
    "ACK, y el audio RTP va y viene por el puerto de la troncal, sin NAT.",
    "Session-Expires 600: refresco a los 300 s. Al cortar, BYE.",
], size=17)

XA, XU, XI = 190, 610, 1010
Y0, YB = 166, 640
g.lane(XA, Y0, YB, "Antel", "203.0.113.10", w=240)
g.lane(XU, Y0, YB, "UCM · LAN1", "198.51.100.2", w=240)
g.lane(XI, Y0, YB, "Interna 1001", "GRP2614", w=240)

B, OK, BAD, GREY, CY = g.BLUE, g.OK, g.BAD, g.GREY, g.CYAN
rows = [262, 302, 342, 382, 422, 462, 502, 546, 586, 626]

# 1 · OPTIONS
g.msg(XA, XU, rows[0], "OPTIONS", B, 2, 7, tok="OPTIONS")
g.msg(XU, XA, rows[1], "200 OK", OK, 9, 14, tok="200 OK")
# 2 · INVITE y ruta entrante
g.msg(XA, XU, rows[2], "INVITE sip:29001001@198.51.100.2", B, 22, 28, tok="INVITE")
g.appear(g.pill(XU + 14, rows[2] - 4, "_2900100X · By DID · Strip 4", g.INK, g.SLATE, 14, 28), 29, 40, still=0)
g.msg(XU, XI, rows[3], "INVITE 1001", B, 31, 37, tok="INVITE")
# 3 · suena y atiende
g.msg(XI, XU, rows[4], "180 Ringing", GREY, 42, 46)
g.msg(XU, XA, rows[4], "180 Ringing", GREY, 46, 50)
g.msg(XI, XU, rows[5], "200 OK", OK, 52, 55)
g.msg(XU, XA, rows[5], "200 OK · SDP c=198.51.100.2", OK, 55, 59, tok="200 OK")
# 4 · ACK y RTP
g.msg(XA, XU, rows[6], "ACK", B, 62, 65)
g.msg(XU, XI, rows[6], "ACK", B, 65, 68)
g.add(g.group(f'<path d="M{XA} {rows[7]} H{XI}" stroke="{CY}" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 10"/>',
              g.show(70, 100), g.keyframes([(0, "0"), (100, "-240")], "stroke-dashoffset"), still=1))
g.appear(g.text((XA + XU) / 2, rows[7] - 12, "RTP · audio en los dos sentidos", 15, CY, g.MONO, 600, "middle"), 70, 100)
g.appear(g.text((XU + XI) / 2, rows[7] - 12, "RTP", 15, CY, g.MONO, 600, "middle"), 70, 100)
# 5 · refresco y corte
g.msg(XU, XA, rows[8], "UPDATE o re-INVITE · a los 300 s", GREY, 82, 87)
g.msg(XA, XU, rows[9], "BYE", BAD, 91, 94)
g.msg(XU, XI, rows[9], "BYE", BAD, 94, 97)

PCTS = [6, 26, 34, 50, 58, 74, 88, 97]
name = "19-t1.svg"
out = SITE / name
g.save(str(out), "Una entrante de Antel, de punta a punta",
       "Animación en cinco tiempos con tres columnas: Antel con su servidor SIP 203.0.113.10, la UCM en su puerto LAN1 198.51.100.2 y la interna 1001. "
       "1: Antel manda OPTIONS desde la IP que la UCM tiene como Host Name del troncal y la UCM contesta 200 OK. "
       "2: llega un INVITE a sip:29001001@198.51.100.2; la ruta entrante con patrón _2900100X, destino By DID y Strip 4 lo lleva a la interna 1001, y la UCM le manda su propio INVITE. "
       "3: la 1001 suena y la UCM pasa el 180 Ringing a Antel; la 1001 atiende y la UCM contesta 200 OK con el SDP, donde la línea c= tiene 198.51.100.2, su IP del lado de Antel. "
       "4: Antel confirma con ACK y el audio RTP va y viene entre Antel y la 1001 pasando por la UCM, por el puerto de la troncal y sin NAT en el medio. "
       "5: con Session-Expires de 600 segundos, uno de los dos lados refresca la sesión a mitad del intervalo, a los 300 segundos, con un UPDATE o un re-INVITE; cuando el que llamó corta, Antel manda BYE y la UCM lo pasa a la 1001. Todos los datos son de ejemplo.")
for old in PREV.glob("_rev-19-t1-*.png"):
    old.unlink()
g._last = out
g.preview(PCTS, str(PREV / "_rev-19-t1"))
kb = out.stat().st_size / 1024
print(f"{name}: {kb:.0f} KB")
assert kb < 120
