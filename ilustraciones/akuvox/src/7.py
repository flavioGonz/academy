from _akv import *

# ---------- 7.svg: público vs por persona
c = Canvas("Akuvox · Lección 7", "Un código para todos o una credencial por persona")
c.add(panel(48, 140, 470, 460, "PIN público", "alert"))
c.add(text(72, 220, "33333333", 40, 600, ALERT, FM))
c.add(text(72, 250, "de fábrica, igual para todos", 15, 500, INK3, FM))
for i in range(6):
    c.add(icon(76 + i * 62, 290, "user", ALERT, 1.5))
svg, _ = bullet_list(72, 380, [("Se muda un vecino: el código hay que cambiarlo para todos", "alert"),
                              ("No sabés quién abrió", "alert"),
                              ("Sin horario: entra a cualquier hora", "alert")], 420)
c.add(svg)
c.add(panel(560, 140, 592, 460, "Usuario con credenciales propias", "ok"))
c.add(Table(584, 190, ["Campo", "Ejemplo"], [["PIN privado", "482913"], ["Tarjetas", "hasta 5 por usuario"], ["Rostro", "si el modelo lo tiene"],
                                             ["Relé", "Relay A"], ["Horario", "Lun a Vie 08 a 18"]], [200, 344], row_h=44, mono_cols=()))
c.add(Note(584, 470, 544, "Se da de baja una persona y el resto sigue igual. Cada uno entra solo en su horario.", kind="ok", size=16))
save(c, "7.svg")

# ---------- 7-paso5.svg: carga masiva
c = Canvas("Akuvox · Lección 7 · Paso 5", "Carga masiva: exportá, editá el .csv y reimportá")
st = [("Export", "Directory > User", ".tgz"), ("Descomprimir", "7-Zip en Windows", ".csv adentro"), ("Editar", "una fila por usuario", ".csv"),
      ("Comprimir", "de nuevo en .tgz", ".tgz"), ("Import", "Select File > Import", "listo")]
for i, (a, b, ch) in enumerate(st):
    x = 48 + i * 224
    c.add(f'<rect x="{x}" y="150" width="200" height="130" rx="16" fill="{WHITE}" stroke="{CYAN if i == 3 else LINE2}" stroke-width="{2.5 if i == 3 else 1.5}"/>')
    c.add(text(x + 18, 190, a, 19, 600, INK, FD))
    svg, _ = wrap(x + 18, 218, b, 170, 15, 500, INK3, FM)
    c.add(svg)
    c.add(Chip(x + 18, 266, ch, "gray"))
    if i < 4:
        c.add(Arrow((x + 203, 215), (x + 221, 215)))
c.add(Step(48 + 3 * 224, 150, 5))
c.add(Terminal(48, 330, 640, ["UserID,Name,PIN Code,Card Code", "1003,Prueba Tres,482913,", "1004,Prueba Cuatro,559107,", "1005,Prueba Cinco,603418,"], title="USUARIOS.CSV"))
c.add(Note(720, 330, 432, "Respetá las columnas que exportó el equipo. Para 200 vecinos de un edificio, esto ahorra una tarde de carga a mano.", title="Por qué así", kind="info", size=15))
save(c, "7-paso5.svg")

# ---------- 7-paso6.svg: horario
c = Canvas("Akuvox · Lección 7 · Paso 6", "El PIN vale solo dentro de su horario")
x0, x1, y = 120, 1080, 300
c.add(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="40" rx="10" fill="{SOFT}" stroke="{LINE2}"/>')
hx = lambda h: x0 + (x1 - x0) * h / 24
c.add(f'<rect x="{hx(8):.0f}" y="{y}" width="{hx(18) - hx(8):.0f}" height="40" rx="6" fill="{OK_BG}" stroke="{OK}" stroke-width="2"/>')
c.add(text((hx(8) + hx(18)) / 2, y + 27, "Lun a Vie 08 a 18", 17, 600, OK, FB, anchor="middle"))
for h in (0, 8, 12, 18, 24):
    c.add(text(hx(h), y + 70, f"{h:02d}:00", 15, 500, INK3, FM, anchor="middle"))
for h, ok, lab in ((7.5, False, "PIN 07:30"), (10, True, "PIN 10:00"), (19.5, False, "PIN 19:30")):
    c.add(f'<path d="M{hx(h):.0f} {y - 60}V{y - 4}" stroke="{OK if ok else ALERT}" stroke-width="3"/>')
    c.add(Mark(hx(h), y - 84, ok=ok))
    c.add(text(hx(h), y - 116, lab, 15, 600, OK if ok else ALERT, FM, anchor="middle"))
c.add(Chip(hx(10), y + 110, "abre", "ok", mono=False, anchor="middle"))
c.add(Chip(hx(7.5), y + 110, "rechaza", "alert", mono=False, anchor="middle"))
c.add(Chip(hx(19.5), y + 110, "rechaza", "alert", mono=False, anchor="middle"))
c.add(Note(120, 480, 960, "Para probar sin esperar a la noche, cambiá la hora del equipo y repetí el PIN. Un usuario en “Always” entra siempre: dejalo solo para quien de verdad lo necesita.", kind="info"))
c.add(Step(120, 180, 6))
save(c, "7-paso6.svg")
