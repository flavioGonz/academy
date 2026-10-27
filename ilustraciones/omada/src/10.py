import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 10.svg: recorrido de un huésped
c = Canvas(K(), "El portal: el huésped entra con un código")
XP, XE, XC, XI = 150, 450, 750, 1050
c.add(lifeline(XP, 120, 496, "Celular", "huésped"))
c.add(lifeline(XE, 120, 496, "EAP", "SSID Huespedes-Lab"))
c.add(lifeline(XC, 120, 496, "Controlador", "corriendo"))
c.add(lifeline(XI, 120, 496, "Internet", "", w=170))
c.add(msg(XP, XE, 222, "se conecta al SSID", kind="flow"))
c.add(msg(XP, XE - 26, 272, "pide una web: queda retenida", kind="alert"))
c.add(Mark(XE, 272, ok=False))
c.add(msg(XE, XP, 322, "lo manda a la página del portal", kind="flow"))
c.add(msg(XP, XC, 372, "ingresa el voucher (HTTPS 8843)", kind="flow"))
c.add(msg(XC, XE, 422, "valida el código y habilita al cliente", kind="ok"))
c.add(msg(XP, XI, 472, "navega hasta que vence el voucher", kind="ok"))
c.add(Note(48, 524, 540, "Si el controlador está apagado, los clientes nuevos no pueden autenticarse. En la nube, además, hace falta la licencia vigente.", title="Sin controlador no hay portal", kind="alert"))
c.add(Note(612, 524, 540, "Hotelería: controlador dedicado, backup al día y prueba con un celular después de cada upgrade grande.", title="Por eso", kind="ok"))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso2: crear el portal
c = Canvas(K(2), "Creá el portal: Hotspot con vouchers")
c.add(Window(48, 124, 600, 330, "Omada · sitio", path="Site Settings > Authentication > Portal", rows=[
    ("Portal Name", "Huespedes"), ("SSID & Network", "Huespedes-Lab"), ("Authentication Type", "Hotspot"),
    ("Hotspot Option", "Voucher"), ("HTTPS Redirection", "activado"), ("Landing Page", "la URL que pidió")], hl=3))
c.add(Step(48, 124, 2))
c.add(panel(684, 124, 468, 330, "Otros tipos de autenticación", "info"))
c.add(lines(708, 190, ["No Authentication, Simple Password", "Hotspot: Voucher, Local User,", "SMS, RADIUS, Form Auth", "RADIUS Server (incorporado", "desde la 5.12)", "External LDAP Server", "External Portal Server"], 16, 32))
c.add(Note(48, 480, 540, "En la sección Voucher generá 2 códigos de 1 día y probá uno desde un celular (paso 5).", title="Vouchers", kind="ok"))
c.add(Note(612, 480, 540, "Con HTTPS Redirection conviene un certificado propio. El controlador lo pide en un único archivo .pfx, con certificado y clave juntos.", title="Certificado", kind="info"))
save(c, "10-paso2.svg")

# ---------------------------------------------------------------- 10-paso4: Access Control
c = Canvas(K(4), "Access Control: qué pasa sin autenticar")
c.add(panel(48, 124, 540, 330, "Pre-Authentication Access", "info"))
c.add(Phone(72, 190, "Celular", "sin autenticar", w=230))
c.add(lines(328, 222, ["Llega a la URL o", "subred de la lista"], 16, 26))
c.add(Mark(96, 330, ok=True))
c.add(text(128, 336, "La web del cliente, antes del portal", 16, 500, INK2, FB))
c.add(Mark(96, 380, ok=False))
c.add(text(128, 386, "El resto de internet, hasta autenticar", 16, 500, INK2, FB))
c.add(panel(612, 124, 540, 330, "Authentication-Free Client", "ok"))
c.add(Laptop(636, 190, "Equipo de prueba", "por MAC o IP", w=260))
c.add(lines(920, 222, ["No ve el", "portal"], 16, 26))
c.add(Mark(660, 330, ok=True))
c.add(text(692, 336, "Navega directo, sin código", 16, 500, INK2, FB))
c.add(text(636, 386, "Sirve para equipos puntuales que tienen", 16, 400, INK3, FB))
c.add(text(636, 412, "que navegar sin pasar por el portal.", 16, 400, INK3, FB))
c.add(Step(48, 124, 4))
c.add(Note(48, 480, 1104, "En el laboratorio: la URL del sitio del cliente en Pre-Authentication Access, y la MAC de un equipo de prueba en Authentication-Free Client.", kind="info"))
save(c, "10-paso4.svg")
