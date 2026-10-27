#!/usr/bin/env python3
"""Lección 4 · Teoría · El camino de un pedido de video.
Sale de teoria_md (Cómo funciona): cada stream de go2rtc.yaml tiene nombre y URL (bosch_ + IP con guiones bajos, cargado
a mano); go2rtc abre su API en el 1984 y su RTSP en el 8554; el navegador pide /go2rtc/api/stream.mp4?src=bosch_192_0_2_10,
el proxy inverso deriva /go2rtc/ al 1984 y go2rtc entrega MP4 fragmentado por HTTP; el reproductor se mantiene pegado al
vivo; el worker de despachos lee el mismo stream por el RTSP local para un anillo de unos 80 segundos."""
from _anim_omni import new, out, when, travel, seq, box

a = new(24, "VIDEO EN VIVO", "Un pedido de video, salto por salto")
a.steps([
    "El navegador pide stream.mp4 con el nombre del stream de la fila.",
    "El proxy inverso deriva /go2rtc/ a la API de go2rtc, en el puerto 1984.",
    "go2rtc busca el nombre en go2rtc.yaml y toma el RTSP de la cámara.",
    "Vuelve MP4 fragmentado por HTTP: el reproductor queda pegado al vivo.",
    "El worker lee el mismo stream por el RTSP local, para el anillo del clip.",
], still=3)

Y = 196
a.add(box(48, Y, 220, 84, "Navegador", "Filas, Monitor", "laptop"))
a.add(box(332, Y, 230, 84, "Proxy inverso", "/go2rtc/ → :1984", "shield"))
a.add(box(626, Y, 230, 84, "go2rtc", "1984 y 8554", "server"))
a.add(box(920, Y, 232, 84, "Cámara Bosch", "192.0.2.10", "camera"))

# 1: pedido
seq(a, f"M276 {Y + 30} H324", 2, 100, a.BLUE, still=1)
when(a, a.pill(48, Y + 140, "GET /go2rtc/api/stream.mp4?src=bosch_192_0_2_10", a.BLUE, a.WHITE, 15, 30), 2, 40, still=0)
travel(a, (268, Y + 30), (330, Y + 30), 3, 8, dot=8)
# 2: proxy -> 1984
seq(a, f"M570 {Y + 30} H618", 21, 100, a.BLUE, still=1)
travel(a, (562, Y + 30), (624, Y + 30), 22, 27, dot=8)
when(a, a.pill(332, Y + 184, "/go2rtc/ → puerto 1984", a.INK, a.SLATE, 15, 30), 21, 40, still=0)
# 3: yaml y RTSP
yaml = (a.box(626, Y + 140, 526, 100, a.INK, rx=10)
        + a.text(644, Y + 166, "go2rtc.yaml · streams:", 15, "#9FC3E3", a.MONO)
        + a.text(644, Y + 194, "bosch_192_0_2_10:", 15, "#FFFFFF", a.MONO, 600)
        + a.text(664, Y + 220, "rtsp://…@192.0.2.10/…", 15, "#9FC3E3", a.MONO))
when(a, yaml, 41, 60, still=0)
when(a, f'<rect x="638" y="{Y + 176}" width="200" height="26" rx="6" fill="none" stroke="#FFD28A" stroke-width="2.5"/>', 44, 60, still=0)
seq(a, f"M864 {Y + 30} H912", 46, 100, a.CYAN, "RTSP", 888, Y + 18, still=1)
# 4: fragmentos hacia el navegador
seq(a, f"M912 {Y + 62} H864", 61, 100, a.CYAN, still=1)
seq(a, f"M700 {Y + 92} V{Y + 116} H158 V{Y + 94}", 61, 100, a.CYAN, still=1)
when(a, a.text(447, Y + 108, "pasa por el proxy", 15, a.CYAN, a.MONO, 600, "middle"), 61, 100, still=1)
for k in range(4):
    t0 = 62 + k * 4
    travel(a, (690, Y + 116), (180, Y + 116), t0, t0 + 10, label="fMP4", bg=a.CYAN, hold=0.3, size=15)
when(a, a.pill(48, Y + 140, "MP4 fragmentado por HTTP · pegado al vivo", a.OK, a.OKBG, 15, 30), 62, 100, still=1)
when(a, a.text(48, Y + 200, "si el video falla: reintentos y,", 15, a.TXT, a.SANS)
     + a.text(48, Y + 222, "después, una captura cada 5 s", 15, a.TXT, a.SANS), 62, 100, still=1)

# 5: worker
WX, WY = 626, 450
a.add(box(WX, WY, 280, 84, "dispatch-worker", "clip de cada alerta", "server"))
seq(a, f"M780 {Y + 92} V{WY - 8}", 81, 100, a.AMB, "RTSP local :8554", 792, (Y + 120 + WY) / 2, still=0, anchor="start")
when(a, f'<circle cx="1030" cy="{WY + 42}" r="56" fill="none" stroke="{a.AMB}" stroke-width="10" stroke-dasharray="14 6"/>'
     + a.text(1030, WY + 40, "anillo", 15, a.AMB, a.MONO, 600, "middle") + a.text(1030, WY + 62, "~80 s", 16, a.AMB, a.MONO, 600, "middle")
     + a.arrow(f"M912 {WY + 42} H966", a.AMB, 3), 84, 100, still=0)

a.add(a.text(48, 640, "Una sola conexión a la cámara alimenta el vivo y el clip: si falta el stream en go2rtc.yaml, faltan los dos.", 16, a.TXT, a.SANS, 600))

out(a, 4, 1, "Un pedido de video, salto por salto",
    "Animación en cinco tiempos con cuatro cajas en fila: el navegador (Filas, Monitor), el proxy inverso que deriva /go2rtc/ al puerto 1984, go2rtc (API en el 1984 y RTSP en el 8554) y la cámara Bosch 192.0.2.10. "
    "Tiempo 1: el navegador pide GET /go2rtc/api/stream.mp4?src=bosch_192_0_2_10. "
    "Tiempo 2: el proxy inverso deriva /go2rtc/ al puerto 1984, la API de go2rtc. "
    "Tiempo 3: go2rtc busca en go2rtc.yaml el stream bosch_192_0_2_10 con su URL rtsp de la cámara y toma el RTSP. "
    "Tiempo 4: vuelven fragmentos de MP4 por HTTP hasta el navegador, que queda pegado al vivo; si el video falla hay reintentos y después una captura cada 5 segundos. "
    "Tiempo 5: dispatch-worker lee el mismo stream por el RTSP local del puerto 8554 para mantener un anillo de unos 80 segundos, del que sale el clip de cada alerta. "
    "Al pie: una sola conexión a la cámara alimenta el vivo y el clip; si falta el stream en go2rtc.yaml, faltan los dos.",
    [8, 30, 52, 72, 94])
