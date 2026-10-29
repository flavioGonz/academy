#!/usr/bin/env python3
"""Lección 2 · Laboratorio, paso 1: tildar VLAN aware y Apply Configuration. La GUI no toca la red en vivo:
escribe /etc/network/interfaces.new y muestra la diferencia; Apply la pasa a /etc/network/interfaces y ifupdown2
(ifreload -a) la aplica sin reiniciar. La sesión web sigue porque la gestión no cambió de VLAN.
Fuentes: guía de administración (interfaces.new, Apply Configuration, ifupdown2), tarjeta de la lección."""
from _anim_pmx_red import *

a = new(24, "Puente VLAN-aware", "VLAN aware y Apply: qué pasa por dentro", lab=True)
a.steps([
    "Tildás VLAN aware: la GUI escribe interfaces.new, no toca la red.",
    "Hasta aplicar, el host sigue con el archivo de siempre.",
    "Apply Configuration: el .new pasa a interfaces e ifreload aplica.",
    "vmbr0 ya filtra VLAN y tu sesión sigue: la gestión no cambió.",
], still=2)

# ---------- GUI
GX, GY, GW, GH = 48, 180, 340, 250
a.add(a.box(GX, GY, GW, GH, a.WHITE, a.LINE, rx=14))
a.add(a.box(GX, GY, GW, 40, a.SLATE, rx=14) + a.box(GX, GY + 26, GW, 14, a.SLATE, rx=0))
a.add(a.text(GX + 18, GY + 27, "Node → System → Network", 15, a.INK, a.MONO, 600))
a.add(a.text(GX + 18, GY + 72, "Edit: Linux Bridge vmbr0", 16, a.INK, a.SANS, 600))
a.add(a.text(GX + 18, GY + 106, "Bridge ports:  eno1", 15, a.TXT, a.MONO))
a.add(a.text(GX + 18, GY + 136, "IPv4/CIDR:  10.10.10.2/24", 15, a.TXT, a.MONO))
# casilla
CBX, CBY = GX + 18, GY + 156
a.add(a.box(CBX, CBY, 22, 22, a.WHITE, a.GREY, rx=4, sw=2))
a.add(during(a, a.box(CBX, CBY, 22, 22, a.BLUE, rx=4) + f'<path d="M{CBX + 5} {CBY + 11} L{CBX + 10} {CBY + 16} L{CBX + 17} {CBY + 6}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>', 4, 100, still=1))
a.add(a.text(CBX + 34, CBY + 17, "VLAN aware", 16, a.INK, a.SANS, 600))
# botón Apply
AX, AY = GX + 18, GY + 198
a.add(a.box(AX, AY, 220, 36, a.SLATE, a.LINE, rx=8) + a.text(AX + 110, AY + 24, "Apply Configuration", 15, a.INK, a.SANS, 600, "middle"))
a.add(during(a, a.box(AX, AY, 220, 36, a.BLUE, rx=8) + a.text(AX + 110, AY + 24, "Apply Configuration", 15, a.WHITE, a.SANS, 600, "middle"), 50, 56))

# ---------- archivos
FX, FW = 420, 360
NEWY, CURY = 180, 384
a.add(a.box(FX, NEWY, FW, 176, a.WHITE, a.LINE, rx=14))
a.add(a.text(FX + 18, NEWY + 30, "/etc/network/interfaces.new", 15, a.GREY, a.MONO))
at(a, a.text(FX + 18, NEWY + 66, "iface vmbr0 inet static", 15, a.TXT, a.MONO) +
   a.text(FX + 18, NEWY + 92, "  bridge-ports eno1", 15, a.TXT, a.MONO, extra='xml:space="preserve"') +
   a.box(FX + 10, NEWY + 104, FW - 20, 58, a.OKBG, rx=8) +
   a.text(FX + 18, NEWY + 126, "+ bridge-vlan-aware yes", 15, a.OK, a.MONO, 600) +
   a.text(FX + 18, NEWY + 150, "+ bridge-vids 2-4094", 15, a.OK, a.MONO, 600), 8, 54, still=0)
at(a, a.text(FX + 18, NEWY + 66, "(no existe: no hay cambios", 15, a.GREY, a.SANS) +
   a.text(FX + 18, NEWY + 90, "pendientes)", 15, a.GREY, a.SANS), 0, 8)
at(a, a.text(FX + 18, NEWY + 66, "ya aplicado: no hay cambios", 15, a.GREY, a.SANS) +
   a.text(FX + 18, NEWY + 90, "pendientes", 15, a.GREY, a.SANS), 58, 100, still=1)
