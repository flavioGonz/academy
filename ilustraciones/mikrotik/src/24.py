"""Lección 24 · Port forwarding: principal + pasos 1, 3 y 7.

Autocontenido (solo importa tools/ilus.py, sin modificarla). Regenerar:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/24.py
  python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/mikrotik/24*.svg
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa: F401,F403
from ilus import text, wrap

OUT = "/home/claude/ies-training/ilustraciones/mikrotik/"
K = "MikroTik"
GREEN_T, RED_T, CYAN_T, GRAY_T, AMBER_T = "#6EE7B7", "#FCA5A5", "#7DD3FC", "#7FA6C9", "#FCD34D"


def rect(x, y, w, h, fill=WHITE, stroke=LINE2, sw=2, rx=16, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def para(x, y, s, w, size=16, color=INK2, weight=400, font=FB):
    return wrap(x, y, s, w, size, weight, color, font)[0]


def arrow(a, b, kind="flow", label=None, **kw):
    return Arrow(a, b, label=label, kind=kind, **kw).svg()


def mini(x, y, w, h, title, sub="", dark=False, hl=None, icon=None, title_size=18):
    fill = DEEP if dark else WHITE
    out = [rect(x, y, w, h, fill, hl or (DEEP if dark else LINE2), 3 if hl else 2, 14)]
    cx = x + w / 2
    if icon:
        out.append(f'<g transform="translate({x + 16} {y + h / 2 - 14}) scale(1.15)" fill="none" stroke="{CYAN if dark else BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[icon]}</g>')
        cx = x + 48 + (w - 48) / 2
    ty = y + h / 2 + (-3 if sub else 6)
    out.append(text(cx, ty, title, title_size, 600, WHITE if dark else INK, FB, anchor="middle"))
    if sub:
        out.append(text(cx, ty + 22, sub, 15, 400, "#9FC3E3" if dark else INK3, FM, anchor="middle"))
    return "".join(out)


def packet(x, y, w, head, src, dst, kind="plain", changed=None):
    """Tarjeta de 'paquete' con origen y destino. changed = 'src' o 'dst' resalta el campo que cambió."""
    bg, st = {"plain": (WHITE, LINE2), "ok": (OK_BG, OK), "hl": (SOFT, CYAN)}[kind]
    out = [rect(x, y, w, 104, bg, st, 2, 12), text(x + 16, y + 28, head, 15, 600, INK, FB)]
    for i, (k, v) in enumerate([("origen", src), ("destino", dst)]):
        yy = y + 58 + i * 28
        hot = changed == ("src" if i == 0 else "dst")
        if hot:
            out.append(rect(x + 8, yy - 19, w - 16, 26, WARN_BG, WARN_BG, 0, 6))
        out.append(text(x + 16, yy, k, 14, 500, INK3, FB))
        out.append(text(x + w - 14, yy, v, 15, 600, WARN if hot else INK, FM, anchor="end"))
    return "".join(out)


def save(c, name):
    p = c.save(OUT + name)
    print("guardado", p)


# ------------------------------------------------------------------ 24.svg principal
c = Canvas(K, "Del 18000 de afuera al 8000 del NVR")
# columnas: afuera | router | adentro
c.add(Zone(36, 132, 300, 470, "INTERNET", INK3))
c.add(Zone(864, 132, 300, 470, "LAN 192.168.88.0/24", BLUE))
app = c.add(Generic(56, 168, "App o iVMS", "198.51.100.20", icon="phone", hl=OK, w=260))
vlc = c.add(Generic(56, 300, "VLC (RTSP)", "198.51.100.20", icon="laptop", hl=OK, w=260))
otro = c.add(Generic(56, 470, "Otra IP", "fuera de la lista", icon="globe", hl=ALERT, w=260))

RX, RY, RW, RH = 400, 150, 400, 360
c.add(rect(RX, RY, RW, RH, DEEP, DEEP, 2, 20))
c.add(text(RX + 22, RY + 36, "MikroTik", 20, 600, WHITE, FD))
c.add(text(RX + RW - 22, RY + 36, "ether1 · 203.0.113.10", 15, 500, CYAN_T, FM, anchor="end"))
c.add(text(RX + 22, RY + 72, "NAT · dstnat (si el origen está", 15, 500, GRAY_T, FM))
c.add(text(RX + 22, RY + 94, "en nvr-permitidos)", 15, 500, GRAY_T, FM))
for i, (a, b) in enumerate([(":18000", "192.168.88.50:8000"), (":18554", "192.168.88.50:554")]):
    yy = RY + 116 + i * 52
    c.add(rect(RX + 18, yy, RW - 36, 40, "#0B3A66", "#4E7396", 1.5, 10))
    c.add(text(RX + 34, yy + 26, a, 16, 600, AMBER_T, FM))
    c.add(text(RX + 112, yy + 26, "→", 16, 600, WHITE, FM))
    c.add(text(RX + RW - 34, yy + 26, b, 16, 600, GREEN_T, FM, anchor="end"))
c.add(text(RX + 22, RY + 248, "FILTER · forward", 15, 500, GRAY_T, FM))
c.add(text(RX + 22, RY + 274, "drop all from WAN not DSTNATed", 15, 500, "#D9E9F8", FM))
c.add(text(RX + 22, RY + 298, "lo dst-nateado pasa", 15, 600, GREEN_T, FB))
c.add(text(RX + 22, RY + 336, "sin dst-nat: descartado", 15, 600, RED_T, FB))

nvr = c.add(Server(884, 222, "NVR", "192.168.88.50", hl=OK, w=260))
c.add(rect(884, 330, 260, 110, WHITE, LINE2, 1.5, 12))
c.add(text(904, 362, "8000  SDK: app e iVMS", 15, 500, INK, FM))
c.add(text(904, 392, "554   RTSP", 15, 500, INK, FM))
c.add(text(904, 422, "80/443 web (no se publica)", 14, 500, INK3, FM))

c.add(arrow(app.right(), (RX - 6, RY + 136), kind="ok", label=":18000", label_at=0.45, label_dy=-14))
c.add(arrow(vlc.right(), (RX - 6, RY + 188), kind="ok", label=":18554", label_at=0.45, label_dy=18))
c.add(arrow((RX + RW + 6, RY + 136), (884, 264), kind="ok", label=":8000", label_at=0.5, label_dy=-14))
c.add(arrow((RX + RW + 6, RY + 188), (884, 300), kind="ok", label=":554", label_at=0.6, label_dy=36))
c.add(arrow(otro.right(), (RX - 6, RY + 330), kind="alert"))
c.add(Mark(370, 480, ok=False))
c.add(Note(48, 614, 1104, "El destino cambia de 203.0.113.10:18000 a 192.168.88.50:8000; la respuesta vuelve por el router, que deshace el cambio.", kind="info", size=15))
save(c, "24.svg")

# ------------------------------------------------------------------ 24-paso1.svg
c = Canvas(K + " · Paso 1", "¿La IP pública llega al MikroTik?")
cases = [
    ("IP pública directa", OK, "ok", [("Internet", None), ("MikroTik", "WAN 203.0.113.10"), ("NVR", "192.168.88.50")],
     "WAN = public-address", "Se publica en el MikroTik."),
    ("Doble NAT", WARN, "warn", [("Internet", None), ("Módem del ISP", "203.0.113.10"), ("MikroTik", "WAN 192.168.1.2")],
     "WAN privada (192.168.x, 10.x)", "Módem u ONT en bridge, o reenvío también en el módem hacia la WAN del MikroTik."),
    ("CGNAT", ALERT, "alert", [("Internet", None), ("NAT del proveedor", "IP compartida"), ("MikroTik", "WAN 100.72.15.4")],
     "WAN en 100.64.0.0/10", "Sin port forwarding: Back To Home, concentrador o IP pública."),
]
for i, (title, col, kind, chain, cond, what) in enumerate(cases):
    x, w = 48 + i * 372, 356
    bg = {"ok": OK_BG, "warn": WARN_BG, "alert": ALERT_BG}[kind]
    c.add(rect(x, 128, w, 470, WHITE, col, 2, 18))
    c.add(rect(x, 128, w, 52, bg, col, 2, 18))
    c.add(rect(x + 2, 160, w - 4, 20, bg, bg, 0, 0))
    c.add(Mark(x + 30, 154, ok=(kind == "ok")) if kind != "warn" else
          f'<circle cx="{x + 30}" cy="154" r="18" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/><g transform="translate({x + 18} 142)" fill="none" stroke="{WARN}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ICON["warn"]}</g>')
    c.add(text(x + 58, 161, title, 19, 600, col, FD))
    for j, (n, sub) in enumerate(chain):
        yy = 200 + j * 104
        dark = n == "MikroTik"
        c.add(mini(x + 40, yy, w - 80, 70, n, sub or "", dark=dark,
                   hl=(ALERT if (kind == "alert" and j == 1) else (WARN if (kind == "warn" and j == 1) else None)), title_size=17))
        if j < 2:
            c.add(arrow((x + w / 2, yy + 72), (x + w / 2, yy + 102), kind="flow"))
    c.add(text(x + 20, 534, cond, 15, 600, INK, FM))
    c.add(para(x + 20, 560, what, w - 40, 15, col, 500))
c.add(text(48, 638, "/ip/address/print where interface=ether1   y   /ip/cloud/print (public-address)", 16, 500, BLUE, FM))
save(c, "24-paso1.svg")

# ------------------------------------------------------------------ 24-paso3.svg
c = Canvas(K + " · Paso 3", "Qué puerto de afuera va a qué NVR")
c.add(text(48, 146, "PUERTOS DE FÁBRICA (CAMBIABLES EN EL NVR)", 14, 600, INK3, FM, ls=1.6))
rows_ = [("Hikvision", "8000 TCP", "app e iVMS-4200", OK), ("Hikvision", "554 / 10554", "RTSP", INK2),
         ("Hikvision", "80 / 443", "web: mejor no", ALERT), ("Dahua", "37777 TCP", "SmartPSS y DMSS", OK),
         ("Dahua", "37778 UDP", "si no hay video", WARN), ("Dahua", "554", "RTSP", INK2), ("Dahua", "80 / 443", "web: mejor no", ALERT)]
TX, TY, RHt, widths = 48, 162, 52, [140, 150, 230]
W = sum(widths)
c.add(rect(TX, TY, W, RHt * len(rows_), WHITE, LINE2, 1.5, 12))
for r, (brand, port, use, col) in enumerate(rows_):
    ry = TY + r * RHt
    if r:
        c.add(f'<path d="M{TX + 12} {ry}H{TX + W - 12}" stroke="{LINE}" stroke-width="1"/>')
    c.add(text(TX + 16, ry + 32, brand, 16, 600, INK, FB))
    c.add(text(TX + widths[0] + 12, ry + 32, port, 16, 600, BLUE, FM))
    c.add(text(TX + widths[0] + widths[1] + 12, ry + 32, use, 16, 500, col, FB))

# mapa: una IP pública, tres puertos externos
MX = 640
c.add(text(MX, 146, "UNA IP PÚBLICA, VARIOS NVR", 14, 600, INK3, FM, ls=1.6))
c.add(rect(MX, 162, 160, 364, DEEP, DEEP, 2, 18))
c.add(text(MX + 80, 196, "203.0.113.10", 15, 600, CYAN_T, FM, anchor="middle"))
maps = [(":18000", "NVR1", "192.168.88.50", ":8000", 230), (":18554", "NVR1", "192.168.88.50", ":554", 330), (":18001", "NVR2", "192.168.88.51", ":8000", 450)]
for ext, n, ip, inn, yy in maps:
    c.add(rect(MX + 16, yy - 22, 128, 40, "#0B3A66", "#4E7396", 1.5, 10))
    c.add(text(MX + 80, yy + 5, ext, 17, 600, AMBER_T, FM, anchor="middle"))
    c.add(arrow((MX + 164, yy - 2), (MX + 330, yy - 2), kind="ok", label=inn, label_dy=-10))
    c.add(mini(MX + 334, yy - 38, 178, 72, n, ip, hl=OK, title_size=17))
c.add(Note(48, 548, 1104, "En la app: IP pública (o nombre DDNS) y el puerto de afuera. dst-port es el de afuera; to-ports, el del NVR.", kind="info", size=15))
c.add(text(48, 650, "Hikvision: puertos según learncctv.com y un distribuidor; Dahua: aviso oficial. Confirmá en tu modelo.", 14, 500, INK3, FB))
save(c, "24-paso3.svg")

# ------------------------------------------------------------------ 24-paso7.svg
c = Canvas(K + " · Paso 7", "Hairpin: dos cambios de ida, dos de vuelta")
c.add(mini(48, 126, 230, 72, "PC de la oficina", "192.168.88.20", icon="laptop", title_size=17))
c.add(mini(485, 126, 230, 72, "MikroTik", "LAN 192.168.88.1", dark=True, title_size=17))
c.add(mini(922, 126, 230, 72, "NVR", "192.168.88.50", hl=OK, title_size=17))
c.add(arrow((282, 162), (481, 162), kind="logical", label="a la IP pública", label_dy=-14))
c.add(arrow((719, 162), (918, 162), kind="logical", label="dst-nat + masquerade", label_dy=-14))
c.add(text(48, 238, "IDA", 14, 600, INK3, FM, ls=1.6))
P = [(48, "Sale de la PC", "192.168.88.20", "203.0.113.10:18000", None, "plain"),
     (420, "Después del dst-nat", "192.168.88.20", "192.168.88.50:8000", "dst", "plain"),
     (792, "Después del masquerade", "192.168.88.1", "192.168.88.50:8000", "src", "plain")]
for x, h, s, d, ch, k in P:
    c.add(packet(x, 252, 360, h, s, d, k, ch))
c.add(arrow((410, 304), (418, 304)))
c.add(arrow((782, 304), (790, 304)))
c.add(text(48, 392, "VUELTA", 14, 600, INK3, FM, ls=1.6))
c.add(packet(792, 406, 360, "Contesta el NVR", "192.168.88.50:8000", "192.168.88.1", "plain"))
c.add(packet(420, 406, 360, "El router deshace los dos", "203.0.113.10:18000", "192.168.88.20", "ok"))
c.add(arrow((790, 458), (782, 458), kind="ok"))
c.add(Mark(392, 458, ok=True))
c.add(para(48, 444, "La PC recibe respuesta de la IP a la que llamó. Sin el masquerade, el NVR le contestaría directo desde 192.168.88.50 y la PC la descartaría.", 320, 15, OK, 500))
c.add(Note(48, 538, 1104, "Alternativa: DNS local (nvr.ejemplo.com → 192.168.88.50). El NVR ve la IP real de cada PC, pero solo sirve si el puerto de afuera es igual al de adentro: el DNS cambia la IP, no el puerto.", kind="warn", size=15))
save(c, "24-paso7.svg")
