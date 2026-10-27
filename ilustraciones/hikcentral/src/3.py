import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 3.svg: base primero, expansiones arriba
c = Canvas(K(), "Primero la licencia base, después las expansiones")
c.add(text(48, 140, "BIEN: SE APILA SOBRE LA BASE", 14, 600, OK, FM, ls=1.5))
exp = ["Expansión: cámaras", "Expansión: puertas", "Expansión: módulos"]
for i, s in enumerate(exp):
    c.add(rect(48 + i * 178, 162, 166, 70, OK_BG, OK, rx=12))
    c.add(mid(48 + i * 178 + 83, 203, s.split(": ")[1], 17, 600, OK))
    c.add(mid(48 + i * 178 + 83, 182, "expansión", 13, 500, INK3, FM))
c.add(rect(48, 244, 522, 70, DEEP, DEEP, rx=12))
c.add(mid(309, 286, "Licencia base", 20, 600, WHITE, FD))
c.add(Mark(600, 238, True))
c.add(text(48, 370, "MAL: EXPANSIÓN SIN BASE", 14, 600, ALERT, FM, ls=1.5))
c.add(rect(48, 392, 166, 70, ALERT_BG, ALERT, rx=12, dash="6 5"))
c.add(mid(131, 433, "cámaras", 17, 600, ALERT))
c.add(rect(48, 474, 522, 70, WHITE, ALERT, rx=12, dash="6 5"))
c.add(mid(309, 516, "sin licencia base", 18, 500, ALERT))
c.add(tag(330, 434, "error 1113", "alert"))
c.add(Mark(600, 468, False))
c.add(panel(660, 124, 492, 420, "Online u offline", "info"))
c.add(text(684, 196, "Online", 19, 600, INK, FD))
c.add(text(684, 226, "El SYS tiene internet y habla con el", 16, 400, INK2))
c.add(text(684, 250, "servidor de licencias. Sin salida: 1103.", 16, 400, INK2))
c.add(text(684, 306, "Offline", 19, 600, INK, FD))
c.add(text(684, 336, "Archivo de pedido y de respuesta, con", 16, 400, INK2))
c.add(text(684, 360, "una PC que sí tiene internet, en 24 h.", 16, 400, INK2))
c.add(rect(684, 396, 444, 120, WARN_BG, WARN, rx=12, sw=1.5))
c.add(text(704, 428, "En los dos casos", 17, 600, WARN))
c.add(text(704, 456, "Solo el usuario admin activa, actualiza", 16, 400, INK2))
c.add(text(704, 480, "o desactiva. Hora del SYS correcta.", 16, 400, INK2))
c.add(text(48, 616, "Registrá el email del admin: sirve para recuperar el código si se pierden la contraseña y el código.", 16, 500, INK2))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso5: ida y vuelta offline
c = Canvas(K(5), "Activación offline: un pedido, una respuesta, 24 horas")
s = c.add(Generic(48, 150, "SYS sin internet", "192.168.88.10", icon="server", w=300, dark=True))
p = c.add(Generic(852, 150, "PC con internet", "kms.hikvision.com", icon="globe", w=300))
c.add(Arrow((348, 175), (852, 175), label="ActivationRequestFile.bin"))
c.add(Arrow((852, 210), (348, 210), label="ActivationResponseFile.bin", label_dy=34))
c.add(mid(600, 290, "en un pendrive, ida y vuelta", 16, 500, INK3))
st = [("1", "Generate Request File", "un solo clic: un segundo clic invalida el primer pedido"),
      ("2", "Subir el pedido", "en kms.hikvision.com, sección de activación"),
      ("3", "Bajar la respuesta", "el .bin que corresponde a ese pedido"),
      ("4", "Import y Activate", "y cargar el email del admin")]
for i, (n, t, d) in enumerate(st):
    x = 48 + i * 282
    c.add(rect(x, 326, 264, 150, WHITE, LINE2, rx=14))
    c.add(badge(x + 32, 360, n))
    c.add(text(x + 60, 367, t, 17, 600, INK))
    svg, _ = wrap(x + 20, 404, d, 230, 16, 400, INK2)
    c.add(svg)
c.add(Note(48, 500, 540, "Si pasan más de 24 horas, o importás una respuesta de otro pedido, falla con 1105. Se genera un pedido nuevo.", title="Todo dentro de las 24 horas", kind="warn"))
c.add(Note(612, 500, 540, "Con más de 24 horas de diferencia con la hora real, la activación offline falla (Operation timeout).", title="La hora del SYS, en hora", kind="warn"))
save(c, "3-paso5.svg")

# ---------------------------------------------------------------- 3-paso6: códigos de error
c = Canvas(K(6), "Los códigos de activación que más aparecen")
c.add(Table(48, 124, ["Código", "Qué pasó", "Qué hacer"], [
    ["1103", "El SYS no llega al servidor de licencias, o está caído", "Revisar internet o pasar a offline"],
    ["1105", "La respuesta no corresponde al pedido, o pasaron 24 h", "Generar un pedido nuevo, un solo clic"],
    ["1108", "Código ya usado en otro SYS", "Desactivar primero en el servidor viejo"],
    ["1113", "Expansión sin licencia base", "Activar primero la base"],
    ["1114", "Se modificó la hora del SYS", "Volver a la hora correcta"],
    ["1116", "Más recursos que los licenciados", "Licenciar según los recursos actuales"],
], [130, 540, 434], row_h=54, mono_cols=(0,)))
c.add(text(48, 540, "Fuente: FAQ V2.5.500. 1108 también aparece si la versión de la licencia no corresponde a la del sistema.", 16, 400, INK3))
c.add(Note(48, 566, 1104, "Anotá en la ficha de la obra qué código salió y cuándo: le ahorra tiempo al próximo técnico.", kind="info"))
save(c, "3-paso6.svg")
