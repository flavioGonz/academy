from _oai import *

# ---------- 10.svg: la cadena
c = Canvas("OmniAccess Intrusión · Lección 10", "De la cámara al monitor, un eslabón por vez")
links = [("Regla armada", "punto verde en la pared"),
         ("Vinculación", "Notificar al centro"),
         ("Servidor de alarma", "campana · Probar reporte"),
         ("Red al :10000", "curl desde la red de cámaras"),
         ("Alta con su IP o MAC", "si no, entra sin cámara")]
for i, (t, d) in enumerate(links):
    x = 48 + i * 224
    c.add(panel(x, 160, 204, 130, None, kind="info"))
    c.add(f'<circle cx="{x + 30}" cy="194" r="16" fill="{CYAN}"/>')
    c.add(text(x + 30, 200, str(i + 1), 16, 700, WHITE, FD, anchor="middle"))
    s, _ = wrap(x + 56, 200, t, 140, 17, 600, INK)
    c.add(s)
    s, _ = wrap(x + 20, 252, d, 170, 14, 500, INK3)
    c.add(s)
    if i < 4:
        c.add(Arrow((x + 206, 225), (x + 222, 225), kind="flow"))
c.add(text(48, 140, "PARA QUE LLEGUE", 13, 600, INK3, FM, ls=1.2))
c.add(text(48, 340, "PARA QUE LLEGUE COMPLETO", 13, 600, INK3, FM, ls=1.2))
extra = [("Foto propia", "clave de la cámara", "camera"), ("Grabación", "NVR y canal vinculados", "server"), ("Hora", "Sincronizar hora", "bolt")]
for i, (t, d, ic) in enumerate(extra):
    x = 48 + i * 300
    c.add(Generic(x, 360, t, d, ic, w=280))
c.add(Note(48, 480, 540, "Dahua: Verificar suscripción tiene que decir «Suscripción activa». «NVR no accesible» es red o credenciales del NVR.", kind="info", size=15))
c.add(Note(612, 480, 540, "No resetees la cámara para probar: se pierden la regla, el horario y el servidor de alarma.", kind="alert", size=15))
save(c, "10.svg")

# ---------- 10-paso5.svg: leer el curl
c = Canvas("OmniAccess Intrusión · Lección 10 · Paso 5", "Cualquier código es puerto abierto; timeout es red")
c.add(Generic(48, 150, "PC en la red de cámaras", "192.0.2.30", "laptop", w=320))
c.add(Arrow((372, 192), (464, 192), label=":10000", kind="flow", label_dy=-12))
c.add(Generic(468, 150, "Servidor OmniAccess", "192.0.2.10 · webhooks", "server", w=330, dark=True))
c.add(Terminal(48, 280, 540, ["$ curl -s -o /dev/null -w \"%{http_code}\" \\", "  -X POST 192.0.2.10:10000/api/webhooks/hikvision", ("200", "#8FE3B5")], title="RESPONDE"))
c.add(Terminal(612, 280, 540, ["$ curl -s -o /dev/null -w \"%{http_code}\" \\", "  -X POST 192.0.2.10:10000/api/webhooks/hikvision", ("000  (timeout)", "#FF9F8A")], title="NO RESPONDE"))
c.add(Note(48, 420, 540, "El puerto está abierto: el problema está antes (regla, vinculación, servidor de alarma) o en el alta.", title="Responde", kind="ok", size=15))
c.add(Note(612, 420, 540, "Revisá firewall, VLAN y ruteo entre las cámaras y el servidor antes de tocar la cámara.", title="Timeout", kind="alert", size=15))
c.add(Step(48, 280, 5))
save(c, "10-paso5.svg")
