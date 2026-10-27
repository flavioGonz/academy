"""Teoría lección 5: el arranque con systemd, del firmware a los servicios habilitados, y el journal."""
from _alnx import *

a = new(25, "Del botón de encendido a los servicios")
a.steps(["El firmware (BIOS o UEFI) inicia el hardware y lanza el cargador.",
         "GRUB carga el kernel y el initramfs en memoria.",
         "El kernel monta la raíz y arranca systemd: el PID 1.",
         "systemd alcanza los targets y arranca lo habilitado.",
         "journald guarda todo: journalctl -b es este arranque."], still=3)

stages = [("Firmware", "BIOS / UEFI"), ("GRUB", "cargador"), ("Kernel", "+ initramfs"), ("systemd", "PID 1")]
for i, (t, s) in enumerate(stages):
    x = 48 + i * 284
    a.add(a.box(x, 180, 250, 86, a.WHITE, a.LINE, rx=14))
    a.add(a.text(x + 125, 218, t, 21, a.INK, a.HEAD, 600, "middle"))
    a.add(a.text(x + 125, 246, s, 15, a.GREY, a.MONO, 500, "middle"))
    at(a, a.box(x, 180, 250, 86, a.INK if i == 3 else "#E5F0FB", a.BLUE, rx=14, sw=3)
       + a.text(x + 125, 218, t, 21, "#FFFFFF" if i == 3 else a.BLUE, a.HEAD, 700, "middle")
       + a.text(x + 125, 246, s, 15, "#9FC3E3" if i == 3 else a.BLUE, a.MONO, 600, "middle"), i * 20, 100, 1)
    if i < 3:
        a.add(a.arrow(f"M{x + 254} 223H{x + 280}", a.GREY, 3))

# targets
tg = [("local-fs.target", "discos montados", 420), ("network-online.target", "red lista", 720), ("multi-user.target", "listo para usar", 1020)]
a.add(line(a, "M1046 266V300H160V330", a.LINE, 3))
for k, (n, d, x) in enumerate(tg):
    xx = x - 280
    at(a, a.box(xx, 330, 270, 70, a.SLATE, None, rx=12) + mono(a, xx + 135, 360, n, 15, a.INK, 700, "middle")
       + a.text(xx + 135, 386, d, 15, a.GREY, a.SANS, 500, "middle"), 61 + k * 4, 100, 1)
svcs = [("ssh.service", 760), ("nftables.service", 950), ("cron.service", 1140)]
at(a, a.text(860, 432, "multi-user.target.wants/  (enable)", 15, a.GREY, a.MONO, 600, "middle"), 70, 100, 1)
for k, (s, x) in enumerate(svcs):
    at(a, chip(a, x - 70, 446, s, "ok", anchor="middle"), 72 + k * 2, 100, 1)

# journal
a.add(a.box(48, 490, 1104, 108, "#03213C", None, rx=12))
a.add(a.text(64, 512, "JOURNAL · journalctl -b", 13, "#7FA6C9", a.MONO, 500, extra='letter-spacing="1.5"'))
logs = [(41, "kernel: Linux version ...  · Command line: BOOT_IMAGE=/boot/vmlinuz ..."),
        (62, "systemd[1]: Reached target local-fs.target - Local File Systems."),
        (72, "systemd[1]: Started ssh.service - OpenBSD Secure Shell server.")]
for k, (t0, s) in enumerate(logs):
    at(a, mono(a, 64, 538 + k * 22, s, 15, T_OUT if k else T_COM, 500), t0, 100, 1)
at(a, a.box(48, 490, 1104, 108, "none", a.CYAN, rx=12, sw=3), 80, 100, 0)

caption(a, 630, [(0, 20, "Lo que pasa antes de GRUB depende del equipo: lo configurás en el firmware.", None),
                 (20, 40, "El initramfs trae lo justo para encontrar el disco raíz.", None),
                 (40, 60, "systemd es el primer proceso: todo lo demás cuelga de él.", None),
                 (60, 80, "Solo arranca solo lo que tiene enable: start no alcanza.", a.OK),
                 (80, 100, "journalctl -b -1 trae el arranque anterior: lo que pasó antes del corte.", a.OK)], still=3)
write(a, "5-t1.svg", "Del botón de encendido a los servicios",
      "Animación en cinco tiempos del arranque de un servidor Debian o Ubuntu. Arriba, cuatro cajas en fila: firmware (BIOS o UEFI), GRUB, kernel con initramfs y systemd como PID 1, que se encienden una tras otra. "
      "1: el firmware inicia el hardware y lanza el cargador. 2: GRUB carga el kernel y el initramfs. 3: el kernel monta la raíz y arranca systemd. "
      "4: debajo aparecen los targets local-fs, network-online y multi-user, y los servicios habilitados que cuelgan de multi-user.target.wants: ssh, nftables y cron. "
      "5: en la franja del journal aparecen líneas del kernel y de systemd, como Reached target local-fs.target y Started ssh.service, y se recuerda que journalctl -b -1 muestra el arranque anterior. El cuadro fijo muestra el tiempo 4.",
      pcts=(10, 30, 50, 70, 92))
