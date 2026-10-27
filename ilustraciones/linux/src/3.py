import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 3.svg: update, upgrade, full-upgrade
c = new(None, "update, upgrade y full-upgrade no son lo mismo")
cols = [("apt update", "Baja la lista", ["Pregunta al repositorio qué", "versiones hay. No instala", "nada."], "info", "todos los días"),
        ("apt upgrade", "Instala lo nuevo", ["Actualiza paquetes sin", "quitar ninguno. Es lo de", "todas las semanas."], "ok", "con regularidad"),
        ("apt full-upgrade", "Puede quitar paquetes", ["Instala y quita lo que haga", "falta. Para el salto de", "versión mayor."], "warn", "planificado y con backup")]
for i, (cmd, t, ls, k, when) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 124, 352, 268, None, k))
    c.add(code(x + 20, 144, 312, cmd, 17, h=44))
    c.add(text(x + 20, 228, t, 20, 600, INK, FD))
    for j, s in enumerate(ls):
        c.add(text(x + 20, 260 + j * 24, s, 16, 400, INK2, FB))
    c.add(tag(x + 20, 368, when, k if k != "info" else "info", 15, mono=False, anchor="start"))
# repositorio
c.add(panel(48, 414, 540, 192, "La seguridad, automática", "ok"))
c.add(lines(72, 476, ["unattended-upgrades aplica solo seguridad,", "una vez por día. Ubuntu lo trae instalado;", "en Debian 13 se verifica y, si falta, se instala."], 16, 26))
c.add(text(72, 572, "Registro: /var/log/apt/history.log", 15, 600, BLUE, FM))
c.add(panel(612, 414, 540, 192, "El reinicio lo decidís vos", "warn"))
c.add(lines(636, 476, ["Automatic-Reboot viene en \"false\".", "Gateway o NVR desatendido: hora fija de", "madrugada. Servidor con gente de día:", "ventana acordada."], 16, 26))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso2: 20auto-upgrades
c = new(2, "Las automáticas, activas: los dos valores en \"1\"")
svg, h = term(48, 124, 620, ["$ sudo apt install unattended-upgrades", "$ sudo dpkg-reconfigure -plow unattended-upgrades",
                             "$ cat /etc/apt/apt.conf.d/20auto-upgrades"], "TERMINAL", size=15, lh=28)
c.add(svg)
fb, fh = fileb(48, 124 + h + 24, 620, "/etc/apt/apt.conf.d/20auto-upgrades",
               ["APT::Periodic::Update-Package-Lists \"1\";", "APT::Periodic::Unattended-Upgrade \"1\";"], size=16, lh=34, hl=(0, 1), hl_col=OK_BG)
c.add(fb)
yf = 124 + h + 24
c.add(callout(610, yf + 44 + 0.5 * 34, 720, yf + 30, "baja las listas cada día", "ok"))
c.add(callout(610, yf + 44 + 1.5 * 34, 720, yf + 100, "instala la seguridad cada día", "ok"))
c.add(Note(48, 470, 540, "dpkg-reconfigure pregunta si querés activarlas: con Sí escribe este archivo. En Ubuntu ya viene así.", kind="info"))
c.add(Note(612, 470, 540, "Si un valor está en \"0\", esa parte no corre: el equipo queda sin parches aunque el paquete esté instalado.", kind="warn"))
save(c, "3-paso2.svg")

# ---------------------------------------------------------------- 3-paso5: reinicio con hora
c = new(5, "Reinicio a hora fija, en un archivo propio")
fb, fh = fileb(48, 124, 640, "/etc/apt/apt.conf.d/52reinicio-ies",
               ["Unattended-Upgrade::Automatic-Reboot \"true\";", "Unattended-Upgrade::Automatic-Reboot-Time \"04:30\";"], size=16, lh=34)
c.add(fb)
svg, h = term(48, 124 + fh + 20, 640, ["$ ls /var/run/reboot-required 2>/dev/null", ("/var/run/reboot-required", "#FFFFFF"),
                                       "$ cat /var/run/reboot-required.pkgs", ("linux-image-... (el kernel nuevo)", "#FFFFFF")], "TERMINAL · EJEMPLO", size=15, lh=28)
c.add(svg)
c.add(text(48, 124 + fh + 20 + h + 34, "Si existe la marca, un paquete (kernel, libc) espera un reinicio para usarse.", 16, 500, INK2, FB))
c.add(panel(716, 124, 436, 220, "Gateway, NVR, equipo desatendido", "ok"))
c.add(lines(740, 186, ["Automatic-Reboot \"true\"", "Automatic-Reboot-Time \"04:30\""], 16, 28, INK, FM, 600))
c.add(lines(740, 260, ["Reinicia solo si hace falta, de", "madrugada, sin nadie usándolo."], 16, 26))
c.add(panel(716, 364, 436, 220, "Accesos, central IP, gente de día", "warn"))
c.add(lines(740, 426, ["Automatic-Reboot \"false\""], 16, 28, INK, FM, 600))
c.add(lines(740, 474, ["Reiniciás vos, en una ventana", "acordada con el cliente, mirando", "la marca reboot-required."], 16, 26))
save(c, "3-paso5.svg")
