import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 2.svg: quién manda
c = Canvas(K(), "En incendio, ¿quién decide qué?")
lv = [("Autoridad: Bomberos (DNB)", "Decreto 372/023 · IT-11 vigente (2010, remite a UNIT 962)", True),
      ("Proyecto firmado", "lo redacta y firma el técnico registrado", False),
      ("Normas de referencia", "EN 54 y NFPA 72: explican equipos y buenas prácticas", False),
      ("Manual del fabricante", "cómo funciona y se instala el AVENAR", False),
      ("Este curso", "te ayuda a entender, no decide nada", False)]
for i, (t, s, dark) in enumerate(lv):
    y = 130 + i * 88
    w = 680 - i * 40
    c.add(rect(48, y, w, 74, DEEP if dark else (SOFT if i == 1 else WHITE), DEEP if dark else (CYAN if i == 1 else LINE2), rx=14))
    c.add(text(70, y + 32, t, 19, 600, WHITE if dark else INK, FD))
    c.add(text(70, y + 56, s, 15, 400, "#9FC3E3" if dark else INK3, FB))
c.add(f'<path d="M26 556V140" stroke="{BLUE}" stroke-width="3" marker-end="url(#a-blue)"/>')
c.add(text(48, 590, "Cuanto más arriba, más manda.", 16, 600, BLUE, FB))
c.add(text(770, 140, "QUIÉN HACE QUÉ (DECRETO 372/023)", 13, 600, INK3, FM, ls=1.5))
roles = [("Técnico registrado", "redacta el proyecto, ingresa el trámite y verifica las medidas", "info"),
         ("Empresa registrada", "suministra, instala, pone en marcha y mantiene el sistema", "ok"),
         ("Propietario", "responde por mantener el sistema en condiciones", "warn")]
for i, (t, s, kd) in enumerate(roles):
    y = 156 + i * 140
    c.add(panel(770, y, 382, 124, t, kd))
    c.add(wrap(790, y + 64, s, 340, 16, 400, INK2)[0])
c.add(text(48, 640, "Si el proyecto y el manual no coinciden, se para y se consulta al técnico registrado.", 17, 600, BLUE))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso2: qué instructivo rige
c = Canvas(K(2), "Instructivo aplicable: el que rige hoy")
c.add(hline(80, 1120, 300, LINE2, 4))
ev = [(130, "2010", "IT-11 de Bomberos", "vigente, remite a UNIT 962", "ok"),
      (430, "enero 2024", "Decreto 372/023", "rige habilitaciones y registros", "ok"),
      (760, "31/07/2026", "Consulta pública", "borrador de la nueva IT11", "warn"),
      (1040, "2027", "Vigencia prevista", "recién ahí se usa", "gray")]
for x, d, t, s, kd in ev:
    col = {"ok": OK, "warn": WARN, "gray": INK3}[kd]
    c.add(f'<circle cx="{x}" cy="300" r="13" fill="{WHITE}" stroke="{col}" stroke-width="4"/>')
    c.add(mid(x, 268, d, 17, 600, col, FM))
    c.add(mid(x, 346, t, 18, 600, INK, FD))
    c.add(mid(x, 372, s, 15, 400, INK3))
c.add(rect(48, 410, 1104, 112, OK_BG, OK, rx=14))
c.add(text(72, 446, "Lo que pide la IT-11 vigente, entre otras cosas", 18, 600, OK, FD))
c.add(text(72, 480, "24 h de batería en reposo · 15 min en alarma · pulsador a no más de 30 m · preseñal de hasta 2 min en locales concurridos", 16, 400, INK2))
c.add(text(72, 506, "La versión exacta la cita el proyecto: si cita otra, se anota en la ficha.", 16, 400, INK2))
c.add(Note(48, 546, 1104, "La DNB aclaró que los borradores en consulta no autorizan su uso en proyectos hasta que entren en vigencia.", title="Borrador no es norma", kind="warn"))
save(c, "2-paso2.svg")

