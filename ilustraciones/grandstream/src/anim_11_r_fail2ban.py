#!/usr/bin/env python3
"""Lección 11 (Central cerrada) · Resumen, "Cómo se ve en la red": Fail2ban en el tiempo. Un barrido acumula
REGISTER fallidos hasta el límite de reintentos, la IP queda en la Blocklist 600 s y la UCM deja de contestarle;
la oficina técnica en la Allowlist nunca se banea. Fuentes: manual de seguridad UCM (Fail2Ban activo de fábrica,
Banned Duration 600 s, 0 = permanente; Allowlist exenta aunque pase el umbral; Blocklist con el tiempo que falta;
SIP Defense: al llegar al límite, la UCM no responde más pedidos SIP de ese host)."""
from _anim_gs_red import R

g = R(T=28, fix=40, kicker="GRANDSTREAM · CENTRAL CERRADA · CÓMO SE VE EN LA RED",
      title="Fail2ban: al que insiste, la central deja de contestarle")
g.steps([
    "Un barrido desde 198.51.100.66 prueba claves con REGISTER: cada fallo suma.",
    "Llega al límite de reintentos: va a la Blocklist por 600 s y la UCM no le contesta más.",
    "La oficina técnica también se equivoca de clave: está en la Allowlist y no se banea.",
    "Pasados los 600 s sale de la Blocklist; si vuelve a insistir, vuelve a entrar.",
])

A_Y, O_Y = 196, 372
g.add(g.dev(48, A_Y, 286, 96, "Barrido", "198.51.100.66", icon="bug", hl=g.BAD))
g.add(g.dev(48, O_Y, 286, 96, "Oficina técnica", "198.51.100.20", icon="laptop"))
UX, UW = 800, 352
g.add(g.box(UX, 186, UW, 292, g.WHITE, g.LINE, rx=16))
g.add(g.box(UX, 186, UW, 60, g.INK, rx=16) + g.box(UX, 226, UW, 20, g.INK, rx=0))
g.add(g.ico(UX + 16, 200, "ucm", g.CYAN, 1.3))
g.add(g.text(UX + 60, 224, "UCM · Fail2Ban", 19, g.WHITE, g.HEAD, 600))
g.add(g.text(UX + 20, 278, "Banned Duration", 15, g.GREY, g.MONO) + g.text(UX + UW - 20, 278, "600 s", 16, g.INK, g.MONO, 600, "end"))
g.add(g.text(UX + 20, 306, "Allowlist", 15, g.GREY, g.MONO) + g.text(UX + UW - 20, 306, "198.51.100.20", 16, g.OK, g.MONO, 600, "end"))
g.add(g.text(UX + 20, 346, "fallos de 198.51.100.66", 15, g.GREY, g.MONO))
# contador
CX0, CW = UX + 20, UW - 40
g.add(g.box(CX0, 358, CW, 18, "#E6EDF4", rx=9))
g.add(f'<line x1="{CX0 + CW}" y1="352" x2="{CX0 + CW}" y2="382" stroke="{g.BAD}" stroke-width="3"/>')
g.add(g.text(CX0 + CW, 398, "límite", 13, g.BAD, g.MONO, 600, "end"))
g.bar(CX0, 358, CW, 18, 3, 22, g.AMB, hold=50)
g.add(g.text(UX + 20, 432, "Blocklist", 15, g.GREY, g.MONO))
g.appear(g.text(UX + UW - 20, 432, "(vacía)", 16, g.GREY, g.MONO, 400, "end"), 0, 24)
g.appear(g.text(UX + UW - 20, 432, "198.51.100.66 · 600 s", 16, g.BAD, g.MONO, 600, "end"), 24, 84)
g.appear(g.text(UX + UW - 20, 432, "(vacía)", 16, g.GREY, g.MONO, 400, "end"), 84, 100)
g.appear(g.box(UX + 10, 412, UW - 20, 32, "none", g.BAD, rx=8, sw=2.5), 24, 50)

# 1 · fallos que suman
X1, X2 = 334, UX
LA = A_Y + 48
for k in range(4):
    t = 3 + k * 5
    g.token([(X1 + 70, LA - 14), (X2 - 70, LA - 14)], t, t + 2.5, g.chip("REGISTER · clave mala", bg=g.BLUE, size=13, h=24), hold=t + 2.7)
    g.token([(X2 - 70, LA + 16), (X1 + 70, LA + 16)], t + 2.6, t + 4.6, g.chip("rechazo", bg=g.GREY, size=13, h=24), hold=t + 4.8)
