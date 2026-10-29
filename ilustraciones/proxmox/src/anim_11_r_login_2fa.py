#!/usr/bin/env python3
"""Lección 11 · Resumen, "Cómo se ve en la red": el técnico entra con 2FA y rol justo. Usuario y clave en la web
(8006); Proxmox pide el segundo factor; la app y el servidor calculan el mismo código TOTP con el secreto
compartido y la hora (cada 30 s); entra; con PVEAuditor puede mirar, pero apagar una VM da Permission check failed.
Fuentes: tarjeta de la lección (realm pve, PVEAuditor, TOTP RFC 6238, Two Factor), guía de administración
(permisos sobre rutas, privilegio VM.PowerMgmt)."""
from _anim_pmx_red import *

a = new(24, "Acceso blindado", "Clave, código del celular y el rol justo")
a.steps([
    "tecnico@pve entra con usuario y clave: Proxmox pide el segundo factor.",
    "App y servidor calculan el mismo código: secreto compartido más la hora.",
    "Código correcto: entra. Con PVEAuditor ve todo el árbol.",
    "Intenta apagar la VM 100: su rol no tiene ese privilegio.",
], still=2)

a.add(dev(a, 48, 186, 250, 84, "Notebook", "tecnico@pve", icon="laptop", tsize=18))
a.add(dev(a, 48, 420, 250, 84, "Celular", "app TOTP", icon="phone", tsize=18))
# web de Proxmox
WX, WY, WW, WH = 340, 182, 470, 330
a.add(a.box(WX, WY, WW, WH, a.WHITE, a.LINE, rx=14))
a.add(a.box(WX, WY, WW, 40, a.SLATE, rx=14) + a.box(WX, WY + 26, WW, 14, a.SLATE, rx=0))
a.add(a.text(WX + 18, WY + 27, "https://pve1:8006", 15, a.INK, a.MONO, 600))
p1 = (a.text(WX + 24, WY + 82, "Usuario: tecnico", 16, a.INK, a.MONO) + a.text(WX + 24, WY + 114, "Realm:   Proxmox VE (pve)", 16, a.INK, a.MONO)
      + a.text(WX + 24, WY + 146, "Clave:   ••••••••", 16, a.INK, a.MONO))
at(a, p1, 0, 14)
p2 = (a.text(WX + 24, WY + 82, "Segundo factor", 18, a.INK, a.SANS, 600) + a.text(WX + 24, WY + 112, "TOTP · ingresá el código de tu app", 15, a.GREY, a.SANS)
      + a.box(WX + 24, WY + 132, 220, 50, a.WHITE, a.BLUE, rx=8, sw=2))
at(a, p2, 14, 56)
at(a, a.text(WX + 40, WY + 166, "_ _ _ _ _ _", 20, a.GREY, a.MONO, 700), 14, 46)
at(a, a.text(WX + 40, WY + 166, "482 917", 20, a.INK, a.MONO, 700), 46, 56)
# árbol (paso 3 y 4)
tree = a.text(WX + 24, WY + 76, "Datacenter", 16, a.INK, a.SANS, 600)
for i, (lab, ind) in enumerate([("pve1", 1), ("100 (servidor)", 2), ("101 (vms)", 2), ("local-lvm", 2)]):
    tree += a.text(WX + 24 + ind * 22, WY + 106 + i * 28, lab, 15, a.TXT, a.MONO)
tree += a.text(WX + 24, WY + 236, "tecnico@pve · PVEAuditor en /", 15, a.BLUE, a.MONO, 600)
at(a, tree, 56, 100, still=1)
at(a, a.box(WX + 250, WY + 60, 196, 40, a.SLATE, a.LINE, rx=8) + a.text(WX + 348, WY + 86, "Shutdown", 15, a.INK, a.SANS, 600, "middle"), 76, 100)
at(a, a.box(WX + 20, WY + 252, WW - 40, 64, a.BADBG, a.BAD, rx=10, sw=2) + a.text(WX + 36, WY + 278, "Permission check failed", 15, a.BAD, a.MONO, 700)
   + a.text(WX + 36, WY + 302, "(/vms/100, VM.PowerMgmt)", 15, a.BAD, a.MONO, 700), 82, 100)

# servidor y app: cálculo
SX, SY, SW, SH = 850, 182, 302, 330
a.add(a.box(SX, SY, SW, SH, a.INK, rx=14))
a.add(a.text(SX + 18, SY + 30, "TOTP · RFC 6238", 15, SKY, a.MONO, 400, extra='letter-spacing="1.2"'))
calc = (tline(a, SX + 18, SY + 70, "secreto compartido", a.WHITE) + tline(a, SX + 18, SY + 94, "(se cargó al escanear", SKY) + tline(a, SX + 18, SY + 116, " el QR del alta)", SKY)
        + tline(a, SX + 18, SY + 152, "+ hora actual / 30 s", a.WHITE) + tline(a, SX + 18, SY + 188, "= código de 6 dígitos", a.WHITE)
        + tline(a, SX + 18, SY + 236, "servidor:  482 917", MINT) + tline(a, SX + 18, SY + 262, "celular:   482 917", MINT) + tline(a, SX + 18, SY + 298, "iguales: entra", MINT))
