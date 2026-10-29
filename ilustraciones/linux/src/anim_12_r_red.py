#!/usr/bin/env python3
"""Lección 12 (Docker sin sorpresas), Resumen: una red de Docker en la obra. app y db en una red creada con
docker network create, sin publicar puertos; app encuentra a db por nombre con el DNS interno de Docker (en redes
creadas por el usuario); solo el proxy inverso publica 443 en el host; desde otra VM solo responde el 443.
Fuentes: teoría de la lección (la red de Docker conecta contenedores sin publicar al host; lo público detrás de un
proxy inverso en 80 y 443) y la documentación de Docker sobre redes bridge definidas por el usuario (resolución por
nombre). Direcciones e imágenes de ejemplo."""
from _anims_lnx_rl import *

a = nueva(28, "LINUX · DOCKER · EN LA RED", "Red de Docker: se hablan por nombre, sin publicar")
a.steps([
    "docker network create obra: app y db se conectan, sin -p.",
    "app pide db: el DNS de Docker le da la IP del contenedor, y conecta al 5432.",
    "Solo el proxy publica -p 443:443: la única puerta del host.",
    "Desde otra VM: el 443 responde; 3000 y 5432 no están en el host.",
], still=3)

a.add(dev(a, 48, 300, 220, 84, "Otra VM", "192.168.88.60", "laptop"))
HX, HY, HW, HH = 330, 168, 822, 352
a.add(a.box(HX, HY, HW, HH, a.WHITE, "#C2D4E6", rx=18) + glyph(a, "server", HX + 18, HY + 14, a.BLUE) + a.text(HX + 62, HY + 36, "Host 192.168.88.50 · Docker", 18, a.INK, a.HEAD, 600))
# red obra
NX, NY, NW, NH = HX + 150, HY + 64, 640, 262
en(a, a.box(NX, NY, NW, NH, "#E5F0FB", a.BLUE, rx=16, sw=2, extra='stroke-dasharray="8 6"') + mono(a, NX + 18, NY + 28, "red obra · 172.18.0.0/16 (ejemplo)", 15, a.BLUE, 700), 3, 100, still=1)


def cont(x, y, n, ip, port, still=1, t0=0):
    en(a, a.box(x, y, 180, 92, a.INK, None, rx=12) + a.text(x + 16, y + 30, n, 17, "#FFFFFF", a.SANS, 600)
       + mono(a, x + 16, y + 54, ip, 14, LIGHT, 500) + mono(a, x + 16, y + 76, port, 14, MINT, 600), t0, 100, still)


cont(NX + 30, NY + 56, "proxy", "172.18.0.2", "escucha :443", t0=52)
cont(NX + 240, NY + 56, "app", "172.18.0.3", "escucha :3000", t0=5)
cont(NX + 440, NY + 56, "db", "172.18.0.4", "escucha :5432", t0=7)
# DNS interno
en(a, a.box(NX + 240, NY + 178, 380, 60, a.WHITE, a.LINE, rx=10) + a.text(NX + 256, NY + 202, "DNS interno de Docker", 15, a.INK, a.SANS, 700)
   + mono(a, NX + 256, NY + 226, "db → 172.18.0.4", 15, a.BLUE, 700), 26, 100, still=1)
viaje(a, "¿db?", [(NX + 300, NY + 150), (NX + 300, NY + 176)], 27, 30, bg=a.BLUE, size=13, hold=1)
viaje(a, "172.18.0.4", [(NX + 400, NY + 176), (NX + 400, NY + 150)], 32, 35, bg=a.OK, size=13, hold=1)
viaje(a, "TCP :5432", [(NX + 420, NY + 30), (NX + 520, NY + 30)], 38, 43, bg=a.CYAN, size=13, hold=6)
en(a, camino(f"M{NX + 420} {NY + 102} H{NX + 440}", a.CYAN, 3), 38, 100, still=1)
en(a, camino(f"M{NX + 210} {NY + 102} H{NX + 240}", a.CYAN, 3), 54, 100, still=1)

# puerta 443 en el host
en(a, a.box(HX - 12, HY + 150, 150, 46, a.OKBG, a.OK, rx=10, sw=2.5) + mono(a, HX + 4, HY + 179, "-p 443:443", 15, a.OK, 700), 54, 100, still=1)
en(a, camino(f"M{HX + 138} {HY + 173} H{NX + 30}", a.OK, 3), 54, 100, still=1)
a.add(camino(f"M268 342 H{HX}", "#C2D4E6", 4))
# nmap desde la otra VM
viaje(a, "SYN :443", [(278, 330), (HX - 20, 330)], 77, 81, bg=a.BLUE, size=13, hold=0.5)
viaje(a, "SYN-ACK", [(HX - 20, 352), (278, 352)], 82, 86, bg=a.OK, size=13, hold=0.5)
viaje(a, "SYN :5432", [(278, 330), (HX - 20, 330)], 88, 92, bg=a.BLUE, size=13, hold=0.5)
en(a, marca(a, HX - 6, 420, False, 13) + a.text(HX - 26, 425, "5432", 14, a.BAD, a.MONO, 700, "end"), 92, 100)

# terminal
TY = 534
a.add(tterm(a, 48, TY, 1104, 74))
def filas(rows, t0, t1, still=0):
    en(a, "".join(trow(a, 48, TY + 30 + i * 25, r, 14) for i, r in enumerate(rows)), t0, t1, still)


filas(["$ sudo docker network create obra", "$ sudo docker run -d --name db --network obra -e POSTGRES_PASSWORD=... postgres    # y app, igual, sin -p"], 0, 50)
filas(["$ sudo docker run -d --name proxy --network obra -p 443:443 nginx", ("# el proxy reenvía a app:3000 por la red obra", T_COM)], 50, 75)
filas(["$ nmap -Pn -p 443,3000,5432 192.168.88.50      # desde la otra VM", ("443/tcp open   ·   3000/tcp y 5432/tcp no aparecen abiertos", T_OK)], 75, 100, still=1)

narr(a, [
    (0, 25, "En una red creada por vos, los contenedores se ven entre sí y nada se publica.", None),
    (25, 50, "Por nombre, no por IP: si recreás db y cambia la IP, app la sigue encontrando.", a.OK),
    (50, 75, "Lo que tiene que ser público entra por el proxy; lo demás queda adentro.", a.AMB),
    (75, 100, "La verificación es desde afuera: solo tiene que aparecer lo que publicaste.", a.OK),
], y=642, still_idx=3)

escribir(a, "12-r1", "Red de Docker: se hablan por nombre, sin publicar",
         "Animación en cuatro tiempos con el host 192.168.88.50 con Docker y, adentro, la red obra, 172.18.0.0/16 de ejemplo; a la izquierda, otra VM de la LAN, 192.168.88.60. "
         "1: con docker network create obra, los contenedores app, en 172.18.0.3 escuchando el 3000, y db, en 172.18.0.4 escuchando el 5432, se conectan a la red sin publicar puertos. "
         "2: app pregunta por db al DNS interno de Docker, recibe 172.18.0.4 y abre una conexión TCP al 5432 dentro de la red. "
         "3: el contenedor proxy, nginx en 172.18.0.2, se suma a la red con -p 443:443: es la única puerta publicada en el host. "
         "4: desde la otra VM, nmap al 443 recibe SYN-ACK y el 5432 no responde: solo aparece abierto lo que se publicó.",
         [10, 38, 64, 94])
