import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

PASOS = ["Tipo", "Equipo", "Conexión", "Ubicación", "Grabación", "Puesta a punto"]

# ---------------------------------------------------------------- 4.svg: el alta guiada
c = Canvas(K(), "Dispositivos → Agregar → Cámara LPR, paso por paso")
bw, gap = 170, 16
for i, p in enumerate(PASOS):
    x = 48 + i * (bw + gap)
    hl = p in ("Ubicación", "Puesta a punto")
    c.add(f'<rect x="{x}" y="138" width="{bw}" height="58" rx="14" fill="{DEEP if hl else WHITE}" stroke="{DEEP if hl else LINE2}" stroke-width="2"/>')
    c.add(text(x + 18, 174, f"{i + 1}. {p}", 17, 600, WHITE if hl else INK, FB))
    if i:
        c.add(f'<path d="M{x - gap + 2} 167H{x - 3}" stroke="{INK3}" stroke-width="2"/>')
c.add(panel(48, 228, 540, 330, "Ubicación decide", "info"))
c.add(panel(72, 280, 236, 150, None, "soft"))
c.add(text(92, 314, "Entrada", 20, 700, BLUE, FD))
lst, _ = wrap(92, 344, "columna Entradas; suma a los que están adentro", 200, 16, 400, INK2)
c.add(lst)
c.add(panel(328, 280, 236, 150, None, "soft"))
c.add(text(348, 314, "Salida", 20, 700, BLUE, FD))
lst, _ = wrap(348, 344, "columna Salidas; permanencia; cierra visitas", 200, 16, 400, INK2)
c.add(lst)
c.add(Note(72, 448, 492, "Sin grupo de acceso la cámara no deja pasar a nadie por servidor.", kind="warn", size=16))
c.add(panel(612, 228, 540, 330, "Puesta a punto (ISAPI)", "dark"))
tareas = ["Dar de alta la cámara", "Poner la hora", "Servidor de alarmas → OmniAccess", "Modo ANPR", "Video H.264", "Video en vivo", "Cargar matrículas", "Vincular la grabación", "Calcular retención"]
for i, t in enumerate(tareas):
    y = 296 + i * 28
    c.add(f'<circle cx="644" cy="{y - 5}" r="5" fill="{CYAN}"/>')
    c.add(text(660, y, t, 16, 500, WHITE, FB))
c.add(text(48, 600, "Nombre con la convención del manual:", 17, 500, INK2, FB))
c.add(pill(470, 601, "P1 - Entrada (21)", fg=BLUE, size=16))
c.add(text(600, 600, "acceso · sentido · último octeto de la IP", 16, 500, INK3, FM))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso6: leer el resultado de la puesta a punto
c = Canvas(K(6), "Leé cada tarea de la puesta a punto")
rows = [
    ("Dar de alta la cámara", "ok", "P1 - Entrada (21) · 192.0.2.21"),
    ("Poner la hora", "ok", "hora del servidor"),
    ("Servidor de alarmas → OmniAccess", "ok", "192.0.2.10:10000/api/webhooks/hikvision"),
    ("Modo ANPR", "alert", "está en 'smart': pasala a roadDetection"),
    ("Video H.264", "ok", "canales 101 y 102"),
    ("Video en vivo", "ok", "stream registrado"),
    ("Cargar matrículas", "ok", "+120 agregadas"),
    ("Vincular la grabación", "ok", "NVR de prueba · canal 3"),
    ("Calcular retención", "ok", "el canal guarda 31 días"),
]
for i, (t, kd, det) in enumerate(rows):
    y = 150 + i * 46
    c.add(f'<rect x="48" y="{y - 26}" width="1104" height="40" rx="10" fill="{WHITE if kd != "alert" else ALERT_BG}" stroke="{LINE if kd != "alert" else ALERT}" stroke-width="1.5"/>')
    c.add(text(68, y, t, 17, 600, INK, FB))
    c.add(tag(440, y + 2, {"ok": "ok", "alert": "error", "gray": "salteado"}[kd], kd, size=15))
    c.add(text(580, y, det, 16, 500, INK2 if kd != "alert" else ALERT, FM))
c.add(text(48, 598, "Sin NVR, Vincular la grabación y Calcular retención quedan salteadas. Error en Modo ANPR: se resuelve con el árbol de diagnóstico.", 16, 500, INK2, FB))
save(c, "4-paso6.svg")

# ---------------------------------------------------------------- 4-paso7: el HTTP host y el primer evento
c = Canvas(K(7), "Pasá un auto y mirá llegar el primer evento")
cam = c.add(Camera(48, 150, "P1 - Entrada (21)", "192.0.2.21", w=300))
c.add(codebox(48, 270, 380, ["HTTP host (servidor de alarmas)", "IP     192.0.2.10", "puerto 10000", "ruta   /api/webhooks/hikvision", "formato XML · sin autenticación"], size=15, title="LO QUE DEJÓ LA PUESTA A PUNTO")[0])
srv = c.add(Server(470, 150, "Servidor OmniAccess", "192.0.2.10:10000", w=290))
c.add(Arrow(cam.right(), srv.left(), label="POST", label_dy=-14))
w = c.add(Window(800, 140, 352, 150, "Webhooks", path="Configuración → Sistema", rows=[("P1 - Entrada (21)", "SBA1234")], hl=0))
c.add(Arrow(srv.right(), (w.x - 4, srv.y + srv.h / 2), bend="straight"))
c.add(Note(470, 330, 682, "Llega con el nombre de la cámara: el servidor la reconoce primero por la MAC que viene en el XML y después por la IP.", kind="ok", size=16))
c.add(Note(470, 450, 682, "Tras un reset de fábrica la cámara pierde el HTTP host y deja de reportar: se repite la puesta a punto desde la ficha del equipo.", kind="warn", size=16))
save(c, "4-paso7.svg")
