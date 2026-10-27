import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 11.svg: anatomía de un rol
c = Canvas(K(), "Un rol a medida: qué, dónde y cuándo puede cada usuario")
c.add(panel(48, 124, 300, 236, "Roles fijos", "gray"))
c.add(tag(72, 200, "Administrator", "dark", 15, True, anchor="start"))
c.add(text(72, 232, "todos los permisos", 15, 400, INK2))
c.add(tag(72, 284, "Operator", "dark", 15, True, anchor="start"))
c.add(text(72, 316, "recursos y aplicaciones", 15, 400, INK2))
c.add(text(72, 346, "No se editan ni se borran.", 15, 600, INK3))
c.add(panel(372, 124, 520, 400, "Rol a medida: Guardia", "info"))
rows = [("Vigencia", "hoy a fin de año"), ("Horario de permisos", "todos los días 19:00 a 07:00"), ("Áreas visibles", "solo Depósito"), ("Recursos", "vivo y reproducción de Depósito")]
for i, (k, v) in enumerate(rows):
    y = 182 + i * 64
    c.add(rect(396, y, 472, 52, WHITE, LINE2, rx=10))
    c.add(text(414, y + 32, k, 16, 600, INK))
    c.add(text(850, y + 32, v, 15, 500, BLUE, FM, anchor="end"))
u = c.add(Person(916, 230, "guardia.lab", "rol Guardia", w=236))
c.add(Arrow((892, 272), u.left()))
c.add(Note(916, 352, 236, "Rol vencido o fuera de horario: el usuario es expulsado.", kind="warn", size=15))
c.add(Note(48, 384, 300, "Contraseña mínima: subila de Medium a Strong.", title="Endurecer", kind="info", size=15))
c.add(text(48, 580, "Cada persona su usuario, cada usuario el rol mínimo.", 18, 600, BLUE, FD))
c.add(text(48, 616, "Datos del rol de ejemplo del laboratorio. Ruta en V2.x: Account and Security > Roles.", 16, 400, INK3))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso4: dentro y fuera del horario del rol
c = Canvas(K(4), "Entrá con guardia.lab dentro y fuera del horario")
for i, (hora, ok) in enumerate([("22:00", True), ("10:00", False)]):
    x = 48 + i * 564
    c.add(panel(x, 124, 540, 380, f"A las {hora}: " + ("dentro del horario" if ok else "fuera del horario"), "ok" if ok else "alert"))
    if ok:
        c.add(rect(x + 24, 176, 492, 52, WHITE, LINE2, rx=10))
        c.add(text(x + 44, 208, "Áreas: Depósito", 16, 600, INK, FM))
        for k in range(4):
            c.add(rect(x + 24 + (k % 2) * 250, 244 + (k // 2) * 88, 242, 78, DEEP, DEEP, rx=8))
            c.add(mid(x + 24 + (k % 2) * 250 + 121, 290 + (k // 2) * 88, f"vivo CAM-0{k + 1}", 15, 600, "#9FC3E3", FM))
        c.add(text(x + 24, 464, "Ve solo lo de Depósito: el resto de las", 16, 400, INK2))
        c.add(text(x + 24, 488, "áreas no existe para este usuario.", 16, 400, INK2))
    else:
        c.add(rect(x + 24, 176, 492, 220, WHITE, ALERT, rx=12, dash="6 5"))
        c.add(Mark(x + 270, 244, False))
        c.add(mid(x + 270, 310, "No puede iniciar sesión", 19, 600, ALERT))
        c.add(mid(x + 270, 344, "y si estaba adentro, lo expulsa", 16, 400, INK2))
        c.add(text(x + 24, 464, "Lo mismo pasa cuando vence la vigencia:", 16, 400, INK2))
        c.add(text(x + 24, 488, "útil para contratistas y turnos.", 16, 400, INK2))
c.add(Note(48, 528, 1104, "Horario del rol Guardia del laboratorio: todos los días de 19:00 a 07:00. Las horas de la prueba son de ejemplo.", kind="info"))
save(c, "11-paso4.svg")

# ---------------------------------------------------------------- 11-paso5: armar el .pem
c = Canvas(K(5), "HTTPS propio: certificado y clave en un .pem")
a = c.add(Generic(48, 150, "certificado.crt", "firmado por una CA", icon="shield", w=300))
b = c.add(Generic(48, 270, "clave privada", "exportada en texto", icon="key", w=300))
c.add(codebox(436, 136, 400, ["-----BEGIN CERTIFICATE-----", ("(contenido del .crt)", "#9FC3E3"), "-----END CERTIFICATE-----", "-----BEGIN PRIVATE KEY-----", ("(clave privada exportada)", "#9FC3E3"), "-----END PRIVATE KEY-----"], 14, 28, "HIKCENTRAL.PEM")[0])
c.add(Arrow(a.right(), (432, 210)))
c.add(Arrow(b.right(), (432, 300)))
h = c.add(Generic(904, 200, "HikCentral", "subir el .pem", icon="server", w=248, dark=True))
c.add(text(904, 316, "System > Advanced > Transfer", 14, 500, INK2, FM))
c.add(Arrow((838, 242), h.left()))
c.add(panel(48, 412, 540, 120, "Con el certificado embebido", "warn"))
c.add(text(72, 476, "El navegador muestra \"No seguro\".", 17, 500, INK2))
c.add(panel(612, 412, 540, 120, "Con el .pem firmado por una CA", "ok"))
c.add(text(636, 476, "Sin advertencia, si los puestos confían en esa CA.", 17, 500, INK2))
c.add(Note(48, 552, 1104, "La clave privada no se manda por correo ni se pega en conversores online con datos de un cliente: armá el .pem en una PC de confianza. Ruta de V2.x.", kind="alert"))
save(c, "11-paso5.svg")
