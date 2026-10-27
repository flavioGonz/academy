from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Mapa del software: nube y celular, o PC y local")
c.add(Zone(40, 150, 540, 340, "nube y celular", CYAN))
c.add(card(70, 190, 480, 130, "SmartPlus App", "Residente: ve, habla, abre y da llaves virtuales. Trabaja con la nube de Akuvox."))
c.add(card(70, 335, 480, 130, "My MobileKey", "Credencial Bluetooth con AES256: abre acercando la mano o con un botón. Se integra con ACMS."))
c.add(Zone(620, 150, 540, 340, "PC o servidor local", BLUE))
c.add(card(650, 190, 230, 130, "ACMS", "Acceso en PC para pymes."))
c.add(card(900, 190, 230, 130, "ACMS Pro", "Empresa: estado de puertas, grupos, varios puestos."))
c.add(card(650, 335, 480, 130, "SDMC", "Gestión local de comunidades: despliegue por lotes, video, acceso y mensajes."))
c.add(card(40, 520, 1120, 110, "Installer Kit Tool", "Sobre hardware S563W con PoE y Wi-Fi: junta la red de los equipos y sube el proyecto a la nube.", kind="dark"))
c.save(out("40.svg"))

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "El bloque B del firmware dice qué versión tenés")
vals = ["567", "30", "12", "802"]
names = ["A · modelo", "B · OEM", "C · rama", "D · número"]
for j, v in enumerate(vals):
    x = 120 + j * 250
    hl = j == 1
    c.add(f'<rect x="{x}" y="150" width="190" height="70" rx="14" fill="{SOFT if hl else WHITE}" stroke="{CYAN if hl else LINE2}" stroke-width="{3 if hl else 2}"/>')
    c.add(text(x + 95, 196, v, 28, 600, INK, FM, anchor="middle"))
    c.add(text(x + 95, 250, names[j], 15, 600 if hl else 500, CYAN if hl else INK3, FM, anchor="middle"))
    if j < 3:
        c.add(text(x + 220, 200, ".", 32, 700, INK3, FM, anchor="middle"))
c.add(Label(120, 290, "Ejemplo: 567.30.12.802, el mínimo del S567 para relés externos.", 15, 500, INK3))
rows = [(True, "B = 30", "versión Akuvox: nube, SDMC y modo descubrimiento"),
        (True, "B = 31", "sin logo, mismas funciones"),
        (False, "otro", "versión a medida: consultá antes de integrarla")]
for i, (ok, k, s) in enumerate(rows):
    y = 360 + i * 70
    c.add(f'<rect x="120" y="{y - 30}" width="960" height="56" rx="12" fill="{OK_BG if ok else WARN_BG}"/>')
    c.add(Mark(152, y - 2, ok) if ok else f'<g transform="translate(140 {y - 14})" fill="none" stroke="{WARN}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICON["warn"]}</g>')
    c.add(text(190, y + 4, k, 18, 600, INK, FM))
    c.add(text(320, y + 4, s, 17, 500, INK2, FB))
c.add(Label(120, 600, "Dónde se lee: Status > Basic > Product Information.", 16, 500, INK2, FM))
c.save(out("40-paso2.svg"))

# ---------------------------------------------------------------- paso 3
c = Canvas(K + " · Paso 3", "Un equipo, un administrador")
c.add(Zone(40, 150, 540, 420, "dos fuentes de verdad", ALERT))
n1 = c.add(CloudBox(70, 190, "Nube", "SmartPlus", w=220))
s1 = c.add(Server(330, 190, "SDMC", "local", w=220))
e1 = c.add(Generic(190, 400, "Monitor", "¿quién manda?", icon="laptop", w=220))
c.add(Arrow(n1.bottom(), e1.top(-40), kind="alert"))
c.add(Arrow(s1.bottom(), e1.top(40), kind="alert"))
c.add(Mark(450, 442, False))
c.add(Zone(620, 150, 540, 420, "uno solo, anotado en la ficha", OK))
s2 = c.add(Server(780, 190, "SDMC", "local", w=220))
e2 = c.add(Generic(780, 400, "Monitor", "lo administra el SDMC", icon="laptop", w=260))
c.add(Arrow(s2.bottom(), e2.top(-20), kind="ok"))
c.add(Mark(1080, 442, True))
c.add(Note(40, 590, 1120, "Elegí uno por equipo y anotalo en la ficha de la obra: así el próximo técnico sabe dónde tocar.", kind="info"))
c.save(out("40-paso3.svg"))
