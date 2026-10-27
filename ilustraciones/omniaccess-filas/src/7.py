from _fil import *

# ---------- 7.svg: la cola de despachos
c = Canvas("OmniAccess Filas · Lección 7", "Cada aviso pasa por la cola de despachos")
a = c.add(Generic(48, 160, "Alerta o regla", "aforo ≥ umbral", icon="bell", w=250))
q = c.add(Generic(360, 160, "Cola dispatch", "despacho Pendiente", icon="server", w=260))
w = c.add(Generic(654, 160, "dispatch-worker", "4 a la vez", icon="server", w=260, dark=True))
c.add(Arrow(a.right(), q.left()))
c.add(Arrow(q.right(), w.left()))
outs = [("Telegram", "foto o clip por URL", "ok"), ("WhatsApp", "OpenWA", "ok"), ("PWA / Push", "Web Push · VAPID", "ok"), ("Email", "sin envío en esta versión", "alert")]
for i, (t, s, k) in enumerate(outs):
    y = 300 + i * 66
    col = OK if k == "ok" else ALERT
    c.add(rect(820, y, 332, 54, OK_BG if k == "ok" else ALERT_BG, col, 2, rx=12))
    c.add(text(842, y + 34, t, 17, 600, INK))
    c.add(text(1132, y + 34, s, 14, 500, col, FM, anchor="end"))
    c.add(line(784, y + 27, 812, y + 27, col, 3, arrow=True))
c.add(line(784, 245, 784, 300 + 3 * 66 + 27, INK3, 3))
c.add(panel(48, 300, 700, 250, "Si un envío falla, reintenta", kind="info"))
for i, (n, t) in enumerate([("1.º", "al instante"), ("2.º", "+5 s"), ("3.º", "+10 s"), ("4.º", "+20 s"), ("5.º", "+40 s")]):
    x = 90 + i * 130
    c.add(Chip(x + 40, 400, n, "blue", anchor="middle"))
    c.add(text(x + 40, 440, t, 15, 600, INK2, FM, anchor="middle"))
c.add(text(68, 500, "Backoff exponencial: cada espera es el doble de la anterior.", 16, 500, INK2))
c.add(text(68, 526, "Después del 5.º intento queda Fallido, con su error.", 16, 500, INK2))
c.add(Note(48, 576, 1104, "Todo queda en Despachos: Pendiente, Procesando, Enviado o Fallido, y el botón Reintentar.", kind="info", size=15))
save(c, "7.svg")

# ---------- 7-paso5.svg: estados en Despachos
c = Canvas("OmniAccess Filas · Lección 7 · Paso 5", "Seguí el despacho hasta Enviado")
seq = [("Pendiente", "gray"), ("Procesando", "blue"), ("Enviado", "ok")]
xs = [180, 470, 760]
for i, ((s_, k), x) in enumerate(zip(seq, xs)):
    c.add(Chip(x, 220, s_, k, anchor="middle"))
    if i < 2:
        w0 = len(s_) * 9.2 + 26
        w1 = len(seq[i + 1][0]) * 9.2 + 26
        c.add(Arrow((x + w0 / 2 + 8, 211), (xs[i + 1] - w1 / 2 - 10, 211), kind="flow"))
c.add(Arrow((470, 240), (470, 330), kind="alert", label="error", label_dy=0))
c.add(Chip(470, 360, "Fallido", "alert", anchor="middle"))
c.add(Arrow((540, 352), (700, 352), kind="flow", label="Reintentar", label_dy=-14))
c.add(Chip(780, 360, "Pendiente", "gray", anchor="middle"))
c.add(Step(48, 150, 5))
c.add(Table(48, 420, ["Error", "Qué revisar"], [
    ["Faltan credenciales de Telegram", "Bot Token y Chat ID en Canales"],
    ["Telegram: … URL de la foto", "dirección pública del servidor"],
    ["Canal no soportado: email", "usar Telegram, WhatsApp o push"],
], [470, 634], row_h=40, mono_cols=(0,)))
save(c, "7-paso5.svg")

# ---------- 7-paso6.svg: Telegram baja la foto de una URL pública
c = Canvas("OmniAccess Filas · Lección 7 · Paso 6", "Telegram baja la foto desde la dirección pública")
wk = c.add(Generic(48, 200, "dispatch-worker", "sendPhoto con URL", icon="server", w=290))
tg = c.add(Internet(470, 200, "Telegram", "servidores del bot", w=260))
pub = c.add(Server(860, 200, "Dirección pública", "foto y clip", w=292))
ph = c.add(Phone(470, 420, "Supervisor", "chat de Telegram", w=260))
c.add(Arrow(wk.right(), tg.left(), label="1 · pedido", label_dy=-30))
c.add(Arrow(tg.right(), pub.left(), label="2 · descarga", label_dy=-30))
c.add(Arrow(tg.bottom(), ph.top(), kind="ok", label="3 · mensaje", label_dy=0))
c.add(Step(48, 200, 6))
c.add(Note(860, 330, 292, "Si la dirección no responde desde internet, el envío queda Fallido.", kind="alert", size=15))
c.add(Note(48, 330, 380, "La prueba de texto puede llegar y la alerta con foto no: es la pista de este problema.", kind="warn", size=15))
save(c, "7-paso6.svg")
