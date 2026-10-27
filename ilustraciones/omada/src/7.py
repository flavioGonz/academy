import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 7.svg: la VLAN separa, la ACL aísla
c = Canvas(K(), "La VLAN separa; la ACL del gateway aísla")
gw = c.add(Box(470, 286, 260, 84, "Gateway", "rutea entre VLAN", dark=True))
of = c.add(Box(48, 150, 330, 84, "Oficina · VLAN 1", "192.168.88.0/24"))
cc = c.add(Box(48, 420, 330, 84, "CCTV · VLAN 20", "10.10.20.0/24"))
it = c.add(Internet(822, 150, "Internet", "", w=330))
gu = c.add(Box(822, 420, 330, 84, "Invitados · VLAN 30", "10.10.30.0/24", hl=CYAN))
c.add(Cable(gw.left(-14), of.right(), kind="data"))
c.add(Cable(gw.left(14), cc.right(), kind="data"))
c.add(Cable(gw.right(-14), it.left(), kind="data"))
c.add(Cable(gw.right(14), gu.left(), kind="data"))
c.add(Mark(424, 250, ok=False))
c.add(Mark(424, 398, ok=False))
c.add(Mark(776, 250, ok=True))
c.add(tag(600, 418, "Deny: Invitados → Redes-Internas", "alert", mono=False))
c.add(text(600, 266, "desde Invitados", 15, 600, INK3, FM, anchor="middle"))
c.add(Note(48, 532, 540, "Las VLAN separan el broadcast, pero el gateway rutea entre ellas: sin una regla, las tres redes se ven.", title="Sin ACL", kind="warn"))
c.add(Note(612, 532, 540, "Con la regla en el gateway, Invitados sale a internet y no llega ni a la oficina ni a las cámaras.", title="Con ACL", kind="ok"))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso3: la regla y el orden
c = Canvas(K(3), "La regla de deny, y arriba de cualquier permit general")
c.add(Window(48, 124, 560, 290, "Omada · sitio", path="Network Security > ACL > Gateway ACL", rows=[
    ("Name", "Invitados-sin-interna"), ("Policy", "Deny"), ("Protocols", "All"), ("Source", "red Invitados"), ("Destination", "IP Group Redes-Internas")], hl=1))
c.add(Step(48, 124, 3))
c.add(text(48, 452, "Redes-Internas (paso 2): 192.168.88.0/24 y 10.10.20.0/24", 15, 500, INK2, FM))
for i, (title, rows, kd) in enumerate([("Bien", [("1", "Deny Invitados → Redes-Internas", "alert"), ("2", "Permit general", "ok")], "ok"),
                                         ("Mal", [("1", "Permit general", "ok"), ("2", "Deny Invitados → Redes-Internas", "alert")], "alert")]):
    y = 124 + i * 168
    c.add(panel(648, y, 504, 150, title, kd))
    for j, (n, r, k2) in enumerate(rows):
        yy = y + 58 + j * 42
        c.add(badge(684, yy + 12, n, r=14, size=15))
        c.add(tag(708, yy + 20, r, k2, mono=False, anchor="start"))
c.add(text(1128, 156, "la deny se evalúa primero", 15, 500, OK, FB, anchor="end"))
c.add(text(1128, 324, "la deny nunca llega a actuar", 15, 500, ALERT, FB, anchor="end"))
c.add(Note(648, 470, 504, "Las ACL se leen de arriba hacia abajo: la regla más específica va arriba.", kind="info"))
c.add(Note(48, 492, 560, "Una ACL mal ordenada en producción puede cortar las cámaras o el propio controlador: primero en laboratorio.", kind="alert"))
save(c, "7-paso3.svg")

# ---------------------------------------------------------------- 7-paso4: la prueba de los tres pings
c = Canvas(K(4), "Tres pings desde Invitados prueban el aislamiento")
c.add(Laptop(48, 132, "Notebook", "SSID Invitados-Lab", w=300))
c.add(text(48, 252, "conectada a la VLAN 30, toma 10.10.30.x", 15, 500, INK3, FM))
c.add(Step(48, 132, 4))
rows = [("ping 10.10.30.1", "responde", "es su propio gateway", "ok"),
        ("ping 192.168.88.1", "no responde", "la oficina quedó aislada", "ok"),
        ("ping 1.1.1.1", "responde", "sale a internet", "ok")]
for i, (cmd, res, why, kd) in enumerate(rows):
    y = 290 + i * 76
    c.add(code(48, y, 470, cmd, 17, h=52))
    c.add(tag(552, y + 34, res, "ok" if res == "responde" else "alert", mono=False, anchor="start"))
    c.add(Mark(720, y + 26, ok=True))
    c.add(text(752, y + 33, why, 17, 500, INK2, FB))
c.add(Note(612, 132, 540, "Si 192.168.88.1 responde, el deny está debajo de un permit general: subilo (paso 5).", title="Si la oficina responde", kind="warn"))
c.add(text(48, 560, "Lo esperado es justo eso: el gateway propio sí, la red interna no, internet sí.", 17, 600, INK, FB))
save(c, "7-paso4.svg")
