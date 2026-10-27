from _oai import *


def check(x, y, on=True, col=OK):
    box = f'<rect x="{x}" y="{y - 16}" width="20" height="20" rx="4" fill="{col if on else WHITE}" stroke="{col if on else LINE2}" stroke-width="2"/>'
    if on:
        box += f'<path d="M{x + 4} {y - 6}l4 4l8 -9" stroke="{WHITE}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    return box


# ---------- 3.svg: cuatro pasos hasta que avisa
c = Canvas("OmniAccess Intrusión · Lección 3", "Alta completa: avisa y la ves llegar")
steps = [("1", "Alta", "Dispositivos → Agregar → Cámara de intrusión, o Importar cámaras (clasificar) desde el NVR"),
         ("2", "Servidor de alarma", "Campana del canal → Configurar OmniAccess como alarma → Probar reporte"),
         ("3", "Vinculación", "En la regla de la cámara: Notificar al centro de vigilancia"),
         ("4", "Cruzar la línea", "El canal se pone rojo y la tarjeta llega con foto")]
for i, (n, t, d) in enumerate(steps):
    x = 48 + i * 282
    kd = "ok" if i == 3 else "info"
    c.add(panel(x, 150, 258, 220, None, kind=kd))
    c.add(f'<circle cx="{x + 34}" cy="{184}" r="18" fill="{CYAN if i < 3 else OK}"/>')
    c.add(text(x + 34, 190, n, 18, 700, WHITE, FD, anchor="middle"))
    c.add(text(x + 62, 192, t, 19, 600, INK, FD))
    s, _ = wrap(x + 22, 240, d, 220, 16, 400, INK2)
    c.add(s)
    if i < 3:
        c.add(Arrow((x + 262, 260), (x + 278, 260), kind="flow"))
c.add(Window(48, 430, 560, 170, "Lo que escribe en la cámara · ISAPI httpHosts",
             rows=[("Host 1", "192.0.2.10:10000"), ("URL", "/api/webhooks/hikvision"), ("Formato · Auth", "XML · ninguna")], hl=0))
c.add(Note(640, 430, 512, "Probar reporte puede no confirmar: varias cámaras no implementan el test. La prueba que vale es el paso 4.", title="El test no alcanza", kind="warn", size=15))
save(c, "3.svg")

# ---------- 3-paso1.svg: importar clasificando
c = Canvas("OmniAccess Intrusión · Lección 3 · Paso 1", "Importá del NVR y elegí qué es cada canal")
c.add(Table(48, 150, ["Canal", "Nombre en el NVR", "Marca", "Rol"],
            [["D1", "Acceso Principal Entrada", "HIKVISION", "LPR · entrada"],
             ["D5", "Perímetro Norte 12", "HIKVISION", "intrusión"],
             ["D6", "Perímetro Sur 07", "DAHUA", "intrusión"],
             ["D9", "Quincho interior", "HIKVISION", "omitir"]],
            [120, 400, 220, 364], hl_row=1, row_h=52, mono_cols=(0, 2)))
c.add(Note(48, 440, 540, "Si el nombre habla de matrícula, patente, entrada, salida, acceso o barrera, sugiere LPR; si no, cámara del perímetro.", title="La sugerencia sale del nombre", kind="info", size=15))
c.add(Note(612, 440, 540, "Las creadas así toman usuario y clave del NVR. Si la cámara tiene otra clave, corregila en Editar: sin ella no hay foto propia.", title="Ojo con la clave", kind="warn", size=15))
save(c, "3-paso1.svg")

# ---------- 3-paso5.svg: el tilde de la vinculación
c = Canvas("OmniAccess Intrusión · Lección 3 · Paso 5", "Sin este tilde la cámara detecta y no avisa")
c.add(panel(48, 140, 660, 380, "Web de la cámara · Detección de cruce de línea", kind="info", title_size=17))
c.add(text(72, 200, "Configuración > Evento > Evento inteligente", 15, 500, BLUE, FM))
tabs = ["Área", "Programación de armado", "Método de vinculación"]
tx = 72
for i, tb in enumerate(tabs):
    w = len(tb) * 9.2 + 26
    on = i == 2
    c.add(f'<rect x="{tx}" y="220" width="{w:.0f}" height="34" rx="8" fill="{SOFT if on else WHITE}" stroke="{CYAN if on else LINE2}" stroke-width="{2 if on else 1.5}"/>')
    c.add(text(tx + w / 2, 243, tb, 15, 600 if on else 500, INK if on else INK3, FB, anchor="middle"))
    tx += w + 10
opts = [("Notificar al centro de vigilancia", True, True), ("Grabar (Trigger Recording)", True, False), ("Enviar email", False, False), ("Alarma sonora", False, False)]
for i, (o, on, hl) in enumerate(opts):
    y = 300 + i * 56
    if hl:
        c.add(f'<rect x="64" y="{y - 30}" width="628" height="46" rx="10" fill="{OK_BG}" stroke="{OK}" stroke-width="2"/>')
    c.add(check(84, y, on))
    c.add(text(118, y, o, 17, 600 if hl else 500, INK if hl else INK2))
c.add(Step(48, 140, 5))
c.add(Note(740, 140, 412, "Hikvision solo manda al servidor de alarma los eventos con esta vinculación tildada.", title="Notify Surveillance Center", kind="ok", size=16))
c.add(Note(740, 280, 412, "Cada regla tiene la suya: la detección de intrusión de zona se tilda aparte.", kind="info", size=16))
save(c, "3-paso5.svg")
