import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 4.svg: el método
c = new(None, "Copia, archivo propio, validación y recién ahí reload")
steps = [("1", "Copia", "sshd_config.original", "chmod a-w: nadie la pisa"),
         ("2", "Cambio en .d", "sshd_config.d/", "en 10-ies.conf: el original queda intacto"),
         ("3", "Validación", "sudo sshd -t", "sin salida = está bien"),
         ("4", "Recarga", "systemctl reload ssh", "con otra sesión abierta")]
for i, (n, t, cmd, d) in enumerate(steps):
    x = 48 + i * 282
    c.add(panel(x, 128, 250, 190, None, "ok" if i == 3 else "info"))
    c.add(badge(x + 34, 166, n, OK if i == 3 else CYAN))
    c.add(text(x + 62, 173, t, 21, 600, INK, FD))
    c.add(text(x + 20, 226, cmd, 15, 600, BLUE, FM))
    svg, _ = wrap(x + 20, 266, d, 214, 16, 400, INK2)
    c.add(svg)
    if i < 3:
        c.add(f'<path d="M{x + 254} 223H{x + 276}" stroke="{BLUE}" stroke-width="3" marker-end="url(#a-blue)"/>')
# vuelta por error
c.add(f'<path d="M{48 + 2 * 282 + 125} 318V350H{48 + 282 + 125}V326" fill="none" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
c.add(text(48 + 282 + 160, 372, "error: te dice archivo y línea, corregís y volvés a validar", 15, 600, ALERT, FB))
# validadores
c.add(text(48, 424, "Cada servicio trae su validador", 19, 600, INK, FD))
c.add(Table(48, 440, ["Qué cambiaste", "Validá con"], [["SSH", "sudo sshd -t"], ["Red en Ubuntu (netplan)", "sudo netplan generate"],
            ["Discos (/etc/fstab)", "sudo findmnt -x"], ["sudo (sudoers)", "sudo visudo -c"], ["nginx", "sudo nginx -t"]],
            [300, 260], row_h=34, mono_cols=(1,)))
c.add(Note(660, 440, 492, "Tu cambio va en un archivo propio del directorio .d: cuando el paquete se actualiza, no te lo pisa ni te pregunta qué hacer.", title="Por qué un archivo .d", kind="info"))
c.add(Note(660, 568, 492, "Un error en sshd_config con SSH como único acceso te deja afuera.", kind="warn"))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso2: snippets existentes y orden
c = new(2, "Mirá qué snippets hay antes de sumar el tuyo")
svg, h = term(48, 124, 640, ["$ ls -l /etc/ssh/sshd_config.d/",
                             ("-rw-r--r-- 1 root root  32 10-ies.conf", "#FFFFFF"),
                             ("-rw-r--r-- 1 root root  27 50-cloud-init.conf", "#FFFFFF")], "TERMINAL · EJEMPLO", size=16, lh=30)
c.add(svg)
c.add(Note(716, 124, 436, "50-cloud-init.conf es un ejemplo de lo que podés encontrar en una imagen de nube: leelo con less antes de seguir.", kind="info"))
c.add(text(48, 318, "Así arma sshd su configuración", 19, 600, INK, FD))
order = [("1", "/etc/ssh/sshd_config", "primera línea: Include sshd_config.d/*.conf"),
         ("2", "sshd_config.d/10-ies.conf", "el tuyo: número bajo, se lee primero"),
         ("3", "sshd_config.d/50-cloud-init.conf", "después, en orden alfabético"),
         ("4", "resto de /etc/ssh/sshd_config", "lo que queda del archivo principal")]
for i, (n, f, d) in enumerate(order):
    y = 340 + i * 66
    c.add(rect(48 + (40 if i in (1, 2) else 0), y, 640 - (40 if i in (1, 2) else 0), 54, SOFT if i == 1 else WHITE, CYAN if i == 1 else LINE2, rx=12))
    c.add(badge(48 + (40 if i in (1, 2) else 0) + 30, y + 27, n, CYAN if i == 1 else INK3, r=15, size=15))
    c.add(text(48 + (40 if i in (1, 2) else 0) + 58, y + 24, f, 15, 600, BLUE, FM))
    c.add(text(48 + (40 if i in (1, 2) else 0) + 58, y + 45, d, 15, 500, INK3, FB))
c.add(panel(716, 340, 436, 250, "En OpenSSH gana el primer valor", "ok"))
svg, _ = wrap(740, 404, "Para la mayoría de las opciones, sshd se queda con el primer valor que lee. Como el Include está arriba, tu snippet gana sobre el archivo principal, y 10-ies gana sobre 50-cloud-init.", 388, 17, 400, INK2)
c.add(svg)
save(c, "4-paso2.svg")

# ---------------------------------------------------------------- 4-paso4: sshd -t atrapa el error
c = new(4, "sshd -t marca el error antes de que tumbe el servicio")
svg, h = term(48, 124, 1104, ["$ echo \"PasswordAuthentication yess\" | sudo tee -a /etc/ssh/sshd_config.d/10-ies.conf",
                              "$ sudo sshd -t",
                              ("/etc/ssh/sshd_config.d/10-ies.conf line 2: unsupported option \"yess\".", T_ERR),
                              "$ sudo sed -i '/yess/d' /etc/ssh/sshd_config.d/10-ies.conf",
                              "$ sudo sshd -t && sudo systemctl reload ssh",
                              ("(sin salida: la configuración es válida y recargó)", T_OK)], "TERMINAL · VM DE LABORATORIO", size=16, lh=32)
c.add(svg)
X, cw = 64, 16 * 0.6
yl = 124 + 32 + 4 + 2.6 * 32
c.add(f'<rect x="{X - 3}" y="{yl - 22}" width="{cw * 34 + 4}" height="30" rx="6" fill="none" stroke="{T_WARN}" stroke-width="2.5"/>')
c.add(f'<rect x="{X + cw * 35 - 1}" y="{yl - 22}" width="{cw * 6 + 6}" height="30" rx="6" fill="none" stroke="{T_WARN}" stroke-width="2.5"/>')
yb = 124 + h
c.add(callout(X + cw * 17, yb, 140, yb + 44, "el archivo", "warn"))
c.add(callout(X + cw * 39, yb, 440, yb + 44, "la línea", "warn"))
c.add(box(48, yb + 80, 540, 150, "Si hubieras hecho restart", ["El servicio intenta arrancar, falla y queda caído.", "Por SSH, nadie más entra hasta arreglarlo", "desde la consola."], kind="alert"))
c.add(box(612, yb + 80, 540, 150, "Con sshd -t primero", ["El error aparece en pantalla y el servicio", "sigue andando con la configuración vieja.", "Corregís, validás otra vez y recién recargás."], kind="ok"))
save(c, "4-paso4.svg")
