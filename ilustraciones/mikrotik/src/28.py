"""Lección 28 · L2TP saliente."""
from _mt import *  # noqa
from _comun_12_22 import pipe

K = "MikroTik"

# ---------------------------------------------------------------- principal
c = Canvas(K, "La sucursal llama a la central: L2TP saliente")
suc = c.add(Box(48, 190, 250, 110, "Sucursal · hAP", "4G con CGNAT", dark=True))
cen = c.add(Box(902, 190, 250, 110, "Central", "203.0.113.10", dark=True))
c.add(pipe(330, 196, 540, 98, OK, "IPsec cifra", OK, .08, 15))
c.add(pipe(360, 222, 480, 46, BLUE, None, None, .12))
c.add(text(600, 251, "L2TP · 10.255.1.2 ↔ 10.255.1.1", 15, 600, INK, FM, anchor="middle"))
c.add(Cable(suc.right(), (330, 245), "data", arrow=False))
c.add(Cable((870, 245), cen.left(), "data", arrow=False))
c.add(arrow((420, 340), (780, 340), "ok", label="la conexión sale de la sucursal"))
c.add(Zone(48, 400, 250, 96, "LAN sucursal"))
c.add(text(173, 458, "192.168.88.0/24", 16, 600, INK, FM, anchor="middle"))
c.add(Zone(902, 400, 250, 96, "LAN central"))
c.add(text(1027, 458, "10.10.1.0/24", 16, 600, INK, FM, anchor="middle"))
c.add(card(318, 390, 278, 110, "Ida (sucursal)", "10.10.1.0/24 por l2tp-central", kind="info", title_size=17, body_size=14))
c.add(card(606, 390, 278, 110, "Vuelta (central)", "192.168.88.0/24 por 10.255.1.2", kind="info", title_size=17, body_size=14))
c.add(Note(48, 540, 1104, "use-ipsec=yes y add-default-route=no: solo las redes de la central van por el túnel. Anda detrás de CGNAT porque nadie tiene que llamar a la sucursal.", kind="ok", size=15))
save(c, "28.svg")

# ---------------------------------------------------------------- paso 4: router llega, PC no
c = Canvas(K + " · Paso 4", "El router llega y la PC no: falta la vuelta")
pc = c.add(Laptop(48, 170, "PC sucursal", "192.168.88.254", w=250))
rs = c.add(Box(360, 160, 230, 104, "Sucursal", "túnel 10.255.1.2", dark=True))
rc = c.add(Box(660, 160, 230, 104, "Central", "túnel 10.255.1.1", dark=True))
dst = c.add(Generic(950, 170, "Servidor", "10.10.1.1", icon="server", w=202))
c.add(Cable(pc.right(), rs.left(), "data"))
c.add(Cable(rs.right(), rc.left(), "logical", arrow=False))
c.add(Cable(rc.right(), dst.left(), "data"))
c.add(mark(380, 330, True))
c.add(Label(412, 337, "ping desde el router: sale como 10.255.1.2, la central conoce esa red", 16, 600, OK, FB))
c.add(mark(380, 384, False))
c.add(Label(412, 391, "ping desde la PC: sale como 192.168.88.254 y la respuesta no vuelve", 16, 600, ALERT, FB))
c.add(card(48, 440, 540, 130, "Opción 1 · Ruta de vuelta",
           "En la central: dst-address=192.168.88.0/24 gateway=10.255.1.2. Lo limpio: desde allá también pueden llegar a tus equipos.",
           kind="ok", title_size=18, body_size=15))
c.add(card(612, 440, 540, 130, "Opción 2 · Masquerade al túnel (paso 5)",
           "Si no podés tocar la central: todo llega como 10.255.1.2. Desde allá no pueden iniciar conexiones a tus equipos.",
           kind="warn", title_size=18, body_size=15))
save(c, "28-paso4.svg")

# ---------------------------------------------------------------- paso 7: add-default-route=yes
c = Canvas(K + " · Paso 7", "add-default-route=yes: todo sale por la central")
t, h = ctable(48, 150, ["destino", "gateway", "qué es"], [
    ["0.0.0.0/0", "l2tp-central", ("la ruta por defecto, ahora por el túnel", INK2)],
    ["203.0.113.10/32", "192.168.1.1 (ISP)", ("dinámica: el túnel sigue saliendo por el ISP", OK)],
    ["10.255.1.1/32", "l2tp-central", ("el otro extremo del túnel (conectada)", INK2)],
    ["192.168.88.0/24", "bridge", ("la LAN de la sucursal (conectada)", INK2)],
], [230, 250, 624], row_h=50, col_fonts=[FM, FM, FB])
c.add(t)
c.add(rect(52, 252, 1096, 44, "none", OK, 2.5, 10))
c.add(Note(48, 420, 540, "Para que la LAN navegue por la central: masquerade hacia el túnel (paso 5) o que la central haga el NAT.", title="La LAN también", kind="info", size=15))
c.add(Note(612, 420, 540, "Probalo en el banco y volvé a add-default-route=no: para unir redes alcanza con las rutas a cada LAN.", title="Después, volvé a no", kind="warn", size=15))
save(c, "28-paso7.svg")
