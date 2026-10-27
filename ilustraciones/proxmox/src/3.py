import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 3.svg: LVM-thin o ZFS
c = Canvas(K(), "LVM-thin o ZFS: decidí con lo que tiene el servidor")
c.add(NOLIG)
cols = [
    (48, "LVM-thin", "local-lvm · instalar con ext4 o xfs", "info",
     [("Simple y rápido", "ok"), ("Snapshots y linked clones", "ok"), ("Ocupa solo lo escrito", "ok"), ("Sin integridad ni RAID propio", "warn")],
     "Va bien con RAID por hardware, SSD de consumo o poca RAM."),
    (612, "ZFS", "local-zfs · instalar con ZFS", "info",
     [("Detecta y corrige corrupción", "ok"), ("Compresión y snapshots", "ok"), ("RAID por software y replicación", "ok"), ("Pide RAM, ECC y discos directos", "warn")],
     "Va bien con HBA (o modo IT), SSD con PLP y RAM de sobra."),
]
for x, t, sub, kd, items, foot in cols:
    c.add(panel(x, 122, 540, 330, None, "info"))
    c.add(text(x + 24, 164, t, 26, 600, INK, FD))
    c.add(text(x + 24, 192, sub, 15, 500, INK3, FM))
    c.add(hline(x + 20, x + 520, 210))
    for j, (s, k) in enumerate(items):
        c.add(check(x + 42, 244 + j * 44, s, k == "ok", 17) if k == "ok" else
              f'<circle cx="{x + 42}" cy="{244 + j * 44}" r="18" fill="{WARN_BG}" stroke="{WARN}" stroke-width="2"/>'
              + text(x + 42, 250 + j * 44, "!", 18, 700, WARN, FD, anchor="middle") + text(x + 72, 250 + j * 44, s, 17, 500, INK, FB))
    svg, _ = wrap(x + 24, 424, foot, 490, 16, 600, BLUE)
    c.add(svg)
c.add(rect(48, 476, 1104, 74, ALERT_BG, ALERT, rx=14))
c.add(Mark(88, 513, False))
c.add(text(120, 506, "Nunca ZFS encima de una controladora RAID por hardware con caché", 19, 700, ALERT, FB))
c.add(text(120, 532, "ZFS necesita ver cada disco: con la RAID en el medio pierde lo que lo hace confiable.", 16, 400, INK2, FB))
c.add(Note(48, 570, 1104, "Es lo más caro de cambiar después: se elige en el instalador, antes de la primera VM.", kind="info"))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso1: pvesm status
c = Canvas(K(1), "pvesm status: qué almacenamientos hay y cuánto usan")
c.add(NOLIG)
c.add(Step(48, 124, 1))
sv, h = codebox(48, 124, 1104, ["# pvesm status",
                                "Name       Type     Status   Total       Used        Available   %",
                                ("local      dir      active   98497780    11584292    81863940    11.76%", "#9FD8F0"),
                                ("local-lvm  lvmthin  active   832888832   61264576    771624256   7.36%", "#7FE0B0")],
                16, 32, title="SALIDA DE EJEMPLO · TAMAÑOS EN KiB")
c.add(sv)
y0 = 124 + h + 30
c.add(rect(48, y0, 540, 124, WHITE, LINE2, rx=14))
c.add(text(72, y0 + 36, "local · dir", 19, 700, BLUE, FM))
svg, _ = wrap(72, y0 + 68, "Un directorio: guarda archivos. ISO, plantillas de contenedor y backups de vzdump en /var/lib/vz.", 490, 16, 400, INK2)
c.add(svg)
c.add(rect(612, y0, 540, 124, WHITE, LINE2, rx=14))
c.add(text(636, y0 + 36, "local-lvm · lvmthin", 19, 700, OK, FM))
svg, _ = wrap(636, y0 + 68, "El thin pool data: discos de VM y contenedores. Un disco de 32 GB con 3 GB escritos ocupa 3 GB.", 490, 16, 400, INK2)
c.add(svg)
c.add(text(48, y0 + 160, "En un host instalado con ZFS vas a ver local-zfs (zfspool) en lugar de local-lvm.", 16, 500, INK3, FB))
save(c, "3-paso1.svg")

# ---------------------------------------------------------------- 3-paso4: la cuenta del ARC
c = Canvas(K(4), "La cuenta del ARC: 2 GiB más 1 GiB por TiB de pool")
c.add(NOLIG)
c.add(Step(48, 124, 4))
c.add(text(80, 132, "Ejemplo: pool ZFS de 4 TiB", 19, 600, INK, FB))
bx = [("2 GiB", "base", SOFT, BLUE), ("+", None, None, None), ("4 GiB", "1 por TiB", SOFT, BLUE), ("=", None, None, None), ("6 GiB", "límite sugerido", OK_BG, OK)]
x = 48
for v, s, bg, fg in bx:
    if s is None:
        c.add(mid(x + 22, 238, v, 36, 600, INK3, FD))
        x += 44
        continue
    c.add(rect(x, 168, 320, 120, bg, fg, rx=16))
    c.add(mid(x + 160, 226, v, 34, 700, fg, FD))
    c.add(mid(x + 160, 262, s, 16, 500, INK2, FB))
    x += 336
c.add(text(48, 334, "En bytes, como lo pide el módulo: 6 × 1024³ = 6442450944", 17, 600, INK, FB))
sv, h = codebox(48, 352, 640, ["# cat /sys/module/zfs/parameters/zfs_arc_max", "6442450944",
                               "# cat /etc/modprobe.d/zfs.conf", ("options zfs zfs_arc_max=6442450944", "#7FE0B0")], 15, 28, title="LO QUE TENDRÍAS QUE VER CON ESE LÍMITE")
c.add(sv)
c.add(Note(720, 352, 432, "Desde la 8.1, el instalador lo deja en el 10 % de la RAM con tope de 16 GiB. Compará ese valor con tu cuenta.", title="Qué trae de fábrica", kind="info"))
c.add(Note(720, 490, 432, "Bajarlo en un servidor en producción hace que el disco rinda menos. Cambialo con cuidado.", kind="warn"))
save(c, "3-paso4.svg")
