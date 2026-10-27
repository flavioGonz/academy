from _oai import *

# ---------- 1.svg: el camino de una detección
c = Canvas("OmniAccess Intrusión · Lección 1", "Así viaja un cruce hasta el monitor")
cam = c.add(Generic(48, 160, "Cámara Hikvision", "detecta el cruce", "camera", w=260))
nvr = c.add(Generic(48, 400, "NVR Dahua", "eventManager", "server", w=260))
c.add(panel(430, 140, 360, 330, "Servidor OmniAccess", kind="soft", sub="192.0.2.10"))
items = [("1", "webhooks en el puerto 10000"), ("2", "guarda la detección"), ("3", "pide la foto a la cámara"), ("4", "foto al bucket intrusion"), ("5", "avisa a las pantallas")]
for i, (n, s) in enumerate(items):
    y = 230 + i * 46
    c.add(f'<circle cx="465" cy="{y - 6}" r="13" fill="{CYAN}"/>')
    c.add(text(465, y - 1, n, 14, 700, WHITE, FD, anchor="middle"))
    c.add(text(490, y, s, 17, 500, INK))
mon = c.add(Generic(900, 200, "Monitor Intrusión", "canal en rojo", "laptop", w=252))
c.add(Generic(900, 330, "Mapa y pared", "suena y titila", "bell", w=252))
c.add(Arrow((cam.x + cam.w + 6, cam.y + 42), (424, 222), label="push HTTP", kind="flow", label_dy=-14))
c.add(wire([(424, 430), (360, 430), (360, 442), (nvr.x + nvr.w + 8, 442)], "logical", arrow=True))
c.add(text(368, 416, "suscribe", 15, 600, INK3, FM, anchor="middle"))
c.add(Arrow((796, 250), (894, 242), kind="flow"))
c.add(Arrow((796, 330), (894, 372), kind="flow"))
c.add(Note(48, 520, 520, "El movimiento simple (VMD) se descarta al llegar: no se guarda ni se muestra.", kind="warn", size=16))
c.add(Note(600, 520, 552, "En esta versión no entra ninguna intrusión por ONVIF.", kind="info", size=16))
save(c, "1.svg")

# ---------- 1-paso3.svg: quién detecta y por dónde avisa
c = Canvas("OmniAccess Intrusión · Lección 1 · Paso 3", "Anotá quién detecta y por dónde avisa")
rows = [("Hikvision directa o en NVR Hikvision", "la cámara", "push al servidor de alarma :10000", "ok"),
        ("Cualquier marca en NVR Dahua", "el NVR Dahua", "OmniAccess se suscribe al NVR", "ok"),
        ("Dahua en NVR Hikvision", "nadie avisa", "sin vía: configurar en la cámara o pasarla a un NVR Dahua", "alert")]
c.add(text(48, 150, "CÁMARA", 13, 600, INK3, FM, ls=1.2))
c.add(text(470, 150, "DETECTA", 13, 600, INK3, FM, ls=1.2))
c.add(text(690, 150, "CÓMO LLEGA A OMNIACCESS", 13, 600, INK3, FM, ls=1.2))
for i, (a, b, v, kd) in enumerate(rows):
    y = 170 + i * 118
    bg, fg = KC[kd]
    c.add(f'<rect x="48" y="{y}" width="1104" height="100" rx="16" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
    c.add(f'<rect x="48" y="{y + 14}" width="6" height="72" rx="3" fill="{fg}"/>')
    t1, h1 = wrap(72, y + 44, a, 370, 18, 600, INK)
    if h1 < 30:
        t1, _ = wrap(72, y + 56, a, 370, 18, 600, INK)
    c.add(t1)
    c.add(text(470, y + 56, b, 17, 600, fg if kd == "alert" else INK2))
    t2, h2 = wrap(690, y + 44, v, 400, 17, 500, INK2)
    if h2 < 30:
        t2, _ = wrap(690, y + 56, v, 400, 17, 500, INK2)
    c.add(t2)
    c.add(Mark(1118, y + 50, ok=(kd == "ok")))
c.add(Note(48, 540, 1104, "La marca de la cámara sola no alcanza: importa quién la graba. El NVR Hikvision no analiza canales de otra marca.", kind="info", size=16))
save(c, "1-paso3.svg")
