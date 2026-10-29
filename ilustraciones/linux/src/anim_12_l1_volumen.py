#!/usr/bin/env python3
"""Lección 12 · Laboratorio, paso 5: un volumen sobrevive al contenedor. El volumen vive en
/var/lib/docker/volumes/<nombre>/_data; un contenedor lo monta con -v y escribe ahí; lo que escribe fuera del volumen
queda en la capa del contenedor y se borra con docker rm -f; un contenedor nuevo con el mismo -v encuentra los datos.
Fuentes: teoría y laboratorio de la lección (imagen, contenedor y volumen; Mountpoint en /var/lib/docker/volumes) y la
documentación de Docker (volúmenes con nombre; docker rm no borra volúmenes con nombre). Imagen y archivos de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · DOCKER · LABORATORIO", "El contenedor se borra; el volumen queda")
a.steps([
    "docker volume create datos-prueba: una carpeta que maneja Docker.",
    "El contenedor la monta en /datos y escribe; lo demás va a su capa.",
    "docker rm -f borra el contenedor y su capa; el volumen no se toca.",
    "Un contenedor nuevo con el mismo -v encuentra los datos.",
], still=3)

# volumen en el disco del host
VX, VY, VW = 48, 404, 560
a.add(a.box(VX, VY, VW, 116, a.WHITE, "#C2D4E6", rx=14) + a.text(VX + 18, VY + 28, "Disco del host", 16, a.INK, a.HEAD, 600))
en(a, a.box(VX + 16, VY + 40, VW - 32, 62, "#E5F0FB", a.BLUE, rx=10, sw=2) + mono(a, VX + 30, VY + 64, "/var/lib/docker/volumes/datos-prueba/_data", 14, a.BLUE, 700), 4, 100, still=1)
en(a, mono(a, VX + 30, VY + 90, "informe.txt", 15, a.OK, 700), 40, 100, still=1)


def contenedor(x, y, nombre, t0, t1, con_cache=True, still=0, nuevo=False):
    s = (a.box(x, y, 560, 170, a.INK, None, rx=14) + a.text(x + 18, y + 30, nombre, 17, "#FFFFFF", a.SANS, 600)
         + a.box(x + 16, y + 46, 250, 108, "#0B3A66", None, rx=10) + a.text(x + 30, y + 70, "capa del contenedor", 15, LIGHT, a.SANS, 600)
         + a.box(x + 286, y + 46, 258, 108, "#0B3A66", MINT, rx=10, sw=2) + mono(a, x + 300, y + 70, "/datos  (volumen)", 15, MINT, 700))
    en(a, s, t0, t1, still)


contenedor(VX, 186, "contenedor prueba · debian (ejemplo)", 24, 54)
contenedor(VX, 186, "contenedor nuevo · mismo -v", 82, 100, still=1)
# escrituras
en(a, mono(a, VX + 30, 186 + 104, "/tmp/cache.txt", 15, GOLD, 700), 40, 54)
en(a, mono(a, VX + 300, 186 + 104, "informe.txt", 15, MINT, 700), 38, 54)
en(a, mono(a, VX + 300, 186 + 104, "informe.txt", 15, MINT, 700) + a.text(VX + 300, 186 + 132, "ya estaba", 15, MINT, a.SANS, 700), 88, 100, still=1)
en(a, a.text(VX + 30, 186 + 104, "(vacía)", 15, LIGHT, a.SANS, 500), 84, 100, still=1)
# enlace montaje
en(a, camino(f"M{VX + 415} {186 + 154} V{VY + 40}", MINT, 3, "6 5"), 30, 54)
en(a, camino(f"M{VX + 415} {186 + 154} V{VY + 40}", MINT, 3, "6 5"), 84, 100, still=1)
viaje(a, "", [(VX + 415, 186 + 120), (VX + 415, VY + 70)], 42, 47, inner=f'<circle r="8" fill="{a.OK}"/>', hold=0)
# borrado
en(a, a.box(VX, 186, 560, 170, a.BADBG, a.BAD, rx=14, sw=3) + marca(a, VX + 280, 186 + 70, False, 24)
   + a.text(VX + 280, 186 + 126, "contenedor y capa borrados: /tmp/cache.txt se perdió", 15, a.BAD, a.SANS, 700, "middle"), 54, 80)
en(a, a.box(VX + 12, VY + 36, VW - 24, 70, "none", a.OK, rx=12, sw=3) , 56, 80)

# terminal
TX = 640
a.add(tterm(a, TX, 186, 512, 334, "TERMINAL"))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, TX, 186 + 56 + i * 26, r, 14) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ sudo docker volume create datos-prueba", ("datos-prueba", T_OUT), "$ sudo docker volume inspect datos-prueba", ('  "Mountpoint": "/var/lib/docker/', T_OK), ('     volumes/datos-prueba/_data"', T_OK)], 0, 25)
filas(["$ sudo docker run --name prueba \\", "    -v datos-prueba:/datos debian sh -c \\", ("    'echo obra > /datos/informe.txt;", T_CMD), ("     echo x > /tmp/cache.txt'", T_CMD), ("# informe.txt va al volumen;", T_COM), ("# cache.txt, a la capa del contenedor", T_COM)], 25, 50)
filas(["$ sudo docker rm -f prueba", ("prueba", T_OUT), "$ sudo docker volume ls", ("local     datos-prueba", T_OK), ("# el volumen sigue: rm no borra volúmenes", T_COM), ("# con nombre", T_COM)], 50, 75)
filas(["$ sudo docker run --rm \\", "    -v datos-prueba:/datos debian \\", "    cat /datos/informe.txt", ("obra", T_OK), ("# los datos sobrevivieron al contenedor", T_COM)], 75, 100, still=1)

narr(a, [
    (0, 25, "El volumen es una carpeta en el host que Docker administra.", None),
    (25, 50, "Solo lo que se escribe en el punto de montaje va al volumen.", a.AMB),
    (50, 75, "Borrar y recrear un contenedor no tiene drama si los datos están en un volumen.", a.OK),
    (75, 100, "Para respaldar, se respalda el volumen, no el contenedor.", a.OK),
], y=642, still_idx=3)

escribir(a, "12-l1", "El contenedor se borra; el volumen queda",
         "Animación en cuatro tiempos con el disco del host abajo a la izquierda, un contenedor arriba y la terminal a la derecha. "
         "1: docker volume create datos-prueba crea la carpeta /var/lib/docker/volumes/datos-prueba/_data, que docker volume inspect muestra como Mountpoint. "
         "2: un contenedor de ejemplo con -v datos-prueba:/datos escribe informe.txt en /datos, que baja al volumen del host, y cache.txt en /tmp, que queda en la capa del contenedor. "
         "3: docker rm -f prueba borra el contenedor y su capa, y cache.txt se pierde; docker volume ls muestra que datos-prueba sigue. "
         "4: un contenedor nuevo con el mismo -v lee /datos/informe.txt y encuentra obra: los datos sobrevivieron.",
         [10, 40, 64, 92])
