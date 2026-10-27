import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *


def pnode(x, y, t, ip, pna, w=230, hl=None):
    return (rect(x, y, w, 92, DEEP, hl or DEEP, rx=14, sw=3 if hl else 2) + text(x + 18, y + 32, t, 17, 600, WHITE, FD)
            + text(x + 18, y + 58, ip, 15, 500, CYAN, FM) + text(x + 18, y + 80, f"PNA {pna}", 14, 500, "#9FC3E3", FM))


# ---------------------------------------------------------------- 13.svg: red dedicada
c = Canvas(K(), "La red de incendio es física, dedicada y en anillo")
c.add(rect(40, 120, 740, 420, "none", BLUE, rx=22, sw=2, dash="8 7"))
c.add(rect(58, 106, 260, 28, GROUND, GROUND, rx=10, sw=0)); c.add(text(70, 126, "RED DE INCENDIO 192.168.1.x", 14, 600, BLUE, FM))
c.add(f'<path d="M290 206H500M615 252V380M500 410H330V300H175V252" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>')
c.add(f'<path d="M100 252V380" stroke="{INK3}" stroke-width="3"/>')
c.add(text(112, 330, "switch en", 14, 500, INK3, FB)); c.add(text(112, 348, "gabinete", 14, 500, INK3, FB))
c.add(pnode(60, 160, "Panel torre A", "192.168.1.1", 1))
c.add(pnode(500, 160, "Panel torre B", "192.168.1.2", 2))
c.add(pnode(500, 380, "Panel torre C", "192.168.1.3", 3))
c.add(rect(60, 380, 230, 92, WHITE, LINE2, rx=14)); c.add(text(78, 412, "Servidor OPC", 17, 600, INK, FD)); c.add(text(78, 438, "192.168.1.4", 15, 500, BLUE, FM)); c.add(text(78, 460, "nodo 4", 14, 500, INK3, FM))
c.add(mid(395, 196, "anillo Ethernet, RSTP", 15, 600, BLUE))
c.add(text(60, 524, "Switches y conversores dentro de los gabinetes · puertos 25001 a 25008", 15, 500, INK2))
c.add(rect(860, 360, 292, 112, WHITE, OK, rx=14, sw=2)); c.add(text(880, 396, "Red del cliente (BMS)", 17, 600, OK, FD)); c.add(text(880, 424, "otra subred", 15, 400, INK2)); c.add(text(880, 448, "solo a través del servidor OPC", 15, 400, INK2))
c.add(f'<path d="M175 472V492H830V430H860" fill="none" stroke="{OK}" stroke-width="3" stroke-dasharray="8 6"/>')
c.add(rect(860, 150, 292, 150, WARN_BG, WARN, rx=14, sw=2)); c.add(text(880, 186, "Acceso remoto", 17, 600, WARN, FD))
c.add(wrap(880, 214, "Solo por el gateway seguro de Bosch, con IPsec (UDP 500 y 4500) y subredes separadas.", 252, 15)[0])
c.add(text(48, 590, "En cada controlador: puertos 1 y 2 para la red de paneles, 3 para BMS, UGM o voz, 4 para servicios remotos.", 16, 500, INK2))
c.add(text(48, 622, "Hasta 32 nodos: paneles, teclados y servidores OPC, FSI, BACnet o UGM.", 16, 600, BLUE))
save(c, "13.svg")

# ---------------------------------------------------------------- 13-paso2: PNA = último octeto = RPS
c = Canvas(K(2), "Tres lugares, el mismo número de nodo")
for i, (t, v, s) in enumerate([("En el panel", "PNA 2", "número de nodo físico cargado en el panel"), ("En la IP", "192.168.1.2", "el último octeto es el nodo"), ("En RPS", "Nodo 2", "el mismo número en la configuración")]):
    x = 48 + i * 376
    c.add(panel(x, 140, 352, 170, t, "ok"))
    c.add(text(x + 20, 230, v, 30, 700, OK, FM))
    c.add(text(x + 20, 280, s, 15, 400, INK2))
    if i < 2:
        c.add(mid(x + 364, 232, "=", 34, 700, OK, FM))
c.add(panel(48, 340, 1104, 150, "Lo que no tiene que pasar", "alert"))
c.add(text(72, 410, "PNA 3", 26, 700, ALERT, FM)); c.add(text(250, 410, "192.168.1.2", 26, 700, ALERT, FM)); c.add(text(560, 410, "Nodo 2", 26, 700, ALERT, FM))
c.add(text(72, 456, "Un número que no coincide es un panel que no aparece en la red o que choca con otro.", 16, 400, INK2))
c.add(Note(48, 516, 1104, "Gateway por defecto del ejemplo: 192.168.1.254. Multicast: 239.192.0.1. Licencia premium en cada panel que tenga que verse en el BMS.", title="Datos del ejemplo del laboratorio", kind="info"))
save(c, "13-paso2.svg")

# ---------------------------------------------------------------- 13-paso3: más de 100 m de cobre
c = Canvas(K(3), "Más de 100 m entre nodos: conversores a fibra")
for i, (x, t) in enumerate([(48, "Gabinete torre A"), (852, "Gabinete torre B")]):
    c.add(rect(x, 170, 300, 230, WHITE, LINE2, rx=16))
    c.add(text(x + 20, 204, t, 17, 600, INK, FD))
    c.add(rect(x + 20, 226, 140, 70, DEEP, DEEP, rx=10)); c.add(text(x + 34, 268, "Panel", 16, 600, WHITE))
    c.add(rect(x + 20, 312, 260, 64, SOFT, CYAN, rx=10, sw=2)); c.add(text(x + 36, 350, "conversor de medios", 15, 600, BLUE))
c.add(f'<path d="M348 344H852" stroke="{WARN}" stroke-width="5"/>')
c.add(mid(600, 330, "fibra óptica · 180 m (ejemplo)", 16, 600, WARN))
c.add(f'<path d="M600 400V440" stroke="{LINE2}" stroke-width="2"/>')
c.add(rect(360, 440, 480, 70, ALERT_BG, ALERT, rx=12, sw=1.5))
c.add(mid(600, 470, "Cobre: menos de 100 m de nodo a nodo", 17, 600, ALERT))
c.add(mid(600, 494, "si no, conversor aprobado por Bosch y fibra", 15, 400, INK2))
c.add(Note(48, 540, 1104, "Switches RSTP externos y conversores se instalan dentro del gabinete del panel: afuera, la instalación no cumple EN 54.", title="Dentro del gabinete", kind="warn"))
save(c, "13-paso3.svg")
