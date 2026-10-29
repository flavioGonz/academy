"""Lección 32 · Bloqueo por DNS: principal + pasos 2 y 5.
Fuentes: class/32-dns-adlist/card.md, research/notes/n29-32.md
(manual 7.25 DNS y Address lists, foro 175351, 111280, 158566, 182097).
Regenerar:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/32.py
  python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/mikrotik/32*.svg
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/mikrotik/src")
from _mt import *  # noqa
from _mt import text, wrap

K = "MikroTik"

# ------------------------------------------------------------ principal: tres herramientas
c = Canvas(K, "Tres formas de bloquear por DNS")
cols = [
    ("Adlist (7.15+)", "/ip/dns/adlist", "Lista de dominios: el router contesta 0.0.0.0. Solo el nombre exacto.",
     [("example.net", "0.0.0.0", "alert"), ("www.example.net", "pasa", "ok")]),
    ("NXDOMAIN", "match-subdomain=yes", "Un sitio entero: el nombre y todo lo de abajo no existen.",
     [("example.com", "no existe", "alert"), ("www.example.com", "no existe", "alert")]),
    ("FWD + address-list", "firewall forward", "El router anota lo que contestó y el firewall corta esas IP.",
     [("example.org", "IP a la lista", "warn"), ("conexión", "reject", "alert")]),
]
for i, (tt, sub, body, ex) in enumerate(cols):
    x = 48 + i * 377
    w = 350
    c.add(rect(x, 140, w, 330, WHITE, LINE2, 2, 16))
    c.add(text(x + 20, 178, tt, 20, 600, INK, FD))
    c.add(text(x + 20, 204, sub, 15, 500, BLUE, FM))
    b, _ = wrap(x + 20, 236, body, w - 40, 16, 400, INK2)
    c.add(b)
    for j, (name, res, k) in enumerate(ex):
        yy = 340 + j * 54
        bg, fg = KIND[k]
        c.add(rect(x + 16, yy, w - 32, 42, bg, bg, 0, 10))
        c.add(text(x + 30, yy + 27, name, 15, 500, INK, FM))
        c.add(text(x + w - 30, yy + 27, res, 15, 600, fg, FM, anchor="end"))
c.add(Note(48, 500, 1104, "Vale para los equipos que usan el DNS del router: sumale el DNS transparente. DoH y VPN pasan igual: esto filtra, no es un candado.", title="El límite de las tres", kind="warn"))
save(c, "32.svg")

# ------------------------------------------------------------ paso 2: adlist y caché
c = Canvas(K + " · Paso 2", "Adlist: subí la caché y probá el nombre exacto")
t, h = code(48, 140, 610, ["/ip/dns/set cache-size=16384",
                           "/file/add name=adlist-prueba.txt \\",
                           "  contents=\"0.0.0.0 example.net\\nads.example.net\\n\"",
                           "/ip/dns/adlist/add file=adlist-prueba.txt",
                           ("/ip/dns/adlist/print   # name-count, match-count", GRAY_T)], title="TERMINAL")
c.add(t)
c.add(caption(700, 160, "nslookup desde la notebook"))
c.add(Table(700, 176, ["nombre", "respuesta"], [
    ["example.net", "0.0.0.0"],
    ["ads.example.net", "0.0.0.0"],
    ["www.example.net", "su IP real"],
], [250, 202], hl_row=2, mono_cols=(0, 1)))
c.add(Note(700, 350, 452, "La adlist bloquea solo el nombre listado, sin comodines. Para un sitio con subdominios: NXDOMAIN con match-subdomain.", title="www.example.net pasa", kind="warn"))
c.add(rect(48, 420, 610, 200, WHITE, LINE2, 2, 16))
c.add(text(68, 456, "La lista vive en la caché DNS", 19, 600, INK, FD))
c.add(text(68, 492, "≈ 75 bytes por nombre", 17, 500, BLUE, FM))
c.add(text(68, 522, "75 000 nombres ≈ 6 MiB", 17, 500, BLUE, FM))
b, _ = wrap(68, 556, "Si no entra: \"adlist read: max cache size reached\". Subí cache-size, borrá la adlist y agregala de nuevo.", 560, 15, 400, INK2)
c.add(b)
save(c, "32-paso2.svg")

# ------------------------------------------------------------ paso 5: FWD + address-list
c = Canvas(K + " · Paso 5", "El firewall corta lo que el DNS contestó")
lp = c.add(Laptop(48, 220, "Notebook", "192.168.88.254", w=250))
c.add(rect(430, 160, 340, 270, DEEP, DEEP, 2, 18))
c.add(text(600, 200, "MikroTik", 21, 600, WHITE, FD, anchor="middle"))
c.add(text(600, 230, "static FWD example.org", 14, 500, CYAN, FM, anchor="middle"))
c.add(text(600, 254, "address-list=bloqueo-ejemplo", 14, 500, CYAN, FM, anchor="middle"))
c.add(rect(455, 278, 290, 64, "#0B3A66", "#4E7396", 1.5, 12))
c.add(text(600, 304, "bloqueo-ejemplo", 15, 600, WHITE, FM, anchor="middle"))
c.add(text(600, 328, "IP que contestó (dinámica)", 14, 400, "#D9E9F8", FB, anchor="middle"))
c.add(text(600, 384, "forward: reject", 15, 600, "#FCA5A5", FM, anchor="middle"))
c.add(text(600, 408, "dst-address-list=bloqueo-ejemplo", 13, 400, "#FCA5A5", FM, anchor="middle"))
site = c.add(Internet(920, 220, "example.org", "en internet", w=232))
c.add(Arrow((302, 236), (426, 236), kind="flow", label="1 ¿example.org?", label_dy=-12))
c.add(Arrow((426, 280), (302, 280), kind="ok", label="2 su IP", label_dy=28))
c.add(f'<path d="M173 306V380H422" fill="none" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
c.add(Chip(300, 366, "3 conexión", "alert", anchor="middle"))
c.add(Arrow((774, 236), (916, 250), kind="logical", label="consulta", label_dy=-12))
c.add(Mark(800, 380, ok=False))
c.add(Note(48, 470, 540, "Se llena cuando un equipo pregunta por el nombre, no con :resolve del router, y cada IP se borra al vencer el TTL.", title="La lista es dinámica", kind="info"))
c.add(Note(612, 470, 540, "Con CDN varias marcas comparten IP: el bloqueo puede cortar servicios que nadie quería cortar.", title="Usalo para casos puntuales", kind="warn"))
save(c, "32-paso5.svg")
