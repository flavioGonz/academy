#!/usr/bin/env python3
"""Lección 37, teoría "Cómo funciona": la tabla de rutas en los dos cortes (sesión caída y PPPoE arriba sin internet)."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=30, kicker="MIKROTIK · DOS WAN", title="PPPoE y 4G: dos cortes, dos caminos en la tabla")
a.steps([
    "Normal: las recursivas por los testigos mandan; el 4G espera.",
    "Corte 1, se cae la sesión: la /32 queda inactiva y entra el 4G.",
    "Corte 2, PPPoE arriba sin internet: lo ven los pings a los testigos.",
    "Con add-default-route=yes esa ruta seguiría activa: sin failover.",
    "Vuelve la fibra: las recursivas mandan otra vez.",
], still=2)

TX, TY, TW = 48, 172, 772
a.add(a.box(TX, TY, TW, 392, a.WHITE, a.LINE, rx=18))
a.add(a.text(TX + 22, TY + 34, "/ip/route", 18, a.INK, a.HEAD, 600))
for x, s in ((22, "destino"), (196, "gateway"), (440, "dist")):
    a.add(a.text(TX + x, TY + 62, s, 15, a.GREY, a.MONO))
ROWS = [("1.1.1.1/32", "pppoe-antel", "1"), ("9.9.9.9/32", "pppoe-antel", "1"),
        ("0.0.0.0/0", "1.1.1.1  recursiva", "1"), ("0.0.0.0/0", "9.9.9.9  recursiva", "1"),
        ("0.0.0.0/0", "192.168.8.1  DHCP 4G", "2")]
RY0, RS = TY + 76, 52
PW = 30
ACT = ("activa", a.OK, a.OKBG)
INA = ("inactiva", a.BAD, a.BADBG)
ESP = ("espera", a.GREY, "#E6EDF4")
ST = {0: [ACT, INA, ACT, ACT, ACT], 1: [ACT, INA, ACT, ACT, ACT],
      2: [ACT, INA, INA, INA, ACT], 3: [ACT, INA, INA, INA, ACT], 4: [ESP, ACT, ACT, ESP, ESP]}
for i, (d, g, dist) in enumerate(ROWS):
    y = RY0 + i * RS
    a.add(a.box(TX + 12, y, TW - 24, 44, a.SLATE, rx=10))
    a.add(a.text(TX + 22, y + 29, d, 16, a.INK, a.MONO, 600))
    a.add(a.text(TX + 196, y + 29, g, 16, a.TXT, a.MONO))
    a.add(a.text(TX + 440, y + 29, dist, 16, a.INK, a.MONO, 600))
    for k in range(5):
        lab, fg, bg = ST[i][k]
        en(a, a.pill(TX + TW - 24, y + 8, lab, fg, bg, 14, 28, "end"), k * 20, (k + 1) * 20, still=1 if k == 2 else 0)
# por qué cae cada una
NOTE = {(2, 1): "sin gateway", (3, 1): "sin gateway", (2, 2): "testigo no contesta", (3, 2): "testigo no contesta",
        (2, 3): "testigo no contesta", (3, 3): "testigo no contesta", (0, 1): "interfaz caída", (1, 1): "interfaz caída", (4, 3): "no llega a entrar"}
for (i, k), s in NOTE.items():
    y = RY0 + i * RS
    en(a, a.text(TX + TW - 128, y + 29, s, 15, a.BAD, a.MONO, 400, "end"), k * 20, (k + 1) * 20, still=1 if k == 2 else 0)
# la ruta automática (tiempo 4)
yg = RY0 + 5 * RS + 8
a.add(f'<rect x="{TX + 12}" y="{yg}" width="{TW - 24}" height="44" rx="10" fill="none" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="6 5"/>')
en(a, a.text(TX + 22, yg + 29, "sin ruta automática del PPPoE: add-default-route=no", 15, a.GREY, a.MONO), 0, 60.5, still=1)
en(a, a.text(TX + 22, yg + 29, "sin ruta automática del PPPoE: add-default-route=no", 15, a.GREY, a.MONO), 80, 100)
ghost = (a.box(TX + 12, yg, TW - 24, 44, a.AMBBG, a.AMB, rx=10, sw=2)
         + a.text(TX + 22, yg + 29, "0.0.0.0/0", 16, a.INK, a.MONO, 600)
         + a.text(TX + 196, yg + 29, "pppoe-antel  automática", 16, a.AMB, a.MONO, 600)
         + a.text(TX + 440, yg + 29, "1", 16, a.INK, a.MONO, 600)
         + a.pill(TX + TW - 24, yg + 8, "activa", a.AMB, "#FFFFFF", 14, 28, "end")
         + a.text(TX + TW - 120, yg + 29, "la sesión sigue", 15, a.AMB, a.MONO, 600, "end"))
en(a, ghost, 60.5, 80)

# ---- estado de los enlaces
SX, SW = 850, 302
a.add(a.box(SX, TY, SW, 392, a.INK, rx=18))
a.add(a.text(SX + 22, TY + 34, "Qué pasa afuera", 18, "#FFFFFF", a.HEAD, 600))
def estado(y, titulo, vals):
    a.add(a.text(SX + 22, y, titulo, 15, LIGHT, a.MONO))
    for k, (s, c) in enumerate(vals):
        en(a, a.text(SX + 22, y + 28, s, 17, c, a.MONO, 600), k * 20, (k + 1) * 20, still=1 if k == 2 else 0)
estado(TY + 76, "sesión pppoe-antel", [("arriba", MINT), ("caída", "#FFB4A3"), ("arriba", MINT), ("arriba", MINT), ("arriba", MINT)])
estado(TY + 148, "internet por la fibra", [("sí", MINT), ("no", "#FFB4A3"), ("no", "#FFB4A3"), ("no", "#FFB4A3"), ("sí", MINT)])
estado(TY + 220, "el tráfico sale por", [("la fibra", MINT), ("el 4G", GOLD), ("el 4G", GOLD), ("la fibra: se pierde", "#FFB4A3"), ("la fibra", MINT)])
a.add(f'<line x1="{SX + 22}" y1="{TY + 282}" x2="{SX + SW - 22}" y2="{TY + 282}" stroke="#2C4A6B" stroke-width="2"/>')
NOTES = [(0, 20, ["check-gateway hace ping", "a 1.1.1.1 y 9.9.9.9"]),
         (20, 40, ["masquerade borra solo", "las conexiones de pppoe-antel"]),
         (40, 60, ["la interfaz sigue arriba:", "solo los pings lo ven"]),
         (60, 80, ["la automática existe", "mientras la sesión esté arriba"]),
         (80, 100, ["lo armado por el 4G sigue", "en conntrack: ether2 no bajó"])]
for i, (t0, t1, ls) in enumerate(NOTES):
    en(a, a.text(SX + 22, TY + 316, ls[0], 15, "#FFFFFF", a.SANS, 600) + a.text(SX + 22, TY + 340, ls[1], 15, "#FFFFFF", a.SANS, 600), t0, t1, still=1 if i == 2 else 0)

narr(a, [
    (0, 20, "Las dos recursivas en distancia 1 forman ECMP; el DHCP del 4G va con distancia 2.", a.TXT),
    (20, 40, "La sesión cae, la interfaz baja y las recursivas no pueden resolver su gateway.", a.BAD),
    (40, 60, "La sesión sigue pero no hay internet: check-gateway marca las recursivas.", a.BAD),
    (60, 80, "Por eso, con PPPoE principal, se apaga la ruta automática y van las recursivas.", a.AMB),
    (80, 100, "Al volver, revisá las conexiones que quedaron armadas por el 4G.", a.OK),
], y=636, still_idx=2)

escribir(a, f"{SITE}/37-t1.svg", "Dos cortes con PPPoE principal y 4G",
         "Animación en cinco tiempos sobre la tabla de rutas: las /32 a los testigos 1.1.1.1 y 9.9.9.9 por pppoe-antel, dos rutas por defecto recursivas por esos testigos en distancia 1, "
         "y la ruta por defecto del DHCP del 4G, gateway 192.168.8.1, en distancia 2. 1: todo normal; las recursivas están activas y el 4G espera. "
         "2: se cae la sesión PPPoE; la interfaz baja, las /32 quedan inactivas, las recursivas no pueden resolver su gateway y entra la ruta del 4G; masquerade borra las conexiones de pppoe-antel. "
         "3: la sesión sigue arriba pero no hay internet; las /32 siguen activas y solo los pings de check-gateway a los testigos fallan; las recursivas quedan inactivas y entra el 4G. "
         "4: si el PPPoE tuviera add-default-route=yes, su ruta automática seguiría activa porque la sesión está arriba, la ruta del 4G no llegaría a entrar y el tráfico se perdería por la fibra: sin failover. "
         "5: vuelve la fibra y las recursivas mandan otra vez; lo armado por el 4G sigue en conntrack porque ether2 nunca bajó.",
         [10, 30, 50, 70, 90], f"{PREV}/_t37")
