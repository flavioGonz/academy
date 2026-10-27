import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 10.svg: lo que pide la HA
c = Canvas(K(), "Alta disponibilidad: tres requisitos y un freno")
c.add(NOLIG)
reqs = [("Tres votos", "Tres nodos, o dos y un QDevice. Sin quórum, la HA no mueve nada.", "9: Tres votos"),
        ("Almacenamiento compartido", "NFS, iSCSI, Ceph, o replicación ZFS. Con disco local, la VM queda en el nodo caído.", ""),
        ("Fencing por watchdog", "El nodo aislado se reinicia solo antes de que la VM arranque en otro lado.", "")]
for i, (t, d, _) in enumerate(reqs):
    x = 48 + i * 376
    c.add(panel(x, 122, 352, 190, None, "info"))
    c.add(badge(x + 36, 162, str(i + 1), CYAN))
    c.add(text(x + 66, 169, t, 19, 700, INK, FB))
    svg, _ = wrap(x + 24, 214, d, 310, 16, 400, INK2)
    c.add(svg)
c.add(text(48, 360, "Cuando cae un nodo", 19, 600, INK, FD))
flow = [("pve1 cae o queda aislado", "alert"), ("pierde quórum: su watchdog lo reinicia", "warn"), ("la VM arranca en pve2", "ok")]
for i, (s, kd) in enumerate(flow):
    x = 48 + i * 376
    bg, fg = {"alert": (ALERT_BG, ALERT), "warn": (WARN_BG, WARN), "ok": (OK_BG, OK)}[kd]
    c.add(rect(x, 378, 340, 64, bg, fg, rx=14))
    c.add(text(x + 170, 417, s, 17, 700, fg, FB, anchor="middle"))
    if i < 2:
        c.add(path(f"M{x + 344} 410 H{x + 372}", INK3, 3, arrow=True))
c.add(rect(48, 476, 1104, 146, DEEP, DEEP, rx=16))
c.add(text(72, 514, "El freno, desde Proxmox VE 9.2", 19, 600, WHITE, FD))
c.add(text(72, 548, "Antes de tocar la red o corosync:", 16, 500, "#9FC3E3", FB))
c.add(code(72, 562, 460, "ha-manager crm-command disarm-ha freeze", 15, color="#FFD38A"))
c.add(text(612, 548, "Terminado el mantenimiento:", 16, 500, "#9FC3E3", FB))
c.add(code(612, 562, 360, "ha-manager crm-command arm-ha", 15, color="#7FE0B0"))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso1: migración en vivo
c = Canvas(K(1), "qm migrate --online: qué viaja por la red")
c.add(NOLIG)
c.add(Step(48, 124, 1))
for row, (y, t, sub, items, kd) in enumerate([(130, "Con almacenamiento compartido", "qm migrate 100 pve2 --online", ["RAM", "estado de la VM"], "ok"),
                                               (370, "Con disco local", "… --online --with-local-disks", ["RAM", "estado de la VM", "disco completo"], "warn")]):
    c.add(text(80, y + 6, t, 19, 600, INK, FD))
    c.add(text(80, y + 32, sub, 15, 600, BLUE, FM))
    c.add(host(80, y + 52, 260, 100, "pve1", "origen"))
    c.add(host(860, y + 52, 260, 100, "pve2", "destino"))
    c.add(path(f"M340 {y + 102} H856", OK if kd == "ok" else BLUE, 4, arrow=True))
    for j, it in enumerate(items):
        c.add(tag([380, 500, 690][j], y + 92, it, kd if it == "disco completo" else "info", 15, mono=False, anchor="start"))
    if kd == "ok":
        c.add(rect(400, y + 128, 400, 52, SOFT, LINE2, rx=12))
        c.add(text(600, y + 160, "disco en el storage compartido: no viaja", 15, 600, INK2, FB, anchor="middle"))
c.add(Note(80, 586, 1040, "La VM sigue andando durante la copia. Con CPU tipo host y procesadores distintos, la migración en vivo puede fallar.", kind="info"))
save(c, "10-paso1.svg")

# ---------------------------------------------------------------- 10-paso3: estados del fencing
c = Canvas(K(3), "disarm-ha: el fencing pasa de armed a disarmed")
c.add(NOLIG)
c.add(Step(48, 124, 3))
states = [("armed", "los watchdogs están abiertos: un nodo sin quórum se reinicia", "ok"),
          ("disarming", "congela los servicios y espera que cada nodo suelte su watchdog", "warn"),
          ("disarmed", "sin fencing ni failover: la HA no protege nada", "alert")]
for i, (s, d, kd) in enumerate(states):
    x = 48 + i * 376
    bg, fg = {"ok": (OK_BG, OK), "warn": (WARN_BG, WARN), "alert": (ALERT_BG, ALERT)}[kd]
    c.add(rect(x, 150, 340, 170, bg, fg, rx=16))
    c.add(text(x + 24, 196, s, 26, 700, fg, FM))
    svg, _ = wrap(x + 24, 236, d, 296, 16, 400, INK2)
    c.add(svg)
    if i < 2:
        c.add(path(f"M{x + 344} 235 H{x + 372}", INK3, 3, arrow=True))
c.add(text(48, 452, "Lo ves en la línea de fencing de:", 17, 600, INK, FB))
c.add(code(340, 424, 260, "ha-manager status", 16))
c.add(path("M808 324 V378 H210 V330", OK, 3, dash="8 6", arrow=True))
c.add(text(510, 404, "para volver: ha-manager crm-command arm-ha", 16, 700, OK, FM, anchor="middle"))
c.add(Note(48, 500, 540, "freeze deja los servicios como están; ignore los saca del control de la HA para moverlos a mano.", title="freeze o ignore", kind="info"))
c.add(Note(612, 500, 540, "Mientras está desarmada, una falla real no se recupera sola. La ventana, lo más corta posible.", title="Ventana corta", kind="warn"))
save(c, "10-paso3.svg")
