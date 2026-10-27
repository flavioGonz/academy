from _akv import *

NOLIG = "<style>text{font-variant-ligatures:none;font-feature-settings:'calt' 0,'liga' 0}</style>"

# ---------- 13.svg: el firmware decide la URL
c = Canvas("Akuvox · Lección 13", "Leé el firmware y después elegí la URL")
c.add(NOLIG)
c.add(Window(48, 140, 420, 200, "Web del portero", path="Status > Basic > Product Information", rows=[("Firmware", "29.30.10.x")], hl=0))
c.add(text(68, 300, "tercer bloque: 10", 17, 600, WARN, FM))
c.add(text(68, 324, "10 o más = rama de alta seguridad", 15, 500, INK3, FB))
cases = [("Tercer bloque menor a 10", "rama sin alta seguridad", "/fcgi/do (formato viejo)", "info"),
         ("10 o más · High Security Mode encendido", "encendido de fábrica en el E18", "solo /fcgi/OpenDoor", "ok"),
         ("10 o más · High Security Mode apagado", "Security > Basic > High Security Mode", "/fcgi/OpenDoor y también /fcgi/do", "warn")]
for i, (a, b, url, kd) in enumerate(cases):
    y = 140 + i * 160
    bg, fg = KC[kd]
    c.add(f'<rect x="520" y="{y}" width="632" height="136" rx="16" fill="{WHITE}" stroke="{LINE2}" stroke-width="1.5"/>')
    c.add(f'<rect x="520" y="{y + 14}" width="6" height="108" rx="3" fill="{fg}"/>')
    c.add(text(546, y + 38, a, 18, 600, INK))
    c.add(text(546, y + 62, b, 15, 500, INK3, FM))
    c.add(code(546, y + 80, 586, url, 15))
    c.add(wire([(470, 236), (492, 236), (492, y + 68), (512, y + 68)], "logical", arrow=True))
c.add(Note(48, 380, 420, "DoorNum=1 dispara el relé A y DoorNum=2 el relé B, en cualquier formato.", kind="info"))
c.add(Note(48, 500, 420, "Apagar la alta seguridad para usar la URL vieja funciona, pero Akuvox recomienda el formato nuevo.", kind="warn", size=15))
save(c, "13.svg")

# ---------- 13-paso3.svg: habilitar Open Relay via HTTP
c = Canvas("Akuvox · Lección 13 · Paso 3", "Habilitá Open Relay via HTTP con usuario propio")
c.add(Window(48, 140, 620, 300, "Web del portero", path="Intercom > Relay (R29) · Access Control > Relay (E18)",
             rows=[("Open Relay via HTTP", "Enabled"), ("Username", "abre-lab"), ("Password", "Ejemplo-Http-2026"), ("Session Check", "apagado")], hl=3))
c.add(Step(48, 140, 3))
c.add(Note(710, 140, 442, "Akuvox avisa que con Session Check activado la apertura puede fallar. Dejalo apagado y tocá Submit.", title="Session Check apagado", kind="warn"))
c.add(Note(710, 320, 442, "Usuario y clave solo para abrir: si se filtran, no dan acceso a la web del equipo.", title="Por qué no el admin", kind="ok"))
c.add(Note(48, 480, 620, "Probalo con una lámpara o una cerradura de banco, no con la puerta de un cliente en uso.", kind="alert", size=16))
save(c, "13-paso3.svg")

# ---------- 13-paso4.svg: anatomía de la URL
c = Canvas("Akuvox · Lección 13 · Paso 4", "Cada parte de la URL hace una cosa")
c.add(NOLIG)
parts = [("http://", "#7FA6C9"), ("abre-lab:Ejemplo-Http-2026", "#F3B562"), ("@192.168.88.21", "#7FD3F0"),
         ("/fcgi/OpenDoor", "#8FE3B5"), ("?action=OpenDoor", "#D9E9F8"), ("&DoorNum=1", "#FF9F8A")]
svg, spans = code_parts(48, 170, parts, 16, 56, 20)
c.add(svg)
labels = [None, ("usuario:clave", "los de Open Relay via HTTP"), ("IP del portero", ""), ("endpoint nuevo", "vale con alta seguridad"),
          ("acción", "abrir"), ("relé", "1 = A · 2 = B")]
lx = [None, 120, 380, 560, 760, 960]
for (x0, x1), lab, tx in zip(spans, labels, lx):
    if not lab:
        continue
    mx = (x0 + x1) / 2
    c.add(f'<path d="M{mx:.0f} 232V262H{tx + 60}V290" fill="none" stroke="{LINE2}" stroke-width="2"/>')
    c.add(text(tx, 316, lab[0], 17, 600, INK))
    if lab[1]:
        c.add(text(tx, 340, lab[1], 15, 500, INK3, FB))
c.add(Step(48, 170, 4))
c.add(text(48, 410, "FORMATO VIEJO · solo sin alta seguridad o con el modo apagado", 14, 600, WARN, FM, ls=1.2))
c.add(code(48, 424, 1104, "http://192.168.88.21/fcgi/do?action=OpenDoor&UserName=abre-lab&Password=Ejemplo-Http-2026&DoorNum=1", 15, "#F3D9A8", 46))
c.add(Note(48, 510, 1104, "Con curl, -u 'abre-lab:Ejemplo-Http-2026' manda lo mismo que usuario:clave@ y sin http:// usa HTTP por defecto. Anotá en la ficha qué formato abrió y con qué firmware (paso 5).", kind="info", size=16))
save(c, "13-paso4.svg")
