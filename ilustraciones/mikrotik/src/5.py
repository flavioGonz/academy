"""Lección 5 · VLAN por sistema: principal + pasos 1, 2 y 4."""
from _mt import *

K = "MikroTik"
V = {10: ("#5B6F84", "datos"), 20: (BLUE, "CCTV"), 30: (CYAN, "acceso"), 99: (NAVY, "gestión")}


def vchip(x, y, vid, anchor="middle", label=True):
    col, name = V[vid]
    s = f"VLAN {vid} · {name}" if label else f"{vid}"
    w = len(s) * 9.2 + 26
    x0 = x - w / 2 if anchor == "middle" else x
    return rect(x0, y - 21, w, 30, col, col, 0, 15) + text(x0 + w / 2, y, s, 15, 600, WHITE, FM, anchor="middle")


# ------------------------------------------------------------------ 5.svg principal
c = Canvas(K, "Un bridge, una VLAN por sistema")
c.add(rect(330, 130, 540, 104, DEEP, DEEP, 2, 18))
c.add(text(354, 166, "MikroTik · un solo bridge", 20, 600, WHITE, FD))
c.add(text(354, 194, "vlan-filtering=yes", 15, 500, CYAN, FM))
c.add(text(354, 218, "rutea entre VLAN: ahí actúa el firewall", 15, 400, "#9FC3E3", FB))
c.add(rect(48, 336, 1104, 74, WHITE, LINE2, 2, 16))
c.add(text(72, 380, "Switch del piso", 19, 600, INK, FD))
c.add(text(1128, 380, "puertos access: el puerto le pone la VLAN al equipo", 15, 500, INK3, FB, anchor="end"))
# trunk: 4 líneas paralelas
for i, vid in enumerate([10, 20, 30, 99]):
    xx = 560 + i * 26
    c.add(line(xx, 234, xx, 336, V[vid][0], 5))
c.add(text(680, 280, "trunk", 17, 700, INK, FM))
c.add(text(680, 302, "10 · 20 · 30 · 99 etiquetadas", 15, 500, INK3, FB))
# equipos
devs = [(Camera, "Cámaras", "NVR y cámaras", 20, 48), (Generic, "Control de acceso", "controladora", 30, 446), (Laptop, "PCs oficina", "datos", 10, 844)]
for cls, t, s_, vid, x in devs:
    d = c.add(Generic(x, 490, t, s_, icon="door", w=300) if cls is Generic else cls(x, 490, t, s_, w=300))
    c.add(line(x + 150, 410, x + 150, 490, V[vid][0], 5))
    c.add(text(x + 164, 456, "access", 14, 600, INK3, FM))
    c.add(vchip(x + 150, 616, vid))
c.add(Note(912, 130, 240, "La gestión del router va por la VLAN 99, nunca por la VLAN 1.", kind="info", size=15))
c.add(Note(48, 130, 260, "Una cámara infectada no ve las PCs: para cruzar tiene que pasar por el router.", kind="ok", size=15))
save(c, "5.svg")

# ------------------------------------------------------------------ 5-paso1.svg
c = Canvas(K + " · Paso 1", "Primero, un puerto de rescate fuera del bridge")
P = ["ether1", "ether2", "ether3", "ether4", "ether5"]
r = c.add(Router(160, 140, "Router de laboratorio", "RouterOS 7", ports=P, hl={"ether5": OK}))
bx0 = r.port("ether2")[0] - 46
bx1 = r.port("ether4")[0] + 46
c.add(rect(bx0, 220, bx1 - bx0, 100, "none", CYAN, 2.5, 14, dash="7 6"))
c.add(text((bx0 + bx1) / 2, 352, "bridge (acá se van a armar las VLAN)", 15, 600, CYAN, FB, anchor="middle"))
x5, yb = r.port("ether5")
c.add(pill(x5 + 18, 406, "fuera del bridge", "ok", anchor="start"))
n = c.add(Laptop(x5 - 125, 440, "Notebook", "10.255.255.2/30", hl=OK, w=250))
c.add(Cable(r.port("ether5"), (x5, 440), kind="data"))
c.add(Step(x5 - 26, 400, 1))
c.add(pill(630, 274, "ether5 · 10.255.255.1/30", "dark", anchor="start"))
c.add(Note(48, 420, 330, "Si al activar el filtrado de VLAN te quedás sin acceso por los puertos del bridge, ether5 no se entera: seguís adentro por ahí.", title="Por qué un puerto aparte", kind="info", size=16))
c.add(Note(48, 590, 1104, "Conectate por ether5 antes de seguir. Desde ahora configurás todo por ese cable.", kind="warn", size=15))
save(c, "5-paso1.svg")

