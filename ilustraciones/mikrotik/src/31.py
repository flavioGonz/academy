"""Lección 31 · DNS transparente: principal + pasos 3, 5 y 6.
Fuentes: class/31-dns-transparente/card.md, research/notes/n29-32.md
(manual 7.25 DNS, foro 138046, 180041, 147912, 157195, Wikipedia DoH).
Regenerar:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/31.py
  python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/mikrotik/31*.svg
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/mikrotik/src")
from _mt import *  # noqa
from _mt import text, wrap

K = "MikroTik · Lección 31"

# ------------------------------------------------------------ principal
c = Canvas(K, "Pregunta a 8.8.8.8 y le contesta el router")
tv = c.add(Generic(48, 190, "Tele o DVR", "DNS clavado 8.8.8.8", icon="server", w=290))
ph = c.add(Phone(48, 420, "Celular con DoH", "HTTPS :443 cifrado", w=290))
c.add(rect(470, 160, 330, 210, DEEP, DEEP, 2, 18))
c.add(text(635, 200, "MikroTik", 21, 600, WHITE, FD, anchor="middle"))
c.add(text(635, 230, "dstnat · redirect :53", 15, 500, CYAN, FM, anchor="middle"))
c.add(text(635, 256, "udp y tcp, desde LAN", 14, 400, "#D9E9F8", FM, anchor="middle"))
c.add(text(635, 282, "dst-address-type=!local", 14, 400, "#D9E9F8", FM, anchor="middle"))
c.add(text(635, 330, "contesta su resolver", 15, 600, "#6EE7B7", FB, anchor="middle"))
g = c.add(Internet(930, 190, "8.8.8.8", "no la recibe", w=225))
inet = c.add(Internet(930, 420, "Servidor DoH", "en internet", w=225))
c.add(Arrow((342, 220), (466, 220), kind="flow", label="a 8.8.8.8:53", label_dy=-12))
c.add(Arrow((466, 290), (342, 290), kind="ok", label="respuesta", label_dy=28))
c.add(Arrow((804, 232), (926, 232), kind="alert"))
c.add(Mark(865, 200, ok=False))
c.add(Arrow((342, 462), (926, 462), kind="flow", label="DoH :443 pasa igual", label_at=0.5, label_dy=-14, bend="straight"))
c.add(Note(48, 540, 1104, "Lo que va al puerto 53 lo resuelve el router: valen sus estáticas y sus bloqueos. DoH viaja cifrado por el 443 y no se redirige: hay paliativos, no un candado.", kind="warn"))
save(c, "31.svg")

# ------------------------------------------------------------ paso 3: excepciones
c = Canvas(K + " · Paso 3", "La lista dns-libre: quién no se redirige")
pc = c.add(Laptop(48, 170, "PC de la oficina", "192.168.88.254", w=280))
srv = c.add(Server(48, 440, "Servidor con DNS propio", "192.168.88.10", w=320))
c.add(rect(480, 150, 300, 250, DEEP, DEEP, 2, 18))
c.add(text(630, 192, "MikroTik", 21, 600, WHITE, FD, anchor="middle"))
c.add(text(630, 222, "src-address-list=!dns-libre", 14, 500, CYAN, FM, anchor="middle"))
c.add(rect(505, 250, 250, 90, "#0B3A66", "#4E7396", 1.5, 12))
c.add(text(630, 280, "dns-libre", 15, 600, WHITE, FM, anchor="middle"))
c.add(text(630, 308, "192.168.88.10", 15, 400, "#D9E9F8", FM, anchor="middle"))
c.add(text(630, 360, "el resto: redirect", 15, 500, "#6EE7B7", FB, anchor="middle"))
c.add(text(630, 384, "al resolver del router", 15, 500, "#6EE7B7", FB, anchor="middle"))
up = c.add(Internet(920, 440, "DNS de internet", "el que use él", w=235))
c.add(Arrow((332, 212), (476, 212), kind="ok", label="redirigida", label_dy=-12))
c.add(Arrow((372, 482), (916, 482), kind="flow", label="sale sin redirigir", label_at=0.5, label_dy=-14, bend="straight"))
c.add(Note(48, 560, 1104, "Sin la excepción, el servidor DNS se redirige a sí mismo a través del router y se arma un lazo. Un controlador de dominio o un Pi-hole en otra VLAN van en la misma lista.", title="Por qué la excepción", kind="warn"))
save(c, "31-paso3.svg")

# ------------------------------------------------------------ paso 5: antes y después
c = Canvas(K + " · Paso 5", "La prueba: el mismo nslookup, antes y después")
t1, h1 = code(48, 160, 540, ["C:\\> nslookup prueba-dns.lan 8.8.8.8",
                             "Servidor:  dns.google",
                             ("*** dns.google no encuentra", RED_T),
                             ("    prueba-dns.lan: Non-existent domain", RED_T)], title="ANTES DE LAS REGLAS")
c.add(t1)
t2, h2 = code(612, 160, 540, ["C:\\> nslookup prueba-dns.lan 8.8.8.8",
                              "Nombre:    prueba-dns.lan",
                              ("Address:   192.168.88.77", GREEN_T),
                              ("# contestó el MikroTik", GRAY_T)], title="DESPUÉS DE LAS REGLAS")
c.add(t2)
c.add(Mark(560, 190, ok=False))
c.add(Mark(1124, 190, ok=True))
t3, _ = code(48, 380, 700, ["/ip/firewall/nat/print stats where comment~\"DNS transparente\"",
                            ("DNS transparente udp   packets 12", CYAN_T),
                            ("DNS transparente tcp   packets 0", GRAY_T)], title="CONTADORES (ejemplo)")
c.add(t3)
c.add(Note(780, 380, 372, "Google no conoce prueba-dns.lan. Si aparece 192.168.88.77, la consulta la respondió el router.", title="Cómo leerlo", kind="ok"))
save(c, "31-paso5.svg")

# ------------------------------------------------------------ paso 6: paliativos DoH
c = Canvas(K + " · Paso 6", "DoH: dos paliativos y lo que queda afuera")
c.add(card(48, 150, 350, 190, "Firefox", "Antes de prender DoH por su cuenta pregunta por use-application-dns.net. Si el router contesta NXDOMAIN, no lo prende.", kind="ok", icon="check"))
c.add(card(425, 150, 350, 190, "DNS sobre TLS", "Reject al TCP 853 desde la LAN: los equipos que usan DoT vuelven al 53, que ya se redirige.", kind="ok", icon="check"))
c.add(card(802, 150, 350, 190, "Queda afuera", "DoH configurado a mano, apps con DoH propio y VPN. Van por el 443 como cualquier sitio y no se redirigen.", kind="alert", icon="x"))
t, _ = code(48, 380, 1104, ["/ip/dns/static/add name=use-application-dns.net type=NXDOMAIN",
                            "/ip/firewall/filter/add chain=forward in-interface-list=LAN protocol=tcp dst-port=853 action=reject",
                            "/tool/torch bridge src-address=192.168.88.254/32 ip-protocol=tcp port=443",
                            ("# ¿aparece 8.8.8.8 o 1.1.1.1 en el 443? es DoH", GRAY_T)], title="TERMINAL (resumen)")
c.add(t)
save(c, "31-paso6.svg")
