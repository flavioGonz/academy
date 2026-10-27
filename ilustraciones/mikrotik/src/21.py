"""Lección 21 · L2TP con IPsec."""
from _comun_12_22 import *

K = "MikroTik · Lección 21"

# ---------------------------------------------------------------- principal: capas
c = Canvas(K, "L2TP/IPsec: tres capas en una sola conexión")
nb = c.add(Laptop(48, 250, "Notebook", "cliente nativo", w=230))
rt = c.add(Box(922, 236, 230, 112, "MikroTik", "203.0.113.10", dark=True))
X1, X2 = 300, 900
c.add(pipe(X1, 180, X2 - X1, 224, OK, "IPsec · cifra todo", OK, .08, 15))
c.add(pipe(X1 + 30, 228, X2 - X1 - 60, 128, BLUE, "L2TP · el túnel (UDP 1701)", BLUE, .10, 15))
c.add(pipe(X1 + 60, 274, X2 - X1 - 120, 64, CYAN, None, None, .18))
c.add(text(X1 + 90, 312, "PPP · usuario y clave · IP del pool 192.168.89.x", 15, 600, INK, FM))
c.add(Label(600, 160, "UDP 500 negocia · los datos van en ESP, o en UDP 4500 si hay NAT (NAT-T)", 15, 500, OK, FM, anchor="middle"))
c.add(Cable(nb.right(), (X1, 292), "data", arrow=False))
c.add(Cable((X2, 292), rt.left(), "data", arrow=False))
c.add(Zone(922, 390, 230, 110, "LAN"))
c.add(text(1037, 452, "192.168.88.0/24", 16, 600, INK, FM, anchor="middle"))
c.add(Arrow(rt.bottom(), (1037, 404), bend="straight"))
c.add(Note(48, 440, 420, "use-ipsec=required: el servidor solo acepta L2TP dentro de IPsec. L2TP solo no cifra.", title="Lo que cifra es IPsec", kind="ok", size=15))
c.add(Note(490, 440, 412, "Pool, perfil PPP y un secret por persona con service=l2tp.", title="Lo que identifica es PPP", kind="info", size=15))
c.add(Label(48, 630, "Para quien solo tiene el cliente nativo: Windows, macOS, iOS o Android.", 17, 500, INK2))
save(c, "21.svg")

# ---------------------------------------------------------------- paso 3: puertos en input
c = Canvas(K + " · Paso 3", "Cuatro aperturas en input, arriba del drop")
c.add(Table(48, 140, ["abrir", "para qué"], [
    ["UDP 500", "IKE: IPsec negocia las claves"],
    ["UDP 4500", "NAT-T: IPsec cuando alguien está detrás de NAT"],
    ["UDP 1701", "L2TP (viaja dentro de IPsec)"],
    ["ipsec-esp", "ESP: los datos cifrados, sin NAT en el medio"],
], [220, 500], mono_cols=(0,), row_h=50))
c.add(Label(976, 156, "CHAIN=INPUT · DE ARRIBA ABAJO", 14, 600, INK3, FM, anchor="middle"))
rules = [("accept established,related", "info"), ("accept UDP 500,4500,1701  ← nueva", "ok"), ("accept ipsec-esp  ← nueva", "ok"),
         ("drop all not coming from LAN", "alert")]
for i, (r, k) in enumerate(rules):
    y = 174 + i * 62
    bg, fg = {"info": (WHITE, INK2), "ok": (OK_BG, OK), "alert": (ALERT_BG, ALERT)}[k]
    c.add(f'<rect x="800" y="{y}" width="352" height="50" rx="10" fill="{bg}" stroke="{LINE2 if k == "info" else fg}" stroke-width="1.5"/>')
    c.add(text(818, y + 31, r, 14, 600, fg, FM))
c.add(Note(800, 440, 352, "place-before=[find comment=\"defconf: drop all not coming from LAN\"]. Debajo del drop no sirven.", kind="warn", size=15))
c.add(Note(48, 440, 720, "El acceso a la LAN por el túnel va además en forward: una regla accept con ipsec-policy=in,ipsec arriba del FastTrack (paso 4).", kind="info", size=15))
save(c, "21-paso3.svg")

# ---------------------------------------------------------------- paso 5: Windows y NAT-T
c = Canvas(K + " · Paso 5", "Windows detrás de NAT: la clave de NAT-T")
nb = c.add(Laptop(48, 150, "Notebook", "Windows", w=230))
nat = c.add(Generic(350, 150, "Router de la casa", "NAT", icon="server", w=260))
srv = c.add(Box(922, 140, 230, 104, "MikroTik", "203.0.113.10", dark=True))
net = c.add(Internet(680, 150, "Internet", "", w=170))
c.add(Cable(nb.right(), nat.left(), "data"))
c.add(Cable(nat.right(), net.left(), "data"))
c.add(Cable(net.right(), srv.left(), "data"))
c.add(Table(48, 290, ["valor", "cuándo"], [
    ["0", "por defecto: no arma IPsec con NAT-T hacia servidores detrás de NAT"],
    ["1", "el servidor está detrás de NAT"],
    ["2", "servidor y cliente pueden estar detrás de NAT"],
], [120, 984], mono_cols=(0,), hl_row=2, row_h=48))
c.add(Terminal(48, 506, 1104, ["New-ItemProperty -Path \"HKLM:\\SYSTEM\\CurrentControlSet\\Services\\PolicyAgent\"",
                                "  -Name AssumeUDPEncapsulationContextOnSendRule -PropertyType DWord -Value 2 -Force", "Restart-Computer"],
               title="POWERSHELL COMO ADMINISTRADOR"))
save(c, "21-paso5.svg")
