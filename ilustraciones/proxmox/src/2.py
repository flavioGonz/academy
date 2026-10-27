import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 2.svg: placas, bond, bridge
c = Canvas(K(), "Placas, bond y bridge: la red del host en capas")
c.add(NOLIG)
X, W = 48, 640
# VMs arriba
for i, (t, s) in enumerate([("VM 100", "tag 10 · cámaras"), ("VM 101", "tag 20 · voz"), ("VM 102", "sin tag")]):
    c.add(vmcard(X + i * 216, 124, 200, t, s, "info"))
    c.add(path(f"M{X + i * 216 + 100} 194V226", BLUE, 3))
c.add(layer(X, 226, W, 70, "vmbr0 · switch virtual", "VLAN aware · bridge-vids 2-4094", fill=DEEP, stroke=DEEP, color=WHITE))
c.add(path(f"M{X + W / 2} 296V326", BLUE, 4))
c.add(layer(X, 326, W, 70, "bond0 · dos placas como una", "802.3ad (LACP) si el switch lo soporta", fill=SOFT, stroke=BLUE))
c.add(path(f"M{X + 160} 396V426", BLUE, 4))
c.add(path(f"M{X + 480} 396V426", BLUE, 4))
c.add(layer(X + 40, 426, 240, 56, "eno1", fill=WHITE, stroke=LINE2, mono=True))
c.add(layer(X + 360, 426, 240, 56, "eno2", fill=WHITE, stroke=LINE2, mono=True))
c.add(path(f"M{X + 160} 482V522", BLUE, 4))
c.add(path(f"M{X + 480} 482V522", BLUE, 4))
c.add(layer(X, 522, W, 70, "Switch · port-channel en trunk", "VLAN 10 y 20 permitidas", fill=WHITE, stroke=LINE2))
# lectura de abajo hacia arriba
c.add(text(X + W + 24, 510, "SE ARMA DE", 13, 600, INK3, FM, ls=1.5))
c.add(text(X + W + 24, 530, "ABAJO HACIA ARRIBA", 13, 600, INK3, FM, ls=1.5))
for i, (s, y) in enumerate([("placas físicas", 454), ("bond encima", 361), ("bridge encima", 261), ("tag en cada VM", 165)]):
    c.add(badge(X + W + 40, y, str(i + 1), CYAN, 15, 15))
    c.add(text(X + W + 64, y + 6, s, 17, 600, INK, FB))
c.add(Note(906, 124, 246, "Con VLAN aware, un solo vmbr0 lleva todas las VLAN. El tag va en la placa de cada VM.", title="Un bridge, muchas VLAN", kind="ok", size=15))
c.add(Note(906, 336, 246, "Sin VLAN aware: un bridge por VLAN (vmbr0v10, vmbr0v20). Funciona, pero se multiplica.", title="El modo viejo", kind="info", size=15))
c.add(Note(906, 522, 246, "balance-alb y balance-tlb no sirven con un bridge con VMs.", title="Bonds a evitar", kind="warn", size=15))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso1: tildar VLAN aware y aplicar
c = Canvas(K(1), "Tildá VLAN aware en vmbr0 y aplicá la configuración")
c.add(NOLIG)
c.add(Step(48, 124, 1))
w = Window(48, 124, 520, 330, "Edit: Linux Bridge", rows=[("Name", "vmbr0"), ("IPv4/CIDR", "10.10.10.2/24"), ("Gateway (IPv4)", "10.10.10.1"), ("Bridge ports", "eno1"), ("VLAN aware", "tildado")], hl=4, path="Node → System → Network → vmbr0")
c.add(w)
# flujo de archivos
c.add(rect(640, 140, 512, 92, WHITE, LINE2, rx=14))
c.add(text(660, 174, "La GUI escribe primero en", 17, 500, INK2, FB))
c.add(text(660, 206, "/etc/network/interfaces.new", 17, 600, BLUE, FM))
c.add(arrowline(896, 236, 896, 282, CYAN, 3))
c.add(rect(720, 282, 352, 48, CYAN, CYAN, rx=24))
c.add(mid(896, 313, "Apply Configuration", 18, 700, WHITE, FB))
c.add(arrowline(896, 334, 896, 378, CYAN, 3))
c.add(rect(640, 378, 512, 76, OK_BG, OK, rx=14))
c.add(text(660, 410, "Recién ahí pasa a", 17, 500, INK2, FB))
c.add(text(660, 438, "/etc/network/interfaces", 17, 600, OK, FM))
c.add(Note(48, 486, 520, "Editado a mano, se aplica con ifreload -a. Así, un error a medio aplicar no te deja el nodo sin red.", title="Por qué en dos tiempos", kind="info"))
c.add(Note(640, 486, 512, "Si la IP de gestión pasa a una VLAN tagueada, al aplicar desde lejos se corta. Hacelo con consola local o IPMI.", title="Ojo con la gestión", kind="warn"))
save(c, "2-paso1.svg")

# ---------------------------------------------------------------- 2-paso4: bridge vlan show
c = Canvas(K(4), "bridge vlan show: qué VLAN lleva cada puerto")
c.add(NOLIG)
c.add(Step(48, 124, 4))
sv, h = codebox(48, 124, 560, ["# bridge vlan show", "port        vlan-id", "eno1        1 PVID Egress Untagged",
                               "            2-4094", "vmbr0       1 PVID Egress Untagged",
                               ("tap100i0    10 PVID Egress Untagged", "#7FE0B0")], 16, 30, title="SALIDA DE EJEMPLO · VM 100 CON TAG 10")
c.add(sv)
c.add(text(48, 124 + h + 32, "tap100i0 es la placa net0 de la VM 100: tap<VMID>i<placa>.", 16, 500, INK2, FB))
# lectura
yy = 140
for t, d, kd in [("eno1 · 2-4094", "la placa física lleva todas las VLAN etiquetadas hacia el switch (trunk).", "info"),
                 ("tap100i0 · 10 PVID", "lo que sale de la VM entra a la VLAN 10; la VM no ve tags.", "ok"),
                 ("Egress Untagged", "al entregarle a la VM, el bridge saca la etiqueta.", "info")]:
    c.add(rect(640, yy, 512, 104, WHITE, LINE2, rx=14))
    c.add(text(660, yy + 34, t, 17, 700, OK if kd == "ok" else BLUE, FM))
    svg, _ = wrap(660, yy + 64, d, 470, 16, 400, INK2)
    c.add(svg)
    yy += 120
c.add(Note(48, 124 + h + 64, 560, "Si tap100i0 no aparece, la VM está apagada. Si aparece con 1 en vez de 10, el tag no quedó en la placa.", title="Qué buscar", kind="warn"))
save(c, "2-paso4.svg")
