from _fil import *

# ---------- 6.svg: umbral, estados, cooldown y escalamiento
c = Canvas("OmniAccess Filas · Lección 6", "Umbral 10: estados, período de calma y escalamiento")
x0, x1, y = 90, 1110, 200
scale = (x1 - x0) / 12
c.add(rect(x0, y, 7 * scale, 46, OK_BG, OK, 2, rx=10))
c.add(rect(x0 + 7 * scale, y, 3 * scale, 46, WARN_BG, WARN, 2, rx=10))
c.add(rect(x0 + 10 * scale, y, 2 * scale, 46, ALERT_BG, ALERT, 2, rx=10))
c.add(text(x0 + 3.5 * scale, y + 30, "OK", 18, 700, OK, FD, anchor="middle"))
c.add(text(x0 + 8.5 * scale, y + 30, "ALTO", 18, 700, WARN, FD, anchor="middle"))
c.add(text(x0 + 11 * scale, y + 30, "LLENO", 18, 700, ALERT, FD, anchor="middle"))
for v in range(0, 13):
    xx = x0 + v * scale
    c.add(line(xx, y + 50, xx, y + 60, INK3, 2))
    c.add(text(xx, y + 82, str(v), 15, 500, INK3, FM, anchor="middle"))
c.add(text(x0 + 7 * scale, y - 14, "70 % = 7", 15, 600, WARN, FM, anchor="middle"))
c.add(text(x0 + 10 * scale, y - 14, "umbral = 10", 15, 600, ALERT, FM, anchor="middle"))
c.add(text(x0 + 6 * scale, y + 112, "personas en la zona (aforo)", 15, 500, INK3, FM, anchor="middle"))
# línea de tiempo
ty = 440
c.add(line(90, ty, 1110, ty, INK3, 2))
c.add(Chip(160, ty - 30, "llega a 10: avisa", "alert", anchor="middle"))
c.add(rect(160, ty + 12, 300, 22, CYAN, CYAN, 0, rx=6, opacity=.25))
c.add(text(310, ty + 58, "cooldown: no repite el aviso", 15, 600, BLUE, FM, anchor="middle"))
c.add(rect(160, ty + 70, 700, 14, WARN, WARN, 0, rx=6, opacity=.25))
c.add(text(510, ty + 108, "sigue sobre el umbral 5 minutos", 15, 600, WARN, FM, anchor="middle"))
c.add(Chip(940, ty - 30, "escalamiento al supervisor", "alert", anchor="middle"))
c.add(f'<circle cx="160" cy="{ty}" r="7" fill="{ALERT}"/><circle cx="860" cy="{ty}" r="7" fill="{ALERT}"/>')
save(c, "6.svg")

# ---------- 6-paso1.svg: horario con reseteo a la apertura
c = Canvas("OmniAccess Filas · Lección 6 · Paso 1", "A la hora de apertura, los contadores vuelven a 0")
c.add(Window(48, 130, 520, 330, "Horarios de Filas · Nuevo horario", rows=[
    ("Nombre", "Apertura Caja 1"), ("Dispositivo", "Fila Caja 1"), ("Días", "L a S"),
    ("Apertura / Cierre", "08:00 / 20:00"), ("Reseteo automático", "activado"), ("Horario activo", "activado")], hl=4))
c.add(Step(568, 160, 1))
srv = c.add(Server(640, 140, "Servidor", "cron cada minuto", w=280))
c.add(code(640, 250, 512, "* * * * *  schedule/tick", 15))
c.add(Arrow((780, 294), (780, 360), kind="flow", label="08:00 hora de Uruguay", label_dy=0))
c.add(Chip(700, 420, "Aforo 0", "ok", anchor="middle"))
c.add(Chip(850, 420, "Entrada 0", "ok", anchor="middle"))
c.add(Chip(1010, 420, "Salida 0", "ok", anchor="middle"))
c.add(Note(48, 490, 1104, "Sin la línea del cron el horario se ve en pantalla pero no resetea nada. \"Reset ahora\" lo hace a mano. El aforo retoma el valor real con el próximo evento de la cámara.", kind="warn", size=15))
save(c, "6-paso1.svg")

# ---------- 6-paso4.svg: la alerta de aforo
c = Canvas("OmniAccess Filas · Lección 6 · Paso 4", "Nueva alerta de aforo: umbral y período de calma")
c.add(Window(48, 130, 560, 350, "Filas · Nuevo Umbral", rows=[
    ("Nombre de la alerta", "Aforo Caja 1"), ("Dispositivo", "Fila Caja 1"), ("Canal (opcional)", "Aforo"),
    ("Umbral (personas)", "2  (prueba)"), ("Cooldown (seg)", "30"), ("Botón", "Crear alerta")], hl=3))
c.add(Step(608, 290, 4))
c.add(Note(650, 130, 502, "Dispara cuando el aforo llega o supera el umbral, por ejemplo de 1 a 2.", title="Cuándo avisa", kind="ok", size=15))
c.add(Note(650, 260, 502, "Si avisó hace menos que el cooldown, aunque siga llena.", title="Cuándo no repite", kind="info", size=15))
c.add(Note(650, 380, 502, "Al terminar la prueba, umbral real del cliente y una sola alerta por fila.", title="Después", kind="warn", size=15))
save(c, "6-paso4.svg")
