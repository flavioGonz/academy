#!/usr/bin/env python3
"""Lección 9 · Resumen, "Cómo se ve en la red": Fast Roaming y los equipos viejos. El SSID con FT lo anuncia; el
celular moderno lo usa; un lector de código viejo no sabe leer ese anuncio y no se conecta; la salida es un SSID de
legado sin FT, WPA2 sin PMF obligatorio, en su propia VLAN. Fuentes: idea_md, theory_md y lab.md de la lección;
Purple ("some older drivers cannot parse the FT information that the AP advertises"; lectores en 9 tiendas)."""
from _anim_red_unifi import *  # noqa

a = new(26, "Roaming sin magia", "Fast Roaming y los equipos viejos: un SSID aparte", [
    "El SSID Prueba-FT anuncia Fast Roaming (802.11r) junto con su seguridad.",
    "El celular entiende el anuncio, se conecta y en cada roam usa FT.",
    "El lector viejo no sabe leer lo que anuncia el SSID con FT: no se conecta.",
    "SSID de legado sin FT, WPA2 sin PMF obligatorio, en su VLAN: el lector entra.",
], still=3)

AX, AY = 470, 196
a.add(a.box(AX, AY, 300, 210, a.WHITE, a.LINE, rx=14))
a.add(ap_icon(a, AX + 42, AY + 44, 22))
a.add(a.text(AX + 80, AY + 40, "AP", 20, a.INK, a.HEAD, 600))
a.add(a.text(AX + 80, AY + 66, "dos SSID", 15, a.GREY, a.MONO))
a.add(a.text(AX + 80, AY + 90, "en el mismo AP", 15, a.GREY, a.MONO))

S1 = (a.box(880, 186, 272, 124, a.WHITE, a.BLUE, rx=14, sw=2.5) + a.text(900, 216, "Prueba-FT · Staff", 17, a.INK, a.SANS, 600)
      + a.text(900, 244, "Fast Roaming: On", 15, a.BLUE, a.MONO, 600) + a.text(900, 268, "BSS Transition: On", 15, a.TXT, a.MONO)
      + a.text(900, 292, "WPA2/WPA3", 15, a.TXT, a.MONO))
a.add(S1)
S2 = (a.box(880, 330, 272, 124, a.WHITE, a.OK, rx=14, sw=2.5) + a.text(900, 360, "Legado · VLAN propia", 17, a.INK, a.SANS, 600)
      + a.text(900, 388, "Fast Roaming: Off", 15, a.OK, a.MONO, 600) + a.text(900, 412, "WPA2, sin PMF", 15, a.TXT, a.MONO)
      + a.text(900, 436, "obligatorio", 15, a.TXT, a.MONO))
vis(a, S2, 3)
a.add(wire(770, 248, 880, 248, a.BLUE, 3, "6 6"))
vis(a, poly([(770, 360), (825, 360), (825, 392), (880, 392)], a.OK, 3, "6 6"), 3)

a.add(dev(a, 48, 186, 270, 90, "Celular", "WPA3 y FT", icon="phone"))
a.add(dev(a, 48, 330, 270, 90, "Lector de códigos", "driver viejo", icon="card"))
a.add(wire(318, 231, AX, 231, a.LINE, 2.5, "4 6"))
a.add(wire(318, 375, AX, 375, a.LINE, 2.5, "4 6"))

# 1 · anuncio
s0, s1 = ph(a, 0)
for k in range(3):
    t = s0 + 2 + k * 7
    go(a, [(AX - 60, 231), (394, 231)], t, t + 4, "beacon: FT", a.BLUE, hold=t + 4.4)
    go(a, [(AX - 60, 375), (394, 375)], t + 1, t + 5, "beacon: FT", a.BLUE, hold=t + 5.4)

# 2 · celular OK
s0, s1 = ph(a, 1)
go(a, [(380, 231), (AX - 64, 231)], s0 + 3, s0 + 7, "se conecta", a.OK, hold=s0 + 8)
during(a, check(a, 300, 186, 15), s0 + 7, 100, still=1)
during(a, pill(a, 48, 290, "roam con FT: pocas tramas", "ok"), s0 + 9, ph(a, 2)[1])

# 3 · lector no entiende
s0, s1 = ph(a, 2)
go(a, [(AX - 60, 375), (394, 375)], s0 + 2, s0 + 6, "beacon: FT", a.BLUE, hold=s0 + 7)
during(a, a.box(48, 434, 210, 40, a.BADBG, None, rx=10) + a.text(153, 460, "¿qué es esto?", 16, a.BAD, a.SANS, 600, "middle"), s0 + 6, s1)
during(a, xmark(a, 300, 330, 15), s0 + 7, s1)
during(a, nbox(a, 420, 470, 732, 110, "Caso de Purple", ["Al activar Fast Roaming en todos los SSID, lectores con firmware viejo", "dejaron de conectar en 9 tiendas. Es un bloqueo, no un equipo pegajoso."], "bad"),
       s0 + 4, s1)

# 4 · SSID de legado
s0, s1 = ph(a, 3)
go(a, [(380, 375), (AX - 64, 375)], s0 + 3, s0 + 7, "se conecta", a.OK, hold=s0 + 8)
during(a, check(a, 300, 330, 15), s0 + 7, 100, still=1)
during(a, pill(a, 48, 434, "en Legado, su VLAN", "ok"), s0 + 8, 100, still=1)
during(a, nbox(a, 420, 470, 732, 110, "No apagues FT para todos", ["Lo que no tolera FT o PMF va a un SSID de legado en su propia VLAN,", "sin acceso a los sistemas del staff."], "ok"),
       s0 + 4, 100, still=1)

status(a, 628, [
    (0, 25, "En UniFi, Fast Roaming es 802.11r y BSS Transition es 802.11v.", a.INK, 0),
    (25, 50, "Con FT, el cambio de AP se completa con claves derivadas por adelantado.", a.OK, 0),
    (50, 75, "Activarlo en producción puede dejar afuera a equipos viejos de golpe.", a.BAD, 0),
    (75, 100, "Primero un SSID de prueba con un equipo de cada tipo; lo que falla, aparte.", a.OK, 1),
])

write(a, 9, "r1", "Fast Roaming y los equipos viejos",
      "Animación en cuatro tiempos con un AP, el SSID Prueba-FT en la red Staff (Fast Roaming On, BSS Transition On, WPA2/WPA3), un celular moderno y un lector de códigos con driver viejo. "
      "1: el SSID Prueba-FT anuncia Fast Roaming, 802.11r, junto con su seguridad, y el anuncio les llega a los dos equipos. "
      "2: el celular entiende el anuncio y se conecta; en cada roam usa FT y el cambio se completa en pocas tramas. "
      "3: el lector viejo no sabe leer lo que anuncia un SSID con FT y no se conecta; en el caso de Purple, lectores con firmware viejo dejaron de conectar en 9 tiendas. "
      "4: se crea un SSID de legado en su propia VLAN, con Fast Roaming Off y WPA2 sin PMF obligatorio; el lector entra y no tiene acceso a los sistemas del staff. "
      "No se apaga FT para todos.",
      [12, 40, 64, 92])
