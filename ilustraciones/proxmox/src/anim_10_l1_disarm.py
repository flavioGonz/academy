#!/usr/bin/env python3
"""Lección 10 · Laboratorio, pasos 3 y 4: desarmar la HA antes de tocar corosync. Armada, el CRM y cada LRM tienen su
watchdog; disarm-ha freeze congela los servicios, cada LRM libera su watchdog (released) y después el CRM
(disarmed); un corte breve de corosync no reinicia ningún nodo; arm-ha vuelve a armar.
Fuentes: guía de administración (Disarming HA for Cluster Maintenance, estados armed / standby / disarming /
disarmed, released, modo freeze, watchdog de 60 s)."""
from _anim_pmx_red import *

a = new(24, "HA con fencing", "disarm-ha: tocar corosync sin reinicios sorpresa", lab=True)
a.steps([
    "Armada: el CRM y cada LRM tienen su watchdog abierto.",
    "disarm-ha freeze: los servicios se congelan y los watchdogs se liberan.",
    "Cambiás el switch de corosync: se pierde el quórum y nadie se reinicia.",
    "arm-ha: vuelven los watchdogs. La ventana, lo más corta posible.",
], still=2)

NX = [48, 318, 588]
NY, NW, NH = 182, 250, 168
for i, x in enumerate(NX):
    a.add(dev(a, x, NY, NW, NH, f"pve{i + 1}", "LRM" + (" · CRM master" if i == 1 else ""), icon="server", dark=True, tsize=19))
    wy = NY + 84
    # watchdog
    at(a, a.box(x + 18, wy, NW - 36, 34, "#0F3A2C", rx=8) + a.text(x + 32, wy + 23, "watchdog: abierto", 15, MINT, a.MONO, 600), 0, 28)
    at(a, a.box(x + 18, wy, NW - 36, 34, "#3A2E12", rx=8) + a.text(x + 32, wy + 23, "watchdog: released", 15, GOLD, a.MONO, 600), 28 + i * 2.5, 78, still=1)
    at(a, a.box(x + 18, wy, NW - 36, 34, "#0F3A2C", rx=8) + a.text(x + 32, wy + 23, "watchdog: abierto", 15, MINT, a.MONO, 600), 80 + i, 100)
    at(a, a.text(x + 18, NY + 150, "servicios: freeze", 15, SKY, a.MONO), 28, 78, still=1)
    at(a, a.text(x + 18, NY + 150, "servicios: started", 15, MINT, a.MONO), 0, 28)
    at(a, a.text(x + 18, NY + 150, "servicios: started", 15, MINT, a.MONO), 80, 100)
# CRM extra: libera último
# switch corosync
SY = 392
at(a, a.box(48, SY, 790, 56, a.WHITE, a.LINE, rx=12) + a.text(66, SY + 35, "switch de corosync", 16, a.INK, a.SANS, 600), 0, 50)
at(a, a.box(48, SY, 790, 56, a.AMBBG, a.AMB, rx=12, sw=2, extra='stroke-dasharray="9 6"') + a.text(66, SY + 35, "switch de corosync · cambiándose", 16, a.AMB, a.SANS, 600), 50, 78, still=1)
at(a, a.box(48, SY, 790, 56, a.OKBG, a.OK, rx=12, sw=2) + a.text(66, SY + 35, "switch nuevo · corosync estable", 16, a.OK, a.SANS, 600), 78, 100)
for x in NX:
    at(a, line(x + NW / 2, NY + NH, x + NW / 2, SY, a.BLUE, 3), 0, 52)
    at(a, line(x + NW / 2, NY + NH, x + NW / 2, SY, a.LINE, 3, "6 6"), 52, 76, still=1)
    at(a, line(x + NW / 2, NY + NH, x + NW / 2, SY, a.BLUE, 3), 76, 100)
for x in NX:
    at(a, chip(a, x + NW / 2, NY + NH + 6, "sin quórum", "bad", anchor="middle", h=26, size=14), 54, 74, still=1)
