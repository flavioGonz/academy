"""Lección 11 (reescrita) · Dos WAN: principal + pasos 3, 5 y 7. Reemplaza las imágenes de src/11.py."""
from _dw import *

K = "MikroTik"

# ------------------------------------------------------------------ 11.svg principal
c = Canvas(K, "Dos WAN: cada una con su ruta y su distancia")
lan = c.add(Generic(40, 252, "LAN", "192.168.88.0/24", icon="server", w=222))
r = router_box(c, 306, 170, w=196, h=250)
c.add(Cable(lan.right(), r["lan"], kind="data"))
w1l, w1r, h1 = wan_box(c, 560, 140, 310, "ISP1 · IP fija", ["ether1 203.0.113.10/29", "gw 203.0.113.9"], "distance=1 · recursiva", "blue", BLUE)
w2l, w2r, h2 = wan_box(c, 560, 326, 310, "ISP2 · router 4G", ["ether2 192.168.8.2/24", "gw 192.168.8.1"], "distance=2 · respaldo", "gray", INK3)
c.add(Cable(r["p1"], w1l, kind="data"))
c.add(Cable(r["p2"], w2l, kind="data"))
t1, _ = witness_box(c, 930, 160, 222, "Testigos ISP1", ["1.1.1.1", "9.9.9.9"], BLUE)
t2, _ = witness_box(c, 930, 352, 222, "Testigos ISP2", ["8.8.8.8", "208.67.222.222"], INK2)
c.add(Cable(w1r, t1, kind="logical"))
c.add(Cable(w2r, t2, kind="logical"))
c.add(text(1041, 140, "/32 · scope=10", 14, 600, INK3, FM, anchor="middle"))
c.add(caption(48, 524, "Cómo pone su ruta por defecto cada tipo de WAN"))
c.add(card(48, 538, 356, 104, "IP fija", "La escribís vos en /ip/route.\nEstática: distance=1.", icon="key", title_size=18, body_size=15))
c.add(card(422, 538, 356, 104, "Cliente DHCP", "La instala sola, con\ndefault-route-distance=1.", icon="server", title_size=18, body_size=15))
c.add(card(796, 538, 356, 104, "Cliente PPPoE", "add-default-route=yes y\ndefault-route-distance=1.", icon="globe", title_size=18, body_size=15))
save(c, "11.svg")

# ------------------------------------------------------------------ 11-paso3.svg
c = Canvas(K + " · Paso 3", "La ruta por defecto apunta al testigo, no al módem")
bx = [48, 430, 812]
heads = ["0.0.0.0/0", "1.1.1.1/32", "203.0.113.8/29"]
subs = [["gateway=1.1.1.1", "target-scope=11", "check-gateway=ping"],
        ["gateway=203.0.113.9", "scope=10", "ruta al testigo"],
        ["conectada · ether1", "scope=10", "la IP fija del router"]]
cols = [BLUE, CYAN, INK3]
for i, x in enumerate(bx):
    c.add(rect(x, 140, 340, 176, WHITE, cols[i], 2.5, 16))
    c.add(text(x + 20, 178, heads[i], 21, 600, INK, FM))
    for j, s in enumerate(subs[i]):
        c.add(text(x + 20, 214 + 30 * j, s, 16, 500, INK2, FM))
c.add(arrow((388, 228), (430, 228), kind="flow"))
c.add(arrow((770, 228), (812, 228), kind="flow"))
c.add(text(409, 344, "¿cómo llego a 1.1.1.1?", 15, 600, BLUE, FB, anchor="middle"))
c.add(text(791, 344, "¿y a 203.0.113.9?", 15, 600, BLUE, FB, anchor="middle"))
c.add(mini(48, 392, 150, 64, "Router", "", dark=True, title_size=17))
c.add(mini(330, 392, 170, 64, "Módem fibra", "", title_size=17))
c.add(mini(640, 392, 170, 64, "Internet", "", title_size=17))
c.add(mini(950, 392, 170, 64, "1.1.1.1", "", hl=BLUE, title_size=17))
c.add(line(198, 424, 330, 424, BLUE, 4))
c.add(line(500, 424, 640, 424, BLUE, 4))
c.add(line(810, 424, 950, 424, BLUE, 4))
c.add(f'<path d="M123 460 C 123 500, 1035 500, 1035 462" fill="none" stroke="{OK}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-ok)"/>')
c.add(text(580, 516, "el ping de check-gateway viaja hasta el testigo, pasando por el módem", 15, 600, OK, FB, anchor="middle"))
c.add(Note(48, 546, 1104, "Solo resuelven el gateway las rutas con scope menor o igual al target-scope: la /32 (scope=10) sirve; la ruta del DHCP del 4G (scope 30) no, así el testigo de la fibra nunca se prueba por el 4G.", kind="info", size=16))
save(c, "11-paso3.svg")

