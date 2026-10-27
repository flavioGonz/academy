"""Teoría lección 12: por qué un puerto publicado por Docker se saltea ufw (DNAT antes de input)."""
from _alnx import *

a = new(22, "Por qué el puerto de Docker se saltea ufw")
a.steps(["Llega un paquete a 192.168.88.50:8080 desde la red.",
         "Docker lo redirige en la tabla nat (DNAT) al contenedor.",
         "Ya no es para el host: va por forward, no por input.",
         "En 127.0.0.1:8081, desde la red no hay nada que alcanzar."], still=2)

# cajas
a.add(card(a, 48, 300, 170, 90, "Red", "otra VM"))
a.add(a.box(270, 256, 210, 178, "#E5F0FB", a.BLUE, rx=14, sw=2) + a.text(375, 294, "tabla nat", 18, a.INK, a.HEAD, 600, "middle")
      + mono(a, 375, 322, "DNAT 8080 ->", 15, a.BLUE, 700, "middle") + mono(a, 375, 346, "172.17.0.2:80", 15, a.BLUE, 700, "middle"))
a.add(a.box(560, 170, 290, 120, a.WHITE, a.LINE, rx=14, sw=2) + a.text(705, 206, "input", 19, a.INK, a.HEAD, 600, "middle")
      + a.text(705, 236, "reglas de ufw:", 15, a.GREY, a.SANS, 600, "middle") + mono(a, 705, 262, "deny incoming", 15, a.BAD, 700, "middle"))
a.add(a.box(560, 400, 290, 120, a.WHITE, a.LINE, rx=14, sw=2) + a.text(705, 436, "forward", 19, a.INK, a.HEAD, 600, "middle")
      + a.text(705, 466, "reglas de Docker", 15, a.GREY, a.SANS, 600, "middle") + mono(a, 705, 492, "(y DOCKER-USER)", 15, a.GREY, 600, "middle"))
a.add(card(a, 920, 400, 232, 120, "Contenedor", "nginx · 172.17.0.2", dark=True))
a.add(card(a, 920, 170, 232, 120, "Host", "procesos locales"))
a.add(line(a, "M218 345H270", a.LINE, 4) + line(a, "M480 320C520 320 520 230 560 230", a.LINE, 4, "6 6")
      + line(a, "M480 370C520 370 520 460 560 460", a.LINE, 4) + line(a, "M850 460H920", a.LINE, 4) + line(a, "M850 230H920", a.LINE, 4, "6 6"))

# paquete 8080
mv = a.move([(0, 130, 345), (2, 130, 345), (20, 375, 396), (45, 375, 396), (55, 705, 460), (68, 885, 460), (100, 885, 460)])
a.add(a.group(pkt(a, ":8080", a.BLUE, 90), mv, a.show(1, 74), still=0))
a.add(a.group(f'<g transform="translate(885 460)">{pkt(a, ":80", a.BLUE, 60)}</g>', a.keyframes([(0, 0), (100, 0)]), still=1))
at(a, a.box(270, 256, 210, 178, "none", a.CYAN, rx=14, sw=4), 25, 50, 0)
at(a, a.box(560, 400, 290, 120, "none", a.AMB, rx=14, sw=4), 50, 75, 1)
at(a, a.box(560, 170, 290, 120, a.BG, None, rx=14, extra='fill-opacity="0.55"') + chip(a, 705, 300, "ufw no lo ve", "bad", anchor="middle"), 52, 75, 1)
at(a, chip(a, 1036, 536, "responde: abierto", "bad", anchor="middle"), 62, 75, 1)
# 127.0.0.1
at(a, a.box(48, 560, 1104, 50, a.OKBG, a.OK, rx=12, sw=2) + mono(a, 600, 592, "-p 127.0.0.1:8081:80  ->  escucha solo en el host: la otra VM no llega", 15, a.OK, 700, "middle"), 76, 100, 0)
mv2 = a.move([(0, 130, 345), (77, 130, 345), (90, 250, 345), (100, 250, 345)])
a.add(a.group(pkt(a, ":8081", a.GREY, 90), mv2, a.show(77, 99), still=0))
at(a, chip(a, 250, 430, "nada que alcanzar", "grey", anchor="middle"), 88, 100, 0)

caption(a, 640, [(0, 25, "Para la red, el 8080 es un puerto más del servidor.", None),
                 (25, 50, "La redirección se decide antes de saber si el paquete es para el host.", None),
                 (50, 75, "ufw status dice cerrado y el puerto responde: la prueba es desde afuera.", a.BAD),
                 (75, 100, "Publicar en 127.0.0.1 deja el servicio para el host o para un proxy inverso.", a.OK)], still=2)
write(a, "12-t1.svg", "Por qué el puerto de Docker se saltea ufw",
      "Animación en cuatro tiempos. A la izquierda, la red; en el medio, la tabla nat; arriba, la cadena input con las reglas de ufw en deny y el host; abajo, la cadena forward con las reglas de Docker y el contenedor nginx con IP 172.17.0.2. "
      "1: un paquete llega desde la otra VM al puerto 8080 del servidor. 2: en la tabla nat, Docker lo redirige con DNAT al puerto 80 del contenedor. "
      "3: como ya no es para el host, el paquete va por forward y llega al contenedor; la cadena input, donde están las reglas de ufw, se apaga con la etiqueta ufw no lo ve, y el puerto responde abierto. "
      "4: con -p 127.0.0.1:8081:80 el servicio escucha solo en el host y un paquete de la red al 8081 no tiene nada que alcanzar. El cuadro fijo muestra el tiempo 3.")
