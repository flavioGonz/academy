"""Lección 36 · Zonas con interface lists: principal (la matriz) + pasos 2, 4 y 6.

Usa tools/ilus.py y los ayudantes de _mt.py, sin modificarlos. Regenerar:
  python3 /home/claude/ies-training/ilustraciones/mikrotik/src/36.py
  python3 /home/claude/ies-training/tools/render_svg.py /home/claude/ies-training/ilustraciones/mikrotik/36.svg ...
"""
import sys
sys.path.insert(0, "/home/claude/ies-training/ilustraciones/mikrotik/src")
from _mt import *  # noqa: F401,F403
from _mt import rect, line, text, wrap, rows, caption, code, save, arrow, mark, pill, GRAY_T, CYAN_T, AMBER_T, GREEN_T, RED_T

K = "MikroTik"
CELL = {"si": (OK_BG, OK), "no": (ALERT_BG, ALERT), "parcial": (WARN_BG, WARN), "self": (GROUND, INK3)}


# ------------------------------------------------------------------ 36.svg: la matriz
c = Canvas(K, "La matriz de zonas: quién habla con quién")
cols = ["WAN", "GESTION", "ADMIN", "CCTV", "ACCESOS", "INVITADOS", "ROUTER"]
data = [
    ("GESTION+VPN", [("sí", "si"), ("·", "self"), ("sí", "si"), ("sí", "si"), ("sí", "si"), ("sí", "si"), ("todo", "si")]),
    ("ADMIN", [("sí", "si"), ("no", "no"), ("·", "self"), ("solo NVR", "parcial"), ("no", "no"), ("no", "no"), ("DNS·DHCP", "parcial")]),
    ("CCTV", [("NTP", "parcial"), ("no", "no"), ("no", "no"), ("·", "self"), ("no", "no"), ("no", "no"), ("DNS·DHCP", "parcial")]),
    ("ACCESOS", [("NTP", "parcial"), ("no", "no"), ("no", "no"), ("no", "no"), ("·", "self"), ("no", "no"), ("DNS·DHCP", "parcial")]),
    ("INVITADOS", [("sí", "si"), ("no", "no"), ("no", "no"), ("no", "no"), ("no", "no"), ("·", "self"), ("DNS·DHCP", "parcial")]),
    ("WAN", [("·", "self"), ("no", "no"), ("no", "no"), ("dst-nat", "parcial"), ("no", "no"), ("no", "no"), ("túnel", "parcial")]),
]
X0, Y0, W0, CW, RH = 48, 136, 170, 133, 54
# encabezado
c.add(rect(X0, Y0, W0 + CW * 7, RH, SOFT, LINE2, 1.5, 12))
c.add(text(X0 + 16, Y0 + 34, "de ↓   a →", 15, 600, INK3, FM))
for j, h in enumerate(cols):
    c.add(text(X0 + W0 + CW * j + CW / 2, Y0 + 34, h, 15, 700, NAVY if h != "ROUTER" else BLUE, FM, anchor="middle"))
for i, (zona, cells) in enumerate(data):
    y = Y0 + RH * (i + 1) + 6
    c.add(rect(X0, y, W0 - 8, RH - 8, DEEP, DEEP, 0, 10))
    c.add(text(X0 + 14, y + 30, zona, 15, 700, WHITE, FM))
    for j, (s, k) in enumerate(cells):
        bg, fg = CELL[k]
        x = X0 + W0 + CW * j + 4
        c.add(rect(x, y, CW - 8, RH - 8, bg, bg if k != "self" else LINE, 1.5, 10))
        c.add(text(x + (CW - 8) / 2, y + 30, s, 15, 700 if k != "self" else 400, fg, FM, anchor="middle"))
yl = Y0 + RH * 7 + 40
c.add(pill(48, yl, "verde: regla accept", "ok", anchor="start"))
c.add(pill(290, yl, "ámbar: accept con puerto o destino", "warn", anchor="start"))
c.add(pill(660, yl, "rojo: lo corta el drop final", "alert", anchor="start"))
c.add(text(48, yl + 46, "Cada casillero verde o ámbar es una regla de forward o de input. Los rojos no se escriben: los descarta el drop del final.", 16, 500, INK2, FB))
save(c, "36.svg")


# ------------------------------------------------------------------ paso 2: interfaces, zonas, listas compuestas
c = Canvas(K + " · paso 2", "Cada interfaz en una zona; las compuestas, por include")
c.add(caption(48, 140, "interfaz (banco)"))
c.add(caption(400, 140, "zona (miembro estático)"))
c.add(caption(790, 140, "lista compuesta (include)"))
ifs = [("bridge (ether2)", "GESTION", BLUE), ("ether3", "CCTV", CYAN), ("ether4", "ACCESOS", CYAN),
       ("ether5", "INVITADOS", WARN), ("wg-gestion", "VPN", BLUE), ("vlan10-admin", "ADMIN", OK)]
zy = {}
for i, (itf, zona, col) in enumerate(ifs):
    y = 160 + i * 72
    dashed = itf == "vlan10-admin"
    c.add(rect(48, y, 250, 52, WHITE, LINE2, 2, 12, dash="6 6" if dashed else None))
    c.add(text(66, y + 33, itf, 16, 600, INK, FM))
    c.add(rect(400, y, 220, 52, WHITE, col, 3, 12))
    c.add(text(418, y + 33, zona, 17, 700, col, FM))
    c.add(arrow((298, y + 26), (400, y + 26), kind="logical" if dashed else "flow"))
    zy[zona] = y + 26
