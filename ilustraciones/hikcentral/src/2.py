import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/hikcentral/src")
from _hc import *

# ---------------------------------------------------------------- 2.svg: perfiles de hardware y virtualización
c = Canvas(K(), "Dimensioná el SYS con la guía, no a ojo")
c.add(panel(48, 124, 540, 250, "Perfil bajo", "info", sub="guía de requisitos V2.4.510"))
c.add(lines(72, 220, ["CPU: Intel Core i5-8500", "RAM: 8 GB", "Red: NIC gigabit", "Disco: 650 GB como mínimo"], 18, 34, INK2, FM))
c.add(panel(612, 124, 540, 250, "Alto rendimiento", "info", sub="guía de requisitos V2.4.510"))
c.add(lines(636, 220, ["CPU: Xeon E-2314 o E-2378", "RAM: 16 GB (recomiendan 32 GB)", "Red: NIC gigabit", "Disco: 650 GB como mínimo"], 18, 34, INK2, FM))
rows = [("SYS en máquina virtual", "sí: ESXi 6.x o 7.x, Hyper-V", True),
        ("Control Client en máquina virtual", "no corre", False),
        ("Migrar la VM del SYS (vMotion o similar)", "rompe la verificación de licencia", False)]
for i, (a, b, ok) in enumerate(rows):
    y = 412 + i * 54
    c.add(Mark(66, y + 18, ok))
    c.add(text(100, y + 25, a, 18, 600, INK))
    c.add(text(560, y + 25, b, 17, 500, OK if ok else ALERT, FM))
c.add(text(48, 640, "Para V3.x, confirmá las cifras en la guía de requisitos de esa versión.", 16, 500, WARN))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso2: verificar el hash
c = Canvas(K(2), "Compará el hash antes de instalar")
f = c.add(Generic(48, 150, "HikCentral_Professional.exe", "instalador descargado", icon="server", w=360))
c.add(code(460, 160, 690, "Get-FileHash .\\HikCentral_Professional.exe -Algorithm MD5", 15, h=60))
c.add(Arrow(f.right(), (456, 190)))
c.add(panel(48, 280, 540, 120, "Valor que da PowerShell", "info"))
c.add(text(72, 360, "MD5  …el que te devuelva el comando", 17, 500, INK2, FM))
c.add(panel(612, 280, 540, 120, "Valor publicado en la descarga", "info"))
c.add(text(636, 360, "MD5  …el de la página de Hikvision", 17, 500, INK2, FM))
c.add(Note(48, 428, 540, "El archivo está completo y es el que publicó el fabricante. Seguí: clic derecho > Ejecutar como administrador.", title="Iguales: instalá", kind="ok"))
c.add(Note(612, 428, 540, "Descarga cortada o archivo cambiado. Bajalo de nuevo de la página oficial y volvé a comparar.", title="Distintos: no lo corras", kind="alert"))
c.add(text(48, 620, "El FAQ lo indica cuando el paquete no arranca: el MD5 tiene que ser igual al de la página de descarga.", 16, 400, INK3))
save(c, "2-paso2.svg")

# ---------------------------------------------------------------- 2-paso3: típica o personalizada
c = Canvas(K(3), "Típica para un servidor, personalizada para separar")
c.add(panel(48, 124, 540, 380, "Instalación típica", "ok"))
c.add(rect(72, 174, 492, 196, WHITE, OK, rx=14))
c.add(text(92, 204, "UNA PC", 14, 600, OK, FM, ls=1.5))
for i, m in enumerate(["SYS (gestión)", "Base de datos", "Streaming Gateway", "Control Client"]):
    c.add(tag(92 + (i % 2) * 236, 252 + (i // 2) * 52, m, "ok", 15, False, anchor="start"))
c.add(text(92, 352, "Todo menos el Streaming Server.", 17, 500, INK2))
c.add(text(72, 410, "Para el laboratorio y la mayoría de las obras:", 16, 400, INK2))
c.add(text(72, 436, "un servidor con SYS, base y clientes.", 16, 400, INK2))
c.add(panel(612, 124, 540, 380, "Instalación personalizada", "info"))
c.add(rect(636, 174, 230, 120, WHITE, LINE2, rx=14))
c.add(text(656, 204, "PC 1", 14, 600, INK3, FM, ls=1.5))
c.add(tag(656, 252, "SYS", "info", 15, False, anchor="start"))
c.add(rect(898, 174, 230, 120, WHITE, LINE2, rx=14))
c.add(text(918, 204, "PC 2", 14, 600, INK3, FM, ls=1.5))
c.add(tag(918, 252, "Streaming Server", "info", 15, False, anchor="start"))
c.add(text(636, 336, "Elegís módulos y carpetas.", 17, 500, INK2))
c.add(text(636, 366, "SYS y Streaming Server nunca en la misma PC.", 17, 500, INK2))
c.add(text(636, 410, "Acá también se decide Normal o", 16, 400, INK2))
c.add(text(636, 436, "Mirror Hot Spare (servidor de respaldo).", 16, 400, INK2))
c.add(Note(48, 528, 1104, "Clic derecho > Ejecutar como administrador. Sin permisos de administrador, la instalación falla. Si el asistente pide reiniciar, reiniciá.", title="Siempre como administrador", kind="warn"))
save(c, "2-paso3.svg")

# ---------------------------------------------------------------- 2-paso5: quién tiene el puerto
c = Canvas(K(5), "Puerto en rojo: averiguá quién lo tiene tomado")
c.add(code(48, 130, 520, "netstat -ano | findstr :80", 16, h=48))
c.add(Step(48, 130, 5))
c.add(text(48, 210, "La última columna es el PID del proceso que escucha.", 16, 400, INK2))
c.add(code(48, 228, 520, "TCP  0.0.0.0:80  …  LISTENING  4321", 16, h=48))
c.add(code(632, 130, 520, "tasklist | findstr 4321", 16, h=48))
c.add(text(632, 210, "Con el PID, el nombre del programa.", 16, 400, INK2))
c.add(code(632, 228, 520, "otro-programa.exe   4321 …", 16, h=48))
c.add(Arrow((574, 240), (626, 172), bend="straight"))
c.add(text(48, 334, "Dos salidas, según lo que diga el cliente:", 19, 600, INK, FD))
c.add(Note(48, 360, 540, "Si ese programa no hace falta en el servidor, lo cerrás o lo desinstalás. Antes, pedí permiso: puede ser otro servicio del cliente.", title="A. Cerrar el proceso, con autorización", kind="warn"))
c.add(Note(612, 360, 540, "Cambiás el puerto del servicio en Service Manager y entrás con el puerto en la URL.", title="B. Cambiar el puerto del SYS", kind="info"))
c.add(code(612, 500, 540, "http://192.168.88.10:81", 17, color="#9FE0C0", h=48))
save(c, "2-paso5.svg")
