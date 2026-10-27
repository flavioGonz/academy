import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 11.svg: capas de defensa
c = Canvas(K(), "Cada capa frena lo que la anterior dejó pasar")
c.add(Generic(48, 150, "Barrido", "INVITE, REGISTER", icon="globe", w=216, hl=ALERT))
c.add(text(60, 270, "varios intentos", 15, 500, ALERT, FB))
c.add(text(60, 292, "por segundo", 15, 500, ALERT, FB))
capas = [("Router", "shield", ["solo puertos con", "nombre y motivo"]),
         ("Geo-IP", "globe", ["solo los países", "que usás"]),
         ("Fail2ban", "lock", ["600 s de baneo", "tras intentos fallidos"]),
         ("Administración", "key", ["lista blanca web,", "sin 80 ni 443,", "SSH y AMI apagados"]),
         ("Rutas", "phone", ["privilegio y PIN:", "si entran, no", "llaman afuera"])]
for i, (t, ic, ls) in enumerate(capas):
    x = 280 + i * 176
    c.add(f'<rect x="{x}" y="130" width="160" height="380" rx="16" fill="{WHITE if i < 4 else OK_BG}" stroke="{BLUE if i < 4 else OK}" stroke-width="2"/>')
    c.add(icon(x + 62, 150, ic, BLUE if i < 4 else OK, 1.5))
    c.add(text(x + 80, 222, t, 17, 600, INK, FD, anchor="middle"))
    for k, l in enumerate(ls):
        c.add(text(x + 80, 256 + k * 22, l, 14, 500, INK2, FB, anchor="middle"))
c.add(f'<path d="M256 418L1128 438L1128 442L256 462z" fill="{ALERT}" opacity=".35"/>')
c.add(f'<path d="M256 418L1128 438M256 462L1128 442" stroke="{ALERT}" stroke-width="1.5" fill="none"/>')
c.add(text(60, 430, "lo que sigue", 15, 600, ALERT, FB))
c.add(text(60, 452, "pasando, capa", 15, 600, ALERT, FB))
c.add(text(60, 474, "tras capa", 15, 600, ALERT, FB))
c.add(Note(48, 540, 1104, "Ninguna capa sola alcanza. Un administrador de Wazo vio varios INVITE maliciosos por segundo y juntó más de 50 IPs en sus primeros baneos: por eso Fail2ban mira y las rutas caras piden PIN igual.", kind="info", size=16))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso1: Fail2ban y la Allowlist
c = Canvas(K(1), "Fail2ban banea al que prueba; tu IP va en la Allowlist")
c.add(Generic(48, 150, "198.51.100.66", "REGISTER fallidos", icon="globe", w=330, hl=ALERT))
c.add(Generic(48, 330, "Oficina técnica", "198.51.100.20 · Allowlist", icon="user", w=330, hl=OK))
c.add(Generic(560, 240, "UCM", "Fail2Ban activo", icon="server", w=250, dark=True))
c.add(arrow((382, 192), (552, 270), kind="alert", label="intento tras intento", label_at=0.45, label_dy=-14))
c.add(arrow((382, 372), (552, 302), kind="ok", label="soporte", label_at=0.5, label_dy=24))
c.add(Chip(830, 268, ".66 baneada 600 s", "alert", mono=False))
c.add(Chip(830, 316, ".20 nunca se banea", "ok", mono=False))
c.add(Window(48, 452, 700, 180, "UCM · web", path="System Settings > Security Settings > Fail2Ban", rows=[("Banned Duration", "600 (o más)"), ("Allowlist", "192.168.88.0/24, 198.51.100.20")], hl=1))
c.add(Step(48, 452, 1))
c.add(Note(780, 452, 372, "SIP Defense mira REGISTER, INVITE y SUBSCRIBE fallidos; Login Attack Defense, los ingresos a la web.", kind="info", size=15))
save(c, "11-paso1.svg")

# ---------------------------------------------------------------- 11-paso2: acceso web cerrado
c = Canvas(K(2), "La web solo para la red local y la oficina técnica")
c.add(Window(48, 132, 560, 250, "UCM · web", path="System Settings > HTTP Server", rows=[("Redirect From Port 80", "No"), ("Port", "8089 (nunca 80 ni 443)"), ("Enable IP Address Whitelist", "Sí"), ("Lista (hasta 10 IPs)", "red local y oficina")], hl=2))
c.add(Step(48, 132, 2))
quien = [("Red local 192.168.88.0/24", True), ("Oficina técnica 198.51.100.20", True), ("Cualquier otra IP de internet", False)]
for i, (q, ok) in enumerate(quien):
    y = 170 + i * 76
    c.add(Mark(670, y, ok=ok))
    c.add(text(702, y + 6, q, 17, 600, OK if ok else ALERT, FB))
    c.add(text(702, y + 30, "ve la página de login" if ok else "ni siquiera ve el login", 15, 500, INK3, FB))
c.add(Note(48, 420, 1104, "Si activás la lista blanca o Geo-IP en remoto sin incluir tu propia IP, te quedás afuera de la central. Agregala primero, guardá, y recién después activá.", title="Antes de guardar", kind="alert", size=16))
c.add(Note(48, 548, 1104, "SSH viene apagado y así se queda; GDMS Remote SSH, encendido solo durante un soporte. AMI no se habilita en una central expuesta.", kind="info", size=16))
save(c, "11-paso2.svg")

# ---------------------------------------------------------------- 11-paso5: tabla de puertos del router
c = Canvas(K(5), "Cada puerto abierto con nombre, motivo y quién lo pidió")
c.add(Table(48, 140, ["Puerto", "Destino", "Motivo", "Pedido por", "Queda"],
            [["UDP 5060", "UCM", "internos remotos", "gerencia", "abierto"],
             ["UDP 10000-20000", "UCM", "audio de remotos", "gerencia", "abierto"],
             ["TCP 8089", "UCM", "sin motivo", "nadie sabe", "se cierra"],
             ["TCP 22", "UCM", "sin motivo", "nadie sabe", "se cierra"]],
            [230, 140, 260, 220, 154], row_h=52, mono_cols=(0,)))
for i, ok in enumerate([True, True, False, False]):
    c.add(Mark(1120, 140 + 52 * (i + 1) + 26, ok=ok))
c.add(Step(48, 140, 5))
c.add(Note(48, 430, 540, "La administración se hace desde la red local o la oficina técnica, nunca con la web publicada en internet.", kind="info", size=16))
c.add(Note(612, 430, 540, "Los puertos que quedan abiertos tienen Fail2ban mirando y, si hay remotos, Geo-IP con los países que usás.", kind="ok", size=16))
save(c, "11-paso5.svg")
