from _oai import *


def estado(x, y, w, t, sub, kd):
    bg, fg = KC[kd]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="84" rx="16" fill="{bg}" stroke="{fg}" stroke-width="2"/>'
            + text(x + 20, y + 36, t, 19, 600, INK, FD) + text(x + 20, y + 62, sub, 14, 500, INK3, FM))


# ---------- 6.svg: de detectada a resuelta
c = Canvas("OmniAccess Intrusión · Lección 6", "De «detectada» a «resuelta», con una decisión")
c.add(estado(48, 260, 250, "Detectada", "canal rojo · sin confirmar", "alert"))
c.add(estado(470, 150, 300, "Archivada como falsa", "queda en el registro", "gray"))
c.add(estado(470, 370, 300, "En atención", "borde animado en el canal", "warn"))
c.add(estado(902, 370, 250, "Resuelta", "fue real y se atendió", "ok"))
c.add(wire([(298, 290), (380, 290), (380, 192), (462, 192)], "flow", arrow=True))
c.add(pill(380, 245, "Falsa alarma · F", INK2, WHITE, 14, mono=False))
c.add(wire([(298, 316), (380, 316), (380, 412), (462, 412)], "power+", arrow=True))
c.add(pill(380, 360, "Confirmar real · A", ALERT, WHITE, 14, mono=False))
c.add(Arrow((776, 412), (894, 412), kind="ok"))
c.add(pill(835, 398, "Resolver", OK, WHITE, 14, mono=False))
c.add(wire([(620, 370), (620, 242)], "logical", arrow=True))
c.add(text(632, 312, "Era falsa alarma", 14, 600, INK3, FB))
c.add(Note(48, 500, 640, "Aceptar abre la ficha del evento. La decisión vale para todas las detecciones sin aceptar de esa cámara de las últimas 6 horas.", kind="info", size=15))
c.add(Note(720, 500, 432, "Teclas en la ficha: ← → recorren eventos, A o Enter real, F falsa, Esc cierra.", kind="ok", size=15))
save(c, "6.svg")

# ---------- 6-paso3.svg: el análisis
c = Canvas("OmniAccess Intrusión · Lección 6 · Paso 3", "Leé los indicios antes de decidir")
c.add(panel(48, 140, 640, 380, "Análisis", kind="info", title_size=18))
cif = [("2", "detecciones en el episodio"), ("7", "hoy en esta cámara"), ("82 %", "de falsas en esta cámara")]
for i, (v, l) in enumerate(cif):
    x = 72 + i * 202
    c.add(f'<rect x="{x}" y="190" width="186" height="92" rx="12" fill="{SOFT}"/>')
    c.add(text(x + 16, 232, v, 28, 700, INK, FD))
    s, _ = wrap(x + 16, 260, l, 160, 14, 500, INK3)
    c.add(s)
ind = [("La cámara lo clasificó como persona.", "info"),
       ("2 detecciones en 14 s: es un mismo episodio, no 2 intrusiones.", "info"),
       ("Fue de noche (02:11:40).", "warn"),
       ("De las últimas 50 revisadas, 41 fueron falsas (82 %).", "ok"),
       ("También detectó Perímetro Sur 07 a las 02:13: puede ser un recorrido.", "warn")]
s, _ = bullet_list(80, 322, ind, 590, 16, 12)
c.add(s)
# mini mapa
c.add(text(720, 162, "DÓNDE FUE EL CRUCE", 13, 600, INK3, FM, ls=1.2))
c.add('<rect x="720" y="176" width="432" height="300" rx="14" fill="#2E3F33"/>')
c.add('<path d="M720 350H1152" stroke="#55626B" stroke-width="18"/>')
c.add('<path d="M760 214L960 214" stroke="#ef4444" stroke-width="7" stroke-linecap="round"/>')
c.add('<circle cx="860" cy="290" r="11" fill="#60a5fa" stroke="#fff" stroke-width="3"/>')
c.add('<circle cx="1080" cy="250" r="10" fill="#f59e0b" stroke="#fff" stroke-width="3"/>')
c.add(text(878, 296, "la cámara", 14, 600, WHITE, FB))
c.add(text(1060, 236, "otra que detectó", 14, 600, WHITE, FB, anchor="end"))
c.add(text(780, 204, "su línea", 14, 600, "#FFB4B4", FB))
c.add(Note(720, 496, 432, "Son indicios, no un veredicto: la alarma la decide quien mira la foto.", kind="ok", size=15))
c.add(Step(48, 140, 3))
save(c, "6-paso3.svg")