# ---------------------------------------------------------------- 2-paso3: si no coinciden
c = Canvas(K(3), "Proyecto y manual no coinciden: parás y consultás")
c.add(box(48, 136, 340, 120, "Proyecto firmado", ["Subsuelo: ramal (clase B)", "firmado por el técnico registrado"]))
c.add(box(48, 280, 340, 120, "Manual Bosch", ["Recomienda lazo siempre", "que se pueda"]))
c.add(rect(470, 226, 220, 84, WARN_BG, WARN, rx=42, sw=2))
c.add(mid(580, 262, "¿Coinciden?", 19, 600, WARN, FD))
c.add(mid(580, 288, "ejemplo de obra", 15, 400, INK3))
c.add(arrow((390, 196), (474, 252)))
c.add(arrow((390, 340), (474, 286)))
c.add(arrow((690, 230), (800, 170), kind="ok"))
c.add(arrow((690, 306), (800, 380), kind="alert"))
c.add(panel(810, 120, 342, 110, "Sí: seguís instalando", "ok"))
c.add(text(830, 190, "con el proyecto como guía", 16, 400, INK2))
c.add(panel(810, 300, 342, 200, "No: parás", "alert"))
c.add(bullet_list(830, 370, [("Anotás la diferencia en la ficha", "alert"), ("Consultás al técnico registrado", "alert"), ("Él decide y lo deja por escrito", "alert")], 300)[0])
c.add(Note(48, 440, 700, "Cambiar ubicación, cantidad o tipo de dispositivos respecto de lo certificado queda bajo responsabilidad de quien lo cambia; el decreto pide informar al técnico registrado.", title="Por qué no se decide en obra", kind="warn"))
save(c, "2-paso3.svg")

# ---------------------------------------------------------------- 2-t2: partes de EN 54 sobre el sistema (teoría, fija)
c = Canvas("Bosch Incendio · Normas", "Cada parte de EN 54 mira una pieza del sistema")
c.add(rect(450, 250, 300, 150, DEEP, DEEP, rx=16))
c.add(mid(600, 300, "Central", 22, 600, WHITE, FD))
c.add(mid(600, 330, "EN 54-2", 17, 600, CYAN, FM))
c.add(mid(600, 370, "fuente: EN 54-4", 16, 500, "#9FC3E3", FM))
parts = [(150, 180, "detector", "Humo puntual", "EN 54-7"), (150, 330, "detector", "Calor puntual", "EN 54-5"),
         (150, 480, "detector", "Multisensor humo y calor", "EN 54-29"), (1050, 180, "pulsador", "Pulsador", "EN 54-11"),
         (1050, 330, "aislador", "Aislador de corto", "EN 54-17"), (1050, 480, "sirena", "Sirena", "EN 54-3")]
for x, y, k, t, n in parts:
    if k == "detector":
        c.add(detector(x - 80, y, 26))
    elif k == "pulsador":
        c.add(pulsador(x + 80, y, 46))
    elif k == "sirena":
        c.add(sirena(x + 80, y, 48))
    else:
        c.add(iso(x + 62, y, True))
    tx = x - 40 if x < 600 else x + 40
    an = "start" if x < 600 else "end"
    c.add(text(tx, y - 4, t, 17, 600, INK, FB, anchor=an))
    c.add(text(tx, y + 20, n, 16, 600, BLUE, FM, anchor=an))
    c.add(f'<path d="M{x + 160 if x < 600 else x - 160} {y}L{450 if x < 600 else 750} {325}" stroke="{LINE2}" stroke-width="2" stroke-dasharray="5 5"/>')
c.add(rect(370, 440, 460, 64, SOFT, CYAN, rx=14))
c.add(mid(600, 470, "EN 54-13: que todo funcione junto", 17, 600, BLUE))
c.add(mid(600, 494, "compatibilidad entre componentes", 15, 400, INK3))
c.add(text(48, 600, "Son normas de producto: dicen cómo se ensaya cada equipo. Dónde va cada uno lo dice el proyecto.", 17, 500, INK2))
save(c, "2-t2.svg")
