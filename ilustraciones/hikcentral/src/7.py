import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 7.svg: graba en el sitio o en el centro
c = Canvas(K(), "Cada cámara graba en el sitio o en el centro")
c.add(Zone(48, 140, 420, 360, "SUCURSAL"))
cam = c.add(Camera(78, 180, "CAM-01", "alta por IP", w=200))
nvr = c.add(Generic(78, 330, "NVR del sitio", "graba en el equipo", icon="server", w=360, hl=OK))
c.add(Cable(cam.bottom(), (cam.bottom()[0], 330), kind="data"))
c.add(text(78, 470, "No depende del enlace al centro.", 16, 500, OK))
c.add(Zone(732, 140, 420, 360, "CENTRO"))
sto = [("pStor", "servicio que administra discos de un servidor"), ("pStor Cluster", "varios pStor juntos"),
       ("Hybrid SAN", "equipo de almacenamiento de Hikvision"), ("Cloud Storage Server", "servidor de almacenamiento")]
for i, (t, d) in enumerate(sto):
    y = 176 + i * 74
    c.add(rect(762, y, 360, 62, WHITE, LINE2, rx=12))
    c.add(text(782, y + 27, t, 17, 600, INK))
    c.add(text(782, y + 50, d, 15, 400, INK3))
c.add(Cable((468, 220), (732, 220), kind="data", label="enlace al centro"))
c.add(text(498, 268, "El video viaja por el enlace:", 15, 500, INK2))
c.add(text(498, 292, "si es chico o inestable,", 15, 500, INK2))
c.add(text(498, 316, "mejor en el sitio.", 15, 500, INK2))
c.add(Note(48, 528, 540, "Por dominio o Hik-Connect no se graba en Hybrid SAN ni en Cloud Storage. pStor Cluster no hace grabación por movimiento.", title="Límites que deciden", kind="warn"))
c.add(Note(612, 528, 540, "Se decide por cámara, por escrito, antes del alta. Cambiarla después no mueve el video viejo.", title="Regla", kind="info"))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso2: revisar cada fila contra los límites
c = Canvas(K(2), "Revisá cada fila de la tabla contra los límites")
c.add(Table(48, 124, ["Cámara", "Alta por", "Graba en", "Chequeo"], [
    ["CAM-01", "IP", "NVR sitio", "válido"],
    ["CAM-02", "ISUP", "NVR sitio", "válido"],
    ["CAM-09", "IP", "pStor central", "válido"],
    ["CAM-05", "Hik-Connect", "Hybrid SAN", "no se soporta"],
], [200, 260, 300, 344], hl_row=3, row_h=56, mono_cols=(0, 1)))
for i in range(4):
    c.add(Mark(1110, 124 + 56 * (i + 1) + 28, i < 3))
c.add(text(48, 440, "CAM-05 es una fila de ejemplo que no pasa el chequeo.", 16, 400, INK3))
c.add(Note(48, 470, 540, "Si la columna Alta por dice dominio o Hik-Connect, la columna Graba en no puede decir Hybrid SAN ni Cloud Storage.", title="La regla del chequeo", kind="alert"))
c.add(Note(612, 470, 540, "O cambiás el alta a IP o ISUP, o la cámara graba en el NVR del sitio. Por dominio, solo graba en el propio equipo.", title="Cómo se arregla", kind="ok"))
save(c, "7-paso2.svg")

# ---------------------------------------------------------------- 7-paso3: tomar el calendario del NVR
c = Canvas(K(3), "Tomá el calendario que ya tiene el NVR")
n = c.add(Generic(48, 150, "NVR del sitio", "ya tiene su calendario", icon="server", w=330))
h = c.add(Generic(822, 150, "HikCentral", "configuración de grabación", icon="server", w=330, dark=True))
c.add(Arrow(n.right(), h.left(), kind="ok", label="Get Device's Recording Settings"))
days = ["L", "M", "X", "J", "V", "S", "D"]
for k, (x0, title, kd) in enumerate([(48, "Calendario del NVR", "ok"), (612, "Lo que queda en HikCentral", "ok")]):
    c.add(panel(x0, 270, 540, 230, title, kd))
    for j, dd in enumerate(days):
        y = 318 + j * 24
        c.add(text(x0 + 24, y + 15, dd, 14, 600, INK3, FM))
        c.add(rect(x0 + 52, y + 2, 460, 16, WHITE, LINE2, rx=4, sw=1))
        w = 460 if j >= 5 else 460 * 0.55
        c.add(rect(x0 + 52 if j < 5 else x0 + 52, y + 2, w, 16, OK, OK, rx=4, sw=1, op=0.55))
c.add(text(48, 538, "Los dos calendarios son de ejemplo: lo importante es que el de HikCentral copia al del NVR.", 16, 400, INK3))
c.add(Note(48, 566, 1104, "Sin esa opción, una plantilla de la plataforma puede pisar el calendario que el NVR ya tenía armado.", kind="warn"))
save(c, "7-paso3.svg")
