import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 12.svg: la escalera de abajo arriba
c = Canvas(K(), "Equipo offline: subí la escalera desde abajo")
rungs = [("Físico", "cable, enlace, alimentación", "luces del puerto, PoE"),
         ("IP y gateway", "dirección, máscara, gateway", "ping 192.168.88.1 y al equipo"),
         ("DNS", "si usa dominio o Hik-Connect", "Resolve-DnsName dev.hik-connect.com"),
         ("Servicio habilitado", "Platform Access, ISUP, ONVIF", "la casilla activada en el equipo"),
         ("Puertos", "contra la Communication Matrix", "Test-NetConnection -Port 7660")]
for i, (t, d, cmd) in enumerate(rungs):
    y = 502 - i * 90
    x = 48 + i * 40
    c.add(rect(x, y, 600, 76, WHITE if i else SOFT, LINE2 if i else BLUE, rx=14))
    c.add(badge(x + 34, y + 38, str(i + 1)))
    c.add(text(x + 64, y + 34, t, 19, 600, INK))
    c.add(text(x + 64, y + 60, d, 15, 400, INK3))
    c.add(text(x + 640, y + 44, cmd, 15, 500, BLUE, FM))
c.add(f'<path d="M30 574V146" stroke="{CYAN}" stroke-width="4" marker-end="url(#a-cyan)"/>')
c.add(text(48, 628, "Si el escalón 2 falla, no tiene sentido mirar puertos. Anotá en qué escalón quedó.", 17, 600, INK))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso2: los puertos clave
c = Canvas(K(2), "Los puertos que probás, y quién habla con quién")
pc = c.add(Laptop(48, 140, "Puesto o navegador", "Web y Control Client", w=270))
sy = c.add(Generic(470, 140, "SYS + Streaming Gateway", "192.168.88.10", icon="server", w=330, dark=True))
cm = c.add(Camera(882, 140, "Cámara", "192.168.88.21", w=270))
c.add(Arrow((318, 168), (470, 168), label="80 · 443"))
c.add(Arrow((318, 206), (470, 206), label="559 vivo web", label_dy=34))
c.add(Arrow((800, 168), (882, 168)))
c.add(text(808, 150, "8000", 15, 600, BLUE, FM))
c.add(Arrow((882, 206), (800, 206), kind="ok"))
c.add(text(808, 246, "7660", 15, 600, OK, FM))
c.add(Table(48, 300, ["Puerto", "Destino", "Para qué"], [
    ["80 / 443", "SYS", "Web, Control y Mobile Client"],
    ["7660", "SYS", "registro de equipos ISUP"],
    ["554", "Streaming Gateway", "video RTSP hacia los clientes"],
    ["559", "Streaming Gateway", "vivo en Chrome y Firefox"],
    ["8000", "equipo", "alta por IP con protocolo privado"],
], [170, 300, 634], row_h=42, mono_cols=(0,)))
c.add(code(48, 566, 1104, "Test-NetConnection 192.168.88.21 -Port 8000  ·  192.168.88.10 -Port 7660  ·  192.168.88.10 -Port 559", 14, h=44))
c.add(text(48, 642, "Fuente: Communication Matrix V2.4.1. En V3.x, confirmá contra la matriz de esa versión.", 15, 400, INK3))
save(c, "12-paso2.svg")

# ---------------------------------------------------------------- 12-paso5: máximo de streams
c = Canvas(K(5), "\"Maximum number of streams\": son conexiones, no ancho de banda")
c.add(panel(48, 124, 540, 400, "Cada puesto pide directo al NVR", "alert"))
n1 = c.add(Generic(72, 420, "NVR", "tope de conexiones remotas", icon="server", w=492, hl=ALERT))
for k in range(5):
    x = 82 + k * 96
    c.add(rect(x, 190, 84, 56, WHITE, LINE2, rx=10))
    c.add(icon(x + 26, 204, "laptop", BLUE, 1.3))
    c.add(f'<path d="M{x + 42} 248 L{318} 418" stroke="{ALERT}" stroke-width="2"/>')
c.add(text(72, 300, "", 15))
c.add(tag(318, 345, "una conexión por pedido", "alert", 14))
c.add(panel(612, 124, 540, 400, "Con Streaming Server", "ok"))
for k in range(5):
    x = 646 + k * 96
    c.add(rect(x, 170, 84, 56, WHITE, LINE2, rx=10))
    c.add(icon(x + 26, 184, "laptop", BLUE, 1.3))
    c.add(f'<path d="M{x + 42} 228 L882 282" stroke="{OK}" stroke-width="2"/>')
ss = c.add(Generic(752, 284, "Streaming Server", "reparte el video", icon="server", w=260, dark=True))
n2 = c.add(Generic(636, 420, "NVR", "menos conexiones directas", icon="server", w=492, hl=OK))
c.add(Cable(ss.bottom(), (882, 420), kind="ok", arrow=False))
c.add(Note(48, 548, 1104, "En el caso del soporte de Hikvision USA, el NVR llegaba a 128 conexiones. Antes de tocar el ancho de banda, contá cuántos clientes están pidiendo video al NVR.", kind="info"))
save(c, "12-paso5.svg")
