#!/usr/bin/env python3
"""Lección 16 (Identificador y audio) · Laboratorio, paso 5: detectar la impedancia (ACIM) con la línea libre antes de
tocar ganancias. Si la impedancia del FXO no coincide con la de la línea, parte de la voz que sale rebota y vuelve como
eco; subir RX Gain sube también ese eco. Fuentes: la lección (lo que sale pasa por TX Gain hacia la línea y lo que entra
por RX Gain hacia las internas; si la impedancia no coincide parte de la voz rebota como eco; Detect ERL o Pr y Update;
ganancias de -13,5 a +12 dB, de a poco; subir el volumen solo agranda el problema)."""
from _anim_gs_red import R

g = R(T=26, fix=88, kicker="GRANDSTREAM · IDENTIFICADOR Y AUDIO · LABORATORIO",
      title="Primero la impedancia: la voz que rebota en la línea")
g.steps([
    "Hablás desde la 1001: tu voz sale por TX Gain y el FXO1 hacia la línea.",
    "Con la impedancia del FXO distinta de la de la línea, parte rebota: te escuchás con eco.",
    "Subir RX Gain para escuchar mejor sube también el eco: el problema se agranda.",
    "Detect (ERL o Pr) con la línea libre y Update: el rebote baja; después, ganancias.",
])

Y = 200
g.add(g.dev(48, Y + 20, 200, 96, "1001", "interna", icon="tel"))
UX, UW = 300, 540
g.add(g.box(UX, Y, UW, 136, g.INK, rx=16))
g.add(g.text(UX + 20, Y + 30, "UCM · Antel_Linea1", 17, g.WHITE, g.HEAD, 600))
blocks = [("TX Gain", UX + 20, Y + 46), ("RX Gain", UX + 20, Y + 92)]
for n, x, y in blocks:
    g.add(g.box(x, y, 150, 34, "#123E66", None, rx=8) + g.text(x + 75, y + 23, n, 15, g.WHITE, g.MONO, 600, "middle"))
g.appear(g.text(UX + 182, Y + 135 - 22, "0 dB", 14, g.SKY, g.MONO), 0, 50)
g.appear(g.text(UX + 182, Y + 135 - 22, "+6 dB", 14, g.GOLD, g.MONO, 600), 50, 75)
g.appear(g.text(UX + 182, Y + 135 - 22, "0 dB", 14, g.SKY, g.MONO), 75, 100)
HX = UX + 300
g.add(g.box(HX, Y + 46, 220, 80, "#123E66", None, rx=10))
g.add(g.text(HX + 110, Y + 74, "FXO1", 16, g.WHITE, g.MONO, 600, "middle"))
g.appear(g.text(HX + 110, Y + 104, "impedancia: no coincide", 13, "#FF9C86", g.MONO, 600, "middle"), 0, 75)
g.appear(g.text(HX + 110, Y + 104, "impedancia: ACIM ajustada", 13, g.MINT, g.MONO, 600, "middle"), 75, 100)
PAR = "#3B4D61"
g.add(f'<line x1="{UX + UW}" y1="{Y + 86}" x2="900" y2="{Y + 86}" stroke="{PAR}" stroke-width="8"/>'
      f'<line x1="{UX + UW}" y1="{Y + 86}" x2="900" y2="{Y + 86}" stroke="#F7FAFD" stroke-width="2"/>')
g.add(g.dev(900, Y + 38, 252, 96, "Línea de Antel", "el que llama", icon="antel"))
g.add(g.wire(248, Y + 68, UX, Y + 68, g.BLUE))

# voz que sale (arriba) y eco que vuelve (abajo)
UP, DN = Y - 22, Y + 162
voz = lambda: g.chip("tu voz", bg=g.BLUE, size=13, h=24)
for k in range(3):
    t = 3 + k * 7
    g.token([(150, UP), (1020, UP)], t, t + 7, voz(), hold=t + 7.3)
