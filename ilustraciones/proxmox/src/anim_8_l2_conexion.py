#!/usr/bin/env python3
"""Lección 8 · Laboratorio, paso 4: qué pasa cuando Proxmox VE se conecta a PBS. Abre TLS al puerto 8007, PBS
muestra su certificado y PVE compara la huella con la que cargaste (fingerprint del dashboard); después se presenta
con el token backup@pbs!pve y su secreto, y PBS revisa el permiso DatastoreBackup sobre /datastore/main.
Fuentes: tarjeta de la lección (pasos 3 y 4: token, secreto, fingerprint, ACL), documentación de PBS
(web en 8007, tokens de API, Datastore.Backup)."""
from _anim_pmx_red import *

a = new(24, "PBS sin sorpresas", "Huella, token y permiso: la primera conexión", lab=True)
a.steps([
    "En PVE cargás servidor, datastore, token, secreto y fingerprint.",
    "TLS al puerto 8007: PVE compara la huella del certificado de PBS.",
    "Se presenta con backup@pbs!pve y el secreto; PBS revisa el permiso.",
    "Backup de prueba: los trozos suben y el backup aparece en Content.",
], still=2)

PV, PB = 250, 950
a.add(dev(a, 48, 180, 404, 80, "pve1 · Proxmox VE", "Storage: pbs-main", icon="server", dark=True, tsize=18))
a.add(dev(a, 748, 180, 404, 80, "PBS · 10.10.10.30:8007", "datastore main", icon="shield", tsize=18))
a.add(lifeline(a, PV, 260, 520))
a.add(lifeline(a, PB, 260, 520))

# paso 1: formulario
f = a.box(300, 284, 600, 232, a.WHITE, a.LINE, rx=14)
f += a.box(300, 284, 600, 40, a.SLATE, rx=14) + a.box(300, 310, 600, 14, a.SLATE, rx=0)
f += a.text(320, 311, "Datacenter → Storage → Add → Proxmox Backup Server", 15, a.INK, a.MONO, 600)
for i, (k, v) in enumerate([("Server", "10.10.10.30"), ("Datastore", "main"), ("Username", "backup@pbs!pve"), ("Password", "•••••••• (secreto del token)"), ("Fingerprint", "AB:12:…:9F")]):
    y = 352 + i * 32
    f += a.text(320, y, k, 15, a.GREY, a.SANS, 600) + a.text(450, y, v, 15, a.INK, a.MONO, 600 if i in (2, 4) else 400)
at(a, f, 0, 25)

# paso 2: TLS y huella
msg(a, PV, PB, 310, "TLS · ClientHello", 28, end=50, still=0)
msg(a, PB, PV, 360, "certificado de PBS", 33, end=50, still=0, color=a.CYAN)
at(a, a.box(PV - 200, 392, 400, 92, a.WHITE, a.LINE, rx=10) + a.text(PV - 182, 420, "huella recibida:   AB:12:…:9F", 15, a.INK, a.MONO)
   + a.text(PV - 182, 446, "huella cargada:    AB:12:…:9F", 15, a.INK, a.MONO) + a.text(PV - 182, 472, "coinciden: es este PBS", 15, a.OK, a.SANS, 600), 38, 50)
# paso 3: token y ACL
msg(a, PV, PB, 310, "backup@pbs!pve + secreto", 53, end=75, still=1)
at(a, a.box(PB - 230, 340, 400, 120, a.INK, rx=12) + tline(a, PB - 212, 370, "ACL /datastore/main", SKY)
   + tline(a, PB - 212, 398, "backup@pbs!pve: DatastoreBackup", MINT) + tline(a, PB - 212, 426, "crear y leer: sí", MINT)
   + tline(a, PB - 212, 450, "borrar: no", CORAL), 57, 75, still=1)
msg(a, PB, PV, 490, "autorizado", 62, end=75, still=1, color=a.OK)
# paso 4: backup de prueba
for i in range(5):
    a.add(travel(a, a.box(-12, -9, 24, 18, a.CYAN, rx=4), [(PV, 330), (PB, 330)], 78 + i * 1.6, 81 + i * 1.6, hold=0.1, fade=0.3))
at(a, a.text((PV + PB) / 2, 318, "trozos nuevos de la VM 100", 16, a.CYAN, a.MONO, 600, "middle"), 78, 100)
at(a, a.box(PB - 230, 360, 400, 92, a.WHITE, a.OK, rx=12, sw=2) + a.text(PB - 212, 390, "Content", 15, a.GREY, a.SANS, 600)
   + a.text(PB - 212, 420, "vm/100 · 2026-10-29 21:00", 15, a.OK, a.MONO, 700), 88, 100)
at(a, chip(a, PV - 200, 380, "backup OK", "ok"), 90, 100)

status(a, 600, [
    (0, 25, "El secreto del token lo muestra PBS una sola vez: va al gestor de contraseñas.", a.AMB, 0),
    (25, 50, "La huella asegura que hablás con tu PBS y no con un equipo que se hace pasar por él.", a.BLUE, 0),
    (50, 75, "El token entra con el permiso justo: escribir backups, nunca borrarlos.", a.OK, 1),
    (75, 100, "La prueba termina en PBS: el backup tiene que aparecer en Content.", a.OK, 0),
])
at(a, a.text(600, 632, "Si la huella no coincide, PVE no se conecta: conviene revisarla en el dashboard de PBS.", 16, a.GREY, a.SANS, 400, "middle"), 25, 50)

write(a, 8, "l2", "Huella, token y permiso: la primera conexión",
      "Animación en cuatro tiempos entre pve1 con Proxmox VE y un Proxmox Backup Server en 10.10.10.30, puerto 8007, con el datastore main. "
      "1: en Datacenter, Storage, Add, Proxmox Backup Server se cargan el servidor 10.10.10.30, el datastore main, el usuario backup@pbs!pve, como contraseña el secreto del token y la huella del certificado; el secreto lo muestra PBS una sola vez. "
      "2: PVE abre TLS al puerto 8007, PBS presenta su certificado y PVE compara la huella recibida con la cargada; coinciden, así que es ese PBS y no otro equipo. Si no coincidiera, PVE no se conecta. "
      "3: PVE se presenta con backup@pbs!pve y el secreto; PBS revisa el ACL de /datastore/main, donde el token tiene DatastoreBackup: crear y leer sí, borrar no; contesta autorizado. "
      "4: en el backup de prueba suben los trozos nuevos de la VM 100 y en Content de PBS aparece vm/100 con la fecha del backup.",
      [8, 44, 66, 72, 94])
