import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 4.svg: IP fija en cuatro pasos y verificar
c = Canvas(K(), "IP fija por consola: cuatro pasos y verificar")
c.add(NOLIG)
cols = [("1", "Ver la placa", "Get-NetAdapter", "nombre e índice"),
        ("2", "Limpiar", "Remove-NetIPAddress", "y Remove-NetRoute 0.0.0.0/0"),
        ("3", "Asignar", "New-NetIPAddress", "-PrefixLength 24 -DefaultGateway"),
        ("4", "DNS aparte", "Set-DnsClient…", "ServerAddresses 10.10.10.1"),
        ("5", "Verificar", "Get-NetIPAddress", "y Get-NetRoute 0.0.0.0/0")]
for i, (n, t, cmd, s) in enumerate(cols):
    x = 48 + i * 224
    ok = n == "5"
    c.add(panel(x, 128, 200, 250, None, "ok" if ok else "info"))
    c.add(badge(x + 32, 166, n, OK if ok else CYAN))
    c.add(text(x + 58, 173, t, 18, 600, OK if ok else INK, FD))
    c.add(code(x + 12, 200, 176, cmd, 13, h=36))
    svg, _ = wrap(x + 16, 270, s, 172, 15, 500, INK2, FM)
    c.add(svg)
    if i < 4:
        c.add(arrow((x + 202, 300), (x + 222, 300), "flow"))
c.add(panel(48, 404, 540, 110, None, "soft"))
c.add(text(72, 444, "-PrefixLength 24", 18, 600, BLUE, FM))
c.add(text(270, 444, "= máscara 255.255.255.0", 17, 500, INK2, FM))
c.add(text(72, 484, "New-NetIPAddress no toma la máscara en decimal.", 16, 400, INK2, FB))
c.add(panel(612, 404, 540, 110, None, "alert"))
c.add(text(636, 444, "Sin limpiar: dos gateways", 18, 600, ALERT, FD))
c.add(text(636, 484, "El tráfico sale por donde quiere.", 16, 400, INK2, FB))
c.add(Note(48, 540, 1104, "Hacelo desde la consola de la VM o del servidor: cambiar la IP por escritorio remoto te desconecta. Después, el script queda en el informe de obra y sirve igual en Server Core.", kind="warn"))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso2: la ruta vieja
c = Canvas(K(2), "Si no borrás la ruta vieja, quedan dos gateways")
c.add(NOLIG)
c.add(Step(65, 141, 2))
c.add(text(94, 147, "Get-NetRoute -DestinationPrefix '0.0.0.0/0'", 17, 600, INK2, FM))
c.add(panel(48, 176, 540, 300, "Sin Remove-NetRoute", "alert"))
c.add(code(68, 230, 500, "0.0.0.0/0   192.168.88.1   vieja", 15))
c.add(code(68, 280, 500, "0.0.0.0/0   10.10.10.1     nueva", 15))
svg, _ = wrap(72, 360, "Dos rutas por defecto en la misma placa: el tráfico puede salir por un gateway que ya no existe.", 490, 16, 400, INK2)
c.add(svg)
c.add(panel(612, 176, 540, 300, "Con Remove-NetRoute antes", "ok"))
c.add(code(632, 230, 500, "0.0.0.0/0   10.10.10.1     nueva", 15))
svg, _ = wrap(636, 310, "Una sola ruta por defecto, la que pusiste con -DefaultGateway. Es lo que tenés que ver al verificar.", 490, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 500, 1104, "Remove-NetIPAddress -InterfaceAlias $if -AddressFamily IPv4 y Remove-NetRoute -InterfaceAlias $if -DestinationPrefix '0.0.0.0/0', los dos con -Confirm:$false, antes de New-NetIPAddress. IPs de ejemplo.", title="El orden del paso 2", kind="info"))
save(c, "4-paso2.svg")

# ---------------------------------------------------------------- 4-paso5: DHCP en Server con reserva
c = Canvas(K(5), "DHCP de laboratorio: ámbito, opciones y una reserva")
c.add(NOLIG)
c.add(Step(65, 141, 5))
c.add(text(94, 147, "Windows Server 2025 de prueba, en una red aislada", 17, 600, INK2, FB))
srv = c.add(Server(48, 190, "Servidor DHCP", "10.10.10.20 · IP fija", w=280))
c.add(panel(380, 176, 772, 290, None, "info"))
c.add(text(404, 214, "Ámbito 'Lab CCTV'", 19, 600, INK, FD))
c.add(text(404, 246, "10.10.10.100 a 10.10.10.200 · 255.255.255.0", 16, 500, BLUE, FM))
c.add(hline(400, 1132, 266))
c.add(text(404, 300, "Opciones", 16, 600, INK3, FB))
c.add(tag(560, 300, "router 10.10.10.1", "info", anchor="start"))
c.add(tag(800, 300, "DNS 10.10.10.20", "info", anchor="start"))
c.add(hline(400, 1132, 324))
c.add(text(404, 358, "Reserva", 16, 600, INK3, FB))
c.add(tag(560, 358, "10.10.10.150", "ok", anchor="start"))
c.add(text(740, 358, "← MAC 00-11-22-33-44-55", 16, 500, INK2, FM))
c.add(text(404, 404, "La cámara de acceso recibe siempre la misma IP,", 16, 400, INK2, FB))
c.add(text(404, 430, "y el inventario queda en un solo lugar.", 16, 400, INK2, FB))
cam = c.add(Camera(48, 360, "Cámara acceso", "00-11-22-33-44-55", w=280))
c.add(Cable(srv.bottom(), cam.top(), kind="data"))
c.add(Note(48, 496, 540, "Si hay dominio, falta Add-DhcpServerInDC: un DHCP no autorizado en Active Directory no entrega direcciones.", title="Con dominio", kind="info"))
c.add(Note(612, 496, 540, "Conectado a la red del cliente, un DHCP de laboratorio puede repartir direcciones. Probalo aislado.", title="Red aislada", kind="warn"))
save(c, "4-paso5.svg")
