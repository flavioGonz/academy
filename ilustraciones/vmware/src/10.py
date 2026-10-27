import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 10.svg: ciclo de Lifecycle Manager
c = Canvas(K(), "Lifecycle Manager en cuatro pasos, con backup antes")
c.add(NOLIG)
c.add(panel(48, 128, 1104, 86, None, "alert"))
c.add(icon(70, 152, "shield", ALERT, 1.3))
c.add(text(118, 164, "Antes de todo: backup", 20, 700, ALERT, FD))
c.add(text(118, 192, "del vCenter, de la configuración del host y de las VMs críticas · Compatibility Guide de la versión destino", 15, 400, INK2, FB))
pasos = [("Check Compliance", "compara el host con la imagen", "no cambia nada", "info"),
         ("Run Pre-check", "revisa que se pueda aplicar", "no cambia nada", "info"),
         ("Stage", "baja los paquetes al host", "todavía sin aplicar", "info"),
         ("Remediate", "modo mantenimiento, aplica", "y reinicia", "warn")]
for i, (t, l1, l2, k) in enumerate(pasos):
    x = 48 + i * 282
    c.add(panel(x, 250, 252, 190, None, k))
    c.add(badge(x + 36, 290, str(i + 1), WARN if k == "warn" else BLUE, 20, 18))
    c.add(text(x + 66, 297, t, 19, 600, INK, FD))
    c.add(text(x + 20, 350, l1, 15.5, 400, INK2, FB))
    c.add(text(x + 20, 376, l2, 15.5, 600 if i < 2 else 400, OK if i < 2 else INK2, FB))
    if i < 3:
        c.add(arrow((x + 254, 345), (x + 280, 345), "flow"))
c.add(text(332, 470, "Con el staging hecho, el host pasa menos tiempo en mantenimiento.", 16, 600, BLUE, FB))
c.add(Note(48, 500, 540, "vLCM vive dentro de vCenter: Cluster > Updates > Image. En vSphere 9 se retiran las baselines y queda el modelo de imágenes.", title="Dónde está", kind="info"))
c.add(Note(612, 500, 540, "Rollback de 8 a 7 solo si no se tocaron los bootbanks. Por eso el backup del arranque va primero.", title="Vuelta atrás", kind="warn"))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso1: host suelto con esxcli
c = Canvas(K(1), "Host suelto: el orden de los comandos con esxcli")
c.add(NOLIG)
c.add(Step(48, 140, 1))
seq = [("vmware -vl", "anotá la versión de partida", "info"),
       ("esxcli system maintenanceMode set -e true", "VMs apagadas o movidas antes", "warn"),
       ("esxcli software sources profile list -d …depot.zip", "qué perfiles trae el parche", "info"),
       ("esxcli software profile update -d … -p … --dry-run", "simula: no aplica nada", "ok"),
       ("esxcli software profile update -d … -p …  y  reboot", "solo en el host de laboratorio", "alert"),
       ("vmware -vl  ·  maintenanceMode set -e false", "verificá y salí de mantenimiento", "ok")]
for i, (cmd, s, k) in enumerate(seq):
    y = 168 + i * 72
    c.add(f'<circle cx="92" cy="{y + 24}" r="13" fill="{ {"info": BLUE, "warn": WARN, "ok": OK, "alert": ALERT}[k]}"/>')
    c.add(text(92, y + 29, str(i + 1), 14, 700, WHITE, FM, anchor="middle"))
    if i < 5:
        c.add(vline(92, y + 38, y + 82, LINE2, 2))
    c.add(code(124, y, 640, cmd, 14.5, h=46))
    c.add(text(788, y + 29, s, 16, 600 if k in ("ok", "alert", "warn") else 400, {"info": INK2, "warn": WARN, "ok": OK, "alert": ALERT}[k], FB))
c.add(text(48, 625, "Depot de ejemplo: /vmfs/volumes/datastore1/VMware-ESXi-8.0U3-depot.zip · perfil ESXi-8.0U3-standard", 15, 500, INK3, FM))
save(c, "10-paso1.svg")
