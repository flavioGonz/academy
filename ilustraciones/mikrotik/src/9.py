"""Lección 9 · Nombre, no puerta: principal + pasos 1 y 3."""
from _mt import *

K = "MikroTik"

# ------------------------------------------------------------------ 9.svg principal
c = Canvas(K, "El nombre encuentra al router, no le abre la puerta")
p = c.add(Person(48, 270, "Técnico afuera", "celular o notebook", w=260))
c.add(rect(380, 140, 440, 130, WHITE, BLUE, 2, 16))
c.add(text(404, 176, "IP Cloud · DDNS", 15, 600, INK3, FM))
c.add(text(404, 210, "<serie>.sn.mynetname.net", 19, 600, BLUE, FM))
c.add(text(404, 246, "→ 203.0.113.10, y la sigue si cambia", 16, 500, INK2, FB))
c.add(arrow((178, 268), (376, 210), kind="logical"))
c.add(text(190, 220, "¿dónde está?", 15, 600, INK3, FB))
# router con firewall
RX = 900
c.add(rect(RX, 250, 252, 170, DEEP, DEEP, 2, 18))
c.add(text(RX + 22, 290, "Router del cliente", 18, 600, WHITE, FD))
c.add(text(RX + 22, 316, "203.0.113.10", 15, 500, "#9FC3E3", FM))
c.add(rect(RX - 26, 240, 18, 190, ALERT_BG, ALERT, 2, 6))
c.add(text(RX + 22, 360, "firewall de fábrica:", 15, 500, "#9FC3E3", FB))
c.add(text(RX + 22, 384, "drop a lo que llega", 15, 500, "#FCA5A5", FB))
c.add(text(RX + 22, 404, "de internet", 15, 500, "#FCA5A5", FB))
c.add(Cable(p.right(), (RX - 30, 335), kind="alert"))
c.add(mark(700, 323, ok=False))
c.add(text(600, 370, "conexión entrante: drop", 15, 600, ALERT, FB))
c.add(caption(48, 470, "Para entrar de verdad"))
c.add(card(48, 488, 540, 120, "Túnel (lección 29)", "WireGuard con su puerto abierto en input, o un túnel saliente a un VPS.", kind="ok", icon="tunnel"))
c.add(card(612, 488, 540, 120, "Back To Home", "WireGuard por los relays de MikroTik. Anda aunque no haya IP pública.", kind="ok", icon="cloud"))
save(c, "9.svg")

# ------------------------------------------------------------------ 9-paso1.svg
c = Canvas(K + " · Paso 1", "Qué te dice /ip/cloud/print")
w = c.add(Window(48, 140, 560, 220, "Terminal · /ip/cloud/print", rows=[("ddns-enabled", "yes"), ("dns-name", "<serie>.sn.mynetname.net"), ("public-address", "203.0.113.10"), ("status", "updated")], hl=2))
ann = [("dns-name", "El nombre fijo del router. Lo arma con el número de serie."),
       ("public-address", "La IP con la que el router llega a los servidores de MikroTik. Es la que vas a comparar."),
       ("status", "Si dice updated, el nombre ya apunta a esa IP.")]
y = 140
for k, s in ann:
    hh = note_h(520, s, k)
    c.add(Note(632, y, 520, s, title=k, kind="info" if k != "public-address" else "ok", size=16))
    y += hh + 16
c.add(Note(48, 384, 560, "Tener el nombre no abre nada: el firewall de fábrica sigue descartando lo que llega de internet.", kind="warn", size=16))
c.add(text(48, 520, "Los servicios cloud no existen en RouterOS x86.", 16, 500, INK3, FB))
save(c, "9-paso1.svg")

# ------------------------------------------------------------------ 9-paso3.svg
c = Canvas(K + " · Paso 3", "IP directa, NAT del módem o CGNAT")
cases = [("IP pública directa", "ok", ["Internet", "MikroTik"], "203.0.113.10", "203.0.113.10", "=",
          "Se puede publicar con cuidado (lección 32)."),
         ("NAT del módem", "warn", ["Internet", "Módem · 203.0.113.10", "MikroTik"], "192.168.1.2", "203.0.113.10", "≠",
          "Módem en modo bridge, o reenvío también en el módem."),
         ("CGNAT del proveedor", "alert", ["Internet", "NAT del proveedor", "MikroTik"], "100.64.12.34", "otra IP", "≠",
          "Sin port forwarding: túnel saliente o Back To Home.")]
for i, (ttl, k, chain, wan, pub, op, verdict) in enumerate(cases):
    x = 48 + i * 376
    bg, fg = KIND[k]
    c.add(rect(x, 140, 352, 470, WHITE, fg, 2, 18))
    c.add(text(x + 20, 176, ttl, 19, 600, INK, FD))
    # cadena vertical
    n = len(chain)
    ys = [200 + j * (156 / (n - 1)) for j in range(n)] if n > 1 else [200]
    for j, nm in enumerate(chain):
        last = j == n - 1
        bw = 250
        c.add(rect(x + 51, ys[j], bw, 40, DEEP if last else GROUND, DEEP if last else LINE2, 1.5, 10))
        c.add(text(x + 51 + bw / 2, ys[j] + 26, nm + (" · WAN " + wan if last else ""), 14, 600, WHITE if last else INK2, FM if last else FB, anchor="middle"))
        if j:
            c.add(line(x + 176, ys[j - 1] + 40, x + 176, ys[j], LINE2, 3))
    # comparación
    yy = 430
    c.add(text(x + 20, yy, "public-address", 14, 600, INK3, FM))
    c.add(text(x + 20, yy + 26, pub, 16, 600, INK, FM))
    c.add(text(x + 176, yy + 26, op, 26, 700, fg, FM, anchor="middle"))
    c.add(text(x + 332, yy, "IP del WAN", 14, 600, INK3, FM, anchor="end"))
    c.add(text(x + 332, yy + 26, wan, 16, 600, INK, FM, anchor="end"))
    c.add(rect(x + 16, 486, 320, 104, bg, bg, 0, 12))
    c.add(wrap(x + 32, 518, verdict, 290, 16, 600, fg)[0])
c.add(text(48 + 2 * 376 + 32, 572, "CGNAT: 100.64.0.0/10", 15, 600, ALERT, FM))
save(c, "9-paso3.svg")
