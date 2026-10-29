"""Lección 18 · Cloud a fondo."""
from _comun_12_22 import *

K = "MikroTik"

# ---------------------------------------------------------------- principal
c = Canvas(K, "DDNS: el nombre sigue a la IP, no abre la puerta")
rt = c.add(Box(48, 150, 300, 110, "MikroTik", "ddns-enabled=yes", dark=True))
cl = c.add(CloudBox(640, 160, "cloud2.mikrotik.com", "ve la public-address", w=330))
c.add(Arrow(rt.right(), cl.left(), "UDP 15252", bend="straight", label_dy=-14))
c.add(Label(494, 240, "tras NAT: cada minuto", 15, 500, INK3, FM, anchor="middle"))
# registro DNS
c.add(f'<rect x="560" y="300" width="592" height="72" rx="14" fill="{WHITE}" stroke="{BLUE}" stroke-width="2"/>')
c.add(text(582, 332, "<serie>.sn.mynetname.net  →  public-address", 17, 600, INK, FB))
c.add(text(582, 358, "TTL 60 s · /ip/cloud/force-update lo actualiza ya", 15, 400, INK3, FM))
c.add(Arrow(cl.bottom(), (805, 296), bend="straight"))
# técnico
nb = c.add(Laptop(48, 430, "Técnico", "resuelve el nombre", w=300))
c.add(Arrow(nb.right(), (554, 340), "1 · resuelve", label_at=.5, label_dy=-6, bend="auto"))
c.add(Arrow(nb.top(), (rt.x + 150, rt.y + rt.h + 6), "2 · intenta entrar", kind="alert", label_at=.5, label_dy=0, bend="straight"))
c.add(Note(560, 420, 592, "Llega a la IP, pero el firewall por defecto sigue descartando lo que entra de internet. Publicar un servicio es otra decisión (lección 32).", title="El nombre no abre nada", kind="alert"))
c.add(Note(48, 560, 1104, "Detrás de CGNAT el nombre apunta a una IP compartida del proveedor: para entrar, Back To Home (lección 30) o un concentrador (lección 31).", kind="warn"))
save(c, "18.svg")

# ---------------------------------------------------------------- paso 5: dos WAN
c = Canvas(K + " · Paso 5", "Con dos WAN, el nombre apunta a la que sale")
for j, (title, kind, a1, a2, ip) in enumerate([
        ("WAN 1 arriba", "ok", True, False, "203.0.113.10"),
        ("WAN 1 cortada", "warn", False, True, "198.51.100.7")]):
    x = 48 + j * 574
    c.add(panel(x, 140, 530, 410, title, kind))
    c.add(f'<rect x="{x + 30}" y="290" width="140" height="74" rx="12" fill="{DEEP}"/>')
    c.add(mono(x + 100, 333, "MikroTik", 16, WHITE, 600, anchor="middle"))
    for k, (nm, ipw, act) in enumerate([("WAN 1", "203.0.113.10", a1), ("WAN 2", "198.51.100.7", a2)]):
        yy = 196 + k * 150
        c.add(Cable((x + 170, 327), (x + 300, yy + 40), "ok" if act else "alert" if (k == 0 and not act) else "logical", arrow=False))
        c.add(Generic(x + 304, yy, nm, ipw, icon="globe", w=200, hl=None))
    if not a1:
        c.add(Mark(x + 236, 268, False))
    c.add(pill(x + 30, 470, 470, 52, "nombre  →  " + ip, OK_BG if a1 else WARN_BG, OK if a1 else WARN, 16, FM, 600))
c.add(Note(48, 572, 1104, "public-address es la IP del enlace por donde sale la ruta hacia la nube. Si cambia de WAN, el nombre la sigue en la próxima actualización.", kind="info"))
save(c, "18-paso5.svg")
