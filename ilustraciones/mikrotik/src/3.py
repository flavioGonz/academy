"""Lección 3 · Cerrar puertas: principal + pasos 1, 2 y 3."""
from _mt import *

K = "MikroTik"

# ------------------------------------------------------------------ 3.svg principal
c = Canvas(K, "La gestión no mira a internet")
inet = c.add(Internet(48, 170, "Internet", "escaneos automáticos", hl=ALERT, w=250))
tec = c.add(Person(48, 420, "Técnico afuera", "con VPN", hl=OK, w=250))
RX, RY, RW, RH = 400, 140, 420, 380
c.add(rect(RX, RY, RW, RH, DEEP, DEEP, 2, 22))
c.add(text(RX + 24, RY + 40, "Router del cliente", 21, 600, WHITE, FD))
c.add(text(RX + 24, RY + 66, "/ip/service", 15, 500, CYAN, FM))
svc = [("winbox", "8291", "LAN o VPN", "ok"), ("ssh", "22", "LAN o VPN", "ok"), ("telnet", "23", "apagado", "gray"),
       ("ftp", "21", "apagado", "gray"), ("www", "80", "apagado", "gray"), ("api", "8728", "apagado", "gray")]
for i, (n, p, st, k) in enumerate(svc):
    yy = RY + 92 + i * 44
    c.add(rect(RX + 20, yy, RW - 40, 36, "#0B3A66", "#0B3A66", 0, 8))
    on = k == "ok"
    c.add(text(RX + 36, yy + 24, n, 15, 600, WHITE if on else "#6E88A1", FM))
    c.add(text(RX + 150, yy + 24, p, 15, 400, "#9FC3E3" if on else "#6E88A1", FM))
    c.add(pill(RX + RW - 36, yy + 24, st, k, anchor="end") if False else "")
    w = len(st) * 9.2 + 26
    c.add(pill(RX + RW - 36 - w, yy + 24, st, "ok" if on else "dark", anchor="start"))
    if not on:
        c.add(line(RX + 34, yy + 18, RX + 200, yy + 18, "#6E88A1", 1.5))
# flechas
c.add(Cable(inet.right(), (RX - 6, RY + 130), kind="alert"))
c.add(mark(350, 228, ok=False))
c.add(text(48, 284, "WinBox o SSH desde internet: no", 15, 600, ALERT, FB))
c.add(Cable(tec.right(), (RX - 6, RY + 330), kind="logical", label="túnel VPN", label_at=.5, label_dy=36))
c.add(mark(346, 436, ok=True))
lan = c.add(Laptop(902, 240, "Notebook en la LAN", "192.168.88.0/24", hl=OK, w=250))
c.add(Cable((RX + RW + 6, RY + 120), lan.left(), kind="ok"))
c.add(Note(870, 380, 282, "available-from corta la conexión, pero el puerto se sigue viendo. Para esconderlo: drop en input (lección 21).", kind="warn", size=15))
c.add(Note(48, 560, 1104, "Cada servicio que escucha es una puerta más. Lo que no usás, se apaga; lo que usás, solo desde la LAN o el túnel.", kind="info", size=16))
save(c, "3.svg")

# ------------------------------------------------------------------ 3-paso1.svg
c = Canvas(K + " · Paso 1", "Apagá lo que no usás y limitá lo que queda")
rows_ = [["telnet", "23", ("apagado", "pill:gray"), "sin cifrar: la clave viaja en texto plano"],
         ["ftp", "21", ("apagado", "pill:gray"), "para pasar archivos usá WinBox (Files)"],
         ["www", "80", ("apagado", "pill:gray"), "WebFig sin cifrar"],
         ["api", "8728", ("apagado", "pill:gray"), "solo si un sistema la usa de verdad"],
         ["winbox", "8291", ("192.168.88.0/24", "pill:ok"), "available-from: solo la LAN"],
         ["ssh", "22", ("192.168.88.0/24", "pill:ok"), "available-from: solo la LAN"]]
