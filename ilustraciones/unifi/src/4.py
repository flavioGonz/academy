import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 4.svg: Site Manager, todo de salida
c = Canvas(K(), "Site Manager: todo sale del sitio, nada entra")
sm = c.add(CloudBox(450, 128, "Site Manager", "unifi.ui.com", w=300))
tec = c.add(Laptop(48, 128, "Técnico", "cuenta de la empresa", w=300))
c.add(arrow(tec.right(), sm.left()))
c.add(text(852, 160, "Ve todas las consolas", 17, 600, INK, FB))
c.add(text(852, 186, "y servidores de la cuenta.", 16, 400, INK2, FB))
c.add(text(852, 212, "La configuración sigue", 16, 400, INK2, FB))
c.add(text(852, 236, "en cada controlador.", 16, 400, INK2, FB))
sites = [(48, "Cliente A", "UCG"), (430, "Cliente B", "CloudKey"), (812, "Oficina", "UniFi OS Server")]
for x, nm, ct in sites:
    c.add(Zone(x, 372, 340, 150, nm))
    c.add(Generic(x + 20, 404, ct, "Remote Management", icon="server", w=300, dark=True))
    c.add(wire([(x + 170, 400), (x + 170, 300), (600, 300), (600, 216)], kind="ok", arrow=True))
c.add(pill(600, 344, "salida TCP 443 y 8883", fg=OK, size=15))
c.add(tag(330, 344, "DNS UDP 53", "info"))
c.add(tag(872, 344, "NTP UDP 123", "info"))
c.add(Note(48, 544, 1104, "No hace falta abrir ningún puerto de entrada. Si un sitio no aparece: Remote Management apagado, salida 443 u 8883 bloqueada, DNS o NTP bloqueados, o entraste con otra cuenta UI. La lista sale de UniHosted, que cita a Ubiquiti: confirmala en cada sitio.", kind="ok"))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso2: si no aparece
c = Canvas(K(2), "Si la consola no aparece, revisá estas cuatro")
items = [("1", "Remote Management apagado", "Settings > Control Plane > Console", "warn"),
         ("2", "Salida TCP 443 u 8883 bloqueada", "firewall del sitio, de salida", "warn"),
         ("3", "DNS (UDP 53) o NTP (UDP 123) bloqueados", "sin hora ni nombres no conecta", "warn"),
         ("4", "Entraste con otra cuenta UI", "solo ves lo que esa cuenta administra", "warn")]
for i, (n_, a, b, kd) in enumerate(items):
    y = 128 + i * 92
    c.add(rect(48, y, 600, 80, WHITE, LINE2, rx=12))
    c.add(f'<circle cx="84" cy="{y + 40}" r="18" fill="{WARN}"/>' + mid(84, y + 46, n_, 17, 700, WHITE, FD))
    c.add(text(116, y + 34, a, 18, 600, INK, FB))
    c.add(text(116, y + 60, b, 15, 500, INK3, FM))
cb, h = codebox(684, 128, 468, [("PS> Test-NetConnection unifi.ui.com -Port 443", "#9FE3B5"), ("    TcpTestSucceeded : True", "#D9E9F8"), ("PS> Resolve-DnsName unifi.ui.com", "#9FE3B5"), ("    devuelve direcciones: DNS anda", "#7FA6C9")], size=15, title="DESDE UNA PC DE ESA RED")
c.add(cb)
c.add(Step(684, 128, 2))
c.add(Note(684, 128 + h + 24, 468, "Si TcpTestSucceeded da False, el 443 de salida está cerrado. El 8883 se revisa en las reglas del firewall: TCP 443 y 8883, UDP 53 y UDP 123, de salida.", kind="info"))
save(c, "4-paso2.svg")

# ---------------------------------------------------------------- 4-paso4: cuenta de la empresa y roles
c = Canvas(K(4), "Consolas en la cuenta de la empresa, técnicos con rol")
own = c.add(Generic(400, 128, "Cuenta UI de la empresa", "dueña de las consolas", icon="shield", w=400, dark=True))
for i, nm in enumerate(["Consola cliente A", "Consola cliente B", "Consola cliente C"]):
    x = 120 + i * 330
    b = c.add(Generic(x, 280, nm, "", icon="server", w=290))
    c.add(wire([(600, 212), (600, 246), (x + 145, 246), (x + 145, 276)], kind="logical", arrow=True))
adm = [("Técnico 1", "rol: solo ver"), ("Técnico 2", "rol: solo el sitio B")]
for i, (a, r) in enumerate(adm):
    y = 410 + i * 0
    x = 120 + i * 330
    c.add(Person(x, 408, a, r, w=290))
c.add(Step(120, 408, 4))
c.add(panel(780, 408, 372, 84, None, "alert"))
c.add(Mark(814, 450, ok=False))
c.add(text(846, 444, "Consola en la cuenta", 17, 600, ALERT, FB))
c.add(text(846, 468, "personal de un técnico", 17, 600, ALERT, FB))
c.add(Note(48, 520, 1104, "Cuando alguien se va, le sacás el acceso y no perdés nada. Para muchos clientes, Fabrics agrupan sitios con los mismos administradores y roles (abril de 2026) y MSP Groups dan acceso a tu equipo (julio de 2026).", kind="info"))
save(c, "4-paso4.svg")

# ---------------------------------------------------------------- 4-paso5: la planilla de sitios
c = Canvas(K(5), "Una fila por cliente: lo que buscás a las tres de la mañana")
c.add(Table(48, 140, ["Cliente", "Host", "UniFi OS", "Network", "Dueño", "Admins", "Últ. backup"],
            [["Cliente A", "UCG", "6.0.x", "11.0.97", "empresa", "2", "dd/mm"],
             ["Cliente B", "CloudKey", "5.x", "10.6.x", "empresa", "1", "dd/mm"],
             ["Oficina", "UOS Server", "5.1.x", "10.6.x", "empresa", "3", "dd/mm"]],
            [150, 170, 140, 150, 160, 140, 194], mono_cols=(1, 2, 3, 6), row_h=48))
c.add(text(48, 360, "Valores de ejemplo: cada fila sale de la consola de ese cliente.", 15, 400, INK3, FB))
c.add(Step(48, 140, 5))
c.add(Note(48, 396, 360, "Con la de Network decidís qué notas de versión leer antes de actualizar.", title="Versiones", kind="info"))
c.add(Note(420, 396, 360, "Siempre la cuenta de la empresa, nunca la de un técnico.", title="Dueño", kind="ok"))
c.add(Note(792, 396, 360, "La fecha te dice si podés actualizar hoy o primero hay que bajar uno.", title="Último backup", kind="warn"))
save(c, "4-paso5.svg")
