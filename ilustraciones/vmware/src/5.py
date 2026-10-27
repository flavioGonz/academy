import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 5.svg: formatos de disco, OVA y Tools
c = Canvas(K(), "Tres formatos de disco y lo que cada uno arriesga")
c.add(NOLIG)
fmts = [("Thick lazy zeroed", "reserva todo al crear;", "pone en cero al primer uso", 1.0, 0.0, "info", "El espacio queda apartado: no te sorprende."),
        ("Thick eager zeroed", "reserva y pone en cero", "todo al crear (tarda más)", 1.0, 1.0, "info", "El que pide Fault Tolerance."),
        ("Thin", "crece a demanda,", "hasta su tamaño máximo", 0.35, 0.35, "warn", "Si llena el datastore, la VM se detiene.")]
for i, (t, l1, l2, res, zero, k, nota) in enumerate(fmts):
    x = 48 + i * 376
    c.add(panel(x, 124, 352, 300, t, k))
    c.add(text(x + 20, 182, l1, 16, 400, INK2, FB))
    c.add(text(x + 20, 206, l2, 16, 400, INK2, FB))
    c.add(text(x + 20, 252, "en el datastore", 14, 600, INK3, FM, ls=1))
    c.add(rect(x + 20, 266, 312, 46, WHITE, LINE2, rx=8))
    c.add(rect(x + 20, 266, 312 * res, 46, SOFT, BLUE, rx=8, sw=1.5))
    c.add(rect(x + 20, 266, max(14, 312 * 0.35), 46, BLUE, BLUE, rx=8, sw=0))
    if zero:
        c.add(rect(x + 20, 266, 312 * zero, 46, "none", CYAN, rx=8, sw=3, dash="6 4"))
    c.add(text(x + 20, 336, "datos de la VM", 14, 500, BLUE, FB))
    c.add(text(x + 332, 336, "reservado" if res == 1 else "libre para otros", 14, 500, INK3, FB, anchor="end"))
    sv, _ = wrap(x + 20, 376, nota, 312, 16, 600, WARN if k == "warn" else INK)
    c.add(sv)
c.add(panel(48, 446, 540, 160, "Appliance del fabricante (.ova)", "info"))
sv, _ = wrap(68, 506, "Entra por Deploy OVF Template, que crea la VM con su hardware. Copiar el .ova al datastore no lo instala.", 500, 16, 400, INK2)
c.add(sv)
c.add(panel(612, 446, 540, 160, "VMware Tools, siempre", "ok"))
c.add(bullet_list(632, 506, [("driver de balloon para la memoria", "ok"), ("snapshots con quiesce", "ok"), ("latido que mira HA", "ok")], 500, 16, 8)[0])
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso1: Tools y cuánto puede crecer
c = Canvas(K(1), "¿Tiene Tools y cuánto puede crecer su disco?")
c.add(NOLIG)
c.add(Step(48, 140, 1))
t = Terminal(48, 162, 560, [("$ vim-cmd vmsvc/get.guest 1 | grep -i tools", "#9FE3F7"), "  toolsRunningStatus = \"guestToolsRunning\"", "  toolsVersionStatus = \"guestToolsCurrent\""], title="SSH AL HOST · VMID 1")
c.add(t)
c.add(tag(328, 326, "Tools corriendo y al día", "ok"))
t2 = Terminal(48, 356, 560, [("$ ls -lh …/vm-prueba/*-flat.vmdk", "#9FE3F7"), "  100G  vm-prueba-flat.vmdk", ("$ du -h …/vm-prueba/*-flat.vmdk", "#9FE3F7"), "  18G   vm-prueba-flat.vmdk"], title="SSH AL HOST · VALORES DE EJEMPLO")
c.add(t2)
# barra
c.add(text(650, 186, "vm-prueba-flat.vmdk (thin)", 17, 600, INK, FM))
c.add(rect(650, 206, 500, 50, WHITE, LINE2, rx=10))
c.add(rect(650, 206, 90, 50, BLUE, BLUE, rx=10, sw=0))
c.add(rect(740, 206, 410, 50, WARN_BG, WARN, rx=10, sw=1.5, dash="6 4"))
c.add(text(660, 288, "du -h: 18G ocupados", 16, 600, BLUE, FM))
c.add(text(1150, 288, "puede crecer 82G más", 16, 600, WARN, FM, anchor="end"))
c.add(text(650, 316, "ls -lh: 100G provisionados", 16, 500, INK2, FM))
c.add(panel(650, 352, 502, 116, "Sumalo por datastore", "warn"))
sv, _ = wrap(670, 410, "Lo que todavía pueden crecer todas las VMs thin, contra el libre que muestra esxcli storage filesystem list.", 460, 16, 400, INK2)
c.add(sv)
c.add(Note(650, 492, 502, "Si la suma supera el libre, estás sobreasignado: vigilalo o pasá a thick lo crítico.", kind="info"))
save(c, "5-paso1.svg")
