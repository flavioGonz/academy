import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 5.svg: perfil y regla
c = Canvas(K(), "Cada placa cae en un perfil; la regla actúa en el suyo")
c.add(NOLIG)
profs = [("Dominio", "unida a Active Directory", "info"), ("Privado", "una red tuya, de confianza", "ok"), ("Público", "cualquier red ajena", "warn")]
for i, (t, s, kd) in enumerate(profs):
    x = 48 + i * 372
    c.add(panel(x, 128, 352, 120, t, kd if kd != "info" else "soft"))
    c.add(text(x + 20, 202, s, 16, 400, INK2, FB))
    c.add(text(x + 20, 228, "entra: bloqueado salvo regla", 15, 500, INK3, FM))
c.add(text(48, 290, "La regla 'LAB VMS web 8443' tiene -Profile Private,Domain", 18, 600, INK, FB))
c.add(panel(48, 312, 540, 150, None, "ok"))
c.add(Mark(86, 352, ok=True))
c.add(text(118, 359, "Placa en Privado", 20, 600, OK, FD))
svg, _ = wrap(72, 400, "Su perfil está activo: la regla actúa y el 8443 entra desde la subred local.", 490, 16, 400, INK2)
c.add(svg)
c.add(panel(612, 312, 540, 150, None, "alert"))
c.add(Mark(650, 352, ok=False))
c.add(text(682, 359, "Placa en Público", 20, 600, ALERT, FD))
svg, _ = wrap(636, 400, "La regla existe pero no actúa: para esa placa, es como si no estuviera. El 8443 queda bloqueado.", 490, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 492, 1104, "Antes de crear nada, mirá el perfil con Get-NetConnectionProfile. Después abrí por puerto o por programa, con origen limitado, y exportá la configuración antes de tocar.", title="Perfil primero, regla después", kind="info"))
save(c, "5.svg")

# ---------------------------------------------------------------- 5-paso4: anatomía de la regla
c = Canvas(K(4), "Una regla dice qué entra, desde dónde y cuándo")
c.add(NOLIG)
c.add(Step(65, 141, 4))
c.add(text(94, 147, "New-NetFirewallRule -DisplayName 'LAB VMS web 8443' …", 17, 600, INK2, FM))
parts = [("-Direction Inbound -Action Allow", "Qué hace", "permite lo que entra", "info"),
         ("-Protocol TCP -LocalPort 8443", "Qué abre", "un puerto concreto, no todo", "info"),
         ("-RemoteAddress LocalSubnet", "Desde dónde", "solo la subred local del equipo", "ok"),
         ("-Profile Private,Domain", "Cuándo", "solo con esos perfiles activos", "warn")]
for i, (p, t, s, kd) in enumerate(parts):
    y = 180 + i * 92
    c.add(code(48, y, 560, p, 16, h=60))
    c.add(arrow((614, y + 30), (660, y + 30), "flow"))
    c.add(panel(668, y, 484, 76, None, {"info": "info", "ok": "ok", "warn": "warn"}[kd]))
    c.add(text(690, y + 32, t, 18, 600, {"info": INK, "ok": OK, "warn": WARN}[kd], FD))
    c.add(text(690, y + 58, s, 16, 400, INK2, FB))
c.add(Note(48, 556, 1104, "Para una regla por programa, en vez de puerto va -Program con la ruta completa del ejecutable. Nunca \"todo a todos\".", kind="info"))
save(c, "5-paso4.svg")

# ---------------------------------------------------------------- 5-paso5: ver qué abre de verdad
c = Canvas(K(5), "La regla sola no muestra puertos: pedí sus filtros")
c.add(NOLIG)
c.add(Step(65, 141, 5))
c.add(text(94, 147, "Get-NetFirewallRule muestra nombre, estado y perfil, no puertos ni IP", 17, 600, INK2, FB))
sv, h = console(48, 170, 1104, [
    ">Get-NetFirewallRule -DisplayName 'LAB VMS web 8443'",
    ("DisplayName : LAB VMS web 8443    Enabled : True    Profile : Private, Domain", "#D9E9F8"),
    ("(sin puerto ni dirección)", "#FFB020"),
])
c.add(sv)
sv, h2 = console(48, 340, 540, [
    ">… | Get-NetFirewallPortFilter",
    ("Protocol  : TCP", "#D9E9F8"),
    ("LocalPort : 8443", "#9FE3F7"),
])
c.add(sv)
sv, h3 = console(612, 340, 540, [
    ">… | Get-NetFirewallAddressFilter",
    ("RemoteAddress : LocalSubnet", "#9FE3F7"),
    ("LocalAddress  : Any", "#D9E9F8"),
])
c.add(sv)
c.add(Note(48, 510, 1104, "Así se audita un servidor que ya tiene reglas: por cada regla, sus filtros de puerto y de dirección. Al terminar el laboratorio, Remove-NetFirewallRule con el mismo nombre.", kind="info"))
save(c, "5-paso5.svg")
