import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 9.svg: reporte, huecos y retención
c = Canvas("OmniAccess Face · Lección 9", "Reportes sin huecos y una retención que no sorprenda")
# bloque 1: historial
c.add(card(48, 130, 352, 300, "1 · La pregunta"))
for i, (k, v) in enumerate([("Tipo", "Rostros"), ("Resultado", "Denegados"), ("Sentido", "Entrada"), ("Rango", "lunes a hoy")]):
    c.add(text(68, 186 + i * 40, k, 16, 500, INK3, FB))
    c.add(Chip(200, 191 + i * 40, v, "blue", mono=False))
c.add(Chip(68, 400, "Exportar (Excel / PDF)", "ok", mono=False))
# bloque 2: huecos
c.add(card(424, 130, 352, 300, "2 · Los huecos"))
t = c.add(FaceTerminal(450, 170, "", "", scale=0.55))
c.add(text(536, 186, "El terminal guarda", 15, 500, INK2, FB))
c.add(text(536, 206, "su propio registro", 15, 500, INK2, FB))
c.add(text(536, 226, "(doorlog) aunque", 15, 500, INK2, FB))
c.add(text(536, 246, "se corte la red.", 15, 500, INK2, FB))
c.add(Arrow((520, 330), (560, 380), kind="flow"))
c.add(text(444, 400, "Auditoría Hardware", 16, 600, BLUE, FM))
c.add(text(444, 420, "→ Sincronizar memoria", 15, 500, BLUE, FM))
# bloque 3: bucket
c.add(card(800, 130, 352, 300, "3 · El Bucket FACE"))
c.add(f'<path d="M830 190h292l-18 180h-256z" fill="{SOFT}" stroke="{BLUE}" stroke-width="2"/>')
for j in range(3):
    c.add(face_thumb(850 + j * 86, 206, 64))
for j in range(3):
    c.add(face_thumb(850 + j * 86, 286, 64))
c.add(text(976, 396, "capturas y fotos de alta", 15, 600, INK2, FB, anchor="middle"))
c.add(text(976, 418, "en el mismo bucket", 15, 600, INK2, FB, anchor="middle"))
c.add(Note(48, 460, 540, "Los eventos traídos así llevan SINCRO_HW en el detalle. La sincronización existe para terminales Akuvox.", kind="info", size=16))
c.add(Note(612, 460, 540, "La regla de días se aplica a todo el bucket: con 30 días, también se borran las fotos de alta de más de 30 días.", title="Retención", kind="warn", size=16))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso1: los filtros del Historial
c = Canvas("OmniAccess Face · Lección 9 · Paso 1", "Armá el reporte con los filtros del Historial")
c.add(f'<rect x="48" y="140" width="1104" height="92" rx="14" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
seg = [(68, ["Rostros", "RFID"], 0), (300, ["Todos", "Permitidos", "Denegados"], 2), (660, ["Ambos", "Entrada", "Salida"], 1)]
for x0, opts, sel in seg:
    x = x0
    for k, o in enumerate(opts):
        w = len(o) * 8.4 + 26
        c.add(Chip(x, 196, o, "dark" if k == sel else "gray", mono=False))
        x += w + 6
c.add(Chip(940, 196, "lun 00:00 → hoy", "blue"))
c.add(Step(48, 140, 1))
c.add(f'<rect x="48" y="256" width="760" height="54" rx="12" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(text(72, 290, "Buscar: Portería peatonal", 17, 500, INK, FM))
c.add(Chip(840, 292, "Exportar (Excel / PDF)", "ok", mono=False))
c.add(Note(48, 350, 540, "¿Quién fue rechazado en la portería peatonal esta semana? Cada filtro contesta una parte de la pregunta.", title="Primero la pregunta", kind="ok", size=16))
c.add(Note(612, 350, 540, "El Monitor Facial muestra solo 24 horas; para una semana o un mes, el Historial de Acceso.", kind="info", size=16))
save(c, "9-paso1.svg")

# ---------------------------------------------------------------- 9-paso4: dónde se ve la retención
c = Canvas("OmniAccess Face · Lección 9 · Paso 4", "Revisá la retención del Bucket FACE")
c.add(Window(48, 128, 700, 180, "OmniAccess · Configuración → Sistema → Almacenamiento",
             rows=[("Bucket FACE", "face"), ("Días de retención antes de borrar", "0 = nunca")], hl=1))
c.add(Step(748, 128, 4))
c.add(Table(48, 370, ["Valor", "Qué pasa"], [["0", "no se borra nada: crece sin límite"], ["30", "a los 30 días se borran capturas y fotos de alta"], ["365", "un año de capturas; las fotos de alta viejas también se van"]], [120, 580], row_h=42))
c.add(Note(790, 140, 362, "Antes de poner un número, acordá con la administración cuánto se guardan las capturas y cómo se resguardan las fotos de alta.", title="Decidir con el responsable", kind="warn", size=16))
c.add(Note(790, 360, 362, "Por debajo es una regla de vencimiento de MinIO: borra objetos a N días de creados.", kind="info", size=16))
save(c, "9-paso4.svg")