def eco(t0, t1, size, op, label="eco"):
    for k in range(3):
        t = t0 + k * 7
        if t + 6 > t1:
            break
        inner = f'<g opacity="{op}">' + g.chip(label, bg=g.BAD, size=size, h=int(size * 1.9)) + '</g>'
        g.token([(HX + 110, DN), (150, DN)], t, t + 6, inner, hold=t + 6.2)
for k in range(3):
    t = 27 + k * 7
    g.token([(150, UP), (1020, UP)], t, t + 7, voz(), hold=t + 7.3)
eco(29, 50, 13, 1)
for k in range(3):
    t = 52 + k * 7
    g.token([(150, UP), (1020, UP)], t, t + 7, voz(), hold=t + 7.3)
eco(54, 75, 17, 1, "ECO")
for k in range(3):
    t = 77 + k * 7
    g.token([(150, UP), (1020, UP)], t, t + 7, voz(), hold=t + 7.3)
eco(79, 100, 11, 0.35)
g.appear(f'<path d="M{HX + 60} {Y + 126} C {HX + 40} {DN - 10}, {HX + 10} {DN}, {HX - 20} {DN}" stroke="{g.BAD}" stroke-width="3" fill="none" stroke-dasharray="6 5"/>'
         + g.text(HX + 120, DN + 6, "rebota", 15, g.BAD, g.MONO, 600), 27, 75)
g.fijo_only(f'<g transform="translate(700 {UP})">' + voz() + '</g>' + f'<g transform="translate(420 {DN})" opacity=".35">' + g.chip("eco", bg=g.BAD, size=11, h=21) + '</g>')

# lo que se escucha
g.add(g.box(48, 400, 520, 116, g.WHITE, g.LINE, rx=14))
g.add(g.text(68, 430, "lo que escuchás en la 1001", 15, g.GREY, g.MONO))
g.appear(g.text(68, 474, "al que llama, sin eco", 19, g.OK, g.SANS, 600), 0, 25)
g.appear(g.text(68, 474, "tu propia voz, un instante después", 19, g.BAD, g.SANS, 600), 25, 50)
g.appear(g.text(68, 474, "más fuerte el otro… y el eco", 19, g.BAD, g.SANS, 600), 50, 75)
g.appear(g.text(68, 474, "el eco bajó: ahora sí, ganancias", 19, g.OK, g.SANS, 600), 75, 100)
g.add(g.term(592, 400, 560, 116, "PBX Settings > Interface Settings > Analog Hardware", [("FXO (opciones) · Detect (ERL o Pr) > Update", g.MINT), ("con la línea libre", None)], size=16, lh=28))

g.add(g.note(48, 540, 1104, None, ["Después, de a poco y con llamadas reales: RX Gain si vos escuchás bajo, TX Gain si al otro lado te escuchan bajo (de -13,5 a +12 dB)."], "info"))

g.done(16, "l1", "Primero la impedancia: la voz que rebota en la línea",
       "Animación en cuatro tiempos con la interna 1001, la UCM con la troncal Antel_Linea1, sus bloques TX Gain y RX Gain y el FXO1, y la línea de Antel; arriba viaja tu voz hacia la línea y abajo vuelve lo que rebota. "
       "1: hablás desde la 1001 y tu voz sale por TX Gain y el FXO1 hacia la línea; escuchás al que llama sin eco. "
       "2: si la impedancia del FXO no coincide con la de la línea, parte de esa voz rebota y vuelve por RX hacia la 1001: te escuchás un instante después, con eco. "
       "3: subir RX Gain, por ejemplo a +6 dB, para escuchar mejor al otro sube también el eco: el problema se agranda. "
       "4: en PBX Settings > Interface Settings > Analog Hardware, opciones del FXO, Detect (ERL o Pr) con la línea libre y Update: la impedancia queda ajustada y el rebote baja; recién ahí, ganancias de a poco con llamadas reales, RX si vos escuchás bajo y TX si te escuchan bajo, de -13,5 a +12 dB.",
       [10, 36, 62, 90])
