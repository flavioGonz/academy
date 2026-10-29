"""Lección 12 · Torch y sniffer."""
from _comun_12_22 import *

K = "MikroTik"

# ---------------------------------------------------------------- principal: dónde mirar
c = Canvas(K, "Torch y sniffer: mirá en la LAN, no en la WAN")
cam = c.add(Camera(48, 180, "Cámara", "192.168.88.50", w=240))
rt = c.add(Box(470, 160, 270, 124, "Router", "masquerade (NAT)", dark=True))
net = c.add(Internet(922, 180, "Internet", "8.8.8.8", w=230))
c.add(Cable(cam.right(), rt.left(), "data", label="bridge", label_dy=-14))
c.add(Cable(rt.right(), net.left(), "data", label="ether1", label_dy=-14))
c.add(Chip(379, 316, "LAN", "gray", anchor="middle"))
c.add(Chip(831, 316, "WAN", "warn", anchor="middle"))

# panel LAN: lo que ve Torch
c.add(panel(48, 350, 530, 200, "Torch en bridge", "ok"))
c.add(Mark(536, 384, True))
c.add(Table(68, 400, ["origen", "destino", "puerto"], [["192.168.88.50", "8.8.8.8", "53"], ["192.168.88.50", "NVR", "554"]], [190, 140, 160], mono_cols=(0, 1, 2), row_h=40))
c.add(Label(68, 538, "Ves la IP de cada equipo: sabés quién es quién.", 16, 500, OK))

# panel WAN
c.add(panel(622, 350, 530, 200, "Torch en ether1", "alert"))
c.add(Mark(1110, 384, False))
c.add(Table(642, 400, ["origen", "destino", "puerto"], [["IP del router", "8.8.8.8", "53"], ["IP del router", "…", "…"]], [190, 140, 160], mono_cols=(0, 1, 2), row_h=40))
c.add(Label(642, 538, "Después del NAT todo tiene la IP del router.", 16, 500, ALERT))

c.add(Note(48, 576, 1104, "Torch ve los paquetes antes del firewall y apaga FastTrack mientras corre (sube la CPU): prendelo, mirá y apagalo.", kind="warn", size=16))
save(c, "12.svg")

# ---------------------------------------------------------------- paso 1: escalera de herramientas
c = Canvas(K + " · Paso 1", "Primero preguntá, después mirá, después capturá")
cols = [
    ("1 · Preguntar", "ping · traceroute", "¿Hay camino hasta 8.8.8.8? ¿Hasta qué salto llega?", "Genera tráfico de prueba."),
    ("2 · Mirar", "Torch", "¿Qué hace la cámara ahora? Flujos y tasas en vivo.", "No genera nada: observa."),
    ("3 · Capturar", "sniffer → .pcap", "¿Qué dicen los paquetes? Se abre en Wireshark.", "Guarda a archivo."),
    ("4 · Registrar", "log=yes", "¿Qué regla del firewall descarta y a quién?", "Temporal: después log=no."),
]
x0, wcol, gap = 48, 249, 36
for i, (t, tool, q, foot) in enumerate(cols):
    x = x0 + i * (wcol + gap)
    y = 150 + (3 - i) * 26
    hgt = 420 - (3 - i) * 26
    c.add(panel(x, y, wcol, hgt, t, "dark" if i == 0 else "info"))
    c.add(pill(x + 20, y + 54, wcol - 40, 38, tool, CYAN if i == 0 else BLUE, WHITE, 16))
    c.add(para(x + 20, y + 130, q, wcol - 40, 17, INK if i else WHITE, 500))
    c.add(para(x + 20, y + hgt - 44, foot, wcol - 40, 15, "#9FC3E3" if i == 0 else INK3, 400, FB))
    if i < 3:
        c.add(Arrow((x + wcol + 4, y + 200), (x + wcol + gap - 4, y + 200), kind="flow", bend="straight"))
c.add(Label(48, 632, "Subís de escalón solo si el anterior no alcanza para explicar la falla.", 17, 500, INK2))
save(c, "12-paso1.svg")

# ---------------------------------------------------------------- paso 2: leer la tasa en Torch
c = Canvas(K + " · Paso 2", "¿Qué hace la cámara? Leé la tasa en Torch")
c.add(Terminal(48, 130, 1104, ["/tool/torch bridge src-address=192.168.88.50/32 duration=20s"], title="TERMINAL · ROUTEROS 7"))
# panel A: cae a cero
c.add(panel(48, 230, 530, 300, "Cae a cero a ratos", "warn"))
c.add(Label(68, 290, "tasa de la cámara (TX/RX)", 15, 500, INK3, FM))
c.add(sparkline(68, 310, 490, 120, [.7, .75, .72, 0, 0, .68, .74, .7, .02, 0, 0, .7, .73, .71, .69, 0, .72, .7], WARN))
c.add(para(68, 470, "El problema está antes del router: mirá la cámara y el cable.", 490, 17, INK, 500))
# panel B: parejo
c.add(panel(622, 230, 530, 300, "Fluye parejo", "ok"))
c.add(Label(642, 290, "tasa de la cámara (TX/RX)", 15, 500, INK3, FM))
c.add(sparkline(642, 310, 490, 120, [.7, .72, .71, .73, .7, .72, .71, .7, .72, .73, .71, .7, .72, .71, .7, .72, .71, .7], OK))
c.add(para(642, 470, "La cámara manda bien: el problema está del lado del NVR. Mirá el NVR.", 490, 17, INK, 500))
c.add(Label(48, 580, "Para ver solo el video: /tool/torch bridge ip-protocol=tcp port=554 (RTSP).", 17, 500, INK2))
save(c, "12-paso2.svg")

# ---------------------------------------------------------------- paso 3: sniffer a Wireshark
c = Canvas(K + " · Paso 3", "Capturá 30 segundos y abrilo en Wireshark")
rt = c.add(Box(48, 170, 300, 124, "Router", "sniffer en bridge", dark=True))
c.add(Chip(198, 330, "ip-address=192.168.88.50/32", "gray", anchor="middle"))
c.add(file_icon(520, 180, "camara.pcap", "/file/print"))
c.add(Arrow(rt.right(), (508, 232), "start · stop", label_dy=-14))
nb = c.add(Laptop(800, 190, "Notebook", "Wireshark", w=300))
c.add(Arrow((600, 232), nb.left(), "bajar el archivo", label_dy=-14))
c.add(Chip(950, 330, "filtro: dns  o  rtsp", "cyan", anchor="middle"))
# tamaños
c.add(panel(48, 400, 530, 130, "Pesa 24 bytes", "alert"))
c.add(para(68, 466, "No capturó nada: revisá interfaz (bridge) y la IP del filtro antes de volver a probar.", 490, 17, INK, 500))
c.add(panel(622, 400, 530, 130, "Pesa más que eso", "ok"))
c.add(para(642, 466, "Hay paquetes: bajalo desde Files y abrilo en la notebook.", 490, 17, INK, 500))
c.add(Note(48, 576, 1104, "En producción: duración corta, filtro por IP y file-limit=10000KiB. Una captura llena el disco rápido.", kind="warn", size=16))
save(c, "12-paso3.svg")
