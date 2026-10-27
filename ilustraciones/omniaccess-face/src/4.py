import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 4.svg: ficha → copia → memoria → Memoria Flash
c = Canvas("OmniAccess Face · Lección 4", "Guardar la ficha no es enrolar: falta la copia")
c.add(card(48, 130, 400, 330, "Ficha de la persona"))
c.add(face_thumb(70, 180, 96))
c.add(text(186, 210, "Ana Ejemplo", 18, 600, INK, FB))
c.add(text(186, 236, "Lote 12", 15, 400, INK3, FM))
c.add(text(186, 262, "foto: JPG < 200 KB", 15, 400, INK3, FM))
c.add(text(70, 318, "A qué equipos se manda", 16, 600, INK, FB))
c.add(text(70, 344, "Terminales de rostro", 15, 500, INK3, FB))
c.add(f'<rect x="70" y="358" width="22" height="22" rx="5" fill="{BLUE}"/>' + icon(72, 360, "check", WHITE, 0.75, 3))
c.add(text(104, 375, "Portería peatonal", 16, 500, INK, FB))
c.add(f'<rect x="70" y="394" width="22" height="22" rx="5" fill="{WHITE}" stroke="{LINE2}" stroke-width="2"/>')
c.add(text(104, 411, "Portería de servicio", 16, 500, INK3, FB))
t = c.add(FaceTerminal(640, 150, "Portería peatonal", "memoria del equipo", hl=BLUE, scale=0.95))
c.add(Arrow((450, 260), (636, 260), label="Enviar el rostro", kind="flow", label_at=0.5, label_dy=-14))
c.add(text(543, 300, "ID de 9 dígitos", 15, 500, INK3, FM, anchor="middle"))
c.add(text(543, 322, "nombre, tarjeta, PIN, foto", 15, 500, INK3, FB, anchor="middle"))
c.add(Window(860, 150, 300, 230, "Memoria Flash · Directorio", rows=[("Ana Ejemplo", "con foto"), ("Bruno Ejemplo", "con foto"), ("Carla Ejemplo", "sin foto")], hl=0))
c.add(Arrow((774, 210), (858, 210), kind="logical"))
c.add(text(816, 196, "lee", 15, 600, INK3, FB, anchor="middle"))
c.add(Note(48, 500, 540, "La persona está enrolada cuando aparece en el Directorio del terminal, no cuando se guardó la ficha.", title="Regla", kind="ok", size=16))
c.add(Note(612, 500, 548, "Volcar Base de Datos a Equipo manda a todos los que tienen foto o tarjeta: usalo solo si ese terminal es para todos.", title="Cuidado", kind="warn", size=16))
save(c, "4.svg")

# ---------------------------------------------------------------- 4-paso1: foto que sirve y fotos que no
c = Canvas("OmniAccess Face · Lección 4 · Paso 1", "La foto que sirve: de frente, una cara, luz pareja")
items = [(None, True, "de frente, luz pareja"), ("side", False, "de costado"), ("dark", False, "oscura o a contraluz"), ("glasses", False, "lentes oscuros"), ("two", False, "dos caras")]
for i, (bad, ok, lab) in enumerate(items):
    x = 60 + i * 222
    c.add(face_thumb(x, 150, 150, ok=ok, bad=bad))
    c.add(text(x + 75, 336, lab, 16, 600, OK if ok else ALERT, FB, anchor="middle"))
c.add(Step(48, 150, 1))
c.add(Table(48, 384, ["Requisito", "Para Akuvox desde OmniAccess"], [["Formato", "JPG"], ["Peso", "menos de 200 KB"], ["Resolución", "al menos 640 x 480"], ["Encuadre", "una sola cara, centrada, de frente"]], [240, 420], row_h=40))
c.add(Note(760, 384, 392, "Cada fabricante tiene su límite (Speco pide menos de 70 KB; Hikvision, entre 40 y 200 KB). Si dudás, manda el equipo destino.", kind="info", size=16))
save(c, "4-paso1.svg")

# ---------------------------------------------------------------- 4-paso4: Memoria Flash, Directorio
c = Canvas("OmniAccess Face · Lección 4 · Paso 4", "Buscala en Memoria Flash → Directorio")
c.add(Window(48, 128, 760, 280, "Portería peatonal · Memoria Flash", path="Directorio · Identidades en memoria física",
             rows=[("ID 000482193 · Ana Ejemplo", "rostro ✓  tag —"), ("ID 001937520 · Bruno Ejemplo", "rostro ✓  tag ✓"), ("ID 003310477 · Carla Ejemplo", "rostro —  tag ✓"), ("Refrescar Memoria", "vuelve a leer el equipo")], hl=0))
c.add(Step(808, 128, 4))
c.add(Note(840, 140, 312, "El ID lo calcula OmniAccess a partir de la ficha: no lo cambies a mano en el terminal.", title="ID de 9 dígitos", kind="warn", size=15))
c.add(Note(840, 300, 312, "Lo que está en el equipo y no en la base se puede traer con Descargar Equipo a App.", kind="info", size=15))
c.add(Table(48, 440, ["Botón", "Qué hace"], [["Inyectar Usuarios", "manda personas elegidas al equipo"], ["Volcar Base de Datos a Equipo", "manda a todos con foto o tarjeta"]], [330, 420], row_h=40))
save(c, "4-paso4.svg")
