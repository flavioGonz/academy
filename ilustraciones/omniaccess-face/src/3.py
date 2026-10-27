import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 3.svg: secuencia aviso → MAC → foto → monitor
c = Canvas("OmniAccess Face · Lección 3", "El aviso trae la MAC; la foto la busca el servidor")
lanes = [(170, "Terminal facial", "192.0.2.21 · MAC …53:21"), (620, "Servidor de eventos", "192.0.2.10 · puerto 10000"), (1030, "Monitor Facial", "navegador del puesto")]
for x, t_, s_ in lanes:
    c.add(f'<rect x="{x - 130}" y="126" width="260" height="62" rx="12" fill="{DEEP}"/>')
    c.add(text(x, 152, t_, 18, 600, WHITE, FB, anchor="middle"))
    c.add(text(x, 175, s_, 14, 500, "#9FC3E3", FM, anchor="middle"))
    c.add(f'<path d="M{x} 190V560" stroke="{LINE2}" stroke-width="2" stroke-dasharray="6 6"/>')
rows = [
    (232, 170, 620, "1", "GET /api/webhooks/akuvox?event=face_valid&mac=…", "flow"),
    (330, 620, 620, "2", "", None),
    (420, 620, 170, "3", "pide la foto al registro del equipo (usuario y clave de API)", "logical"),
    (462, 170, 620, "", "devuelve la imagen", "logical"),
    (540, 620, 1030, "4", "evento + foto en tiempo real", "ok"),
]
for y, a, b, n, lab, kind in rows:
    if kind:
        c.add(Arrow((a + (8 if b > a else -8), y), (b - (8 if b > a else -8), y), kind=kind, bend="straight"))
        c.add(text((a + b) / 2, y - 12, lab, 14 if "GET" in lab else 15, 600 if n else 500, INK if n else INK3, FM if "GET" in lab else FB, anchor="middle"))
    if n:
        sx = {"1": 194, "2": 644, "3": 644, "4": 644}[n]
        c.add(Step(sx, y + 24 if n != "3" else y, n))
c.add(Note(672, 290, 330, "Busca el equipo por la MAC. Si no coincide, prueba por IP; si tampoco, el evento se descarta.", kind="warn", size=15))
c.add(Note(40, 584, 600, "La Action URL no lleva la imagen: sin camino de vuelta al terminal, hay evento sin foto.", kind="info", size=15))
save(c, "3.svg")

# ---------------------------------------------------------------- 3-paso2: alta del dispositivo
c = Canvas("OmniAccess Face · Lección 3 · Paso 2", "Alta del terminal: la MAC no es opcional")
c.add(Window(48, 128, 700, 470, "OmniAccess · Gestión → Dispositivos Faciales → Agregar",
             rows=[("Tipo", "Acceso Facial"), ("Fabricante", "Akuvox"), ("Modelo Hardware", "el del equipo"), ("Host / IP", "192.0.2.21"),
                   ("Hardware ID (MAC)", "00:00:5E:00:53:21"), ("Usuario Manager", "usuario de API"), ("API Password", "••••••••"),
                   ("Sentido del Flujo", "ENTRADA (Ingreso)"), ("Ubicación Física", "Portería peatonal")], hl=4))
c.add(Step(748, 128, 2))
c.add(Note(790, 140, 362, "Con la MAC, el servidor sabe qué equipo avisa. Escribila como la muestra la web del terminal; el servidor ignora dos puntos y guiones.", title="Hardware ID (MAC)", kind="warn", size=15))
c.add(Note(790, 330, 362, "Con el usuario y la clave de la API, OmniAccess cuenta caras y tarjetas, busca la foto de cada evento y acciona el relé.", title="Usuario y API Password", kind="info", size=15))
c.add(Note(790, 500, 362, "Entrada o Salida decide en qué columna del Monitor Facial cae cada evento.", title="Sentido del Flujo", kind="ok", size=15))
save(c, "3-paso2.svg")

# ---------------------------------------------------------------- 3-paso4: configurador de Action URLs
c = Canvas("OmniAccess Face · Lección 3 · Paso 4", "Copiá la URL de cada evento desde el configurador")
c.add(Window(48, 128, 1104, 300, "Configurador de Action URLs · menú ⋯ → Webhooks (Action URL)",
             rows=[("Valid Face", "…:10000/api/webhooks/akuvox?event=face_valid&mac=$mac&user=$user_name…"),
                   ("Invalid Face", "…?event=face_invalid&mac=$mac&FaceUrl=$FaceUrl…"),
                   ("Relay Output", "…?event=relay_open&mac=$mac&relay=$relay_id…"),
                   ("System Boot", "…?event=boot&mac=$mac&model=$model&firmware=$firmware…"),
                   ("Copiar URL", "un botón por evento")], hl=0))
c.add(Step(1152, 128, 4))
c.add(Table(48, 456, ["Variable", "La completa el terminal con"], [["$mac", "su MAC (identifica el equipo)"], ["$user_name", "el nombre reconocido"], ["$userid", "el ID de la persona en el equipo"]], [200, 420], mono_cols=(0,), row_h=38))
c.add(Note(720, 456, 432, "Va al puerto 10000 del servidor. Si quedó \"$mac\" sin reemplazar en el registro de Webhooks, el modelo no conoce esa variable: revisalo en el curso Porteros IP Akuvox.", kind="warn", size=15))
save(c, "3-paso4.svg")

# ---------------------------------------------------------------- 3-paso6: registro de webhooks, bien y mal
c = Canvas("OmniAccess Face · Lección 3 · Paso 6", "En Webhooks, el aviso tiene que tener nombre de equipo")
c.add(Table(48, 140, ["Hora", "Fuente", "Dispositivo", "MAC", "Dato"],
            [["10:02:11", "Akuvox", "Portería peatonal", "00:00:5E:00:53:21", "Ana Ejemplo"],
             ["10:05:40", "Akuvox", "Dispositivo Desconocido", "00:00:5E:00:53:99", "Ana Ejemplo"]], [130, 130, 270, 250, 200], mono_cols=(0, 3), row_h=46))
c.add(Step(48, 326, 6))
c.add(Mark(1064, 209, True))
c.add(Mark(1064, 255, False))
c.add(Note(84, 312, 520, "Bien: el servidor encontró el equipo por su MAC. En Dispositivos se prende el ícono Push (azul).", kind="ok", size=16))
c.add(Note(632, 312, 520, "Mal: la MAC del aviso no es la cargada en la ficha del equipo. Corregí el Hardware ID (MAC).", kind="alert", size=16))
c.add(Note(84, 420, 1068, "Ruta: Configuración → Sistema → Webhooks → fuente Akuvox. Ahí se ven todos los avisos que llegan al puerto 10000, con sus parámetros.", kind="info", size=16))
save(c, "3-paso6.svg")
