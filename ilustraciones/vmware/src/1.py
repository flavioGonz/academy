import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 1.svg: qué licencia hay y qué habilita
c = Canvas(K(), "¿Qué licencia tiene el host? Lo que cada una habilita")
c.add(NOLIG)
cols = [("Suscripción VVF o VCF", "vigente, por núcleo", "info"),
        ("Standard o Ent. Plus", "solo hasta 8.0 U3", "warn"),
        ("ESXi gratuito", "8.0 Update 3e", "alert")]
x0, y0, cw = 312, 124, 280
c.add(panel(48, y0, 1104, 400, None, "info"))
for i, (t, s, k) in enumerate(cols):
    x = x0 + i * cw
    c.add(rect(x + 8, y0 + 12, cw - 16, 70, {"info": SOFT, "warn": WARN_BG, "alert": ALERT_BG}[k], {"info": BLUE, "warn": WARN, "alert": ALERT}[k], rx=12, sw=1.5))
    c.add(mid(x + cw / 2, y0 + 44, t, 18, 600, INK, FD))
    c.add(mid(x + cw / 2, y0 + 68, s, 15, 500, INK3, FM))
rows = [("vCenter", ["incluido", "incluido", "no se gestiona"]),
        ("vMotion y HA", ["sí", "sí", "no"]),
        ("Backup por API (VADP)", ["sí", "sí", "no"]),
        ("Soporte y parches", ["sí", "hasta 11/10/2027", "sin soporte"]),
        ("Límites", ["según edición", "no pasa a la 9", "2 CPU, 8 vCPU por VM"])]
for r, (name, vals) in enumerate(rows):
    y = y0 + 100 + r * 58
    if r:
        c.add(hline(64, 1136, y - 12))
    c.add(text(72, y + 22, name, 17, 600, INK, FB))
    for i, v in enumerate(vals):
        x = x0 + i * cw + cw / 2
        good = v in ("incluido", "sí")
        bad = v in ("no", "no se gestiona", "sin soporte")
        col = OK if good else (ALERT if bad else INK2)
        c.add(mid(x, y + 22, v, 16, 600 if (good or bad) else 500, col, FB))
c.add(Note(48, 546, 540, "Por núcleo físico, con un mínimo de 16 núcleos por CPU. vCenter viene incluido en la suscripción.", title="Cómo se cobra", kind="info"))
c.add(Note(612, 546, 540, "vSphere 8 (ESXi y vCenter) pierde soporte general el 11 de octubre de 2027.", title="Fecha para la ficha", kind="warn"))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso1: Host Client, Manage > Licensing
c = Canvas(K(1), "En el Host Client: Manage > Licensing")
c.add(NOLIG)
c.add(Step(48, 140, 1))
c.add(rect(48, 162, 720, 420, WHITE, LINE2, rx=16))
c.add(f'<path d="M48 176a14 14 0 0 1 14 -14h692a14 14 0 0 1 14 14v26h-720z" fill="{SOFT}"/>')
c.add(text(72, 190, "https://192.168.88.20/ui", 15, 600, BLUE, FM))
# barra lateral
c.add(rect(60, 216, 200, 352, GROUND, LINE, rx=10, sw=1.5))
side = [("Host", False, 0), ("Manage", True, 18), ("Monitor", False, 18), ("Virtual Machines", False, 0), ("Storage", False, 0), ("Networking", False, 0)]
for i, (s, on, ind) in enumerate(side):
    y = 236 + i * 52
    if on:
        c.add(rect(68 + ind, y, 184 - ind, 40, SOFT, CYAN, rx=8))
    c.add(text(84 + ind, y + 26, s, 15, 600 if on else 500, INK if on else INK2, FB))
# pestañas
tabs = ["System", "Hardware", "Licensing", "Packages"]
tx = 280
for t in tabs:
    w = len(t) * 9 + 26
    on = t == "Licensing"
    c.add(rect(tx, 224, w, 34, CYAN if on else WHITE, CYAN if on else LINE2, rx=17, sw=1.5))
    c.add(text(tx + w / 2, 247, t, 14, 600, WHITE if on else INK2, FM, anchor="middle"))
    tx += w + 8
