"""Lección 37 · Dos WAN: PPPoE + DHCP: principal + pasos 1, 4 y 7."""
from _dw import *

K = "MikroTik · Lección 37"

# ------------------------------------------------------------------ 37.svg principal
c = Canvas(K, "Fibra por PPPoE principal, 4G por DHCP de respaldo")
lan = c.add(Generic(40, 262, "LAN", "192.168.88.0/24", icon="server", w=222))
r = router_box(c, 306, 180, w=196, h=250)
c.add(Cable(lan.right(), r["lan"], kind="data"))
w1l, w1r, h1 = wan_box(c, 560, 128, 330, "Principal · PPPoE Antel", ["pppoe-antel sobre ether1", "add-default-route=no", "testigos por la interfaz"], "recursiva · distance=1", "blue", BLUE)
w2l, w2r, h2 = wan_box(c, 560, 340, 330, "Respaldo · DHCP del 4G", ["ether2 · gw 192.168.8.1", "default-route-distance=2", "use-peer-dns=no"], "distance=2 · espera", "gray", INK3)
c.add(Cable(r["p1"], w1l, kind="data"))
c.add(Cable(r["p2"], w2l, kind="data"))
t1, _ = witness_box(c, 940, 150, 212, "Testigos", ["1.1.1.1", "9.9.9.9"], BLUE)
c.add(Cable(w1r, t1, kind="logical"))
c.add(text(1046, 290, "gateway=pppoe-antel", 14, 600, INK3, FM, anchor="middle"))
c.add(rect(940, 372, 212, 128, WHITE, LINE2, 2, 16))
c.add(text(958, 404, "DNS del router", 16, 600, INK, FB))
c.add(text(958, 436, "1.0.0.1", 16, 600, INK2, FM))
c.add(text(958, 466, "8.8.4.4", 16, 600, INK2, FM))
c.add(text(958, 490, "no son testigos", 14, 500, INK3, FB))
c.add(Note(40, 560, 1112, "En RouterOS 7 la ruta /32 al testigo puede usar el nombre de la interfaz PPPoE como gateway: la IP del otro extremo cambia en cada reconexión y no importa.", kind="info", size=16))
save(c, "37.svg")

# ------------------------------------------------------------------ 37-paso1.svg
c = Canvas(K + " · Paso 1", "ether1 a la fibra, ether2 al 4G y fuera del bridge")
svg, anc, w = port_router(330, 160, ["ether1", "ether2", "ether3", "ether4", "ether5"], colors={"ether1": BLUE, "ether2": WARN, "ether3": OK}, name="Router", sub="RouterOS 7", pw=88, gap=12)
c.add(svg)
c.add(pill(694, 146, "bridge: ether3 a ether5", "ok"))
ont = c.add(Generic(60, 420, "ONT de Antel", "modo puente", icon="globe", w=250))
g4 = c.add(Generic(370, 420, "Router 4G", "DHCP · 192.168.8.1", icon="phone", w=250))
nb = c.add(Generic(680, 420, "Notebook", "entrás por acá", icon="laptop", w=250))
c.add(Cable(anc["ether1"], ont.top(), kind="data", label="PPPoE", label_at=0.55))
c.add(Cable(anc["ether2"], g4.top(), kind="data", label="DHCP", label_at=0.55))
c.add(Cable(anc["ether3"], nb.top(), kind="data"))
c.add(Note(960, 300, 192, "Si entrás por ether2, al sacarlo del bridge te cortás.", kind="warn", size=15))
c.add(Step(318, 160, 1))
c.add(text(48, 580, "/interface/bridge/port/remove [find interface=ether2]", 16, 600, BLUE, FM))
c.add(text(48, 612, "/ip/dhcp-client/disable [find interface=ether1]", 16, 600, BLUE, FM))
save(c, "37-paso1.svg")

# ------------------------------------------------------------------ 37-paso4.svg
c = Canvas(K + " · Paso 4", "La tabla esperada después del paso 4")
c.add(caption(48, 140, "/ip/route/print"))
rows_ = [["1.1.1.1/32", "pppoe-antel", "1", ("activa", "pill:ok")],
         ["9.9.9.9/32", "pppoe-antel", "1", ("activa", "pill:ok")],
         ["0.0.0.0/0", "1.1.1.1", "1", ("activa", "pill:ok")],
         ["0.0.0.0/0", "9.9.9.9", "1", ("activa", "pill:ok")],
         ["0.0.0.0/0 · DHCP", "192.168.8.1", "2", ("espera", "pill:gray")]]
h = route_table(c, 48, 156, rows_, [250, 210, 90, 160], head=("Destino", "Gateway", "Dist.", "Estado"), row_h=50)
c.add(text(48, 156 + h + 34, "Las dos recursivas en distancia 1 forman ECMP: la fibra sigue mientras conteste un testigo.", 15, 500, INK2, FB))
c.add(card(800, 156, 352, 188, "Si ves esto, está mal", "0.0.0.0/0 · gateway=pppoe-antel\nen distancia 1: el PPPoE quedó con\nadd-default-route=yes y el\nfailover nunca ocurre.", kind="alert", icon="x", body_size=15))
c.add(card(800, 364, 352, 150, "Y esto también", "La ruta del DHCP con distancia 1: reparte tráfico con la fibra.", kind="warn", icon="warn", body_size=15))
save(c, "37-paso4.svg")

# ------------------------------------------------------------------ 37-paso7.svg
c = Canvas(K + " · Paso 7", "Dos cortes distintos, el mismo resultado")
panels = [("Corte 1 · la sesión se cae", [("pppoe-client disable pppoe-antel", "plain"), ("pppoe-antel baja: la /32 queda inactiva", "warn"), ("las recursivas caen, entra la del DHCP", "ok"), ("masquerade borra sus conexiones solo", "ok")]),
          ("Corte 2 · PPPoE arriba, sin internet", [("drop en output a los testigos", "plain"), ("la sesión sigue: solo los testigos fallan", "warn"), ("las recursivas caen, entra la del DHCP", "ok"), ("las conexiones por la fibra quedan", "warn")])]
for i, (title, items) in enumerate(panels):
    x = 48 + i * 564
    c.add(rect(x, 132, 540, 290, WHITE, LINE2, 2, 18))
    c.add(text(x + 24, 172, title, 19, 600, INK, FD))
    c.add(rows(x + 20, 196, 500, items, h=40, gap=14, size=15))
c.add(card(48, 446, 1104, 150, "Al volver la fibra", "Lo que se armó por el 4G sigue en conntrack, porque ether2 nunca bajó: una llamada SIP o una VPN pueden quedar colgadas. Miralo con /ip/firewall/connection/print where reply-dst-address~\"^192.168.8.\" y, si hace falta, un Netwatch que borra las conexiones UDP cuando vuelve el testigo.", kind="info", icon="warn", body_size=16))
save(c, "37-paso7.svg")
