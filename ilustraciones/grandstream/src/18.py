import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _fxo import *

# ---------------------------------------------------------------- 18.svg: el método
c = Canvas(K(), "De la ficha a la configuración: el método")
pasos = [("1", "Foto del estado", "Dashboard, Active Calls y CDR antes de tocar nada", "info"),
         ("2", "Medí el par", "Tensión en reposo y descolgado, con el UCM desconectado", "info"),
         ("3", "Teléfono de prueba", "Tono, timbre y número en pantalla en la misma ficha", "info"),
         ("4", "Sacá lo que cuelga", "Alarma, posnet, fax y teléfonos: una línea, un equipo", "info"),
         ("5", "Cambiá el par de puerto", "La línea 2 al FXO1 y la 1 al FXO2: ¿la falla sigue a la línea?", "ok"),
         ("6", "Configuración y grabación", "Ruta entrante, detección, Analog Record Trace y syslog", "info")]
for i, (n, t, d, kd) in enumerate(pasos):
    col, row = i % 3, i // 3
    x, y = 48 + col * 376, 136 + row * 196
    c.add(panel(x, y, 352, 172, None, kd))
    c.add(f'<circle cx="{x + 34}" cy="{y + 36}" r="18" fill="{OK if kd == "ok" else CYAN}"/>')
    c.add(text(x + 34, y + 42, n, 17, 700, WHITE, FD, anchor="middle"))
    c.add(text(x + 64, y + 43, t, 19, 600, INK, FD))
    svg, _ = wrap(x + 24, y + 86, d, 310, 16, 400, INK2)
    c.add(svg)
    if col < 2:
        c.add(Arrow((x + 352, y + 86), (x + 376, y + 86), kind="flow"))
c.add(f'<path d="M1076 308V320H224V332" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round" marker-end="url(#a-blue)"/>')
c.add(Note(48, 540, 540, "Si la falla sigue a la línea: reclamo a Antel al 121, con número, síntoma, horario y mediciones.", kind="warn", size=16))
c.add(Note(612, 540, 540, "Si se queda en el puerto: es la central. Configuración, detección y, si hace falta, el puerto.", kind="info", size=16))
save(c, "18.svg")

# ---------------------------------------------------------------- 18-paso5: cambiar el par de puerto
c = Canvas(K(5), "Cambiá el par de puerto: la falla dice de qué lado está")
# antes
c.add(panel(48, 132, 540, 250, "Antes", "info"))
c.add(dev(72, 190, "Línea 1", "par A", icon="central", w=200, h=70))
c.add(dev(72, 286, "Línea 2", "par B · falla", icon="central", w=200, h=70, hl=WARN))
for i, (lab, st) in enumerate([("FXO1", "libre"), ("FXO2", "uso")]):
    y = 196 + i * 96
    col = {"libre": LIBRE, "uso": USO}[st]
    c.add(f'<rect x="420" y="{y}" width="140" height="58" rx="10" fill="{col}"/>')
    c.add(text(490, y + 36, lab, 18, 700, WHITE, FM, anchor="middle"))
c.add(par([(272, 225), (420, 225)], w=2))
c.add(par([(272, 321), (420, 321)], w=2))
# después
c.add(panel(612, 132, 540, 250, "Después de cruzar los pares", "info"))
c.add(dev(636, 190, "Línea 2", "par B", icon="central", w=200, h=70, hl=WARN))
c.add(dev(636, 286, "Línea 1", "par A", icon="central", w=200, h=70))
for i, lab in enumerate(["FXO1", "FXO2"]):
    y = 196 + i * 96
    c.add(f'<rect x="984" y="{y}" width="140" height="58" rx="10" fill="#2C4A66"/>')
    c.add(text(1054, y + 36, lab, 18, 700, WHITE, FM, anchor="middle"))
c.add(par([(836, 225), (984, 225)], w=2))
c.add(par([(836, 321), (984, 321)], w=2))
c.add(Step(48, 132, 5))
# resultados
c.add(panel(48, 404, 540, 130, "La falla pasa al FXO1", "warn"))
svg, _ = wrap(68, 466, "Sigue a la línea 2: es la línea o algo conectado en ella. Revisá lo que cuelga del par y, si sigue, reclamo a Antel.", 500, 16, 400, INK2)
c.add(svg)
c.add(panel(612, 404, 540, 130, "La falla se queda en el FXO2", "info"))
svg, _ = wrap(632, 466, "Se queda en el puerto: es la central. Troncal, ruta entrante y detección de ese puerto; después, el hardware.", 500, 16, 400, INK2)
c.add(svg)
c.add(Note(48, 560, 1104, "Al terminar, volvé cada par a su puerto: las troncales Antel_Linea1 y Antel_Linea2 están atadas al FXO1 y al FXO2.", kind="info", size=16))
save(c, "18-paso5.svg")
