import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 3.svg: descubrimiento y adopción en la misma subred
c = Canvas(K(), "Así encuentra el EAP al controlador en su subred")
XE, XC = 170, 610
c.add(lifeline(XE, 124, 560, "EAP", "de fábrica, por DHCP"))
c.add(lifeline(XC, 124, 560, "Controlador", "misma VLAN y subred"))
c.add(msg(XE, XC, 246, "broadcast a UDP 29810", kind="logical"))
c.add(msg(XC, XE, 312, "responde por el mismo puerto", kind="flow"))
c.add(tag(XC, 372, "Devices: Pending", "warn"))
c.add(tag(XC - 200, 372, "el técnico toca Adopt", "info", mono=False))
c.add(msg(XC, XE, 436, "configuración y Device Account", kind="ok"))
c.add(tag(XC, 500, "Connected", "ok"))
c.add(tag(XE, 500, "GUI local: ya no manda", "gray", mono=False))
c.add(Note(784, 124, 368, "El broadcast no cruza routers. EAP y controlador tienen que compartir VLAN y subred.", title="Misma VLAN", kind="ok"))
c.add(Note(784, 276, 368, "Primero la VLAN: tags en todos los puertos hasta el DHCP. Después loops, ping y firewall.", title="No aparece en Pending", kind="warn"))
c.add(Note(784, 428, 368, "Reset de fábrica antes de adoptar. Adoptado, obedece al controlador y no a su web local.", title="Equipo usado", kind="info"))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso2: forzar un Adopt Failed
c = Canvas(K(2), "Forzá un Adopt Failed a propósito")
flow = [("Forget", "en el controlador,", "Devices > el EAP", "info"),
        ("Reset", "botón hasta que", "titile el LED", "info"),
        ("Web local", "http://<IP-del-EAP>", "admin / admin", "info"),
        ("Clave nueva", "Lab-Omada-2026", "(de ejemplo)", "warn")]
for i, (t, a, b, kd) in enumerate(flow):
    x = 48 + i * 282
    c.add(panel(x, 128, 254, 150, None, kd))
    c.add(badge(x + 34, 166, str(i + 1)))
    c.add(text(x + 62, 173, t, 21, 600, INK, FD))
    c.add(text(x + 24, 220, a, 15, 500, INK2, FM if "//" in a or "Lab" in a else FB))
    c.add(text(x + 24, 246, b, 15, 500, INK2, FM if "/" in b and "admin" in b else FB))
    if i < 3:
        c.add(arrow((x + 258, 203), (x + 278, 203)))
c.add(Step(48, 128, 2))
c.add(text(48, 334, "Ahora el EAP está en modo standalone, con una clave que el controlador no conoce.", 18, 600, INK, FB))
c.add(Window(48, 360, 540, 142, "Adopt Failed · Retry", rows=[("Username", "admin"), ("Password", "Lab-Omada-2026")], hl=1))
c.add(Note(612, 360, 540, "En el paso 3 aparece Adopt Failed. Con Retry y el usuario y la clave de la web local, adopta. Eso es lo que hay que buscar en obra cuando alguien ya configuró el equipo.", title="Lo que viene", kind="ok"))
save(c, "3-paso2.svg")

# ---------------------------------------------------------------- 3-paso4: leer el mensaje
c = Canvas(K(4), "Leé el mensaje antes de resetear")
c.add(Table(48, 128, ["Mensaje", "Qué revisar"], [
    ["username or password is incorrect", "Clave de la web local, o Device Account del otro controlador"],
    ["does not respond to adopt commands", "Tags de VLAN hasta el DHCP, loops, ping, firewall"],
    ["Failed to link to uplink AP", "Mesh: distancia u obstáculos, u otro uplink"],
    ["This device does not exist", "Refrescá el navegador y volvé a revisar"],
    ["Switch sin botón de reset", "Consola a 38400 baudios y BootUtil"],
], [420, 684], row_h=46, mono_cols=(0,)))
c.add(Step(48, 128, 4))
c.add(Note(48, 430, 540, "Si el equipo estuvo en otro controlador, la clave está en Settings > Site > Device Account de ese controlador.", title="Managed by Others", kind="info"))
c.add(Note(612, 430, 540, "Con el controlador software, mirá también el firewall o el antivirus de la PC: tienen que dejar pasar el 29810 y del 29811 al 29816.", title="Sin respuesta", kind="warn"))
save(c, "3-paso4.svg")
