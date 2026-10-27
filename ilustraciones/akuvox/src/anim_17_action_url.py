#!/usr/bin/env python3
"""Lección 17 · teoría: Action URL toma la URL del evento, reemplaza variables y manda un GET que el servidor registra."""
from _anim_akuvox_15_28 import *

a = new(24, "AKUVOX · LECCIÓN 17", "Action URL: el evento arma la URL y la manda")
a.steps([
    "Se dispara el relé A. El portero toma la URL cargada para ese evento.",
    "Reemplaza las variables: $relay1status vale 1 con el relé abierto.",
    "Manda el GET. El servidor responde 404, pero imprime la línea: esa es la prueba.",
    "Se cierra el relé A: la URL de Relay A Closed llega como GET /relayclose=0.",
], still=2)

# portero y relé
a.add(I.Generic(48, 192, "Portero", "192.168.88.21", icon="bell", w=240).svg())
a.add(a.box(48, 300, 240, 84, a.WHITE, a.LINE))
a.add(a.text(68, 334, "Relé A", 19, a.INK, a.SANS, 600))
a.add(at(a, a.text(68, 358, "en reposo", 15, a.GREY, a.MONO), 0, 3, still=0))
a.add(at(a, a.box(48, 300, 240, 84, a.OKBG, a.OK, sw=3) + a.text(68, 334, "Relé A", 19, a.INK, a.SANS, 600)
         + a.text(68, 358, "activado", 15, a.OK, a.MONO, 600), 3, 76, still=1))
a.add(at(a, a.text(68, 358, "cerrado", 15, a.GREY, a.MONO, 600), 76, 100, still=0))
a.add(f'<path d="M168 276 V300" stroke="{a.LINE}" stroke-width="3"/>')

# tarjeta Action URL
CX, CW = 320, 520
a.add(a.box(CX, 192, CW, 192, a.WHITE, a.LINE))
a.add(a.text(CX + 18, 220, "Action URL · cargadas en la web", 15, a.GREY, a.MONO, 600))
rows = [("Relay A Triggered", "http://192.168.88.10:8000/relaytrigger=", 246),
        ("Relay A Closed", "http://192.168.88.10:8000/relayclose=", 318)]
for lab, url, y in rows:
    a.add(a.text(CX + 18, y, lab, 15, a.INK, a.SANS, 600))
    a.add(a.text(CX + 18, y + 26, url + "$relay1status", 15, a.TXT, a.MONO))
# resaltado de fila y de variable
for (lab, url, y), (t0, t1) in zip(rows, [(3, 50), (77, 100)]):
    a.add(at(a, a.box(CX + 8, y - 20, CW - 16, 56, "none", a.CYAN, rx=10, sw=2), t0, t1, still=1 if t0 == 3 else 0))
    vx = CX + 18 + len(url) * 15 * 0.6
    a.add(at(a, f'<rect x="{vx - 3:.0f}" y="{y + 10}" width="{13 * 9 + 6:.0f}" height="22" rx="5" fill="{a.AMBBG}" stroke="{a.AMB}" stroke-width="1.5"/>'
             + a.text(round(vx, 1), y + 26, "$relay1status", 15, a.AMB, a.MONO, 600), t0 + 24 if t0 == 3 else t0 + 2, t1, still=1 if t0 == 3 else 0))

# URL armada
a.add(a.text(CX, 414, "Lo que sale del portero", 15, a.GREY, a.SANS, 600))
u1, s1 = code(a, CX, 424, [("http://192.168.88.10:8000/relaytrigger=", "#D9E9F8"), ("1", "#FFD28A")], size=16)
u2, s2 = code(a, CX, 424, [("http://192.168.88.10:8000/relayclose=", "#D9E9F8"), ("0", "#FFD28A")], size=16)
a.add(at(a, u1 + a.text(s1[1][1] + 30, 452, "1 = abierto", 15, a.AMB, a.MONO, 600), 28, 76, still=1))
a.add(at(a, u2 + a.text(s2[1][1] + 30, 452, "0 = cerrado", 15, a.AMB, a.MONO, 600), 80, 100, still=0))
a.add(at(a, a.arrow(f"M{CX + 250} 386 V418", a.AMB, 2.5), 27, 50, still=0))
a.add(at(a, a.arrow(f"M{CX + 250} 386 V418", a.AMB, 2.5), 79, 90, still=0))

# servidor
a.add(I.Server(870, 192, "PC de laboratorio", "192.168.88.10:8000", w=282).svg())
a.add(packet(a, "GET /relaytrigger=1", (960, 446), (1011, 300), 52, 62, hide=63, size=15, via=[(55, 1011, 446)]))
a.add(packet(a, "GET /relayclose=0", (960, 446), (1011, 300), 86, 93, hide=94, size=15, via=[(88, 1011, 446)]))

# terminal
TY = 498
a.add(a.box(48, TY, 1104, 150, "#03213C", rx=14))
a.add(a.text(66, TY + 26, "TERMINAL · PC DE LABORATORIO · python3 -m http.server 8000", 15, "#7FA6C9", a.MONO, 500, extra='letter-spacing="1.5"'))
a.add(a.text(66, TY + 56, "Serving HTTP on 192.168.88.10 port 8000 ...", 15, "#D9E9F8", a.MONO))
l1 = '192.168.88.21 - - [...] "GET /relaytrigger=1 HTTP/1.1" 404 -'
l2 = '192.168.88.21 - - [...] "GET /relayclose=0 HTTP/1.1" 404 -'
a.add(at(a, a.text(66, TY + 84, l1, 15, "#7FE0FF", a.MONO, 600), 63, 100, still=1))
a.add(at(a, a.text(66, TY + 112, l2, 15, "#7FE0FF", a.MONO, 600), 94, 100, still=0))
a.add(at(a, a.text(1132, TY + 84, "404 no importa: vale la línea", 15, "#FFD28A", a.SANS, 600, "end"), 64, 100, still=1))

a.write(*out(17)[:1], title="Action URL en un portero Akuvox",
        desc=("Animación en cuatro tiempos. 1: se dispara el relé A y el portero 192.168.88.21 toma la URL cargada en Action URL para Relay A Triggered, "
              "http://192.168.88.10:8000/relaytrigger=$relay1status. 2: reemplaza la variable $relay1status por 1 (abierto) y arma http://192.168.88.10:8000/relaytrigger=1. "
              "3: manda el GET a la PC de laboratorio, que corre python3 -m http.server; responde 404 porque no tiene esa página, pero imprime la línea GET /relaytrigger=1, que es la prueba de que el portero avisó. "
              "4: al cerrarse el relé A, la URL de Relay A Closed llega como GET /relayclose=0."),
        preview=[12, 40, 56, 68, 96], prefix=out(17)[1])
