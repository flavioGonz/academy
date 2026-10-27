import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/unifi/src")
from _uf import *

# ---------------------------------------------------------------- 11.svg: actualizar por etapas
c = Canvas(K(), "Actualizar por etapas: nunca todos el mismo día")
st = [("1", "Backup", "dos copias fuera del equipo", "ok"),
      ("2", "Notas de versión", "qué pide, qué saca, qué migra", "info"),
      ("3", "Solo Official", "ni Release Candidate ni Beta", "info"),
      ("4", "Esperar", "HostiFi: 2 a 3 semanas", "info"),
      ("5", "Sitio piloto", "uno, con alguien atento", "warn"),
      ("6", "El resto", "recién ahí, por tandas", "ok")]
for i, (n_, a, b, kd) in enumerate(st):
    r, k = divmod(i, 3)
    x = 48 + k * 376 if r == 0 else 48 + (2 - k) * 376
    y = 132 + r * 170
    c.add(panel(x, y, 340, 124, None, kd))
    c.add(f'<circle cx="{x + 38}" cy="{y + 44}" r="20" fill="{CYAN}"/>' + mid(x + 38, y + 51, n_, 19, 700, WHITE, FD))
    c.add(text(x + 72, y + 52, a, 22, 600, INK, FD))
    c.add(text(x + 24, y + 96, b, 16, 400, INK2, FB))
c.add(arrow((392, 194), (420, 194)))
c.add(arrow((768, 194), (796, 194)))
c.add(wire([(970, 260), (970, 296)], kind="flow", arrow=True))
c.add(arrow((796, 364), (768, 364)))
c.add(arrow((420, 364), (392, 364)))
c.add(Note(48, 474, 540, "Network 10.5 y posteriores permiten revertir firmware y aplicación, y Test and Confirm deshace un cambio si perdés conexión.", title="Si igual sale mal", kind="info"))
c.add(Note(612, 474, 540, "HostiFi saltó la 7.5.174 por redes WiFi que no se emitían. Esperar y mirar los foros evita estrenar la falla.", title="Por qué esperar", kind="warn"))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso1: el backup y sus dos copias
c = Canvas(K(1), "Un backup, dos copias fuera del equipo")
con = c.add(Generic(48, 160, "Consola", "Settings > System > Backups", icon="server", w=360, dark=True))
c.add(rect(470, 166, 170, 72, WHITE, CYAN, rx=10, sw=2.5))
c.add(mid(555, 210, "backup .unf", 17, 600, INK, FM))
c.add(arrow((412, 202), (464, 202)))
n1 = c.add(Laptop(740, 128, "Copia 1", "notebook o NAS", w=380, hl=OK))
n2 = c.add(CloudBox(740, 236, "Copia 2", "otro lugar fuera del sitio", w=380, hl=OK))
c.add(arrow((646, 196), (734, 170), kind="ok"))
c.add(arrow((646, 210), (734, 278), kind="ok"))
c.add(Step(48, 160, 1))
c.add(panel(48, 360, 540, 160, "Lleva", "ok"))
lst, _ = bullet_list(72, 420, ["Configuración, dispositivos y clientes.", "Redes, WiFi, reglas y nombres de equipos."], 500, size=17)
c.add(lst)
c.add(panel(612, 360, 540, 160, "No lleva", "alert"))
lst, _ = bullet_list(636, 420, [("Video de Protect.", "alert"), ("Logs locales.", "alert")], 500, size=17)
c.add(lst)
c.add(text(48, 560, "Paso 2: revisá que el autobackup esté activo y con qué frecuencia.", 17, 500, INK2, FB))
save(c, "11-paso1.svg")

# ---------------------------------------------------------------- 11-paso3: restaurar en la VM
c = Canvas(K(3), "Restaurá en misma versión o superior")
flow = [("Consola de laboratorio", "Network versión X", "info"), ("UniFi OS Server en la VM", "versión X o superior", "ok"), ("Reinicia y pide login", "usuario del día del backup", "info")]
for i, (a, b, kd) in enumerate(flow):
    x = 48 + i * 376
    c.add(panel(x, 140, 340, 110, None, kd))
    c.add(text(x + 22, 186, a, 20, 600, INK, FD))
    c.add(text(x + 22, 218, b, 15, 500, INK3, FM))
    if i < 2:
        c.add(arrow((x + 344, 195), (x + 372, 195)))
c.add(tag(400, 282, ".unf: Restore > subir archivo", "info"))
c.add(Step(424, 140, 3))
c.add(panel(48, 330, 1104, 150, "Si los equipos quedan Disconnected", "warn", sub="cambió la IP del controlador: apuntalos al nuevo (paso 5)"))
for i, s in enumerate(["option 43", "DNS unifi", "set-inform"]):
    c.add(tag(90 + i * 200, 448, s, "warn", anchor="start"))
c.add(code(640, 418, 496, "set-inform http://<controlador-nuevo>:8080/inform", size=15))
c.add(Note(48, 506, 1104, "Restaurar no es infalible: Network 10.6.101 corrigió un caso en que se perdía la configuración MC-LAG al restaurar. Después de restaurar, revisá redes, WiFi y equipos.", kind="info"))
save(c, "11-paso3.svg")

# ---------------------------------------------------------------- 11-paso6: leer las notas de versión
c = Canvas(K(6), "Leé las notas antes del salto: el ejemplo de 11.0.97")
cols = [("Versión mínima", "info", ["UniFi OS 6.0 o superior.", "La actualización puede", "tardar hasta 20 minutos."]),
        ("Qué se elimina", "alert", ["Soporte a USG (10.6 fue", "la última que lo tuvo).", "El Network Server: el", "reemplazo es UniFi OS Server.", "El historial de estadísticas."]),
        ("Qué se migra", "warn", ["La base de datos, a", "PostgreSQL.", "Todos los sitios, al", "firewall por zonas."])]
for i, (t, kd, lines) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 132, 352, 236, t, kd))
    for k, s in enumerate(lines):
        c.add(text(x + 22, 200 + k * 32, s, 18, 400, INK2, FB))
c.add(Step(48, 132, 6))
c.add(Note(48, 400, 1104, "Un cliente con USG, o con un server que todavía no está en UniFi OS 6, no puede pasar a Network 11: se entera leyendo la nota, no el lunes. Las notas están en community.ui.com, sección Releases.", kind="ok"))
save(c, "11-paso6.svg")
