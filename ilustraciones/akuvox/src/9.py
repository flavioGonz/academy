from _akv import *

# ---------- 9.svg: tres accesos al video
c = Canvas("Akuvox · Lección 9", "Del portero al NVR: qué stream va a dónde")
it = c.add(Intercom(60, 160, "Portero", "192.168.88.21"))
rows = [("rtsp://IP/live/ch00_0", "principal · 2048 kbps", "NVR: grabar con detalle", "camera", BLUE),
        ("rtsp://IP/live/ch00_1", "secundario · 512 kbps", "NVR: grilla y grabación", "camera", OK),
        ("http://IP/onvif/device_service", "ONVIF · alta en el NVR", "NVR: lo descubre solo", "server", BLUE),
        ("http://IP:8080/video.cgi", "MJPEG · puerto 8080", "MJPEG Authorization: activala", "lock", WARN)]
for i, (url, tag, dest, ic, col) in enumerate(rows):
    y = 150 + i * 110
    c.add(Cable((214, 290), (290, y + 36), kind="flow" if col != WARN else "logical", arrow=False))
    c.add(code(290, y + 14, 380, url, 15))
    c.add(text(300, y + 80, tag, 15, 600, col if col != BLUE else INK2, FM))
    c.add(Arrow((676, y + 34), (760, y + 34), kind="ok" if col == OK else "flow"))
    c.add(Generic(766, y, dest.split(": ")[0], dest.split(": ")[1], icon=ic, w=386, hl=OK if col == OK else None))
c.add(Chip(60, 630, "H.264 · 25 fps", "gray"))
c.add(Chip(260, 630, "RTSP, ONVIF y MJPEG: cada uno con usuario propio, ninguno admin / admin", "warn", mono=False))
save(c, "9.svg")

# ---------- 9-paso2.svg: RTSP con Digest
c = Canvas("Akuvox · Lección 9 · Paso 2", "Ponele usuario y clave propios al RTSP")
c.add(Window(48, 140, 560, 290, "Web del portero", path="Surveillance > RTSP > RTSP Basic",
             rows=[("RTSP Authorization", "activada"), ("Authorization Mode", "Digest"), ("Username", "nvr-lab"), ("Password", "Ejemplo-Rtsp-2026")], hl=1))
c.add(Step(48, 140, 2))
c.add(Terminal(650, 140, 502, [("# antes (paso 1): entra cualquiera", "#7FA6C9"), "ffprobe \"rtsp://192.168.88.21/live/ch00_1\"", ("# después (paso 3): con credencial", "#7FA6C9"), "ffprobe \"rtsp://nvr-lab:…@192.168.88.21/live/ch00_1\"", ("# … = Ejemplo-Rtsp-2026", "#7FA6C9")], title="PC DE LABORATORIO"))
c.add(Note(48, 470, 560, "Digest no manda la clave en claro por la red: el NVR prueba que la conoce sin mostrarla.", title="Por qué Digest", kind="ok", size=15))
c.add(Note(650, 470, 502, "Si un monitor mira este portero por RTSP, cargale el mismo usuario en Device > Monitor (paso 7).", kind="warn", size=15))
save(c, "9-paso2.svg")

# ---------- 9-paso5.svg: alta en el NVR
c = Canvas("Akuvox · Lección 9 · Paso 5", "Sumá el portero al NVR como una cámara más")
c.add(panel(48, 140, 520, 250, "Opción A · ONVIF", "info"))
c.add(code(70, 200, 476, "http://192.168.88.21/onvif/device_service", 15))
svg, _ = bullet_list(74, 284, ["Discoverable activado en Surveillance > ONVIF", "Usuario ONVIF propio, no admin / admin"], 470, 15)
c.add(svg)
c.add(panel(48, 410, 520, 200, "Opción B · RTSP manual", "info"))
c.add(code(70, 466, 476, "rtsp://nvr-lab:…@192.168.88.21/live/ch00_1", 15))
c.add(text(74, 540, "ruta ch00_1 para la grilla", 15, 500, INK3, FM))
c.add(text(74, 566, "… = clave del usuario nvr-lab", 15, 500, INK3, FM))
# NVR con grilla
c.add(f'<rect x="640" y="140" width="512" height="360" rx="18" fill="{DEEP}"/>')
c.add(text(664, 176, "NVR · vista en vivo", 17, 600, WHITE, FB))
for r in range(2):
    for k in range(3):
        x, y = 664 + k * 160, 196 + r * 140
        hl = r == 0 and k == 0
        c.add(f'<rect x="{x}" y="{y}" width="148" height="126" rx="8" fill="{"#0B3A66" if hl else "#0B1A28"}" stroke="{CYAN if hl else "#2C4A66"}" stroke-width="{3 if hl else 1}"/>')
c.add(text(738, 256, "Portero", 16, 600, WHITE, FB, anchor="middle"))
c.add(text(738, 280, "ch00_1", 15, 600, CYAN, FM, anchor="middle"))
c.add(Arrow((572, 260), (636, 260)))
c.add(Arrow((572, 486), (636, 450), bend="straight"))
c.add(Step(48, 140, 5))
c.add(Note(640, 525, 512, "En la grilla alcanza el secundario (512 kbps). El principal, si hace falta ver detalle.", kind="info", size=15))
save(c, "9-paso5.svg")
