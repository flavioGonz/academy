#!/usr/bin/env python3
"""Lección 10 · Resumen, "Cómo se ve en la red": la receptora de alarmas en HA. Se cae la fuente de pve1; el CRM ve
que el nodo no responde, el servicio pasa a fence hasta que el nodo se da por cercado (plazo del watchdog), después a
recovery, y arranca en pve2 sobre el almacenamiento compartido.
Fuentes: guía de administración (estados de servicio started, fence, recovery; watchdog de 60 s; recuperación en
nodos con quórum; salida de ha-manager status), tarjeta de la lección (ejemplo del centro de monitoreo)."""
from _anim_pmx_red import *

a = new(24, "HA con fencing", "Se cae un nodo: la receptora vuelve sola en pve2")
a.steps([
    "La receptora de alarmas, vm:100, corre en pve1 bajo HA.",
    "Falla la fuente de pve1: el servicio pasa a fence y la HA espera.",
    "Vencido el plazo, pve1 se da por cercado: recovery elige pve2.",
    "La VM arranca en pve2 sobre el mismo disco compartido: started.",
], still=2)

NX = [48, 318, 588]
NY, NW, NH = 182, 250, 150
names = ["pve1", "pve2", "pve3"]
for i, x in enumerate(NX):
    if i == 0:
        at(a, dev(a, x, NY, NW, NH, "pve1", "lrm active", icon="server", dark=True, tsize=19), 0, 26)
        at(a, a.box(x, NY, NW, NH, a.SLATE, a.BAD, rx=14, sw=2.5, extra='stroke-dasharray="9 7"') + glyph(a, "bolt", x + 18, NY + 18, a.BAD)
           + a.text(x + 62, NY + 34, "pve1 · sin energía", 19, a.BAD, a.SANS, 600) + a.text(x + 62, NY + 58, "falla de fuente", 15, a.BAD, a.MONO), 26, 100, still=1)
    else:
        a.add(dev(a, x, NY, NW, NH, names[i], "lrm active" if i == 1 else "lrm active · master", icon="server", dark=True, tsize=19))
# VM receptora
VW, VH = 210, 56
at(a, a.box(NX[0] + 20, NY + 78, VW, VH, a.OK, rx=10) + a.text(NX[0] + 20 + VW / 2, NY + 113, "vm:100 receptora", 15, a.WHITE, a.MONO, 700, "middle"), 0, 26)
at(a, a.box(NX[0] + 20, NY + 78, VW, VH, "none", a.BAD, rx=10, sw=2, extra='stroke-dasharray="6 5"') + a.text(NX[0] + 20 + VW / 2, NY + 113, "vm:100 caída", 15, a.BAD, a.MONO, 700, "middle"), 26, 100, still=1)
at(a, a.box(NX[1] + 20, NY + 78, VW, VH, a.AMBBG, a.AMB, rx=10, sw=2) + a.text(NX[1] + 20 + VW / 2, NY + 113, "vm:100 arrancando", 15, a.AMB, a.MONO, 700, "middle"), 70, 80)
at(a, a.box(NX[1] + 20, NY + 78, VW, VH, a.OK, rx=10) + a.text(NX[1] + 20 + VW / 2, NY + 113, "vm:100 receptora", 15, a.WHITE, a.MONO, 700, "middle"), 80, 100)
# storage compartido
SY = 380
a.add(a.box(48, SY, 790, 60, a.WHITE, a.LINE, rx=12) + glyph(a, "server", 66, SY + 14) + a.text(110, SY + 37, "almacenamiento compartido · disco de vm:100", 16, a.INK, a.SANS, 600))
for i, x in enumerate(NX):
    a.add(line(x + NW / 2, NY + NH, x + NW / 2, SY, a.LINE, 3))
at(a, line(NX[0] + NW / 2, NY + NH, NX[0] + NW / 2, SY, a.BLUE, 4), 0, 26)
at(a, line(NX[1] + NW / 2, NY + NH, NX[1] + NW / 2, SY, a.BLUE, 4), 72, 100)
for t in (3, 11, 19):
    a.add(travel(a, a.box(-10, -8, 20, 16, a.CYAN, rx=4), [(NX[0] + NW / 2, NY + NH + 6), (NX[0] + NW / 2, SY - 6)], t, t + 3, hold=0.2, fade=0.2))
for t in (82, 90):
    a.add(travel(a, a.box(-10, -8, 20, 16, a.CYAN, rx=4), [(NX[1] + NW / 2, NY + NH + 6), (NX[1] + NW / 2, SY - 6)], t, t + 3, hold=0.2, fade=0.2))
