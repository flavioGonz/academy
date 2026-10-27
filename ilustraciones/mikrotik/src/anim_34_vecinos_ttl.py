#!/usr/bin/env python3
"""Lección 34, teoría "Anuncios periódicos": el TTL de cada vecino, la renovación, el vencimiento y el dying-gasp."""
from _anim_mt2739 import escribir, Anim, SITE, PREV, en, ventanas, fijo, paquete, nodo, marca, narr, pill_c, LIGHT, GOLD, MINT

T = 28
a = Anim(T=T, kicker="MIKROTIK · IP NEIGHBORS", title="La tabla de vecinos vive de anuncios")
a.steps([
    "Cada vecino se anuncia; LLDP trae un TTL de 121 s.",
    "Llega el anuncio siguiente: el contador vuelve a 121.",
    "Se cortó el cable del switch: a los 121 s se borra.",
    "hap-oficina reinicia con dying-gasp: TTL 0, se borra ya.",
], still=1)

nodo(a, 48, 196, 236, 82, "sw-rack", "switch · ether3", dark=False)
nodo(a, 48, 336, 236, 82, "hap-oficina", "MikroTik · ether4", dark=False)
TX, TY, TW, TH = 520, 178, 632, 258
a.add(a.box(TX, TY, TW, TH, a.INK, rx=18))
a.add(a.text(TX + 24, TY + 36, "Router · /ip/neighbor", 20, "#FFFFFF", a.HEAD, 600))
a.add(a.text(TX + 24, TY + 68, "interface", 15, LIGHT, a.MONO))
a.add(a.text(TX + 196, TY + 68, "identity", 15, LIGHT, a.MONO))
a.add(a.text(TX + 380, TY + 68, "tiempo que le queda", 15, LIGHT, a.MONO))
ROWY = [TY + 84, TY + 164]
ROWS = [("ether3,bridge", "sw-rack"), ("ether4,bridge", "hap-oficina")]
BX, BW = TX + 380, 220

# corte del cable del switch
en(a, f'<line x1="284" y1="237" x2="508" y2="237" stroke="{a.LINE}" stroke-width="3"/>', 0, 50, still=1)
en(a, f'<line x1="284" y1="237" x2="370" y2="237" stroke="{a.LINE}" stroke-width="3"/>'
      + f'<path d="M378 225 L392 249 M392 225 L378 249" stroke="{a.BAD}" stroke-width="3"/>'
      + a.text(385, 212, "cable cortado", 15, a.BAD, a.MONO, 600, "middle"), 50, 100)
a.add(f'<line x1="284" y1="377" x2="508" y2="377" stroke="{a.LINE}" stroke-width="3"/>')

def fila(i, wins, bar_pts, labels, still=0):
    y = ROWY[i]
    row = (a.box(TX + 14, y, TW - 28, 62, a.NAVY2, rx=12)
           + a.text(TX + 28, y + 38, ROWS[i][0], 16, "#FFFFFF", a.MONO, 600)
           + a.text(TX + 196, y + 38, ROWS[i][1], 16, "#FFFFFF", a.MONO, 600)
           + f'<rect x="{BX}" y="{y + 16}" width="{BW}" height="12" rx="6" fill="#2C4A6B"/>')
    ventanas(a, row, wins, still=still)
    k = a.keyframes(bar_pts, "transform", "scaleX({})")
    a.add(a.group(f'<rect x="{BX}" y="{y + 16}" width="{BW}" height="12" rx="6" fill="{a.CYAN}"/>', k, vis(wins), still=0, origin=f"{BX}px {y + 22}px"))
    for t0, t1, s, c, st in labels:
        en(a, a.text(BX, y + 50, s, 15, c, a.MONO, 600), t0, t1, still=st)

from _anim_mt2739 import vis as _vis
def vis(w):
    return _vis(a, w)

# sw-rack: anuncio a los 3 y a los 29; sin anuncios desde el 50; se borra a los 71
fila(0, [(3, 72)], [(0, 1), (3, 1), (26, .76), (29, 1), (50, .82), (70, 0), (100, 0)],
     [(4, 26, "121 s · se renueva", MINT, 0), (29, 50, "121 s otra vez", MINT, 1),
      (51, 69, "sin anuncios, baja…", GOLD, 0), (69, 72, "0 s: se borra", "#FFB4A3", 0)], still=1)
