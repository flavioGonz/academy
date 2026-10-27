import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 1.svg: qué Windows es y qué cambió en SMB
c = Canvas(K(), "Antes que la IP: edición, versión y build")
c.add(NOLIG)
c.add(Window(48, 128, 520, 262, "HKLM:\\…\\Windows NT\\CurrentVersion",
             rows=[("EditionID", "Professional"), ("DisplayVersion", "24H2"), ("CurrentBuild", "26100"), ("UBR", "parche del mes")], hl=1))
c.add(text(68, 372, "Valores de ejemplo: en la obra, los del equipo.", 15, 400, INK3, FB))
c.add(panel(600, 128, 552, 262, "Desde 24H2 y Server 2025", "info"))
c.add(text(624, 196, "RequireSecuritySignature", 16, 600, INK, FM))
c.add(tag(1128, 196, "True", "ok", anchor="end"))
c.add(text(624, 222, "firma SMB obligatoria en cada conexión", 15, 400, INK3, FB))
c.add(hline(620, 1132, 246))
c.add(text(624, 282, "EnableInsecureGuestLogons", 16, 600, INK, FM))
c.add(tag(1128, 282, "False", "warn", anchor="end"))
c.add(text(624, 308, "Windows 11 Pro ya no entra como invitado", 15, 400, INK3, FB))
c.add(text(624, 350, "Get-SmbClientConfiguration", 15, 500, BLUE, FM))
# abajo: NAS viejo
pc = c.add(Laptop(48, 430, "Windows 11 24H2", "cliente SMB"))
nas = c.add(Generic(470, 430, "NAS o grabador viejo", "sin firma · invitado", icon="server", w=290, hl=ALERT))
c.add(Cable(pc.right(), nas.left(), kind="alert", label="\\\\IP\\carpeta"))
c.add(Mark(800, 472, ok=False))
c.add(text(830, 466, "\"Dejó de abrir\"", 18, 600, ALERT, FB))
c.add(text(830, 490, "y la red está bien", 16, 400, INK2, FB))
c.add(Note(48, 548, 1104, "Primero firmware del NAS o grabador, o una cuenta con contraseña propia del equipo. Volver a permitir invitados o quitar la firma deja el puesto más expuesto.", title="Qué conviene hacer", kind="warn"))
save(c, "1.svg")

# ---------------------------------------------------------------- 1-paso2: versión por registro
c = Canvas(K(2), "Los mismos datos de winver, por consola")
c.add(NOLIG)
c.add(Step(48, 140, 2))
c.add(text(80, 146, "Sirve también por escritorio remoto o en Server Core", 17, 600, INK2, FB))
sv, h = console(48, 176, 1104, [
    ">Get-ItemProperty 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion' |",
    ">>Select-Object EditionID, DisplayVersion, CurrentBuild, UBR",
    "",
    ("EditionID      DisplayVersion  CurrentBuild  UBR", "#7FA6C9"),
    ("---------      --------------  ------------  ---", "#7FA6C9"),
    ("Professional   24H2            26100         ....", "#D9E9F8"),
])
c.add(sv)
cols = [(62, "Edición", "Pro, Enterprise, Server…"), (344, "Versión", "24H2, 25H2…"), (626, "Build", "la base del sistema"), (908, "UBR", "sube con cada parche")]
for x, t, s in cols:
    c.add(rect(x - 14, 404, 258, 96, WHITE, LINE2, rx=14))
    c.add(text(x + 4, 438, t, 19, 600, INK, FD))
    c.add(text(x + 4, 466, s, 15, 400, INK3, FB))
c.add(Note(48, 528, 1104, "Anotalo en la planilla de obra junto con los dos valores de SMB: con edición, versión y build sabés qué reglas de seguridad trae ese Windows antes de culpar a la red.", title="Va a la planilla", kind="info"))
save(c, "1-paso2.svg")

# ---------------------------------------------------------------- 1-paso5: abrir la carpeta con usuario propio
c = Canvas(K(5), "Abrí la carpeta del NAS con un usuario del equipo")
c.add(NOLIG)
c.add(Step(65, 141, 5))
c.add(text(94, 147, "Probá las dos formas", 17, 600, INK2, FB))
pc = c.add(Laptop(48, 190, "Notebook", "Windows 11 24H2"))
c.add(code(48, 300, 300, "\\\\192.168.88.30\\video", 16))
c.add(panel(420, 128, 732, 168, None, "alert"))
c.add(Mark(458, 170, ok=False))
c.add(text(492, 177, "Como invitado, sin usuario", 20, 600, ALERT, FD))
svg, _ = wrap(444, 214, "Pro 24H2 ya no hace el acceso invitado: Windows no abre la carpeta aunque el NAS responda y el cable esté bien.", 680, 16, 400, INK2)
c.add(svg)
c.add(panel(420, 316, 732, 168, None, "ok"))
c.add(Mark(458, 358, ok=True))
c.add(text(492, 365, "Con usuario y contraseña del NAS", 20, 600, OK, FD))
svg, _ = wrap(444, 402, "Abre si el NAS también firma SMB. Si igual falla con usuario propio, el siguiente paso es el firmware del NAS o del grabador.", 680, 16, 400, INK2)
c.add(svg)
c.add(Cable((348, 320), (420, 212), kind="alert", bend="auto"))
c.add(Cable((348, 320), (420, 400), kind="ok", bend="auto"))
c.add(Note(48, 512, 1104, "La IP 192.168.88.30 y la carpeta video son de ejemplo. Bajar la seguridad del cliente SMB es la última opción, no la primera.", kind="warn"))
save(c, "1-paso5.svg")
