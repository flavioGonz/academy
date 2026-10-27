import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 11.svg: el ciclo
c = new(None, "Un backup existe cuando restauraste un archivo")
cards = [("1", "Copiar", ["tar czf para /etc", "rsync para datos", "dump para bases"], "info"),
         ("2", "A otro lugar", ["otro disco u otro", "servidor: la copia no", "vive con el original"], "info"),
         ("3", "Programar", ["timer 02:30 con", "Persistent=true,", "o una línea de cron"], "info"),
         ("4", "Restaurar", ["un archivo a /tmp", "y diff contra el", "original: recién ahí"], "ok")]
for i, (n, t, ls, k) in enumerate(cards):
    x = 48 + i * 282
    c.add(panel(x, 128, 250, 230, None, k))
    c.add(badge(x + 34, 168, n, OK if k == "ok" else CYAN))
    c.add(text(x + 62, 175, t, 21, 600, INK, FD))
    c.add(lines(x + 22, 222, ls, 16, 28))
    if i < 3:
        c.add(f'<path d="M{x + 254} 243H{x + 276}" stroke="{BLUE}" stroke-width="3" marker-end="url(#a-blue)"/>')
c.add(f'<path d="M{48 + 3 * 282 + 125} 358V392H{48 + 125}V362" fill="none" stroke="{OK}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-ok)"/>')
c.add(text(600, 418, "si la restauración falla, el backup no existía: se corrige y se vuelve a probar", 16, 600, OK, FB, anchor="middle"))
svg, h = term(48, 452, 640, ["$ ls -lh /srv/backup", ("srv1-etc-2026-10-26.tar.gz", T_OUT), ("srv1-etc-2026-10-27.tar.gz", T_OUT)], "TERMINAL · EJEMPLO", size=15, lh=27)
c.add(svg)
c.add(Note(712, 452, 440, "Falcot Corp, en el Debian Handbook, guarda el servidor de backup en otra sala, por si hay un incendio.", kind="info"))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso2: servicio y timer
c = new(2, "Un timer son dos archivos: qué hacer y cuándo")
fb1, h1 = fileb(48, 124, 540, "/etc/systemd/system/backup-etc.service",
                ["[Unit]", "Description=Backup de /etc", "", "[Service]", "Type=oneshot", "ExecStart=/usr/local/bin/backup-etc.sh"], size=16, lh=30, hl=(4, 5))
c.add(fb1)
fb2, h2 = fileb(612, 124, 540, "/etc/systemd/system/backup-etc.timer",
                ["[Unit]", "Description=Backup diario de /etc", "", "[Timer]", "OnCalendar=*-*-* 02:30:00", "Persistent=true",
                 "RandomizedDelaySec=15min", "", "[Install]", "WantedBy=timers.target"], size=16, lh=30, hl=(4, 5, 6, 9))
c.add(fb2)
c.add(text(48, 124 + h1 + 36, "QUÉ", 15, 700, INK3, FM, ls=2))
c.add(lines(48, 124 + h1 + 66, ["oneshot: corre una vez y termina.", "ExecStart: el script de backup."], 16, 26))
y = 124 + h1 + 130
c.add(box(48, y, 540, 150, "Se habilita el timer", ["sudo systemctl enable backup-etc.timer", "systemctl list-timers | grep backup", "journalctl -u backup-etc.service"], kind="ok", mono=True, size=15, lh=28))
sv, _ = bullet_list(612, 124 + h2 + 40, [("OnCalendar: a las 02:30 todos los días", "info"), ("Persistent=true: si estaba apagado, corre al arrancar", "ok"),
                                         ("RandomizedDelaySec: hasta 15 min de demora al azar", "info"), ("WantedBy=timers.target: se engancha al habilitarlo", "info")], 540, 16, 8)
c.add(sv)
save(c, "11-paso2.svg")

# ---------------------------------------------------------------- 11-paso3: restaurar y comparar
c = new(3, "La prueba que importa: restaurar a /tmp y comparar")
svg, h = term(48, 124, 1104, ["$ sudo tar xzf /srv/backup/srv1-etc-2026-10-27.tar.gz -C /tmp etc/hostname",
                              "$ diff /tmp/etc/hostname /etc/hostname && echo \"restaurado OK\"", ("restaurado OK", T_OK)], "TERMINAL · EJEMPLO", size=16, lh=30)
c.add(svg)
y = 124 + h + 40
c.add(rect(48, y, 300, 110, SOFT, CYAN, rx=14))
c.add(text(68, y + 40, "srv1-etc-...tar.gz", 17, 700, BLUE, FM))
c.add(text(68, y + 70, "en /srv/backup", 15, 500, INK3, FB))
c.add(rect(450, y, 300, 110, WHITE, OK, rx=14))
c.add(text(470, y + 40, "/tmp/etc/hostname", 17, 700, OK, FM))
c.add(text(470, y + 70, "lo restaurado, aparte", 15, 500, INK3, FB))
c.add(rect(852, y, 300, 110, WHITE, LINE2, rx=14))
c.add(text(872, y + 40, "/etc/hostname", 17, 700, INK, FM))
c.add(text(872, y + 70, "el original, sin tocar", 15, 500, INK3, FB))
c.add(arrow((348, y + 55), (450, y + 55), "flow", label="-C /tmp"))
c.add(arrow((750, y + 55), (852, y + 55), "ok", label="diff"))
c.add(Note(48, y + 140, 540, "Listar con tar -tzvf no prueba que se pueda restaurar: lo prueba sacar un archivo y compararlo.", kind="info"))
c.add(Note(612, y + 140, 540, "Restaurar sobre / sobrescribe lo actual. La prueba se hace siempre a otra carpeta.", kind="warn"))
save(c, "11-paso3.svg")