# hap-oficina: anuncios a los 6, 32 y 58; dying-gasp a los 81
fila(1, [(6, 82)], [(0, 1), (6, 1), (30, .76), (32, 1), (56, .78), (58, 1), (80, .8), (81, 0), (100, 0)],
     [(7, 30, "121 s · se renueva", MINT, 0), (32, 56, "121 s otra vez", MINT, 1), (58, 80, "121 s otra vez", MINT, 0),
      (81, 82, "TTL 0: se borra", "#FFB4A3", 0)], still=1)
en(a, a.text(TX + TW / 2, ROWY[0] + 40, "sw-rack vencido: borrado", 16, "#FFB4A3", a.MONO, 600, "middle"), 72, 100)
en(a, a.text(TX + TW / 2, ROWY[1] + 40, "hap-oficina: borrado al instante", 16, "#FFB4A3", a.MONO, 600, "middle"), 82, 100)
fijo(a, f'<rect x="{BX}" y="{ROWY[0] + 16}" width="{BW}" height="12" rx="6" fill="{a.CYAN}"/>'
        + f'<rect x="{BX}" y="{ROWY[1] + 16}" width="{BW * .8}" height="12" rx="6" fill="{a.CYAN}"/>')

AN = "LLDP · TTL 121"
paquete(a, AN, [(0.5, 396, 237), (3, 470, 237)], 0.5, 4, bg=a.BLUE, size=14)
paquete(a, AN, [(26.5, 396, 237), (29, 470, 237)], 26.5, 30, bg=a.BLUE, size=14)
for t in (3.5, 29.5, 55.5):
    paquete(a, AN, [(t, 396, 377), (t + 2.5, 470, 377)], t, t + 3.5, bg=a.BLUE, size=14)
paquete(a, "dying-gasp · TTL 0", [(76, 396, 377), (80.5, 470, 377)], 76, 81.5, bg=a.BAD, size=14)
en(a, a.pill(166, 428, "reinicio ordenado", a.BAD, a.BADBG, 15, 30, "middle"), 76, 100)

# fórmula
FY = 462
a.add(a.box(48, FY, 1104, 128, a.WHITE, a.LINE, rx=16))
a.add(a.text(72, FY + 36, "TTL del anuncio en LLDP y CDP", 18, a.INK, a.HEAD, 600))
a.add(a.text(72, FY + 74, "discover-interval × 4 + 1  =  30 s × 4 + 1  =  121 s", 19, a.BLUE, a.MONO, 600))
a.add(a.text(72, FY + 106, "Si en ese tiempo no llega otro anuncio, el vecino se borra de la tabla.", 16, a.TXT, a.SANS))

narr(a, [
    (0, 25, "El anuncio sale por cada interfaz de la lista de descubrimiento.", a.TXT),
    (25, 50, "Mientras los anuncios lleguen cada 30 s, el vecino no vence nunca.", a.OK),
    (50, 75, "Sin anuncios, el vecino sigue en la tabla hasta que vence su TTL.", a.AMB),
    (75, 100, "Con dying-gasp el vecino no espera los 121 s: lo borra en el momento.", a.BAD),
], y=636, still_idx=1)

escribir(a, f"{SITE}/34-t1.svg", "Vecinos LLDP y su TTL",
         "Animación en cuatro tiempos sobre la tabla /ip/neighbor del router, con dos vecinos: sw-rack en ether3 y hap-oficina en ether4. "
         "1: cada vecino manda un anuncio LLDP con TTL de 121 segundos y aparece en la tabla con su contador lleno. "
         "2: a los 30 segundos llega el anuncio siguiente y el contador vuelve a 121. "
         "3: se corta el cable del switch; no llegan más anuncios, el contador baja y a los 121 segundos sw-rack se borra. "
         "4: hap-oficina hace un reinicio ordenado y manda un anuncio dying-gasp con TTL 0; el router lo borra al instante. "
         "Abajo: el TTL es discover-interval por 4 más 1, 30 por 4 más 1, 121 segundos.",
         [10, 35, 62, 71, 90], f"{PREV}/_t34")
