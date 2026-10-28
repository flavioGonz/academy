#!/usr/bin/env python3
"""Lección 25 · Resumen, "Cómo se ve en la red": el NVR graba cámaras en un router con dos bridges;
el segundo bridge no tiene hardware offloading y el video pasa por la CPU. Con un solo bridge
(y una VLAN para las cámaras) el switch chip conmuta y la CPU queda libre.
Fuente: Bridging and Switching (solo un bridge offloaded por switch chip salvo CRS1xx/2xx;
la VLAN filtering por hardware depende del chip: tabla de la documentación)."""
from _anim_red_1_9 import *

a = Anim(T=26, kicker="MIKROTIK · UN SOLO BRIDGE · CÓMO SE VE EN LA RED", title="Dos bridges: el video de las cámaras sube a la CPU")
a.steps([
    "Router de la obra con dos bridges: oficina en bridge, cámaras y NVR en bridge-cctv.",
    "bridge-cctv no tiene H: cada trama de video pasa por la CPU, que se satura.",
    "Un solo bridge, con una VLAN para las cámaras: todos los puertos llevan H.",
    "El switch chip lleva el video de la cámara al NVR. La CPU ni lo ve.",
], still=3)

# ---------- router
RX, RY, RW, RH = 48, 186, 652, 262
a.add(a.box(RX, RY, RW, RH, a.INK, rx=18))
a.add(a.text(RX + 22, RY + 34, "Router de la obra", 19, a.WHITE, a.HEAD, 600))
CPUX, CPUY, CPUW, CPUH = 300, RY + 14, 160, 56
a.add(a.box(CPUX, CPUY, CPUW, CPUH, a.NAVY2, "#2E5C88", rx=10))
a.add(a.text(CPUX + CPUW / 2, CPUY + 35, "CPU", 18, a.WHITE, a.MONO, 600, "middle"))
a.add(during(a, a.box(CPUX - 3, CPUY - 3, CPUW + 6, CPUH + 6, "none", "#FF7A5C", rx=12, sw=3), 30, 50))
CHY = RY + 112
a.add(a.box(RX + 20, CHY, RW - 40, 64, "#12385C", rx=10))
a.add(a.text(RX + 36, CHY + 26, "switch", 15, SKY, a.MONO))
a.add(a.text(RX + 36, CHY + 48, "chip", 15, SKY, a.MONO))
PORTS = ["ether2", "ether3", "ether4", "ether5"]
PX = [250 + i * 118 for i in range(4)]   # centros
PY = RY + 196
for x, n in zip(PX, PORTS):
    a.add(a.box(x - 50, PY, 100, 40, "#12385C", rx=8))
    a.add(a.text(x, PY + 26, n, 15, a.WHITE, a.MONO, 600, "middle"))
    a.add(f'<line x1="{x}" y1="{PY}" x2="{x}" y2="{CHY + 64}" stroke="#2E5C88" stroke-width="3"/>')
# pertenencia a bridges, sobre el chip
before = (a.box(PX[0] - 50, CHY + 6, PX[1] - PX[0] + 100, 28, "#16452E", rx=8)
          + a.text((PX[0] + PX[1]) / 2, CHY + 26, "bridge · H", 15, MINT, a.MONO, 600, "middle")
          + a.box(PX[2] - 50, CHY + 6, PX[3] - PX[2] + 100, 28, "#4A3410", rx=8)
          + a.text((PX[2] + PX[3]) / 2, CHY + 26, "bridge-cctv · sin H", 15, GOLD, a.MONO, 600, "middle"))
after = (a.box(PX[0] - 50, CHY + 6, PX[3] - PX[0] + 100, 28, "#16452E", rx=8)
         + a.text((PX[0] + PX[3]) / 2, CHY + 26, "bridge · H en los cuatro puertos", 15, MINT, a.MONO, 600, "middle"))
a.add(during(a, before, 0, 50))
a.add(during(a, after, 50, 100, still=1))

# ---------- equipos
DEV = [("PC oficina", "laptop"), ("AP WiFi", "wifi"), ("Cámaras", "camera"), ("NVR", "server")]
DY = 486
for x, (n, ic) in zip(PX, DEV):
    a.add(a.box(x - 56, DY, 112, 70, a.WHITE, a.LINE, rx=12))
    a.add(glyph(a, ic, x - 14, DY + 8, a.BLUE, 1.2))
    a.add(a.text(x, DY + 58, n, 15, a.INK, a.SANS, 600, "middle"))
    a.add(line(x, PY + 40, x, DY, a.BLUE, 3))
for x in PX[2:]:
    a.add(during(a, a.pill(x + 8, PY + 48, "VLAN 20", a.CYAN, "#E3F4FA", 14, 24), 52, 100, still=1))

# ---------- flujo de video cámara -> NVR
C, N = PX[2], PX[3]
via_cpu = [(C, DY - 6), (C, CHY + 48), (CPUX + 50, CPUY + CPUH - 6), (CPUX + CPUW - 50, CPUY + CPUH - 6), (N, CHY + 48), (N, DY - 6)]
via_chip = [(C, DY - 6), (C, CHY + 48), (N, CHY + 48), (N, DY - 6)]
dot = f'<circle cx="0" cy="0" r="7" fill="{a.CYAN}" stroke="{a.WHITE}" stroke-width="2"/>'
t = 2.0
while t < 46:
    a.add(travel(a, dot, via_cpu, t, t + 4.5, hold=0, fade=0.3))
    t += 1.6
t = 52.0
while t < 96:
    a.add(travel(a, dot, via_chip, t, t + 2.6, hold=0, fade=0.3))
    t += 1.6
