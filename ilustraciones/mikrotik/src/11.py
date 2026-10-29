"""Lección 11 · Dos WAN: principal + pasos 3 y 5."""
from _mt import *

K = "MikroTik"

# ------------------------------------------------------------------ 11.svg principal
c = Canvas(K, "Failover que mira más allá del módem")
lan = c.add(Generic(48, 300, "LAN del local", "cajas, NVR, PCs", icon="server", w=230))
RX, RY = 330, 230
c.add(rect(RX, RY, 220, 230, DEEP, DEEP, 2, 18))
c.add(text(RX + 20, RY + 36, "Router", 20, 600, WHITE, FD))
c.add(rect(RX + 20, RY + 58, 180, 40, BLUE, BLUE, 0, 8)); c.add(text(RX + 110, RY + 84, "ether1 · ISP1", 14, 600, WHITE, FM, anchor="middle"))
c.add(rect(RX + 20, RY + 150, 180, 40, "#0B3A66", "#4E7396", 2, 8)); c.add(text(RX + 110, RY + 176, "ether2 · ISP2", 14, 600, WHITE, FM, anchor="middle"))
c.add(text(RX + 20, RY + 128, "lista WAN: las dos", 14, 500, "#9FC3E3", FB))
c.add(Cable(lan.right(), (RX, RY + 115), kind="data"))
g1 = c.add(Generic(640, 170, "Módem fibra", "gw 203.0.113.1", icon="globe", w=240))
g2 = c.add(Generic(640, 420, "Módem 4G", "gw 192.168.8.1", icon="phone", w=240))
t1 = c.add(rect(940, 150, 212, 124, WHITE, BLUE, 2, 16))
c.add(text(960, 182, "Testigos ISP1", 16, 600, INK, FB)); c.add(text(960, 214, "1.1.1.1", 16, 600, BLUE, FM)); c.add(text(960, 242, "9.9.9.9", 16, 600, BLUE, FM))
c.add(rect(940, 400, 212, 124, WHITE, LINE2, 2, 16))
c.add(text(960, 432, "Testigos ISP2", 16, 600, INK, FB)); c.add(text(960, 464, "8.8.8.8", 16, 600, INK2, FM)); c.add(text(960, 492, "208.67.222.222", 15, 600, INK2, FM))
c.add(Cable((RX + 220, RY + 78), g1.left(), kind="data"))
c.add(Cable((RX + 220, RY + 170), g2.left(), kind="data"))
c.add(Cable(g1.right(), (940, 212), kind="data"))
c.add(Cable(g2.right(), (940, 462), kind="data"))
c.add(pill(640, 300, "distance=1 · principal", "blue", anchor="start"))
c.add(pill(640, 550, "distance=2 · respaldo", "gray", anchor="start"))
c.add(f'<path d="M{RX + 200} {RY} C {RX + 240} 150, 880 150, 980 146" fill="none" stroke="{OK}" stroke-width="3" stroke-dasharray="8 7" marker-end="url(#a-ok)"/>')
c.add(text(760, 134, "check-gateway=ping al testigo, no al módem", 15, 600, OK, FB, anchor="middle"))
c.add(Note(48, 590, 1104, "Si la fibra se corta en la calle, el módem sigue contestando pero los testigos no: la ruta 1 cae y el tráfico sale por el 4G.", kind="info", size=16))
save(c, "11.svg")

