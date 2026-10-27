import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 6.svg: RDP por VPN, con NLA y desde la subred de gestión
c = Canvas(K(), "Escritorio remoto: por VPN y desde la subred de gestión")
c.add(NOLIG)
net = c.add(Internet(48, 150, "Internet", "escaneos al 3389"))
tec = c.add(Laptop(48, 400, "Técnico en la casa", "cliente VPN"))
rt = c.add(Generic(400, 270, "Router del cliente", "VPN · sin reenvío al 3389", icon="shield", w=310, dark=True))
c.add(Zone(770, 200, 382, 270, "gestión 10.10.10.0/24", OK))
srv = c.add(Server(800, 240, "Servidor del VMS", "RDP 3389 · NLA activa", w=330, hl=OK))
c.add(code(800, 350, 330, "-RemoteAddress 10.10.10.0/24", 14, h=40))
c.add(text(806, 420, "La regla de RDP solo acepta", 15, 400, INK2, FB))
c.add(text(806, 444, "esta subred.", 15, 400, INK2, FB))
c.add(Cable(net.right(), (400, 300), kind="alert", label="3389 directo", label_at=0.5))
c.add(Mark(352, 272, ok=False))
c.add(Cable(tec.right(), rt.bottom(), kind="logical", label="túnel VPN"))
c.add(Cable(rt.right(), (800, 282), kind="ok"))
c.add(Note(48, 520, 540, "Ni con contraseña larga ni con otro puerto: expuesto a internet recibe fuerza bruta y bloqueos de cuenta todo el día.", title="El 3389 nunca abierto a internet", kind="alert"))
c.add(Note(612, 520, 540, "NLA autentica antes de abrir la sesión y viene activada. Cambiar el puerto solo baja el ruido de los escaneos.", title="Adentro, NLA y origen limitado", kind="ok"))
save(c, "6.svg")

# ---------------------------------------------------------------- 6-paso4: probar desde dos subredes
c = Canvas(K(4), "Desde la subred de gestión entra; desde otra, no")
c.add(NOLIG)
c.add(Step(65, 141, 4))
c.add(text(94, 147, "Test-NetConnection IP -CommonTCPPort RDP", 17, 600, INK2, FM))
srv = c.add(Server(820, 290, "Servidor", "regla RDP: 10.10.10.0/24", w=332))
a1 = c.add(Laptop(48, 190, "Puesto de gestión", "10.10.10.40"))
a2 = c.add(Laptop(48, 420, "Puesto de otra red", "192.168.88.40"))
c.add(Cable(a1.right(), srv.left(-14), kind="ok", label="TcpTestSucceeded : True", label_at=0.45))
c.add(Cable(a2.right(), srv.left(14), kind="alert", label="TcpTestSucceeded : False", label_at=0.45))
c.add(Note(48, 540, 1104, "Si tocás estas reglas por escritorio remoto desde fuera de la subred elegida, te cortás: hacelo por consola o desde la subred de gestión. IPs de ejemplo.", kind="warn"))
save(c, "6-paso4.svg")

# ---------------------------------------------------------------- 6-paso5: ningún reenvío al 3389
c = Canvas(K(5), "En el router: ningún reenvío de puerto al 3389")
c.add(NOLIG)
c.add(Step(65, 141, 5))
c.add(text(94, 147, "Reenvío de puertos (port forwarding) del router del laboratorio", 17, 600, INK2, FB))
c.add(Table(48, 180, ["Protocolo", "Puerto externo", "Destino", "Qué hacer"],
            [["TCP", "3389", "10.10.10.20:3389", "borrarla"], ["TCP", "33890", "10.10.10.20:3389", "borrarla también"]],
            [180, 240, 320, 364], row_h=54, mono_cols=(1, 2)))
c.add(Mark(1118, 261, ok=False))
c.add(Mark(1118, 315, ok=False))
c.add(Note(48, 380, 540, "Otro puerto externo que apunta al 3389 es lo mismo: el servidor queda expuesto, solo que lo encuentran un poco más tarde.", title="Cambiar el número no alcanza", kind="alert"))
c.add(Note(612, 380, 540, "El acceso desde afuera entra por la VPN del router y, adentro, llega al servidor desde la subred de gestión.", title="Lo que sí", kind="ok"))
c.add(text(48, 536, "Filas de ejemplo: así se ve lo que hay que buscar y borrar.", 15, 400, INK3, FB))
save(c, "6-paso5.svg")