# ------------------------------------------------------------------ 5-paso2.svg
c = Canvas(K + " · Paso 2", "La tabla VLAN: quién lleva qué y cómo")
cols = ["bridge", "ether2", "ether3", "ether4"]
sub = ["el CPU del router", "cámara", "cámara", "trunk"]
X0, Y0, CW, RH = 250, 140, 225, 64
c.add(text(48, Y0 + 40, "puerto →", 15, 500, INK3, FM))
for j, (p, s) in enumerate(zip(cols, sub)):
    x = X0 + j * CW
    c.add(rect(x + 6, Y0, CW - 12, 60, DEEP if j == 0 else WHITE, DEEP if j == 0 else LINE2, 2, 12))
    c.add(text(x + CW / 2, Y0 + 28, p, 17, 600, WHITE if j == 0 else INK, FM, anchor="middle"))
    c.add(text(x + CW / 2, Y0 + 48, s, 14, 400, "#9FC3E3" if j == 0 else INK3, FB, anchor="middle"))
cells = {20: ["tagged", "untagged", "untagged", "tagged"], 99: ["tagged", "", "", "tagged"]}
for i, vid in enumerate([20, 99]):
    y = Y0 + 80 + i * (RH + 12)
    c.add(vchip(48, y + 38, vid, anchor="start"))
    for j, v in enumerate(cells[vid]):
        x = X0 + j * CW
        if v:
            k = "blue" if v == "tagged" else "cyan"
            c.add(rect(x + 6, y + 6, CW - 12, RH - 12, SOFT if v == "tagged" else "#E2F5FB", BLUE if v == "tagged" else CYAN, 1.5, 10))
            c.add(text(x + CW / 2, y + 38, "con etiqueta" if v == "tagged" else "sin etiqueta", 15, 600, BLUE if v == "tagged" else "#0B7FA6", FB, anchor="middle"))
        else:
            c.add(text(x + CW / 2, y + 38, "no pasa", 15, 400, INK3, FB, anchor="middle"))
# configuración de puertos
y = 400
c.add(caption(48, y, "Y en cada puerto"))
c.add(card(48, y + 16, 540, 150, "ether2 y ether3 · access", None, kind="info"))
c.add(text(68, y + 92, "pvid=20", 15, 600, BLUE, FM))
c.add(text(68, y + 118, "frame-types=admit-only-untagged-…", 15, 500, INK2, FM))
c.add(text(68, y + 144, "ingress-filtering=yes", 15, 500, INK2, FM))
c.add(card(612, y + 16, 540, 150, "ether4 · trunk", None, kind="info"))
c.add(text(632, y + 92, "frame-types=admit-only-vlan-tagged", 15, 500, INK2, FM))
c.add(text(632, y + 118, "ingress-filtering=yes", 15, 500, INK2, FM))
c.add(text(632, y + 144, "sin etiqueta: se descarta", 15, 500, ALERT, FB))
c.add(text(48, 612, "Si bridge no figura como tagged en una VLAN, el router no ve esa VLAN: ni IP, ni DHCP, ni gestión.", 16, 500, INK2, FB))
save(c, "5-paso2.svg")

# ------------------------------------------------------------------ 5-paso4.svg
c = Canvas(K + " · Paso 4", "vlan-filtering=yes es lo último que se toca")
items = [("Rescate", "ether5 con IP propia"), ("Puertos y tabla", "pvid, filtros, VLAN 20 y 99"), ("Capa 3", "IP en vlan20 y vlan99")]
for i, (t, s_) in enumerate(items):
    x = 48 + i * 270
    c.add(rect(x, 160, 254, 120, WHITE, OK, 2, 14))
    c.add(mark(x + 30, 194, ok=True))
    c.add(text(x + 20, 240, t, 18, 600, INK, FD))
    c.add(text(x + 20, 264, s_, 15, 400, INK3, FB))
    c.add(Step(x + 234, 160, i + 1, INK3))
c.add(arrow((848, 220), (880, 220)))
c.add(rect(888, 140, 264, 160, DEEP, CYAN, 3, 18))
c.add(text(912, 182, "Último", 15, 600, CYAN, FM))
c.add(text(912, 216, "vlan-filtering", 21, 600, WHITE, FM))
c.add(text(912, 244, "=yes", 21, 600, WHITE, FM))
c.add(text(912, 278, "desde ether5", 15, 500, "#9FC3E3", FB))
c.add(Step(1152, 140, 4))
t, h = code(48, 330, 1104, [("/interface/bridge/vlan/print", "#D9E9F8"), ("# revisá: bridge tagged en 20 y 99, ether4 tagged, ether2 y ether3 untagged en 20", GRAY_T), ("/interface/bridge/set bridge vlan-filtering=yes", CYAN_T)], title="TERMINAL · DESDE ETHER5")
c.add(t)
c.add(Note(48, 330 + h + 24, 1104, "Si activás el filtrado primero y la gestión todavía no está en su VLAN, el puerto por el que estás conectado deja de hablar con el router. Por eso: rescate abierto, revisión de la tabla y recién ahí el interruptor.", kind="warn", size=16))
save(c, "5-paso4.svg")
