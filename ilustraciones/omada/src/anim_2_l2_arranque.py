#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 3: esperar el arranque. Java y MongoDB levantan en 1 a 2 minutos con unos 1,9 GB de RAM;
la web del 8043 contesta recién cuando aparece la línea de arranque con la versión. Reiniciar por impaciencia vuelve el reloj a cero."""
from _anim_om_red import *

a = nueva(24, "HOST DEDICADO", "El arranque tarda: esperá la línea con la versión", "l")
F = a.steps([
    "docker compose up -d: el contenedor arranca, pero adentro recién empiezan Java y MongoDB.",
    "Mientras tanto, el navegador al 8043 no responde todavía. No es un error.",
    "Entre 1 y 2 minutos: aparece la línea de arranque con la versión y la web contesta.",
    "Si lo reiniciás por impaciencia, el arranque vuelve a empezar de cero.",
], still=2)

# reloj de arranque (barra)
BX, BY, BW = 48, 196, 1104
a.add(a.box(BX, BY, BW, 104, a.WHITE, a.LINE, rx=16))
a.add(a.text(BX + 22, BY + 30, "Arranque del controlador", 16, a.INK, a.SANS, 600))
X0, X1, Y = 80, 1120, BY + 52
a.add(line(X0, Y, X1, Y, a.LINE, 10))
for x, lab in ((X0, "0"), (600, "1 min"), (X1, "2 min")):
    a.add(a.text(x, Y + 34, lab, 15, a.GREY, a.MONO, 400, "middle" if x not in (X0, X1) else ("start" if x == X0 else "end")))
a.add(line(600, Y - 8, 600, Y + 8, a.GREY, 2))
# barra: 0 -> 75% (llega a ~1,5 min) entre 0 y 70; fase 4 vuelve a 0 y crece de nuevo
pts = [(0, 0.02), (70, 0.78), (75, 0.78), (76, 0.02), (100, 0.30)]
fill = a.keyframes([(p, f"{v:.3f}") for p, v in pts], "transform", "scaleX({})")
a.n += 1
c = f"c{a.n}"
a.css.append(f".{c}{{transform-box:view-box;transform-origin:{X0}px {Y}px;transform:scaleX(.78);animation:{fill} {a.T}s linear infinite}}")
a.add(f'<g class="{c}">{line(X0, Y, X1, Y, a.BLUE, 10)}</g>')

# terminal con el log (líneas genéricas, sin texto inventado)
TX, TY, TW, TH = 48, 316, 560, 270
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 32, "$ docker logs -f omada-controller", 15, a.WHITE, a.MONO))
for i, (t0, w) in enumerate([(4, 420), (10, 360), (16, 470), (24, 300), (32, 440), (40, 380), (47, 330)]):
    at(a, a.box(TX + 20, TY + 54 + i * 22, w, 10, "#24507A", rx=5), t0, 76)
at(a, a.box(TX + 14, TY + 214, TW - 28, 40, "#0E8F5E", rx=10)
   + a.text(TX + 30, TY + 240, "línea de arranque con la versión", 16, a.WHITE, a.SANS, 600), 52, 76, still=1)
at(a, a.text(TX + 20, TY + 240, "(reinicio: el log empieza de nuevo)", 15, GOLD, a.MONO), 77, 100)

# navegador
NX, NY, NW = 640, 316, 512
a.add(a.box(NX, NY, NW, 150, a.WHITE, a.LINE, rx=14))
a.add(a.box(NX, NY, NW, 44, a.SLATE, rx=14) + a.box(NX, NY + 30, NW, 14, a.SLATE, rx=0))
a.add(a.text(NX + 20, NY + 29, "https://<IP-de-la-VM>:8043", 15, a.INK, a.MONO))
at(a, a.text(NX + 24, NY + 90, "No responde todavía", 18, a.AMB, a.SANS, 600)
   + a.text(NX + 24, NY + 118, "el servicio sigue arrancando", 15, a.GREY, a.MONO), 26, 52)
at(a, check(a, NX + 38, NY + 96, 15) + a.text(NX + 64, NY + 102, "Asistente de configuración", 18, a.OK, a.SANS, 600)
   + a.text(NX + 64, NY + 128, "Create a Local Account", 15, a.GREY, a.MONO), 54, 76, still=1)
at(a, a.text(NX + 24, NY + 90, "No responde, otra vez", 18, a.BAD, a.SANS, 600)
   + a.text(NX + 24, NY + 118, "el reinicio solo lo demoró", 15, a.GREY, a.MONO), 82, 100)
for t0 in (28, 38):
    travel(a, dot(a, a.CYAN), [(NX + 40, NY + 150), (NX + 40, NY + 190)], t0, t0 + 2, hold=0.2)

# RAM
RX, RY = 640, 490
a.add(a.box(RX, RY, NW, 96, a.WHITE, a.LINE, rx=14))
a.add(a.text(RX + 20, RY + 32, "RAM del contenedor", 16, a.INK, a.SANS, 600))
a.add(line(RX + 24, RY + 64, RX + NW - 24, RY + 64, a.LINE, 12))
rpts = [(0, 0.05), (55, 0.80), (75, 0.80), (76, 0.05), (100, 0.35)]
rk = a.keyframes([(p, f"{v:.3f}") for p, v in rpts], "transform", "scaleX({})")
a.n += 1
c2 = f"c{a.n}"
a.css.append(f".{c2}{{transform-box:view-box;transform-origin:{RX + 24}px {RY + 64}px;transform:scaleX(.8);animation:{rk} {a.T}s linear infinite}}")
a.add(f'<g class="{c2}">{line(RX + 24, RY + 64, RX + NW - 24, RY + 64, a.CYAN, 12)}</g>')
at(a, a.text(RX + NW - 24, RY + 32, "unos 1,9 GB", 16, a.CYAN, a.MONO, 600, "end"), 50, 76, still=1)

status(a, 628, [
    (0, 25, "El contenedor figura Up desde el primer segundo: eso no quiere decir que el controlador esté listo.", a.INK, 0),
    (25, 50, "Esperá mirando el log; el 8043 contesta cuando termina de arrancar.", a.INK, 0),
    (50, 75, "Listo: entrá al asistente y elegí Create a Local Account.", a.OK, 1),
    (75, 100, "Reiniciar por impaciencia solo demora: el arranque vuelve a empezar.", a.BAD, 0),
], x=48, anchor="start", size=16)

write(a, 2, "l2", "Esperar el arranque del controlador en Docker",
      "Animación en cuatro tiempos con una barra del tiempo de arranque de 0 a 2 minutos, la terminal con docker logs -f omada-controller, "
      "el navegador apuntando a https://IP-de-la-VM:8043 y la RAM del contenedor. "
      "1: docker compose up -d deja el contenedor arriba, pero adentro recién empiezan Java y MongoDB; el log va sumando líneas. "
      "2: el navegador al 8043 todavía no responde, porque el servicio sigue arrancando; no es un error. "
      "3: entre 1 y 2 minutos aparece la línea de arranque con la versión, la RAM llega a unos 1,9 GB y la web contesta con el asistente para crear la cuenta local. "
      "4: si se reinicia el contenedor por impaciencia, el log y el arranque vuelven a empezar de cero y la web vuelve a no responder.",
      [8, 36, 62, 90])
