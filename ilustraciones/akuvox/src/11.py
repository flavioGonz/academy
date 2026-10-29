from _akv import *

# ---------- 11.svg: el portero en su VLAN
c = Canvas("Akuvox", "El portero vive en su VLAN y habla con tres")
c.add(Zone(410, 250, 300, 200, "VLAN porteros 10.10.10.0/24", CYAN))
p = c.add(Generic(440, 310, "Portero", "10.10.10.21", icon="bell", w=250, hl=CYAN))
dst = [("Central", "10.10.20.10", "server", "UDP 5060 + RTP", 150),
       ("NVR", "10.10.30.10", "camera", "TCP 554 (RTSP)", 320),
       ("Gestión", "10.10.40.0/28", "laptop", "TCP 80/443", 490)]
for ttl, ip, ic, port, y in dst:
    b = c.add(Generic(890, y, ttl, ip, icon=ic, w=262, hl=OK))
    c.add(Arrow(p.right(), b.left(), kind="ok", label=port, label_at=0.62, label_dy=-4))
inet = c.add(Internet(48, 170, "Internet", "sin reenvío de puertos", w=290))
usr = c.add(Generic(48, 450, "Red de usuarios", "PCs, Wi-Fi", icon="user", w=290))
c.add(Arrow(inet.right(), p.left(-14), kind="alert"))
c.add(Arrow(usr.right(), p.left(14), kind="alert"))
c.add(Mark(372, 268, ok=False))
c.add(Mark(372, 446, ok=False))
c.add(text(400, 620, "Todo lo demás: denegado.", 18, 600, INK, FD))
c.add(text(640, 620, "Cámara, micrófono y relé en la calle no se exponen a internet.", 16, 500, INK3))
save(c, "11.svg")

# ---------- 11-paso2.svg: escanear desde la red de usuarios
c = Canvas("Akuvox · Paso 2", "Escaneá el portero desde la red de usuarios")
c.add(Terminal(48, 140, 1104, ["nmap -sS -sU -p T:22,23,80,443,554,5060,8080,U:5060,8500 10.10.10.21"], title="PC EN LA RED DE USUARIOS"))
c.add(Step(48, 140, 2))
pc = c.add(Generic(48, 300, "PC de usuarios", "escanea", icon="laptop", w=250))
fw = c.add(Generic(400, 300, "Firewall", "reglas de la VLAN", icon="shield", w=250))
po = c.add(Generic(752, 300, "Portero", "10.10.10.21", icon="bell", w=250))
c.add(Arrow(pc.right(), fw.left()))
c.add(Arrow(fw.right(), po.left(), kind="alert"))
ports = ["22", "23", "80", "443", "554", "5060", "8080", "U 5060", "U 8500"]
x = 48
for prt in ports:
    c.add(Chip(x, 460, prt, "alert"))
    x += len(prt) * 9.2 + 26 + 10
c.add(text(48, 510, "Desde la red de usuarios, ninguno debería responder.", 17, 600, INK))
c.add(Note(48, 540, 1104, "Lo que conteste es un hueco: filtralo en el firewall y volvé a escanear (paso 3). Solo equipos propios o con autorización escrita del cliente.", kind="warn", size=15))
save(c, "11-paso2.svg")

# ---------- 11-paso5.svg: Prevent SIP Hacking
c = Canvas("Akuvox · Paso 5", "Que el portero atienda solo a quien conoce")
po = c.add(Intercom(540, 150, "Portero", "Prevent SIP Hacking"))
a = c.add(Generic(60, 170, "Central", "10.10.20.10 · en contactos", icon="server", w=330, hl=OK))
b = c.add(Generic(60, 390, "IP desconocida", "llamada SIP directa", icon="globe", w=330, hl=ALERT))
c.add(Arrow(a.right(), (530, 230), kind="ok", label="llamada", label_dy=-12))
c.add(Arrow(b.right(), (530, 340), kind="alert", label="llamada", label_dy=-12))
c.add(Chip(760, 230, "atiende", "ok", mono=False))
c.add(Chip(760, 340, "rechaza", "alert", mono=False))
c.add(Mark(735, 222, ok=True))
c.add(Mark(735, 332, ok=False))
c.add(Window(760, 400, 392, 130, "Web del portero", path="Account > Advanced > Call", rows=[("Prevent SIP Hacking", "activado")], hl=0))
c.add(Step(60, 170, 5))
c.add(text(60, 600, "Antes de activarlo, verificá que la central esté en contactos: si no, deja de recibir sus llamadas.", 16, 500, WARN))
save(c, "11-paso5.svg")
