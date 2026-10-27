#!/usr/bin/env python3
"""Lección 29, teoría: traceroute con TTL creciente (t1) y MTU del camino con do-not-fragment (t2)."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT

# ======================= t1: traceroute
a = Anim(T=24, kicker="MIKROTIK · DIAGNÓSTICO", title="Traceroute: el TTL sube de a uno")
a.steps([
    "Sonda con TTL 1: contesta el primer router.",
    "TTL 2: pasa el primero, contesta el segundo.",
    "TTL 3: contesta el tercero.",
    "TTL 4: llega al destino y contesta él.",
], still=3)

NODES = [("MikroTik", "origen"), ("Salto 1", "203.0.113.1"), ("Salto 2", "203.0.113.6"), ("Salto 3", "198.51.100.1"), ("Destino", "1.1.1.1")]
XS = [48, 278, 508, 738, 968]
W, NY, NH = 184, 182, 80
CX = [x + W / 2 for x in XS]
for i, (n, s) in enumerate(NODES):
    nodo(a, XS[i], NY, W, NH, n, s, dark=(i == 0))
UP, DN = 314, 356
a.add(f'<line x1="{CX[0]}" y1="{NY + NH}" x2="{CX[0]}" y2="{DN}" stroke="{a.LINE}" stroke-width="3"/>')
for c in CX[1:]:
    a.add(f'<line x1="{c}" y1="{NY + NH}" x2="{c}" y2="{DN}" stroke="{a.LINE}" stroke-width="3"/>')
a.add(f'<line x1="{CX[0]}" y1="{UP}" x2="{CX[-1]}" y2="{UP}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
a.add(f'<line x1="{CX[0]}" y1="{DN}" x2="{CX[-1]}" y2="{DN}" stroke="{a.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')

# tabla de resultado
TY = 404
a.add(a.box(48, TY, 1104, 196, a.WHITE, a.LINE, rx=16))
a.add(a.text(70, TY + 30, "#", 15, a.GREY, a.MONO))
a.add(a.text(120, TY + 30, "address", 15, a.GREY, a.MONO))
a.add(a.text(420, TY + 30, "quién contesta", 15, a.GREY, a.MONO))
RES = ["tiempo excedido: TTL llegó a 0 en el salto 1", "tiempo excedido: TTL llegó a 0 en el salto 2",
       "tiempo excedido: TTL llegó a 0 en el salto 3", "el destino contesta: fin del recorrido"]

for i in range(4):
    t0 = i * 25
    n = i + 1                       # TTL de la sonda = salto que contesta
    seg = 3.2 if n < 4 else 2.6
    pts, t = [], t0 + 1
    for j in range(n):
        lab = f"TTL {n - j}"
        paquete(a, lab, [(t, CX[j], UP), (t + seg, CX[j + 1], UP)], t, t + seg + (0.4 if j == n - 1 else 0), bg=a.CYAN)
        t += seg
    arrive = t
    if n < 4:
        en(a, a.pill(CX[n], 272, "1 − 1 = 0: descarta", a.BAD, a.BADBG, 15, 28, "middle"), arrive, arrive + 5)
        back = "tiempo excedido"
        col = a.AMB
    else:
        en(a, a.pill(CX[n], 272, "es para mí: contesta", a.OK, a.OKBG, 15, 28, "middle"), arrive, arrive + 5)
        back = "respuesta"
        col = a.OK
    rb = arrive + 1.5
    paquete(a, back, [(rb, CX[n], DN), (rb + 6, CX[0], DN)], rb, rb + 6.5, bg=col)
    # fila de la tabla
    y = TY + 46 + i * 36
    row = (a.box(60, y, 1080, 30, a.SLATE if n < 4 else a.OKBG, rx=8)
           + a.text(72, y + 21, str(n), 16, a.INK, a.MONO, 600)
           + a.text(120, y + 21, NODES[n][1], 16, a.INK, a.MONO, 600)
           + a.text(420, y + 21, RES[i], 16, a.TXT if n < 4 else a.OK, a.SANS, 600 if n == 4 else 400))
    en(a, row, rb + 6.5, 100, still=1)

narr(a, [
    (0, 25, "Cada router resta uno al TTL; si llega a cero, descarta el paquete y avisa con ICMP.", a.TXT),
    (25, 50, "El aviso trae la dirección del router que lo descartó: así aparece cada salto.", a.TXT),
    (50, 75, "La sonda siguiente sale con un TTL más: hasta 30 saltos o hasta el destino.", a.TXT),
    (75, 100, "Pérdida real: empieza en un salto y sigue en todos los que vienen después.", a.INK),
], y=636, still_idx=3)

escribir(a, f"{SITE}/29-t1.svg", "Traceroute y el TTL",
        "Animación en cuatro tiempos. El MikroTik manda sondas hacia 1.1.1.1 con TTL creciente. 1: la sonda con TTL 1 llega al primer router, 203.0.113.1, "
        "que le resta uno, llega a cero, la descarta y contesta tiempo excedido. 2: con TTL 2 pasa el primero y contesta el segundo, 203.0.113.6. "
        "3: con TTL 3 contesta el tercero, 198.51.100.1. 4: con TTL 4 la sonda llega al destino, que contesta. Abajo se arma la tabla de saltos, uno por sonda.",
        [6, 20, 37, 62, 86, 97], f"{PREV}/_t29-1")

# ======================= t2: MTU con do-not-fragment
b = Anim(T=22, kicker="MIKROTIK · DIAGNÓSTICO", title="La MTU del camino: do-not-fragment y size")
b.steps([
    "ping con size=1500 y do-not-fragment: sale entero.",
    "El enlace PPPoE pasa hasta 1492: el router no lo parte, avisa.",
    "Bajás size a 1492: pasa entero y el destino contesta.",
    "MTU del camino: 1492. En RouterOS, size incluye los encabezados.",
], still=3)

NY, NH = 182, 86
nodo(b, 48, NY, 220, NH, "MikroTik", "origen", dark=True)
nodo(b, 490, NY, 220, NH, "Router del camino", "", dark=False, size=19)
nodo(b, 932, NY, 220, NH, "Destino", "1.1.1.1", dark=False)
b.add(b.text(510, NY + 60, "PPPoE hacia adelante", 15, b.GREY, b.MONO))
LY = NY + NH / 2
b.add(f'<rect x="268" y="{LY - 14}" width="222" height="28" fill="{b.SLATE}" stroke="{b.LINE}" stroke-width="2"/>')
b.add(f'<rect x="710" y="{LY - 9}" width="222" height="18" fill="{b.AMBBG}" stroke="{b.AMB}" stroke-width="2"/>')
b.add(b.text(379, LY - 24, "Ethernet · MTU 1500", 15, b.TXT, b.MONO, 600, "middle"))
b.add(b.text(821, LY - 24, "PPPoE · MTU 1492", 15, b.AMB, b.MONO, 600, "middle"))

UP, DN = 326, 366
C0, C1, C2 = 158, 600, 1042
for c in (C0, C1, C2):
    b.add(f'<line x1="{c}" y1="{NY + NH}" x2="{c}" y2="{DN}" stroke="{b.LINE}" stroke-width="3"/>')
b.add(f'<line x1="{C0}" y1="{UP}" x2="{C2}" y2="{UP}" stroke="{b.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
b.add(f'<line x1="{C0}" y1="{DN}" x2="{C2}" y2="{DN}" stroke="{b.LINE}" stroke-width="2" stroke-dasharray="4 6"/>')

paquete(b, "1500 · DF", [(1, C0, UP), (14, C1, UP), (25, C1, UP)], 1, 30, bg=b.CYAN)
en(b, b.pill(C1 + 128, UP - 15, "no entra en 1492", b.BAD, b.BADBG, 15, 30), 26, 50)
paquete(b, "fragmentation needed", [(31, C1, DN), (44, C0, DN), (49, C0, DN)], 31, 49, bg=b.AMB)
paquete(b, "1492 · DF", [(51, C0, UP), (57, C1, UP), (63, C2, UP), (65, C2, UP)], 51, 65.5, bg=b.CYAN)
paquete(b, "respuesta", [(66, C2, DN), (74, C0, DN)], 66, 74.5, bg=b.OK)
en(b, marca(b, C0 + 90, DN, ok=True), 73, 100, still=1)

# terminal
TY = 404
b.add(b.box(48, TY, 600, 196, b.INK, rx=16))
b.add(b.text(70, TY + 30, "TERMINAL", 15, LIGHT, b.MONO, 400, extra='letter-spacing="2"'))
lines = [
    (1, "/ping 1.1.1.1 do-not-fragment size=1500", "#FFFFFF", 400),
    (44, "# contesta el router: fragmentation needed", "#FFB4A3", 400),
    (51, "/ping 1.1.1.1 do-not-fragment size=1492", "#FFFFFF", 400),
    (74, "# contesta 1.1.1.1: la MTU del camino es 1492", "#5BE0A5", 600),
]
for i, (t, s, c, w) in enumerate(lines):
    en(b, b.text(70, TY + 72 + i * 34, s, 16, c, b.MONO, w), t, 100, still=1)

# anatomía del paquete (tiempo 4)
AX, AY = 680, TY
b.add(b.box(AX, AY, 472, 196, b.WHITE, b.LINE, rx=16))
b.add(b.text(AX + 22, AY + 32, "Qué cuenta size", 18, b.INK, b.HEAD, 600))
segs = [("IP", "20", 74, b.BLUE), ("ICMP", "8", 74, b.CYAN), ("datos", "1464", 280, b.GREY)]
x = AX + 22
bar = ""
for n, v, w, c in segs:
    bar += b.box(x, AY + 62, w - 4, 52, c, rx=8) + b.text(x + (w - 4) / 2, AY + 86, n, 15, "#FFFFFF", b.MONO, 600, "middle") + b.text(x + (w - 4) / 2, AY + 106, v, 15, "#FFFFFF", b.MONO, 600, "middle")
    x += w
bar += (b.text(AX + 22, AY + 148, "size=1492 = 20 + 8 + 1464 de datos", 16, b.INK, b.MONO, 600)
        + b.text(AX + 22, AY + 176, "Windows cuenta solo los datos: 1464", 16, b.TXT, b.SANS))
b.add(bar)

narr(b, [
    (0, 25, "do-not-fragment pide que nadie parta el paquete en el camino.", b.TXT),
    (25, 50, "Un router que no puede pasarlo entero contesta en vez de partirlo.", b.AMB),
    (50, 75, "Bajando size hasta que conteste encontrás el paquete más grande que pasa.", b.TXT),
    (75, 100, "Ethernet 1500, PPPoE 1492: el enlace más chico del camino manda.", b.INK),
], y=636, still_idx=3)

escribir(b, f"{SITE}/29-t2.svg", "MTU del camino con do-not-fragment",
        "Animación en cuatro tiempos. Camino: MikroTik, enlace Ethernet con MTU 1500, un router del camino y un enlace PPPoE con MTU 1492 hasta el destino 1.1.1.1. "
        "1: ping con size=1500 y do-not-fragment sale entero. 2: el router del camino no puede pasarlo por el PPPoE de 1492 y, en vez de partirlo, contesta fragmentation needed. "
        "3: con size=1492 el paquete pasa entero y el destino contesta. 4: la MTU del camino es 1492; en RouterOS size incluye el encabezado IP de 20 bytes y el ICMP de 8, "
        "así que quedan 1464 de datos, que es lo que cuenta Windows.",
        [10, 37, 62, 90], f"{PREV}/_t29-2")
