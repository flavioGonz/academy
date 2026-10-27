"""Teoría lección 9: bajar de a un nivel con du hasta encontrar qué llenó el disco."""
from _alnx import *

a = new(20, "Disco lleno: bajar de a un nivel hasta el culpable")
a.steps(["df -h: el sistema de archivos / está al 97 %.",
         "du en /: la carpeta grande es /var.",
         "du en /var: lo que pesa es /var/log.",
         "du en /var/log: el journal ocupa 6,5 GB."], still=3)

X0, W = 260, 860
levels = [  # (y, etiqueta, [(nombre, GB, destacar)], total)
    (186, "df -h /", [("usado 30 GB", 30, True), ("libre 1 GB", 1, False)], 31),
    (300, "du /", [("/usr 4,1G", 4.1, False), ("/var 8,2G", 8.2, True), ("/home 2,3G", 2.3, False), ("otros", 15.4, False)], 30),
    (414, "du /var", [("/var/lib", 1.1, False), ("/var/log 6,8G", 6.8, True), ("resto", 0.3, False)], 8.2),
    (528, "du /var/log", [("journal 6,5G", 6.5, True), ("resto", 0.3, False)], 6.8),
]
for k, (y, lab, parts, tot) in enumerate(levels):
    t0 = k * 25
    g = [mono(a, 48, y + 34, lab, 17, a.INK, 700)]
    x = X0
    for name, v, hl in parts:
        w = W * v / tot
        fill = (a.BAD if k == 0 else a.AMB) if hl else a.SLATE
        tc = "#FFFFFF" if hl else a.TXT
        g.append(a.box(x, y, max(w - 4, 2), 52, fill, None, rx=8))
        if w > len(name) * 9.2 + 24:
            g.append(a.text(x + 12, y + 32, name, 15, tc, a.MONO, 700 if hl else 500))
        x += w
    at(a, "".join(g), t0 + 1, 100, 1)
    if k < 3:
        # flecha que baja desde la parte destacada
        xs = X0
        for name, v, hl in parts:
            if hl:
                break
            xs += W * v / tot
        at(a, a.arrow(f"M{xs + 30} {y + 56}C{xs + 30} {y + 84},{X0 + 30} {y + 80},{X0 + 30} {y + 108}", a.GREY, 2.5), t0 + 18, 100, 1)
at(a, a.box(X0, 528, 860, 52, "none", a.BAD, rx=8, sw=3), 82, 100, 1)
at(a, chip(a, 1152, 600, "tope: SystemMaxUse=500M", "ok", anchor="end"), 84, 100, 1)

caption(a, 636, [(0, 25, "df mide sistemas de archivos: te dice cuál se llenó, no por qué.", None),
                 (25, 50, "du suma carpetas: con -d1 ves un nivel por vez y con -x no cruzás de disco.", None),
                 (50, 75, "Se baja siempre por la carpeta más grande, sin borrar nada todavía.", None),
                 (75, 100, "Encontrado el culpable, se arregla la causa: tope al journal, no rm a mano.", a.OK)], still=3)
write(a, "9-t1.svg", "Disco lleno: bajar de a un nivel hasta el culpable",
      "Animación en cuatro tiempos con cuatro barras horizontales que aparecen una debajo de la otra. 1: df -h muestra el sistema de archivos / con 30 GB usados en rojo y 1 GB libre. "
      "2: du sobre / reparte lo usado en /usr, /var, /home y otros, y /var, con 8,2 GB, queda destacada. 3: du sobre /var muestra /var/lib y /var/log, y /var/log, con 6,8 GB, se destaca. "
      "4: du sobre /var/log muestra el journal con 6,5 GB, marcado en rojo, y aparece la solución: tope con SystemMaxUse=500M. Los tamaños son de ejemplo.")
