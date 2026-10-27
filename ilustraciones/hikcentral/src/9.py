import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 9.svg: la cadena hasta la puerta
c = Canvas(K(), "Nada llega a la puerta hasta que aplicás")
ch = [("Persona", "Prueba Lab · ID 9001", "con credencial: tarjeta, huella, rostro, PIN o QR", "user"),
      ("Nivel de acceso", "Oficina hábil", "puertas + plantilla de horario", "key"),
      ("Asignación", "a la persona", "o a un departamento entero", "card")]
for i, (t, s, d, ic) in enumerate(ch):
    x = 48 + i * 300
    c.add(rect(x, 140, 270, 170, WHITE, LINE2, rx=16))
    c.add(icon(x + 22, 160, ic, BLUE, 1.3))
    c.add(text(x + 64, 182, t, 19, 600, INK))
    c.add(text(x + 22, 226, s, 16, 600, BLUE, FM))
    svg, _ = wrap(x + 22, 258, d, 230, 15, 400, INK2)
    c.add(svg)
    c.add(Arrow((x + 272, 225), (x + 298, 225), bend="straight"))
c.add(rect(948, 140, 204, 170, DEEP, DEEP, rx=16))
c.add(text(968, 182, "Aplicar", 21, 600, WHITE, FD))
c.add(text(968, 214, "a los dispositivos", 15, 400, "#9FC3E3"))
c.add(text(968, 252, "recién acá viaja", 15, 400, "#9FC3E3"))
c.add(text(968, 274, "a la controladora", 15, 400, "#9FC3E3"))
ctl = c.add(Generic(948, 370, "Controladora", "Puerta Lab", icon="door", w=204, hl=CYAN))
c.add(Arrow((1050, 312), ctl.top()))
c.add(panel(48, 350, 870, 170, "Si no aplicaste", "warn"))
c.add(text(72, 412, "La plataforma muestra el permiso, pero la controladora no lo tiene: la tarjeta no abre.", 17, 500, INK2))
c.add(text(72, 444, "Al lado de Apply aparece un ícono de pendiente.", 17, 500, INK2))
c.add(text(72, 476, "Si el aplicado falla, Access Control Test muestra en qué quedó.", 17, 500, INK2))
c.add(text(48, 580, "Alta de personas: en la plataforma, y de ahí a los equipos. Una sola fuente de verdad.", 17, 600, INK))
c.add(text(48, 616, "Plantilla de ejemplo del laboratorio: lunes a viernes, 08:00 a 19:00.", 16, 400, INK3))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso4: aplicar cambios o Apply (Initial)
c = Canvas(K(4), "Aplicar cambios o Apply (Initial): no es lo mismo")
c.add(panel(48, 124, 540, 400, "Apply (Initial) sin marcar", "ok"))
s1 = c.add(Generic(72, 180, "HikCentral", "", w=180, dark=True))
d1 = c.add(Generic(372, 180, "Controladora", "online", icon="door", w=200, hl=OK))
c.add(Arrow(s1.right(), d1.left(), kind="ok"))
c.add(mid(312, 294, "solo lo cambiado", 15, 600, OK, FM))
c.add(bullet_list(72, 330, [("Manda solo lo modificado.", "ok"), ("Las puertas siguen funcionando.", "ok"), ("Para el día a día: altas, bajas, horarios.", "ok")], 492, 17)[0])
c.add(panel(612, 124, 540, 400, "Apply (Initial) marcado", "alert"))
s2 = c.add(Generic(636, 180, "HikCentral", "", w=180, dark=True))
d2 = c.add(Generic(936, 180, "Controladora", "offline", icon="door", w=200, hl=ALERT))
c.add(Arrow(s2.right(), d2.left(), kind="alert"))
c.add(mid(876, 294, "borra y reescribe", 15, 600, ALERT, FM))
c.add(bullet_list(636, 330, [("Borra todo en el equipo y vuelve a escribir.", "alert"), ("Mientras tanto, offline: nadie pasa.", "alert"), ("Solo fuera de horario y con aviso al cliente.", "warn")], 492, 17)[0])
c.add(code(48, 548, 1104, "Persons: Specified Persons > Prueba Lab · Specified Access Point: on > Puerta Lab · Apply (Initial): sin marcar", 14, h=44))
c.add(text(48, 628, "Ruta de V2.x: Passing Management > Access Control > Access Level > Apply Access Level Settings.", 15, 400, WARN))
save(c, "9-paso4.svg")

# ---------------------------------------------------------------- 9-paso5: dentro y fuera del horario
c = Canvas(K(5), "Probá la tarjeta dentro y fuera del horario")
X0, X1, Y = 120, 1130, 230
sc = (X1 - X0) / 24
c.add(text(48, 150, "LUNES · PLANTILLA OFICINA HÁBIL", 14, 600, INK3, FM, ls=1.5))
c.add(rect(X0, Y - 26, X1 - X0, 52, WHITE, LINE2, rx=10))
c.add(rect(X0 + 8 * sc, Y - 26, 11 * sc, 52, OK_BG, OK, rx=10))
c.add(mid(X0 + 13.5 * sc, Y + 6, "08:00 a 19:00", 16, 600, OK, FM))
for h in (0, 6, 8, 12, 19, 24):
    c.add(mid(X0 + h * sc, Y + 56, f"{h:02d}:00", 14, 500, INK3, FM))
for (h, ok, lab) in [(10, True, "10:00 · acceso concedido"), (21, False, "21:00 · acceso denegado")]:
    x = X0 + h * sc
    c.add(f'<path d="M{x} {Y - 40}V{Y + 30}" stroke="{OK if ok else ALERT}" stroke-width="3"/>')
    c.add(icon(x - 16, Y - 108, "card", OK if ok else ALERT, 1.35))
    c.add(text(x + (14 if ok else -14), Y - 50, lab, 16, 600, OK if ok else ALERT, anchor="start" if ok else "end"))
c.add(text(48, 360, "Después, en el registro de acceso:", 19, 600, INK, FD))
c.add(Table(48, 384, ["Hora", "Persona", "Puerta", "Resultado"], [["10:00", "Prueba Lab", "Puerta Lab", "concedido"], ["21:00", "Prueba Lab", "Puerta Lab", "denegado"]], [180, 300, 300, 324], row_h=46, mono_cols=(0,)))
c.add(text(48, 560, "Horas de ejemplo. Si las dos abren, o ninguna, revisá que hayas aplicado y que la hora de la controladora sea la correcta.", 16, 400, INK2))
save(c, "9-paso5.svg")
