import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 7.svg: dónde vive cada llave
c = new(None, "La llave privada nunca sale de tu notebook")
c.add(panel(48, 124, 470, 300, "Tu notebook", "info", sub="tecnico@notebook-2026"))
c.add(rect(72, 200, 422, 92, ALERT_BG, ALERT, rx=12))
c.add(icon(88, 226, "key", ALERT, 1.5))
c.add(text(134, 236, "~/.ssh/id_ed25519", 18, 700, ALERT, FM))
c.add(text(134, 264, "privada · 600 · no se copia nunca", 15, 600, INK2, FB))
c.add(rect(72, 308, 422, 92, OK_BG, OK, rx=12))
c.add(icon(88, 334, "key", OK, 1.5))
c.add(text(134, 344, "~/.ssh/id_ed25519.pub", 18, 700, OK, FM))
c.add(text(134, 372, "pública · se puede copiar", 15, 600, INK2, FB))
c.add(panel(682, 124, 470, 300, "Servidor 192.168.88.50", "info", sub="usuario tecnico"))
c.add(rect(706, 200, 422, 92, OK_BG, OK, rx=12))
c.add(text(726, 236, "~/.ssh/authorized_keys", 18, 700, OK, FM))
c.add(text(726, 264, "copia de la pública · 600", 15, 600, INK2, FB))
c.add(rect(706, 308, 422, 92, WHITE, LINE2, rx=12))
c.add(text(726, 344, "~/.ssh", 18, 700, INK, FM))
c.add(text(726, 372, "carpeta con permisos 700", 15, 600, INK2, FB))
c.add(arrow((494, 354), (706, 246), "ok", label="ssh-copy-id"))
# orden seguro
c.add(text(48, 470, "El orden que no te deja afuera", 19, 600, INK, FD))
sv, xs = flow(48, 490, ["ssh-keygen", "ssh-copy-id", "entrar con llave", "apagar clave", "probar en otra"], w=192, h=72, gap=36,
              kinds=["info", "info", "ok", "warn", "ok"], size=16,
              sub=["-t ed25519", "a tu usuario", "sin pedir clave", "sshd_config.d", "terminal"])
c.add(sv)
c.add(text(48, 600, "La sesión que funciona no se cierra hasta que una nueva entra con la llave.", 17, 600, ALERT, FB))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso3: snippet de acceso y sshd -T
c = new(3, "Contraseña apagada en un archivo propio, y verificada")
fb, fh = fileb(48, 124, 560, "/etc/ssh/sshd_config.d/10-ies-acceso.conf",
               ["PasswordAuthentication no", "KbdInteractiveAuthentication no", "PermitRootLogin no"], size=18, lh=38)
c.add(fb)
svg, h = term(48, 124 + fh + 24, 560, ["$ sudo sshd -t && sudo systemctl reload ssh",
                                       "$ sudo sshd -T | grep -Ei \"passwordauth|permitroot\"",
                                       ("permitrootlogin no", T_OK), ("passwordauthentication no", T_OK)], "TERMINAL · SESIÓN ABIERTA", size=15, lh=28)
c.add(svg)
items = [("PasswordAuthentication no", "nadie entra con contraseña"), ("KbdInteractiveAuthentication no", "cierra la otra puerta de clave"),
         ("PermitRootLogin no", "root no entra por SSH")]
for i, (k, d) in enumerate(items):
    y = 124 + i * 96
    c.add(rect(640, y, 512, 80, WHITE, LINE2, rx=12))
    c.add(text(660, y + 32, k, 16, 700, BLUE, FM))
    c.add(text(660, y + 60, d, 16, 500, INK2, FB))
c.add(Note(640, 420, 512, "sshd -T muestra el valor que quedó en uso. Si dice yes, otro snippet con número más bajo lo está fijando antes.", kind="warn"))
save(c, "7-paso3.svg")

# ---------------------------------------------------------------- 7-paso4: probar desde otra terminal
c = new(4, "Probá desde otra terminal, con la primera abierta")
svg, h = term(48, 124, 520, ["$ ssh tecnico@192.168.88.50", ("tecnico@servidor:~$", T_OK), ("(abierta: tu salida de emergencia)", T_COM)], "TERMINAL A · LA QUE FUNCIONA", size=16, lh=30)
c.add(svg)
svg2, h2 = term(632, 124, 520, ["$ ssh -o PubkeyAuthentication=no \\", ("    tecnico@192.168.88.50", T_CMD),
                                ("tecnico@192.168.88.50: Permission denied", T_ERR), ("(publickey).", T_ERR),
                                "$ ssh tecnico@192.168.88.50", ("tecnico@servidor:~$", T_OK)], "TERMINAL B · NUEVA", size=16, lh=30)
c.add(svg2)
c.add(box(632, 124 + h2 + 24, 520, 130, "Las dos cosas que querés ver", ["Sin llave, Permission denied (publickey).", "Con llave, entra sin pedir la clave del servidor."], kind="ok"))
c.add(box(48, 124 + h + 24, 520, 160, "Si B no entra con la llave", ["Desde A: borrá el snippet, sshd -t y reload.", "Si ya cerraste A, la salida es la consola", "de la VM o del hipervisor."], kind="alert"))
save(c, "7-paso4.svg")
