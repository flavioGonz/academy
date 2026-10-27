import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 2.svg: el orden del diagnóstico
c = Canvas(K(), "Capa por capa: de tu puesto hacia afuera")
c.add(NOLIG)
cols = [("1", "ipconfig /all", "¿Mi placa está bien?", "IP, máscara, puerta de enlace y DNS", "Si esto está mal, lo demás no importa."),
        ("2", "ping 192.168.88.1", "¿Llego al gateway?", "el primer salto de la red", "Sin gateway, nada sale de la subred."),
        ("3", "arp -a", "¿El equipo está vivo?", "su MAC en la tabla ARP", "Hay MAC: respondió, aunque el ping falle."),
        ("4", "pathping -n", "¿Dónde se pierde?", "pérdida y demora por salto", "Para destinos en otra red.")]
for i, (n, cmd, q, s, foot) in enumerate(cols):
    x = 48 + i * 284
    c.add(panel(x, 128, 252, 300, None, "info"))
    c.add(badge(x + 34, 166, n, CYAN))
    c.add(text(x + 62, 172, q if len(q) < 20 else q, 17, 600, INK, FD))
    c.add(code(x + 16, 196, 220, cmd, 15))
    svg, _ = wrap(x + 20, 270, s, 220, 16, 500, INK2)
    c.add(svg)
    svg, _ = wrap(x + 20, 350, foot, 220, 15, 400, INK3)
    c.add(svg)
    if i < 3:
        c.add(arrow((x + 256, 278), (x + 280, 278), "flow"))
c.add(panel(48, 456, 1104, 130, None, "warn"))
c.add(text(72, 494, "Un ping que falla no prueba que el equipo esté apagado", 20, 600, WARN, FD))
svg, _ = wrap(72, 528, "Muchos equipos y firewalls bloquean ICMP, que es lo que usa el ping. El Firewall de Windows, por ejemplo, bloquea lo entrante salvo que haya regla. Antes de mandar a alguien al sitio, mirá ARP en su subred.", 1050, 17, 400, INK2)
c.add(svg)
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso2: ping falla, ARP responde
c = Canvas(K(2), "El ping no vuelve, pero la MAC está en la tabla")
c.add(NOLIG)
c.add(Step(65, 141, 2))
c.add(text(94, 147, "Misma subred: 192.168.88.0/24", 17, 600, INK2, FB))
pc = c.add(Laptop(48, 190, "Tu notebook", "192.168.88.10"))
gw = c.add(Generic(470, 176, "Gateway", "192.168.88.1", icon="globe", w=240))
cam = c.add(Camera(470, 300, "Cámara", "192.168.88.20", w=240, hl=WARN))
c.add(Cable(pc.right(), gw.left(), kind="ok", label="ping: responde"))
c.add(Cable(pc.right(), cam.left(), kind="alert", label="ping: no vuelve"))
c.add(tag(800, 340, "bloquea ICMP", "warn", anchor="start"))
sv, h = console(48, 420, 700, [
    ">arp -a",
    ("  Dirección de Internet   Dirección física      Tipo", "#7FA6C9"),
    ("  192.168.88.1            00-11-22-33-44-01     dinámico", "#D9E9F8"),
    ("  192.168.88.20           00-11-22-33-44-20     dinámico", "#9FE3F7"),
], title="Símbolo del sistema", prompt="C:\\> ")
c.add(sv)
c.add(crow(48, 420, 700, 3))
c.add(Note(780, 420, 372, "La cámara contestó la pregunta de ARP: está viva. Lo que no contesta es el ping. MAC de ejemplo.", title="Hay MAC, hay equipo", kind="ok"))
save(c, "2-paso2.svg")

# ---------------------------------------------------------------- 2-paso3: leer pathping
c = Canvas(K(3), "pathping: buscá el salto donde empieza la pérdida")
c.add(NOLIG)
c.add(Step(65, 141, 3))
c.add(code(94, 122, 560, "pathping -n -q 10 -h 5 203.0.113.10", 16))
rows = [["1", "192.168.88.1", "0/10 = 0%", "tu gateway"],
        ["2", "198.51.100.1", "0/10 = 0%", "proveedor"],
        ["3", "203.0.113.1", "4/10 = 40%", "acá empieza"],
        ["4", "203.0.113.10", "4/10 = 40%", "sigue hasta el destino"]]
c.add(Table(48, 186, ["Salto", "Dirección", "Perdidos/Enviados", "Lectura"], rows, [110, 240, 260, 494], hl_row=2, row_h=52, mono_cols=(1, 2)))
c.add(Note(48, 470, 540, "La pérdida que aparece en un salto y sigue en todos los siguientes es la que importa: el problema está entre el salto 2 y el 3.", title="Cómo se lee", kind="info"))
c.add(Note(612, 470, 540, "-n no resuelve nombres, -q 10 baja de 100 a 10 consultas por salto y -h 5 corta a 5 saltos. Valores de ejemplo.", title="Para que no tarde", kind="info"))
save(c, "2-paso3.svg")