# ------------------------------------------------------------------ 11-paso3.svg
c = Canvas(K + " · Paso 3", "¿Por qué rutas recursivas y no ping al módem?")
for i, good in enumerate([False, True]):
    x = 48 + i * 564
    col = OK if good else ALERT
    c.add(rect(x, 140, 540, 420, WHITE, col, 2, 18))
    c.add(mark(x + 32, 174, good))
    c.add(text(x + 62, 181, "check-gateway al testigo" if good else "check-gateway al módem", 18, 600, INK, FD))
    c.add(mini(x + 24, 220, 140, 64, "Router", "", dark=True, title_size=17))
    c.add(mini(x + 200, 220, 140, 64, "Módem", "", title_size=17))
    c.add(mini(x + 376, 220, 140, 64, "Testigo", "", title_size=17))
    c.add(line(x + 164, 252, x + 200, 252, BLUE, 4))
    c.add(line(x + 340, 252, x + 376, 252, ALERT, 4, "4 6"))
    c.add(f'<path d="M{x + 350} 236l16 32M{x + 366} 236l-16 32" stroke="{ALERT}" stroke-width="3"/>')
    c.add(text(x + 358, 310, "fibra cortada", 14, 600, ALERT, FB, anchor="middle"))
    if not good:
        c.add(f'<path d="M{x + 94} 288 C {x + 94} 340, {x + 270} 340, {x + 270} 290" fill="none" stroke="{OK}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-ok)"/>')
        c.add(text(x + 182, 360, "el módem contesta", 15, 600, OK, FB, anchor="middle"))
        c.add(card(x + 24, 400, 492, 136, "La ruta 1 sigue activa", "El router cree que hay internet y no conmuta. El local queda sin conexión aunque el 4G esté listo.", kind="alert", icon="x"))
    else:
        c.add(f'<path d="M{x + 94} 288 C {x + 94} 350, {x + 446} 350, {x + 446} 290" fill="none" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
        c.add(text(x + 270, 366, "el testigo no contesta", 15, 600, ALERT, FB, anchor="middle"))
        c.add(card(x + 24, 400, 492, 136, "La ruta 1 cae, entra la 2", "El router se da cuenta de que no hay internet por ISP1 y usa la ruta de distance=2.", kind="ok", icon="check"))
c.add(text(48, 600, "Por eso la default apunta al testigo (gateway=1.1.1.1, target-scope=11) y el testigo se alcanza por su ISP (scope=10).", 16, 500, INK2, FB))
save(c, "11-paso3.svg")

# ------------------------------------------------------------------ 11-paso5.svg
c = Canvas(K + " · Paso 5", "Probalo desenchufando y contá los pings")
c.add(text(48, 150, "Desde una PC de la LAN:", 16, 600, INK2, FB))
c.add(text(260, 150, "ping -t 1.0.0.1", 16, 600, BLUE, FM))
seq = ["ok"] * 5 + ["x"] * 6 + ["ok"] * 5
for i, s in enumerate(seq):
    x = 48 + i * 69
    good = s == "ok"
    c.add(rect(x, 172, 60, 52, OK_BG if good else ALERT_BG, OK if good else ALERT, 1.5, 10))
    c.add(f'<g transform="translate({x + 18} {186}) scale(1)" fill="none" stroke="{OK if good else ALERT}" stroke-width="2.6" stroke-linecap="round">{ICON["check" if good else "x"]}</g>')
c.add(f'<path d="M{48 + 5 * 69 - 4} 244v10H{48 + 11 * 69 - 13}v-10" fill="none" stroke="{ALERT}" stroke-width="2"/>')
c.add(text(48 + 8 * 69 - 8, 280, "contá cuántos se pierden", 16, 600, ALERT, FB, anchor="middle"))
c.add(text(48 + 8 * 69 - 8, 302, "(MKController habla de 20 a 30 s)", 14, 500, INK3, FB, anchor="middle"))
c.add(text(48 + 2 * 69, 280, "ISP1 anda", 15, 600, OK, FB, anchor="middle"))
c.add(text(48 + 13 * 69, 280, "ya por ISP2", 15, 600, OK, FB, anchor="middle"))
c.add(caption(48, 352, "/ip/route/print where dst-address=0.0.0.0/0"))
rows_ = [["gateway=1.1.1.1", "1", ("activa", "pill:ok"), ("cae", "pill:alert")],
         ["gateway=9.9.9.9", "1", ("activa", "pill:ok"), ("cae", "pill:alert")],
         ["gateway=8.8.8.8", "2", ("espera", "pill:gray"), ("activa", "pill:ok")],
         ["gateway=208.67.222.222", "2", ("espera", "pill:gray"), ("activa", "pill:ok")]]
t, h = ctable(48, 368, ["Ruta por defecto", "Distance", "Antes del corte", "Con ISP1 cortado"], rows_, [300, 130, 210, 210], row_h=46, col_fonts=[FM, FM, FB, FB])
c.add(t)
c.add(Note(922, 368, 230, "Cortá aguas arriba del módem (por ejemplo, la fibra del ISP1), no el cable del router.", kind="warn", size=15))
save(c, "11-paso5.svg")
