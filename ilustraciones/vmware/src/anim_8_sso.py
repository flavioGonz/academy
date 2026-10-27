"""Teoría lección 8: SSO autentica; el permiso (usuario + rol + objeto) decide qué se ve y qué se puede hacer."""
from _avmw import *

a = new(24, "Quién sos lo dice SSO; qué podés hacer, el permiso")
a.steps(["tecnico.prueba entra: SSO valida el usuario en vsphere.local.",
         "En Lab-Pruebas tiene Soporte-Lectura: ve las VMs y abre la consola.",
         "Intenta apagar una VM: el rol no tiene ese privilegio, se rechaza.",
         "En Produccion no tiene permiso: ni siquiera la ve."], still=1)

a.add(card(a, 48, 190, 280, 90, "tecnico.prueba", "@vsphere.local"))
a.add(card(a, 48, 320, 280, 110, "vCenter SSO", "dominio vsphere.local", dark=True))
# inventario
a.add(card(a, 420, 180, 732, 380, "Inventario de vCenter", None))
a.add(a.box(450, 236, 330, 300, "#E5F0FB", a.CYAN, rx=12, sw=2) + a.text(470, 266, "Lab-Pruebas", 17, a.INK, a.SANS, 600) + a.text(470, 288, "Soporte-Lectura, propagado", 13, a.BLUE, a.MONO, 600))
for k, n in enumerate(["vm-prueba", "vm-prueba-2"]):
    a.add(vmbox(a, 470, 310 + k * 80, 290, 60, n))
a.add(a.box(800, 236, 330, 300, a.SLATE, a.LINE, rx=12, sw=2) + a.text(820, 266, "Produccion", 17, a.INK, a.SANS, 600) + a.text(820, 288, "sin permiso", 13, a.GREY, a.MONO, 600))
a.add(vmbox(a, 820, 310, 290, 60, "srv-video"))
# 1: login
a.add(a.group('<circle r="11" fill="#FFB020" stroke="#fff" stroke-width="3"/>', a.move([(0, 188, 280), (2, 188, 280), (12, 188, 330), (22, 188, 330), (100, 188, 330)]),
              a.keyframes([(0, 0), (1, 0), (2, 1), (22, 1), (24, 0), (100, 0)]), still=0))
at(a, chip(a, 68, 446, "usuario y clave ok", "ok"), 12, 100, 1)
# 2: consola
at(a, a.box(470, 310, 290, 60, "none", a.OK, rx=12, sw=3) + chip(a, 470, 470, "ver y abrir consola: sí", "ok"), 25, 50, 1)
# 3: apagar rechazado
at(a, a.box(470, 390, 290, 60, a.BADBG, a.BAD, rx=12, sw=3) + a.text(518, 416, "vm-prueba-2", 16, a.BAD, a.SANS, 600) + a.text(518, 438, "Power Off", 14, a.BAD, a.MONO, 600)
   + chip(a, 470, 470, "apagar: permiso denegado", "bad"), 50, 75, 0)
# 4: producción invisible
at(a, a.box(800, 236, 330, 300, a.BG, a.LINE, rx=12, sw=2) + a.text(965, 386, "no aparece", 18, a.GREY, a.MONO, 600, "middle"), 75, 100, 0)
caption(a, 610, [(0, 25, "SSO solo responde quién sos; todavía no dice qué podés tocar.", None),
                 (25, 50, "El permiso puesto en la carpeta baja a sus hijos con Propagate to children.", a.OK),
                 (50, 75, "Un error de soporte no puede apagar un servidor si el rol no lo permite.", a.BAD),
                 (75, 100, "Sin permiso en un objeto, ese objeto no existe para ese usuario.", None)], still=1)
write(a, "8-t1.svg", "Quién sos lo dice SSO; qué podés hacer, el permiso",
      "Animación en cuatro tiempos. A la izquierda el usuario tecnico.prueba y vCenter SSO; a la derecha el inventario con dos carpetas: Lab-Pruebas, con el rol Soporte-Lectura propagado, y Produccion, sin permiso. "
      "1: el usuario entra y SSO valida usuario y clave en vsphere.local. 2: en Lab-Pruebas ve las VMs y puede abrir la consola. "
      "3: intenta apagar vm-prueba-2 y se rechaza porque el rol no tiene ese privilegio. 4: la carpeta Produccion directamente no aparece para ese usuario.")
