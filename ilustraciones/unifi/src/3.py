import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 3.svg: tres caminos para encontrar el controlador
c = Canvas(K(), "Cómo se entera el AP de dónde está su controlador")
c.add(Zone(48, 140, 330, 290, "Oficina · 10.10.10.0/24"))
ctl = c.add(Generic(68, 236, "UniFi OS Server", "10.10.10.5", icon="server", w=290, dark=True))
c.add(text(88, 360, "unifi.example.com", 16, 500, BLUE, FM))
c.add(Zone(470, 140, 682, 290, "Sitio remoto · 192.168.88.0/24"))
rt = c.add(Generic(500, 176, "MikroTik del sitio", "DHCP y DNS", icon="server", w=270))
nb = c.add(Laptop(500, 318, "Notebook", "SSH al AP", w=270))
ap = c.add(APNode(1040, 284, "AP", "192.168.88.20"))
c.add(arrow((770, 204), (994, 262), kind="ok"))
c.add(arrow((770, 232), (994, 278), kind="ok"))
c.add(tag(860, 196, "A · option 43", "ok"))
c.add(tag(880, 258, "B · DNS unifi", "ok"))
c.add(arrow((770, 360), (996, 302), kind="flow"))
c.add(tag(880, 362, "C · set-inform", "warn"))
c.add(wire([(1040, 376), (1040, 470), (213, 470), (213, 324)], kind="flow", arrow=True))
c.add(pill(626, 476, "http://unifi.example.com:8080/inform", fg=BLUE, size=15))
c.add(Note(48, 512, 540, "Option 43 y DNS los entrega la red del sitio: sobreviven a reinicios y actualizaciones del AP.", title="A y B: lo que recomienda Ubiquiti", kind="ok"))
c.add(Note(612, 512, 540, "Queda en la memoria del equipo. Funciona, pero tras un reinicio puede volver a unifi:8080/inform.", title="C: el plan B", kind="warn"))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso1: option 43 byte a byte
c = Canvas(K(1), "La option 43 lleva la IP del controlador en hex")
c.add(code(48, 128, 1104, "/ip dhcp-server option add name=unifi-inform code=43 value=0x01040A0A0A05", size=17, h=46))
bytes_ = ["01", "04", "0A", "0A", "0A", "05"]
for i, b in enumerate(bytes_):
    x = 150 + i * 150
    kd = CYAN if i < 2 else BLUE
    c.add(rect(x, 220, 120, 84, WHITE, kd, rx=14, sw=3))
    c.add(mid(x + 60, 274, b, 34, 600, INK, FM))
    if i >= 2:
        c.add(mid(x + 60, 336, str(int(b, 16)), 24, 600, BLUE, FM))
def brace(x1, x2, y, label, sub, col):
    return (f'<path d="M{x1} {y}V{y + 14}H{x2}V{y}" fill="none" stroke="{col}" stroke-width="2.5"/>'
            + mid((x1 + x2) / 2, y + 44, label, 18, 600, INK, FB) + mid((x1 + x2) / 2, y + 68, sub, 15, 400, INK3, FM))
c.add(brace(160, 260, 312, "subopción", "01 = 1", CYAN))
c.add(brace(310, 410, 312, "largo", "4 bytes", CYAN))
c.add(brace(460, 1010, 360, "la IP del controlador", "0A.0A.0A.05 = 10.10.10.5", BLUE))
c.add(Step(150, 220, 1))
c.add(Note(48, 478, 540, "Con 10.10.10.20 sería 0x01040A0A0A14: cada número de la IP pasa a dos dígitos hexadecimales (20 = 14).", title="Para otra IP", kind="info"))
c.add(Note(612, 478, 540, "Si el sitio tiene gateway UniFi, el mismo dato va en la red, campo Option 43 Application Host Address.", title="Con gateway UniFi", kind="ok"))
save(c, "3-paso1.svg")

# ---------------------------------------------------------------- 3-paso4: anatomía de la URL de inform
c = Canvas(K(4), "La URL de inform, pieza por pieza")
parts = [("http://", "http, no https", 150), ("unifi.example.com", "nombre DNS mejor que IP", 330), (":8080", "puerto 8080", 140), ("/inform", "termina así", 150)]
x = 60
for s, lab, w in parts:
    c.add(rect(x, 140, w, 66, WHITE, BLUE, rx=12, sw=2.5))
    c.add(mid(x + w / 2, 182, s, 22, 600, INK, FM))
    c.add(mid(x + w / 2, 236, lab, 16, 500, OK, FB))
    x += w + 14
c.add(Mark(944, 172, ok=True))
c.add(text(974, 178, "así adopta", 18, 600, OK, FB))
c.add(Mark(80, 292, ok=False))
c.add(text(112, 286, "https:// o un puerto que no es 8080", 18, 600, ALERT, FM))
c.add(text(112, 312, "Un lector de LazyAdmin dejó sus AP \"en el limbo\" así.", 16, 400, INK2, FB))
cb, h = codebox(48, 352, 640, [("$ ssh ubnt@192.168.88.20", "#9FE3B5"), "# set-inform http://unifi.example.com:8080/inform", "# info", ("  -> pendiente en el controlador: Adopt", "#7FA6C9"), "# set-inform http://unifi.example.com:8080/inform", ("  -> una vez más, para completar la asociación", "#7FA6C9")], size=15, title="PLAN B POR SSH")
c.add(cb)
c.add(Step(48, 352, 4))
c.add(Note(716, 352, 436, "Sikich avisa que a veces hay que repetir set-inform más de una vez para que el equipo termine de asociarse.", title="Por qué se repite", kind="info"))
c.add(Note(716, 500, 436, "Lo que entra por SSH puede perderse tras un reinicio: mirá el sitio después de cada actualización.", kind="warn"))
save(c, "3-paso4.svg")

# ---------------------------------------------------------------- 3-paso5: Inform Host con Override
c = Canvas(K(5), "Con NAT o contenedor, marcá Override en Inform Host")
c.add(Zone(48, 150, 420, 300, "VM con NAT o contenedor"))
c.add(Generic(78, 196, "Controlador", "IP interna, solo adentro", icon="server", w=360, dark=True))
c.add(text(78, 340, "Hacia afuera se lo alcanza como:", 16, 400, INK2, FB))
c.add(text(78, 370, "unifi.example.com", 18, 600, BLUE, FM))
c.add(Window(530, 140, 622, 190, "UniFi Network", path="Settings > System > Advanced", rows=[("Inform Host", "unifi.example.com"), ("Override", "marcado")], hl=1))
c.add(Step(530, 140, 5))
c.add(APNode(620, 430, "", ""))
c.add(Mark(652, 398, ok=False))
c.add(text(680, 412, "Sin Override", 17, 600, ALERT, FB))
c.add(text(680, 436, "el AP recibe la IP interna y no llega", 16, 400, INK2, FB))
c.add(APNode(620, 540, "", ""))
c.add(Mark(652, 508, ok=True))
c.add(text(680, 522, "Con Override", 17, 600, OK, FB))
c.add(text(680, 546, "el AP recibe un nombre alcanzable", 16, 400, INK2, FB))
c.add(Note(48, 480, 420, "Abrí el 8080 solo hacia las IP de tus sitios o por VPN, nunca a todo internet.", title="El puerto 8080", kind="alert"))
save(c, "3-paso5.svg")
