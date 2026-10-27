import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 14.svg: de la central hacia afuera
c = Canvas(K(), "Cuando no reporta: de la central hacia afuera")
c.add(NOLIG)
st = [("1", "Serie", "LED RX/TX del módulo titilando: habla con la central."),
      ("2", "Red", "Cable, IP del módulo y salida a internet."),
      ("3", "Puertos", "Salida abierta: TCP 8883 y 443 en módulos MQTT; el puerto de la receptora en legado."),
      ("4", "Receptora", "Registro, abonado y perfil. A veces, el abonado atado a otra MAC.")]
for i, (n, t, d) in enumerate(st):
    x = 48 + i * 282
    c.add(panel(x, 140, 258, 250, None, "info"))
    c.add(badge(x + 36, 180, n, CYAN, 20))
    c.add(text(x + 68, 188, t, 22, 600, INK, FD))
    svg, _ = wrap(x + 22, 236, d, 220, 16, 400, INK2)
    c.add(svg)
    if i < 3:
        c.add(Arrow((x + 262, 265), (x + 280, 265)))
c.add(text(48, 128, "CENTRAL", 13, 600, INK3, FM, ls=2))
c.add(text(1152, 128, "MONITOREO", 13, 600, INK3, FM, ls=2, anchor="end"))
c.add(rect(48, 420, 1104, 92, "#03213C", "#03213C", rx=14))
c.add(text(72, 458, "[935]  estado del registro IP/GPRS", 20, 600, "#D9E9F8", FM))
c.add(text(72, 490, "grupo 2 = error del módulo · grupo 3 = programación incompleta · grupo 4 = error de registro", 15, 500, "#9FC3E3", FM))
c.add(Note(48, 534, 1104, "Reiniciar a ciegas no dice nada. Con el número del teclado y una llamada a monitoreo, llegás a la causa. Reiniciar el módulo desde BlueEye tarda hasta 5 min (firmware 4.xx) o 15 min (5.xx).", kind="ok", size=16))
save(c, "14.svg")

# ---------------------------------------------------------------- 14-paso1: tabla de [935]
c = Canvas(K(1), "Leé [935]: cada grupo apunta a otra parte")
c.add(NOLIG)
c.add(Step(48, 130, 1))
sv, _ = keys(80, 114, ["[ENTER]", "+", "0000", "+", "[935]"], 17, hl=(4,))
c.add(sv)
c.add(Table(48, 180, ["Grupo", "Qué es", "Submenú"], [
    ["1", "estado de registro", "apagado: sin registrar · titila: registrando · fijo: OK"],
    ["2", "error del módulo", "7 sin módulo · 8 cable desenchufado · 9 sin IP o red GPRS"],
    ["3", "error de programación", "7 sin IP · 8 sin puerto · 9 sin abonado · 10 sin APN"],
    ["4", "error de registro", "7 no conecta · 8 perfil · 9 formato · 10 otra MAC"],
], [110, 260, 734], row_h=56))
labels = [("2", "paso 2: desenchufá el cable", 2), ("3", "paso 3: borrá el puerto [930]", 3), ("4", "paso 4: perfil inexistente en [934]", 4)]
for i, (g, t, n) in enumerate(labels):
    x = 48 + i * 376
    c.add(panel(x, 486, 352, 80, None, "warn"))
    c.add(badge(x + 32, 526, str(n), CYAN))
    c.add(text(x + 62, 532, t, 16, 600, INK, FB))
c.add(text(48, 610, "Después de cada prueba, volvé todo a normal. Sin errores, ARM en [935] registra (paso 5).", 16, 500, INK2, FB))
save(c, "14-paso1.svg")

# ---------------------------------------------------------------- 14-paso7: el abonado atado a la MAC vieja
c = Canvas(K(7), "Módulo nuevo, abonado atado a la MAC vieja")
c.add(NOLIG)
c.add(Step(48, 140, 7))
old = c.add(Generic(80, 150, "Módulo viejo", "MAC A · quemado", icon="server", w=280))
new = c.add(Generic(80, 330, "Módulo nuevo", "MAC B · misma programación", icon="server", w=330))
rc = c.add(Box(690, 220, 300, 140, "Receptora", "abonado 1A01 → MAC A", icon=ICON["server"]))
c.add(Cable(old.right(), rc.left(-30), kind="logical", label="registrado"))
c.add(Arrow(new.right(), rc.left(30), kind="alert", label="ARM"))
c.add(rect(400, 430, 590, 60, ALERT_BG, ALERT, rx=12))
c.add(text(420, 468, "[935] grupo 4, submenú 10: abonado registrado con otra MAC", 16, 700, ALERT, FB))
c.add(Note(48, 520, 1104, "No se arregla en la central: pedile a monitoreo que libere el abonado del módulo anterior y volvé a registrar con ARM.", title="La solución está en la receptora", kind="ok"))
c.add(Mark(1040, 290, False))
save(c, "14-paso7.svg")