fields = [("Clave", "XXXXX-XXXXX-XXXXX-…"), ("Producto", "lo que diga el host"), ("Funciones", "lista de habilitadas"), ("Vencimiento", "fecha o Never")]
for i, (k, v) in enumerate(fields):
    y = 290 + i * 66
    c.add(rect(280, y, 470, 50, GROUND, LINE2, rx=10, sw=1.5))
    c.add(text(300, y + 31, k, 16, 600, INK, FB))
    c.add(text(735, y + 31, v, 15, 500, INK2, FM, anchor="end"))
c.add(Note(800, 162, 352, "Clave, producto, funciones y vencimiento: los cuatro datos van a la ficha del cliente.", title="Anotá estos cuatro", kind="info"))
c.add(Note(800, 330, 352, "En el ejemplo el host es 192.168.88.20. En tu laboratorio, la IP que le diste en la DCUI, seguida de /ui.", kind="info"))
c.add(Note(800, 474, 352, "Si dice gratuito, no prometas vCenter, vMotion, HA ni backup por API.", kind="warn"))
save(c, "1-paso1.svg")

# ---------------------------------------------------------------- 1-paso3: núcleos físicos y licenciables
c = Canvas(K(3), "Núcleos físicos contra núcleos licenciables")
c.add(NOLIG)
c.add(Step(48, 140, 3))
t = Terminal(48, 162, 470, [("$ esxcli hardware cpu global get", "#9FE3F7"), "   CPU Packages: 2", "   CPU Cores: 16", "   …"], title="SSH AL HOST")
c.add(t)
c.add(text(48, 356, "Núcleos por CPU = CPU Cores / CPU Packages", 18, 600, INK, FB))
c.add(text(48, 384, "Por cada CPU se paga el mayor entre sus núcleos y 16.", 16, 400, INK2, FB))


def caso(x, y, titulo, cpus, nucleos, kind):
    lic = max(nucleos, 16)
    out = [panel(x, y, 530, 230, titulo, kind)]
    for i in range(cpus):
        cx = x + 24 + i * 250
        out.append(rect(cx, y + 54, 230, 100, WHITE, LINE2, rx=12))
        out.append(text(cx + 16, y + 80, f"CPU {i + 1}", 15, 600, INK3, FM))
        n = nucleos
        cols = 8
        size = 14 if n <= 8 else 12
        for k in range(min(n, 24)):
            r, q = divmod(k, cols)
            out.append(f'<rect x="{cx + 16 + q * 25}" y="{y + 92 + r * 18}" width="{size + 6}" height="{size}" rx="3" fill="{BLUE}"/>')
        for k in range(n, lic):
            r, q = divmod(k, cols)
            out.append(f'<rect x="{cx + 16 + q * 25}" y="{y + 92 + r * 18}" width="{size + 6}" height="{size}" rx="3" fill="none" stroke="{WARN}" stroke-width="1.5" stroke-dasharray="3 2"/>')
    fis, tot = cpus * nucleos, cpus * lic
    out.append(text(x + 24, y + 190, f"{fis} físicos", 18, 600, BLUE, FM))
    out.append(text(x + 506, y + 190, f"{tot} licenciables", 18, 700, WARN if tot > fis else OK, FM, anchor="end"))
    out.append(text(x + 24, y + 215, f"{cpus} CPU de {nucleos} núcleos", 15, 400, INK3, FB))
    return "".join(out)


c.add(caso(560, 124, "Ejemplo del laboratorio", 2, 8, "warn"))
c.add(caso(560, 380, "Con CPUs de 24 núcleos", 2, 24, "ok"))
c.add(f'<rect x="48" y="416" width="18" height="14" rx="3" fill="{BLUE}"/>')
c.add(text(76, 429, "núcleo real", 15, 500, INK2, FB))
c.add(f'<rect x="48" y="446" width="18" height="14" rx="3" fill="none" stroke="{WARN}" stroke-width="1.5" stroke-dasharray="3 2"/>')
c.add(text(76, 459, "núcleo que se paga sin existir", 15, 500, INK2, FB))
c.add(Note(48, 496, 470, "Con CPUs chicas pagás el doble de lo que tenés. Con 16 núcleos o más por CPU, la cuenta es 1 a 1.", kind="info"))
save(c, "1-paso3.svg")
