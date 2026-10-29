#!/usr/bin/env python3
"""Lección 9 (Interno remoto) · Resumen, "Cómo se ve en la red": External Host sin Local Network Address. La UCM le
anuncia la IP pública también al teléfono de la oficina, que manda el audio hacia el router y la llamada queda
sin audio de ese lado; con Local Network Address cada uno recibe la dirección que le sirve. Fuentes: la lección
(si el destino está en Local Network Address pone 192.168.88.20, si no External Host; sin Local Network Address la
dirección externa no se arma bien; ejemplo: los internos de la oficina con audio cortado)."""
from _anim_gs_red import R

g = R(T=26, fix=88, kicker="GRANDSTREAM · INTERNO REMOTO · CÓMO SE VE EN LA RED",
      title="External Host solo no alcanza: la oficina pierde el audio")
g.steps([
    "Con External Host 203.0.113.10, la UCM le anuncia esa IP al remoto y su audio llega.",
    "Sin Local Network Address, al teléfono de la oficina también le anuncia 203.0.113.10.",
    "La 1001 manda su audio a 203.0.113.10, hacia el router: no llega a la central.",
    "Con Local Network Address 192.168.88.0/24, a la oficina le anuncia 192.168.88.20.",
])

Y, H = 190, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 232, H, "1001", "oficina", icon="tel", sub2="192.168.88.30"))
g.add(g.dev(336, Y, 250, H, "UCM", "192.168.88.20", icon="ucm", dark=True))
g.add(g.dev(642, Y, 250, H, "Router oficina", "203.0.113.10", icon="router", sub2="reenvía 5060 y RTP"))
g.add(g.dev(950, Y, 202, H, "Remoto", "en internet", icon="tel"))
g.add(g.wire(280, YL, 336, YL, g.BLUE))
g.add(g.wire(586, YL, 642, YL, g.BLUE))
g.add(g.wire(892, YL, 950, YL, g.BLUE, dash="8 6"))

LANE = Y - 20
# 1 · SDP al remoto y su audio
g.token([(461, LANE), (1051, LANE)], 2, 10, g.chip("SDP c=203.0.113.10", bg=g.CYAN, size=13, h=26), hold=11)
for k in range(2):
    t = 13 + k * 5
    g.token([(1051, LANE), (461, LANE)], t, t + 5, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 5.3)
# 2 · SDP a la 1001 con la pública
g.token([(461, LANE), (164, LANE)], 27, 34, g.chip("SDP c=203.0.113.10", bg=g.AMB, size=13, h=26), hold=35)
# 3 · el audio de la 1001 va al router
for k in range(3):
    t = 52 + k * 6
    g.token([(164, LANE), (767, LANE)], t, t + 6, g.chip("RTP", bg=g.BAD, size=13, h=24), hold=t + 6.3)
g.appear(g.pillc(767, Y + H + 12, "no vuelve a la central", g.BAD, g.BADBG, 13, 26), 58, 75)
g.appear(g.pillc(164, Y + H + 12, "no se escucha", g.BAD, g.BADBG, 13, 26), 60, 75)
# 4 · cada uno con lo suyo
g.token([(461, LANE), (164, LANE)], 77, 83, g.chip("SDP c=192.168.88.20", bg=g.OK, size=13, h=26), hold=84)
for k in range(2):
    t = 86 + k * 5
    g.token([(164, LANE), (461, LANE)], t, t + 4, g.chip("RTP", bg=g.OK, size=13, h=24), hold=t + 4.3)
g.fijo_only(f'<g transform="translate(300 {LANE})">' + g.chip("RTP", bg=g.OK, size=13, h=24) + '</g>')
g.appear(g.pillc(164, Y + H + 12, "audio en los dos sentidos", g.OK, g.OKBG, 13, 26), 86, 100)

