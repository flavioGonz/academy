"""Teoría lección 1: qué repositorio responde a apt update y qué hace full-upgrade que upgrade no."""
from _apmx import *

a = new(20, "Repositorio y full-upgrade, en cuatro tiempos")
a.steps(["apt update contra enterprise sin suscripción: 401.",
         "Enterprise deshabilitado: responde no-subscription.",
         "apt upgrade no puede quitar paquetes: queda a medias.",
         "apt full-upgrade instala y quita lo necesario: coherente."], still=3)
# host
a.add(card(a, 48, 190, 300, 150, "pve1", "Proxmox VE 9", dark=True))
for s, e, cmd, st in [(0, 50, "apt update", 0), (50, 75, "apt upgrade", 0), (75, 100, "apt full-upgrade", 1)]:
    at(a, a.box(68, 268, 260, 44, "#03213C", None, rx=10) + a.text(84, 296, "# " + cmd, 17, "#D9E9F8", a.MONO, 600), s, e, still=st)
# repos
a.add(card(a, 780, 180, 372, 92, "pve-enterprise", "pide clave de suscripción"))
a.add(card(a, 780, 300, 372, 92, "pve-no-subscription", "gratis, sin clave"))
at(a, a.box(780, 180, 372, 92, a.SLATE, a.LINE, rx=14, sw=2) + a.text(800, 214, "pve-enterprise", 19, a.GREY, a.HEAD, 600) + chip(a, 800, 228, "Enabled: no", "grey", 15), 25, 100, still=1)
# tiempo 1: pedido y 401
at(a, a.arrow("M352 230 H772", a.BAD, 4) + chip(a, 470, 196, "GET … 401 Unauthorized", "bad"), 0, 25, 0)
# tiempo 2-4: respuesta de no-subscription
at(a, a.arrow("M352 300 C 540 300, 600 346, 772 346", a.OK, 4) + chip(a, 440, 326, "listas de paquetes OK", "ok"), 25, 100, still=1)
# paquetes
a.add(a.text(48, 420, "EJEMPLO GENÉRICO DE DEPENDENCIAS", 15, a.GREY, a.MONO, 600, extra='letter-spacing="1.5"'))
P = [(48, "paquete A"), (424, "paquete B"), (800, "paquete C")]
for x, n in P:
    a.add(a.box(x, 436, 352, 120, a.WHITE, a.LINE, rx=14, sw=2) + a.text(x + 20, 468, n, 18, a.INK, a.SANS, 600))
# estados por tiempo
def st(x, label, kind, s, e, still=0, sub=None):
    g = chip(a, x + 20, 486, label, kind, 15)
    if sub:
        g += a.text(x + 20, 540, sub, 15, a.GREY, a.SANS, 400)
    at(a, g, s, e, still)

for s, e in [(0, 25), (25, 50)]:
    st(48, "9.1 instalado", "grey", s, e)
    st(424, "no instalado", "grey", s, e, sub="la 9.2 de A lo necesita")
    st(800, "instalado", "grey", s, e, sub="la 9.2 de A lo reemplaza")
st(48, "9.1 retenido", "amb", 50, 75, sub="no se actualiza")
st(424, "no instalado", "grey", 50, 75)
st(800, "sigue", "grey", 50, 75, sub="upgrade no quita nada")
st(48, "9.2 instalado", "ok", 75, 100, still=1)
st(424, "instalado", "ok", 75, 100, still=1, sub="lo pidió la 9.2")
st(800, "quitado", "bad", 75, 100, still=1, sub="ya no hace falta")
caption(a, 610, [(0, 25, "Sin clave, enterprise no deja bajar nada: el primer apt update termina en error.", a.BAD),
                 (25, 50, "Con enterprise apagado y no-subscription sumado, apt update baja las listas sin error.", a.OK),
                 (50, 75, "apt upgrade no puede quitar paquetes: lo que pide un cambio así, queda retenido.", a.AMB),
                 (75, 100, "full-upgrade instala lo nuevo y quita lo que sobra: el host queda en una versión coherente.", a.OK)], still=3)
write(a, "1-t1.svg", "Repositorio y full-upgrade, en cuatro tiempos",
      "Animación en cuatro tiempos. 1: el host pve1 corre apt update contra el repositorio pve-enterprise sin clave de suscripción y recibe 401 Unauthorized. "
      "2: con enterprise deshabilitado (Enabled: no), responde pve-no-subscription y las listas de paquetes bajan bien. "
      "3: con apt upgrade, un paquete A que en su versión 9.2 necesita instalar B y reemplazar a C queda retenido en 9.1, porque upgrade no quita paquetes. "
      "4: con apt full-upgrade, A pasa a 9.2, B se instala y C se quita: el host queda coherente. Las dependencias son un ejemplo genérico.")
