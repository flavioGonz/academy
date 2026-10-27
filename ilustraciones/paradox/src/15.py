import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/paradox/src")
from _pdx import *

# ---------------------------------------------------------------- 15.svg: el llavero de una SP+
c = Canvas(K(), "Todas las llaves de una SP+ y su valor de fábrica")
c.add(NOLIG)
rows = [["Código de instalador", "[397]", "0000"], ["Código de mantenimiento", "[398]", "vacío"], ["Maestro del sistema", "[399]", "1234"],
        ["ID de panel", "[910]", "0000 (*)"], ["Contraseña de PC", "[911]", "0000 (*)"], ["Instalador del software BabyWare", "[927]", "admin"],
        ["Contraseña de receptor IP (legado)", "[933]", "123456"], ["Contraseña del módulo IP150", "app / web", "paradox"]]
c.add(Table(48, 124, ["Llave", "Dónde", "Fábrica"], rows, [380, 150, 170], row_h=46, mono_cols=(1, 2)))
for i in range(len(rows)):
    c.add(f'<circle cx="730" cy="{124 + 46 * (i + 1) + 23}" r="6" fill="{ALERT}"/>')
c.add(text(48, 576, "(*) La guía SP+ dice que BabyWare obliga a cambiarlas; otros manuales siguen citando 0000.", 15, 500, INK3, FB))
c.add(text(48, 600, "La del IP150, en firmware viejo.", 15, 500, INK3, FB))
c.add(Note(780, 124, 372, "Todos esos valores están en manuales públicos. Una central que sale de obra con uno solo de fábrica se abre con un cable y una lista.", title="Por qué todas", kind="alert"))
c.add(Note(780, 300, 372, "Bloqueo de teclado ([717] intentos, [716] minutos) y bloqueo de instalador ([395] = 147, solo si está en el contrato).", title="Y dos protecciones", kind="info"))
c.add(Note(780, 456, 372, "La ficha con las llaves nuevas va al sistema de gestión, nunca dentro del gabinete.", kind="ok"))
save(c, "15.svg")

# ---------------------------------------------------------------- 15-paso3: bloqueo de teclado
c = Canvas(K(3), "Bloqueo de teclado: cinco intentos y diez minutos afuera")
c.add(NOLIG)
c.add(Step(48, 140, 3))
c.add(code(80, 124, 470, "[717] 005    5 intentos inválidos", 16, h=40))
c.add(code(580, 124, 470, "[716] 010    10 minutos de bloqueo", 16, h=40))
for i in range(5):
    x = 80 + i * 130
    c.add(rect(x, 220, 110, 80, ALERT_BG, ALERT, rx=12))
    c.add(mid(x + 55, 254, "código", 15, 500, INK2, FB))
    c.add(mid(x + 55, 282, f"inválido {i + 1}", 16, 700, ALERT, FB))
c.add(Arrow((730, 260), (780, 260), kind="alert"))
c.add(rect(790, 200, 362, 120, "#03213C", "#03213C", rx=14))
c.add(text(812, 240, "Teclados bloqueados", 20, 600, WHITE, FD))
c.add(text(812, 270, "10 minutos", 18, 600, "#FFD28A", FM))
c.add(text(812, 300, "y la central lo reporta", 16, 500, "#9FC3E3", FB))
c.add(Note(48, 360, 540, "Frena al que prueba códigos de memoria o de manual en el teclado, y el reporte avisa a monitoreo que alguien lo intentó.", title="Para qué sirve", kind="ok"))
c.add(Note(612, 360, 540, "000 lo deja apagado (fábrica). Valores de ejemplo: acordalos con el cliente, que también puede quedar afuera por equivocarse.", title="Valores", kind="info"))
save(c, "15-paso3.svg")

# ---------------------------------------------------------------- 15-paso4: bloqueo de instalador y reseteo
c = Canvas(K(4), "Bloqueo de instalador: el reseteo ya no borra")
c.add(NOLIG)
c.add(Step(48, 124, 4))
cols = [("Sin bloqueo · [395] = 000", "info", "Reseteo por botón", ["Vuelve todo a fábrica", "salvo ID de panel y contraseña de PC.", "El buffer de eventos no se borra."]),
        ("Con bloqueo · [395] = 147", "warn", "Reseteo por botón", ["No borra la programación.", "Al energizar, LED de estado", "rápido durante 6 s."])]
for i, (t, kd, s, ls) in enumerate(cols):
    x = 48 + i * 564
    c.add(panel(x, 124, 540, 260, t, kd))
    c.add(text(x + 24, 196, s, 18, 600, INK3, FB))
    c.add(lines(x + 24, 240, ls, 18, 32, INK, FB, 600))
c.add(Note(48, 410, 540, "Se usa solo si está en el contrato con el cliente: protege la cartera del instalador, pero ata al cliente a quien tiene el código.", title="Una decisión comercial", kind="warn"))
c.add(Note(612, 410, 540, "Central bloqueada sin códigos: el camino es el cliente y el instalador anterior. Si no hay forma y el bloqueo está apagado, reseteo con autorización escrita.", title="Si te toca una ajena", kind="alert"))
save(c, "15-paso4.svg")
