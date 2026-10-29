"""Lección 17 · Elegir el canal."""
from _comun_12_22 import *

K = "MikroTik"

# ---------------------------------------------------------------- principal: los cuatro canales
c = Canvas(K, "Cuatro canales: de lo más probado a lo más nuevo")
c.add(Arrow((60, 150), (1140, 150), bend="straight", kind="flow"))
c.add(Label(60, 136, "más probado, sale poco", 15, 500, INK3, FM))
c.add(Label(1140, 136, "más nuevo, sale seguido", 15, 500, INK3, FM, anchor="end"))
chans = [
    ("long-term", "ok", "Sale poco", "Solo arreglos críticos, sin funciones nuevas en su rama.", "Sitios de clientes, por defecto."),
    ("stable", "warn", "Cada pocos meses", "Funciones nuevas ya probadas.", "Solo si necesitás una función nueva y la probaste en el banco."),
    ("testing", "alert", "Cada pocas semanas", "Prueba interna básica.", "No va en producción. Solo tu banco."),
    ("development", "alert", "Lo último", "Para probar lo que viene.", "Solo tu banco."),
]
wc, gap = 258, 24
for i, (nm, kind, freq, what, where) in enumerate(chans):
    x = 48 + i * (wc + gap)
    c.add(panel(x, 180, wc, 360, None, "info"))
    c.add(pill(x + 18, 198, wc - 36, 46, nm, {"ok": OK, "warn": WARN, "alert": ALERT}[kind], WHITE, 17))
    c.add(text(x + 20, 284, freq, 17, 600, INK, FD))
    c.add(para(x + 20, 314, what, wc - 40, 16, INK2))
    c.add(line(x + 20, 404, x + wc - 20, 404, LINE, 1.5))
    c.add(text(x + 20, 434, "EN CLIENTES", 13, 600, INK3, FM, ls=1.2))
    c.add(para(x + 20, 462, where, wc - 40, 16, {"ok": OK, "warn": WARN, "alert": ALERT}[kind], 600))
c.add(Label(48, 590, "Se cambia en Check for Updates o con /system/package/update/set channel=long-term", 17, 500, INK2))
save(c, "17.svg")

# ---------------------------------------------------------------- paso 3: decidir
c = Canvas(K + " · Paso 3", "¿Qué canal le dejo a este equipo?")
q1 = c.add(Box(48, 150, 330, 96, "¿Es tu banco de pruebas?", "", hl=CYAN))
q2 = c.add(Box(48, 360, 330, 120, "", "", hl=CYAN))
c.add(para(68, 410, "¿Necesitás una función que solo trae stable?", 290, 19, INK, 600))
r1 = c.add(Box(560, 150, 300, 96, "testing o development", "solo en el banco", hl=ALERT))
r2 = c.add(Box(560, 300, 300, 96, "long-term", "sitio que se visita poco", hl=OK))
r3 = c.add(Box(560, 450, 300, 96, "stable", "probado antes en el banco", hl=WARN))
c.add(Arrow(q1.right(), r1.left(), "sí", bend="straight", label_dy=-12))
c.add(Arrow(q1.bottom(), q2.top(), "no, es de un cliente", bend="straight", label_dy=0))
c.add(Arrow(q2.right(-20), r2.left(), "no", label_dy=-8))
c.add(Arrow(q2.right(20), r3.left(), "sí", label_dy=8))
c.add(Note(900, 150, 252, "Todos los equipos del mismo cliente, en el mismo canal.", title="Flota pareja", kind="ok"))
c.add(Note(900, 330, 252, "Anotá en el legajo canal, versión y fecha.", title="Legajo", kind="info"))
c.add(Terminal(48, 570, 1104, ["/system/package/update/set channel=long-term"], title="EL QUE QUEDA EN CLIENTES"))
save(c, "17-paso3.svg")
