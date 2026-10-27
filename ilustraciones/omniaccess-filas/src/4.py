from _fil import *

# ---------- 4.svg: un stream, varios usos
c = Canvas("OmniAccess Filas · Lección 4", "Un stream en go2rtc: el vivo y el clip de la alerta")
cam = c.add(Camera(48, 250, "Cámara Bosch", "stream 2 · H.264", w=230))
g = c.add(Generic(400, 250, "go2rtc", "API 1984 · RTSP 8554", icon="server", w=280, dark=True))
nav = c.add(Generic(820, 130, "Navegador", "stream.mp4 por HTTP", icon="laptop", w=332))
wk = c.add(Generic(820, 370, "dispatch-worker", "RTSP local · 8554", icon="server", w=332))
c.add(Arrow(cam.right(), g.left(), label="RTSP", label_dy=-16))
c.add(Arrow(g.right(-14), nav.left(), kind="flow"))
c.add(Arrow(g.right(14), wk.left(), kind="flow"))
c.add(text(986, 246, "Filas · Monitor en Vivo · app", 15, 600, BLUE, FM, anchor="middle"))
c.add(Chip(540, 380, "bosch_192_0_2_10", "cyan", anchor="middle"))
c.add(text(540, 410, "una sola conexión a la cámara", 15, 500, INK3, FM, anchor="middle"))
c.add(text(986, 486, "anillo de ~80 s → clip de la alerta", 15, 600, BLUE, FM, anchor="middle"))
c.add(text(986, 508, "5 s antes · 3 s después", 15, 500, INK3, FM, anchor="middle"))
c.add(Note(48, 545, 1104, "Si el stream no existe o tiene otro nombre, no hay vivo ni clip: el monitor reintenta y pasa a mostrar una foto cada 5 s.", kind="warn", size=15))
save(c, "4.svg")

# ---------- 4-paso2.svg: cómo se arma el nombre del stream
c = Canvas("OmniAccess Filas · Lección 4 · Paso 2", "El nombre del stream sale de la IP de la cámara")
c.add(Chip(140, 190, "192.0.2.10", "blue", anchor="middle"))
c.add(Arrow((215, 181), (450, 181), kind="flow", label="puntos por guiones bajos", label_dy=-18))
c.add(Chip(560, 190, "bosch_192_0_2_10", "cyan", anchor="middle"))
c.add(Step(48, 150, 2))
c.add(text(48, 264, "go2rtc.yaml", 15, 600, INK3, FM, ls=1.2))
c.add(code(48, 280, 1104, "streams:", 16))
c.add(code(48, 328, 1104, "  bosch_192_0_2_10: rtsp://omniaccess:Cambiar.2026@192.0.2.10/rtsp_tunnel?p=1&line=1&inst=2&vcd=2", 15))
c.add(pill(210, 410, "nombre exacto", CYAN))
c.add(pill(735, 410, "rtsp_tunnel va antes del ?", BLUE))
c.add(pill(1040, 410, "inst=2 · stream 2", BLUE))
c.add(Note(48, 450, 540, "Un carácter distinto en el nombre y el panel no encuentra el video.", kind="warn", size=15))
c.add(Note(612, 450, 540, "La clave queda en texto en este archivo: lectura solo para el servicio.", kind="alert", size=15))
save(c, "4-paso2.svg")

# ---------- 4-paso6.svg: qué pasa cuando el stream falla
c = Canvas("OmniAccess Filas · Lección 4 · Paso 6", "Si el stream falla: reintentos y foto de respaldo")
seq = [("pide stream.mp4", "blue"), ("falla", "alert"), ("reintenta hasta 6 veces", "warn"), ("foto cada 5 s", "gray")]
xs = [150, 400, 680, 990]
for i, ((s_, k), x) in enumerate(zip(seq, xs)):
    c.add(Chip(x, 230, s_, k, anchor="middle"))
    if i < 3:
        w0 = len(s_) * 9.2 + 26
        w1 = len(seq[i + 1][0]) * 9.2 + 26
        c.add(Arrow((x + w0 / 2 + 8, 221), (xs[i + 1] - w1 / 2 - 10, 221), kind="flow"))
c.add(Step(48, 160, 6))
c.add(rect(360, 290, 480, 230, "#0B1A28", "#0B1A28", 2, rx=16))
c.add(text(600, 395, "Cámara offline", 22, 600, WHITE, FD, anchor="middle"))
c.add(text(600, 428, "Sin señal · reintentando…", 16, 500, "#9FC3E3", FM, anchor="middle"))
c.add(f'<circle cx="600" cy="345" r="9" fill="{ALERT}"/>')
c.add(Note(48, 550, 1104, "Para la prueba renombrá el stream y recargá Filas; al terminar, volvé el nombre a su lugar y reiniciá go2rtc.", kind="info", size=15))
save(c, "4-paso6.svg")
