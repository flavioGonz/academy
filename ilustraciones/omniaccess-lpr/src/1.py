import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

# ---------------------------------------------------------------- 1.svg: el recorrido de una lectura
c = Canvas(K(), "Así viaja una patente de la cámara al guardia")
c.add(Zone(30, 140, 906, 360, "Predio · red local", color=INK3))
cam = c.add(Camera(48, 190, "Cámara ANPR", "lee a bordo", w=210))
srv = c.add(Server(372, 190, "Servidor OmniAccess", "decide · puerto 10000", w=262))
mon = c.add(Generic(700, 190, "Monitor LPR", "en vivo, 1 a 3 s", icon="laptop", w=222))
nvr = c.add(Generic(48, 380, "NVR", "graba 24/7", icon="server", w=210))
db = c.add(Generic(372, 380, "Base y fotos", "PostgreSQL · MinIO", icon="server", w=262))
c.add(Arrow(cam.right(), srv.left(), label="HTTP", label_dy=-14))
c.add(text((cam.x + cam.w + srv.x) / 2, 258, "XML + fotos", 15, 500, INK2, FM, anchor="middle"))
c.add(Arrow(srv.right(), mon.left()))
c.add(Arrow(srv.bottom(), db.top(), label="evento y foto", label_dy=0, bend="straight"))
c.add(Cable(cam.bottom(), nvr.top(), kind="data", label="RTSP", label_dy=0))
c.add(Arrow(nvr.right(), db.left(), kind="logical", label="clip", label_dy=-14))
for n, (x, y) in enumerate([(cam.x + 18, cam.y - 2), ((cam.x + cam.w + srv.x) / 2, 292), (srv.x + 18, srv.y - 2), (db.x + db.w + 22, db.y + 16), (mon.x + 18, mon.y - 2)], 1):
    c.add(Step(x, y, n))
net = c.add(Internet(968, 190, "Internet", "opcional", w=196))
c.add(wire([(srv.x + 210, srv.y), (srv.x + 210, 160), (net.x + 98, 160), (net.x + 98, net.y - 4)], kind="logical"))
c.add(pill(820, 166, "solo avisos", fg=INK3, bg=GROUND))
c.add(Note(968, 300, 196, "Sin enlace se sigue leyendo, decidiendo y grabando.", kind="ok", size=15))
c.add(Note(30, 528, 1134, "1 cámara · 2 red · 3 servidor que decide · 4 base y fotos · 5 monitor. Cuando algo falla, primero se ubica el tramo.", title="Cinco tramos", kind="info", size=16))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso2: Webhooks abierto mientras pasa el auto
c = Canvas(K(2), "Dejá Webhooks abierto y mirá llegar el evento")
w = c.add(Window(48, 132, 660, 256, "OmniAccess · Webhooks", path="Configuración → Sistema → Webhooks",
                 rows=[("hikvision · P1 - Entrada (21)", "SBA1234"), ("hikvision · P1 - Entrada (21)", "SCD5678"), ("hikvision · P2 - Salida (22)", "SAB2024"), ("hikvision · P1 - Entrada (21)", "NO_LEIDA")], hl=0))
cam = c.add(Camera(820, 150, "P1 - Entrada (21)", "192.0.2.21", w=300))
c.add(Arrow(cam.left(), (w.x + w.w + 6, w.y + 120), label="cada lectura", label_dy=-14))
c.add(codebox(820, 290, 330, ["192.0.2.10:10000/health", ("OK", "#7EE2B8")], title="PASO 1 · RECEPTOR")[0])
c.add(Note(48, 420, 660, "Si el evento aparece acá, la cámara y la red están bien. Si no aparece, el problema está antes del servidor: cámara o red.", title="Qué te dice esta pantalla", kind="info", size=16))
c.add(Note(820, 420, 330, "NO_LEIDA también llega: la cámara vio un auto pero no leyó la chapa.", kind="warn", size=15))
save(c, "1-paso2.svg")
