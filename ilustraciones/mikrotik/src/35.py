"""Lección 35 · Netwatch: principal, paso 2 (desenchufar y leer el log), paso 4 (mail y Telegram) y paso 5 (PoE)."""
from _mt import *

K = "MikroTik · Lección 35"

# ------------------------------------------------------------------ 35.svg
c = Canvas(K, "Una sonda vigila; al cambiar de estado, un script")
rt = c.add(Box(48, 200, 260, 124, "Router", "/tool/netwatch", dark=True))
nvr = c.add(Server(470, 140, "NVR", "192.168.88.50", w=250))
cam = c.add(Camera(470, 320, "Cámara PoE", "192.168.88.60", w=250))
c.add(Cable(rt.right(-20), nvr.left(), "logical", label="tcp-conn :554", label_dy=-12))
c.add(Cable(rt.right(20), cam.left(), "logical", label="icmp · 10 paq.", label_dy=22))
c.add(rect(800, 128, 352, 130, ALERT_BG, ALERT, 2, 16))
c.add(text(822, 164, "up → down", 19, 600, ALERT, FD))
c.add(text(822, 194, "down-script", 16, 600, INK, FM))
c.add(text(822, 222, "mail · Telegram · cortar PoE", 16, 400, INK2, FB))
c.add(rect(800, 280, 352, 130, OK_BG, OK, 2, 16))
c.add(text(822, 316, "down → up", 19, 600, OK, FD))
c.add(text(822, 346, "up-script", 16, 600, INK, FM))
c.add(text(822, 374, "aviso de que volvió", 16, 400, INK2, FB))
c.add(arrow((724, 182), (796, 192), kind="flow", bend="straight"))
c.add(arrow((724, 362), (796, 345), kind="flow", bend="straight"))
c.add(caption(48, 470, "Sondas de RouterOS 7"))
c.add(pills(48, 510, ["simple", "icmp", "tcp-conn", "http-get", "https-get", "dns"], kind="blue", gap=12))
c.add(Note(48, 552, 1104, "Cada script corre una vez por cambio de estado, no en cada prueba. Sin scripts, el cambio igual queda en el log.", kind="info", size=16))
save(c, "35.svg")

# ------------------------------------------------------------------ 35-paso2.svg
c = Canvas(K + " · Paso 2", "Desenchufá el NVR y mirá cuándo cambia el estado")
xs = [100 + i * 110 for i in range(10)]
res = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1]
c.add(caption(48, 150, "una prueba cada 30 s · tcp-conn al puerto 554"))
c.add(line(80, 230, 1130, 230, LINE2, 3))
for i, (x, r) in enumerate(zip(xs, res)):
    c.add(Mark(x, 230, bool(r)))
c.add(rect(370, 270, 300, 80, ALERT_BG, ALERT, 2, 14))
c.add(text(390, 302, "event down", 17, 600, ALERT, FM))
c.add(text(390, 330, "corre el down-script", 15, 400, INK2, FB))
c.add(line(430, 252, 430, 270, ALERT, 2))
c.add(rect(700, 270, 300, 80, OK_BG, OK, 2, 14))
c.add(text(720, 302, "event up", 17, 600, OK, FM))
c.add(text(720, 330, "corre el up-script", 15, 400, INK2, FB))
c.add(line(760, 252, 760, 270, OK, 2))
c.add(pill(430, 196, "desenchufás", "alert"))
c.add(pill(760, 196, "enchufás", "ok"))
s, _ = code(48, 384, 1104, ["/log/print where message~\"NVR|192.168.88.50\"",
                              ("netwatch,info  event down  ...  host: 192.168.88.50", "#FCA5A5"),
                              ("script,warning NVR 192.168.88.50 caido", "#FCD34D"),
                              ("netwatch,info  event up  ...  host: 192.168.88.50", "#6EE7B7")], title="LOG", lh=30)
c.add(s)
c.add(Note(48, 580, 1104, "Después de reiniciar el router, Netwatch espera 5 minutos (startup-delay) antes de la primera prueba.", kind="warn", size=16))
save(c, "35-paso2.svg")