# ------------------------------------------------------------------ 11-paso5.svg
c = Canvas(K + " · Paso 5", "Simulá el corte y mirá qué rutas quedan activas")
c.add(text(48, 150, "Desde la notebook:", 16, 600, INK2, FB))
c.add(text(222, 150, "ping -t 1.0.0.1", 16, 600, BLUE, FM))
seq = ["ok"] * 7 + ["sw"] + ["ok"] * 8
for i, s in enumerate(seq):
    x = 48 + i * 69
    good = s == "ok"
    c.add(rect(x, 172, 60, 52, OK_BG if good else WARN_BG, OK if good else WARN, 1.5, 10))
    if good:
        c.add(f'<g transform="translate({x + 18} 186)" fill="none" stroke="{OK}" stroke-width="2.6" stroke-linecap="round">{ICON["check"]}</g>')
    else:
        c.add(text(x + 30, 206, "⇄", 22, 700, WARN, FB, anchor="middle"))
c.add(text(48 + 3 * 69 + 30, 262, "siguen por el ISP1: el drop solo", 15, 600, OK, FB, anchor="middle"))
c.add(text(48 + 3 * 69 + 30, 284, "frena los pings del router", 15, 600, OK, FB, anchor="middle"))
c.add(text(48 + 7 * 69 + 30, 262, "conmutan", 15, 600, WARN, FB, anchor="middle"))
c.add(text(48 + 7 * 69 + 30, 284, "0 o 1 perdido", 14, 500, INK3, FB, anchor="middle"))
c.add(text(48 + 12 * 69 - 10, 262, "ya por el ISP2", 15, 600, OK, FB, anchor="middle"))
c.add(caption(48, 330, "/ip/route/print where dst-address=0.0.0.0/0"))
rows_ = [["gateway=1.1.1.1", "1", ("activa", "pill:ok"), ("inactiva", "pill:alert")],
         ["gateway=9.9.9.9", "1", ("activa", "pill:ok"), ("inactiva", "pill:alert")],
         ["gateway=8.8.8.8", "2", ("espera", "pill:gray"), ("activa", "pill:ok")],
         ["gateway=208.67.222.222", "2", ("espera", "pill:gray"), ("activa", "pill:ok")]]
t, h = ctable(48, 346, ["Ruta por defecto", "Dist.", "Antes", "Con el corte"], rows_, [290, 90, 190, 210], row_h=46, col_fonts=[FM, FM, FB, FB])
c.add(t)
c.add(Note(860, 346, 292, "El corte simulado descarta los pings del router a 1.1.1.1 y 9.9.9.9. El módem sigue vivo: solo las recursivas lo ven.", kind="warn", size=15))
c.add(text(860, 560, "Los pings perdidos de verdad", 15, 600, INK2, FB))
c.add(text(860, 584, "se cuentan en el paso 8.", 15, 600, INK2, FB))
save(c, "11-paso5.svg")

# ------------------------------------------------------------------ 11-paso7.svg
c = Canvas(K + " · Paso 7", "Lo que entra por la WAN2, que responda por la WAN2")
for i, good in enumerate([False, True]):
    x = 48 + i * 564
    col = OK if good else ALERT
    c.add(rect(x, 132, 540, 330, WHITE, col, 2, 18))
    c.add(mark(x + 32, 166, good))
    c.add(text(x + 62, 173, "Con marcas" if good else "Sin marcas", 19, 600, INK, FD))
    c.add(mini(x + 20, 274, 120, 64, "NVR", ".88.20", title_size=17))
    c.add(mini(x + 180, 274, 130, 64, "Router", "", dark=True, title_size=17))
    c.add(mini(x + 370, 200, 150, 60, "ISP1", "ether1", title_size=16))
    c.add(mini(x + 370, 356, 150, 60, "ISP2", "ether2", title_size=16))
    c.add(line(x + 140, 306, x + 180, 306, BLUE, 4))
    # pedido: entra por ISP2
    c.add(f'<path d="M{x + 370} 372 C {x + 340} 372, {x + 330} 330, {x + 310} 322" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#a-blue)"/>')
    c.add(text(x + 380, 316, "pedido entra", 15, 600, BLUE, FB))
    if good:
        c.add(f'<path d="M{x + 280} 338 C {x + 290} 410, {x + 330} 412, {x + 370} 408" fill="none" stroke="{OK}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-ok)"/>')
        c.add(text(x + 250, 432, "respuesta por ISP2", 15, 600, OK, FB, anchor="middle"))
    else:
        c.add(f'<path d="M{x + 310} 290 C {x + 330} 260, {x + 340} 230, {x + 370} 230" fill="none" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
        c.add(text(x + 300, 220, "respuesta por ISP1", 15, 600, ALERT, FB, anchor="end"))
        c.add(text(x + 300, 242, "con otra IP: se descarta", 15, 500, ALERT, FB, anchor="end"))
c.add(caption(48, 500, "Tres reglas de mangle y una tabla (por-isp2)"))
c.add(rows(48, 514, 1104, [("1 · prerouting · in-interface=ether2 · nueva → mark-connection entra-isp2", "hl"),
                           ("2 · prerouting · desde la LAN con entra-isp2 → mark-routing por-isp2", "plain"),
                           ("3 · output · respuestas del router con entra-isp2 → mark-routing por-isp2", "plain")], h=34, gap=6, size=15))
save(c, "11-paso7.svg")
