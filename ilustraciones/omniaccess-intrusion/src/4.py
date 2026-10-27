from _oai import *

DIAS = ["L", "M", "X", "J", "V", "S", "D"]


def semana(x, y, w, filas, alto=22, gap=10, ahora=None, etiqueta_x=36):
    """filas: lista de (dia, [(desde_h, hasta_h, color)])"""
    out = []
    W = w - etiqueta_x
    for h in (0, 6, 12, 18, 24):
        hx = x + etiqueta_x + W * h / 24
        out.append(text(hx, y - 10, f"{h:02d}", 13, 500, INK3, FM, anchor="middle"))
    for i, (d, bloques) in enumerate(filas):
        yy = y + i * (alto + gap)
        out.append(text(x, yy + alto - 5, d, 15, 700, INK2, FM))
        out.append(f'<rect x="{x + etiqueta_x}" y="{yy}" width="{W}" height="{alto}" rx="5" fill="{SOFT}"/>')
        for a, b, col in bloques:
            out.append(f'<rect x="{x + etiqueta_x + W * a / 24:.1f}" y="{yy}" width="{W * (b - a) / 24:.1f}" height="{alto}" rx="4" fill="{col}"/>')
    if ahora is not None:
        ax = x + etiqueta_x + W * ahora / 24
        tot = len(filas) * (alto + gap)
        out.append(f'<path d="M{ax} {y - 4}V{y + tot}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 4"/>')
        out.append(text(ax, y + tot + 18, "ahora 15:00", 13, 600, INK, FM, anchor="middle"))
    return "".join(out)


# ---------- 4.svg
c = Canvas("OmniAccess Intrusión · Lección 4", "Grabar no es avisar: el armado decide")
c.add(text(48, 158, "Grabación del NVR", 18, 600, INK, FD))
c.add(text(48, 180, "24 horas, todos los días", 15, 500, INK3, FM))
c.add(semana(48, 212, 520, [(d, [(0, 24, "#7FB2E5")]) for d in DIAS], ahora=15))
c.add(text(632, 158, "Armado de la línea en la cámara", 18, 600, INK, FD))
c.add(text(632, 180, "línea L–D 22:00–06:00", 15, 500, OK, FM))
c.add(semana(632, 212, 520, [(d, [(0, 6, OK), (22, 24, OK)]) for d in DIAS], ahora=15))
c.add(Note(48, 470, 520, "Fuera del horario la cámara sigue grabando en el NVR, pero no avisa nada: ni cruce, ni zona, ni foto.", kind="warn", size=16))
c.add(Note(632, 470, 520, "A las 15:00 la línea está desarmada: punto ámbar en la vista de pared. A las 22:00 pasa a verde.", kind="info", size=16))
save(c, "4.svg")

# ---------- 4-paso3.svg: el horario en la web de la cámara
c = Canvas("OmniAccess Intrusión · Lección 4 · Paso 3", "En la cámara, la noche se carga en dos bloques")
c.add(panel(48, 140, 700, 440, "Programación de armado · Detección de cruce de línea", kind="info", title_size=17))
c.add(semana(72, 220, 652, [(d, [(0, 6, OK), (22, 24, OK)]) for d in DIAS], alto=26, gap=12))
c.add(text(72, 520, "Bloque 1: 00:00 a 06:00   ·   Bloque 2: 22:00 a 24:00", 15, 500, BLUE, FM))
c.add(button(72, 536, 200, "Copiar a todos", "light", 15, 34))
c.add(button(284, 536, 120, "Guardar", "dark", 15, 34))
c.add(Step(48, 140, 3))
c.add(Note(780, 140, 372, "Un rango que cruza la medianoche se guarda partido: el día termina en 24:00 y el siguiente arranca en 00:00.", title="22:00 a 06:00", kind="info", size=15))
c.add(Note(780, 330, 372, "OmniAccess lo vuelve a juntar y lo muestra como L–D 22:00–06:00. Se relee cada 5 minutos.", title="En la vista de pared", kind="ok", size=15))
save(c, "4-paso3.svg")

# ---------- 4-paso6.svg: dos horarios distintos
c = Canvas("OmniAccess Intrusión · Lección 4 · Paso 6", "Dos horarios con el mismo nombre")
c.add(panel(48, 150, 532, 250, "Horario de armado en la cámara", kind="ok"))
items1 = [("Decide si la cámara avisa", "ok"), ("Fuera de horario: no llega nada", "warn"), ("Se cambia en la web de la cámara", "info")]
s, _ = bullet_list(72, 235, items1, 480, 19, 18)
c.add(s)
c.add(panel(620, 150, 532, 250, "Horario en el Mapa", kind="warn"))
items2 = [("Solo calla el mapa: no suena ni titila", "warn"), ("La detección llega igual al monitor", "ok"), ("Queda en el historial", "ok"), ("Sin horario = siempre armada", "info")]
s, _ = bullet_list(644, 235, items2, 480, 19, 18)
c.add(s)
c.add(Note(48, 430, 1104, "Para que el mapa no calle lo que la cámara avisa: Mapa → Editar mapa → Cruces de línea → Horario → Quitar.", kind="info", size=16))
save(c, "4-paso6.svg")