t, h = ctable(48, 140, ["Servicio", "Puerto", "Queda", "Por qué"], rows_, [170, 120, 260, 554], row_h=50,
              col_fonts=[FM, FM, FM, FB])
c.add(t)
lines = [("/ip/service/disable telnet,ftp,www,api", "#D9E9F8"),
         ("/ip/service/set winbox,ssh available-from=192.168.88.0/24", "#D9E9F8")]
tt, th = code(48, 140 + h + 24, 1104, lines, title="TERMINAL")
c.add(tt)
save(c, "3-paso1.svg")

# ------------------------------------------------------------------ 3-paso2.svg
c = Canvas(K + " · Paso 2", "MAC server y descubrimiento, solo hacia la LAN")
svg, anc, w = port_router(400, 150, ["ether1", "ether2", "ether3", "ether4", "ether5"], colors={"ether1": WARN, "ether2": BLUE, "ether3": BLUE, "ether4": BLUE, "ether5": BLUE},
                          name="Router", sub="allowed-interface-list=LAN")
c.add(svg)
# WAN
c.add(Internet(48, 360, "Red del proveedor", "lado WAN", hl=ALERT, w=270))
c.add(Cable((183, 360), anc["ether1"], kind="data"))
c.add(mark(300, 360, ok=False))
c.add(wrap(48, 478, "No ve el router en Neighbors ni puede entrar por MAC.", 280, 16, 500, ALERT)[0])
# LAN
lan = c.add(Laptop(860, 360, "Notebook en la LAN", "WinBox · Neighbors", hl=OK, w=292))
c.add(Cable((1006, 360), anc["ether4"], kind="data"))
c.add(mark(1134, 360, ok=True))
c.add(wrap(860, 478, "Lo ve en Neighbors y entra por MAC si hace falta.", 292, 16, 500, OK)[0])
c.add(caption(400, 330, "Además, apagados"))
c.add(pills(400, 366, ["bandwidth-server", "socks"], "gray"))
c.add(pills(400, 406, ["proxy", "upnp"], "gray"))
c.add(Note(48, 540, 1104, "La lista LAN viene en la configuración por defecto. Si el equipo no la tiene (un CCR, un CHR), creala antes y poné ahí el bridge: si no, te quedás sin MAC-WinBox también en la LAN.", kind="warn", size=16))
save(c, "3-paso2.svg")

# ------------------------------------------------------------------ 3-paso3.svg
c = Canvas(K + " · Paso 3", "Equipo heredado: qué buscar y qué es raro")
rows_ = [["/system/scheduler/print", ("vacío o tareas que reconocés", OK), ("tareas que bajan cosas con fetch", ALERT)],
         ["/system/script/print", ("scripts propios, documentados", OK), ("scripts que nadie conoce", ALERT)],
         ["/ip/socks/print", ("enabled: no", OK), ("SOCKS habilitado", ALERT)],
         ["/interface/l2tp-client/print", ("vacío o tus túneles", OK), ("cliente desconocido, ej. lvpn", ALERT)],
         ['filter where dst-port~"5678"', ("ninguna regla", OK), ("regla que acepta el 5678", ALERT)]]
t, h = ctable(48, 140, ["Comando", "Normal", "Sospechoso"], rows_, [400, 330, 374], row_h=52, col_fonts=[FM, FB, FB])
c.add(t)
c.add(Note(48, 140 + h + 24, 540, "Si aparece algo sospechoso: contraseña nueva para todos los usuarios, revisión del firewall y nota en el legajo del cliente.", title="Si encontrás algo", kind="alert", size=16))
c.add(Note(612, 140 + h + 24, 540, "En Mēris los atacantes entraron en 2018 y dejaron su configuración. Actualizar no la borra: hay que buscarla.", title="Por qué no alcanza con actualizar", kind="info", size=16))
save(c, "3-paso3.svg")
