import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 8.svg: deny por defecto
c = new(None, "Deny por defecto: entra solo lo que el equipo sirve")
srv = Box(500, 150, 240, 380, "Servidor", "192.168.88.50", dark=True, icon=ICON["shield"])
c.add(srv)
c.add(Person(48, 150, "Notebook de gestión", "10.10.10.25", w=290))
c.add(Internet(48, 298, "Internet", "203.0.113.7", w=290))
c.add(Generic(48, 446, "Cliente del servicio", "red local", icon="laptop", w=290))
c.add(Cable((338, 192), (500, 192), "ok", label="22/tcp", arrow=True, bend="straight"))
c.add(Cable((338, 340), (452, 340), "alert", label="22/tcp", arrow=True, bend="straight"))
c.add(Mark(476, 340, False))
c.add(Cable((338, 488), (500, 488), "ok", label="lo que sirve", arrow=True, bend="straight"))
c.add(Cable((740, 340), (870, 340), "ok", arrow=True, bend="straight"))
c.add(text(878, 334, "saliente: permitido", 17, 600, OK, FB))
c.add(text(878, 358, "apt, DNS, NTP", 15, 500, INK3, FM))
c.add(Table(780, 410, ["Equipo", "Herramienta"], [["Ubuntu", "ufw (viene apagado)"], ["Debian 13", "nftables"]], [140, 232], row_h=38))
c.add(Note(780, 136, 372, "Entrante: deny. SSH primero, y solo desde la red de gestión. Después, lo que el equipo sirve.", title="El orden", kind="ok"))
c.add(Note(48, 590, 1104, "Antes de filtrar, que el servicio no escuche donde no hace falta: el firewall es la segunda capa.", kind="info"))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso1: qué escucha y dónde
c = new(1, "ss -tlnp: qué escucha y en qué dirección")
svg, h = term(48, 124, 1104, ["$ sudo ss -tlnp",
                              ("State   Local Address:Port   Process", T_COM),
                              ("LISTEN  0.0.0.0:22             users:((\"sshd\",...))", "#FFFFFF"),
                              ("LISTEN  [::]:22                users:((\"sshd\",...))", "#FFFFFF"),
                              ("LISTEN  127.0.0.1:5432         users:((\"postgres\",...))", "#FFFFFF")], "TERMINAL · EJEMPLO", size=17, lh=32)
c.add(svg)
cw = 17 * 0.6
X = 64
def ly(k): return 124 + 32 + 4 + (k + 0.6) * 32
c.add(f'<rect x="{X + cw * 8 - 3}" y="{ly(2) - 23}" width="{cw * 10 + 6}" height="64" rx="6" fill="none" stroke="{T_WARN}" stroke-width="2.5"/>')
c.add(f'<rect x="{X + cw * 8 - 3}" y="{ly(4) - 23}" width="{cw * 14 + 6}" height="31" rx="6" fill="none" stroke="{T_OK}" stroke-width="2.5"/>')
y = 124 + h + 30
c.add(box(48, y, 352, 170, "0.0.0.0 y [::]", ["Todas las interfaces, IPv4", "e IPv6: lo ve la red.", "Es lo que hay que filtrar."], kind="warn"))
c.add(box(424, y, 352, 170, "127.0.0.1", ["Solo el propio equipo.", "Desde la red no llega,", "con o sin firewall."], kind="ok"))
c.add(box(800, y, 352, 170, "Process", ["Qué programa escucha.", "Si no lo reconocés,", "averiguá antes de abrir."], kind="info"))
save(c, "8-paso1.svg")

# ---------------------------------------------------------------- 8-paso4: verificar desde otra máquina
c = new(4, "Verificá desde otra máquina: abierto, cerrado o filtrado")
svg, h = term(48, 124, 1104, ["$ nc -zv 192.168.88.50 22",
                              ("Connection to 192.168.88.50 22 port [tcp/ssh] succeeded!", T_OK),
                              "$ nmap -Pn -p 22,80,443 192.168.88.50",
                              ("22/tcp   open      ssh", T_OK), ("80/tcp   filtered  http", T_ERR), ("443/tcp  filtered  https", T_ERR)],
            "TERMINAL · OTRA MÁQUINA DE LA RED DE GESTIÓN · EJEMPLO", size=17, lh=32)
c.add(svg)
y = 124 + h + 28
c.add(box(48, y, 352, 170, "open", ["Algo escucha y el firewall", "deja pasar desde acá."], kind="ok"))
c.add(box(424, y, 352, 170, "closed", ["Connection refused: llega,", "pero nada escucha. Pasa con", "el puerto permitido y sin servicio."], kind="warn"))
c.add(box(800, y, 352, 170, "filtered", ["No hay respuesta, timeout:", "un DROP del firewall lo", "descarta en silencio."], kind="alert"))
save(c, "8-paso4.svg")
