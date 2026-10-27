import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 12.svg: día contra noche
c = Canvas(K(), "Mismo detector, distinta respuesta de día y de noche")
for i, (t, kd, steps) in enumerate([("Modo día: hay gente para investigar", "warn", [("1 detector", "prealarma al personal"), ("investiga", "tiempo que fija el proyecto"), ("confirma o vence", "alarma general")]),
                                    ("Modo noche: nadie investiga", "alert", [("1 detector", "alarma general + transmisión")])]):
    y = 130 + i * 200
    col = WARN if kd == "warn" else ALERT
    c.add(panel(48, y, 820, 180, t, kd))
    c.add(detector(110, y + 108, 28))
    for j, (a, b) in enumerate(steps):
        x = 190 + j * 230
        if not a and not b:
            continue
        if a:
            c.add(rect(x, y + 70, 210 if kd == "warn" else 260, 76, WHITE, col, rx=12, sw=2))
            c.add(text(x + 16, y + 102, a, 17, 600, INK))
            c.add(text(x + 16, y + 128, b, 15, 400, INK2))
        else:
            c.add(text(x - 10, y + 115, b, 16, 600, col))
        if j < len(steps) - 1 and steps[j + 1][0]:
            c.add(arrow((x + 212, y + 108), (x + 228, y + 108), kind="alert" if kd == "alert" else "flow"))
c.add(rect(48, 540, 820, 92, ALERT_BG, ALERT, rx=14, sw=2.5))
c.add(pulsador(104, 586, 44))
c.add(text(150, 576, "Pulsador: alarma general inmediata, de día y de noche", 18, 600, ALERT))
c.add(text(150, 604, "El pulsador anula cualquier retardo. Nunca se demora.", 16, 400, INK2))
c.add(rect(900, 150, 252, 170, DEEP, DEEP, rx=16))
c.add(text(920, 184, "Teclas de función", 16, 600, WHITE, FB))
for k in range(3):
    kx = 922 + k * 76
    c.add(rect(kx, 210, 62, 44, NAVY, CYAN if k == 0 else "#3E6A93", rx=8, sw=2.5 if k == 0 else 1.5))
c.add(text(953, 290, "día / noche", 15, 600, CYAN, FB, anchor="middle"))
c.add(f'<path d="M953 256V272" stroke="{CYAN}" stroke-width="2"/>')
c.add(wrap(900, 352, "El panel trae 3 teclas programables. Una (o un horario) puede pasar de día a noche o a la sensibilidad alternativa.", 252, 15)[0])
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso1: la tabla del laboratorio
c = Canvas(K(1), "Completá la tabla: acción y retardo en cada modo")
c.add(Table(48, 136, ["Evento", "Modo día", "Modo noche"], [
    ["1 detector", "prealarma, personal investiga 3 min", "alarma general + transmisión"],
    ["2 detectores", "", ""],
    ["1 pulsador", "alarma general inmediata", "alarma general inmediata"],
    ["Falla de red", "", ""],
    ["Cambio día/noche", "tecla de función / horario: ____", ""]], [230, 440, 434], hl_row=2, row_h=56))
c.add(text(48, 500, "Las filas completas son el ejemplo del laboratorio; las vacías las completás vos.", 15, 400, INK3))
c.add(Note(48, 530, 540, "BS 5839-1 limita la alarma demorada a 6 minutos y un pulsador la anula. La IT-11 de 2010 admite preseñal de hasta 2 minutos en locales concurridos.", title="Topes de referencia", kind="info"))
c.add(Note(612, 530, 540, "Lo que pongas en la tabla todavía no vale: la valida el técnico registrado antes de programarla.", title="Paso 3", kind="warn"))
save(c, "12-paso1.svg")

# ---------------------------------------------------------------- 12-paso2: verificación
c = Canvas(K(2), "Dos controles antes de llevar la tabla")
for i, (ok, t, s) in enumerate([(False, "Retardo sobre un pulsador", "Un pulsador es una persona que vio fuego: nunca se demora."),
                                 (False, "Retardo mayor al del proyecto", "Si el proyecto dice 3 minutos, 5 no es una mejora: es otra obra."),
                                 (True, "Retardos solo donde el proyecto los admite", "con el tiempo que firmó el técnico registrado")]):
    y = 140 + i * 130
    kd = "ok" if ok else "alert"
    c.add(panel(48, y, 1104, 110, None, kd))
    c.add(Mark(100, y + 55, ok))
    c.add(text(140, y + 48, t, 20, 600, OK if ok else ALERT, FD))
    c.add(text(140, y + 78, s, 16, 400, INK2))
c.add(Note(48, 540, 1104, "Un retardo mal configurado demora la evacuación en un fuego real. Solo se programa lo que está en el proyecto firmado y aceptado por la autoridad.", title="Por qué tanto cuidado", kind="warn"))
save(c, "12-paso2.svg")
