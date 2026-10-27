import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 2.svg: red host contra red bridge
c = Canvas(K(), "Red host: el anuncio del EAP llega al controlador")
for x, title, kd in ((48, "Red bridge con puertos publicados", "alert"), (612, "network_mode: host", "ok")):
    c.add(panel(x, 124, 540, 344, title, kd))
# bridge
c.add(APNode(112, 288, "EAP", "de fábrica", r=34))
c.add(Zone(196, 186, 372, 196, "VM Linux"))
c.add(Zone(296, 226, 256, 140, "red bridge", color=ALERT))
c.add(Generic(310, 262, "Controlador", "contenedor", icon="server", w=228, dark=True))
c.add(Cable((150, 304), (284, 304), kind="alert", arrow=False))
c.add(text(166, 290, "UDP 29810", 15, 600, ALERT, FM))
c.add(Mark(296, 304, ok=False))
c.add(Mark(84, 414, ok=True))
c.add(text(114, 420, "La web en :8043 abre", 16, 500, INK2, FB))
c.add(Mark(330, 414, ok=False))
c.add(text(360, 420, "Los EAP nunca aparecen", 16, 600, ALERT, FB))
# host
c.add(APNode(676, 288, "EAP", "de fábrica", r=34))
c.add(Zone(760, 186, 372, 196, "VM Linux · red del host"))
c.add(Generic(804, 262, "Controlador", "escucha el 29810", icon="server", w=300, dark=True))
c.add(Cable((714, 304), (798, 304), kind="ok"))
c.add(text(722, 290, "29810", 15, 600, OK, FM))
c.add(Mark(648, 414, ok=True))
c.add(text(678, 420, "El broadcast entra", 16, 500, INK2, FB))
c.add(Mark(870, 414, ok=True))
c.add(text(900, 420, "El EAP queda en Pending", 16, 600, OK, FB))
c.add(Note(48, 490, 540, "TP-Link no publica imagen Docker. Se usa la comunitaria mbentley/omada-controller, que trae Java y MongoDB adentro.", title="Imagen no oficial", kind="info"))
c.add(Note(612, 490, 540, "En Docker Desktop de Windows o macOS la red host no funciona: ahí los equipos llegan por Inform URL.", title="Docker Desktop", kind="warn"))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso1: AVX
c = Canvas(K(1), "Antes de instalar, mirá si la CPU tiene AVX")
c.add(Terminal(48, 128, 1104, ['$ grep -o -m1 avx /proc/cpuinfo || echo "SIN AVX: usar mbentley/omada-controller:5"'], title="VM LINUX"))
c.add(Step(48, 128, 1))
c.add(panel(48, 236, 540, 190, "Imprime avx", "ok"))
c.add(lines(72, 304, ["Imagen mbentley/omada-controller:6.2", "Controlador 6.x con su MongoDB.", "Seguí con el compose del paso 2."], 16, 30))
c.add(panel(612, 236, 540, 190, "Imprime SIN AVX", "warn"))
c.add(lines(636, 304, ["Imagen :5, la rama 5 del controlador,", "o una mini PC Intel de 6.ª generación", "o más nueva."], 16, 30))
c.add(Note(48, 450, 540, "El controlador 6.x usa un MongoDB que pide la instrucción AVX. Una Raspberry Pi 4 o un NAS viejo no la tienen y el contenedor no arranca.", title="Por qué importa", kind="info"))
c.add(Note(612, 450, 540, "Al arrancar usa unos 1,9 GB de RAM, según LazyAdmin: conviene dejarle 4 GB libres en la VM.", title="Memoria", kind="info"))
save(c, "2-paso1.svg")

# ---------------------------------------------------------------- 2-paso2: el compose comentado
c = Canvas(K(2), "Cada línea del compose evita un problema")
code_lines = [
    "services:",
    "  omada-controller:",
    "    image: mbentley/omada-controller:6.2",
    ("    network_mode: host", CYAN),
    ("    restart: unless-stopped", CYAN),
    ("    stop_grace_period: 60s", CYAN),
    "    environment:",
    ("      - TZ=America/Montevideo", CYAN),
    "    volumes:",
    ("      - omada-data:/opt/tplink/EAPController/data", CYAN),
    "      - omada-logs:/opt/tplink/EAPController/logs",
]
svg, h = codebox(48, 124, 640, code_lines, size=15, lh=30, title="/opt/omada/docker-compose.yml")
c.add(svg)
c.add(Step(48, 124, 2))
call = [(3, "El broadcast de descubrimiento llega", "ok"), (4, "Vuelve solo después de un reinicio", "info"),
        (5, "MongoDB cierra limpio al apagar", "ok"), (7, "Hora correcta en logs y programaciones", "info"),
        (9, "Acá vive toda la configuración", "warn")]
for i, s, kd in call:
    y = 124 + 30 + 4 + (i + 0.6) * 30
    c.add(f'<path d="M{690} {y - 5:.0f}H{716}" stroke="{CYAN}" stroke-width="2"/>')
    c.add(tag(724, y, s, kd, mono=False, anchor="start"))
c.add(Note(48, 530, 1104, "Para actualizar: docker compose pull && docker compose up -d. Nunca docker compose down -v: borra los volúmenes con toda la configuración.", title="Actualizar sin perder nada", kind="alert"))
save(c, "2-paso2.svg")

# ---------------------------------------------------------------- 2-paso4: asistente con cuenta local
c = Canvas(K(4), "En el asistente: cuenta local y región real")
c.add(code(48, 124, 520, "https://<IP-de-la-VM>:8043", 16))
c.add(text(48, 192, "Entrá cuando el log muestre la versión (1 a 2 minutos).", 16, 400, INK2, FB))
c.add(Window(48, 216, 520, 176, "Omada Controller · asistente", rows=[("Cuenta", "Create a Local Account"), ("Región", "Uruguay"), ("Zona horaria", "America/Montevideo")], hl=0))
c.add(Step(48, 216, 4))
c.add(Note(612, 124, 540, "El controlador no depende de la nube de TP-Link. El acceso remoto con TP-Link ID se puede sumar después, si hace falta.", title="Cuenta local", kind="ok"))
c.add(Note(612, 276, 540, "La región define qué canales y qué potencia son legales. Elegí el país donde están los AP, no el que viene marcado.", title="Región", kind="info"))
c.add(Note(612, 428, 540, "Cerrado el asistente, el EAP de la misma subred tiene que aparecer en Devices como Pending.", title="Prueba final (paso 5)", kind="ok"))
save(c, "2-paso4.svg")
