"""Lección 39 · Dos WAN: IP fija + DHCP: principal + pasos 5 y 7."""
from _dw import *

K = "MikroTik"

# ------------------------------------------------------------------ 39.svg principal
c = Canvas(K, "IP fija principal, 4G por DHCP de respaldo")
lan = c.add(Generic(40, 262, "LAN", "192.168.88.0/24", icon="server", w=222))
r = router_box(c, 306, 180, w=196, h=250)
c.add(Cable(lan.right(), r["lan"], kind="data"))
w1l, w1r, h1 = wan_box(c, 560, 128, 330, "Principal · IP fija", ["ether1 203.0.113.10/29", "gw 203.0.113.9", "testigos 1.1.1.1 · 9.9.9.9"], "recursiva · distance=1", "blue", BLUE)
w2l, w2r, h2 = wan_box(c, 560, 340, 330, "Respaldo · DHCP del 4G", ["ether2 · gw 192.168.8.1", "default-route-distance=2", "IP privada o CGNAT"], "distance=2 · espera", "gray", INK3)
c.add(Cable(r["p1"], w1l, kind="data"))
c.add(Cable(r["p2"], w2l, kind="data"))
c.add(rect(926, 200, 226, 276, WHITE, WARN, 2, 16))
c.add(text(944, 234, "Con el 4G activo", 17, 600, INK, FB))
items = [(True, "sale todo"), (False, "no entra lo"), (None, "Back To Home")]
subs = ["", "publicado", "por el relay"]
for i, (ok, s) in enumerate(items):
    y = 286 + i * 66
    if ok is None:
        c.add(f'<circle cx="962" cy="{y}" r="18" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/>')
        c.add(icon(950, y - 12, "warn", WARN, 1.0, 2.2))
    else:
        c.add(mark(962, y, ok))
    c.add(text(992, y - 2 + (0 if subs[i] else 6), s, 16, 600, INK, FB))
    if subs[i]:
        c.add(text(992, y + 20, subs[i], 16, 600, INK, FB))
c.add(Note(40, 560, 1112, "Si el router 4G está en modo router, su gateway 192.168.8.1 no cambia; si cambia, el script de lease del cliente DHCP mantiene la ruta al día.", kind="info", size=16))
save(c, "39.svg")

# ------------------------------------------------------------------ 39-paso5.svg
c = Canvas(K + " · Paso 5", "Lo que ve la nube antes y durante el failover")
for i, (title, rows_l, col) in enumerate([
        ("Fibra activa", [("public-address: 203.0.113.10", GREEN_T), ("vpn-relay-ipv4-status:", "#D9E9F8"), ("  reachable directly", GREEN_T)], OK),
        ("4G activo", [("public-address: 198.51.100.77", AMBER_T), ("vpn-relay-ipv4-status:", "#D9E9F8"), ("  reachable via relay", AMBER_T)], WARN)]):
    x = 48 + i * 564
    c.add(text(x, 150, title, 19, 600, col, FD))
    svg, h = code(x, 168, 540, ["/ip/cloud/force-update", "/ip/cloud/print"] + rows_l, title="TERMINAL", lh=32, size=16)
    c.add(svg)
c.add(Note(48, 430, 1104, "El servidor de la nube contesta con la IP desde la que recibió el pedido: el nombre .sn.mynetname.net sigue a la WAN por la que sale el router, con TTL de 60 segundos. Con el 4G en IP privada o CGNAT, los celulares con Back To Home entran por el relay de MikroTik.", kind="info", size=16))
c.add(text(48, 600, "198.51.100.77 es un ejemplo: con CGNAT, la IP pública es del operador y es compartida.", 15, 500, INK3, FB))
save(c, "39-paso5.svg")

# ------------------------------------------------------------------ 39-paso7.svg
c = Canvas(K + " · Paso 7", "PCC: cada par cliente servidor, a un enlace")
c.add(mini(40, 300, 200, 80, "Conexión nueva", "desde la LAN", title_size=17))
c.add(mini(290, 150, 270, 80, "¿Va a una red local?", "no-balancear", title_size=17))
c.add(mini(640, 150, 250, 80, "accept", "sigue en main", hl=OK, title_size=17))
c.add(mini(290, 330, 270, 80, "PCC", "both-addresses:2", dark=True, title_size=18))
c.add(mini(640, 290, 250, 70, "resto 0", "pcc-fija", hl=BLUE, title_size=17))
c.add(mini(640, 420, 250, 70, "resto 1", "pcc-4g", hl=INK3, title_size=17))
c.add(mini(940, 290, 212, 70, "tabla por-fija", "ether1", hl=BLUE, title_size=17))
c.add(mini(940, 420, 212, 70, "tabla por-4g", "ether2", hl=INK3, title_size=17))
c.add(arrow((240, 330), (290, 200), kind="flow"))
c.add(arrow((560, 190), (640, 190), kind="ok", label="sí"))
c.add(arrow((425, 230), (425, 330), kind="flow", label="no", bend="straight"))
c.add(arrow((560, 360), (640, 325), kind="flow"))
c.add(arrow((560, 385), (640, 455), kind="flow"))
c.add(arrow((890, 325), (940, 325), kind="flow", bend="straight"))
c.add(arrow((890, 455), (940, 455), kind="flow", bend="straight"))
c.add(Note(40, 530, 1112, "Si el gateway de una tabla no responde (check-gateway=ping), sus conexiones caen a main y siguen el failover. El chequeo mira solo el gateway, no internet. FastTrack, solo para lo que no tiene marca.", kind="warn", size=16))
save(c, "39-paso7.svg")
