"""Lección 16 · Paquetes al día."""
from _comun_12_22 import *

K = "MikroTik"

# ---------------------------------------------------------------- principal: paquetes
c = Canvas(K, "Un paquete principal y extras que se habilitan")
c.add(f'<rect x="48" y="140" width="520" height="250" rx="20" fill="{DEEP}"/>')
c.add(text(76, 196, "routeros", 34, 600, WHITE, FM))
c.add(para(76, 240, "Casi todo viene acá: firewall, ruteo, VPN, DHCP, herramientas. Se actualiza con System > Packages > Check for Updates.", 460, 17, "#D9E9F8", 400))
c.add(Chip(76, 360, ".npk de la arquitectura del equipo", "cyan", mono=False))

c.add(Label(622, 160, "PAQUETES EXTRA (flags X A = disponibles, no instalados)", 14, 600, INK3, FM))
extras = [("container", 622, 190), ("zerotier", 842, 190), ("user-manager", 622, 262)]
for nm, x, y in extras:
    c.add(pill(x, y, 200 if nm != "user-manager" else 230, 52, nm, WHITE, INK, 17, FM, 600, stroke=LINE2))
c.add(pill(622, 334, 200, 52, "wifi-qcom", WHITE, INK, 17, FM, 600, stroke=ALERT))
c.add(pill(942, 334, 200, 52, "wireless", WHITE, INK, 17, FM, 600, stroke=ALERT))
c.add(line(822, 360, 942, 360, ALERT, 3, "6 6"))
c.add(Mark(882, 360, False))
c.add(para(622, 420, "wifi-qcom y wireless no pueden estar activos a la vez (desde 7.13). Un extra se habilita y se aplica con reinicio.", 530, 16, ALERT, 500))

c.add(panel(48, 480, 520, 116, "Download", "info"))
c.add(para(68, 544, "Baja la versión y espera: reiniciás vos cuando el cliente puede.", 480, 17, INK, 500))
c.add(panel(632, 480, 520, 116, "Download&Install", "warn"))
c.add(para(652, 544, "Baja e instala: reinicia solo al terminar.", 480, 17, INK, 500))
save(c, "16.svg")

# ---------------------------------------------------------------- paso 4: sin internet
c = Canvas(K + " · Paso 4", "Sin internet: el .npk correcto, a la raíz de Files")
pc = c.add(Laptop(48, 150, "PC con internet", "mikrotik.com", w=280))
c.add(file_icon(420, 140, "routeros-(versión)-arm64.npk", "misma arquitectura"))
c.add(Arrow(pc.right(), (408, 192), bend="straight"))
w = c.add(Window(760, 130, 392, 150, "WinBox · Files", rows=[("routeros-…-arm64.npk", "raíz"), ("hotspot/", "carpeta")], hl=0))
c.add(Arrow((560, 192), (750, 210), "arrastrar", label_dy=-12))
c.add(Note(48, 330, 560, "En System > Resources mirá architecture-name (acá arm64 es el ejemplo) y bajá el .npk de esa misma arquitectura.", title="1 · La arquitectura manda", kind="info"))
c.add(Note(632, 330, 520, "Si lo soltás dentro de una carpeta, no se instala. Tiene que quedar en la raíz.", title="2 · En la raíz, no en una carpeta", kind="warn"))
c.add(Terminal(48, 490, 560, ["/file/print where name~\".npk\"", "/system/reboot"], title="3 · VERIFICÁ Y REINICIÁ"))
save(c, "16-paso4.svg")

# ---------------------------------------------------------------- paso 6: orden y RouterBOOT
c = Canvas(K + " · Paso 6", "Después de RouterOS, RouterBOOT")
steps = [("Backup", "antes de tocar"), ("RouterOS", "instalar y reiniciar"), ("routerboard print", "comparar versiones"),
         ("routerboard upgrade", "carga el nuevo"), ("Reiniciar", "queda aplicado")]
x0, wst, gap = 48, 204, 21
for i, (t, s) in enumerate(steps):
    x = x0 + i * (wst + gap)
    c.add(panel(x, 140, wst, 110, None, "dark" if i in (3, 4) else "info"))
    c.add(badge(x + 30, 172, i + 1))
    c.add(text(x + 20, 216, t, 15 if " " in t else 18, 600, WHITE if i in (3, 4) else INK, FM if " " in t else FD))
    c.add(text(x + 20, 238, s, 15, 400, "#9FC3E3" if i in (3, 4) else INK3))
    if i < 4:
        c.add(Arrow((x + wst + 3, 195), (x + wst + gap - 3, 195), bend="straight"))
w = c.add(Window(48, 300, 560, 140, "/system/routerboard/print", rows=[("current-firmware", "versión anterior"), ("upgrade-firmware", "la de RouterOS nuevo")], hl=1))
c.add(Note(632, 300, 520, "Cada versión de RouterOS trae su RouterBOOT. Si current-firmware y upgrade-firmware no coinciden, falta el paso 4 y el reinicio.", title="Qué mirar", kind="info"))
c.add(Note(48, 480, 1104, "Equipos WiFi con actualización manual: subí también wifi-qcom o wireless de la misma versión. Nunca cortes la energía durante la instalación.", kind="warn"))
save(c, "16-paso6.svg")
