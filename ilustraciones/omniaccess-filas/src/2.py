from _fil import *

# ---------- 2.svg: ubicación de la cámara (de frente vs desde arriba)
c = Canvas("OmniAccess Filas · Lección 2", "Ubicá la cámara arriba de la fila, no de frente")
# panel izquierdo: de frente
c.add(panel(48, 130, 540, 400, "De frente, a la altura de la gente", kind="alert"))
c.add(line(70, 470, 566, 470, INK3, 2))
c.add(Camera(70, 230, "Cámara", "frontal", w=170, hl=ALERT))
for i, x in enumerate([300, 360, 420, 480, 540]):
    c.add(person(x, 438, BLUE if i == 0 else INK3, 16))
c.add(line(240, 272, 540, 410, ALERT, 2, dash="6 6"))
c.add(line(240, 272, 300, 400, ALERT, 2, dash="6 6"))
c.add(text(318, 500, "la primera tapa a las de atrás", 15, 600, ALERT, FM, anchor="middle"))
c.add(Mark(552, 166, ok=False))
# panel derecho: desde arriba
c.add(panel(612, 130, 540, 400, "Desde arriba, a más de 3 m", kind="ok"))
c.add(line(634, 470, 1130, 470, INK3, 2))
c.add(Camera(800, 190, "Cámara", "cenital", w=170, hl=OK))
for x in [700, 780, 860, 940, 1020]:
    c.add(person(x, 438, BLUE, 16))
c.add(poly([(885, 274), (680, 455), (1080, 455), (885, 274)], stroke=OK, fill=OK, sw=2, opacity=.15))
c.add(line(1110, 270, 1110, 462, OK, 2, arrow=True))
c.add(line(1110, 462, 1110, 270, OK, 2, arrow=True))
c.add(text(1100, 360, "> 3 m", 16, 600, OK, FM, anchor="end"))
c.add(text(720, 500, "se ve y se separa a cada persona", 15, 600, OK, FM))
c.add(Mark(1116, 166, ok=True))
c.add(Note(48, 552, 1104, "Según Bosch: más de 3 m de altura, nada que refleje, pasillos rectos, hasta 64 personas en escena. Un objeto tapado más del 50 % no se cuenta.", kind="info", size=15))
save(c, "2.svg")

# ---------- 2-paso3.svg: una zona, tres tareas, tres canales
c = Canvas("OmniAccess Filas · Lección 2 · Paso 3", "Una zona de fila, tres tareas, tres canales")
c.add(panel(48, 130, 520, 420, "Cámara · VCA → Tasks", kind="info", sub="IVA Pro Buildings"))
zone = [(110, 230), (500, 215), (520, 470), (90, 490)]
c.add(poly(zone + [zone[0]], stroke=CYAN, fill=CYAN, sw=3, opacity=.18))
c.add(poly(zone + [zone[0]], stroke=CYAN, sw=3))
for x, y in [(170, 330), (250, 380), (330, 340), (410, 400), (220, 440)]:
    c.add(head_top(x, y, BLUE, 13))
c.add(text(300, 270, "zona de la fila", 16, 600, CYAN, FM, anchor="middle"))
c.add(Step(48, 130, 3))
rows = [("Occupancy", "Aforo", "Aforo", OK), ("Entering field", "(libre)", "Entrada", BLUE), ("Leaving field", "(libre)", "Salida", BLUE)]
c.add(text(640, 158, "TAREA EN LA CÁMARA", 13, 600, INK3, FM, ls=1.2))
c.add(text(1000, 158, "CANAL EN OMNIACCESS", 13, 600, INK3, FM, ls=1.2))
for i, (tipo, nombre, canal, col) in enumerate(rows):
    y = 190 + i * 110
    c.add(rect(620, y, 300, 80, WHITE, col, 2.5 if i == 0 else 2))
    c.add(text(640, y + 34, tipo, 18, 600, INK))
    c.add(text(640, y + 60, "nombre: " + nombre, 15, 500, col if i == 0 else INK3, FM))
    c.add(Arrow((925, y + 40), (995, y + 40), kind="flow"))
    c.add(Chip(1000, y + 50, canal, "ok" if i == 0 else "blue"))
c.add(Note(620, 520, 532, "La tarea de ocupación se llama Aforo: la espera estimada, el reporte diario y el reseteo buscan ese canal.", kind="ok", size=15))
save(c, "2-paso3.svg")

# ---------- 2-paso7.svg: ONVIF y el usuario de OmniAccess
c = Canvas("OmniAccess Filas · Lección 2 · Paso 7", "ONVIF habilitado y un usuario para OmniAccess")
cam = c.add(Camera(48, 200, "Cámara Bosch", "192.0.2.10", w=260))
srv = c.add(Server(780, 200, "OmniAccess", "servidor de la fila", w=300))
c.add(Arrow(srv.left(-14), cam.right(-14), kind="flow", label="HTTPS · puerto 443", label_dy=-16))
c.add(Arrow(cam.right(14), srv.left(14), kind="logical", label="eventos ONVIF", label_dy=28))
c.add(Step(48, 200, 7))
c.add(Window(48, 360, 560, 220, "Ficha de la obra", rows=[("Cámara", "192.0.2.10"), ("Usuario", "omniaccess"), ("Clave", "Cambiar.2026"), ("Tareas", "Aforo · entrada · salida")], hl=1))
c.add(Note(640, 360, 512, "OmniAccess usa este usuario para leer eventos, sacar la foto de la alerta y, si sos administrador, escribir la analítica desde Calibración. La clave de ejemplo se cambia en obra.", title="Un usuario, varios usos", kind="info", size=15))
save(c, "2-paso7.svg")
