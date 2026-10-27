from _oai import *

# ---------- 7.svg: de dónde sale cada pestaña
c = Canvas("OmniAccess Intrusión · Lección 7", "Vivo, grabación y evidencia salen de lugares distintos")
cam = c.add(Generic(48, 150, "Cámara", "RTSP principal y sub", "camera", w=320))
nvr = c.add(Generic(48, 300, "NVR", "graba 24 h · H.264/H.265", "server", w=320))
s3 = c.add(Generic(48, 450, "Bucket intrusion", "foto de cada detección", "cloud", w=320))
g2 = c.add(Generic(440, 150, "go2rtc", "en el servidor OmniAccess", "server", w=340, dark=True))
pb = c.add(Generic(440, 300, "Reproducción NVR", "transcodifica si hace falta", "server", w=340, dark=True))
c.add(Arrow((372, 192), (434, 192), label="RTSP", kind="flow", label_dy=-12))
c.add(Arrow((372, 342), (434, 342), kind="flow"))
tabs = [("Vivo", "SD o HD · PTZ · seguimiento", 150), ("Grabación", "línea de tiempo · ×1 ×2 ×4 ×8", 300), ("Evidencia", "fotos de la cámara", 450)]
for t, d, y in tabs:
    c.add(panel(860, y, 292, 84, None, kind="info"))
    c.add(text(882, y + 36, t, 19, 600, INK, FD))
    c.add(text(882, y + 62, d, 14, 500, INK3, FM))
c.add(Arrow((784, 192), (854, 192), kind="flow"))
c.add(Arrow((784, 342), (854, 342), kind="flow"))
c.add(wire([(372, 492), (854, 492)], "flow", arrow=True))
c.add(Note(450, 560, 702, "Sin NVR y canal vinculados en Dispositivos, la pestaña Grabación no tiene qué pedir.", kind="warn", size=15))
save(c, "7.svg")

# ---------- 7-paso2.svg: seguimiento visual
c = Canvas("OmniAccess Intrusión · Lección 7 · Paso 2", "Poné la cámara vecina donde se pasa a ella")
c.add(frame(48, 140, 700, 420, "Perímetro Norte 12 · Vivo", night=False))
c.add(person(330, 470, 1.1))
c.add(f'<path d="M360 440Q520 380 600 330" stroke="{WARN}" stroke-width="3" stroke-dasharray="8 6" fill="none"/>')
c.add(f'<circle cx="640" cy="300" r="28" fill="{WARN}" stroke="{WHITE}" stroke-width="3"/>')
c.add(icon(626, 286, "camera", WHITE, 1.15, 2))
c.add(pill(640, 254, "Perímetro Sur 07", WARN, WHITE, 14, mono=False))
c.add(Step(600, 360, 2))
c.add(panel(790, 140, 362, 200, "Seguimiento visual", kind="warn", sub="lápiz del vivo"))
s, _ = bullet_list(810, 225, ["Agregar cámara: la vecina", "Arrastrá el ícono al punto de paso", "Tocá el ícono para seguir al intruso"], 320, 16, 12)
c.add(s)
c.add(Note(790, 360, 362, "Si la vecina tiene eventos, el ícono rebota en rojo.", kind="alert", size=15))
save(c, "7-paso2.svg")

# ---------- 7-paso5.svg: el clip
c = Canvas("OmniAccess Intrusión · Lección 7 · Paso 5", "El clip: 10 s antes y 10 s después del instante")
x0, x1, y = 120, 1080, 300
c.add(f'<rect x="{x0}" y="{y - 14}" width="{x1 - x0}" height="28" rx="14" fill="{SOFT}"/>')
mid = (x0 + x1) / 2
c.add(f'<rect x="{mid - 240}" y="{y - 14}" width="480" height="28" rx="8" fill="{CYAN}" opacity=".9"/>')
c.add(f'<path d="M{mid} {y - 50}V{y + 40}" stroke="{ALERT}" stroke-width="4"/>')
c.add(tag(mid, y - 62, "cruce 02:11:40", "alert", 15, anchor="middle"))
c.add(text(mid - 240, y + 52, "−10 s", 16, 600, INK2, FM, anchor="middle"))
c.add(text(mid + 240, y + 52, "+10 s", 16, 600, INK2, FM, anchor="middle"))
c.add(text(x0, y + 52, "grabación del NVR", 14, 500, INK3, FB))
c.add(button(330, 420, 240, "Descargar", "dark", 16, 46))
c.add(button(630, 420, 240, "Enviar por WhatsApp", "ok", 16, 46))
c.add(Step(300, 420, 5))
c.add(Note(120, 500, 960, "El clip sale con una intro; por WhatsApp va a destinatarios del Centro de Notificaciones o a un usuario, con un tope de segundos.", kind="info", size=15))
save(c, "7-paso5.svg")
