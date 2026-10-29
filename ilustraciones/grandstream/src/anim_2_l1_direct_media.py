#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 3: Media > Enable Direct Media desactivado. Con la opción apagada la UCM lleva
el audio de los dos lados; activada, intenta que los teléfonos se manden el RTP directo (le pasa a cada uno la
dirección del otro con un nuevo INVITE) y con la 1002 detrás de un NAT ese audio directo no llega.
Fuentes: manual UCM630x (Enable Direct Media: por defecto el PBX rutea el audio por sí mismo; activado intenta
redirigirlo entre los extremos y no siempre se puede negociar); RFC 3261 (re-INVITE para cambiar la sesión)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · EXTENSIÓN SÓLIDA · LABORATORIO",
      title="Direct Media apagado: el audio pasa por la central")
g.steps([
    "Apagado, como viene: cada teléfono manda su audio a la UCM y la UCM lo reenvía.",
    "Activado: ya en la llamada, la UCM le pasa a cada teléfono la dirección del otro.",
    "La 1001 manda el audio a 192.168.1.50, una IP privada de otra red: no llega.",
    "Apagado otra vez: la central vuelve a llevar el audio y el NAT no lo corta.",
])

Y, H = 186, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 236, H, "1001", "oficina", icon="tel", sub2="192.168.88.31"))
g.add(g.dev(374, Y, 250, H, "UCM", "192.168.88.20", icon="ucm", dark=True))
g.add(g.cloud(664, Y + 14, 120, 68))
g.add(g.dev(824, Y, 150, H, "Router", "casa", sub2="198.51.100.7"))
g.add(g.dev(994, Y, 158, H, "1002", "remoto", sub2="192.168.1.50"))
g.add(g.wire(284, YL, 374, YL, g.BLUE))
g.add(g.wire(624, YL, 664, YL, g.BLUE))
g.add(g.wire(784, YL, 824, YL, g.BLUE))
g.add(g.wire(974, YL, 994, YL, g.BLUE))

# carril del audio
AY = Y + H + 34
rtp = lambda c: g.chip("RTP", bg=c, size=13, h=24)
C1, CU, C2 = 166, 499, 1073
for k in range(3):  # 1 · por la central, ida y vuelta
    t = 3 + k * 6
    g.token([(C1, AY), (CU, AY)], t, t + 4, rtp(g.OK), hold=t + 4.3)
    g.token([(CU, AY), (C2, AY)], t + 4.5, t + 10, rtp(g.OK), hold=t + 10.3)
    g.token([(C2, AY + 34), (CU, AY + 34)], t + 1, t + 6.5, rtp(g.OK), hold=t + 6.8)
    g.token([(CU, AY + 34), (C1, AY + 34)], t + 7, t + 10.5, rtp(g.OK), hold=t + 10.8)
for k in range(3):  # 4 · otra vez por la central
    t = 77 + k * 6
    g.token([(C1, AY), (CU, AY)], t, t + 4, rtp(g.OK), hold=t + 4.3)
    g.token([(CU, AY), (C2, AY)], t + 4.5, t + 10, rtp(g.OK), hold=t + 10.3)
    g.token([(C2, AY + 34), (CU, AY + 34)], t + 1, t + 6.5, rtp(g.OK), hold=t + 6.8)
    g.token([(CU, AY + 34), (C1, AY + 34)], t + 7, t + 10.5, rtp(g.OK), hold=t + 10.8)
# 2 · re-INVITE a cada teléfono
g.token([(CU, AY), (C1, AY)], 28, 34, g.chip("INVITE: el otro es 192.168.1.50", bg=g.CYAN, size=13, h=26), hold=48)
g.token([(CU, AY + 34), (C2 - 60, AY + 34)], 30, 38, g.chip("INVITE: el otro es 192.168.88.31", bg=g.CYAN, size=13, h=26), hold=48)
# 3 · audio directo que no llega
for k in range(3):
    t = 52 + k * 6
    g.token([(C1, AY), (720, AY)], t, t + 5, rtp(g.BAD), hold=t + 5.4)
g.appear(g.mark(720, AY, False, 15), 54, 75)
g.appear(g.pillc(720, AY + 26, "privada: no se enruta", g.BAD, g.BADBG, 13, 24), 54, 75)
# en el cuadro fijo, el instante del paso 3
g.fijo_only(f'<g transform="translate(560 {AY})">' + rtp(g.BAD) + '</g>')

# ajuste
g.appear(g.pillc(499, Y - 16, "Enable Direct Media: No", g.OK, g.OKBG, 13, 26), 0, 25)
g.appear(g.pillc(499, Y - 16, "Enable Direct Media: Sí", g.BAD, g.BADBG, 13, 26), 25, 75)
g.appear(g.pillc(499, Y - 16, "Enable Direct Media: No", g.OK, g.OKBG, 13, 26), 75, 100)

PY = 420
g.appear(g.note(48, PY, 700, "La central en el medio", ["Cada teléfono le habla a la UCM, que tiene una dirección que los dos", "alcanzan: la de la LAN para la 1001 y la pública para la 1002."], "ok"), 0, 25)
g.appear(g.note(48, PY, 700, "Nuevo INVITE con la dirección del otro", ["La 1001 recibe c=IN IP4 192.168.1.50; la 1002, c=IN IP4 192.168.88.31.", "Son direcciones privadas de dos redes distintas."], "amb"), 25, 50)
g.appear(g.note(48, PY, 700, "El audio directo se corta en el NAT", ["192.168.1.50 no existe en internet: el paquete se descarta en el", "camino. La llamada sigue armada y no se escucha."], "bad"), 50, 75)
g.appear(g.note(48, PY, 700, "Por eso, apagado", ["Media > Enable Direct Media: desactivado, junto con NAT activado.", "El manual avisa que no siempre se puede negociar el audio directo."], "ok"), 75, 100)
g.add(g.term(776, PY, 376, 126, "Media de cada extensión", [("NAT: activado", "#5BE0A5"), ("Direct Media: desactivado", "#5BE0A5")], size=16, lh=28))

g.status(626, [
    (0, 25, "Con Direct Media apagado, el audio de la 1002 llega y sale por la central.", g.OK),
    (25, 50, "Activado, la central intenta salir del medio de la llamada.", g.AMB),
    (50, 75, "Una IP privada de otra red no se alcanza: el audio directo no llega.", g.BAD),
    (75, 100, "Apagado, la central vuelve a llevar el audio de los dos lados.", g.OK),
])

g.done(2, "l1", "Direct Media apagado: el audio pasa por la central",
       "Animación en cuatro tiempos con la interna 1001 de la oficina (192.168.88.31), la UCM en 192.168.88.20, internet, el router de una casa (198.51.100.7) y la interna remota 1002 detrás de él (192.168.1.50); abajo, el carril del audio RTP. "
       "1: con Enable Direct Media en No, como viene, cada teléfono manda su audio a la UCM y la UCM lo reenvía al otro, en los dos sentidos. "
       "2: con Direct Media en Sí, ya en la llamada, la UCM le manda a cada teléfono un nuevo INVITE con la dirección del otro: la 1001 recibe 192.168.1.50 y la 1002 recibe 192.168.88.31. "
       "3: la 1001 manda el audio a 192.168.1.50, una IP privada de otra red, y se descarta en el camino: la llamada sigue armada y no se escucha. "
       "4: con Direct Media apagado otra vez, la central vuelve a llevar el audio de los dos lados y el NAT no lo corta. "
       "Recuadro: en Media de cada extensión, NAT activado y Direct Media desactivado.",
       [10, 36, 62, 88])
