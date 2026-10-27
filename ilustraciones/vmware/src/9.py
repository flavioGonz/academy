import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 9.svg: vMotion, HA y DRS
c = Canvas(K(), "vMotion, HA y DRS: qué hace cada uno")
c.add(NOLIG)
cols = [("vMotion", "mueve una VM encendida a otro host", "info"),
        ("HA", "reinicia en otro host las VMs de un host caído", "warn"),
        ("DRS", "reparte la carga de CPU y memoria", "info")]
rows = [("¿Corta el servicio?", ["no: copia memoria y estado en vivo", "sí: minutos, lo que tarda en arrancar", "no: usa vMotion para mover"]),
        ("¿Necesita vCenter?", ["sí, para lanzarla", "no para actuar: anda con vCenter caído", "sí, siempre"]),
        ("¿Qué pide?", ["almacenamiento compartido y vmk de vMotion", "capacidad libre en los otros hosts", "empezar en manual o parcial"])]
x0, cw = 300, 284
for i, (t, s, k) in enumerate(cols):
    x = x0 + i * cw
    c.add(panel(x, 124, cw - 16, 96, None, k))
    c.add(text(x + 20, 162, t, 22, 700, WARN if k == "warn" else BLUE, FD))
    sv, _ = wrap(x + 20, 190, s, cw - 56, 15, 400, INK2)
    c.add(sv)
for r, (name, vals) in enumerate(rows):
    y = 244 + r * 100
    c.add(rect(48, y, 1104, 88, WHITE, LINE2, rx=14))
    c.add(text(68, y + 50, name, 17, 600, INK, FB))
    for i, v in enumerate(vals):
        x = x0 + i * cw
        col = OK if v.startswith("no") and r == 0 else (ALERT if v.startswith("sí: minutos") else INK2)
        sv, _ = wrap(x + 20, y + 38, v, cw - 50, 16, 600 if col != INK2 else 400, col)
        c.add(sv)
c.add(Note(48, 556, 540, "Crear el clúster es libre. Activar HA o DRS depende de la licencia del cliente.", title="Licencia", kind="info"))
c.add(Note(612, 556, 540, "Al cliente: \"HA reinicia en otro host\". Nunca \"no se cae\".", title="Cómo decirlo", kind="warn"))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso3: Change compute resource only
c = Canvas(K(3), "Change compute resource only: cambia el host, no el disco")
c.add(NOLIG)
c.add(Step(48, 140, 3))
for i, (x, t) in enumerate([(80, "esxi-lab01"), (700, "esxi-lab02")]):
    c.add(host(x, 170, 420, 210, t, "Cluster-Lab"))
    c.add(rect(x + 20, 312, 180, 46, "#0B3A66", WARN, rx=10))
    c.add(text(x + 110, 341, "vmk vMotion", 15, 600, WHITE, FM, anchor="middle"))
c.add(vm(110, 240, 230, 58, "vm-prueba", "encendida", dark=True))
c.add(f'<rect x="730" y="240" width="230" height="58" rx="12" fill="none" stroke="{CYAN}" stroke-width="2" stroke-dasharray="7 6"/>')
c.add(text(845, 275, "destino", 16, 600, CYAN, FM, anchor="middle"))
c.add(arrow((342, 269), (726, 269), "flow", label="memoria y estado", label_dy=-12))
c.add(Cable((290, 335), (720, 335), "logical", label="red de vMotion, VLAN propia", arrow=False, label_dy=6))
c.add(cyl(420, 430, 360, 120, "datastore compartido", "el disco no se mueve"))
c.add(Cable((290, 380), (470, 440), "data"))
c.add(Cable((910, 380), (730, 440), "data"))
c.add(Note(48, 430, 340, "Los dos hosts tienen que ver el mismo datastore.", kind="info"))
c.add(Note(812, 430, 340, "Si la migración falla, la VM vuelve sola a su host de origen.", kind="ok"))
c.add(text(48, 630, "Migrate > Change compute resource only > destino: el otro host.", 17, 600, BLUE, FM))
save(c, "9-paso3.svg")

# ---------------------------------------------------------------- 9-paso4: ping continuo durante el vMotion
c = Canvas(K(4), "Ping continuo mientras migra: contá los perdidos")
c.add(NOLIG)
c.add(Step(48, 140, 4))
c.add(code(80, 122, 360, "ping -t 192.168.88.50"))
t = Terminal(48, 182, 620, ["Respuesta desde 192.168.88.50: bytes=32 tiempo<1m", "Respuesta desde 192.168.88.50: bytes=32 tiempo<1m", ("Respuesta desde 192.168.88.50: bytes=32 tiempo=3ms", "#FFD27A"), "Respuesta desde 192.168.88.50: bytes=32 tiempo<1m", "Respuesta desde 192.168.88.50: bytes=32 tiempo<1m"], title="NOTEBOOK · SALIDA DE EJEMPLO")
c.add(t)
c.add(text(690, 290, "durante el cambio de host", 16, 600, WARN, FB))
# línea de tiempo
c.add(text(48, 410, "Línea de tiempo de la VM", 18, 600, INK, FD))
c.add(rect(48, 430, 1104, 40, OK_BG, OK, rx=10))
c.add(rect(640, 430, 26, 40, WARN, WARN, rx=4))
c.add(text(68, 456, "sigue respondiendo en esxi-lab01", 15, 600, OK, FB))
c.add(text(1132, 456, "sigue en esxi-lab02", 15, 600, OK, FB, anchor="end"))
c.add(text(653, 500, "cambio de host: un instante", 15, 600, WARN, FB, anchor="middle"))
c.add(Note(48, 530, 540, "Anotá cuántos pings se perdieron (cero o casi) y el tiempo de la migración en Monitor > Tasks (paso 5).", kind="info"))
c.add(Note(612, 530, 540, "Compará con HA: ahí la VM se reinicia y el ping se corta minutos.", kind="warn"))
save(c, "9-paso4.svg")
