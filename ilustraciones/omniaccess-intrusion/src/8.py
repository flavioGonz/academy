from _oai import *


def tarjeta(x, y, w, h, cam, hora, estado_txt, kd, night=True):
    out = [frame(x, y, w, h, None, night=night)]
    out.append(f'<rect x="{x}" y="{y + h - 50}" width="{w}" height="50" rx="0" fill="#000" opacity=".45"/>')
    out.append(text(x + 14, y + h - 28, cam, 14, 600, WHITE, FB))
    out.append(text(x + 14, y + h - 10, hora, 13, 500, "#C9D6E2", FM))
    out.append(tag(x + w - 12, y + 32, estado_txt, kd, 13, anchor="start") if False else tag(x + w - 100, y + 30, estado_txt, kd, 13))
    return "".join(out)


# ---------- 8.svg
c = Canvas("OmniAccess Intrusión · Lección 8", "Cada detección termina Real o Falsa, nunca Pendiente")
c.add(panel(48, 140, 230, 400, "Filtros", kind="info"))
flt = [("Cámara", "Perímetro Norte 12"), ("Estado", "Pendientes"), ("Desde", "anoche 22:00"), ("Hasta", "hoy 06:00")]
for i, (k, v) in enumerate(flt):
    y = 200 + i * 76
    c.add(text(68, y, k.upper(), 12, 600, INK3, FM, ls=1.2))
    c.add(f'<rect x="68" y="{y + 10}" width="190" height="36" rx="8" fill="{SOFT}"/>')
    c.add(text(80, y + 34, v, 14, 500, INK, FB))
cards = [("Perímetro Norte 12", "02:11", "Pendiente", "warn"), ("Perímetro Norte 12", "03:40", "Real", "alert"),
         ("Perímetro Norte 12", "04:05", "Falsa", "gray"), ("Perímetro Sur 07", "04:06", "Pendiente", "warn")]
for i, (cm, h, st, kd) in enumerate(cards):
    x = 310 + (i % 2) * 290
    y = 140 + (i // 2) * 205
    c.add(tarjeta(x, y, 270, 185, cm, h, st, kd))
c.add(panel(900, 140, 252, 400, "Corregir una", kind="ok", sub="ficha de la detección"))
s, _ = bullet_list(920, 230, [("Pendiente → Falsa alarma o Fue real", "warn"), ("Real → Era falsa alarma", "alert"), ("Falsa → Era real", "info")], 220, 15, 14)
c.add(s)
c.add(Note(920, 400, 212, "Solo esa detección: las demás de la cámara no se tocan.", kind="info", size=14))
c.add(Note(48, 560, 1104, "Las fotos viven en el bucket intrusion con la retención de Configuración → Almacenamiento. Bajarla borra lo viejo para siempre.", kind="warn", size=15))
save(c, "8.svg")

# ---------- 8-paso6.svg: el guardia más cercano
c = Canvas("OmniAccess Intrusión · Lección 8 · Paso 6", "Mandá al guardia más cercano, con cuatro datos")
c.add('<rect x="48" y="140" width="660" height="440" rx="16" fill="#25352A"/>')
c.add('<path d="M48 380H708" stroke="#55626B" stroke-width="24"/>')
c.add('<path d="M380 140V580" stroke="#55626B" stroke-width="20"/>')
c.add('<path d="M60 162H696" stroke="#8FA3B5" stroke-width="3" stroke-dasharray="10 6"/>')
c.add('<path d="M430 170L620 170" stroke="#ef4444" stroke-width="8" stroke-linecap="round"/>')
c.add(text(525, 200, "Perímetro Norte 12", 15, 700, "#FFB4B4", FB, anchor="middle"))
guards = [(300, 280, "Guardia 1", True), (150, 500, "Guardia 2", False), (540, 520, "Guardia 3", False)]
for x, y, n, near in guards:
    c.add(f'<circle cx="{x}" cy="{y}" r="15" fill="{OK if near else "#94A3B8"}" stroke="#fff" stroke-width="3"/>')
    c.add(text(x + 22, y + 6, n, 15, 600, WHITE, FB))
c.add(f'<path d="M312 268L432 184" stroke="{OK}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-ok)"/>')
c.add(Step(250, 280, 6))
c.add(panel(740, 140, 412, 290, "Por radio", kind="ok", sub="posición cada 10 s en el Mapa"))
msg = ["Cámara: Perímetro Norte 12", "Lugar: cerco norte, entre lotes 14 y 16", "Qué se vio: una persona cruzando", "Hace cuánto: 40 segundos"]
for i, m in enumerate(msg):
    y = 232 + i * 52
    c.add(f'<circle cx="772" cy="{y - 6}" r="13" fill="{OK}"/>')
    c.add(text(772, y - 1, str(i + 1), 14, 700, WHITE, FD, anchor="middle"))
    c.add(text(796, y, m, 16, 500, INK))
c.add(Note(740, 450, 412, "La tablet del guardia no recibe la intrusión en esta versión: el puesto avisa.", kind="warn", size=15))
save(c, "8-paso6.svg")
