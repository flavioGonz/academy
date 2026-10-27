from _fil import *

# ---------- 3.svg: pull point cada 5 s y push opcional
c = Canvas("OmniAccess Filas · Lección 3", "Pull cada 5 segundos; push, solo como complemento")
xs, xc = 250, 950
c.add(Server(xs - 150, 130, "OmniAccess", "omniaccess-web", w=300))
c.add(Camera(xc - 150, 130, "Cámara Bosch", "events_service", w=300))
c.add(line(xs, 214, xs, 600, LINE2, 2, dash="4 6"))
c.add(line(xc, 214, xc, 600, LINE2, 2, dash="4 6"))
c.add(Arrow((xs + 6, 262), (xc - 6, 262), label="CreatePullPointSubscription · 300 s", label_dy=-14))
c.add(Arrow((xc - 6, 300), (xs + 6, 300), kind="ok", label="dirección del pull point", label_dy=-12))
c.add(rect(xs - 40, 330, 780, 150, OK_BG, OK, 2, rx=14))
c.add(text(xs - 22, 356, "CADA 5 s", 14, 600, OK, FM, ls=1.5))
c.add(Arrow((xs + 6, 392), (xc - 6, 392), label="PullMessages", label_dy=-12))
c.add(Arrow((xc - 6, 444), (xs + 6, 444), kind="ok", label="Aforo = 4 · Changed", label_dy=-12))
c.add(Arrow((xc - 6, 540), (xs + 6, 540), kind="logical", label="push opcional: Notify a /api/onvif/notify", label_dy=-14))
c.add(Note(48, 566, 1104, "El pull es el camino completo: graba solo si el valor cambió y dispara todos los avisos. Si el push entrega, el pull se calla para no contar doble.", kind="info", size=15))
save(c, "3.svg")

# ---------- 3-paso1.svg: alta del contador
c = Canvas("OmniAccess Filas · Lección 3 · Paso 1", "Alta: Dispositivos Conteo → Agregar")
c.add(Window(48, 130, 640, 420, "Dispositivos Conteo · Agregar", rows=[
    ("Tipo", "Contador de Filas"), ("Fabricante", "Bosch"), ("Nombre", "Fila Caja 1"),
    ("IP", "192.0.2.10"), ("Usuario", "omniaccess"), ("Contraseña", "••••••••••"),
], hl=0, path="Filas → Dispositivos Conteo"))
c.add(Step(688, 230, 1))
c.add(Arrow((712, 340), (800, 340), kind="flow"))
c.add(panel(810, 130, 342, 420, "En unos segundos", kind="ok"))
for i, s in enumerate(["se crea la suscripción", "llegan Aforo, Entrada", "y Salida a la tabla", "\"Detección por fila\"", "con su última lectura"]):
    c.add(text(834, 196 + i * 34, s, 17, 500, INK))
c.add(Chip(834, 400, "Aforo · 0", "dark"))
c.add(Chip(834, 446, "Entrada · 0", "blue"))
c.add(Chip(834, 492, "Salida · 0", "blue"))
save(c, "3-paso1.svg")

# ---------- 3-paso4.svg: estado del sondeo en el servidor
c = Canvas("OmniAccess Filas · Lección 3 · Paso 4", "¿El sondeo está vivo? Preguntale al servidor")
c.add(Terminal(48, 140, 720, [
    "$ curl -s \"127.0.0.1:10001/api/queue/poll?info=1\"",
    ("{ \"autoPolling\": true,", "#9BE7C4"),
    "  \"subscriptions\": [ {",
    ("    \"pullPointUrl\": \"https://192.0.2.10/...\",", "#D9E9F8"),
    ("    \"expiresAt\": \"…T14:05:00Z\",", "#D9E9F8"),
    ("    \"lastPull\": \"…T14:00:31Z\" } ] }", "#9BE7C4"),
], title="servidor de la fila"))
c.add(Step(48, 140, 4))
c.add(Note(800, 140, 352, "autoPolling en true y un lastPull de hace segundos: el sondeo anda.", title="Sano", kind="ok", size=15))
c.add(Note(800, 300, 352, "Sin suscripciones o lastPull viejo: revisá red, HTTPS 443 y usuario de la cámara.", title="Para revisar", kind="warn", size=15))
c.add(Note(48, 460, 1104, "Después mirá el registro de omniaccess-web: \"Created subscription\" al conectar y \"Aforo = N personas (Changed)\" cada vez que el número cambia.", kind="info", size=15))
save(c, "3-paso4.svg")
