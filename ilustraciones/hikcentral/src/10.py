import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 10.svg: el orden de la asistencia
c = Canvas(K(), "Asistencia: primero la hora, después los turnos")
st = [("0", "Hora y zona", "SYS y controladoras iguales"), ("1", "Puntos de marca", "qué lectoras: entrada, salida o ambas"),
      ("2", "Regla general", "fin de semana y ausencias"), ("3", "Plantilla de turno", "Normal o Man-Hour"),
      ("4", "Turno", "repetir por semana"), ("5", "Asignar", "a personas, con fechas"), ("6", "Registros", "al día siguiente")]
for i, (n, t, d) in enumerate(st):
    col, row = i % 4, i // 4
    x, y = 48 + col * 282, 132 + row * 176
    first = i == 0
    c.add(rect(x, y, 262, 150, WARN_BG if first else WHITE, WARN if first else LINE2, rx=14))
    c.add(badge(x + 32, y + 34, n, WARN if first else CYAN))
    c.add(text(x + 60, y + 41, t, 18, 600, INK))
    svg, _ = wrap(x + 20, y + 84, d, 226, 16, 400, INK2)
    c.add(svg)
    if col < 3 and i < 6:
        c.add(Arrow((x + 264, y + 75), (x + 280, y + 75), bend="straight"))
c.add(rect(894, 308, 258, 150, SOFT, BLUE, rx=14))
c.add(text(914, 344, "La plataforma calcula", 17, 600, BLUE))
c.add(text(914, 372, "con la hora del servidor", 16, 400, INK2))
c.add(text(914, 396, "y no maneja múltiples", 16, 400, INK2))
c.add(text(914, 420, "zonas horarias.", 16, 400, INK2))
c.add(Note(48, 492, 1104, "Receta del soporte de Hikvision USA: controladora y personas con credenciales, puntos de marca, regla general, plantilla, turno, asignación y registros. Las mismas lectoras de acceso hacen de reloj.", title="La receta, en orden", kind="info"))
c.add(text(48, 640, "Primero la hora, después los turnos.", 18, 600, BLUE, FD))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso1: misma zona horaria
c = Canvas(K(1), "SYS y controladora en la misma hora y la misma zona")
for i, ok in enumerate([True, False]):
    x = 48 + i * 564
    c.add(panel(x, 124, 540, 380, "Misma zona, NTP común" if ok else "Controladora en otra zona", "ok" if ok else "alert"))
    s = c.add(Generic(x + 24, 180, "SYS", "192.168.88.10 · UTC-3", w=492, dark=True))
    d = c.add(Generic(x + 24, 320, "Controladora", "UTC-3 · NTP 192.168.88.10" if ok else "otra zona horaria", icon="door", w=492, hl=None if ok else ALERT))
    c.add(Arrow((x + 270, 320), (x + 270, 266), kind="ok" if ok else "alert"))
    c.add(text(x + 290, 300, "pasadas", 15, 600, OK if ok else ALERT, FM))
    c.add(Mark(x + 44, 450, ok))
    c.add(text(x + 76, 457, "Pasadas en vivo y reportes que cierran" if ok else "Histórico sí, pasadas en vivo no", 17, 600, OK if ok else ALERT))
c.add(code(48, 528, 540, "Get-TimeZone ; w32tm /query /status", 16, h=48))
c.add(text(612, 548, "En la controladora: Configuración > Hora,", 16, 500, INK2))
c.add(text(612, 574, "misma zona y NTP al SYS o al del cliente.", 16, 500, INK2))
c.add(text(48, 628, "Uruguay es UTC-3 todo el año: sin horario de verano desde 2015.", 16, 500, INK3))
save(c, "10-paso1.svg")

# ---------------------------------------------------------------- 10-paso4: Man-Hour, primera entrada y última salida
c = Canvas(K(4), "Man-Hour: cuenta la primera entrada y la última salida")
X0, X1, Y = 110, 1140, 260
sc = (X1 - X0) / 12   # de 07:00 a 19:00
def hx(h): return X0 + (h - 7) * sc
c.add(rect(X0, Y - 24, X1 - X0, 48, WHITE, LINE2, rx=10))
c.add(rect(hx(8), Y - 24, 9 * sc, 48, SOFT, LINE2, rx=10, dash="6 5"))
c.add(mid(hx(10.2), Y + 6, "plantilla 08:00 a 17:00", 15, 500, INK3, FM))
for h in range(7, 20, 2):
    c.add(mid(hx(h), Y + 52, f"{h:02d}:00", 14, 500, INK3, FM))
marks = [(7 + 52 / 60, "07:52", "primera entrada", OK, True), (12.5, "12:30", "", INK3, False), (13.25, "13:15", "", INK3, False), (17 + 10 / 60, "17:10", "última salida", OK, True)]
for h, lab, d, col, key in marks:
    x = hx(h)
    c.add(f'<path d="M{x} {Y - 50}V{Y + 24}" stroke="{col}" stroke-width="{3 if key else 2}"' + ("" if key else ' stroke-dasharray="4 4"') + "/>")
    c.add(mid(x, Y - 60, lab, 15, 600, col, FM))
    if d:
        c.add(mid(x, Y - 86, d, 15, 600, col))
c.add(f'<path d="M{hx(7 + 52 / 60)} {Y + 86}H{hx(17 + 10 / 60)}" stroke="{OK}" stroke-width="4"/>')
c.add(mid(hx(12.5), Y + 114, "el cálculo toma de 07:52 a 17:10", 17, 600, OK))
c.add(text(48, 420, "Las marcas del medio quedan en el registro; el cálculo usa la primera y la última del día. Horas de ejemplo.", 16, 400, INK2))
c.add(Note(48, 452, 540, "Exige entrar y salir dentro de ventanas válidas. Sirve cuando el horario es rígido.", title="Normal", kind="info"))
c.add(Note(612, 452, 540, "Más flexible: no exige ventana de entrada y salida. El cálculo más usado es primera entrada y última salida.", title="Man-Hour", kind="ok"))
save(c, "10-paso4.svg")
