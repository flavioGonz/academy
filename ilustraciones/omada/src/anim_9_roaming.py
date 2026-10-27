#!/usr/bin/env python3
"""Teoría lección 9 (Roaming y mesh): el cliente decide cuándo cambiar; 802.11k, v y r lo ayudan;
con EAP a máxima potencia la señal nunca baja del umbral y el cliente no cambia.
Salida: site2/ilustraciones/omada/9-t1.svg"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _anim_omada import *  # noqa

a = nueva(24, "ROAMING", "El cliente decide cuándo cambiar de EAP")
F = a.steps([
    "El cliente camina y mide la señal de su EAP. Todavía está arriba de su umbral.",
    "Con 802.11k sabe qué vecinos hay; con 802.11v el EAP le sugiere otro.",
    "La señal baja del umbral: el cliente salta. Con 802.11r, las claves ya están listas.",
    "EAP a máxima potencia: la señal nunca baja del umbral y el cliente no cambia.",
], still=2)
(a0, a1), (b0, b1), (c0, c1), (d0, d1) = F

E1, E2, EY, R = 220, 620, 330, 150
PY = 466  # carril del cliente
a.add(a.box(48, 174, 812, 330, a.WHITE, a.LINE, rx=16))
a.add(a.text(66, 200, "planta", 15, a.GREY, a.MONO))
a.add(f'<clipPath id="cl9"><rect x="49" y="175" width="810" height="328" rx="15"/></clipPath>')
# celdas
cel1 = f'<circle cx="{E1}" cy="{EY}" r="{R}" fill="{a.BLUE}" fill-opacity=".08" stroke="{a.BLUE}" stroke-width="2"/>'
k = a.keyframes([(0, 1), (d0 + 1, 1), (d0 + 6, 1.8), (99, 1.8), (100, 1)], "transform", "scale({})")
a.add(f'<g clip-path="url(#cl9)">' + a.group(cel1, k, a.keyframes([(0, 1), (100, 1)]), still=1, origin=f"{E1}px {EY}px")
      + f'<circle cx="{E2}" cy="{EY}" r="{R}" fill="{a.OK}" fill-opacity=".08" stroke="{a.OK}" stroke-width="2"/></g>')
a.add(eap(a, E1, EY, 26, a.BLUE) + eap(a, E2, EY, 26, a.OK))
a.add(a.text(E1, EY + 50, "EAP 1", 17, a.INK, a.HEAD, 600, "middle") + a.text(E2, EY + 50, "EAP 2", 17, a.INK, a.HEAD, 600, "middle"))
a.add(a.text(E1, EY - 46, "Roaming-Lab", 15, a.GREY, a.MONO, 400, "middle") + a.text(E2, EY - 46, "Roaming-Lab", 15, a.GREY, a.MONO, 400, "middle"))
fase(a, chip(a, E1, EY - 92, "máxima potencia", a.BAD, a.BADBG, anchor="middle", stroke=a.BAD), F, 3)
a.add(linea(a, 120, PY, 760, PY, a.LINE, 2, "4 8"))

# cliente: celular con la etiqueta del EAP al que está asociado
def cliente(ap_label, color):
    return (f'<rect x="-11" y="-19" width="22" height="38" rx="5" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="2.5"/>'
            f'<circle cx="0" cy="12" r="2.5" fill="{a.INK}"/>'
            + chip(a, 0, -60, ap_label, color, a.WHITE, anchor="middle", stroke=color))


# tramos de movimiento (posición x por tiempo)
X0, XM, XJ, XE = 160, 400, 470, 640
mv = a.move([(0, X0, PY), (a0 + 2, X0, PY), (a1, XM, PY), (b1, XJ - 30, PY), (c0 + 6, XJ, PY), (c1 - 4, XE, PY), (c1, XE, PY),
             (d0 + 1, X0, PY), (d0 + 7, X0, PY), (d1 - 4, XE, PY), (100, XE, PY)])
asoc1 = a.group(cliente("EAP 1", a.BLUE), a.keyframes([(0, 1), (c0 + 6, 1), (c0 + 6.5, 0), (d0 + 1, 0), (d0 + 1.5, 1), (100, 1)]), still=0)
asoc2 = a.group(cliente("EAP 2", a.OK), a.keyframes([(0, 0), (c0 + 6, 0), (c0 + 6.5, 1), (d0 + 1, 1), (d0 + 1.5, 0), (100, 0)]), still=1)
a.add(a.group(asoc1 + asoc2, mv, a.keyframes([(0, 1), (100, 1)]), still=0))
# cuadro fijo: el cliente ya asociado al EAP 2
solo_fijo(a, f'<g transform="translate({XE} {PY})">{cliente("EAP 2", a.OK)}</g>')

# 802.11k / v / r
KX, KY, KW = 884, 186, 268
a.add(a.box(KX, KY - 12, KW, 330, a.WHITE, a.LINE))
a.add(a.text(KX + 20, KY + 22, "Lo que ayuda", 18, a.INK, a.HEAD, 600))
ITEMS = [("802.11k", "lista de vecinos", b0), ("802.11v", "sugiere otro EAP", b0 + 8), ("802.11r", "claves listas antes", c0 + 2)]
for i, (std, txt, t) in enumerate(ITEMS):
    y = KY + 44 + i * 76
    a.add(a.box(KX + 16, y, KW - 32, 62, a.SLATE, None, rx=12))
    a.add(a.text(KX + 32, y + 26, std, 16, a.INK, a.MONO, 600) + a.text(KX + 32, y + 50, txt, 16, a.TXT, a.SANS))
    en(a, a.box(KX + 16, y, KW - 32, 62, "none", a.OK, rx=12, sw=3) + ok(a, KX + KW - 38, y + 22, 12), t, c1, still=1)
fase(a, a.text(KX + 20, KY + 294, "Ninguna obliga al cliente.", 15, a.GREY, a.SANS, 600), F, 1, 3, still=1)

# medidor de señal
MX, MY, MW = 48, 556, 1104
a.add(a.text(MX, MY + 2, "Señal del EAP asociado", 16, a.INK, a.SANS, 600))
BX0, BW0 = 270, 830
a.add(a.box(BX0, MY - 18, BW0, 26, a.SLATE, None, rx=8))
lvl = a.keyframes([(0, 0.92), (a0 + 2, 0.92), (a1, 0.6), (b1, 0.5), (c0 + 5.5, 0.36), (c0 + 7, 0.9), (c1 - 4, 0.92), (c1, 0.92),
                   (d0 + 1, 0.95), (d0 + 7, 0.95), (d1 - 4, 0.62), (100, 0.62)], "transform", "scaleX({})")
col = a.keyframes([(0, a.BLUE), (c0 + 5, a.BLUE), (c0 + 5.5, a.AMB), (c0 + 6.5, a.AMB), (c0 + 7, a.OK), (d0 + 1, a.OK), (d0 + 1.5, a.BLUE), (100, a.BLUE)], "fill")
a.n += 1
cname = f"c{a.n}"
a.css.append(f".{cname}{{animation:{col} {a.T}s linear infinite}}")
bar = f'<rect class="{cname}" x="{BX0}" y="{MY - 18}" width="{BW0}" height="26" rx="8" fill="{a.OK}"/>'
a.add(a.group(bar, lvl, a.keyframes([(0, 1), (100, 1)]), still=1, origin=f"{BX0}px {MY}px"))
TH = BX0 + BW0 * 0.42
a.add(linea(a, TH, MY - 30, TH, MY + 18, a.AMB, 3))
a.add(a.text(TH + 8, MY + 34, "umbral propio del cliente", 15, a.AMB, a.MONO, 600))

pie(a, F, [
    "El roaming lo decide el cliente, no el EAP.",
    "k y v le dan información; el cliente puede aceptar o no.",
    "Si algún equipo pierde internet con 802.11r, dejalo apagado en ese SSID.",
    "No es un problema de roaming: es de potencia.",
], y=640, still=2, colores=[a.INK, a.INK, a.AMB, a.BAD])

salida(a, 9, 1, "El cliente decide cuándo cambiar de EAP",
       "Animación en cuatro tiempos con dos EAP del mismo SSID, Roaming-Lab, y un celular que camina del EAP 1 al EAP 2, con una barra "
       "de señal del EAP asociado y una marca del umbral propio del cliente. 1: el cliente camina y la señal baja, pero sigue arriba del "
       "umbral. 2: con 802.11k sabe qué vecinos hay y con 802.11v el EAP le sugiere otro; ninguna obliga al cliente. 3: la señal baja del "
       "umbral y el cliente salta al EAP 2; con 802.11r las claves ya estaban listas. 4: con el EAP 1 a máxima potencia la celda es "
       "enorme, la señal nunca baja del umbral y el cliente sigue pegado al EAP 1 aunque esté al lado del EAP 2: es un problema de potencia.",
       [14, 40, 68, 94])
