import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *


def node(x, y, name, up=True, w=150, sub="1 voto", qd=False):
    fill, st, col = (DEEP, DEEP, WHITE) if up else (GROUND, LINE2, INK3)
    if qd and up:
        fill, st, col = (WHITE, CYAN, CYAN)
    out = rect(x, y, w, 76, fill, st, rx=14, dash=None if up else "7 6")
    out += text(x + w / 2, y + 32, name, 18, 700, col, FM, anchor="middle")
    out += text(x + w / 2, y + 56, sub if up else "apagado", 15, 500, "#9FC3E3" if (up and not qd) else INK3, FB, anchor="middle")
    return out


# ---------------------------------------------------------------- 9.svg: quórum es mayoría
c = Canvas(K(), "Quórum es mayoría: por qué dos nodos no alcanzan")
c.add(NOLIG)
cases = [("Dos nodos, cae uno", [("pve1", True, False), ("pve2", False, False)], "1 de 2 votos", "Sin quórum: solo lectura", "alert"),
         ("Dos nodos + QDevice", [("pve1", True, False), ("pve2", False, False), ("QDevice", True, True)], "2 de 3 votos", "Con quórum: sigue andando", "ok"),
         ("Tres nodos, cae uno", [("pve1", True, False), ("pve2", True, False), ("pve3", False, False)], "2 de 3 votos", "Con quórum: sigue andando", "ok")]
for i, (t, nodes, votes, verdict, kd) in enumerate(cases):
    x = 48 + i * 376
    c.add(panel(x, 122, 352, 380, None, "info"))
    c.add(text(x + 20, 160, t, 20, 600, INK, FD))
    for j, (n, up, qd) in enumerate(nodes):
        nx = x + 20 + (j % 2) * 166
        ny = 186 + (j // 2) * 92
        c.add(node(nx, ny, n, up, 146, "1 voto", qd))
    c.add(text(x + 176, 410, votes, 26, 700, OK if kd == "ok" else ALERT, FD, anchor="middle"))
    c.add(rect(x + 20, 430, 312, 50, OK_BG if kd == "ok" else ALERT_BG, OK if kd == "ok" else ALERT, rx=25))
    c.add(text(x + 176, 462, verdict, 17, 700, OK if kd == "ok" else ALERT, FB, anchor="middle"))
c.add(Note(48, 528, 540, "Sin quórum, /etc/pve queda de solo lectura: no se crean ni arrancan VMs, y la HA no conmuta.", title="Qué pasa sin mayoría", kind="alert"))
c.add(Note(612, 528, 540, "Corosync: menos de 5 ms, red física propia y un segundo enlace. El QDevice va por TCP y puede estar en otra sede.", title="La red del clúster", kind="info"))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso4: pve2 apagado
c = Canvas(K(4), "Apagás pve2: pvecm status en pve1 dice Quorate: No")
c.add(NOLIG)
c.add(Step(48, 124, 4))
c.add(node(80, 140, "pve1", True, 200, "10.10.10.11"))
c.add(node(80, 250, "pve2", False, 200))
c.add(path("M180 216 V250", ALERT, 3, dash="6 6"))
sv, h = codebox(330, 128, 520, ["# pvecm status   (en pve1)", "Expected votes:   2", ("Total votes:      1", "#FFB4A6"),
                                "Quorum:           2", ("Quorate:          No", "#FFB4A6")], 16, 30, title="SALIDA RECORTADA")
c.add(sv)
c.add(rect(880, 128, 272, 190, ALERT_BG, ALERT, rx=16))
c.add(Mark(912, 166, False))
c.add(text(942, 172, "Crear una VM", 18, 700, ALERT, FB))
svg, _ = wrap(904, 214, "No te deja: con 1 voto de 2, /etc/pve está en solo lectura.", 230, 16, 400, INK2)
c.add(svg)
c.add(rect(80, 380, 1072, 110, WHITE, LINE2, rx=16))
c.add(text(104, 416, "La cuenta", 17, 600, INK3, FB))
c.add(text(104, 462, "Quorum = mayoría de Expected votes = 2.   Total votes = 1   →   1 < 2   →   sin quórum", 19, 600, INK, FM))
c.add(Note(80, 516, 1072, "En el paso 6, con el QDevice, Expected votes pasa a 3, Quorum a 2, y pve1 con el QDevice suman 2: Quorate: Yes.", kind="ok"))
save(c, "9-paso4.svg")

# ---------------------------------------------------------------- 9-paso5: el QDevice
c = Canvas(K(5), "El QDevice: un tercer voto que no es un nodo")
c.add(NOLIG)
c.add(Step(48, 124, 5))
c.add(node(120, 170, "pve1", True, 240, "10.10.10.11"))
c.add(node(120, 400, "pve2", True, 240, "10.10.10.12"))
c.add(path("M240 246 V400", BLUE, 4))
c.add(pill(240, 330, "corosync · UDP 5405-5412", BLUE, size=15))
c.add(rect(760, 280, 340, 110, WHITE, CYAN, rx=16))
c.add(text(780, 318, "Debian 10.10.10.13", 18, 700, CYAN, FM))
c.add(text(780, 346, "corosync-qnetd", 16, 600, INK, FM))
c.add(text(780, 370, "no corre VMs: solo vota", 15, 500, INK3, FB))
c.add(path("M360 208 C 560 208, 600 320, 756 320", CYAN, 3, dash="8 6", arrow=True))
c.add(path("M360 438 C 560 438, 600 352, 756 352", CYAN, 3, dash="8 6", arrow=True))
c.add(pill(560, 250, "TCP", CYAN, size=15))
c.add(text(120, 520, "En los dos nodos: corosync-qdevice. En pve1:", 17, 600, INK, FB))
c.add(code(120, 536, 460, "pvecm qdevice setup 10.10.10.13", 16))
c.add(Note(640, 470, 512, "El QDevice no exige la latencia de corosync: puede estar en otra sede. Se recomienda en clústeres pares, no en impares.", kind="info"))
save(c, "9-paso5.svg")
