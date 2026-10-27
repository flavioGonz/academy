import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 1.svg: quién decide y quién registra
c = Canvas("OmniAccess Face · Lección 1", "La puerta la abre el terminal; OmniAccess la cuenta")
c.add(Zone(40, 130, 470, 440, "EN LA PARED · DECIDE", OK))
c.add(Zone(560, 130, 600, 440, "EN EL SERVIDOR · REGISTRA", BLUE))
c.add(Person(64, 190, "Persona", "se presenta", w=190))
t = c.add(FaceTerminal(300, 160, "Terminal facial", "Akuvox o Hikvision", hl=OK, scale=0.9))
c.add(Arrow((254, 232), (296, 232), kind="flow"))
c.add(Lock(64, 332, "Cerradura", "relé", w=170))
c.add(Cable((300, 374), (234, 374), kind="relay", bend="straight"))
c.add(text(267, 360, "abre", 15, 600, CYAN, FM, anchor="middle"))
c.add(Note(64, 452, 420, "El terminal compara con su propia memoria y su umbral, y dispara su relé. No espera al servidor.", kind="ok", size=16))
srv = c.add(Server(600, 170, "Servidor de eventos", "puerto 10000", w=250))
c.add(Arrow(t.port("eth"), (598, 212), label="aviso (Action URL)", kind="logical", label_at=0.55, label_dy=-14))
c.add(Box(600, 300, 250, 90, "Modo Face", "Lista Blanca / Negra"))
c.add(Arrow((725, 256), (725, 298), kind="flow"))
c.add(Box(890, 170, 240, 84, "Foto del evento", "bucket face"))
c.add(Arrow((852, 212), (888, 212), kind="flow"))
c.add(Box(890, 300, 240, 90, "Monitor Facial", "Permitido / Denegado"))
c.add(Arrow((852, 345), (888, 345), kind="flow"))
c.add(Note(600, 420, 530, "Cambiar el Modo Face cambia cómo se registra el evento. No traba ni libera la puerta.", title="La cámara controla la apertura física", kind="warn", size=16))
c.add(Note(40, 596, 1120, "Bloquear a alguien de verdad es sacar su cara de la memoria del terminal (lección 8).", kind="info", size=16))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso3: las tres opciones del Modo Face
c = Canvas("OmniAccess Face · Lección 1 · Paso 3", "Qué hace cada opción del Modo Face")
c.add(Window(48, 128, 620, 214, "OmniAccess · Configuración", path="Modos → Modos (LPR / Face / Cola) → Modo Face",
             rows=[("Lista Negra", "identificado → DENEGADO"), ("Lista Blanca", "identificado → PERMITIDO"), ("Aprendizaje", "deshabilitado")], hl=1))
c.add(Step(668, 128, 3))
c.add(Table(48, 380, ["Opción", "Registro en OmniAccess", "Puerta"],
            [["Lista Blanca", "permitido si encuentra la ficha", "la decide el terminal"],
             ["Lista Negra", "denegado si encuentra la ficha", "la decide el terminal"],
             ["Aprendizaje", "no disponible", "la decide el terminal"]], [190, 330, 260], row_h=40))
c.add(Note(860, 128, 292, "Activar un modo recarga la interfaz de todos los puestos. En producción, avisá antes.", title="Atención", kind="warn", size=16))
c.add(Note(860, 300, 292, "La columna Puerta no cambia con ninguna opción: ese es el punto de la lección.", kind="ok", size=16))
save(c, "1-paso3.svg")