# reloj del plazo (paso 2)
CX, CY = 168, 520
at(a, a.box(48, 470, 790, 100, a.WHITE, a.LINE, rx=12), 26, 75, still=1)
at(a, a.text(66, 500, "El CRM espera a que pve1 quede cercado antes de mover nada", 16, a.INK, a.SANS, 600), 26, 75, still=1)
a.add(during(a, a.box(66, 520, 754, 16, "#E6EDF4", rx=8), 26, 75, still=1))
k = a.keyframes([(0, 0.01), (28, 0.01), (56, 1), (100, 1)], "transform", "scaleX({})")
a.add(during(a, a.group(a.box(66, 520, 754, 16, a.AMB, rx=8), k, still=None, origin="66px 528px"), 27, 75))
a.add(still_only(a, a.box(66, 520, 754, 16, a.AMB, rx=8)))
at(a, a.text(66, 558, "plazo del watchdog: 60 s", 15, a.AMB, a.MONO, 600), 26, 75, still=1)
at(a, a.text(820, 558, "cercado: ya no puede escribir", 15, a.OK, a.MONO, 600, "end"), 56, 75, still=1)

# ha-manager status
TX, TY, TW, TH = 870, 182, 282, 388
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(tline(a, TX + 16, TY + 32, "# ha-manager status", MINT))
a.add(tline(a, TX + 16, TY + 62, "quorum OK", MINT))
a.add(tline(a, TX + 16, TY + 88, "master pve3 (active)"))
at(a, tline(a, TX + 16, TY + 114, "lrm pve1 (active)"), 0, 30)
at(a, tline(a, TX + 16, TY + 114, "lrm pve1 (old timestamp", CORAL) + tline(a, TX + 16, TY + 136, "  - dead?)", CORAL), 30, 100, still=1)
a.add(tline(a, TX + 16, TY + 166, "lrm pve2 (active)"))
a.add(tline(a, TX + 16, TY + 192, "lrm pve3 (active)"))
a.add(tline(a, TX + 16, TY + 232, "service vm:100", SKY))
for t0, t1, s_, col, st in [(0, 30, "(pve1, started)", MINT, 0), (30, 56, "(pve1, fence)", GOLD, 0), (56, 72, "(pve1, recovery)", GOLD, 1),
                            (72, 80, "(pve2, started)", GOLD, 0), (80, 100, "(pve2, started)", MINT, 0)]:
    at(a, tline(a, TX + 16, TY + 258, s_, col), t0, t1, still=st)
at(a, tline(a, TX + 16, TY + 300, "espera el cercado", SKY), 30, 56)
at(a, tline(a, TX + 16, TY + 300, "busca nodo con quórum", SKY) + tline(a, TX + 16, TY + 322, "y menos carga: pve2", SKY), 56, 72, still=1)
at(a, tline(a, TX + 16, TY + 300, "corriendo otra vez,", MINT) + tline(a, TX + 16, TY + 322, "en un par de minutos", MINT), 80, 100)

status(a, 628, [
    (0, 25, "HA con tres votos y disco compartido: la base para que la VM pueda cambiar de nodo.", a.INK, 0),
    (25, 50, "Antes de arrancarla en otro lado, la HA se asegura de que la copia vieja no pueda escribir.", a.AMB, 0),
    (50, 75, "Con el nodo cercado, el gestor elige dónde recuperar el servicio.", a.BLUE, 1),
    (75, 100, "Nadie entró a las tres de la mañana: la receptora volvió sola.", a.OK, 0),
])

write(a, 10, "r1", "Se cae un nodo: la receptora vuelve sola en pve2",
      "Animación en cuatro tiempos con un clúster de tres nodos, pve1, pve2 y pve3 (master del CRM), el almacenamiento compartido con el disco de la VM y la salida de ha-manager status. "
      "1: la VM de la receptora de alarmas, vm:100, corre en pve1 bajo HA y escribe en el almacenamiento compartido; ha-manager status muestra quorum OK y service vm:100 (pve1, started). "
      "2: falla la fuente de pve1 y el nodo se apaga; ha-manager status muestra lrm pve1 (old timestamp - dead?) y el servicio pasa a fence: la HA espera el plazo del watchdog, 60 segundos, para que pve1 quede cercado y la copia vieja no pueda escribir. "
      "3: con pve1 cercado, el servicio pasa a recovery y el gestor busca un nodo con quórum y menos carga: pve2. "
      "4: la VM arranca en pve2 sobre el mismo disco compartido y queda (pve2, started); la receptora vuelve a funcionar en un par de minutos sin que nadie intervenga.",
      [8, 36, 62, 66, 90])
