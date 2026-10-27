"""Teoría lección 11: habilitar el firewall con IPSet management y una sesión SSH de respaldo."""
from _apmx import *

a = new(20, "Firewall de Proxmox: qué pasa al habilitarlo")
a.steps(["Firewall apagado: cualquiera llega a la web (8006) y a SSH.",
         "Antes: sesión SSH abierta e IPSet management con tu IP.",
         "Firewall: Yes. Tu IP pasa; la de otra red, no.",
         "Si algo salió mal: desde la SSH abierta, pve-firewall stop."], still=2)
a.add(card(a, 48, 190, 300, 92, "PC de administración", "10.10.10.50"))
a.add(card(a, 48, 410, 300, 92, "PC de otra red", "198.51.100.20"))
a.add(card(a, 852, 270, 300, 160, "pve1", "8006 web · 22 SSH", dark=True))
# muro
at(a, a.box(586, 176, 28, 340, a.BAD, None, rx=8) + a.text(600, 540, "firewall", 16, a.BAD, a.MONO, 700, "middle"), 50, 75, 1)
at(a, a.box(586, 176, 28, 340, "#FFFFFF", a.LINE, rx=8, extra='stroke-dasharray="6 5"') + a.text(600, 540, "firewall detenido", 16, a.GREY, a.MONO, 700, "middle"), 75, 100, 0)
# IPSet
at(a, a.box(852, 460, 300, 70, a.OKBG, a.OK, rx=12) + a.text(872, 490, "IPSet management", 17, a.OK, a.MONO, 700) + a.text(872, 515, "10.10.10.50", 15, a.INK, a.MONO, 600), 25, 100, 1)
# sesión SSH
at(a, line(a, "M348 226 C 600 226, 600 300, 846 300", a.CYAN, 3, "3 6") + chip(a, 420, 240, "ssh abierta", "cyan"), 25, 100, 1)


def pkt(kind):
    c = {"ok": a.OK, "bad": a.BAD, "info": a.BLUE}[kind]
    return dot(a, 0, 0, 12, c)


for s, e in [(0, 25)]:
    a.add(a.group(pkt("info"), a.move([(s, 360, 250), (e - 4, 840, 340), (e, 840, 340)]), a.show(s, e), still=0))
    a.add(a.group(pkt("info"), a.move([(s, 360, 456), (e - 4, 840, 380), (e, 840, 380)]), a.show(s, e), still=0))
a.add(a.group(pkt("ok"), a.move([(50, 360, 250), (70, 840, 350), (75, 840, 350)]), a.show(50, 75), still=0))
a.add(a.group(pkt("bad"), a.move([(50, 360, 456), (64, 572, 420), (75, 572, 420)]), a.show(50, 75), still=0))
at(a, chip(a, 624, 316, "pasa: está en el IPSet", "ok") + chip(a, 430, 470, "bloqueado", "bad"), 50, 75, 1)
at(a, a.box(380, 330, 420, 54, a.INK, None, rx=12) + a.text(400, 364, "# pve-firewall stop", 18, "#FFD38A", a.MONO, 700), 75, 100, 0)
caption(a, 600, [(0, 25, "Viene deshabilitado: el host atiende a cualquiera que llegue por la red.", None),
                 (25, 50, "La sesión SSH abierta es la puerta de atrás; el IPSet management, la lista de quién administra.", a.CYAN),
                 (50, 75, "Habilitado a nivel datacenter, el tráfico al host se bloquea salvo lo permitido.", a.OK),
                 (75, 100, "Con la sesión abierta, un error no te deja afuera: lo apagás, corregís y volvés a habilitar.", a.AMB)], still=2)
write(a, "11-t1.svg", "Firewall de Proxmox: qué pasa al habilitarlo",
      "Animación en cuatro tiempos con dos PC y el nodo pve1. 1: con el firewall apagado, la PC de administración 10.10.10.50 y una PC de otra red, 198.51.100.20, llegan a la web por 8006 y a SSH. "
      "2: antes de habilitarlo, se abre una sesión SSH desde la PC de administración y se carga el IPSet management con 10.10.10.50. "
      "3: con Firewall: Yes, el tráfico de 10.10.10.50 pasa porque está en management y el de 198.51.100.20 queda bloqueado. "
      "4: si algo salió mal, desde la sesión SSH que quedó abierta se corre pve-firewall stop y se recupera el acceso.")
