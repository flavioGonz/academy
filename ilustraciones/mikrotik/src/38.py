"""Lección 38 · Dos WAN: IP fija + PPPoE: principal + pasos 5 y 7."""
from _dw import *

K = "MikroTik · Lección 38"

# ------------------------------------------------------------------ 38.svg principal
c = Canvas(K, "IP fija principal, PPPoE de respaldo, NVR por la fija")
nvr = c.add(Generic(40, 262, "NVR", "192.168.88.20:443", icon="camera", w=230))
r = router_box(c, 306, 180, w=196, h=250)
c.add(Cable(nvr.right(), r["lan"], kind="data"))
w1l, w1r, h1 = wan_box(c, 560, 128, 330, "Principal · IP fija", ["ether1 203.0.113.10/29", "gw 203.0.113.9", "testigos 1.1.1.1 · 9.9.9.9"], "recursiva · distance=1", "blue", BLUE)
w2l, w2r, h2 = wan_box(c, 560, 340, 330, "Respaldo · PPPoE", ["pppoe-respaldo sobre ether2", "add-default-route=yes", "default-route-distance=2"], "distance=2 · espera", "gray", INK3)
c.add(Cable(r["p1"], w1l, kind="data"))
c.add(Cable(r["p2"], w2l, kind="data"))
cen = c.add(Generic(930, 150, "Central", "198.51.100.50", icon="user", w=222))
c.add(Arrow(cen.left(), (893, 228), kind="flow"))
c.add(pill(1041, 270, "203.0.113.10:8443", "blue"))
c.add(rect(930, 372, 222, 126, WHITE, LINE2, 2, 16))
c.add(text(948, 404, "IP dinámica", 16, 600, INK, FB))
c.add(text(948, 432, "Nada publicado", 15, 500, INK2, FB))
c.add(text(948, 456, "entra por acá", 15, 500, INK2, FB))
c.add(Note(40, 560, 1112, "Lo publicado entra por la IP fija: el dst-nat va atado a ether1 y a 203.0.113.10, y solo para la lista monitoreo.", kind="info", size=16))
save(c, "38.svg")

# ------------------------------------------------------------------ 38-paso5.svg
c = Canvas(K + " · Paso 5", "El dst-nat va atado a la IP fija, no a la lista WAN")
for i, good in enumerate([True, False]):
    y = 136 + i * 250
    col = OK if good else ALERT
    c.add(rect(48, y, 1104, 226, OK_BG if good else ALERT_BG, col, 2, 18))
    c.add(mark(84, y + 38, good))
    c.add(text(116, y + 45, "Así" if good else "Así no", 20, 600, INK, FD))
    lines = (["chain=dstnat in-interface=ether1 dst-address=203.0.113.10",
              "protocol=tcp dst-port=8443 src-address-list=monitoreo",
              "action=dst-nat to-addresses=192.168.88.20 to-ports=443"] if good else
             ["chain=dstnat in-interface-list=WAN",
              "protocol=tcp dst-port=8443",
              "action=dst-nat to-addresses=192.168.88.20 to-ports=443"])
    for j, s in enumerate(lines):
        c.add(text(84, y + 90 + 30 * j, s, 16, 500, INK, FM))
    msg = ("Solo la central, solo por la IP fija. La respuesta sale por la fija mientras sea la principal."
           if good else "Agarra por las dos WAN y para cualquiera. Lo que entra por el PPPoE responde por la fija y se pierde.")
    c.add(text(84, y + 196, msg, 16, 600, col, FB))
save(c, "38-paso5.svg")

# ------------------------------------------------------------------ 38-paso7.svg
c = Canvas(K + " · Paso 7", "Al revés: PPPoE principal y la IP fija sigue publicando")
for i, good in enumerate([False, True]):
    x = 48 + i * 564
    col = OK if good else ALERT
    c.add(rect(x, 132, 540, 330, WHITE, col, 2, 18))
    c.add(mark(x + 32, 166, good))
    c.add(text(x + 62, 173, "Con marcas" if good else "Sin marcas", 19, 600, INK, FD))
    c.add(mini(x + 20, 274, 120, 64, "NVR", ".88.20", title_size=17))
    c.add(mini(x + 180, 274, 130, 64, "Router", "", dark=True, title_size=17))
    c.add(mini(x + 370, 200, 150, 60, "IP fija", "ether1", hl=BLUE, title_size=16))
    c.add(mini(x + 370, 356, 150, 60, "PPPoE", "principal", title_size=16))
    c.add(line(x + 140, 306, x + 180, 306, BLUE, 4))
    c.add(f'<path d="M{x + 370} 232 C {x + 340} 236, {x + 330} 270, {x + 312} 288" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#a-blue)"/>')
    c.add(text(x + 445, 188, "entra la central", 15, 600, BLUE, FB, anchor="middle"))
    if good:
        c.add(f'<path d="M{x + 280} 274 C {x + 290} 214, {x + 330} 206, {x + 368} 214" fill="none" stroke="{OK}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-ok)"/>')
        c.add(text(x + 210, 230, "responde por la fija", 15, 600, OK, FB, anchor="middle"))
    else:
        c.add(f'<path d="M{x + 310} 330 C {x + 330} 360, {x + 340} 386, {x + 368} 386" fill="none" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
        c.add(text(x + 300, 412, "responde por el PPPoE,", 15, 600, ALERT, FB, anchor="end"))
        c.add(text(x + 300, 434, "con otra IP: no abre", 15, 600, ALERT, FB, anchor="end"))
c.add(caption(48, 492, "Tabla por-fija (0.0.0.0/0 por 203.0.113.9@main) y tres reglas de mangle"))
c.add(rows(48, 506, 1104, [("1 · prerouting · in-interface=ether1 · nueva → mark-connection entra-fija", "hl"),
                           ("2 · prerouting · desde la LAN con entra-fija → mark-routing por-fija", "plain"),
                           ("3 · output · el router responde con entra-fija → mark-routing por-fija", "plain")], h=34, gap=6, size=15))
c.add(text(48, 646, "Y FastTrack solo para connection-mark=no-mark: FastTrack usa únicamente la tabla main.", 15, 600, WARN, FB))
save(c, "38-paso7.svg")