at(a, note(a, 48, 470, 790, 100, "Sin watchdogs, perder el quórum no dispara el fencing", ["Con la HA armada, a los 60 s sin quórum el watchdog reiniciaría el nodo.", "Desarmada, no hay fencing ni recuperación: si algo falla ahora, lo resolvés a mano."], "amb"), 50, 78, still=1)
at(a, note(a, 48, 470, 790, 100, "Armada: el fencing protege", ["Si un nodo pierde el quórum y no renueva su watchdog, a los 60 s se reinicia.", "Bien para una falla; mal para un corte que vos mismo vas a provocar."], "info"), 0, 28)
at(a, note(a, 48, 470, 790, 100, "Orden del desarme", ["El CRM congela los servicios; cada LRM termina lo suyo y libera su watchdog;", "cuando todos lo hicieron, el CRM libera el suyo."], "info"), 28, 50)
at(a, note(a, 48, 470, 790, 100, "De vuelta a la protección", ["arm-ha y ha-manager status: fencing armado y servicios en started.", "Si el comando de desarme no existe, revisá pveversion: es de 9.2 en adelante."], "ok"), 78, 100)

# estado
TX, TY, TW, TH = 870, 182, 282, 388
a.add(a.box(TX, TY, TW, TH, a.INK, rx=14))
a.add(a.text(TX + 16, TY + 28, "TERMINAL DE PVE1", 13, SKY, a.MONO, 400, extra='letter-spacing="1.8"'))
at(a, tline(a, TX + 16, TY + 60, "# ha-manager status", MINT) + tline(a, TX + 16, TY + 90, "fencing:", SKY), 0, 100, still=1)
for t0, t1, st, col, stl in [(0, 28, "armed", MINT, 0), (28, 38, "disarming", GOLD, 0), (38, 78, "disarmed", GOLD, 1), (78, 100, "armed", MINT, 0)]:
    at(a, tline(a, TX + 106, TY + 90, st, col), t0, t1, still=stl)
at(a, tline(a, TX + 16, TY + 140, "# ha-manager", MINT) + tline(a, TX + 16, TY + 164, "  crm-command", MINT) + tline(a, TX + 16, TY + 188, "  disarm-ha freeze", MINT), 28, 78, still=1)
at(a, tline(a, TX + 16, TY + 140, "# ha-manager", MINT) + tline(a, TX + 16, TY + 164, "  crm-command arm-ha", MINT), 78, 100)
at(a, tline(a, TX + 16, TY + 240, "LRM pve1: released", GOLD) + tline(a, TX + 16, TY + 264, "LRM pve2: released", GOLD) + tline(a, TX + 16, TY + 288, "LRM pve3: released", GOLD), 36, 78, still=1)
at(a, tline(a, TX + 16, TY + 240, "LRM: watchdog activo", MINT) + tline(a, TX + 16, TY + 264, "en los tres nodos", MINT), 0, 28)
at(a, tline(a, TX + 16, TY + 240, "LRM: watchdog activo", MINT) + tline(a, TX + 16, TY + 264, "en los tres nodos", MINT), 82, 100)
at(a, tline(a, TX + 16, TY + 340, "ventana sin protección", CORAL), 38, 78, still=1)

status(a, 618, [
    (0, 25, "El fencing está para las fallas, no para los trabajos programados.", a.INK, 0),
    (25, 50, "freeze: los servicios quedan como están y la HA no actúa sobre ellos.", a.AMB, 0),
    (50, 75, "Sin watchdogs que venzan, un corte breve de corosync no reinicia nodos.", a.OK, 1),
    (75, 100, "Confirmás el quórum con pvecm status y volvés a armar enseguida.", a.OK, 0),
])

write(a, 10, "l1", "disarm-ha: tocar corosync sin reinicios sorpresa",
      "Animación en cuatro tiempos con tres nodos, pve1, pve2 (con el CRM master) y pve3, cada uno con su LRM, el switch de corosync y la salida de ha-manager status. "
      "1: con la HA armada el CRM y cada LRM tienen su watchdog abierto y el fencing está en armed; si un nodo pierde el quórum y no renueva su watchdog, a los 60 segundos se reinicia. "
      "2: ha-manager crm-command disarm-ha freeze congela los servicios; cada LRM termina lo suyo y libera su watchdog, que queda released, y al final el CRM libera el suyo: el fencing pasa por disarming y queda disarmed. "
      "3: se cambia el switch de corosync y los nodos pierden el quórum un momento; como no hay watchdogs, ningún nodo se reinicia. Durante esa ventana tampoco hay recuperación automática. "
      "4: ha-manager crm-command arm-ha vuelve a armar: los watchdogs se abren otra vez, el fencing vuelve a armed y los servicios a started. Si el comando de desarme no existe, la versión es anterior a 9.2.",
      [8, 40, 62, 66, 92])