# ------------------------------------------------------------------ 35-paso4.svg
c = Canvas(K + " · Paso 4", "Del script al celular: mail al caer, Telegram al volver")
rt = c.add(Box(48, 150, 280, 124, "Netwatch nvr", "down-script / up-script", dark=True))
c.add(rect(420, 130, 360, 120, WHITE, LINE2, 2, 16))
c.add(text(440, 166, "/tool/e-mail/send", 16, 600, BLUE, FM))
c.add(text(440, 196, "SMTP 587 · tls=starttls", 15, 500, INK2, FM))
c.add(text(440, 224, "texto sin tildes (ASCII)", 15, 400, INK3, FB))
c.add(rect(420, 280, 360, 120, WHITE, CYAN, 2, 16))
c.add(text(440, 316, "/tool/fetch mode=https", 16, 600, "#0B7FA6", FM))
c.add(text(440, 346, "address=api.telegram.org", 15, 500, INK2, FM))
c.add(text(440, 374, "output=none", 16, 700, OK, FM))
c.add(arrow(rt.right(-20), (416, 190), kind="flow", label="cae", label_dy=-12))
c.add(arrow(rt.right(20), (416, 340), kind="flow", label="vuelve", label_dy=18))
m = c.add(Generic(880, 148, "Mail", "soporte@example.com", icon="bell", w=272))
t = c.add(Phone(880, 298, "Telegram", "chat del equipo", w=272))
c.add(arrow((784, 190), m.left(), kind="flow", bend="straight"))
c.add(arrow((784, 340), t.left(), kind="flow", bend="straight"))
c.add(rect(48, 440, 1104, 108, ALERT_BG, ALERT, 2, 16))
c.add(text(72, 476, "Desde RouterOS 7.13, sin output=none no llega", 18, 600, ALERT, FD))
c.add(wrap(72, 506, "fetch intenta guardar la respuesta en un archivo y Netwatch no tiene ese permiso (solo read, write, test, reboot). Desde la terminal anda: por eso engaña.", 1060, 16, 400, INK)[0])
c.add(Note(48, 568, 1104, "Después de cada actualización, probá el aviso desenchufando: es la única forma de saber que sigue llegando.", kind="info", size=16))
save(c, "35-paso4.svg")

# ------------------------------------------------------------------ 35-paso5.svg
c = Canvas(K + " · Paso 5", "Cámara colgada: Netwatch le corta el PoE 10 s")
svg, anc, w = port_router(48, 130, ["ether2", "ether3", "ether4", "ether5"], {"ether5": WARN}, name="Router PoE out", sub="hEX PoE", pw=90, gap=12)
c.add(svg)
cam = c.add(Camera(300, 360, "Cámara", "192.168.88.60", w=240))
c.add(Cable(anc["ether5"], cam.top(40), "power+", label="PoE · ether5", label_dy=0))
# línea de tiempo de alimentación
c.add(caption(620, 150, "alimentación del puerto"))
c.add(line(620, 300, 1150, 300, LINE2, 2))
c.add(f'<path d="M620 220H820V290H900V220H1150" fill="none" stroke="{OK}" stroke-width="4"/>')
c.add(pill(860, 330, "10 s sin PoE", "warn"))
c.add(pill(720, 200, "colgada", "alert"))
c.add(pill(1030, 200, "arranca de nuevo", "ok"))
c.add(rect(620, 380, 532, 120, WHITE, LINE2, 2, 16))
c.add(text(640, 414, "Otra opción, sin Netwatch", 18, 600, INK, FD))
c.add(text(640, 444, "power-cycle-ping-enabled=yes", 15, 600, BLUE, FM))
c.add(text(640, 472, "el propio puerto vigila y reinicia", 15, 400, INK2, FB))
s, _ = code(48, 520, 1104, ["/tool/netwatch/add name=cam-entrada host=192.168.88.60 type=icmp interval=1m \\",
                              "    down-script=\"/interface/ethernet/poe/power-cycle ether5 duration=10s\""], title="NETWATCH", lh=28)
c.add(s)
save(c, "35-paso5.svg")