a.add(still_only(a, place(a, dot, (C + N) / 2, CHY + 48) + place(a, dot, (C + N) / 2 - 34, CHY + 48) + place(a, dot, (C + N) / 2 + 34, CHY + 48)))

# ---------- panel derecho
PX0, PY0, PWd = 730, 186, 422
a.add(a.box(PX0, PY0, PWd, 370, a.WHITE, a.LINE, rx=18))
a.add(a.text(PX0 + 20, PY0 + 34, "/interface/bridge/port/print", 16, a.INK, a.MONO, 600))
rows_b = [("H", "ether2", "bridge"), ("H", "ether3", "bridge"), ("", "ether4", "bridge-cctv"), ("", "ether5", "bridge-cctv")]
rows_a = [("H", "ether2", "bridge"), ("H", "ether3", "bridge"), ("H", "ether4", "bridge"), ("H", "ether5", "bridge")]
for k, (rows, t0, t1, st) in enumerate(((rows_b, 0, 50, 0), (rows_a, 50, 100, 1))):
    body = ""
    for i, (h, p, b) in enumerate(rows):
        y = PY0 + 52 + i * 38
        body += a.box(PX0 + 16, y, PWd - 32, 32, a.SLATE if h else a.AMBBG, rx=6)
        body += a.text(PX0 + 30, y + 22, h or "·", 15, a.OK if h else a.AMB, a.MONO, 600)
        body += a.text(PX0 + 62, y + 22, p, 15, a.INK, a.MONO, 600)
        body += a.text(PX0 + 170, y + 22, b, 15, a.TXT, a.MONO)
    a.add(during(a, body, t0, t1, still=st))
# medidor de CPU
MY = PY0 + 222
a.add(a.text(PX0 + 20, MY, "cpu-used", 15, a.GREY, a.MONO))
BW = PWd - 40
a.add(a.box(PX0 + 20, MY + 12, BW, 22, "#E6EDF4", rx=11))
k = a.keyframes([(0, 0.25), (20, 0.35), (34, 1), (50, 1), (56, 0.06), (100, 0.06)], "transform", "scaleX({})")
fill_bad = a.group(a.box(PX0 + 20, MY + 12, BW, 22, a.BAD, rx=11), k, still=None, origin=f"{PX0 + 20}px {MY + 12}px")
a.add(a.group(fill_bad, a.show(0, 50, 0.6), still=0))
k2 = a.keyframes([(0, 0.06), (100, 0.06)], "transform", "scaleX({})")
fill_ok = a.group(a.box(PX0 + 20, MY + 12, BW, 22, a.OK, rx=11), k2, still=None, origin=f"{PX0 + 20}px {MY + 12}px")
a.add(a.group(fill_ok, a.show(50, 100, 0.6), still=0))
a.add(still_only(a, a.box(PX0 + 20, MY + 12, BW * 0.06, 22, a.OK, rx=11)))
a.add(during(a, a.text(PX0 + PWd - 20, MY, "100 %", 15, a.BAD, a.MONO, 600, "end"), 34, 50))
a.add(during(a, a.text(PX0 + PWd - 20, MY, "baja", 15, a.OK, a.MONO, 600, "end"), 56, 100, still=1))
a.add(during(a, a.text(PX0 + 20, MY + 70, "La grabación del NVR tiene cortes.", 15, a.BAD, a.SANS, 600), 36, 50))
a.add(during(a, a.text(PX0 + 20, MY + 70, "El video ya no pasa por la CPU.", 15, a.OK, a.SANS, 600), 76, 100, still=1))
a.add(during(a, a.text(PX0 + 20, MY + 96, "Las VLAN por hardware dependen del chip:", 15, a.TXT, a.SANS)
             + a.text(PX0 + 20, MY + 117, "mirá la tabla de tu modelo en la documentación.", 15, a.TXT, a.SANS), 50, 100, still=1))

status(a, 628, [
    (0, 25, "Fuera de los CRS1xx/2xx, el switch chip hace hardware offloading para un solo bridge.", a.INK, 0),
    (25, 50, "Sin H, la trama sube del chip a la CPU y vuelve a bajar: con 16 cámaras, la CPU no da abasto.", a.BAD, 0),
    (50, 75, "Para separar redes en el mismo chip se usa VLAN, no un bridge más.", a.INK, 0),
    (75, 100, "Con H, el chip decide el puerto de salida solo: la CPU solo ve estadísticas.", a.OK, 1),
], size=17)

write(a, 25, "r1", "Dos bridges contra uno: dónde pasa el video",
      "Animación en cuatro tiempos con el router de la obra: la CPU arriba, el switch chip en el medio y los puertos ether2 a ether5 con una PC de oficina, un AP WiFi, las cámaras y el NVR. "
      "1: hay dos bridges: bridge con ether2 y ether3, con la marca H, y bridge-cctv con ether4 y ether5, sin H, porque fuera de los CRS1xx/2xx el chip hace hardware offloading para un solo bridge. "
      "2: el video de las cámaras al NVR sube del chip a la CPU y vuelve a bajar; cpu-used llega al 100 % y la grabación tiene cortes. "
      "3: queda un solo bridge con los cuatro puertos y la marca H, y las cámaras y el NVR van en la VLAN 20. "
      "4: el switch chip lleva el video de ether4 a ether5 sin pasar por la CPU, que queda baja. "
      "Aclaración: que la VLAN se haga por hardware depende del chip de cada modelo, según la tabla de la documentación.",
      [10, 40, 60, 85])