a.add(a.box(FX, CURY, FW, 176, a.WHITE, a.LINE, rx=14))
a.add(a.text(FX + 18, CURY + 30, "/etc/network/interfaces", 15, a.GREY, a.MONO))
a.add(a.text(FX + 18, CURY + 66, "iface vmbr0 inet static", 15, a.TXT, a.MONO))
a.add(a.text(FX + 18, CURY + 92, "  bridge-ports eno1", 15, a.TXT, a.MONO, extra='xml:space="preserve"'))
at(a, a.text(FX + 18, CURY + 126, "(sin VLAN aware)", 15, a.GREY, a.SANS), 0, 56)
at(a, a.box(FX + 10, CURY + 104, FW - 20, 58, a.OKBG, rx=8) +
   a.text(FX + 18, CURY + 126, "  bridge-vlan-aware yes", 15, a.OK, a.MONO, 600, extra='xml:space="preserve"') +
   a.text(FX + 18, CURY + 150, "  bridge-vids 2-4094", 15, a.OK, a.MONO, 600, extra='xml:space="preserve"'), 58, 100, still=1)
# GUI escribe el .new
go(a, "guarda", [(GX + GW - 20, GY + 166), (FX + 40, NEWY + 120)], 5, 9, a.BLUE, hold=0.6)
# Apply: el .new baja a interfaces
a.add(travel(a, a.box(-150, -16, 300, 32, a.OKBG, a.OK, rx=8, sw=2) + a.text(0, 6, "interfaces.new → interfaces", 15, a.OK, a.MONO, 600, "middle"),
             [(FX + FW / 2, NEWY + 132), (FX + FW / 2, CURY + 132)], 52, 57, hold=0.5))
# pendiente
at(a, chip(a, GX, GY + GH + 16, "Pending changes: + 2 líneas", "amb", h=30), 10, 54)

# ---------- host en vivo
HX, HY, HW, HH = 812, 180, 340, 204
a.add(a.box(HX, HY, HW, HH, a.INK, rx=14))
a.add(glyph(a, "server", HX + 18, HY + 16, a.CYAN))
a.add(a.text(HX + 60, HY + 36, "pve1 · red en vivo", 18, a.WHITE, a.SANS, 600))
a.add(a.text(HX + 20, HY + 82, "vmbr0  10.10.10.2/24", 15, a.WHITE, a.MONO))
at(a, a.text(HX + 20, HY + 112, "vlan_filtering 0", 15, SKY, a.MONO), 0, 57)
at(a, a.text(HX + 20, HY + 112, "vlan_filtering 1", 15, MINT, a.MONO, 600), 57, 100, still=1)
at(a, a.text(HX + 20, HY + 146, "sin reiniciar el nodo", 15, MINT, a.SANS, 600), 60, 100, still=1)
at(a, a.text(HX + 20, HY + 146, "igual que antes del clic", 15, SKY, a.SANS), 10, 50)
at(a, a.box(HX - 3, HY - 3, HW + 6, HH + 6, "none", GOLD, rx=16, sw=3), 54, 62)
at(a, a.text(HX + 20, HY + 182, "# ifreload -a", 15, GOLD, a.MONO, 600), 54, 75)

# notebook y sesión
NX, NY = 812, 460
a.add(dev(a, NX, NY, 340, 84, "Notebook del técnico", "10.10.10.50 · web :8006", icon="laptop"))
a.add(line(NX + 170, NY, NX + 170, HY + HH, a.BLUE, 3, "6 6"))
for t in (2, 22, 42, 62, 82):
    a.add(travel(a, f'<circle r="8" fill="{a.CYAN}"/>', [(NX + 170, NY - 4), (NX + 170, HY + HH + 6)], t, t + 4, hold=0.2, fade=0.3))
at(a, chip(a, NX + 186, NY - 52, "sesión abierta", "ok"), 62, 100, still=1)

status(a, 622, [
    (0, 25, "La GUI prepara el cambio en un archivo aparte: un error a medio escribir no corta la red.", a.INK, 0),
    (25, 50, "Pending changes muestra la diferencia: es el momento de revisar antes de aplicar.", a.AMB, 0),
    (50, 75, "Apply usa ifupdown2: aplica la configuración nueva sin reiniciar el nodo.", a.BLUE, 1),
    (75, 100, "Si la IP de gestión cambiara de VLAN, esto se hace con consola local o IPMI.", a.OK, 0),
])

write(a, 2, "l1", "VLAN aware y Apply: qué pasa por dentro",
      "Animación en cuatro tiempos con la ventana Node, System, Network de la GUI, los archivos /etc/network/interfaces.new y /etc/network/interfaces, "
      "el host pve1 con su red en vivo y la notebook del técnico con la sesión web en el puerto 8006. "
      "1: al tildar VLAN aware en vmbr0, la GUI guarda el cambio en interfaces.new, con las líneas nuevas bridge-vlan-aware yes y bridge-vids 2-4094; la red del host no cambia. "
      "2: hasta aplicar, el host sigue con el archivo de siempre y la GUI muestra Pending changes con la diferencia. "
      "3: Apply Configuration pasa interfaces.new a interfaces y ifreload -a, de ifupdown2, lo aplica sin reiniciar; vmbr0 pasa a filtrar VLAN. "
      "4: la sesión web del técnico sigue abierta porque la IP de gestión no cambió de VLAN; si cambiara, el trabajo se hace con consola local o IPMI.",
      [6, 30, 56, 66, 90])
