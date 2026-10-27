import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/proxmox/src")
from _pmx import *

# ---------------------------------------------------------------- 11.svg: tres capas de acceso
c = Canvas(K(), "Quién entra y cómo: usuarios, 2FA y firewall")
c.add(NOLIG)
cols = [("Un usuario por persona", "user", [("tecnico@pve", "PVEAuditor: mira, no toca"), ("operador@pve", "PVEVMUser: consola, encendido, backup"), ("root@pam", "solo el administrador")]),
        ("Segundo factor", "key", [("TOTP", "código de la app del celular"), ("WebAuthn", "llave de seguridad"), ("Recovery keys", "guardadas en el gestor")]),
        ("Firewall sin quedarse afuera", "shield", [("Sesión SSH abierta", "antes de habilitar"), ("IPSet management", "IPs de administración"), ("Firewall: Yes", "recién al final")])]
for i, (t, ic, items) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 122, 352, 400, None, "info"))
    c.add(icon(x + 22, 140, ic, BLUE, 1.3))
    c.add(text(x + 62, 166, t, 19, 700, INK, FB))
    c.add(hline(x + 20, x + 332, 190))
    for j, (k, v) in enumerate(items):
        y = 214 + j * 98
        c.add(rect(x + 20, y, 312, 80, SOFT if j < 2 or i != 2 else OK_BG, LINE2 if j < 2 or i != 2 else OK, rx=12))
        c.add(text(x + 36, y + 32, k, 17, 700, BLUE if (j < 2 or i != 2) else OK, FM))
        c.add(text(x + 36, y + 60, v, 15, 500, INK2, FB))
c.add(Note(48, 546, 1104, "Con usuarios personales, el log dice quién hizo cada cambio. Con más de un factor, perder el celular no te deja afuera.", kind="ok"))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso1: el permiso en el árbol
c = Canvas(K(1), "pveum: un usuario y un rol sobre el árbol de permisos")
c.add(NOLIG)
c.add(Step(48, 124, 1))
sv, h = codebox(80, 124, 640, ["pveum user add tecnico@pve --comment \"Técnico de soporte\"", "pveum passwd tecnico@pve",
                               ("pveum acl modify / --user tecnico@pve --role PVEAuditor", "#7FE0B0"), "pveum user permissions tecnico@pve"], 15, 28)
c.add(sv)
# árbol
c.add(rect(760, 124, 392, 240, WHITE, LINE2, rx=16))
c.add(text(784, 160, "Árbol de permisos", 17, 600, INK3, FB))
tree = [("/", 0, True), ("/nodes", 1, False), ("/vms", 1, False), ("/storage", 1, False)]
for j, (p, lvl, hl) in enumerate(tree):
    y = 196 + j * 40
    c.add(text(800 + lvl * 30, y + 6, p, 17, 700 if hl else 500, BLUE if hl else INK2, FM))
c.add(path("M808 206 V322", LINE2, 2))
c.add(tag(880, 203, "PVEAuditor", "info", 15))
c.add(text(784, 352, "Asignado en /, se hereda hacia abajo.", 15, 500, INK3, FB))
c.add(text(80, 420, "Lo que puede hacer tecnico@pve:", 18, 600, INK, FB))
for i, (s, ok) in enumerate([("ver nodos, VMs y almacenamiento", True), ("ver estado y configuración", True), ("prender, apagar o borrar VMs", False), ("cambiar la configuración", False)]):
    c.add(check(104 + (i // 2) * 540, 464 + (i % 2) * 52, s, ok, 18))
c.add(Note(80, 566, 1072, "Realm pve: contraseñas propias de Proxmox, lo más cómodo en instalaciones chicas. pam es para usuarios del sistema Linux.", kind="info"))
save(c, "11-paso1.svg")

# ---------------------------------------------------------------- 11-paso3: el orden del firewall
c = Canvas(K(3), "Firewall en este orden, y una puerta trasera abierta")
c.add(NOLIG)
c.add(Step(48, 124, 3))
steps = [("a", "Abrí una sesión SSH al nodo", "y dejala abierta: es tu salida si algo falla", "info"),
         ("b", "IPSet management", "Datacenter → Firewall → IPSet: tu IP, por ejemplo 10.10.10.50", "info"),
         ("c", "Firewall: Yes", "Datacenter → Firewall → Options, recién ahora", "ok")]
for i, (n, t, d, kd) in enumerate(steps):
    y = 136 + i * 108
    c.add(rect(80, y, 640, 90, OK_BG if kd == "ok" else WHITE, OK if kd == "ok" else LINE2, rx=14))
    c.add(badge(116, y + 45, n, OK if kd == "ok" else CYAN))
    c.add(text(150, y + 38, t, 19, 700, INK, FB))
    c.add(text(150, y + 66, d, 15, 500, INK2, FB))
c.add(rect(760, 136, 392, 306, DEEP, DEEP, rx=16))
c.add(text(784, 174, "Desde la sesión SSH", 19, 600, WHITE, FD))
c.add(text(784, 212, "¿Compila sin errores?", 16, 500, "#9FC3E3", FB))
c.add(code(784, 226, 344, "pve-firewall status", 15))
c.add(text(784, 300, "¿Quedaste afuera de la web?", 16, 500, "#9FC3E3", FB))
c.add(code(784, 314, 344, "pve-firewall stop", 15, color="#FFD38A"))
c.add(text(784, 388, "Y revisás las reglas con calma.", 15, 500, "#9FC3E3", FB))
c.add(Note(80, 474, 1072, "En un servidor remoto sin consola fuera de banda, un firewall mal configurado te deja sin acceso. Hubo quien tuvo que arrancar en modo rescate y editar la base de configuración de Proxmox para volver a entrar.", title="Por qué este orden", kind="warn"))
save(c, "11-paso3.svg")
