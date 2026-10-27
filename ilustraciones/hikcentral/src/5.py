import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 5.svg: tres formas de alta, quién llama a quién
c = Canvas(K(), "Tres formas de alta: fijate quién llama a quién")
cols = [("Por IP o dominio", "info", "El SYS entra al equipo", "Hace falta IP fija y ruta al equipo.", "puerto 8000 · 8443 cifrado"),
        ("Por ISUP (ex EHome)", "ok", "El equipo se registra en el SYS", "Sin IP fija: alcanza con salida.", "puerto 7660 · Device ID + clave"),
        ("Por Hik-Connect", "warn", "Los dos pasan por la nube", "Serie y código de verificación.", "no graba en Hybrid SAN ni Cloud")]
for i, (t, kd, sub, l1, l2) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 124, 352, 420, t, kd))
    c.add(text(x + 20, 182, sub, 17, 600, INK))
    if i == 0:
        s = c.add(Generic(x + 24, 214, "SYS", "192.168.88.10", w=304, dark=True))
        d = c.add(Generic(x + 24, 360, "Cámara o NVR", "192.168.88.21", icon="camera", w=304))
        c.add(Arrow(s.bottom(), d.top()))
        c.add(text(x + 196, 336, "SYS → equipo", 15, 600, BLUE, FM))
    elif i == 1:
        s = c.add(Generic(x + 24, 214, "SYS", "escucha el 7660", w=304, dark=True))
        d = c.add(Generic(x + 24, 360, "Cámara o NVR", "sin IP fija", icon="camera", w=304))
        c.add(Arrow(d.top(), s.bottom(), kind="ok"))
        c.add(text(x + 196, 336, "equipo → SYS", 15, 600, OK, FM))
    else:
        s = c.add(Generic(x + 24, 214, "SYS", "", w=140, dark=True))
        n = c.add(CloudBox(x + 188, 214, "Nube", "", w=140))
        d = c.add(Generic(x + 24, 360, "Cámara o NVR", "Hik-Connect activo", icon="camera", w=304))
        c.add(Arrow((x + 258, 360), n.bottom(), kind="flow"))
        c.add(Arrow((x + 188, 256), s.right(), kind="flow"))
    c.add(text(x + 20, 488, l1, 16, 400, INK2))
    c.add(text(x + 20, 518, l2, 15, 600, {"info": BLUE, "ok": OK, "warn": WARN}[kd], FM))
c.add(text(48, 586, "IP fija y ruta, por IP. Sin IP fija, ISUP. Hik-Connect, solo si aceptás sus límites de grabación.", 18, 600, INK))
c.add(text(48, 622, "Para equipos de otras marcas, ONVIF. Abrir el 8000 o el 80 a internet: no.", 16, 500, INK2))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso2: los mismos datos en los dos lados
c = Canvas(K(2), "Cámara y HikCentral: los mismos datos de los dos lados")
a = c.add(Window(48, 124, 520, 300, "Cámara · Platform Access", rows=[
    ("Tipo", "ISUP"), ("Server address", "192.168.88.10"), ("Port", "7660"), ("Device ID", "LAB-CAM-01"), ("Key", "Ejemplo.2026!")]))
b = c.add(Window(632, 124, 520, 300, "HikCentral · Add Encoding Device", rows=[
    ("Access Protocol", "Hikvision ISUP"), ("Adding mode", "Device ID"), ("Device ID", "LAB-CAM-01"), ("ISUP 5.0: clave", "Ejemplo.2026!"), ("Add Resource to Area", "on")]))
for ya, yb in ((290, 290), (328, 328)):
    pass
c.add(f'<path d="M570 303 C600 303,600 265,630 265" stroke="{OK}" stroke-width="3" fill="none"/>')
c.add(f'<path d="M570 341 C600 341,600 303,630 303" stroke="{OK}" stroke-width="3" fill="none"/>')
c.add(tag(600, 395, "iguales", "ok", 13))
c.add(Note(48, 452, 540, "Antes de cargar la cámara, el SYS tiene que aceptar ISUP: System > Network > Device Access Protocol > Allow ISUP Registration.", title="Del lado del SYS, primero", kind="info"))
c.add(Note(612, 452, 540, "Server address es la IP del SYS que la cámara alcanza. El equipo sale hacia el 7660: no hace falta abrir nada hacia la cámara.", title="La cámara llama", kind="ok"))
c.add(text(48, 644, "Rutas de menú de V2.x; en V3.x pueden cambiar de nombre.", 15, 400, WARN))
save(c, "5-paso2.svg")

# ---------------------------------------------------------------- 5-paso5: si no aparece online
c = Canvas(K(5), "No aparece online: revisá estas cuatro cosas")
items = [("Allow ISUP Registration", "activado en el SYS"), ("Device ID", "idéntico en la cámara y en HikCentral"),
         ("Clave ISUP", "la misma de los dos lados (ISUP 5.0)"), ("Puerto 7660", "alcanzable desde la red de la cámara")]
for i, (t, d) in enumerate(items):
    y = 128 + i * 72
    c.add(rect(48, y, 560, 60, WHITE, LINE2, rx=12))
    c.add(badge(80, y + 30, str(i + 1)))
    c.add(text(112, y + 27, t, 17, 600, INK))
    c.add(text(112, y + 49, d, 15, 400, INK3))
c.add(code(648, 128, 504, "Test-NetConnection 192.168.88.10 -Port 7660", 15, h=48))
c.add(codebox(648, 196, 504, ["ComputerName     : 192.168.88.10", "RemotePort       : 7660", ("TcpTestSucceeded : True", "#9FE0C0")], 15, 26, "SI LLEGA")[0])
c.add(codebox(648, 340, 504, ["RemotePort       : 7660", ("TcpTestSucceeded : False", "#FFB4A3")], 15, 26, "SI NO LLEGA")[0])
c.add(Note(48, 444, 560, "Si da False, el problema está en el camino: firewall del servidor, ruta o VPN. Antes de tocar la cámara, que el puerto conteste.", title="False: es red, no es la cámara", kind="warn"))
c.add(Note(648, 456, 504, "Probalo desde una PC de la misma red que la cámara, no desde el propio servidor.", kind="info"))
save(c, "5-paso5.svg")
