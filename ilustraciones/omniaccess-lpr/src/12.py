import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *


def box(c, x, y, w, h, t, kd="info", sub=None, size=17):
    c.add(panel(x, y, w, h, None, kd))
    lst, hh = wrap(x + w / 2, y + 30, t, w - 30, size, 600, INK, anchor="middle")
    c.add(lst)
    if sub:
        c.add(text(x + w / 2, y + 30 + hh + 4, sub, 14, 500, INK3, FM, anchor="middle"))


# ---------------------------------------------------------------- 12.svg: el árbol de "dejaron de entrar matrículas"
c = Canvas(K(), "«Dejaron de entrar matrículas»: seguí el árbol")
box(c, 420, 126, 360, 64, "¿Llegan eventos a Webhooks?", "soft")
box(c, 48, 250, 330, 90, "No llega nada", "alert", "red o receptor caído")
box(c, 435, 250, 330, 90, "Llegan sin matrícula", "warn", "la cámara no hace ANPR")
box(c, 822, 250, 330, 90, "Llegan, pero de una sola no", "info", "mirar esa cámara")
c.add(Arrow((470, 190), (213, 246), label="no", label_dy=-8))
c.add(Arrow((600, 190), (600, 246), bend="straight", label="sin chapa", label_dy=0))
c.add(Arrow((730, 190), (987, 246), label="una sola", label_dy=-8))
lists = [(48, ["ping al servidor", "receptor 10000/health → OK", "switch y enlace"]),
         (435, ["modo: roadDetection", "canal fuera de la búsqueda del NVR", "reiniciar y esperar 80 s"]),
         (822, ["estado y latencia", "HTTP host (reset)", "tasa de lectura por hora"])]
for x, items in lists:
    for k, s in enumerate(items):
        c.add(text(x + 18, 384 + k * 30, "· " + s, 16, 500, INK2, FB))
c.add(Note(48, 520, 1104, "Mientras se diagnostica, el control de accesos se hace a mano en la garita. La falla silenciosa (cámara con imagen que no lee) la avisa la alerta de ANPR apagado.", kind="warn", size=16))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso3: roadDetection contra smart
c = Canvas(K(3), "Un solo motor: lee patentes o alimenta la búsqueda del NVR")
c.add(panel(48, 130, 540, 250, "roadDetection", "ok", sub="VCAResource · lee matrículas"))
c.add(cam_icon(90, 250, 1.2))
c.add(plate(420, 220, "SBA 1234", w=170, size=24))
c.add(text(72, 350, "Los eventos llegan con matrícula.", 17, 600, OK, FB))
c.add(panel(612, 130, 540, 250, "smart", "alert", sub="la búsqueda por imagen del NVR la forzó"))
c.add(cam_icon(654, 250, 1.2))
c.add(plate(984, 220, "· · ·", w=170, size=24, stroke=ALERT))
c.add(text(636, 350, "Imagen sana, pero no lee: falla silenciosa.", 17, 600, ALERT, FB))
steps = ["Sacar el canal de la búsqueda por imagen del NVR", "Volver el recurso a roadDetection", "Reiniciar la cámara", "Esperar unos 80 s y mirar Webhooks"]
c.add(text(48, 428, "Para revertir, en este orden:", 18, 600, INK, FB))
for i, s in enumerate(steps):
    x = 48 + (i % 2) * 560
    y = 470 + (i // 2) * 60
    c.add(Step(x + 18, y, i + 1))
    c.add(text(x + 48, y + 6, s, 17, 500, INK, FB))
c.add(code(48, 592, 1104, "curl -s --digest -u integrador 192.0.2.21/ISAPI/System/Video/inputs/channels/1/VCAResource", size=15))
save(c, "12-paso3.svg")

# ---------------------------------------------------------------- 12-paso6: la alerta que se abre y se cierra
c = Canvas(K(6), "Desconectá la cámara de prueba y mirá la alerta")
pts = [(130, "cámara desconectada", "gray"), (420, "2 sondeos sin respuesta", "warn"), (720, "alerta · Sin respuesta", "alert"), (1020, "reconectada · normalizado", "ok")]
c.add(f'<path d="M100 300H1110" stroke="{INK3}" stroke-width="2"/>')
for x, t, kd in pts:
    c.add(f'<circle cx="{x}" cy="300" r="12" fill="{ {"gray": INK3, "warn": AMBER, "alert": ALERT, "ok": OK}[kd] }"/>')
    c.add(tag(x, 254, t, kd, size=15, anchor="middle"))
c.add(text(720, 350, "aviso por Telegram (cámaras LPR y NVR)", 15, 500, INK2, FM, anchor="middle"))
c.add(Table(48, 400, ["Alerta", "Se abre cuando"], [["Sin respuesta", "dos sondeos seguidos sin contestar"], ["Disco", "un disco del NVR no está OK"], ["Memoria", "uso sostenido arriba de 95 %"], ["Reloj", "más de 120 s contra el servidor"], ["ANPR apagado", "la cámara salió de roadDetection"]],
            [300, 804], row_h=38))
save(c, "12-paso6.svg")
