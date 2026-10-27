"""Teoría lección 2: cómo decide el kernel si un usuario puede escribir en una carpeta."""
from _alnx import *

a = new(20, "Dueño, grupo o resto: la primera que coincide")
a.steps(["tec1 quiere crear un archivo en /srv/obra.",
         "¿Es el dueño (root)? No: el kernel pasa al grupo.",
         "Está en tecnicos: valen rwx del grupo. Permitido.",
         "nobody no es dueño ni del grupo: resto ---, denegado."], still=2)

# permisos grandes
a.add(card(a, 300, 176, 600, 150))
a.add(mono(a, 330, 214, "/srv/obra   root : tecnicos", 17, a.GREY, 500))
segs = [("d", 336, None), ("rwx", 384, "dueño · root"), ("rws", 548, "grupo · tecnicos"), ("---", 712, "resto")]
for s, x, lb in segs:
    a.add(mono(a, x, 280, s, 44, a.INK, 700))
    if lb:
        a.add(a.text(x + 50, 312, lb, 15, a.GREY, a.SANS, 600, "middle"))
# resaltes por tiempo
at(a, a.box(370, 238, 128, 56, "none", a.BAD, rx=10, sw=3), 25, 50, 0)
at(a, a.box(534, 238, 128, 56, "none", a.OK, rx=10, sw=3), 50, 75, 1)
at(a, a.box(698, 238, 128, 56, "none", a.BAD, rx=10, sw=3), 75, 100, 0)

# preguntas en orden
qs = [("1. ¿Es el dueño?", 60), ("2. ¿Está en el grupo?", 440), ("3. Si no, el resto", 820)]
for q, x in qs:
    a.add(a.box(x, 362, 320, 54, a.SLATE, None, rx=12) + a.text(x + 160, 396, q, 18, a.INK, a.HEAD, 600, "middle"))

# usuario que viaja
tok1 = a.box(-70, -24, 140, 48, a.BLUE, None, rx=24) + a.text(0, 7, "tec1", 18, "#FFFFFF", a.MONO, 700, "middle")
mv = a.move([(0, 220, 480), (25, 220, 480), (33, 220, 480), (45, 600, 480), (100, 600, 480)])
a.add(a.group(tok1, mv, a.show(0, 46), still=0))
at(a, f'<g transform="translate(600 480)">{tok1}</g>', 45, 75, 1)
at(a, chip(a, 220, 516, "no es root", "bad", anchor="middle"), 27, 50, 0)
at(a, chip(a, 600, 516, "sí: está en tecnicos", "ok", anchor="middle"), 50, 75, 1)
at(a, a.box(460, 560, 560, 46, a.OKBG, None, rx=12) + a.text(480, 590, "plano.txt nace con grupo tecnicos (setgid)", 17, a.OK, a.SANS, 600), 56, 75, 1)

tok2 = a.box(-80, -24, 160, 48, a.GREY, None, rx=24) + a.text(0, 7, "nobody", 18, "#FFFFFF", a.MONO, 700, "middle")
mv2 = a.move([(0, 220, 480), (76, 220, 480), (84, 600, 480), (90, 980, 480), (100, 980, 480)])
a.add(a.group(tok2, mv2, a.show(75, 100), still=0))
at(a, chip(a, 980, 516, "Permission denied", "bad", anchor="middle"), 90, 100, 0)

caption(a, 640, [(0, 25, "El kernel revisa cada acceso: no importa con qué programa lo intentes.", None),
                 (25, 50, "Se usa una sola categoría: la primera que coincide, no la más generosa.", None),
                 (50, 75, "Por eso el acceso compartido se da con un grupo y no con 777.", a.OK),
                 (75, 100, "Con 0 en el resto, quien no está en el grupo no puede ni listar.", a.BAD)], still=2)
write(a, "2-t1.svg", "Dueño, grupo o resto: la primera que coincide",
      "Animación en cuatro tiempos sobre la carpeta /srv/obra, dueño root, grupo tecnicos, permisos rwx rws y tres guiones. Abajo, las tres preguntas en orden: ¿es el dueño?, ¿está en el grupo?, si no, el resto. "
      "1: el usuario tec1 quiere crear un archivo. 2: no es root, se marca en rojo el bloque del dueño y el kernel pasa a la pregunta del grupo. "
      "3: tec1 está en tecnicos, se marca en verde el bloque del grupo, el acceso se permite y plano.txt nace con grupo tecnicos por el setgid. "
      "4: el usuario nobody no es dueño ni del grupo, cae en el resto, con tres guiones, y recibe Permission denied. El cuadro fijo muestra el tiempo 3.")
