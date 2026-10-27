import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/windows/src")
from _win import *

# ---------------------------------------------------------------- 11.svg: actualizar con calendario y con red
c = Canvas(K(), "Actualizar sí: con calendario, aviso y backup antes")
c.add(NOLIG)
cols = [("1", "Backup restaurable", "wbadmin -allCritical", "la única marcha atrás real", "ok"),
        ("2", "Momento elegido", "horas activas · ventana", "nada de reinicios sorpresa", "info"),
        ("3", "Aviso en servidores", "avisar para instalar y reiniciar", "opción 7 de Microsoft", "info"),
        ("4", "Verificar", "Get-HotFix · evento 1074", "qué entró y quién reinició", "info")]
for i, (n, t, cmd, s, kd) in enumerate(cols):
    x = 48 + i * 280
    c.add(panel(x, 128, 256, 230, None, "ok" if kd == "ok" else "info"))
    c.add(badge(x + 34, 168, n, OK if kd == "ok" else CYAN))
    c.add(text(x + 62, 175, t, 17, 600, OK if kd == "ok" else INK, FD))
    svg, _ = wrap(x + 20, 222, cmd, 220, 15, 600, BLUE, FM)
    c.add(svg)
    svg, _ = wrap(x + 20, 296, s, 220, 15, 400, INK2)
    c.add(svg)
    if i < 3:
        c.add(arrow((x + 258, 243), (x + 278, 243), "flow"))
c.add(panel(48, 384, 540, 150, "Ciclo validado con el VMS", "info"))
svg, _ = wrap(72, 446, "Bosch pide para su VMS un ciclo de actualización de 6 meses como máximo. Lo que diga el fabricante del VMS instalado va primero.", 500, 16, 400, INK2)
c.add(svg)
c.add(panel(612, 384, 540, 150, "Noviembre de 2024", "alert"))
svg, _ = wrap(636, 446, "Servidores con Windows Server 2022 amanecieron actualizados a 2025, sin licencia, por una actualización mal clasificada. Sin backup, quedaba reinstalar o pagar.", 500, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 558, 1104, "Antes de actualizar, backup. Siempre.", kind="ok"))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso1: horas activas
c = Canvas(K(1), "Horas activas: Windows reinicia fuera de ese rango")
c.add(NOLIG)
c.add(Step(65, 141, 1))
c.add(text(94, 147, "Configuración > Windows Update > Opciones avanzadas > Horas activas", 17, 600, INK2, FB))
X0, W = 80, 1040
c.add(rect(X0, 220, W, 70, WHITE, LINE2, rx=12))
c.add(f'<rect x="{X0 + W * 8 / 24:.0f}" y="220" width="{W * 9 / 24:.0f}" height="70" rx="12" fill="{OK_BG}" stroke="{OK}" stroke-width="2"/>')
c.add(mid(X0 + W * 12.5 / 24, 262, "horas activas: no reinicia", 17, 600, OK, FB))
c.add(mid(X0 + W * 3.5 / 24, 262, "puede reiniciar", 16, 500, INK3, FB))
c.add(mid(X0 + W * 20.5 / 24, 262, "puede reiniciar", 16, 500, INK3, FB))
for h in range(0, 25, 4):
    x = X0 + W * h / 24
    c.add(f'<path d="M{x:.0f} 292V302" stroke="{INK3}" stroke-width="2"/>')
    c.add(mid(x, 324, f"{h:02d}:00" if h < 24 else "24:00", 14, 500, INK3, FM))
c.add(text(X0 + W * 8 / 24, 208, "8:00", 15, 600, OK, FM, anchor="middle"))
c.add(text(X0 + W * 17 / 24, 208, "17:00", 15, 600, OK, FM, anchor="middle"))
c.add(Note(48, 360, 540, "De fábrica van de 8 a 17 y el rango máximo es de 18 horas. Ajustalas al horario de operación del cliente.", title="Valores", kind="info"))
c.add(Note(612, 360, 540, "Solo cuenta como usuario conectado una sesión local o de escritorio remoto activa: sin nadie, el equipo se reinicia cuando le toca.", title="Sin sesión, reinicia", kind="warn"))
save(c, "11-paso1.svg")

# ---------------------------------------------------------------- 11-paso4: el backup con wbadmin
c = Canvas(K(4), "Backup de los volúmenes críticos a un segundo disco")
c.add(NOLIG)
c.add(Step(65, 141, 4))
c.add(text(94, 147, "Windows Server 2025 de prueba, con un disco E: aparte", 17, 600, INK2, FB))
sv, h = console(48, 172, 1104, [
    ">wbadmin start backup -backupTarget:E: -allCritical -quiet",
    ">wbadmin get versions -backupTarget:E:",
    ("Identificador de versión: (fecha-hora del backup)", "#9FE3F7"),
], title="Símbolo del sistema (administrador)", prompt="C:\\> ")
c.add(sv)
c.add(crow(48, 172, 1104, 2))
srv = c.add(Server(48, 360, "Servidor", "C: y volúmenes críticos", w=300))
dsk = c.add(Generic(480, 360, "Disco E:", "destino del backup", icon="server", w=300, hl=OK))
c.add(Arrow(srv.right(), dsk.left(), label="-allCritical"))
c.add(panel(840, 340, 312, 124, "Paso 5: a la planilla", "ok", title_size=16))
c.add(text(864, 404, "identificador y fecha", 16, 500, INK2, FB))
c.add(text(864, 432, "de esta versión", 16, 500, INK2, FB))
c.add(Note(48, 488, 1104, "-allCritical incluye lo necesario para restaurar el sistema. Un backup se confirma restaurando: en el paso 6, un archivo a otra carpeta con -recoveryTarget. -recreateDisks borra datos: solo si sabés lo que hace.", kind="warn"))
save(c, "11-paso4.svg")
