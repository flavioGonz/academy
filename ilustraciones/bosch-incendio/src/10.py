import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/bosch-incendio/src")
from _bi import *

# ---------------------------------------------------------------- 10.svg: física y lógica
c = Canvas(K(), "Un detector, dos direcciones: dónde está y cómo se llama")
c.add(detector(600, 250, 46, "Detector", "FAP-425-O-R", hl=CYAN))
c.add(panel(48, 160, 400, 190, "Dirección física", "info"))
c.add(text(68, 230, "su lugar en el lazo", 16, 400, INK2))
c.add(text(68, 270, "módulo · lazo · elemento 17", 18, 600, BLUE, FM))
c.add(text(68, 306, "sale de las perillas o del orden de cable", 15, 400, INK3))
c.add(panel(752, 160, 400, 190, "Dirección lógica", "ok"))
c.add(text(772, 230, "grupo y subdirección", 16, 400, INK2))
c.add(text(772, 270, "3.4", 26, 700, OK, FM))
c.add(text(772, 306, "la elegís vos en RPS, sin repetir", 15, 400, INK3))
c.add(arrow((450, 255), (548, 255)))
c.add(arrow((652, 255), (750, 255), kind="ok"))
c.add(text(48, 410, "LA LÓGICA ES LA LLAVE DE TODO LO QUE VIENE DESPUÉS", 13, 600, INK3, FM, ls=1.5))
for i, (t, s) in enumerate([("Mensaje del panel", "tipo, elemento, ubicación y 3.4"), ("Integración y BMS", "por RS-232 se ve línea.3.4"), ("Mantenimiento", "el técnico busca 3.4 en el plano")]):
    x = 48 + i * 376
    c.add(box(x, 426, 352, 100, t, [s], kind="info", size=15, mono=(i == 1)))
c.add(text(48, 580, "Desde la cuenta 4.5: puntos de alarma (deciden si hace falta redundancia)", 16, 500, INK2))
c.add(text(48, 606, "y puntos lógicos (4096 en panel solo, 2048 por panel en red).", 16, 500, INK2))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso2: cómo se marca la matriz
c = Canvas(K(2), "Cada cruce de la matriz lleva una de tres marcas")
eff = ["Sirenas piso", "Retención puertas", "Ventilación", "Transmisión"]
cau = ["Detector grupo 3 (1 eq.)", "Detector grupo 3 (2 eq.)", "Pulsador piso 3", "Flujo rociadores piso 3"]
x0, y0, cw, rh = 48, 140, 150, 58
c.add(rect(x0, y0, 290 + cw * 4, rh * 5, WHITE, LINE2, rx=12))
c.add(text(x0 + 16, y0 + 36, "CAUSA \\ EFECTO", 13, 600, INK3, FM, ls=1.2))
for j, e_ in enumerate(eff):
    c.add(mid(x0 + 290 + cw * j + cw / 2, y0 + 36, e_, 15, 600, INK2))
for i, ca in enumerate(cau):
    y = y0 + rh * (i + 1)
    c.add(hline(x0 + 10, x0 + 290 + cw * 4 - 10, y, LINE))
    c.add(text(x0 + 16, y + 36, ca, 15, 600, INK))
    for j in range(4):
        cx = x0 + 290 + cw * j + cw / 2
        c.add(rect(cx - 55, y + 12, 110, 34, GROUND, LINE2, rx=8, sw=1.5, dash="4 4"))
c.add(rect(x0 + 290 + 20, y0 + rh * 3 + 12, 110, 34, OK_BG, OK, rx=8, sw=2))
c.add(mid(x0 + 290 + 75, y0 + rh * 3 + 35, "activa", 15, 600, OK))
c.add(text(x0 + 16, y0 + rh * 5 + 30, "Ejemplo de una marca: el pulsador activa las sirenas del piso.", 15, 500, OK, FB))
c.add(text(980, 160, "LAS TRES MARCAS", 13, 600, INK3, FM, ls=1.5))
for i, (t, kd) in enumerate([("activa", "ok"), ("no activa", "gray"), ("solo en modo noche", "warn")]):
    c.add(tag(980, 210 + i * 50, t, kd, size=15, mono=False, anchor="start"))
c.add(Note(48, 480, 1104, "La matriz de causa y efecto es parte del proyecto: la define y firma el técnico responsable. Vos la pasás a reglas, no la inventás en obra.", title="De quién es la matriz", kind="warn"))
save(c, "10-paso2.svg")

# ---------------------------------------------------------------- 10-paso3: direcciones lógicas sin repetir
c = Canvas(K(3), "Grupos lógicos separados, sin pisarse")
blocks = [("Grupo 3", "sub 1 a 20", "detectores piso 3", BLUE), ("Grupo 30", "sub 1 a 4", "pulsadores piso 3", ALERT),
          ("Grupo 300", "", "entradas técnicas (flujo, presión)", CYAN), ("Grupo propio", "", "teclas de función", INK3)]
for i, (g, sub, d, col) in enumerate(blocks):
    y = 140 + i * 84
    c.add(rect(48, y, 700, 68, WHITE, col, rx=12, sw=2.5))
    c.add(rect(48, y, 14, 68, col, col, rx=6, sw=0))
    c.add(text(82, y + 42, g, 19, 700, col, FM))
    c.add(text(300, y + 42, sub, 16, 500, INK2, FM))
    c.add(text(450, y + 42, d, 16, 500, INK))
c.add(panel(790, 140, 362, 190, "Lo que RPS puede no avisar", "alert"))
c.add(wrap(812, 210, "Si una tecla de función y un grupo de entradas comparten dirección, RPS puede no avisar. Por eso las teclas van en un grupo propio.", 320, 16)[0])
c.add(panel(790, 350, 362, 136, "Lo que RPS te ahorra", "ok"))
c.add(wrap(812, 420, "Copiar y pegar detectores les da la siguiente subdirección del mismo grupo.", 320, 16)[0])
c.add(text(48, 600, "Números del ejemplo del laboratorio. Lo que importa: ninguna dirección lógica repetida.", 16, 500, INK2))
save(c, "10-paso3.svg")
