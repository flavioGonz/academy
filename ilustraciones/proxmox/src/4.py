import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 4.svg: lo que se elige al crear la VM
c = Canvas(K(), "Una VM bien armada: cuatro elecciones al crearla")
c.add(NOLIG)
w = Window(48, 122, 560, 330, "VM 100 · Hardware y Options", rows=[
    ("Processors · Type", "x86-64-v2-AES"), ("SCSI Controller", "VirtIO SCSI single"), ("Hard Disk (scsi0)", "iothread=1"),
    ("Network Device (net0)", "virtio, bridge=vmbr0"), ("QEMU Guest Agent", "Enabled"), ("CD/DVD (ide2)", "virtio-win.iso")], hl=None)
c.add(w)
cards = [
    (130, "1", "Disco en VirtIO SCSI single con IO Thread", "Es lo que la guía recomienda para rendimiento. IDE solo para sistemas muy viejos.", "ok"),
    (222, "2", "Placa de red VirtIO", "Paravirtual: el invitado sabe que es virtual y no emula una placa vieja.", "ok"),
    (314, "3", "Guest agent activado y adentro", "Apagado limpio y backups con el sistema de archivos congelado.", "ok"),
    (406, "4", "CPU host, solo si no vas a migrar", "Con migración en vivo, el modelo de la generación más vieja del clúster.", "warn"),
]
for y, n, t, d, kd in cards:
    c.add(badge(690, y + 14, n, CYAN if kd == "ok" else WARN))
    c.add(text(720, y + 20, t, 17, 700, INK, FB))
    svg, _ = wrap(720, y + 46, d, 430, 15, 400, INK2)
    c.add(svg)
# marcas sobre las filas de la ventana
for i, n in [(1, "1"), (2, "1"), (3, "2"), (4, "3"), (0, "4")]:
    c.add(badge(632, 52 + 122 + 18 + i * 38, n, CYAN if n != "4" else WARN, 13, 15))
c.add(Note(48, 494, 1104, "Los drivers no vienen en Windows: van desde el ISO virtio-win, en la versión que la wiki de Proxmox marca sin problemas conocidos (0.1.271 a septiembre de 2026), no la última a ciegas.", title="Windows", kind="info"))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso4: el agente responde
c = Canvas(K(4), "qm agent ping: el host le habla al agente de adentro")
c.add(NOLIG)
c.add(Step(48, 124, 4))
c.add(host(48, 124, 440, 300, "pve1 · host", "Proxmox VE"))
sv, h = codebox(68, 210, 400, ["# qm agent 100 ping", ("(sin salida: respondió)", "#7FE0B0"), "# qm agent 100 network-get-interfaces", ('"ip-address": "10.10.10.100"', "#7FE0B0")], 15, 28)
c.add(sv)
c.add(rect(712, 124, 440, 300, WHITE, BLUE, rx=18))
c.add(icon(730, 140, "laptop", BLUE, 1.15))
c.add(text(770, 162, "VM 100 · Debian", 20, 600, INK, FD))
c.add(rect(732, 210, 400, 70, OK_BG, OK, rx=12))
c.add(text(752, 240, "qemu-guest-agent", 18, 700, OK, FM))
c.add(text(752, 266, "servicio corriendo adentro", 15, 400, INK2, FB))
c.add(text(732, 330, "Lo instalaste en el paso 2:", 16, 500, INK3, FB))
c.add(code(732, 344, 400, "apt install qemu-guest-agent", 15))
c.add(path("M488 244 H704", BLUE, 4, arrow=True))
c.add(path("M712 268 H496", OK, 4, arrow=True))
c.add(pill(600, 226, "pedido", BLUE, size=15))
c.add(pill(600, 304, "respuesta", OK, size=15))
c.add(text(600, 350, "canal virtio-serial", 15, 500, INK3, FM, anchor="middle"))
c.add(Note(48, 452, 540, "QEMU guest agent is not running: falta instalar o arrancar el servicio adentro, o la VM no se apagó y prendió desde Proxmox después del qm set.", title="Si no responde", kind="warn"))
c.add(Note(612, 452, 540, "Con el agente, Proxmox ve las IP de la VM, la apaga limpia y congela el disco antes de un backup.", title="Para qué sirve", kind="ok"))
save(c, "4-paso4.svg")

# ---------------------------------------------------------------- 4-paso6: Windows con virtio-win
c = Canvas(K(6), "Windows: virtio-win como segundo CD y dos instaladores")
c.add(NOLIG)
c.add(Step(48, 124, 6))
c.add(text(80, 132, "Subí el ISO a local y montalo como segundo CD de la VM", 18, 600, INK, FB))
c.add(vmcard(48, 160, 340, "CD 1 · Windows", "instalador del sistema", "gray", ic="laptop"))
c.add(vmcard(48, 250, 340, "CD 2 · virtio-win", "drivers de Proxmox", "info", ic="laptop"))
c.add(path("M388 285 H470", BLUE, 3, arrow=True))
c.add(rect(480, 160, 672, 190, WHITE, LINE2, rx=16))
c.add(text(504, 196, "Adentro de Windows, desde el CD de virtio-win:", 17, 600, INK, FB))
c.add(badge(524, 240, "a", CYAN))
c.add(text(556, 247, "virtio-win-gt-x64", 19, 700, BLUE, FM))
c.add(text(840, 247, "los drivers", 16, 400, INK2, FB))
c.add(badge(524, 300, "b", CYAN))
c.add(text(556, 307, "virtio-win-guest-tools", 19, 700, BLUE, FM))
c.add(text(840, 307, "agente y servicios", 16, 400, INK2, FB))
c.add(rect(48, 376, 1104, 140, SOFT, LINE2, rx=16))
c.add(text(72, 408, "Qué versión", 17, 600, INK, FB))
c.add(tag(72, 450, "0.1.271 · sin problemas conocidos", "ok", 15, anchor="start"))
c.add(tag(440, 450, "0.1.285 · errores con Server 2025 y SQL", "alert", 15, anchor="start"))
c.add(tag(72, 494, "0.1.215 a 0.1.262 · eventos 129 Reset to device", "warn", 15, anchor="start"))
c.add(Note(48, 540, 1104, "La lista cambia: antes de instalar, mirá la página Windows VirtIO Drivers de la wiki de Proxmox. Los datos de arriba son a septiembre de 2026.", kind="info"))
save(c, "4-paso6.svg")
