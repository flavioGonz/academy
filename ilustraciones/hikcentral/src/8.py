import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 8.svg: evento y alarma
c = Canvas(K(), "Evento o alarma: ¿alguien la va a atender?")
parts = [("Disparador", "Camera Offline, Alarm Input"), ("Fuente", "qué cámaras o entradas"), ("Horario", "cuándo se recibe"), ("Acciones", "grabar, bloquear, avisar")]
for i, (t, d) in enumerate(parts):
    x = 48 + i * 196
    c.add(rect(x, 132, 180, 100, WHITE, LINE2, rx=14))
    c.add(text(x + 18, 168, t, 18, 600, INK))
    svg, _ = wrap(x + 18, 196, d, 150, 15, 400, INK3)
    c.add(svg)
    if i < 3:
        c.add(mid(x + 188, 188, "+", 22, 700, INK3))
c.add(mid(832, 188, "=", 26, 700, INK3))
c.add(rect(860, 132, 292, 100, SOFT, BLUE, rx=14))
c.add(text(880, 172, "Evento", 22, 600, BLUE, FD))
c.add(text(880, 202, "queda registrado", 16, 400, INK2))
c.add(Arrow((1006, 236), (1006, 288), label=None))
c.add(rect(860, 292, 292, 140, ALERT_BG, ALERT, rx=14))
c.add(text(880, 330, "Alarma", 22, 600, ALERT, FD))
c.add(text(880, 360, "Trigger Alarm: on", 16, 600, INK, FM))
c.add(text(880, 388, "con prioridad y destinatarios", 16, 400, INK2))
c.add(text(880, 412, "que la reciben en clientes y móvil", 16, 400, INK2))
c.add(panel(48, 268, 780, 164, "Menos ruido", "info"))
c.add(text(72, 330, "Ignore Repetitive Events · 30 s", 17, 600, INK, FM))
c.add(text(72, 356, "iguales de la misma fuente en 30 s cuentan como uno", 16, 400, INK2))
c.add(text(72, 394, "Delay Alarm · cámara offline", 17, 600, INK, FM))
c.add(text(72, 420, "si vuelve dentro del plazo, no avisa", 16, 400, INK2))
c.add(Note(48, 460, 540, "Más de 20 eventos con imagen por segundo hacia el Web Client lo traban (FAQ). El ruido también pesa en la plataforma.", title="Ojo con la cantidad", kind="warn"))
c.add(Note(612, 460, 540, "Cámara caída: evento para mantenimiento. Puerta forzada de noche: alarma para el guardia.", title="Ejemplo", kind="info"))
c.add(text(48, 638, "Si nadie la va a atender, no es alarma: es evento.", 18, 600, BLUE, FD))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso2: Delay Alarm en una línea de tiempo
c = Canvas(K(2), "Delay Alarm de 120 s: solo avisan las caídas reales")
X0, SC = 140, 6.2  # px por segundo hasta 160 s
for k, (y, off, label, ok) in enumerate([(200, 30, "Corte de 30 s", True), (380, 160, "Corte de 3 min", False)]):
    c.add(text(48, y - 40, label, 19, 600, INK, FD))
    c.add(hline(X0, X0 + 160 * SC, y, LINE2, 2))
    for s in (0, 30, 60, 90, 120, 150):
        c.add(f'<path d="M{X0 + s * SC} {y - 6}V{y + 6}" stroke="{INK3}" stroke-width="2"/>')
        c.add(mid(X0 + s * SC, y + 30, f"{s} s", 14, 500, INK3, FM))
    w = min(off, 160) * SC
    c.add(rect(X0, y - 18, w, 36, ALERT_BG if not ok else WARN_BG, ALERT if not ok else WARN, rx=8, sw=1.5))
    c.add(text(X0 + 12, y + 6, "offline", 15, 600, ALERT if not ok else WARN, FM))
    c.add(f'<path d="M{X0 + 120 * SC} {y - 34}V{y + 18}" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="6 5"/>')
    c.add(text(X0 + 120 * SC + 8, y - 24, "fin de la demora", 14, 600, BLUE, FM))
    if ok:
        c.add(Mark(X0 + 30 * SC + 26, y, True))
        c.add(text(X0 + 30 * SC + 52, y + 6, "vuelve: no avisa", 16, 600, OK))
    else:
        c.add(badge(X0 + 120 * SC, y + 62, "!", ALERT, 16, 16))
        c.add(text(X0 + 120 * SC + 24, y + 68, "aparece el evento", 16, 600, ALERT))
c.add(Note(48, 506, 540, "Triggering Event: Camera Offline (Maintenance). Source: CAM-01 a CAM-04. Trigger Alarm: off, queda como evento.", title="Regla 1 del laboratorio", kind="info"))
c.add(Note(612, 506, 540, "Mantenimiento ve las cámaras realmente caídas, no las que parpadean por un corte de red de unos segundos.", title="Para qué sirve", kind="ok"))
save(c, "8-paso2.svg")

# ---------------------------------------------------------------- 8-paso3: pre y post evento, bloqueo
c = Canvas(K(3), "Clip con 10 s antes y 30 s después, bloqueado 7 días")
X0, SC, Y = 160, 16, 250   # 0 s del evento en X0 + 10*SC
t0 = X0 + 10 * SC
c.add(hline(X0 - 60, X0 + 50 * SC, Y, LINE2, 2))
c.add(rect(X0, Y - 34, 40 * SC, 68, OK_BG, OK, rx=10))
c.add(rect(X0, Y - 34, 10 * SC, 68, SOFT, BLUE, rx=10))
c.add(mid(X0 + 5 * SC, Y + 6, "pre 10 s", 16, 600, BLUE, FM))
c.add(mid(t0 + 15 * SC, Y + 6, "post 30 s", 16, 600, OK, FM))
c.add(f'<path d="M{t0} {Y - 70}V{Y + 50}" stroke="{ALERT}" stroke-width="3"/>')
c.add(text(t0 - 8, Y - 80, "se activa la entrada 1 (contacto de puerta)", 16, 600, ALERT, anchor="middle"))
c.add(mid(X0, Y + 70, "-10 s", 15, 500, INK3, FM))
c.add(mid(t0, Y + 70, "0", 15, 500, INK3, FM))
c.add(mid(t0 + 30 * SC, Y + 70, "+30 s", 15, 500, INK3, FM))
c.add(f'<path d="M{t0 + 4} {Y + 96}H{t0 + 30 * SC}" stroke="{WARN}" stroke-width="3" stroke-dasharray="4 5"/>')
c.add(text(t0 + 8, Y + 122, "Ignore Repetitive 30 s: otro disparo acá cuenta como el mismo", 15, 600, WARN))
c.add(Table(48, 412, ["Campo", "Valor de la regla 2"], [["Trigger Recording", "CAM-02, pre 10 s, post 30 s"], ["Lock Video Files", "7 días, no se sobrescribe"], ["Trigger Alarm", "on, prioridad alta, usuario guardia"]], [330, 774], row_h=44, mono_cols=(0,)))
c.add(text(48, 628, "CAM-02 necesita calendario de grabación: sin él, la regla queda en excepción.", 16, 600, INK))
save(c, "8-paso3.svg")