at(a, calc, 26, 56)
at(a, tline(a, SX + 18, SY + 70, "esperando el segundo", SKY) + tline(a, SX + 18, SY + 94, "factor...", SKY), 14, 26)
at(a, tline(a, SX + 18, SY + 70, "ticket de tecnico@pve", MINT) + tline(a, SX + 18, SY + 104, "permisos efectivos:", SKY)
   + tline(a, SX + 18, SY + 128, "/  PVEAuditor", a.WHITE) + tline(a, SX + 18, SY + 152, "   (se hereda abajo)", SKY)
   + tline(a, SX + 18, SY + 192, "Sys.Audit, VM.Audit,", a.WHITE) + tline(a, SX + 18, SY + 216, "Datastore.Audit ...", a.WHITE), 56, 78, still=1)
at(a, tline(a, SX + 18, SY + 70, "pide: VM.PowerMgmt", GOLD) + tline(a, SX + 18, SY + 94, "en /vms/100", GOLD)
   + tline(a, SX + 18, SY + 134, "PVEAuditor no lo", CORAL) + tline(a, SX + 18, SY + 158, "tiene: rechazado", CORAL)
   + tline(a, SX + 18, SY + 204, "nada cambió en la VM", MINT), 78, 100)
# código en el celular
for t0, t1, code, st in [(0, 27, "731 204", 0), (27, 100, "482 917", 1)]:
    at(a, a.box(196, 446, 92, 30, a.OKBG, rx=6) + a.text(242, 467, code, 15, a.OK, a.MONO, 700, "middle"), t0, t1, still=st)
at(a, a.text(48, 530, "cambia cada 30 s", 15, a.GREY, a.SANS), 0, 100, still=1)

# viajes
go(a, "usuario + clave", [(298, 228), (WX, 228)], 3, 7, a.BLUE, hold=0.5)
go(a, "¿segundo factor?", [(WX, 252), (298, 252)], 11, 14, a.AMB, hold=1)
go(a, "482 917", [(260, 420), (260, 300), (WX, 300)], 40, 46, a.OK, hold=0.5)
go(a, "Shutdown", [(298, 228), (WX + 250, 228)], 78, 82, a.BLUE, hold=0.5)
at(a, chip(a, 48, 290, "el código viaja una vez", "info"), 44, 56)

status(a, 600, [
    (0, 25, "Con una clave filtrada no alcanza: falta algo que el técnico tiene en la mano.", a.INK, 0),
    (25, 50, "El código no viaja desde el servidor: los dos lo calculan por su cuenta.", a.BLUE, 0),
    (50, 75, "PVEAuditor en / se hereda a todo el árbol: ve nodos, VMs y almacenamiento.", a.OK, 1),
    (75, 100, "El rol justo evita el error: mirar sí, apagar o borrar no.", a.AMB, 0),
])
at(a, a.text(600, 632, "Claves de recuperación guardadas en el gestor: por si se pierde el celular.", 16, a.GREY, a.SANS, 400, "middle"), 0, 100, still=1)

write(a, 11, "r1", "Clave, código del celular y el rol justo",
      "Animación en cuatro tiempos con la notebook del técnico, su celular con una app TOTP, la web de Proxmox en https://pve1:8006 y el cálculo del servidor. "
      "1: tecnico@pve entra con usuario, realm Proxmox VE (pve) y clave; Proxmox no lo deja pasar todavía y pide el segundo factor TOTP. "
      "2: la app del celular y el servidor calculan cada uno el mismo código de 6 dígitos con el secreto compartido, que se cargó al escanear el QR del alta, y la hora actual en pasos de 30 segundos, como define la RFC 6238; el técnico escribe 482 917 y coinciden. "
      "3: entra con su ticket; con PVEAuditor asignado en /, que se hereda hacia abajo, ve el árbol completo: pve1, las VM 100 y 101 y local-lvm, con privilegios de lectura como Sys.Audit, VM.Audit y Datastore.Audit. "
      "4: intenta apagar la VM 100 con Shutdown; hace falta VM.PowerMgmt en /vms/100 y PVEAuditor no lo tiene: aparece Permission check failed (/vms/100, VM.PowerMgmt) y la VM no cambia.",
      [8, 36, 50, 66, 92])
