import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 7.svg: modos de transporte de VADP
c = Canvas(K(), "Por dónde viaja el backup: NBD, HotAdd o SAN")
c.add(NOLIG)
c.add(host(48, 124, 560, 300, "Host ESXi", "con la VM a respaldar"))
c.add(vm(72, 196, 220, 64, "srv-video", "VM a respaldar", dark=True))
c.add(rect(420, 140, 164, 46, "#0B3A66", "#4E7396", rx=10))
c.add(text(502, 169, "vmk0 gestión", 15, 600, WHITE, FM, anchor="middle"))
c.add(vm(340, 210, 244, 64, "Proxy virtual", "monta el disco", dark=True))
c.add(cyl(300, 300, 284, 104, "datastore (LUN)", "disco de srv-video"))
# servidor de backup y proxy físico
c.add(Server(700, 140, "Repositorio", "servidor de backup", w=260))
c.add(Server(700, 330, "Proxy físico", "ve la LUN en la SAN", w=260))
# caminos
c.add(arrow((584, 160), (698, 160), "flow", label="NBD", label_dy=-14))
c.add(arrow((584, 242), (698, 206), "ok", label="HotAdd", label_at=0.5, label_dy=24))
c.add(arrow((584, 370), (698, 372), "flow", label="SAN", label_dy=-14))
c.add(arrow((830, 330), (830, 226), "flow"))
rows = [("NBD", "el más simple; en 1 GbE puede ir lento (10 a 20 MB/s según una guía vieja de Veeam)", "info"),
        ("HotAdd", "un proxy virtual en el mismo host monta el disco; no anda con discos IDE", "ok"),
        ("SAN", "un proxy físico lee la LUN directo, sin pasar por el host", "info")]
for i, (t, s, k) in enumerate(rows):
    y = 446 + i * 50
    c.add(tag(48, y + 26, t, "ok" if k == "ok" else "info", anchor="start"))
    c.add(text(160, y + 26, s, 16, 400, INK2, FB))
c.add(Note(990, 124, 162, "Todos usan la API de vSphere (VADP).", kind="info", size=15))
c.add(Note(990, 286, 162, "ESXi gratuito: sin VADP. Solo agente adentro de la VM.", kind="alert", size=15))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso1: red aislada para restaurar
c = Canvas(K(1), "Un port group sin uplinks para restaurar sin riesgo")
c.add(NOLIG)
c.add(Step(48, 140, 1))
c.add(host(48, 168, 1104, 330, "Host ESXi", None))
# producción
c.add(rect(72, 214, 500, 260, "#0B3A66", "#4E7396", rx=14))
c.add(text(92, 246, "Producción", 18, 600, WHITE, FD))
c.add(vm(92, 266, 250, 60, "srv-prueba", "IP 192.168.88.50", dark=True))
c.add(rect(92, 344, 460, 44, "#0E4A80", CYAN, rx=10))
c.add(text(322, 372, "vSwitch1 · VM-VLAN20", 15, 700, WHITE, FM, anchor="middle"))
c.add(nicport(150, 416, "vmnic2"))
c.add(nicport(350, 416, "vmnic3"))
c.add(f'<path d="M198 388V416M398 388V416M217 326V344" stroke="{CYAN}" stroke-width="3"/>')
c.add(Cable((198, 456), (198, 540), "data"))
c.add(Cable((398, 456), (398, 540), "data"))
c.add(text(214, 560, "a la red del cliente", 15, 500, INK3, FB))
# aislado
c.add(rect(620, 214, 508, 260, "#0B3A66", OK, rx=14, sw=2.5))
c.add(text(640, 246, "Aislado", 18, 600, WHITE, FD))
c.add(vm(640, 266, 300, 60, "srv-prueba-restore", "misma IP, otro nombre", dark=True))
c.add(rect(640, 344, 468, 44, "#0E4A80", OK, rx=10))
c.add(text(874, 372, "vSwitch-Aislado · Restore-Aislado", 15, 700, WHITE, FM, anchor="middle"))
c.add(f'<path d="M790 326V344" stroke="{OK}" stroke-width="3"/>')
c.add(rect(700, 410, 348, 44, "none", "#4E7396", rx=10, dash="6 5"))
c.add(text(874, 438, "sin uplinks: no sale del host", 15, 600, "#9FE3F7", FM, anchor="middle"))
c.add(Mark(1110, 432, True))
c.add(code(612, 520, 540, "esxcli network vswitch standard add -v vSwitch-Aislado", 14))
c.add(code(612, 568, 540, "… portgroup add -p Restore-Aislado -v vSwitch-Aislado", 14))
c.add(Note(48, 584, 540, "Restaurada con la misma IP que el original: aislada, no choca.", kind="ok", size=15))
save(c, "7-paso1.svg")

# ---------------------------------------------------------------- 7-paso4: la ficha de la prueba
c = Canvas(K(4), "Anotá lo que vas a necesitar el día del problema")
c.add(NOLIG)
c.add(Step(48, 140, 4))
c.add(rect(48, 164, 640, 400, WHITE, LINE2, rx=18))
c.add(text(72, 202, "PRUEBA DE RESTAURACIÓN", 14, 600, INK3, FM, ls=2))
rows = [("VM restaurada", "srv-prueba-restore"), ("Tiempo total", "__ h __ min"), ("Modo de transporte", "NBD · HotAdd · SAN"),
        ("Tamaño", "___ GB"), ("Datos y servicios", "verificados sí / no"), ("Snapshots colgados", "ninguno en el original")]
for i, (k, v) in enumerate(rows):
    y = 222 + i * 50
    c.add(text(72, y + 26, k, 17, 600, INK, FB))
    c.add(rect(330, y, 336, 40, GROUND, LINE2, rx=8))
    c.add(text(346, y + 26, v, 15, 500, INK2, FM))
c.add(text(72, 548, "Valores a completar con tu prueba; el modo sale del log del job.", 15, 400, INK3, FB))
c.add(panel(720, 164, 432, 230, "Regla 3-2-1", "info"))
for i, (n, s) in enumerate([("3", "copias de los datos"), ("2", "medios distintos"), ("1", "fuera del sitio")]):
    c.add(badge(760, 236 + i * 52, n, BLUE, 18, 18))
    c.add(text(792, 242 + i * 52, s, 17, 500, INK, FB))
c.add(Note(720, 414, 432, "Con el tiempo anotado sabés cuánto tarda volver el día que se rompe algo, y lo podés decir al cliente.", title="Para qué sirve el tiempo", kind="ok"))
save(c, "7-paso4.svg")
