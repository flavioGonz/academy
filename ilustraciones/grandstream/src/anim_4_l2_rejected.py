#!/usr/bin/env python3
"""Lección 4 · Laboratorio, paso 3: qué hay detrás de un Rejected en el Dashboard. Dos causas: la UCM no llega al
proveedor (el host no resuelve o no responde) o llega y las credenciales no coinciden. Fuentes: la lección
(Rejected = alcance al servidor o credenciales; probar que el host resuelve y responde; Auth ID distinto del usuario);
RFC 3261 (REGISTER, 401 con desafío, rechazo cuando la respuesta no coincide)."""
from _anim_gs_red import R

g = R(T=28, fix=73, kicker="GRANDSTREAM · TRONCAL REGISTRADO · LABORATORIO",
      title="Rejected: no llega o no lo reconocen")
g.steps([
    "Primero la UCM pregunta la IP del host: si el DNS no contesta, no hay a quién registrarse.",
    "Resuelve y manda REGISTER, pero no vuelve nada: salida a internet o firewall.",
    "Llega y recibe el 401, pero la respuesta va con otro Auth ID: el proveedor la rechaza.",
    "Usuario, Auth ID y clave copiados del proveedor: 200 OK y Registered.",
])

XU, XD, XP = 150, 450, 760
g.lane(XU, 176, 600, "UCM", "Proveedor_Lab", w=220)
g.lane(XD, 176, 600, "DNS", "de la red", w=180)
g.lane(XP, 176, 600, "Proveedor", "sip.proveedor.example", w=230)
S = [0, 25, 50, 75, 100]
# 1 · DNS sin respuesta
g.msg(XU, XD, 270, "¿sip.proveedor.example?", g.BLUE, 3, 9, hold=25)
g.appear(g.text(XD + 20, 314, "sin respuesta", 15, g.BAD, g.MONO, 600) + g.mark(XD + 175, 309, False, 13), 12, 25)
# 2 · resuelve, REGISTER que no vuelve
g.msg(XU, XD, 270, "¿sip.proveedor.example?", g.BLUE, 27, 31, hold=50)
g.msg(XD, XU, 310, "198.51.100.20", g.OK, 32, 36, hold=50)
g.arrow([(XU, 380), (XP - 200, 380)], 38, 44, g.BLUE, hold=50)
g.appear(g.text((XU + XP - 200) / 2, 370, "REGISTER", 15, g.BLUE, g.MONO, 600, "middle"), 41, 50)
g.appear(g.mark(XP - 180, 380, False, 13) + g.text(XP - 160, 386, "no vuelve nada", 15, g.BAD, g.MONO, 600), 45, 50)
# 3 · credenciales
g.msg(XU, XP, 380, "REGISTER 21000000", g.BLUE, 52, 57, hold=75)
g.msg(XP, XU, 424, "401 · desafío", g.GREY, 58, 62, hold=75, dashed=True)
g.msg(XU, XP, 468, "REGISTER + respuesta (Auth ID mal)", g.BLUE, 63, 67, hold=75)
g.msg(XP, XU, 512, "rechazo", g.BAD, 68, 72, hold=75)
# 4 · bien
g.msg(XU, XP, 380, "REGISTER 21000000", g.BLUE, 77, 81)
g.msg(XP, XU, 424, "401 · desafío", g.GREY, 82, 85, dashed=True)
g.msg(XU, XP, 468, "REGISTER + respuesta correcta", g.BLUE, 86, 89)
g.msg(XP, XU, 512, "200 OK", g.OK, 90, 93)

# Dashboard
DX, DW = 930, 222
g.add(g.box(DX, 186, DW, 150, g.WHITE, g.LINE, rx=14))
g.add(g.text(DX + 18, 216, "Dashboard · Trunks", 15, g.GREY, g.MONO))
g.add(g.text(DX + 18, 252, "Proveedor_Lab", 17, g.INK, g.MONO, 600))
g.appear(g.pill(DX + 18, 276, "Rejected", g.BAD, g.BADBG, 15, 32), 0, 93)
g.appear(g.pill(DX + 18, 276, "Registered", g.OK, g.OKBG, 15, 32), 93, 100)
g.appear(g.note(DX, 356, DW, "Probá", ["desde una PC de", "la misma red: que", "el host resuelva", "y responda."], "amb", size=15, lh=21), 0, 50)
g.appear(g.note(DX, 356, DW, "Pegá de nuevo", ["usuario, Auth ID", "y contraseña: el", "Auth ID puede ser", "distinto del usuario."], "amb", size=15, lh=21), 50, 75)
g.appear(g.note(DX, 356, DW, "Listo", ["después, las cuatro", "pruebas: sale, entra,", "número y tonos."], "ok", size=15, lh=21), 75, 100)

g.status(636, [
    (0, 25, "Causa 1: alcance. Sin la IP del host, el REGISTER ni sale.", g.BAD),
    (25, 50, "Causa 1: alcance. El pedido sale y nadie contesta.", g.BAD),
    (50, 75, "Causa 2: credenciales. Llega, pero la cuenta no coincide.", g.BAD),
    (75, 100, "Con los datos del proveedor, el troncal registra.", g.OK),
])

g.done(4, "l2", "Rejected: no llega o no lo reconocen",
       "Animación en cuatro tiempos con tres líneas de vida, la UCM con el troncal Proveedor_Lab, el DNS de la red y el proveedor sip.proveedor.example, y a la derecha el estado del troncal en Dashboard, Trunks. "
       "1: la UCM pregunta la IP de sip.proveedor.example y el DNS no contesta: no hay a quién registrarse y el troncal queda Rejected. "
       "2: el DNS responde 198.51.100.20, la UCM manda REGISTER y no vuelve nada, por la salida a internet o un firewall; sigue Rejected. Se prueba desde una PC de la misma red que el host resuelva y responda. "
       "3: el REGISTER 21000000 llega, el proveedor responde 401 con el desafío, la UCM contesta con una respuesta hecha con otro Auth ID y el proveedor la rechaza; sigue Rejected. Se vuelven a pegar usuario, Auth ID y contraseña. "
       "4: con los datos del proveedor copiados y pegados, el proveedor responde 200 OK y el troncal pasa a Registered.",
       [8, 40, 68, 95])
