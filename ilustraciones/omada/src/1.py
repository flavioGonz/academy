import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 1.svg: tres familias de controlador
c = Canvas(K(), "Tres familias: elegí por dónde corre el servicio")
cols = [
    (48, "Local", "info", Generic(68, 186, "OC200 a OC400", "o Software propio", icon="server", w=312, dark=True),
     ["El servicio corre en tu red.", "Sin internet, se sigue gestionando.", "Host, backups y versiones: tuyos."]),
    (424, "En la nube", "info", CloudBox(444, 186, "Omada Central", "Essentials o Standard", w=312),
     ["Essentials: gratis y sin MSP.", "Standard: una licencia por equipo.", "Sin internet, no hay gestión."]),
    (800, "Gateway integrado", "info", Generic(820, 186, "Fusion · ER7212PC", "router y controlador", icon="server", w=312, dark=True),
     ["El controlador vive en el router.", "ER7212PC V2: hasta 22 SW y EAP.", "Fusion: un sistema, sin multisitio."]),
]
for x, t, kd, dev, ls in cols:
    c.add(panel(x, 124, 352, 300, t, kd))
    c.add(dev)
    c.add(lines(x + 24, 316, ls, 16, 30))
c.add(Note(48, 448, 540, "La red sigue con la última configuración, pero se apagan Portal, Fast Roaming y Schedule hasta renovar.", title="Licencia vencida en Central Standard", kind="warn"))
c.add(Note(612, 448, 540, "Es una puerta remota. El servicio, la configuración y los logs siguen en tu OC, tu servidor o tu gateway.", title="Cloud Access no es controlador en la nube", kind="info"))
c.add(text(48, 628, "Capacidad recomendada: OC200 25 equipos · OC220 40 · OC300 160 · OC400 500", 16, 500, INK2, FM))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso2: cuatro preguntas para elegir
c = Canvas(K(2), "Qué mirar según lo que pide cada obra")
c.add(code(48, 124, 1104, "Obra | Equipos | ¿Sin internet? | ¿Portal? | ¿MSP? | Controlador | Licencias/año", 15))
c.add(Step(48, 124, 2))
c.add(Table(48, 192, ["Si la obra pide", "Mirá"], [
    ["Gestionar sin internet", "OC, Software propio o gateway integrado"],
    ["Varios clientes con MSP", "Software propio o Central Standard"],
    ["Nadie que mantenga un servidor", "OC, Central o Fusion / ER7212PC"],
    ["Cero costo de licencias", "OC, Software, Essentials o gateway integrado"],
    ["Todo en una caja, local chico", "ER7212PC (V2: 22 SW y EAP, 2 gateways)"],
], [430, 674], row_h=44))
c.add(Note(48, 470, 540, "Essentials no tiene modo MSP, y los OC tampoco, según la tabla oficial. Para una cadena con varios clientes, Software propio o Central Standard.", title="El MSP achica la lista", kind="info"))
c.add(Note(612, 470, 540, "Si elegís Central Standard, anotá cuántas licencias, desde cuándo corren y quién las renueva: corren desde que se activan.", title="Licencias con dueño", kind="warn"))
save(c, "1-paso2.svg")

# ---------------------------------------------------------------- 1-paso4: cifra recomendada con margen
c = Canvas(K(4), "Dimensioná por la cifra recomendada, con margen")
models = [("OC200", "25"), ("OC220", "40"), ("OC300", "160"), ("OC400", "500")]
for i, (m, n) in enumerate(models):
    x = 48 + i * 282
    c.add(panel(x, 124, 258, 112, None, "info"))
    c.add(text(x + 22, 166, m, 22, 600, INK, FD))
    c.add(text(x + 22, 210, f"hasta {n} equipos", 17, 500, BLUE, FM))
c.add(text(48, 278, "Ejemplo: obra con 22 equipos entre gateway, switches y EAP", 18, 600, INK, FB))
bars = [("OC200", 25, "warn", "22 de 25: entra, pero sin lugar para crecer"), ("OC220", 40, "ok", "22 de 40: entra y queda margen")]
for i, (m, cap, kd, lab) in enumerate(bars):
    y = 304 + i * 74
    bg, fg = {"warn": (WARN_BG, WARN), "ok": (OK_BG, OK)}[kd]
    c.add(text(48, y + 32, m, 18, 600, INK, FM))
    c.add(rect(150, y + 8, 520, 34, WHITE, LINE2, rx=10))
    w = 520 * 22 / cap
    c.add(rect(150, y + 8, w, 34, bg, fg, rx=10))
    c.add(text(694, y + 32, lab, 16, 500, fg, FB))
c.add(Step(48, 124, 4))
c.add(Note(48, 470, 540, "Una reseña de 2022 citaba el OC200 hasta 100 equipos. La tabla oficial actual recomienda 25: se dimensiona por esa.", title="Cifras viejas y máximas", kind="warn"))
c.add(Note(612, 470, 540, "Software propio: recomendado hasta 10.000. ER7212PC V2: 22 switches y EAP. Fusion: 30 equipos según el modelo.", title="Otras cifras de la tabla oficial", kind="info"))
save(c, "1-paso4.svg")