# ajustes
PY = 352
g.add(g.box(48, PY, 520, 172, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, PY + 32, "PBX Settings > SIP Settings > NAT", 15, g.BLUE, g.MONO, 600))
g.add(g.text(68, PY + 70, "External Host", 15, g.GREY, g.MONO) + g.text(548, PY + 70, "203.0.113.10", 16, g.INK, g.MONO, 600, "end"))
g.add(g.text(68, PY + 104, "Local Network Address", 15, g.GREY, g.MONO))
g.appear(g.text(548, PY + 104, "(vacío)", 16, g.BAD, g.MONO, 600, "end"), 0, 75)
g.appear(g.text(548, PY + 104, "192.168.88.0/24", 16, g.OK, g.MONO, 600, "end"), 75, 100)
g.appear(g.box(58, PY + 84, 500, 30, "none", g.BAD, rx=8, sw=2.5), 27, 75)
g.appear(g.box(58, PY + 84, 500, 30, "none", g.OK, rx=8, sw=2.5), 75, 100)
g.add(g.text(68, PY + 146, "Use IP address in SDP: Sí", 15, g.GREY, g.MONO))

g.add(g.box(592, PY, 560, 172, "#03213C", None, rx=14))
g.add(g.text(612, PY + 32, "lo que anuncia la UCM en el SDP", 15, g.SKY, g.MONO))
g.add(g.text(612, PY + 76, "al remoto", 15, g.SKY, g.MONO) + g.text(800, PY + 76, "c=IN IP4 203.0.113.10", 17, g.MINT, g.MONO, 600))
g.add(g.text(612, PY + 120, "a la 1001", 15, g.SKY, g.MONO))
g.appear(g.text(800, PY + 120, "(todavía nada)", 16, g.SKY, g.SANS), 0, 27)
g.appear(g.text(800, PY + 120, "c=IN IP4 203.0.113.10", 17, g.GOLD, g.MONO, 600), 27, 75)
g.appear(g.text(800, PY + 120, "c=IN IP4 192.168.88.20", 17, g.MINT, g.MONO, 600), 75, 100)
g.appear(g.text(612, PY + 152, "una dirección que la 1001 no debería usar", 15, "#FF9C86", g.SANS, 600), 30, 75)
g.appear(g.text(612, PY + 152, "cada uno, la dirección que alcanza", 15, g.MINT, g.SANS, 600), 77, 100)

g.status(612, [
    (0, 25, "Para el remoto, la UCM está en 203.0.113.10: el router le pasa el audio.", g.OK),
    (25, 50, "Sin la lista de redes internas, la central no distingue adentro de afuera.", g.AMB),
    (50, 75, "Arreglaste al remoto y rompiste la oficina: el caso típico de este ajuste.", g.BAD),
    (75, 100, "Local Network Address con todas las redes que tengan teléfonos, VLAN de voz incluida.", g.OK),
], size=16)

g.done(9, "r1", "External Host solo no alcanza: la oficina pierde el audio",
       "Animación en cuatro tiempos con la interna 1001 de la oficina (192.168.88.30), la UCM en 192.168.88.20, el router de la oficina con IP pública 203.0.113.10, que reenvía 5060 y el RTP, y un interno remoto en internet; abajo, los ajustes NAT de la UCM y lo que anuncia en el SDP. "
       "1: con External Host 203.0.113.10, la UCM le anuncia al remoto c=IN IP4 203.0.113.10 y su audio llega por el router. "
       "2: con Local Network Address vacío, al teléfono de la oficina también le anuncia c=IN IP4 203.0.113.10. "
       "3: la 1001 manda su audio a 203.0.113.10, hacia el router, y no vuelve a la central: en la oficina no se escucha. "
       "4: con Local Network Address 192.168.88.0/24, a la 1001 le anuncia c=IN IP4 192.168.88.20 y al remoto 203.0.113.10: el audio va en los dos sentidos para los dos. "
       "Se cargan todas las redes que tengan teléfonos, VLAN de voz incluida.",
       [8, 36, 64, 92])
