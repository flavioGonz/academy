import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 3.svg: hay alguien, atiende, con qué nombre
c = Canvas(K(), "¿Hay alguien, atiende el servicio, qué nombre ve?")
c.add(NOLIG)
rows = [("1", "¿Hay alguien?", "ping · arp -a", "MAC en la tabla", "ok", "La red llega al equipo."),
        ("2", "¿El servicio atiende?", "Test-NetConnection 192.168.88.20 -Port 554", "TcpTestSucceeded : True", "ok", "El puerto exacto responde."),
        ("3", "¿Qué nombre ve la app?", "Resolve-DnsName vms-lab", "192.168.88.50", "ok", "Igual que una aplicación de Windows.")]
for i, (n, q, cmd, res, kd, s) in enumerate(rows):
    y = 128 + i * 118
    c.add(panel(48, y, 1104, 102, None, "info"))
    c.add(badge(84, y + 51, n, CYAN))
    c.add(text(116, y + 42, q, 19, 600, INK, FD))
    c.add(text(116, y + 74, s, 15, 400, INK3, FB))
    c.add(code(400, y + 30, 500, cmd, 15))
    c.add(tag(1132, y + 57, res, kd, size=14, anchor="end"))
c.add(panel(48, 488, 540, 150, "Get-NetTCPConnection -State Listen", "soft", title_size=16))
c.add(text(72, 552, "0.0.0.0", 17, 600, BLUE, FM))
c.add(text(176, 552, "escucha en todas las placas", 16, 400, INK2, FB))
c.add(text(72, 590, "192.168.88.10", 17, 600, BLUE, FM))
c.add(text(236, 590, "solo en esa placa", 16, 400, INK2, FB))
c.add(Note(612, 488, 540, "No digas \"no hay red\" hasta probar el puerto exacto del servicio: el ping dice que hay alguien, no que el servicio atiende.", title="Regla", kind="ok"))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso2: quién escucha
c = Canvas(K(2), "Qué escucha en tu equipo y qué programa es")
c.add(NOLIG)
c.add(Step(65, 141, 2))
c.add(text(94, 147, "Valores de ejemplo: el número de proceso cambia en cada equipo", 17, 600, INK2, FB))
sv, h = console(48, 176, 1104, [
    ">Get-NetTCPConnection -State Listen | Sort-Object LocalPort |",
    ">>Select-Object LocalAddress, LocalPort, OwningProcess",
    ("LocalAddress    LocalPort  OwningProcess", "#7FA6C9"),
    ("0.0.0.0         135        1104", "#9FE3F7"),
    ("192.168.88.10   139        4", "#D9E9F8"),
])
c.add(sv)
c.add(crow(48, 176, 1104, 3))
sv2, h2 = console(48, 404, 700, [
    ">Get-Process -Id 1104",
    ("ProcessName : svchost", "#9FE3F7"),
])
c.add(sv2)
c.add(arrow((300, 324), (300, 400), "flow"))
c.add(text(316, 370, "OwningProcess → Get-Process", 15, 600, BLUE, FM))
c.add(Note(780, 404, 372, "0.0.0.0 es todas las placas. Si figura la IP de una placa, el servicio solo atiende por esa.", title="LocalAddress", kind="info"))
c.add(Note(48, 556, 1104, "Lo mismo a la vieja usanza: netstat -ano | findstr LISTENING. La última columna es el mismo número de proceso.", kind="info"))
save(c, "3-paso2.svg")

# ---------------------------------------------------------------- 3-paso5: hosts, Resolve-DnsName y nslookup
c = Canvas(K(5), "Una línea en hosts: una herramienta la ve, la otra no")
c.add(NOLIG)
c.add(Step(65, 141, 5))
c.add(text(94, 147, "C:\\Windows\\System32\\drivers\\etc\\hosts (como administrador)", 17, 600, INK2, FM))
c.add(code(48, 172, 520, "192.168.88.50   vms-lab", 18, h=46))
c.add(panel(48, 252, 540, 180, None, "ok"))
c.add(Mark(86, 292, ok=True))
c.add(text(118, 299, "Resolve-DnsName vms-lab", 18, 600, OK, FM))
svg, _ = wrap(72, 340, "Usa el resolvedor de Windows: archivo hosts, caché y después DNS. Encuentra 192.168.88.50, como lo haría el VMS.", 490, 16, 400, INK2)
c.add(svg)
c.add(panel(612, 252, 540, 180, None, "alert"))
c.add(Mark(650, 292, ok=False))
c.add(text(682, 299, "nslookup vms-lab", 18, 600, ALERT, FM))
svg, _ = wrap(636, 340, "Pregunta solo al servidor DNS: no lee hosts ni la caché. Además le agrega los sufijos de búsqueda a un nombre sin punto final.", 490, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 460, 1104, "Al terminar, borrá la línea de hosts. Empezá con Resolve-DnsName y usá nslookup para comparar y aislar fallas del resolvedor.", kind="warn"))
save(c, "3-paso5.svg")

# ---------------------------------------------------------------- 3-t2: dos caminos para un nombre (fija, teoría)
c = Canvas("Windows · Teoría", "Dos caminos para resolver un nombre")
c.add(NOLIG)
app = c.add(Box(48, 168, 300, 90, "Resolve-DnsName", "igual que el VMS", icon=ICON["laptop"]))
ns = c.add(Box(48, 440, 300, 90, "nslookup", "consulta directa", icon=ICON["laptop"]))
c.add(Zone(392, 150, 760, 128, "resolvedor de Windows", BLUE))
st = [("archivo hosts", 412, None), ("caché DNS", 598, None), ("servidor DNS", 784, CYAN), ("LLMNR · mDNS", 970, None)]
for i, (t, x, hl) in enumerate(st):
    c.add(rect(x, 180, 164, 70, SOFT if hl else WHITE, hl or LINE2, rx=12, sw=2.5 if hl else 2))
    c.add(mid(x + 82, 222, t, 16, 600, INK, FB))
    if i < 3:
        c.add(arrow((x + 166, 215), (x + 184, 215), "flow"))
c.add(text(970, 300, "si DNS no lo encuentra", 15, 500, INK3, FB))
c.add(arrow(app.right(), (408, 215), "flow"))
c.add(Cable(ns.right(), (866, 254), kind="logical", label="solo el servidor DNS", label_at=0.42))
c.add(panel(612, 420, 540, 150, None, "warn"))
c.add(text(636, 458, "nslookup vms-lab", 17, 600, WARN, FM))
c.add(text(636, 488, "prueba vms-lab.sufijo1, vms-lab.sufijo2, …", 16, 500, INK2, FM))
c.add(text(636, 518, "antes del nombre tal cual. Con punto", 16, 400, INK2, FB))
c.add(text(636, 544, "final (vms-lab.) pregunta solo ese.", 16, 400, INK2, FB))
save(c, "3-t2.svg")
