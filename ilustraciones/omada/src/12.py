import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omada/src")
from _om import *

# ---------------------------------------------------------------- 12.svg: backup por versión y saltos de a uno
c = Canvas(K(), "Antes de actualizar, backup. Y uno por versión")
for i, (v, f) in enumerate([("Controlador 5.x", "backup-5.x.cfg"), ("Controlador 6.x", "backup-6.x.cfg")]):
    x = 120 + i * 560
    c.add(Generic(x, 140, v, "", icon="server", w=360, dark=True))
    c.add(rect(x + 40, 252, 280, 46, WHITE, BLUE, rx=10))
    c.add(icon(x + 54, 262, "card", BLUE, 1.0))
    c.add(text(x + 90, 282, f, 16, 600, INK, FM))
c.add(arrow((484, 182), (676, 182), kind="ok"))
c.add(mid(580, 166, "de a una versión mayor", 15, 600, OK, FB))
c.add(f'<path d="M860 300V352H300V306" fill="none" stroke="{ALERT}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a-alert)"/>')
c.add(tag(580, 360, "backup de 6.x en un 5.x: no entra", "alert", mono=False))
c.add(Mark(800, 352, ok=False))
c.add(text(120, 420, "Volver atrás es reinstalar:", 18, 600, INK, FB))
c.add(lines(120, 450, ["desinstalar sin guardar datos, instalar la versión vieja", "y restaurar el backup de esa misma versión."], 16, 26))
c.add(Note(48, 510, 352, "Programado y guardado fuera del controlador: si muere el host, el backup sigue.", title="Fuera del equipo", kind="ok"))
c.add(Note(424, 510, 352, "De 5.x a 6.x sin saltear, verificando que arranque limpio en cada paso.", title="Saltos de a uno", kind="info"))
c.add(Note(800, 510, 352, "Beta y Release Candidate, solo en laboratorio. En producción, estable.", title="Canales", kind="warn"))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso1: backup programado fuera del equipo
c = Canvas(K(1), "Backup programado, guardado en otro equipo")
c.add(Window(48, 124, 600, 290, "Omada · Global", path="Settings > Maintenance > Backup Schedule", rows=[
    ("Estado", "activado"), ("Frecuencia", "semanal"), ("Día y hora", "domingo 3:00"), ("Contenido", "Configuration"), ("Destino", "Save to File Server")], hl=4))
c.add(Step(48, 124, 1))
c.add(Generic(712, 140, "Controlador", "VM o contenedor", icon="server", w=300, dark=True))
c.add(Generic(712, 322, "Servidor de archivos", "SFTP, otro host", icon="server", w=300))
c.add(arrow((862, 228), (862, 316), kind="ok"))
c.add(text(880, 278, ".cfg semanal", 15, 600, OK, FM))
c.add(code(48, 444, 1104, "omada-lab_v6.2.10.17_2026-10-27.cfg", 16, h=44))
c.add(text(48, 518, "Paso 2: el export a mano lleva la versión en el nombre. Así sabés en qué versión se restaura.", 16, 500, INK2, FB))
c.add(Note(48, 548, 1104, "Un Administrator común no programa backups automáticos: lo hace el Main Administrator.", kind="info"))
save(c, "12-paso1.svg")

# ---------------------------------------------------------------- 12-paso3: copia del volumen en Docker
c = Canvas(K(3), "En Docker, también el volumen, con el contenedor parado")
svg, h = codebox(48, 124, 1104, [
    "cd /opt/omada && docker compose stop",
    ("sudo tar czf ~/omada-data-$(date +%F).tar.gz -C /var/lib/docker/volumes/omada_omada-data/_data .", CYAN),
    "docker compose start"], size=15, lh=34, title="VM LINUX")
c.add(svg)
c.add(Step(48, 124, 3))
steps = [("Parar", "MongoDB cierra limpio y no se copia a mitad de escritura", "info"),
         ("Copiar", "el volumen omada-data entero, en un .tar.gz con fecha", "ok"),
         ("Arrancar", "el controlador vuelve en 1 a 2 minutos", "info")]
for i, (t, d, kd) in enumerate(steps):
    x = 48 + i * 376
    c.add(panel(x, 300, 352, 130, None, kd))
    c.add(badge(x + 34, 338, str(i + 1)))
    c.add(text(x + 62, 345, t, 20, 600, INK, FD))
    svg2, _ = wrap(x + 24, 384, d, 310, 16, 400, INK2)
    c.add(svg2)
c.add(Note(48, 456, 540, "Ese .tar.gz más el docker-compose.yml alcanzan para rearmar el controlador en otro host.", title="Qué te salva", kind="ok"))
c.add(Note(612, 456, 540, "Nunca docker compose down -v: borra los volúmenes con toda la configuración.", title="Lo que te hunde", kind="alert"))
save(c, "12-paso3.svg")

# ---------------------------------------------------------------- 12-paso5: migración en orden
c = Canvas(K(5), "Migrar en orden: Forget recién al final")
flow = [("Exportar", "Global View >", "Settings > Migration"), ("Importar", "en el destino, misma", "Major.Minor.Patch"),
        ("Migrar equipos", "con la IP o la", "Inform URL nueva"), ("Forget", "en el viejo, cuando", "todos estén Connected")]
for i, (t, a, b) in enumerate(flow):
    x = 48 + i * 282
    kd = "ok" if i == 3 else "info"
    c.add(panel(x, 128, 254, 150, None, kd))
    c.add(badge(x + 34, 166, str(i + 1)))
    c.add(text(x + 62, 173, t, 20, 600, INK, FD))
    c.add(text(x + 24, 220, a, 15, 500, INK2, FB))
    c.add(text(x + 24, 246, b, 15, 500, INK2, FM if "." in b or "URL" in b else FB))
    if i < 3:
        c.add(arrow((x + 258, 203), (x + 278, 203)))
c.add(Step(48, 128, 5))
c.add(Note(48, 310, 540, "Desde la 5.15.24, si salteás la importación y pasás directo a migrar equipos, el destino no los adopta solo.", title="Saltear el paso 2", kind="alert"))
c.add(Note(612, 310, 540, "Desde la 5.13.11.41 solo se importa un archivo de la misma Major.Minor.Patch, por ejemplo 5.13.11.", title="Misma versión", kind="warn"))
c.add(Note(48, 450, 540, "El backup de un ER7212PC solo vuelve a otro ER7212PC: no se cruza con software, OC ni Central.", title="ER7212PC", kind="info"))
c.add(Note(612, 450, 540, "Pasar de un controlador local a la nube deja los equipos Unactivated hasta asignarles licencia.", title="Hacia la nube", kind="info"))
save(c, "12-paso5.svg")
