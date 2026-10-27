import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

# ---------------------------------------------------------------- 8.svg: la ficha del evento
c = Canvas(K(), "La ficha del evento: seis acciones y tres pestañas")
c.add(f'<rect x="48" y="126" width="1104" height="520" rx="16" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(f'<rect x="68" y="146" width="470" height="300" rx="12" fill="#14222F"/>')
c.add(car_side(170, 400, w=270, color="#5B6F84"))
c.add(plate(303, 168, "SBA 1234", w=160, size=22))
chips = [("Dirección", "Salida"), ("Cámara", "P2 - Salida"), ("Permanencia", "2h 15m")]
for i, (k, v) in enumerate(chips):
    x = 68 + i * 160
    hl = k == "Permanencia"
    c.add(f'<rect x="{x}" y="462" width="150" height="70" rx="10" fill="{OK_BG if hl else GROUND}" stroke="{OK if hl else LINE2}" stroke-width="1.5"/>')
    c.add(text(x + 12, 488, k.upper(), 14, 700, OK if hl else INK3, FM))
    c.add(text(x + 12, 518, v, 17, 600, INK, FB))
c.add(text(68, 560, "Marca, color y tipo, debajo de la foto.", 15, 500, INK3, FB))
c.add(tag(570, 170, "AUTORIZADO", "ok", size=16))
acts = [("Grabación", "video del NVR en ese segundo"), ("Similares", "el mismo vehículo en otras cámaras"), ("Clip", "descargar o enviar"),
        ("Exportar", "ZIP con la evidencia"), ("Registrar", "alta con la matrícula"), ("Lista negra", "marca la matrícula")]
for i, (a, d) in enumerate(acts):
    x = 570 + (i % 3) * 192
    y = 200 + (i // 3) * 92
    c.add(f'<rect x="{x}" y="{y}" width="180" height="80" rx="12" fill="{SOFT if a != "Lista negra" else ALERT_BG}" stroke="{BLUE if a != "Lista negra" else ALERT}" stroke-width="1.5"/>')
    c.add(text(x + 14, y + 30, a, 17, 700, BLUE if a != "Lista negra" else ALERT, FB))
    lst, _ = wrap(x + 14, y + 54, d, 160, 14, 400, INK2)
    c.add(lst)
for i, t in enumerate(["Perfil", "Historial", "Datos"]):
    x = 570 + i * 130
    c.add(f'<rect x="{x}" y="398" width="120" height="36" rx="10" fill="{DEEP if i == 0 else WHITE}" stroke="{DEEP if i == 0 else LINE2}" stroke-width="1.5"/>')
    c.add(text(x + 60, 422, t, 16, 600, WHITE if i == 0 else INK2, FB, anchor="middle"))
vals = [2, 2, 3, 2, 2, 0, 1, 2, 2, 3, 2, 2, 1, 0, 2, 2, 2, 3, 2, 2, 0, 1, 2, 2, 2, 3, 2, 2, 1, 2]
for i, v in enumerate(vals):
    c.add(f'<rect x="{570 + i * 11}" y="{520 - v * 18}" width="8" height="{v * 18}" rx="2" fill="{CYAN}"/>')
c.add(text(570, 548, "pasadas por día, últimos 30 días", 15, 500, INK3, FM))
c.add(text(920, 470, "Cámaras habituales", 16, 600, INK, FB))
c.add(text(920, 496, "P1 entra · P2 sale", 15, 500, INK2, FM))
c.add(text(920, 530, "Horarios habituales", 16, 600, INK, FB))
c.add(text(920, 556, "entra 07-09 · sale 18-20", 15, 500, INK2, FM))
c.add(text(570, 610, "Pregunta que responde: ¿es habitual o es la primera vez?", 17, 600, INK, FB))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso6: qué trae el ZIP
c = Canvas(K(6), "Exportar arma un ZIP con cuatro archivos")
files = [("captura.jpg", "la foto completa de la escena", "camera"), ("recorte_matricula.jpg", "el acercamiento de la patente", "card"),
         ("clip_30s.mp4", "video del NVR alrededor del evento", "server"), ("evento.json", "hora, cámara, vehículo y decisión", "check")]
for i, (f, d, ic) in enumerate(files):
    x = 48 + (i % 2) * 560
    y = 140 + (i // 2) * 150
    c.add(panel(x, y, 544, 128, None, "info"))
    c.add(icon(x + 24, y + 40, ic, BLUE, 1.6))
    c.add(text(x + 80, y + 56, f, 21, 700, INK, FM))
    c.add(text(x + 80, y + 88, d, 17, 500, INK2, FB))
c.add(Note(48, 460, 1104, "Tarda 5 a 15 segundos porque le pide el video al NVR en el momento. Sin canal de NVR, el ZIP sale sin clip.", kind="info", size=16))
c.add(Note(48, 552, 1104, "Tiene datos personales: se entrega solo a quien el cliente autoriza.", kind="warn", size=16))
save(c, "8-paso6.svg")

# ---------------------------------------------------------------- 8-paso7: el reclamo "no me abrió"
c = Canvas(K(7), "Reclamo «no me abrió»: dos caminos según haya evento")
start = c.add(Generic(430, 130, "Buscar la matrícula", "a la hora del reclamo", icon="key", w=340))
a = c.add(panel(48, 300, 520, 210, "Hay evento Denegado", "warn"))
b = c.add(panel(632, 300, 520, 210, "No hay evento", "info"))
c.add(Arrow((500, 214), (300, 296), label="hay evento", label_dy=-10))
c.add(Arrow((700, 214), (900, 296), label="no hay", label_dy=-10))
for i, s in enumerate(["La matrícula no está en el padrón,", "está mal cargada o suspendida.", "Revisar usuario, credencial y grupo.", "Exportar el ZIP para la respuesta."]):
    c.add(text(72, 372 + i * 34, s, 17, 500, INK, FB))
for i, s in enumerate(["La cámara no lo leyó.", "Mirar la grabación de esa hora", "para confirmar que pasó.", "Revisar esa cámara en Dispositivos."]):
    c.add(text(656, 372 + i * 34, s, 17, 500, INK, FB))
c.add(text(48, 560, "Matrícula de prueba para practicar: SBA1234. En un barrio real, primero el recorte y la grabación; después la respuesta.", 16, 500, INK2, FB))
save(c, "8-paso7.svg")
