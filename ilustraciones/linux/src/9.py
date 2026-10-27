import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 9.svg: df dónde, du qué
c = new(None, "df dice dónde se llenó; du dice qué lo llenó")
svg, h = term(48, 124, 540, ["$ df -h", ("Filesystem  Size  Used Avail Use% Mounted on", T_COM),
                             ("/dev/sda2    31G   30G  1,0G  97% /", T_ERR), ("/dev/sdb1   492G  120G  347G  26% /srv/datos", T_OUT)],
            "1 · QUÉ SISTEMA DE ARCHIVOS", size=15, lh=28)
c.add(svg)
svg, h2 = term(612, 124, 540, ["$ sudo du -xh -d1 /var | sort -h | tail -3", ("1,1G   /var/lib", T_OUT), ("6,8G   /var/log", T_WARN), ("8,2G   /var", T_OUT)],
               "2 · QUÉ CARPETA (DE A UN NIVEL)", size=15, lh=28)
c.add(svg)
c.add(f'<path d="M588 {124 + h / 2}H612" stroke="{BLUE}" stroke-width="3" marker-end="url(#a-blue)"/>')
c.add(text(48, 124 + max(h, h2) + 40, "Sospechosos de siempre", 19, 600, INK, FD))
sus = [("/var/cache/apt", "sudo apt-get clean", "paquetes ya instalados"), ("/var/log/journal", "SystemMaxUse=500M", "el journal sin tope"),
       ("/var/log", "logrotate", "logs de texto sin rotar"), ("/tmp", "usar /var/tmp", "en 26.04 vive en RAM")]
y = 124 + max(h, h2) + 60
for i, (p, fix, d) in enumerate(sus):
    x = 48 + i * 282
    c.add(rect(x, y, 264, 140, WHITE, LINE2, rx=14))
    c.add(text(x + 18, y + 36, p, 18, 700, BLUE, FM))
    c.add(text(x + 18, y + 66, d, 16, 500, INK2, FB))
    c.add(code(x + 14, y + 84, 236, fix, 15, h=38))
c.add(Note(48, 512, 1104, "df -i: si los inodos están al 100 %, sobran archivos chicos aunque haya espacio libre.", kind="info"))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso2: bajar de a un nivel
c = new(2, "du de a un nivel, con -x para no cruzar a otro disco")
svg, h = term(48, 124, 560, ["$ sudo du -xh -d1 /var | sort -h | tail", ("180M   /var/cache", T_OUT), ("1,1G   /var/lib", T_OUT),
                             ("6,8G   /var/log", T_WARN), ("8,2G   /var", T_OUT)], "PRIMER NIVEL · EJEMPLO", size=16, lh=29)
c.add(svg)
svg, h2 = term(632, 124, 520, ["$ sudo du -xh -d1 /var/log | sort -h | tail", ("40M    /var/log/apt", T_OUT), ("210M   /var/log/installer", T_OUT),
                               ("6,5G   /var/log/journal", T_ERR), ("6,8G   /var/log", T_OUT)], "SEGUNDO NIVEL · EJEMPLO", size=16, lh=29)
c.add(svg)
c.add(f'<path d="M608 {124 + 32 + 4 + 3.6 * 29 - 5}H632" stroke="{WARN}" stroke-width="3" marker-end="url(#a-gray)"/>')
y = 124 + max(h, h2) + 30
c.add(box(48, y, 352, 170, "-x", ["No cruza a otros discos", "montados adentro, como", "/srv/datos: suma solo este."], kind="info"))
c.add(box(424, y, 352, 170, "-d1 y sort -h", ["Un nivel por vez, ordenado", "de menor a mayor: lo más", "grande queda al final."], kind="info"))
c.add(box(800, y, 352, 170, "Encontrado", ["El journal ocupa 6,5 GB:", "se mide con du -sh y se le", "pone tope en journald.conf.d."], kind="warn"))
save(c, "9-paso2.svg")

# ---------------------------------------------------------------- 9-paso4: fstab por UUID
c = new(4, "Un disco extra en fstab: UUID, nofail y validación")
svg, h = term(48, 124, 1104, ["$ lsblk -f", ("NAME   FSTYPE  UUID", T_COM), ("sdb1   ext4    el UUID de tu disco: anotalo tal cual", "#FFFFFF")], "TERMINAL · EJEMPLO", size=16, lh=29)
c.add(svg)
y = 124 + h + 34
fields = [("UUID=el-uuid-que-viste", "qué disco", 0, OK), ("/srv/datos", "dónde se monta", 1, BLUE), ("ext4", "tipo", 2, BLUE),
          ("defaults,nofail,x-systemd.device-timeout=5", "opciones", 3, WARN), ("0", "dump", 4, INK3), ("2", "orden de chequeo", 5, INK3)]
c.add(rect(48, y, 1104, 64, WHITE, LINE2, rx=12))
x = 64
pos = []
for s, lb, i, col in fields:
    w = len(s) * 15 * 0.6
    c.add(text(x, y + 40, s, 15, 700, col, FM))
    pos.append((x + w / 2, lb, col))
    x += w + 22
for k, (cx, lb, col) in enumerate(pos):
    ty = y + 104 + (k % 2) * 30
    c.add(callout(cx, y + 64, cx - 20 if k < 4 else (cx - 80 if k == 4 else cx + 30), ty, lb, {OK: "ok", BLUE: "info", WARN: "warn", INK3: "gray"}[col]))
yb = y + 170
c.add(box(48, yb, 352, 168, "UUID, nunca /dev/sdb1", ["Los nombres del kernel cambian", "según el orden en que aparecen", "los discos al arrancar."], kind="alert"))
c.add(box(424, yb, 352, 168, "nofail con timeout", ["Si el disco falta, arranca igual.", "Sin el timeout, systemd lo", "espera 90 segundos."], kind="warn"))
c.add(box(800, yb, 352, 168, "sudo findmnt -x", ["Valida fstab antes de reiniciar:", "un error puede dejar el equipo", "en modo emergencia."], kind="ok"))
save(c, "9-paso4.svg")