c.add(text(48, 160 + 6 * 72 - 6, "vlan10-admin entra en el paso 6", 15, 500, INK3, FB))
# compuestas
comp = [("GESTION", "include=VPN", "VPN cuenta como gestión", 160),
        ("SISTEMAS", "include=CCTV,ACCESOS", "NTP para los sistemas", 268),
        ("CLIENTES", "include=ADMIN,CCTV,", "ACCESOS,INVITADOS · DNS y DHCP", 376)]
for name, inc, why, y in comp:
    c.add(rect(790, y, 362, 92, DEEP, DEEP, 2, 14))
    c.add(text(810, y + 32, name, 18, 700, WHITE, FM))
    c.add(text(810, y + 56, inc, 15, 500, CYAN_T, FM))
    c.add(text(810, y + 78, why, 15, 400, GRAY_T, FB))
c.add(arrow((620, zy["VPN"]), (790, 206), kind="logical"))
c.add(Note(790, 494, 362, "Orden: 1 include suma, 2 exclude resta, 3 los miembros estáticos suman. member/print solo muestra los estáticos.", kind="info", size=15))
save(c, "36-paso2.svg")


# ------------------------------------------------------------------ paso 4: forward por par de zonas
c = Canvas(K + " · paso 4", "Forward: una regla por casillero y el resto al drop")
c.add(caption(48, 146, "dos paquetes del NVR (ether3, zona CCTV)"))
c.add(rect(48, 166, 330, 104, OK_BG, OK, 2, 14))
c.add(text(68, 198, "10.10.20.50 → WAN", 16, 600, INK, FM))
c.add(text(68, 224, "UDP 123 (NTP)", 16, 600, OK, FM))
c.add(text(68, 250, "CCTV está en SISTEMAS", 15, 400, INK2, FB))
c.add(rect(48, 420, 330, 104, ALERT_BG, ALERT, 2, 14))
c.add(text(68, 452, "10.10.20.50 → WAN", 16, 600, INK, FM))
c.add(text(68, 478, "TCP 443 (navegar)", 16, 600, ALERT, FM))
c.add(text(68, 504, "ningún casillero lo permite", 15, 400, INK2, FB))
c.add(caption(470, 146, "chain=forward · después de la defconf"))
rl = [("GESTION a todas", "plain"), ("ADMIN a WAN", "plain"), ("INVITADOS a WAN", "plain"),
      ("ADMIN al NVR · tcp 80,443,8000", "plain"), ("SISTEMAS a WAN · udp 123", "ok"),
      ("WAN a lo publicado · dstnat", "plain"), ("drop final · log ZONA-DROP", "alert")]
c.add(rows(470, 166, 682, rl, h=42, gap=10, size=15))
ry = lambda i: 166 + i * 52 + 21
c.add(arrow((378, 218), (470, ry(4)), kind="ok"))
c.add(arrow((378, 472), (470, ry(6)), kind="alert"))
c.add(text(470, 560, "Cada regla usa in-interface-list y out-interface-list: la zona de origen y la de destino.", 16, 500, INK2, FB))
c.add(text(470, 588, "Lo que no coincide con ningún casillero baja hasta el drop final.", 16, 500, INK2, FB))
save(c, "36-paso4.svg")


# ------------------------------------------------------------------ paso 6: una red nueva sin tocar reglas
c = Canvas(K + " · paso 6", "Una red nueva entra a la zona, no al firewall")
t, h = code(48, 140, 560, [
    "/interface/vlan/add name=vlan10-admin \\",
    "    interface=bridge vlan-id=10",
    "/ip/address/add address=10.10.10.1/24 \\",
    "    interface=vlan10-admin",
    ("/interface/list/member/add list=ADMIN \\", GREEN_T),
    ("    interface=vlan10-admin", GREEN_T),
], title="TERMINAL · TRES LÍNEAS, CERO REGLAS NUEVAS", lh=30)
c.add(t)
c.add(rect(690, 140, 200, 60, WHITE, OK, 3, 12))
c.add(text(790, 178, "vlan10-admin", 16, 700, INK, FM, anchor="middle"))
c.add(arrow((790, 200), (790, 250), kind="ok"))
c.add(rect(690, 250, 200, 60, OK_BG, OK, 3, 12))
c.add(text(790, 288, "ADMIN", 18, 700, OK, FM, anchor="middle"))
c.add(caption(930, 158, "ya aplica"))
for i, (s, ok) in enumerate([("ADMIN a WAN", True), ("ADMIN al NVR", True), ("DNS y DHCP", True), ("WinBox al router", False)]):
    y = 176 + i * 50
    c.add(mark(948, y + 14, ok))
    c.add(text(978, y + 20, s, 16, 600, INK if ok else ALERT, FM))
c.add(Note(48, 400, 520, "La WAN pasa a PPPoE: pppoe-out1 va a la lista WAN, o las reglas de WAN no la ven.", title="Lo mismo con cualquier interfaz", kind="warn", size=15))
c.add(Note(632, 400, 520, "Los túneles L2TP o SSTP del servidor son dinámicos: entran a VPN desde el perfil, /ppp/profile interface-list=VPN.", title="Interfaces dinámicas", kind="info", size=15))
save(c, "36-paso6.svg")
