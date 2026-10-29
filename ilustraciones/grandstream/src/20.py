"""IVR que solo anuncia: ilustración principal y pasos 2, 5 y 8.

Caso real anonimizado ("un comercio"): IVR 7000 que solo pasa la bienvenida y deriva al Ring Group 6000,
con marcar internos (Dial Other Extensions) prendido, sin teclas numeradas y repeticiones en 3.
Nombres de campos del manual del UCM630x / UCM630xA vigente y de la guía de IVR de Grandstream.
"""
import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 20.svg: bienvenida y al grupo
c = Canvas(K(), "Bienvenida y al grupo, sin teclas ni marcar internos")
c.add(Generic(48, 128, "Línea de Antel", "FXO1 · UCM6304A", icon="phone", w=270))
c.add(f'<rect x="440" y="128" width="320" height="84" rx="16" fill="{DEEP}"/>')
c.add(icon(460, 152, "bell", CYAN, 1.35))
c.add(text(506, 164, "IVR 7000", 19, 600, WHITE, FB))
c.add(text(506, 188, "solo la bienvenida", 15, 400, "#9FC3E3", FM))
c.add(Generic(882, 128, "Ring Group 6000", "1001 · 1002", icon="user", w=270, hl=OK))
c.add(arrow((322, 170), (434, 170)))
c.add(arrow((764, 170), (876, 170), kind="ok"))

# la línea de tiempo de la llamada
X0, X1 = 48, 1152
segs = [("bienvenida completa", 620, BLUE, WHITE), ("silencio", 150, LINE2, INK2), ("suena el grupo", 334, OK, WHITE)]
x = X0
for s, w, bg, fg in segs:
    c.add(f'<rect x="{x}" y="244" width="{w - 6}" height="44" rx="10" fill="{bg}"/>')
    c.add(text(x + (w - 6) / 2, 272, s, 16, 600, fg, FB, anchor="middle"))
    x += w
c.add(text(48 + 620 + 72, 312, "Response Timeout", 14, 500, INK3, FM, anchor="middle"))

c.add(Window(48, 334, 580, 310, "UCM · IVR 7000", path="Basic Call Features > IVR",
             rows=[("Dial Other Extensions", "nada seleccionado"), ("Response Timeout (s)", "2"),
                   ("Response Timeout Prompt", "silencio"), ("Response Timeout Prompt Repeats", "1"),
                   ("Invalid Input Prompt Repeats", "1"), ("Timeout · Invalid", "Ring Group 6000")], hl=0))
c.add(Note(660, 334, 492, "«Lo siento, no lo entiendo» es el aviso de opción inválida: al IVR le llegó un dígito que no es tecla ni interno, a veces un DTMF falso de la línea analógica.", kind="alert", size=16))
c.add(Note(660, 494, 492, "Si el firmware tiene Advanced Call Features > Announcement, el audio no se saltea y pasa solo al destino: no espera teclas.", kind="info", size=16))
save(c, "20.svg")

# ---------------------------------------------------------------- 20-paso2: el IVR del caso
c = Canvas(K(2), "El IVR del caso: tres cosas que se juntan")
c.add(Window(48, 124, 560, 272, "UCM · IVR 7000 · como estaba", path="Basic Call Features > IVR",
             rows=[("Dial Other Extensions", "Extension, Ring Group"), ("Digit Timeout (s)", "3"),
                   ("Response Timeout (s)", "10"), ("Response Timeout Prompt Repeats", "3"),
                   ("Invalid Input Prompt Repeats", "3")], hl=0))
c.add(Window(640, 124, 512, 234, "Key Pressing Events", path="Standard Key Event",
             rows=[("teclas 0 a 9", "ninguna"), ("Tecla *", "Select an Option"), ("Timeout", "Ring Group 6000"),
                   ("Invalid", "Ring Group 6000")], hl=1))
c.add(Step(48, 124, 2))
cards = [("1 · Marcar internos prendido", "El IVR queda esperando que el que llama disque un número.", "alert"),
         ("2 · Ninguna tecla numerada", "Un dígito solo puede ser un interno; si no existe, es inválido.", "alert"),
         ("3 · Repeticiones en 3", "Saludo y aviso pueden sonar hasta tres veces antes del grupo.", "alert")]