# 2 · baneado: sin respuesta
for k in range(3):
    t = 28 + k * 6
    g.token([(X1 + 70, LA - 14), (X2 - 30, LA - 14)], t, t + 3, g.chip("REGISTER", bg=g.BLUE, size=13, h=24), hold=t + 3.2)
g.appear(g.mark(X2 - 14, LA - 14, False, 13) + g.text((X1 + X2) / 2, LA + 22, "sin respuesta: la UCM no le contesta", 15, g.BAD, g.MONO, 600, "middle"), 30, 50)
g.appear(g.pillc(191, A_Y + 108, "baneada 600 s", g.BAD, g.BADBG, 13, 26), 24, 84)
# 3 · oficina en la Allowlist
LO = O_Y + 48
for k in range(4):
    t = 52 + k * 5
    g.token([(X1 + 70, LO - 14), (X2 - 70, LO - 14)], t, t + 2.5, g.chip("login con clave mala", bg=g.BLUE, size=13, h=24), hold=t + 2.7)
    g.token([(X2 - 70, LO + 16), (X1 + 70, LO + 16)], t + 2.6, t + 4.6, g.chip("rechazo · sigue", bg=g.GREY, size=13, h=24), hold=t + 4.8)
g.appear(g.pillc(191, O_Y + 108, "nunca se banea", g.OK, g.OKBG, 13, 26), 56, 100)
g.appear(g.box(UX + 10, 290, UW - 20, 26, "none", g.OK, rx=8, sw=2.5), 52, 75)
# 4 · sale y vuelve
g.appear(g.pillc(191, A_Y + 108, "fuera de la Blocklist", g.AMB, g.AMBBG, 13, 26), 84, 100)
g.token([(X1 + 70, LA - 14), (X2 - 70, LA - 14)], 88, 91, g.chip("REGISTER · clave mala", bg=g.BLUE, size=13, h=24), hold=91.2)
g.token([(X2 - 70, LA + 16), (X1 + 70, LA + 16)], 91.3, 93.5, g.chip("rechazo", bg=g.GREY, size=13, h=24), hold=93.7)
g.bar(CX0, 358, CW * 0.25, 18, 88, 94, g.AMB, hold=100)
g.fijo_only(f'<g transform="translate({X1 + 300} {LA - 14})">' + g.chip("REGISTER", bg=g.BLUE, size=13, h=24) + '</g>')

g.add(g.note(48, 512, 1104, None, ["SIP Defense mira REGISTER, INVITE y SUBSCRIBE fallidos; Login Attack Defense, los ingresos a la web. Banned Duration en 0 es baneo permanente."], "info"))

g.status(628, [
    (0, 25, "Cada intento fallido queda contado contra esa IP.", g.INK),
    (25, 50, "Baneada: sus pedidos SIP ni se contestan. Probar claves se vuelve lento.", g.BAD),
    (50, 75, "Tu red local y la IP fija de la oficina técnica, siempre en la Allowlist.", g.OK),
    (75, 100, "Un barrido que vuelve a insistir vuelve a quedar afuera.", g.AMB),
])

g.done(11, "r1", "Fail2ban: al que insiste, la central deja de contestarle",
       "Animación en cuatro tiempos con un barrido desde 198.51.100.66, la oficina técnica en 198.51.100.20 y la UCM con Fail2Ban: Banned Duration 600 s, Allowlist con 198.51.100.20, un contador de fallos con su límite y la Blocklist. "
       "1: el barrido manda REGISTER con claves malas, la UCM los rechaza y cada fallo suma en el contador. "
       "2: al llegar al límite de reintentos, 198.51.100.66 entra en la Blocklist por 600 segundos y la UCM deja de contestarle: sus REGISTER quedan sin respuesta. "
       "3: la oficina técnica también falla el ingreso varias veces; está en la Allowlist y nunca se banea. "
       "4: pasados los 600 segundos la IP sale de la Blocklist; si vuelve a insistir, los fallos vuelven a sumar y vuelve a entrar. "
       "Nota: SIP Defense mira REGISTER, INVITE y SUBSCRIBE fallidos y Login Attack Defense los ingresos a la web; Banned Duration en 0 es baneo permanente.",
       [10, 40, 66, 92])
