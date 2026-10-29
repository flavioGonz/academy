"""Lección 19 · Back To Home."""
import random
from _comun_12_22 import *

K = "MikroTik"


def qr(x, y, size=150, n=21, seed=7):
    """Código QR genérico (decorativo, no decodifica nada)."""
    rnd = random.Random(seed)
    cell = size / n
    out = [f'<rect x="{x - 8}" y="{y - 8}" width="{size + 16}" height="{size + 16}" rx="10" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>']
    for r in range(n):
        for k in range(n):
            finder = any(r0 <= r < r0 + 7 and k0 <= k < k0 + 7 for r0, k0 in ((0, 0), (0, n - 7), (n - 7, 0)))
            if finder:
                rr, kk = (r % 7 if r < 7 else (r - (n - 7))), (k % 7 if k < 7 else (k - (n - 7)))
                on = rr in (0, 6) or kk in (0, 6) or (2 <= rr <= 4 and 2 <= kk <= 4)
            else:
                on = rnd.random() < .45
            if on:
                out.append(f'<rect x="{x + k * cell:.1f}" y="{y + r * cell:.1f}" width="{cell + .3:.1f}" height="{cell + .3:.1f}" fill="{INK}"/>')
    return "".join(out)


# ---------------------------------------------------------------- principal
c = Canvas(K, "El celular entra al sitio aunque haya CGNAT")
ph = c.add(Phone(48, 270, "Celular", "datos móviles", w=230))
rel = c.add(CloudBox(400, 420, "Relay de MikroTik", "si el sitio no tiene IP pública", w=360))
rt = c.add(Box(560, 140, 270, 130, "MikroTik", "ARM o ARM64 · 7.12+", dark=True))
c.add(Arrow(ph.right(-14), (rt.x - 6, rt.y + 60), "directo, con IP pública", kind="ok", label_at=.5, label_dy=-12))
c.add(Arrow(ph.right(14), (rel.x - 6, rel.y + 42), kind="flow"))
c.add(Arrow((rt.x + 135, rt.y + rt.h + 4), (rel.x + 260, rel.y - 6), "el router abre y mantiene la conexión", kind="logical", label_at=.5, label_dy=0, bend="straight"))
c.add(Zone(876, 140, 276, 300, "LAN 192.168.88.0/24"))
c.add(Generic(896, 180, "WinBox al router", "192.168.88.1", icon="server", w=240))
c.add(Generic(896, 300, "NVR", "192.168.88.50", icon="camera", w=240))
c.add(Cable((rt.x + rt.w, rt.y + 65), (894, 222), "data"))
c.add(Note(48, 540, 520, "WireGuard cifrado de punta a punta: el relay no lee el tráfico, pero por el relay puede ir más lento.", kind="info"))
c.add(Note(800, 480, 352, "RouterBOARD MIPS: Back To Home no está. Mirá architecture-name antes de prometerlo.", kind="warn", size=15))
save(c, "19.svg")

# ---------------------------------------------------------------- paso 3: QR al celular
c = Canvas(K + " · Paso 3", "Del QR al celular, y probá con datos móviles")
c.add(Terminal(48, 140, 470, ["/ip/cloud/back-to-home-user/", "  show-client-config [find name=tecnico-lucia]"], title="EN EL ROUTER"))
c.add(qr(178, 290, 170))
c.add(Label(263, 498, "QR de tecnico-lucia", 15, 600, INK2, FM, anchor="middle"))
c.add(Arrow((370, 375), (520, 375), "escanear", bend="straight", label_dy=-12))
# teléfono dibujado
PX, PY = 540, 170
c.add(f'<rect x="{PX}" y="{PY}" width="210" height="380" rx="30" fill="{DEEP}"/><rect x="{PX + 14}" y="{PY + 40}" width="182" height="300" rx="10" fill="{WHITE}"/>')
c.add(text(PX + 105, PY + 26, "datos móviles", 14, 600, CYAN, FM, anchor="middle"))
c.add(text(PX + 30, PY + 80, "WireGuard", 18, 600, INK, FD))
c.add(text(PX + 30, PY + 106, "tecnico-lucia", 15, 500, INK2, FM))
c.add(f'<rect x="{PX + 30}" y="{PY + 126}" width="150" height="40" rx="20" fill="{OK}"/>')
c.add(text(PX + 105, PY + 152, "conectado", 15, 600, WHITE, FB, anchor="middle"))
c.add(para(PX + 30, PY + 210, "Probá entrar a la LAN del sitio", 150, 15, INK2))
c.add(Arrow((PX + 220, 300), (850, 230), kind="ok"))
c.add(Arrow((PX + 220, 380), (850, 420), kind="ok"))
c.add(Generic(860, 190, "WinBox al router", "192.168.88.1", icon="server", w=292))
c.add(Generic(860, 380, "NVR de ejemplo", "192.168.88.50", icon="camera", w=292))
c.add(Note(48, 560, 1104, "Con datos móviles, no con el WiFi del sitio: así probás el camino de afuera, igual que cuando estés lejos.", kind="info"))
save(c, "19-paso3.svg")

# ---------------------------------------------------------------- paso 4: con LAN y sin LAN
c = Canvas(K + " · Paso 4", "Un usuario por equipo: con LAN o solo internet")
users = [
    ("tecnico-lucia", "allow-lan=yes", "client-allowed-address=192.168.88.0/24", "expires=30d", True),
    ("invitado", "allow-lan=no", "(por defecto)", "expires=1d", False),
]
for j, (nm, al, ca, ex, lan) in enumerate(users):
    x = 48 + j * 574
    c.add(panel(x, 140, 530, 350, None, "info"))
    c.add(Phone(x + 20, 160, nm, ex, w=300))
    c.add(Chip(x + 20, 296, al, "ok" if lan else "gray"))
    c.add(mono(x + 20, 332, ca, 14, INK3, 500))
    for k, (dest, ok) in enumerate([("Internet por el router", True), ("LAN 192.168.88.0/24", lan)]):
        yy = 380 + k * 64
        c.add(Mark(x + 40, yy, ok))
        c.add(text(x + 72, yy + 6, dest, 18, 600, OK if ok else ALERT))
c.add(Note(48, 516, 1104, "La restricción usa la lista LAN: tus redes locales tienen que estar en ella (paso 5). Para una baja, borrá el usuario; nunca revoques todo.", kind="warn"))
save(c, "19-paso4.svg")
