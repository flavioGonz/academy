#!/usr/bin/env python3
"""Lección 3 · Resumen, "Cómo se ve en la red": qué puerto usa cada momento de la adopción.
UDP 29810 para el anuncio y la respuesta; TCP 29814 (firmware v5) o 29811/29812 (v4) para adoptar y gestionar;
29815 y 29816 desde la 5.9; 29817 desde la 6.0. Todos son puertos del controlador."""
from _anim_om_red import *

a = nueva(26, "ADOPCIÓN LIMPIA", "La adopción en el cable: un puerto para cada cosa")
F = a.steps([
    "El EAP de fábrica toma IP por DHCP y se presenta por broadcast al UDP 29810.",
    "El controlador escucha el 29810 y responde por el mismo puerto: el EAP queda Pending.",
    "Adopt: la adopción y la gestión van por TCP 29814 y la Device Account reemplaza admin/admin.",
    "Ya Connected, el equipo también usa el 29815, el 29816 y, en el controlador 6, el 29817.",
], still=3)

XE, XC = 170, 760
a.add(dev(a, 48, 172, 244, 58, "EAP de fábrica", icon="wifi"))
a.add(dev(a, 638, 172, 244, 58, "Controlador", icon="server", dark=True))
a.add(lifeline(a, XE, 230, 566) + lifeline(a, XC, 230, 566))
at(a, chip(a, XE, 240, "IP por DHCP", a.INK, a.SLATE, anchor="middle"), 2, 100, still=1)

msg(a, XE, XC, 296, "broadcast · UDP 29810", 4, color=a.AMB, dash="7 6")
msg(a, XC, XE, 350, "respuesta · UDP 29810", 29, color=a.OK)
msg(a, XE, XC, 410, "TCP 29814 · adopción y gestión", 54, color=a.BLUE)
at(a, a.text((XE + XC) / 2, 436, "con firmware de la época del 4: TCP 29811/29812", 15, a.GREY, a.SANS, 400, "middle"), 57, 100, still=1)
msg(a, XE, XC, 486, "TCP 29815 · info, capturas, DPI (5.9)", 78, color=a.CYAN, lsize=15)
msg(a, XE, XC, 524, "TCP 29816 · terminal remota (5.9)", 82, color=a.CYAN, lsize=15)
msg(a, XE, XC, 562, "TCP 29817 · monitoreo (6.0)", 86, color=a.NAVY2, lsize=15)

# panel de estado
PX, PY, PW = 900, 172, 252
a.add(a.box(PX, PY, PW, 220, a.WHITE, a.LINE, rx=16))
a.add(a.text(PX + 20, PY + 32, "En Devices", 16, a.GREY, a.SANS, 600))
at(a, a.text(PX + 20, PY + 72, "(todavía nada)", 17, a.GREY, a.SANS, 600), 0, 30)
at(a, chip(a, PX + 20, PY + 50, "Pending", a.AMB, a.AMBBG, stroke=a.AMB), 31, 62)
at(a, chip(a, PX + 20, PY + 50, "Connected", a.OK, a.OKBG, stroke=a.OK), 62, 100, still=1)
a.add(a.text(PX + 20, PY + 124, "Credenciales del EAP", 16, a.GREY, a.SANS, 600))
at(a, a.text(PX + 20, PY + 158, "admin / admin", 17, a.INK, a.MONO, 600) + a.text(PX + 20, PY + 186, "de fábrica", 15, a.GREY, a.SANS), 0, 60)
at(a, a.text(PX + 20, PY + 158, "Device Account", 17, a.OK, a.MONO, 600) + a.text(PX + 20, PY + 186, "las del sitio", 15, a.GREY, a.SANS), 60, 100, still=1)

at(a, note(a, PX, 412, PW, 156, "Puertos del controlador", ["Su firewall, o el NAT", "de adelante, deja pasar", "UDP 29810 y", "TCP 29811 a 29817."], "amb"), 76, 100, still=1)
at(a, note(a, PX, 412, PW, 156, "El broadcast", ["no cruza routers: solo", "sirve si el EAP y el", "controlador están en la", "misma VLAN."], "info"), 0, 50)
at(a, note(a, PX, 412, PW, 156, "Desde acá", ["la web local del EAP", "deja de mandar: la", "configuración llega del", "controlador."], "ok"), 50, 76)

status(a, 628, [
    (0, 25, "El EAP no sabe dónde está el controlador: pregunta a toda su subred.", a.INK, 0),
    (25, 50, "Si nunca aparece en Pending, el anuncio no llegó: otra VLAN, otra subred o un firewall.", a.INK, 0),
    (50, 75, "El controlador le carga la configuración del sitio y sus propias credenciales.", a.INK, 0),
    (75, 100, "Con controlador software en una PC, el firewall o el antivirus es sospechoso habitual.", a.AMB, 1),
], x=48, anchor="start", size=16)

write(a, 3, "r1", "Los puertos de cada momento de la adopción en Omada",
      "Diagrama de mensajes animado entre un EAP de fábrica y el controlador, con un panel del estado en Devices y de las credenciales del EAP. "
      "1: el EAP toma IP por DHCP y se presenta por broadcast al UDP 29810; el broadcast no cruza routers, así que solo sirve en la misma VLAN. "
      "2: el controlador escucha el 29810 y responde por el mismo puerto; el EAP aparece en Pending. "
      "3: con Adopt, la adopción y la gestión van por TCP 29814 (con firmware de la época del controlador 4, por TCP 29811 y 29812); "
      "el equipo pasa a Connected y la Device Account del sitio reemplaza las credenciales de fábrica admin/admin. "
      "4: ya conectado, el equipo usa también TCP 29815 para información, capturas y estadísticas DPI y TCP 29816 para la terminal remota, los dos desde la 5.9, "
      "y TCP 29817 para los datos de monitoreo desde el controlador 6. Todos son puertos del controlador: su firewall o el NAT de adelante tienen que dejar pasar UDP 29810 y TCP 29811 a 29817.",
      [8, 38, 60, 72, 92])
