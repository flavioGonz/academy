import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-lpr/src")
from _lpr import *

# ---------------------------------------------------------------- 10.svg: tres categorías y sus efectos
c = Canvas(K(), "Lista de vigilancia: tres categorías, tres efectos")
cats = [("Lista negra", "alert", ["Toda lectura queda Denegada.", "Rojo con sonido en el monitor.", "Pasa a la lista de bloqueo", "de las lectoras."], "SAB 2024"),
        ("VIP / Autorizado", "ok", ["Se destaca en verde.", "No cambia lo que decide", "la barrera.", ""], "SBA 1234"),
        ("En búsqueda", "warn", ["Avisa cuando aparece,", "sin bloquear.", "El motivo es obligatorio:", "lo ve el guardia en la captura."], "SCD 5678")]
for i, (t, kd, lines, pl) in enumerate(cats):
    x = 48 + i * 376
    c.add(panel(x, 130, 352, 320, t, kd, title_size=22))
    c.add(plate(x + 176, 182, pl, w=170, size=24))
    for k, ln in enumerate(lines):
        c.add(text(x + 22, 294 + k * 30, ln, 17, 500, INK, FB))
c.add(text(48, 496, "Se carga desde el escudo del Monitor LPR o con el botón Lista negra de la ficha.", 17, 500, INK, FB))
c.add(text(48, 528, "La matrícula va como la lee la cámara: SAB2024, sin espacios ni guiones.", 17, 500, INK2, FB))
c.add(text(48, 560, "Con Avisa manda Telegram al detectarla; En silencio, solo se ve en el monitor.", 17, 500, INK2, FB))
c.add(text(48, 606, "Un usuario con rol de bloqueado arrastra sus matrículas. La lista negra le gana a cualquier pase de invitado.", 16, 500, INK2, FB))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso4: verificar el recorte antes de actuar
c = Canvas(K(4), "Antes de actuar, compará el recorte con la lista")
c.add(panel(48, 130, 540, 380, "Coincide", "ok"))
c.add(text(72, 196, "recorte de la cámara", 15, 600, INK3, FM))
c.add(plate(318, 210, "SAB 2024", w=240, size=32))
c.add(text(72, 330, "en la lista de vigilancia", 15, 600, INK3, FM))
c.add(plate(318, 344, "SAB 2024", w=240, size=32))
c.add(text(72, 480, "Se sigue el protocolo del cliente.", 17, 600, OK, FB))
c.add(panel(612, 130, 540, 380, "No coincide", "alert"))
c.add(text(636, 196, "recorte de la cámara", 15, 600, INK3, FM))
c.add(plate(882, 210, "SAB 2924", w=240, size=32))
c.add(text(636, 330, "lectura que disparó la alerta", 15, 600, INK3, FM))
c.add(plate(882, 344, "SAB 2024", w=240, size=32))
c.add(f'<circle cx="911" cy="250" r="22" fill="none" stroke="{ALERT}" stroke-width="3"/>')
c.add(text(636, 480, "Un 9 leído como 0: no se actúa, se avisa.", 17, 600, ALERT, FB))
c.add(Note(48, 534, 1104, "En Roseville el 71 % de las alertas de vehículo buscado eran lecturas equivocadas; no hubo detenciones porque cada una se verificaba.", kind="info", size=16))
save(c, "10-paso4.svg")

# ---------------------------------------------------------------- 10-paso5: pasar a lista negra y leer las lectoras
c = Canvas(K(5), "Pasala a Lista negra y leé qué lectoras se actualizaron")
c.add(Window(48, 130, 430, 160, "Lista de vigilancia", rows=[("SAB2024", "En búsqueda"), ("¿Pasarla a Lista negra?", "Sí, cambiarla")], hl=1))
srv = c.add(Server(520, 250, "OmniAccess", "en todas las lectoras", w=260))
c.add(Arrow((478, 250), (516, 280)))
cams = [("P1 - Entrada (21)", "ok", "lista negra"), ("P2 - Salida (22)", "ok", "lista negra"), ("P3 - Servicio (23)", "alert", "no respondió")]
for i, (n, kd, st) in enumerate(cams):
    y = 140 + i * 130
    cam = c.add(Camera(900, y, n, "lectora LPR", w=252))
    c.add(Cable(srv.right(), cam.left(), kind=kd, label=st, label_at=0.55, label_dy=-10))
c.add(Note(48, 330, 430, "Si una lectora no respondió, la barrera la deniega igual por servidor. Conviene reintentar cuando vuelva.", kind="warn", size=16))
c.add(card(48, 520, 600, 104, "alert", "LISTA NEGRA · DENEGADA", "SAB 2024", "nueva lectura pasados 25 s, con sonido"))
save(c, "10-paso5.svg")
