import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 12.svg: el orden del diagnóstico
c = Canvas(K(), "Cuando algo anda mal: diagnóstico en orden")
c.add(NOLIG)
steps = [("Quórum", "pvecm status", "¿Quorate: Yes?"), ("Logs", "journalctl -b", "corosync y pve-cluster desde el arranque"),
         ("Locks", "grep '^lock:'", "¿una VM quedó trabada?"), ("Storage", "pvesm status", "¿todo active?"),
         ("Firewall", "pve-firewall", "status, si hay sospecha")]
for i, (t, cmd, q) in enumerate(steps):
    x = 48 + i * 224
    c.add(rect(x, 130, 204, 196, WHITE if i < 4 else GROUND, BLUE if i < 4 else LINE2, rx=16, dash=None if i < 4 else "7 6"))
    c.add(badge(x + 34, 166, str(i + 1), CYAN if i < 4 else INK3))
    c.add(text(x + 62, 173, t, 18, 700, INK, FB))
    c.add(rect(x + 14, 200, 176, 40, "#03213C", "#03213C", rx=8))
    c.add(text(x + 26, 226, cmd, 15, 500, "#D9E9F8", FM))
    svg, _ = wrap(x + 18, 272, q, 172, 15, 500, INK2)
    c.add(svg)
    if i < 4:
        c.add(path(f"M{x + 206} 228 H{x + 222}", INK3, 3, arrow=True))
c.add(text(48, 380, "Upgrade mayor de 8 a 9", 21, 600, INK, FD))
rules = [("Backup probado de todo", True), ("pve8to9 --full antes, durante y después", True), ("SSH con tmux o IPMI, nunca la consola de la GUI", True), ("Un nodo por vez, verificando antes de seguir", True)]
for i, (s, ok) in enumerate(rules):
    c.add(check(72 + (i % 2) * 560, 424 + (i // 2) * 52, s, ok, 17))
c.add(Note(48, 534, 1104, "En Proxmox VE 9, /etc/sysctl.conf ya no se lee: lo que estaba ahí se pierde en el próximo reinicio. Va en /etc/sysctl.d/.", title="La trampa silenciosa", kind="warn"))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso3: un lock
c = Canvas(K(3), "Un lock que quedó: mirá antes de destrabar")
c.add(NOLIG)
c.add(Step(48, 124, 3))
sv, h = codebox(80, 124, 560, ["# grep -l '^lock:' /etc/pve/qemu-server/*.conf", ("/etc/pve/qemu-server/100.conf", "#FFD38A"), "", "# grep '^lock:' /etc/pve/qemu-server/100.conf", ("lock: backup", "#FFD38A")], 15, 28, title="EJEMPLO")
c.add(sv)
c.add(rect(680, 124, 472, 200, WHITE, LINE2, rx=16))
c.add(text(704, 160, "Quién pone un lock", 18, 600, INK, FB))
for j, s in enumerate(["un backup en curso", "un snapshot", "una migración"]):
    c.add(f'<circle cx="{712}" cy="{194 + j * 36 - 5}" r="4.5" fill="{CYAN}"/>')
    c.add(text(728, 194 + j * 36, s, 17, 500, INK2, FB))
c.add(text(704, 306, "Si se corta la luz a mitad, queda puesto.", 15, 500, INK3, FB))
c.add(text(80, 372, "Antes de destrabar, confirmá:", 18, 600, INK, FB))
for i, s in enumerate(["no hay una tarea corriendo sobre la VM 100 (Tasks del nodo)", "no hay un backup ni una migración en curso"]):
    c.add(check(104, 414 + i * 50, s, True, 17))
c.add(path("M760 440 H812", OK, 4, arrow=True))
c.add(code(820, 418, 260, "qm unlock 100", 18, color="#7FE0B0", h=46))
c.add(Note(80, 530, 1072, "Destrabar con un backup corriendo puede dejar la VM o el backup a medias. El lock está para protegerte: sacalo solo cuando sabés por qué quedó.", kind="warn"))
save(c, "12-paso3.svg")

# ---------------------------------------------------------------- 12-paso5: sysctl.conf en PVE 9
c = Canvas(K(5), "De la 8 a la 9: /etc/sysctl.conf deja de leerse")
c.add(NOLIG)
c.add(Step(48, 124, 5))
c.add(rect(80, 140, 470, 250, ALERT_BG, ALERT, rx=16))
c.add(text(104, 178, "/etc/sysctl.conf", 21, 700, ALERT, FM))
c.add(text(104, 206, "en Proxmox VE 9: ignorado", 16, 600, INK2, FB))
sv, h = codebox(104, 226, 422, ["net.ipv4.ip_forward=1", "vm.swappiness=10"], 15, 28, title="AJUSTES DE EJEMPLO")
c.add(sv)
c.add(text(104, 368, "al reiniciar, vuelven al valor por defecto", 15, 600, ALERT, FB))
c.add(path("M556 265 H640", OK, 5, arrow=True))
c.add(pill(598, 246, "mover", OK, size=15))
c.add(rect(648, 140, 504, 250, OK_BG, OK, rx=16))
c.add(text(672, 178, "/etc/sysctl.d/", 21, 700, OK, FM))
c.add(text(672, 206, "un archivo por tema: NN-nombre.conf", 16, 600, INK2, FB))
sv, h = codebox(672, 226, 456, ["# /etc/sysctl.d/90-ies.conf", "net.ipv4.ip_forward=1", "vm.swappiness=10"], 15, 28)
c.add(sv)
c.add(text(80, 438, "Para ver qué hay en el viejo, sin comentarios ni líneas vacías:", 17, 600, INK, FB))
c.add(code(80, 454, 720, "cat /etc/sysctl.conf | grep -v '^#' | grep .", 16))
c.add(Note(80, 532, 1072, "Los valores de arriba son un ejemplo de formato, no una recomendación: mové los que encuentres en el host.", kind="info"))
save(c, "12-paso5.svg")
