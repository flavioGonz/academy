#!/usr/bin/env python3
"""Lección 35, teoría "Estados" y "Pruebas": la sonda icmp, el umbral de pérdida y los scripts que corren una vez por cambio."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

a = Anim(T=30, kicker="MIKROTIK · NETWATCH", title="Sonda icmp: el estado cambia, el script corre una vez")
a.steps([
    "Arranca en unknown. Prueba 1: vuelven los 10 paquetes.",
    "Prueba 2: se pierden 3 de 10. 30% no llega al umbral.",
    "Prueba 3: se pierden los 10. Pasa a down: down-script.",
    "Prueba 4: falla otra vez. Sigue down, sin repetir el script.",
    "Prueba 5: vuelve. Pasa a up: up-script.",
], still=2)

nodo(a, 48, 180, 236, 96, "Router", "/tool/netwatch", sub2="type=icmp")
nodo(a, 916, 180, 236, 96, "Cámara", "192.168.88.60", dark=False)

# ---- la prueba: 10 paquetes
PX, PW = 312, 576
a.add(a.box(PX, 176, PW, 104, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 22, 204, "una prueba: 10 paquetes, uno cada 50 ms", 16, a.INK, a.SANS, 600))
TESTS = [set(), {2, 5, 8}, set(range(10)), set(range(10)), set()]
SX = [PX + 40 + i * 55 for i in range(10)]
SY = 246
for x in SX:
    a.add(f'<circle cx="{x}" cy="{SY}" r="16" fill="{a.SLATE}" stroke="{a.LINE}" stroke-width="2"/>')
for k, lost in enumerate(TESTS):
    t0 = k * 20
    for i, x in enumerate(SX):
        ok = i not in lost
        c, bg = (a.OK, a.OKBG) if ok else (a.BAD, a.BADBG)
        en(a, marca(a, x, SY, ok=ok, r=16), t0 + 1 + i * 0.6, t0 + 19.5, still=1 if k == 2 else 0)

# ---- pérdida contra el umbral
MX, MY, MW = 48, 304, 560
a.add(a.box(MX, MY, MW, 132, a.WHITE, a.LINE, rx=16))
a.add(a.text(MX + 22, MY + 32, "pérdida de la prueba", 18, a.INK, a.HEAD, 600))
BX, BY, BW = MX + 22, MY + 56, MW - 44
a.add(a.box(BX, BY, BW, 22, a.SLATE, rx=11))
thr = BX + BW * 0.85
a.add(f'<line x1="{thr}" y1="{BY - 8}" x2="{thr}" y2="{BY + 30}" stroke="{a.AMB}" stroke-width="3"/>')
a.add(a.text(thr, BY + 52, "thr-loss-percent 85%", 15, a.AMB, a.MONO, 600, "middle"))
for k, lost in enumerate(TESTS):
    t0 = k * 20
    pct = len(lost) * 10
    if pct:
        c = a.BAD if pct > 85 else a.CYAN
        en(a, a.box(BX, BY, BW * pct / 100, 22, c, rx=11), t0 + 7, t0 + 19.5, still=1 if k == 2 else 0)
    verdict = ("falla" if pct > 85 else "pasa")
    col = a.BAD if pct > 85 else a.OK
    en(a, a.text(BX, BY + 52, f"{pct}% · la prueba {verdict}", 16, col, a.MONO, 600), t0 + 7.5, t0 + 19.5, still=1 if k == 2 else 0)

# ---- estados
EX, EY, EW = 640, 304, 512
a.add(a.box(EX, EY, EW, 132, a.INK, rx=16))
a.add(a.text(EX + 22, EY + 32, "estado de la sonda", 18, "#FFFFFF", a.HEAD, 600))
ST = [("unknown", GOLD), ("up", MINT), ("down", "#FFB4A3")]
SXs = [EX + 22, EX + 188, EX + 330]
for (n, c), x in zip(ST, SXs):
    a.add(a.box(x, EY + 56, 140 if n == "unknown" else 120, 40, a.NAVY2, rx=20) + a.text(x + (70 if n == "unknown" else 60), EY + 82, n, 17, LIGHT, a.MONO, 600, "middle"))
def on(i, wins, still=0):
    n, c = ST[i]; x = SXs[i]; w = 140 if n == "unknown" else 120
    ventanas(a, a.box(x, EY + 56, w, 40, c, rx=20) + a.text(x + w / 2, EY + 82, n, 17, a.INK, a.MONO, 600, "middle"), wins, still)
on(0, [(0, 8.5)])
on(1, [(8.5, 48.5), (88.5, 100)])
on(2, [(48.5, 88.5)], still=1)
en(a, a.text(EX + 22, EY + 120, "corre el down-script, una sola vez", 16, "#FFB4A3", a.SANS, 600), 49, 68, still=1)
en(a, a.text(EX + 22, EY + 120, "sin cambio de estado: no corre nada", 16, LIGHT, a.SANS, 600), 69, 88)
en(a, a.text(EX + 22, EY + 120, "corre el up-script", 16, MINT, a.SANS, 600), 89, 100)
en(a, a.text(EX + 22, EY + 120, "sigue up: no corre nada", 16, LIGHT, a.SANS, 600), 29, 48)
en(a, a.text(EX + 22, EY + 120, "con ignore-initial-up, sin aviso", 16, LIGHT, a.SANS, 600), 9, 20)

# ---- registro
LY = 456
a.add(a.box(48, LY, 1104, 146, a.WHITE, a.LINE, rx=16))
LOG = [(8.5, "prueba 1 · 0% → unknown a up", a.TXT), (28.5, "prueba 2 · 30% → sigue up", a.TXT),
       (48.5, "prueba 3 · 100% → down · down-script", a.BAD), (68.5, "prueba 4 · 100% → sigue down", a.TXT),
       (88.5, "prueba 5 · 0% → up · up-script", a.OK)]
for i, (t, s, c) in enumerate(LOG):
    x = 72 + (i // 3) * 540
    y = LY + 38 + (i % 3) * 38
    en(a, a.text(x, y, s, 16, c, a.MONO, 600 if c != a.TXT else 400), t, 100, still=1 if i <= 2 else 0)
a.add(a.text(1128, LY + 114, "una prueba cada interval: 10 s", 15, a.GREY, a.MONO, 400, "end"))

narr(a, [
    (0, 20, "Cada interval la sonda manda packet-count paquetes y calcula la pérdida.", a.TXT),
    (20, 40, "Una pérdida suelta no alcanza: así se evitan las falsas alarmas.", a.OK),
    (40, 60, "100% supera el umbral: la prueba falla y el estado pasa a down.", a.BAD),
    (60, 80, "Los scripts corren al cambiar de estado, no en cada prueba.", a.TXT),
    (80, 100, "Al pasar de down a up corre el up-script: el aviso de que volvió.", a.OK),
], y=640, still_idx=2)

escribir(a, f"{SITE}/35-t1.svg", "Netwatch: sonda icmp y estados",
         "Animación en cinco tiempos de una sonda Netwatch de tipo icmp hacia una cámara, 192.168.88.60. Cada prueba manda 10 paquetes, uno cada 50 milisegundos, "
         "y falla si la pérdida supera thr-loss-percent, 85%. 1: la sonda arranca en unknown; vuelven los 10 paquetes y pasa a up, sin aviso si está ignore-initial-up. "
         "2: se pierden 3 de 10, 30%, no llega al umbral y sigue up sin correr nada. 3: se pierden los 10, 100%, la prueba falla, pasa a down y corre el down-script una vez. "
         "4: la prueba siguiente falla otra vez; sigue down y el script no se repite. 5: vuelven los 10 paquetes, pasa a up y corre el up-script.",
         [10, 30, 55, 75, 95], f"{PREV}/_t35")
