import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 8.svg: baja en orden y qué borra cada cosa
c = Canvas("OmniAccess Face · Lección 8", "La baja va primero en el terminal, después en la ficha")
flow = [("Alta", "Nueva visita + foto + terminal", OK), ("Uso", "hasta la fecha anotada", BLUE), ("1 · Terminal", "Memoria Flash → eliminar", ALERT), ("2 · Ficha", "decidir: conservar o borrar", WARN)]
for i, (t_, s_, col) in enumerate(flow):
    x = 48 + i * 282
    c.add(card(x, 136, 250, 100, stroke=col, sw=2.5))
    c.add(text(x + 20, 176, t_, 19, 600, INK, FB))
    c.add(text(x + 20, 204, s_, 15, 400, INK3, FB))
    if i < 3:
        c.add(Arrow((x + 252, 186), (x + 280, 186), kind="flow", bend="straight"))
c.add(Table(48, 280, ["Acción", "La cara en el terminal", "La foto guardada", "Los eventos del Historial"],
            [["Eliminar en Memoria Flash", "se borra: deja de abrir", "queda", "quedan"],
             ["Borrar la ficha", "queda: sigue abriendo", "queda", "se borran con la ficha"],
             ["Cambiar el Modo Face", "queda: sigue abriendo", "queda", "cambia cómo se registran"]], [300, 280, 210, 314], row_h=46, hl_row=0))
c.add(Note(48, 480, 540, "Bloquear a alguien en Face es sacarlo de la memoria del terminal y probar que no abre.", title="Bloqueo real", kind="ok", size=16))
c.add(Note(612, 480, 540, "Si la administración necesita conservar el historial de esa persona, dejá la ficha sin terminales marcados en lugar de borrarla.", title="Antes de borrar la ficha", kind="warn", size=16))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso3: eliminar en Memoria Flash
c = Canvas("OmniAccess Face · Lección 8 · Paso 3", "Sacalo del terminal desde Memoria Flash")
c.add(Window(48, 128, 760, 250, "Portería peatonal · Memoria Flash · Directorio",
             rows=[("Buscar", "Obrero Ejemplo"), ("ID 004410862 · Obrero Ejemplo", "rostro ✓   eliminar"), ("Resultado", "Rostro eliminado correctamente")], hl=1))
c.add(Step(808, 128, 3))
t = c.add(FaceTerminal(900, 150, "Portería peatonal", "ya no lo reconoce", hl=ALERT, scale=0.85, mark=False))
c.add(Note(48, 410, 760, "Probá la cara: el terminal no abre. Si cargaste la Action URL de Invalid Face, en el monitor aparece como rostro desconocido.", title="Paso 4", kind="info", size=16))
c.add(Note(48, 540, 1104, "La ficha se toca recién después: borrarla también borra sus eventos del Historial.", kind="warn", size=16))
save(c, "8-paso3.svg")
