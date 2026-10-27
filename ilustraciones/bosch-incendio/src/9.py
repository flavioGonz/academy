import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 9.svg: secuencia de puesta en marcha
c = Canvas(K(), "Puesta en marcha: el orden que pide el manual")
groups = [("En el panel", BLUE, ["Alimentar", "Calibrar la pantalla", "Fecha, hora, PNA y red", "Reiniciar"]),
          ("Con FSP-5000-RPS", CYAN, ["Conectar por USB", "Autodetección", "Editar la configuración", "Descargar"]),
          ("Cerrar", OK, ["Walk test", "Pruebas funcionales", "Diagnóstico como acta"])]
n = 1
for gi, (g, col, items) in enumerate(groups):
    x = 48 + gi * 376
    c.add(rect(x, 130, 352, 380, WHITE, col, rx=16, sw=2.5))
    c.add(text(x + 22, 166, g, 20, 600, col, FD))
    for i, it in enumerate(items):
        y = 210 + i * 72
        c.add(badge(x + 40, y, str(n), col, r=17, size=16))
        c.add(text(x + 70, y + 6, it, 17, 600 if it in ("Descargar", "Diagnóstico como acta") else 500, INK))
        if i < len(items) - 1:
            c.add(f'<path d="M{x + 40} {y + 20}V{y + 52}" stroke="{col}" stroke-width="2" stroke-dasharray="4 4"/>')
        n += 1
    if gi < 2:
        c.add(arrow((x + 354, 320), (x + 374, 320)))
c.add(Note(48, 534, 540, "FSP-5000-RPS 5.15.28 en Windows 11 24H2 de 64 bits, bajado de la extranet de Bosch con usuario habilitado.", title="Versión vigente (octubre 2026)", kind="info"))
c.add(Note(612, 534, 540, "Una descarga cambia un sistema de seguridad de vida: en un sitio ocupado, con el monitoreo avisado y prueba funcional después.", title="En sitio ocupado", kind="warn"))
save(c, "9.svg")

# ---------------------------------------------------------------- 9-paso2: datos de la configuración de práctica
c = Canvas(K(2), "La configuración de práctica, de arriba abajo")
rows = [(0, "Versión de cuenta", "AVENAR panel 4.8"), (0, "País", "Uruguay"), (1, "Nodo 1", "AVENAR panel 2000 · PNA 1"),
        (2, "Riel, primera posición", "LSN 0300 A"), (3, "Lazo", "dirección manual · T-tap marcado"), (4, "10 detectores", "FAP-425-O-R · direcciones 1 a 10")]
for i, (lvl, k, v) in enumerate(rows):
    y = 140 + i * 70
    x = 70 + lvl * 46
    if lvl:
        c.add(f'<path d="M{x - 26} {y - 30}V{y + 22}H{x - 6}" fill="none" stroke="{LINE2}" stroke-width="2"/>')
    c.add(rect(x, y, 700 - lvl * 46, 52, DEEP if i < 2 else WHITE, DEEP if i < 2 else LINE2, rx=12))
    c.add(text(x + 18, y + 33, k, 17, 600, WHITE if i < 2 else INK, FB))
    c.add(text(420, y + 33, v, 16, 500, CYAN if i < 2 else BLUE, FM))
c.add(Note(820, 140, 332, "La cuenta 4.8 corresponde al firmware 4.8 y es la que agrega Uruguay a la lista de países.", title="Por qué 4.8", kind="info"))
c.add(Note(820, 300, 332, "Las perillas de los diez quedan en 001 a 010: con dirección manual se marca T-tap sea cual sea la topología.", title="Manual = T-tap", kind="info"))
c.add(text(48, 600, "Datos del laboratorio, no una captura de RPS: los nombres de los campos en pantalla pueden variar según la versión.", 15, 400, INK3))
save(c, "9-paso2.svg")

# ---------------------------------------------------------------- 9-paso3: chequeo de consistencia
c = Canvas(K(3), "Consistencia: errores, advertencias y pistas")
cols = [("Errores", "alert", ["Se corrigen antes de descargar", "Regla de obra: consistencia sin errores"]),
        ("Advertencias", "warn", ["Se leen una por una", "Se decide y se anota por qué queda así"]),
        ("Pistas", "info", ["Novedad de RPS 5.15.27", "Ayudan a ubicar qué corregir"])]
for i, (t, kd, ls) in enumerate(cols):
    x = 48 + i * 376
    c.add(panel(x, 140, 352, 170, t, kd, title_size=22))
    c.add(bullet_list(x + 24, 214, [(s, kd if kd != "info" else "info") for s in ls], 310, 17)[0])
c.add(Note(48, 344, 700, "Copiá cada error, advertencia y pista tal cual aparece, con el elemento al que se refiere. Esa lista es tu registro de qué corregiste antes de descargar.", title="Paso 3: anotá todo", kind="info"))
c.add(Note(780, 344, 372, "Guardá y exportá la configuración con la fecha en el nombre del archivo.", title="Paso 4", kind="ok"))
save(c, "9-paso3.svg")
