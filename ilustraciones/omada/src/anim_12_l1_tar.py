#!/usr/bin/env python3
"""Lección 12 · Laboratorio, paso 3: copia del volumen con el contenedor detenido. docker compose stop manda la señal
de parada y espera hasta 60 s (stop_grace_period) para que MongoDB cierre; con el volumen quieto, tar copia todo; start vuelve a levantar."""
from _anim_om_red import *

a = nueva(26, "BACKUP PRIMERO", "Parar, copiar el volumen, arrancar", "l")
F = a.steps([
    "docker compose stop: el contenedor recibe la orden de parar y MongoDB cierra en hasta 60 s.",
    "Con el contenedor detenido, el volumen está quieto: tar lo copia entero con la fecha.",
    "docker compose start: el controlador vuelve en 1 a 2 minutos.",
    "El tar.gz y el docker-compose.yml, fuera de la VM: con eso se rearma en otro host.",
], still=1)

# terminal
TX, TY, TW = 48, 186, 600
a.add(a.box(TX, TY, TW, 250, a.INK, rx=14))
a.add(a.text(TX + 20, TY + 32, "VM · /opt/omada", 15, SKY, a.MONO))
CMDS = [(2, "$ docker compose stop", a.WHITE), (14, "Container omada-controller  Stopped", MINT),
        (27, "$ sudo tar czf ~/omada-data-$(date +%F).tar.gz \\", a.WHITE), (27, "    -C /var/lib/docker/volumes/omada_omada-data/_data .", a.WHITE),
        (52, "$ docker compose start", a.WHITE), (56, "Container omada-controller  Started", MINT)]
for i, (t0, txt, col) in enumerate(CMDS):
    at(a, a.text(TX + 20, TY + 70 + i * 28, txt, 15, col, a.MONO), t0, 100, still=1 if t0 < 50 else 0)

# contenedor y volumen
CX = 690
CONT = lambda sub, dark=True: dev(a, CX, 186, 462, 84, "omada-controller", sub, icon="server", dark=dark)
at(a, CONT("corriendo · MongoDB escribiendo"), 0, 4)
at(a, CONT("parando · MongoDB cierra (hasta 60 s)"), 4, 14)
at(a, CONT("detenido", dark=False), 14, 52, still=1)
at(a, CONT("arrancando · 1 a 2 minutos"), 52, 70)
at(a, CONT("corriendo"), 70, 100)
# volumen como cilindro
VX, VY = CX + 40, 320
CYL = (f'<ellipse cx="{VX + 100}" cy="{VY}" rx="100" ry="18" fill="#DCEBF8" stroke="{a.BLUE}" stroke-width="2"/>'
       f'<path d="M{VX} {VY} V{VY + 90} A100 18 0 0 0 {VX + 200} {VY + 90} V{VY}" fill="#DCEBF8" stroke="{a.BLUE}" stroke-width="2"/>'
       f'<ellipse cx="{VX + 100}" cy="{VY}" rx="100" ry="18" fill="#EAF4FC" stroke="{a.BLUE}" stroke-width="2"/>')
a.add(CYL + a.text(VX + 100, VY + 52, "omada-data", 16, a.INK, a.MONO, 600, "middle") + a.text(VX + 100, VY + 76, "volumen", 15, a.GREY, a.SANS, 400, "middle"))
a.add(line(VX + 100, 270, VX + 100, VY - 18, a.BLUE, 3))
# escrituras mientras corre
for t0 in (0.5, 2.0):
    travel(a, dot(a, a.AMB, 7), [(VX + 100, 272), (VX + 100, VY - 8)], t0, t0 + 1.5, hold=0.2)
at(a, a.text(VX + 214, 300, "quieto", 16, a.OK, a.SANS, 600), 16, 52, still=1)
# archivo tar.gz
FX, FY = CX + 300, 330
FILE = (f'<path d="M{FX} {FY} h96 l26 26 v92 h-122 Z" fill="{a.WHITE}" stroke="{a.INK}" stroke-width="2"/>'
        + a.text(FX + 61, FY + 72, ".tar.gz", 15, a.INK, a.MONO, 600, "middle"))
at(a, FILE + a.text(FX + 61, FY + 140, "con fecha", 15, a.GREY, a.SANS, 400, "middle"), 34, 100, still=1)
travel(a, pkt(a, "copia", a.BLUE), [(VX + 200, VY + 45), (FX, VY + 45)], 30, 36, hold=0.5)
# afuera
at(a, a.box(48, 460, 600, 110, a.OKBG, a.OK, rx=14, sw=1.5)
   + a.text(68, 490, "Fuera de la VM, juntos:", 16, a.OK, a.SANS, 600)
   + a.text(68, 518, "omada-data-2026-10-27.tar.gz", 15, a.INK, a.MONO, 600)
   + a.text(68, 544, "docker-compose.yml", 15, a.INK, a.MONO, 600), 76, 100)
travel(a, pkt(a, ".tar.gz + compose", a.OK), [(FX + 60, FY + 120), (520, 500)], 78, 84, hold=0.5)
at(a, a.box(48, 460, 600, 110, a.BADBG, a.BAD, rx=14, sw=1.5)
   + a.text(68, 490, "Con el contenedor corriendo, no:", 16, a.BAD, a.SANS, 600)
   + a.text(68, 518, "tar podría copiar la base a mitad de una escritura.", 15, a.INK, a.SANS)
   + a.text(68, 544, "Y nunca docker compose down -v: borra el volumen.", 15, a.INK, a.SANS), 0, 76, still=1)

status(a, 618, [
    (0, 25, "stop_grace_period: 60s en el compose le da a MongoDB tiempo para cerrar limpio.", a.INK, 0),
    (25, 50, "La copia de un volumen quieto se puede restaurar; la de uno en uso, quizás no.", a.INK, 1),
    (50, 75, "Mientras arranca, la red sigue andando: solo falta la gestión.", a.INK, 0),
    (75, 100, "Este tar.gz es el respaldo de Docker; el .cfg del paso 2 es el del controlador.", a.OK, 0),
], x=48, anchor="start", size=16)

write(a, 12, "l1", "Copiar el volumen de Docker con el contenedor detenido",
      "Animación en cuatro tiempos con la terminal de la VM en /opt/omada, el contenedor omada-controller, el volumen omada-data y el archivo .tar.gz. "
      "1: docker compose stop le da al contenedor la orden de parar y espera hasta 60 segundos, el stop_grace_period del compose, para que MongoDB termine de escribir y cierre limpio. "
      "2: con el contenedor detenido el volumen queda quieto y sudo tar czf copia todo el contenido de /var/lib/docker/volumes/omada_omada-data/_data a omada-data con la fecha en el nombre; "
      "con el contenedor corriendo tar podría copiar la base a mitad de una escritura. "
      "3: docker compose start vuelve a levantar el controlador, que tarda de 1 a 2 minutos; mientras, la red sigue andando. "
      "4: el tar.gz y el docker-compose.yml se guardan juntos fuera de la VM: con eso se rearma el controlador en otro host. Nunca docker compose down -v, que borra el volumen.",
      [8, 36, 62, 90])
