from _akv import *

# ---------- 14.svg: los modos de la HTTP API
c = Canvas("Akuvox", "¿Quién puede hablarle a la HTTP API?")
c.add(text(48, 146, "Setting > HTTP API · Authorization Mode", 16, 600, BLUE, FM))
modes = [("None", "alert", "nadie se autentica", "solo mesa de laboratorio"),
         ("Allowlist", "ok", "solo las IP de la lista", "red local: cámara LPR, central"),
         ("Basic", "warn", "usuario y clave en Base64", "viaja en claro: evitalo"),
         ("Digest", "ok", "la clave no viaja en claro", "integraciones con usuario propio"),
         ("Normal", "gray", "reservado", "uso interno de Akuvox")]
for i, (name, kd, what, when) in enumerate(modes):
    y = 168 + i * 88
    bg, fg = KC[kd] if kd != "gray" else (WHITE, INK3)
    c.add(f'<rect x="48" y="{y}" width="1104" height="76" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
    c.add(f'<rect x="48" y="{y + 12}" width="6" height="52" rx="3" fill="{fg}"/>')
    c.add(text(78, y + 46, name, 22, 600, INK, FD))
    c.add(text(280, y + 46, what, 17, 500, INK2))
    c.add(text(640, y + 46, when, 17, 500, fg if kd != "gray" else INK3))
    if kd in ("ok", "alert"):
        c.add(Mark(1110, y + 38, ok=kd == "ok"))
    elif kd == "warn":
        c.add(icon(1096, y + 24, "warn", WARN, 1.15, 2))
save(c, "14.svg")

# ---------- 14-paso1.svg: Digest con usuario propio
c = Canvas("Akuvox · Paso 1", "HTTP API en Digest con un usuario que no es admin")
c.add(Window(48, 140, 540, 290, "Web del portero", path="Setting > HTTP API",
             rows=[("HTTP API", "Enabled"), ("Authorization Mode", "Digest"), ("Username", "api-lab"), ("Password", "Ejemplo-Api-2026")], hl=1))
c.add(Step(48, 140, 1))
c.add(Terminal(630, 140, 522, ["auth = AuthConfig(", "\u00a0\u00a0method=AuthMethod.DIGEST,", "\u00a0\u00a0username=\"api-lab\",", "\u00a0\u00a0password=\"Ejemplo-Api-2026\")", ("# paso 2: pylocal-akuvox, misma VLAN", "#7FA6C9")], title="SCRIPT DE PRUEBA"))
c.add(Note(48, 470, 540, "Con Digest la clave no viaja en claro: el equipo la verifica sin que pase por la red tal cual.", title="Por qué Digest", kind="ok", size=15))
c.add(Note(630, 470, 522, "Cambiá la clave del script por una mala: tiene que dar error de autenticación (paso 3).", kind="info", size=15))
save(c, "14-paso1.svg")

# ---------- 14-paso4.svg: una credencial por integración
c = Canvas("Akuvox · Paso 4", "Un usuario por integración: se cambia de a uno")
po = c.add(Intercom(1000, 170, "Portero", "VLAN porteros"))
ints = [("Home Assistant", "10.10.40.5", "ha-porton", "Open Relay via HTTP", True),
        ("Central", "10.10.20.10", "pbx-porton", "Open Relay via HTTP", False),
        ("Cámara LPR", "10.10.30.21", "lpr-porton", "HTTP API · Allowlist", False)]
for i, (name, ip, user, mech, revoked) in enumerate(ints):
    y = 150 + i * 150
    c.add(Generic(48, y, name, ip, icon="server" if i == 1 else ("camera" if i == 2 else "laptop"), w=280, hl=ALERT if revoked else OK))
    c.add(Chip(360, y + 36, user, "alert" if revoked else "ok"))
    c.add(text(360, y + 70, mech, 15, 500, INK3, FM))
    c.add(Arrow((560, y + 42), (990, 220 + i * 50), kind="alert" if revoked else "ok"))
    if revoked:
        c.add(Mark(770, y + 62, ok=False))
c.add(Note(48, 590 - 30, 900, "Se va el integrador de Home Assistant: cambiás solo ha-porton. La central y la cámara siguen abriendo.", kind="info", size=16))
save(c, "14-paso4.svg")
