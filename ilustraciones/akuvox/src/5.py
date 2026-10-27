from _akv import *

# ---------- 5.svg: el portero es una extensión más
c = Canvas("Akuvox · Lección 5", "El portero, una extensión más de la central")
pbx = c.add(Generic(400, 140, "Central SIP", "192.168.88.10 · puerto 5060", icon="server", w=400))
p = c.add(Generic(60, 340, "Portero", "extensión 201", icon="bell", w=250))
m = c.add(Generic(475, 340, "Monitor", "extensión 202", icon="laptop", w=250))
a = c.add(Generic(890, 340, "Celular o interno", "desvío · cola · app", icon="phone", w=250))
c.add(Arrow(p.top(), pbx.bottom(-150), kind="logical", label="registra 201", label_at=0.5, label_dy=-6))
c.add(Arrow(m.top(), pbx.bottom(0), kind="logical", label="registra 202", label_at=0.5, label_dy=-6))
c.add(Arrow(pbx.bottom(150), a.top(), kind="flow", label="desvío", label_at=0.55, label_dy=-6))
c.add(panel(60, 470, 520, 130, "Cuenta 1", "cyan"))
c.add(text(80, 540, "la toma SmartPlus si se activa", 17, 500, INK))
c.add(text(80, 568, "Account > Basic", 15, 500, INK3, FM))
c.add(panel(620, 470, 520, 130, "Cuenta 2", "info"))
c.add(text(640, 540, "libre para la central local", 17, 500, INK))
c.add(text(640, 568, "si la 1 no registra, pasa a la 2", 15, 500, INK3, FM))
save(c, "5.svg")

# ---------- 5-paso3.svg: los campos de Account > Basic
c = Canvas("Akuvox · Lección 5 · Paso 3", "Copiá la extensión de la central al portero")
c.add(panel(48, 150, 360, 250, "En la central", "soft"))
c.add(text(68, 220, "Extensión", 15, 500, INK3))
c.add(text(68, 250, "201", 26, 600, INK, FM))
c.add(text(68, 300, "Contraseña", 15, 500, INK3))
c.add(text(68, 326, "Ejemplo-201-Lab!", 18, 600, INK, FM))
c.add(text(68, 372, "Portero calle", 15, 500, INK3, FM))
c.add(Window(500, 140, 650, 352, "Web del portero", path="Account > Basic",
             rows=[("Account Enabled", "activada"), ("Register Name", "201"), ("Username", "201"),
                   ("Password", "Ejemplo-201-Lab!"), ("Server Address", "192.168.88.10"), ("Port", "5060")], hl=3))
c.add(Step(500, 140, 3))
c.add(Arrow((412, 250), (494, 265), label="201", label_dy=-12))
c.add(Arrow((412, 322), (494, 377)))
c.add(Note(48, 430, 360, "Register Name y Username llevan el mismo número. El monitor, igual con la 202.", kind="info", size=15))
c.add(Note(500, 520, 650, "Server Address es la IP de la central, no la del router. Después: Submit y verificá el registro en la central (paso 5).", kind="warn", size=15))
save(c, "5-paso3.svg")

# ---------- 5-paso7.svg: síntomas y causas
c = Canvas("Akuvox · Lección 5 · Paso 7", "Si no registra, el síntoma te dice dónde mirar")
rows = [("“Failed to authenticate”", "en el log de la central", "contraseña mal", "revisá la Password"),
        ("El registro cambia de puerto", "a cada refresco", "SIP ALG del router", "desactivá SIP ALG"),
        ("Registra pero no llama", "marcaste *202", "prefijo de más", "marcá 202, sin asterisco")]
for i, (s1, s2, cause, fix) in enumerate(rows):
    y = 150 + i * 150
    c.add(f'<rect x="48" y="{y}" width="360" height="110" rx="16" fill="{ALERT_BG}" stroke="{ALERT}" stroke-width="1.5"/>')
    c.add(text(70, y + 44, s1, 18, 600, INK))
    c.add(text(70, y + 72, s2, 15, 500, INK3, FM))
    c.add(Arrow((414, y + 55), (470, y + 55)))
    c.add(f'<rect x="476" y="{y}" width="300" height="110" rx="16" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
    c.add(text(498, y + 34, "CAUSA", 13, 600, INK3, FM, ls=1.5))
    c.add(text(498, y + 68, cause, 19, 600, INK, FD))
    c.add(Arrow((782, y + 55), (838, y + 55), kind="ok"))
    c.add(f'<rect x="844" y="{y}" width="308" height="110" rx="16" fill="{OK_BG}" stroke="{OK}" stroke-width="1.5"/>')
    c.add(text(866, y + 34, "ARREGLO", 13, 600, OK, FM, ls=1.5))
    c.add(text(866, y + 68, fix, 17, 600, INK))
save(c, "5-paso7.svg")
