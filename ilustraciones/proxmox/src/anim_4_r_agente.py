#!/usr/bin/env python3
"""Lección 4 · Resumen, "Cómo se ve en la red" (entre el host y la VM): el canal del QEMU guest agent. Proxmox habla
con el servicio qemu-guest-agent de adentro por el socket /var/run/qemu-server/100.qga: ping, las IP para el
Summary, el apagado sin depender de ACPI y el congelamiento del sistema de archivos antes de un backup.
Fuentes: wiki Qemu-guest-agent y guía de administración (QEMU Guest Agent: IPs en Summary, shutdown por agente,
guest-fsfreeze-freeze / thaw, socket .qga)."""
from _anim_pmx_red import *

a = new(24, "VM bien armada", "El agente: un canal entre el host y la VM")
a.steps([
    "qm agent 100 ping: el pedido entra a la VM y el agente contesta.",
    "Summary pide las IP: el agente las lee adentro y las devuelve.",
    "Shutdown: Proxmox le pide el apagado al agente, no al botón ACPI.",
    "Antes del backup: freeze, se copia el instante, thaw.",
], still=3)

HXc, GXc = 210, 990
a.add(dev(a, 48, 180, 330, 76, "pve1 · Proxmox", "qm · web · vzdump", icon="server", dark=True, tsize=18))
a.add(dev(a, 822, 180, 330, 76, "VM 100 · Debian", "qemu-guest-agent", icon="server", tsize=18))
# canal
CX, CW = 470, 260
a.add(a.box(CX, 180, CW, 76, a.SLATE, a.LINE, rx=14))
a.add(a.text(CX + CW / 2, 210, "canal del agente", 16, a.INK, a.SANS, 600, "middle"))
a.add(a.text(CX + CW / 2, 236, "/var/run/qemu-server/100.qga", 15, a.GREY, a.MONO, 400, "middle"))
a.add(f'<rect x="{CX + CW / 2 - 1}" y="256" width="2" height="250" fill="{a.LINE}"/>')
a.add(lifeline(a, HXc, 256, 506))
a.add(lifeline(a, GXc, 256, 506))

Y1, Y2 = 320, 420
# 1 · ping
msg(a, HXc, GXc, Y1, "guest-ping", 3, end=25, still=0)
msg(a, GXc, HXc, Y2, "{} · sin error", 12, end=25, color=a.OK, still=0)
# 2 · IP
msg(a, HXc, GXc, Y1, "network-get-interfaces", 28, end=50, still=0)
msg(a, GXc, HXc, Y2, "eth0 · 10.10.10.100", 37, end=50, color=a.OK, still=0)
# 3 · shutdown
msg(a, HXc, GXc, Y1, "guest-shutdown", 53, end=75, still=0, color=a.AMB)
at(a, a.text(GXc - 16, Y2 - 18, "el sistema cierra servicios", 15, a.TXT, a.SANS, 400, "end") + a.text(GXc - 16, Y2 + 6, "y se apaga solo", 15, a.TXT, a.SANS, 400, "end"), 58, 75)
# 4 · freeze / thaw
msg(a, HXc, GXc, Y1 - 30, "guest-fsfreeze-freeze", 78, end=100, still=1)
at(a, chip(a, GXc - 20, Y1 - 6, "escrituras en pausa", "amb", anchor="end"), 81, 100, still=1)
at(a, chip(a, HXc + 20, 384, "se marca el instante del backup", "info"), 86, 100, still=1)
msg(a, HXc, GXc, Y2 + 40, "guest-fsfreeze-thaw", 91, end=100, still=1, color=a.OK)

# resultado abajo
RY = 524
r1 = note(a, 48, RY, 1104, 74, "Respuesta sin error", ["Si el agente no corre adentro, el mismo comando termina en error: así se prueba el canal."], "ok")
r2 = (a.box(48, RY, 1104, 74, a.WHITE, a.LINE, rx=12) + a.text(70, RY + 30, "VM 100 · Summary", 16, a.INK, a.SANS, 600)
      + a.text(70, RY + 56, "IPs: 10.10.10.100", 16, a.OK, a.MONO, 600) + a.text(1130, RY + 44, "sin agente: \"Guest Agent not running\"", 15, a.GREY, a.MONO, 400, "end"))
r3 = note(a, 48, RY, 1104, 74, "Apagado limpio", ["Sin el agente corriendo, Shutdown depende del ACPI del invitado y puede quedar esperando hasta el timeout."], "amb")
r4 = note(a, 48, RY, 1104, 74, "Backup consistente", ["La foto se toma con el sistema de archivos quieto: nada a medio escribir. En Windows lo resuelve VSS."], "ok")
at(a, r1, 14, 25)
at(a, r2, 39, 50)
at(a, r3, 60, 75)
at(a, r4, 93, 100, still=1)

status(a, 640, [
    (0, 25, "El agente es un servicio adentro de la VM; el canal lo arma QEMU al arrancar.", a.INK, 0),
    (25, 50, "Las IP que ves en la GUI no las adivina Proxmox: se las cuenta el agente.", a.BLUE, 0),
    (50, 75, "Con el agente, el apagado no depende de la configuración de energía del invitado.", a.AMB, 0),
    (75, 100, "Freeze y thaw duran un instante: la VM sigue trabajando durante el backup.", a.OK, 1),
])

write(a, 4, "r1", "El agente: un canal entre el host y la VM",
      "Animación en cuatro tiempos con el host pve1 (qm, la web y vzdump), la VM 100 con Debian y el servicio qemu-guest-agent, y en el medio el canal del agente, el socket /var/run/qemu-server/100.qga. "
      "1: qm agent 100 ping manda guest-ping por el canal y el agente contesta sin error; si el agente no corre adentro, el comando termina en error. "
      "2: el panel Summary pide network-get-interfaces y el agente devuelve eth0 con 10.10.10.100, que aparece en IPs; sin agente la GUI muestra Guest Agent not running. "
      "3: al tocar Shutdown, Proxmox manda guest-shutdown al agente y el sistema cierra sus servicios y se apaga solo, sin depender del botón ACPI; sin el agente corriendo, puede quedar esperando hasta el timeout. "
      "4: antes de un backup, Proxmox manda guest-fsfreeze-freeze, las escrituras quedan en pausa, se marca el instante del backup y guest-fsfreeze-thaw las libera; la VM sigue trabajando y el backup sale consistente.",
      [8, 18, 44, 66, 97])
