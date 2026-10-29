#!/usr/bin/env python3
"""Lección 11 (Central cerrada) · Laboratorio, paso 4: Geo-IP Access Control. Se permiten solo los países que se usan;
lo demás se corta antes de llegar a Fail2ban. Antes de guardar, la UCM avisa si tu IP de administración quedaría
bloqueada; las IP de otras listas blancas pasan igual. Fuentes: manual de seguridad UCM (Geo-IP evalúa el origen
contra una base geográfica; banner de aviso si tu IP de gestión es de un país bloqueado; las IP de otras allowlists
pasan sin importar Geo-IP) y la lección (verificar antes que tu propia IP no quede bloqueada)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · CENTRAL CERRADA · LABORATORIO",
      title="Geo-IP: los países que se usan, y tu IP primero")
g.steps([
    "Geo-IP permite Uruguay y Argentina: el interno remoto de Montevideo registra.",
    "Un REGISTER desde un país que no está en la lista se corta: ni llega a Fail2ban.",
    "Vos administrás desde otro país, de viaje: la UCM avisa que tu IP quedaría bloqueada.",
    "Antes de guardar, tu IP va a una lista blanca: esas pasan aunque Geo-IP bloquee el país.",
])

R1, R2, R3 = 186, 304, 422
g.add(g.dev(48, R1, 300, 80, "Remoto en Montevideo", "198.51.100.7 · Uruguay", icon="tel"))
g.add(g.dev(48, R2, 300, 80, "Barrido", "203.0.113.99 · otro país", icon="bug", hl=g.BAD))
g.add(g.dev(48, R3, 300, 80, "Vos, de viaje", "192.0.2.44 · otro país", icon="laptop"))
UX, UW = 812, 340
g.add(g.box(UX, 186, UW, 320, g.WHITE, g.LINE, rx=16))
g.add(g.box(UX, 186, UW, 60, g.INK, rx=16) + g.box(UX, 226, UW, 20, g.INK, rx=0))
g.add(g.ico(UX + 16, 200, "ucm", g.CYAN, 1.3))
g.add(g.text(UX + 60, 224, "UCM · Geo-IP", 19, g.WHITE, g.HEAD, 600))
g.add(g.text(UX + 20, 278, "países permitidos", 15, g.GREY, g.MONO))
g.add(g.pill(UX + 20, 290, "Uruguay", g.OK, g.OKBG, 14, 28) + g.pill(UX + 130, 290, "Argentina", g.OK, g.OKBG, 14, 28))
g.add(g.text(UX + 20, 352, "listas blancas (pasan igual)", 15, g.GREY, g.MONO))
g.add(g.text(UX + 20, 380, "192.168.88.0/24", 16, g.INK, g.MONO, 600))
g.appear(g.text(UX + 20, 408, "192.0.2.44", 16, g.OK, g.MONO, 600) + g.pill(UX + 140, 390, "agregada", g.OK, g.OKBG, 13, 26), 82, 100)

X1, X2 = 348, UX
def ida(y, t0, t1, label, col, end=None, hold=None):
    g.token([(X1 + 80, y), (end or X2 - 80, y)], t0, t1, g.chip(label, bg=col, size=13, h=26), hold=hold or t1 + 0.4)

ida(R1 + 40, 3, 10, "REGISTER", g.BLUE)
g.token([(X2 - 80, R1 + 68), (X1 + 80, R1 + 68)], 11, 17, g.chip("200 OK", bg=g.OK, size=13, h=26), hold=17.4)
g.appear(g.pillc(198, R1 + 86, "registrado", g.OK, g.OKBG, 13, 24), 17, 100)
for k in range(2):
    ida(R2 + 40, 28 + k * 8, 33 + k * 8, "REGISTER", g.BLUE, end=X2 - 40)
g.appear(g.mark(X2 - 20, R2 + 40, False, 14) + g.text((X1 + X2) / 2, R2 + 76, "país no permitido: se corta en Geo-IP", 15, g.BAD, g.MONO, 600, "middle"), 32, 100)
g.add(g.wire(X1, R3 + 40, X2, R3 + 40, g.LINE, 2, "6 6"))
g.appear(g.text((X1 + X2) / 2, R3 + 30, "conectado a la web de la UCM", 15, g.GREY, g.MONO, 400, "middle"), 0, 100)

# banner de aviso
BX, BY, BW = X1 + 30, 532, 734
g.appear(g.box(48, BY, 1104, 74, g.AMBBG, g.AMB, rx=12, sw=2)
         + g.text(70, BY + 30, "Aviso de la UCM antes de guardar", 17, g.AMB, g.SANS, 600)
         + g.text(70, BY + 56, "Tu IP de administración es de un país bloqueado: conviene permitirlo antes de guardar.", 16, g.TXT), 54, 75)
g.appear(g.box(48, BY, 1104, 74, g.OKBG, g.OK, rx=12, sw=2)
         + g.text(70, BY + 30, "Ahora sí, Save", 17, g.OK, g.SANS, 600)
         + g.text(70, BY + 56, "Tu IP está en una lista blanca: entrás aunque Geo-IP bloquee el país donde estás.", 16, g.TXT), 82, 100)
g.appear(g.note(48, BY, 1104, None, ["System Settings > Security Settings > Geo-IP Access Control. Lo que se corta acá no llega a Fail2ban ni a la central."], "info"), 0, 54)
g.appear(g.pillc(198, R3 + 83, "quedaría afuera", g.BAD, g.BADBG, 13, 24), 56, 80)
g.appear(g.pillc(198, R3 + 83, "sigue adentro", g.OK, g.OKBG, 13, 24), 84, 100)

g.status(642, [
    (0, 25, "El remoto está en un país permitido: registra como siempre.", g.OK),
    (25, 50, "La mayoría de los barridos viene de países que el cliente no usa.", g.INK),
    (50, 75, "Activar Geo-IP en remoto sin tu IP te deja afuera de la central.", g.BAD),
    (75, 100, "Primero tu IP en la lista blanca; después Save.", g.OK),
])

g.done(11, "l1", "Geo-IP: los países que se usan, y tu IP primero",
       "Animación en cuatro tiempos con tres orígenes, el interno remoto de Montevideo (198.51.100.7, Uruguay), un barrido (203.0.113.99, otro país) y vos administrando de viaje (192.0.2.44, otro país), y la UCM con Geo-IP: países permitidos Uruguay y Argentina y listas blancas que pasan igual, con 192.168.88.0/24. "
       "1: el remoto de Montevideo manda REGISTER y recibe 200 OK: está en un país permitido. "
       "2: los REGISTER del barrido vienen de un país que no está en la lista y se cortan en Geo-IP, sin llegar a Fail2ban. "
       "3: vos estás conectado a la web desde otro país; antes de guardar, la UCM avisa con un banner que tu IP de administración pertenece a un país bloqueado y quedarías afuera. "
       "4: agregás tu IP 192.0.2.44 a una lista blanca, que pasa aunque Geo-IP bloquee el país, y recién ahí guardás: seguís adentro. "
       "Se configura en System Settings > Security Settings > Geo-IP Access Control.",
       [8, 40, 64, 92])
