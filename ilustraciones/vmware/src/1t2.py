import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 1-t2: línea de tiempo de licencias
c = Canvas(K(), "De la licencia perpetua a la suscripción por núcleo")
c.add(NOLIG)
Y = 330
c.add(f'<path d="M70 {Y}H1130" stroke="{LINE2}" stroke-width="6" stroke-linecap="round"/>')
ev = [
    (110, "2001", "ESX Server", "el hipervisor de VMware sobre el servidor", "info", True),
    (300, "2011", "vSphere 5.0", "queda solo ESXi, sin consola de servicio", "info", False),
    (490, "nov. 2023", "Broadcom compra VMware", "", "info", True),
    (680, "feb. 2024", "Solo suscripción", "por núcleo, mínimo 16 por CPU; vCenter incluido", "warn", False),
    (870, "abr. 2025", "ESXi gratuito 8.0 U3e", "sin vCenter, sin VADP, sin soporte", "warn", True),
    (1070, "11/10/2027", "Fin de soporte de vSphere 8", "sin parches ni soporte técnico", "alert", False),
]
for x, fecha, t, s, k, up in ev:
    col = {"info": BLUE, "warn": WARN, "alert": ALERT}[k]
    c.add(f'<circle cx="{x}" cy="{Y}" r="13" fill="{WHITE}" stroke="{col}" stroke-width="4"/>')
    w = 232
    bx = min(max(x - w / 2, 48), 1152 - w)
    by = Y - 190 if up else Y + 40
    c.add(vline(x, Y - 14 if up else Y + 14, by + (150 if up else 0), col, 2, "4 4"))
    c.add(rect(bx, by, w, 150, {"info": WHITE, "warn": WARN_BG, "alert": ALERT_BG}[k], col, rx=14, sw=2))
    c.add(text(bx + 16, by + 32, fecha, 17, 700, col, FM))
    sv, _ = wrap(bx + 16, by + 62, t, w - 30, 17, 600, INK, FD)
    c.add(sv)
    if s:
        sv, _ = wrap(bx + 16, by + 108, s, w - 30, 14, 400, INK2)
        c.add(sv)
c.add(text(48, 640, "Fechas de la KB de Broadcom, Thomas-Krenn e Introserv; 2001 y 2011 son historia conocida del producto.", 15, 400, INK3, FB))
save(c, "1-t2.svg")
