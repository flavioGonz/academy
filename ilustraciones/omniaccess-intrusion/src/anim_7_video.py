#!/usr/bin/env python3
"""Lección 7 · Teoría · De dónde sale el vivo y de dónde la grabación.
Sale de teoria_md (Cómo funciona): cada cámara tiene dos flujos en go2rtc (liviano y alta resolución); el navegador pide
el video al servidor (/go2rtc/api/stream.mp4) y no a la cámara, así la cámara recibe una sola conexión aunque la miren
varios operadores; la grabación viene del NVR: el servidor busca NVR y canal (mapeo de canales), pide el tramo y, si el
NVR graba en H.265, lo transcodifica antes de mandarlo; sin vínculo con un canal, la pestaña lo dice."""
from _anim_omni import new, out, when, travel, seq, box

a = new(24, "VIVO Y GRABACIÓN", "El vivo pasa por go2rtc; la grabación, por el NVR")
a.steps([
    "Tres operadores abren Vivo: piden el video al servidor, no a la cámara.",
    "go2rtc tiene los dos flujos de la cámara: ella atiende una sola conexión.",
    "Grabación: el servidor busca NVR y canal de la cámara y pide el tramo.",
    "El NVR graba en H.265: el servidor lo transcodifica antes de mandarlo.",
], still=2)

# operadores
OPS = [(48, 196), (48, 290), (48, 384)]
for i, (x, y) in enumerate(OPS):
    a.add(box(x, y, 236, 76, f"Operador {i + 1}", "navegador", "laptop"))

# servidor
SX, SY, SW, SH = 392, 182, 400, 400
a.add(a.box(SX, SY, SW, SH, a.WHITE, a.LINE, rx=16))
a.add(a.text(SX + 20, SY + 32, "Servidor OmniAccess", 18, a.INK, a.SANS, 600))
a.add(a.box(SX + 16, SY + 50, SW - 32, 140, a.SLATE, rx=12))
a.add(a.text(SX + 34, SY + 80, "go2rtc", 17, a.INK, a.SANS, 600))
a.add(a.text(SX + 34, SY + 106, "/go2rtc/api/stream.mp4", 15, a.GREY, a.MONO))
a.add(a.pill(SX + 34, SY + 124, "liviano", a.BLUE, a.WHITE, 15, 30) + a.pill(SX + 150, SY + 124, "alta resolución", a.BLUE, a.WHITE, 15, 30))
a.add(a.box(SX + 16, SY + 206, SW - 32, 178, a.SLATE, rx=12))
a.add(a.text(SX + 34, SY + 236, "reproducción", 17, a.INK, a.SANS, 600))
a.add(a.text(SX + 34, SY + 262, "mapeo de canales", 15, a.GREY, a.MONO))
when(a, a.text(SX + 34, SY + 292, "Perímetro Norte 12 → NVR · D5", 15, a.INK, a.MONO, 600), 51, 100, still=1)
when(a, f'<rect x="{SX + 26}" y="{SY + 272}" width="{SW - 52}" height="30" rx="8" fill="none" stroke="{a.AMB}" stroke-width="2.5"/>', 51, 75, still=0)
when(a, a.pill(SX + 34, SY + 308, "transcodifica", a.WHITE, a.AMB, 15, 30), 76, 100, still=0)
when(a, a.text(SX + 34, SY + 362, "a algo que el navegador reproduce", 15, a.AMB, a.MONO, 600), 76, 100, still=0)

# cámara y NVR
a.add(box(912, 230, 240, 84, "Cámara", "Perímetro Norte 12", "camera"))
a.add(box(912, 444, 240, 84, "NVR", "graba en H.265", "server"))

# 1: operadores -> servidor (go2rtc)
for i, (x, y) in enumerate(OPS):
    yy = y + 38
    seq(a, f"M292 {yy} C340 {yy} 350 {SY + 120} {SX - 8} {SY + 120}", 2 + i * 2, 50, a.BLUE, still=1)
when(a, a.text(48, 492, "piden el video al servidor", 15, a.BLUE, a.MONO, 600), 2, 50, still=0)
# 2: una sola conexión
seq(a, f"M{SX + SW + 6} {SY + 110} H904", 26, 50, a.CYAN, "1 conexión", (SX + SW + 904) / 2, SY + 100, still=1, width=4)
travel(a, (890, SY + 110), (SX + SW + 20, SY + 110), 27, 34, dot=8, bg=a.CYAN, hold=14)
when(a, a.pill(912, 330, "no importa cuántos miren", a.OK, a.OKBG, 15, 30), 30, 50, still=1)

# 3: grabación
seq(a, f"M292 {OPS[2][1] + 28} C340 {OPS[2][1] + 28} 340 {SY + 250} {SX - 8} {SY + 250}", 51, 100, a.AMB, still=1)
when(a, a.text(48, 492, "Operador 3: pestaña Grabación", 15, a.AMB, a.MONO, 600), 51, 100, still=1)
seq(a, f"M{SX + SW + 6} {SY + 290} H904", 54, 100, a.AMB, "tramo", (SX + SW + 904) / 2, SY + 280, still=1)
seq(a, f"M904 {SY + 320} H{SX + SW + 6}", 62, 100, a.GREY, "H.265", (SX + SW + 904) / 2, SY + 344, still=1)
# 4: entrega
seq(a, f"M{SX - 8} {SY + 340} C340 {SY + 340} 340 {OPS[2][1] + 56} 292 {OPS[2][1] + 56}", 78, 100, a.AMB, still=0)
when(a, a.pill(48, 520, "sin vínculo: la pestaña lo dice", a.GREY, a.SLATE, 15, 30), 80, 100, still=0)

a.add(a.text(48, 640, "Por eso puede andar el vivo y no la grabación: salen de lugares distintos.", 16, a.TXT, a.SANS, 600))

out(a, 7, 1, "El vivo y la grabación salen de lugares distintos",
    "Animación en cuatro tiempos. A la izquierda, tres operadores con su navegador; en el centro, el servidor OmniAccess con go2rtc (flujo liviano y de alta resolución, en /go2rtc/api/stream.mp4) "
    "y la reproducción con el mapeo de canales; a la derecha, la cámara Perímetro Norte 12 y el NVR, que graba en H.265. "
    "Tiempo 1: los tres operadores abren Vivo y piden el video al servidor, no a la cámara. "
    "Tiempo 2: go2rtc toma el video de la cámara por una sola conexión, no importa cuántos miren. "
    "Tiempo 3: el operador 3 abre la pestaña Grabación; el servidor busca en el mapeo que Perímetro Norte 12 graba en el canal D5 del NVR y le pide el tramo; el NVR lo devuelve en H.265. "
    "Tiempo 4: el servidor lo transcodifica a algo que el navegador reproduce y lo entrega. Sin vínculo con un canal, la pestaña lo dice. "
    "Al pie: por eso puede andar el vivo y no la grabación, salen de lugares distintos.",
    [12, 40, 62, 92])
