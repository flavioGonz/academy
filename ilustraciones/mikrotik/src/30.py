"""Lección 30 · DNS en MikroTik: principal + pasos 4 y 5.
Fuentes: class/30-dns-mikrotik/card.md, research/notes/n29-32.md
(manual 7.25 DNS, foro 68310, CSIRT LACNIC, guía Quad9).
Regenerar:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/30.py
  python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/mikrotik/30*.svg
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/mikrotik/src")
from _mt import *  # noqa
from _mt import text, wrap

K = "MikroTik · Lección 30"

# ------------------------------------------------------------ principal
c = Canvas(K, "El DNS del router: sí a la LAN, no a internet")
c.add(Zone(40, 150, 300, 330, "LAN", BLUE))
lp = c.add(Laptop(70, 190, "Notebook", "DNS 192.168.88.1", w=245))
cam = c.add(Camera(70, 330, "NVR", "DNS 192.168.88.1", w=245))
c.add(rect(450, 220, 300, 170, DEEP, DEEP, 2, 18))
c.add(text(600, 262, "MikroTik", 21, 600, WHITE, FD, anchor="middle"))
c.add(text(600, 292, "resolver con caché", 15, 400, "#9FC3E3", FM, anchor="middle"))
c.add(text(600, 318, "allow-remote-requests=yes", 14, 500, CYAN, FM, anchor="middle"))
c.add(text(600, 344, "estáticas · caché · DoH", 14, 400, "#9FC3E3", FM, anchor="middle"))
up = c.add(Internet(900, 190, "Servidores de arriba", "1.1.1.1 · 9.9.9.9", w=260))
bad = c.add(Generic(900, 380, "Cualquiera en internet", "consulta al :53", icon="user", w=260))
c.add(Arrow(lp.right(), (446, 270), kind="ok", label=":53", label_dy=-10))
c.add(Arrow(cam.right(), (446, 330), kind="ok", label=":53", label_dy=22))
c.add(Arrow((754, 260), up.left(), kind="flow", label="servers", label_dy=-12))
c.add(Arrow(bad.left(), (754, 360), kind="alert"))
c.add(Mark(815, 395, ok=False))
c.add(Note(450, 500, 700, "Con firewall propio, dos reglas de input: drop UDP y TCP 53 desde la lista WAN. Si no, el router es un resolver abierto y presta su enlace a ataques de amplificación.", title="drop en input: la defconf ya lo hace", kind="alert"))
c.add(Note(40, 500, 380, "El DHCP le entrega 192.168.88.1 como DNS a la LAN.", kind="ok"))
save(c, "30.svg")

# ------------------------------------------------------------ paso 4: estática
c = Canvas(K + " · Paso 4", "Un nombre local para el NVR")
lp = c.add(Laptop(48, 200, "Notebook", "nslookup nvr.lan", w=270))
c.add(rect(450, 170, 320, 150, DEEP, DEEP, 2, 18))
c.add(text(610, 210, "MikroTik", 21, 600, WHITE, FD, anchor="middle"))
c.add(text(610, 240, "/ip/dns/static", 15, 500, CYAN, FM, anchor="middle"))
c.add(text(610, 268, "nvr.lan  A  192.168.88.50", 15, 400, "#D9E9F8", FM, anchor="middle"))
c.add(text(610, 294, "TTL 1d", 15, 400, "#9FC3E3", FM, anchor="middle"))
nvr = c.add(Camera(900, 200, "NVR", "192.168.88.50", w=250))
c.add(Arrow((322, 225), (446, 225), kind="flow", label="¿nvr.lan?", label_dy=-12))
c.add(Arrow((446, 275), (322, 275), kind="ok", label="192.168.88.50", label_dy=28))
c.add(f'<path d="M183 286V352H1025V292" fill="none" stroke="{INK3}" stroke-width="3" stroke-dasharray="8 8" marker-end="url(#a-gray)"/>')
c.add(rect(775, 336, 230, 30, WHITE, INK3, 1.5, 15))
c.add(text(890, 357, "después, por nombre", 14, 600, INK3, FM, anchor="middle"))
t, _ = code(48, 400, 640, ["/ip/dns/cache/print where name~\"mikrotik\"",
                           "/ip/dns/cache/flush",
                           ("# vacía la caché: el cambio se ve enseguida", GRAY_T)], title="CACHÉ")
c.add(t)
c.add(Note(720, 400, 432, "Las respuestas quedan en caché su TTL. Si cambiaste una estática y no la ves, vaciá la caché del router y la de la PC.", title="¿Sigue la dirección vieja?", kind="warn"))
save(c, "30-paso4.svg")

# ------------------------------------------------------------ paso 5: DoH sin respaldo
c = Canvas(K + " · Paso 5", "DoH: consultas cifradas, sin plan B")
lp = c.add(Laptop(48, 200, "LAN", "pregunta al :53", w=230))
c.add(rect(400, 170, 330, 150, DEEP, DEEP, 2, 18))
c.add(text(565, 212, "MikroTik", 21, 600, WHITE, FD, anchor="middle"))
c.add(text(565, 242, "use-doh-server=<URL-DoH>", 14, 500, CYAN, FM, anchor="middle"))
c.add(text(565, 268, "verify-doh-cert=yes", 14, 400, "#D9E9F8", FM, anchor="middle"))
c.add(text(565, 294, "servers: solo para el nombre DoH", 14, 400, "#9FC3E3", FM, anchor="middle"))
doh = c.add(CloudBox(900, 160, "Servidor DoH", "HTTPS · TCP 443", w=252))
dns = c.add(Internet(900, 300, "DNS comunes", "servers", w=252))
c.add(Arrow((282, 245), (396, 245), kind="flow"))
c.add(Arrow((734, 215), (896, 200), kind="ok", label="cifrado :443", label_dy=-12))
c.add(Arrow((734, 290), (896, 342), kind="alert", label="no son respaldo", label_dy=30))
c.add(Note(48, 420, 540, "Si el servidor DoH no responde, toda la LAN recibe SERVFAIL. El router no vuelve solo a los DNS comunes.", title="Lo que dice la documentación 7.25", kind="alert"))
c.add(Note(612, 420, 540, "Algunos servicios piden HTTP/2: solo ARM64 y x86. Cloudflare, Google, NextDNS y OpenDNS andan en todos. Errores: /log/print where topics~\"dns\".", title="Antes de dejarlo en un cliente", kind="warn"))
save(c, "30-paso5.svg")
