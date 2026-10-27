import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 9.svg: las perillas de roaming, de suave a dura
c = Canvas(K(), "El roaming lo decide el cliente; el AP solo sugiere")
rows = [
    ("802.11k", "neighbor reports", "Le pasa la lista de AP vecinos.", "sin interruptor propio", "gray"),
    ("BSS Transition", "802.11v", "Le sugiere un AP mejor; puede ignorarlo.", "siempre activado", "ok"),
    ("Band steering", "del SSID", "Lo empuja de 2.4 a 5 GHz.", "preferir, no forzar", "ok"),
    ("Fast Roaming", "802.11r", "Acelera la reautenticación.", "solo si probaste cada equipo", "warn"),
    ("Mínimo RSSI", "del fabricante", "Lo desconecta bajo un umbral.", "al final, suave", "alert"),
]
c.add(f'<defs><linearGradient id="g9" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OK}"/><stop offset=".6" stop-color="{WARN}"/><stop offset="1" stop-color="{ALERT}"/></linearGradient></defs>')
c.add('<rect x="56" y="134" width="10" height="404" rx="5" fill="url(#g9)"/>')
c.add(text(82, 128, "informa", 15, 600, OK, FM))
c.add(text(82, 562, "patea", 15, 600, ALERT, FM))
for i, (nm, sub, what, rec, kd) in enumerate(rows):
    y = 140 + i * 80
    c.add(rect(90, y, 1062, 68, WHITE, LINE2, rx=12))
    c.add(text(112, y + 32, nm, 19, 600, INK, FD))
    c.add(text(112, y + 54, sub, 15, 500, INK3, FM))
    c.add(text(330, y + 42, what, 17, 400, INK2, FB))
    c.add(tag(1132, y + 42, rec, kd, size=15, mono=False, anchor="start") if False else tag(1000, y + 42, rec, kd, size=15, mono=False))
c.add(Note(48, 584, 1104, "Equipos que no toleran Fast Roaming o WPA3 (PMF obligatorio) van a un SSID aparte, en su propia VLAN.", kind="info", size=16))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso2: un equipo de cada tipo
c = Canvas(K(2), "Un equipo de cada tipo al SSID de prueba")
c.add(Window(48, 130, 470, 290, "Prueba-FT", path="Settings > WiFi > Advanced: Manual", rows=[("BSS Transition", "On"), ("Fast Roaming", "On"), ("Band Steering", "preferir 5 GHz"), ("Minimum RSSI", "Off"), ("Security", "WPA2/WPA3 o WPA2")], hl=1))
devs = [("Celular", "phone", "conecta", "ok"), ("Notebook", "laptop", "conecta", "ok"), ("Lector de código viejo", "card", "no conecta", "alert"), ("Impresora", "server", "probalo", "gray"), ("Terminal de pago", "card", "probalo", "gray")]
c.add(text(560, 150, "Ejemplo de inventario", 18, 600, INK, FD))
for i, (nm, ic, st, kd) in enumerate(devs):
    y = 168 + i * 58
    c.add(rect(560, y, 592, 48, WHITE, LINE2, rx=10))
    c.add(icon(574, y + 10, ic, BLUE, 1.15))
    c.add(text(616, y + 31, nm, 17, 500, INK, FB))
    c.add(tag(1080, y + 31, st, kd, size=15, mono=False))
c.add(Step(560, 168, 2))
c.add(Note(48, 460, 1104, "El lector viejo es el caso que cuenta Purple: una cadena activó Fast Roaming en todos los SSID y los lectores de código de barras dejaron de conectar en 9 de 40 locales. Lo que no conecta acá va al SSID aparte del paso 5.", title="Por qué uno de cada tipo", kind="warn"))
save(c, "9-paso2.svg")

# ---------------------------------------------------------------- 9-paso4: roam o desconexión
c = Canvas(K(4), "En el historial: roam, no desconexión")
def lane(y, ok):
    col = OK if ok else ALERT
    out = [text(48, y - 20, "Bien: un roam" if ok else "Mal: desconexión y reconexión", 19, 600, col, FD)]
    out.append(rect(48, y, 500, 50, SOFT, BLUE, rx=10))
    out.append(mid(298, y + 32, "AP 1", 17, 600, BLUE, FM))
    if ok:
        out.append(rect(548, y, 604, 50, "#E0F5FA", CYAN, rx=10))
        out.append(mid(850, y + 32, "AP 2", 17, 600, CYAN, FM))
        out.append(f'<circle cx="548" cy="{y + 25}" r="14" fill="{OK}" stroke="{WHITE}" stroke-width="3"/>')
        out.append(mid(548, y + 82, "roam en el borde de la celda", 15, 600, OK))
    else:
        out.append(rect(548, y, 150, 50, ALERT_BG, ALERT, rx=10, dash="6 5"))
        out.append(mid(623, y + 32, "sin red", 16, 600, ALERT, FM))
        out.append(rect(698, y, 454, 50, "#E0F5FA", CYAN, rx=10))
        out.append(mid(925, y + 32, "AP 2", 17, 600, CYAN, FM))
        out.append(mid(623, y + 82, "hueco de cobertura o equipo que no tolera la función", 15, 600, ALERT))
    return "".join(out)
c.add(lane(170, True))
c.add(lane(330, False))
c.add(text(48, 470, "tiempo de la caminata con la llamada en curso →", 15, 500, INK3, FM))
c.add(Step(48, 170, 4))
c.add(Note(48, 500, 1104, "Client Devices > el cliente > historial de conexión y roaming (Network 10.5 en adelante). Cada paso de AP tiene que verse como roam; si ves desconexiones, el cambio no está listo para producción.", kind="info"))
save(c, "9-paso4.svg")

# ---------------------------------------------------------------- 9-paso5: SSID aparte para legado
c = Canvas(K(5), "Lo que no tolera Fast Roaming, a su propio SSID")
c.add(APNode(600, 200, "", "", r=46))
c.add(panel(48, 140, 440, 280, "SSID principal", "ok", sub="red Staff"))
lst, _ = bullet_list(72, 230, ["BSS Transition: On", "Fast Roaming: On", "WPA2/WPA3", "Celulares y notebooks probados"], 400, size=17, gap=12)
c.add(lst)
c.add(panel(712, 140, 440, 280, "SSID de legado", "warn", sub="su propia VLAN"))
lst, _ = bullet_list(736, 230, ["Fast Roaming: Off", "WPA2 (sin PMF obligatorio)", "Lectores, impresoras, sensores", "Sin acceso a los sistemas del staff"], 400, size=17, gap=12)
c.add(lst)
c.add(arrow((560, 230), (494, 260), kind="ok"))
c.add(arrow((640, 230), (706, 260), kind="flow"))
c.add(mid(600, 300, "mismo AP,", 16, 500, INK2))
c.add(mid(600, 322, "dos SSID", 16, 500, INK2))
c.add(Step(712, 140, 5))
c.add(Note(48, 450, 1104, "Así el lector viejo sigue andando y el SSID principal conserva Fast Roaming para las llamadas. El SSID de legado va en su VLAN para que lo que no pudo subir de seguridad no llegue a los sistemas del staff.", kind="info"))
save(c, "9-paso5.svg")
