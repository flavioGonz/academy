"""Lección 10 · NVR con criterio: principal + pasos 2 y 5."""
from _mt import *

K = "MikroTik"

# ------------------------------------------------------------------ 10.svg principal
c = Canvas(K, "Si publicás el NVR: un puerto, para una lista")
c.add(Note(48, 124, 1104, "Primera opción: VPN (lección 29). Publicar es para cuando no queda otra, por ejemplo una central de monitoreo que no puede usar túnel.", kind="info", size=15))
cen = c.add(Generic(48, 250, "Central de monitoreo", "203.0.113.25", icon="shield", hl=OK, w=290))
esc = c.add(Generic(48, 430, "Cualquier otra IP", "escaneos", icon="globe", hl=ALERT, w=290))
RX, RY, RW = 420, 240, 400
c.add(rect(RX, RY, RW, 290, DEEP, DEEP, 2, 20))
c.add(text(RX + 22, RY + 36, "Router · dst-nat", 19, 600, WHITE, FD))
for i, (s, col) in enumerate([("in-interface-list=WAN", "#D9E9F8"), ("tcp dst-port=8000", "#D9E9F8"), ("src-address-list=nvr-permitidos", GREEN_T), ("→ 192.168.88.50:8000", CYAN_T)]):
    c.add(text(RX + 22, RY + 74 + i * 28, s, 15, 500, col, FM))
c.add(rect(RX + 18, RY + 196, RW - 36, 74, "#2A1A1A", ALERT, 1.5, 10))
c.add(text(RX + 34, RY + 226, "80 · 443 · 8291 del router", 15, 600, "#FCA5A5", FM))
c.add(text(RX + 34, RY + 252, "nunca se publican", 15, 500, "#FCA5A5", FB))
nvr = c.add(Server(900, 290, "NVR", "192.168.88.50", hl=OK, w=252))
c.add(Cable(cen.right(), (RX - 4, RY + 60), kind="ok"))
c.add(Cable((RX + RW + 4, RY + 100), nvr.left(), kind="ok", label="TCP 8000"))
c.add(Cable(esc.right(), (RX - 4, RY + 230), kind="alert"))
c.add(mark(380, 455, ok=False))
c.add(text(48, 562, "No está en la lista: el dst-nat no coincide y el firewall lo descarta.", 16, 500, ALERT, FB))
c.add(text(48, 606, "En la lista, cada IP con comentario y fecha de revisión: \"central monitoreo, revisar 2027-04\".", 16, 500, INK2, FB))
save(c, "10.svg")

# ------------------------------------------------------------------ 10-paso2.svg
c = Canvas(K + " · Paso 2", "Cada parte del dst-nat cierra una puerta")
parts = [("in-interface-list=WAN", "Por dónde", "Solo lo que llega desde internet, por cualquier WAN de la lista."),
         ("protocol=tcp dst-port=8000", "Qué puerto", "Solo el puerto que usa la app del NVR. Nada de \"todos por las dudas\"."),
         ("src-address-list=nvr-permitidos", "Quién", "Solo las IP que están en la lista. Las demás ni llegan al NVR."),
         ("to-addresses=192.168.88.50 to-ports=8000", "A dónde", "La IP interna del NVR y su puerto real.")]
for i, (code_, q, why) in enumerate(parts):
    y = 140 + i * 100
    c.add(rect(48, y, 1104, 84, WHITE, OK if i == 2 else LINE2, 2.5 if i == 2 else 1.5, 14))
    c.add(pill(68, y + 50, q, "dark", anchor="start", mono=False))
    c.add(text(200, y + 36, code_, 17, 600, OK if i == 2 else BLUE, FM))
    c.add(text(200, y + 64, why, 15, 400, INK2, FB))
t, h = code(48, 548, 1104, [('/ip/firewall/address-list/add list=nvr-permitidos address=203.0.113.25 comment="central monitoreo ejemplo, revisar 2027-04"', "#D9E9F8")], title="LA LISTA, CON FECHA DE REVISIÓN", size=14)
c.add(t)
save(c, "10-paso2.svg")

# ------------------------------------------------------------------ 10-paso5.svg
c = Canvas(K + " · Paso 5", "Hairpin: cuando desde adentro entran por la IP pública")
for i, good in enumerate([False, True]):
    x = 48 + i * 564
    col = OK if good else ALERT
    c.add(rect(x, 140, 540, 400, WHITE, col, 2, 18))
    c.add(mark(x + 32, 174, good))
    c.add(text(x + 62, 181, "Con hairpin (masquerade)" if good else "Sin hairpin", 18, 600, INK, FD))
    c.add(mini(x + 170, 210, 200, 70, "Router", "203.0.113.10", dark=True, title_size=17))
    c.add(mini(x + 24, 400, 180, 70, "PC", "192.168.88.20", icon=None, title_size=17))
    c.add(mini(x + 336, 400, 180, 70, "NVR", "192.168.88.50", icon=None, title_size=17))
    c.add(arrow((x + 110, 398), (x + 186, 284)))
    c.add(text(x + 30, 330, "a 203.0.113.10", 14, 600, BLUE, FM))
    c.add(text(x + 30, 350, ":8000", 14, 600, BLUE, FM))
    c.add(arrow((x + 352, 284), (x + 424, 398)))
    c.add(text(x + 410, 330, "dst-nat", 14, 600, BLUE, FM))
    if good:
        c.add(arrow((x + 400, 398), (x + 330, 286), kind="ok"))
        c.add(arrow((x + 210, 286), (x + 140, 398), kind="ok"))
        c.add(wrap(x + 24, 504, "El NVR ve como origen al router: le contesta al router, y el router se lo devuelve a la PC.", 492, 15, 500, OK)[0])
    else:
        c.add(arrow((x + 334, 446), (x + 208, 446), kind="alert"))
        c.add(text(x + 270, 430, "contesta directo", 14, 600, ALERT, FB, anchor="middle"))
        c.add(wrap(x + 24, 504, "La PC esperaba respuesta de 203.0.113.10, le llega de 192.168.88.50 y la descarta.", 492, 15, 500, ALERT)[0])
c.add(Note(48, 560, 1104, "Con hairpin, el dst-nat cambia: en lugar de in-interface-list=WAN usa dst-address-type=local dst-address=!192.168.88.1, para no tapar el acceso al propio router.", kind="warn", size=15))
save(c, "10-paso5.svg")