for i, (t, d, k) in enumerate(cards):
    x = 48 + i * 372
    c.add(panel(x, 424, 352, 128, t, k, title_size=18))
    svg, _ = wrap(x + 20, 486, d, 312, 16, 400, INK2)
    c.add(svg)
c.add(Note(48, 572, 1104, "La fila * con «Select an Option» no estaba guardada: era una fila nueva abierta en el formulario. Una tecla sin destino no se guarda: se quita con el ícono (-).", kind="warn", size=16))
save(c, "20-paso2.svg")

# ---------------------------------------------------------------- 20-paso5: la receta
c = Canvas(K(5), "La receta: qué cambia en el IVR")
rows = [["Dial Other Extensions", "Extension, Ring Group", "nada seleccionado"],
        ["Response Timeout (s)", "10 (de fábrica)", "2"],
        ["Response Timeout Prompt", "el de fábrica", "silencio (Custom Prompt)"],
        ["Response Timeout Prompt Repeats", "3", "1"],
        ["Invalid Input Prompt Repeats", "3", "1"],
        ["Timeout · Invalid", "Ring Group 6000", "Ring Group 6000 (igual)"],
        ["Tecla * sin destino", "fila abierta", "se quita con (-)"]]
c.add(Table(48, 124, ["Campo", "Antes", "Después"], rows, [400, 330, 374], row_h=48, mono_cols=(1, 2)))
c.add(f'<rect x="782" y="128" width="366" height="{48 * 8 - 8}" rx="10" fill="none" stroke="{OK}" stroke-width="2.5"/>')
c.add(Step(48, 124, 5))
c.add(Note(48, 532, 540, "Más adelante, «1 ventas, 2 administración» van como teclas en Key Pressing Events, y marcar internos sigue apagado.", kind="ok", size=16))
c.add(Note(612, 532, 540, "Marcar internos sirve para que el que llama disque un interno directo. Si un día se prende, con lista blanca (lección IVR con horario).", kind="info", size=16))
save(c, "20-paso5.svg")

# ---------------------------------------------------------------- 20-paso8: IVR o Announcement
c = Canvas(K(8), "Para un saludo: IVR o Announcement")
c.add(panel(48, 124, 540, 276, "IVR 7000", "info", title_size=21))
c.add(text(68, 182, "Basic Call Features > IVR", 15, 500, BLUE, FM))
lst, _ = bullet_list(68, 224, [("Escucha teclas mientras suena la bienvenida", "warn"),
                               "Response Timeout, repeticiones, Timeout e Invalid",
                               "Teclas por horario si después piden opciones",
                               ("Con la receta del paso 5, deriva limpio", "ok")], 500, size=17, gap=18)
c.add(lst)
c.add(panel(612, 124, 540, 276, "Announcement", "ok", title_size=21))
c.add(text(632, 182, "Advanced Call Features > Announcement", 15, 500, BLUE, FM))
lst, _ = bullet_list(632, 224, [("Un audio que no se puede saltear", "ok"),
                                "Name, Prompt y Default Destination",
                                "Se elige como destino de una ruta entrante",
                                ("No espera teclas: un DTMF falso no lo cambia", "ok")], 500, size=17, gap=18)
c.add(lst)
c.add(Step(612, 124, 8))
# recorrido con Announcement
c.add(Generic(48, 448, "Ruta entrante", "troncal de la línea", icon="phone", w=300))
c.add(Generic(450, 448, "Announcement", "bienvenida", icon="bell", w=300, hl=OK))
c.add(Generic(852, 448, "Ring Group 6000", "1001 · 1002", icon="user", w=300))
c.add(arrow((352, 490), (444, 490)))
c.add(arrow((754, 490), (846, 490), kind="ok"))
c.add(text(48, 590, "Announcement figura en el manual del UCM630x y del UCM630xA vigentes; en firmwares viejos puede no estar.", 15, 400, INK3, FB))
save(c, "20-paso8.svg")
