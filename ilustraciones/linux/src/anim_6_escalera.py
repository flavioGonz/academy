"""Teoría lección 6: subir la escalera hasta el escalón que falla (DNS) y netplan try."""
from _alnx import *

# ------------------------------------------------------------------ 6-t1: escalera
a = new(20, "Subir la escalera hasta el escalón que falla")
a.steps(["ip -br addr e ip route: hay IP y ruta por defecto.",
         "ping al gateway 192.168.88.1: responde.",
         "ping a 1.1.1.1: responde. Hay salida a internet.",
         "ping a debian.org: no resuelve. Es DNS."], still=3)
rows = [("1", "Interfaz", "ip -br addr", "ens18 UP 192.168.88.50/24"),
        ("2", "Gateway", "ping -c3 192.168.88.1", "3 received"),
        ("3", "IP pública", "ping -c3 1.1.1.1", "3 received"),
        ("4", "Nombre", "ping -c3 debian.org", "Temporary failure in name resolution")]
for i, (n, t, cmd, res) in enumerate(rows):
    y = 500 - i * 92
    x = 48 + i * 60
    a.add(a.box(x, y, 1104 - i * 60, 76, a.WHITE, a.LINE, rx=12))
    a.add(a.box(x + 16, y + 20, 36, 36, a.SLATE, None, rx=18) + a.text(x + 34, y + 44, n, 17, a.GREY, a.MONO, 700, "middle"))
    a.add(a.text(x + 66, y + 32, t, 18, a.INK, a.HEAD, 600))
    a.add(mono(a, x + 66, y + 58, cmd, 15, a.BLUE, 600))
    ok = i < 3
    t0 = i * 25 + 4
    col, bg, kind = (a.OK, a.OKBG, "ok") if ok else (a.BAD, a.BADBG, "bad")
    at(a, a.box(x, y, 1104 - i * 60, 76, "none", col, rx=12, sw=3) + a.box(x + 16, y + 20, 36, 36, col, None, rx=18)
       + a.text(x + 34, y + 44, n, 17, "#FFFFFF", a.MONO, 700, "middle"), t0, 100, 1)
    at(a, mono(a, 1130, y + 46, res, 15, col, 700, "end"), t0 + 3, 100, 1)
at(a, a.box(708, 142, 444, 72, a.BADBG, a.BAD, rx=12, sw=2) + a.text(728, 170, "IP pública sí, nombre no: es DNS.", 17, a.BAD, a.SANS, 700)
   + a.text(728, 196, "Revisá los nameservers (dig, netplan).", 16, a.INK, a.SANS, 500), 82, 100, 1)
caption(a, 620, [(0, 25, "Sin IP o sin ruta por defecto, nada de lo de arriba puede andar.", None),
                 (25, 50, "Si el gateway no responde, el problema está en la red local.", None),
                 (50, 75, "Llegar a una IP pública prueba ruta y salida, sin depender del DNS.", a.OK),
                 (75, 100, "El primer escalón que falla es el problema: no hace falta seguir adivinando.", a.BAD)], still=3)
write(a, "6-t1.svg", "Subir la escalera hasta el escalón que falla",
      "Animación en cuatro tiempos con cuatro escalones que suben de izquierda a derecha. 1: interfaz, ip -br addr muestra ens18 UP con 192.168.88.50/24, en verde. "
      "2: gateway, ping a 192.168.88.1 con 3 paquetes recibidos, en verde. 3: IP pública, ping a 1.1.1.1 con 3 recibidos, en verde. "
      "4: nombre, ping a debian.org falla con Temporary failure in name resolution, en rojo, y un recuadro dice que si la IP pública responde y el nombre no, es DNS y hay que revisar los nameservers.")

# ------------------------------------------------------------------ 6-t2: netplan try
a = new(20, "netplan try: si no confirmás, vuelve solo")
a.steps(["netplan try aplica la IP nueva y empieza a contar 120 s.",
         "Seguís conectado: apretás Enter y el cambio queda.",
         "Otra vez, pero la IP nueva te deja sin conexión.",
         "Sin Enter en 120 s, vuelve solo a la configuración anterior."], still=3)
X0, X1 = 120, 1080
for y, title in [(220, "Cambio que anda"), (420, "Cambio que te deja afuera")]:
    a.add(a.text(48, y - 26, title, 18, a.INK, a.HEAD, 600))
    a.add(line(a, f"M{X0} {y + 40}H{X1}", a.LINE, 8))
    a.add(mono(a, X0, y + 80, "0 s", 15, a.GREY, 500, "middle"))
    a.add(mono(a, X1, y + 80, "120 s", 15, a.GREY, 500, "middle"))
    a.add(a.box(X0 - 72, y + 18, 60, 44, a.SLATE, None, rx=10) + mono(a, X0 - 42, y + 47, "try", 15, a.INK, 700, "middle"))
# carril 1: confirma
mv1 = a.move([(0, X0, 260), (2, X0, 260), (40, X0 + 260, 260), (100, X0 + 260, 260)])
a.add(a.group(dot(a, 0, 0, 12, a.BLUE), mv1, a.show(0, 100), still=0))
at(a, a.box(X0 + 210, 160, 120, 44, a.OK, None, rx=10) + mono(a, X0 + 270, 189, "Enter", 17, "#FFFFFF", 700, "middle"), 28, 100, 1)
at(a, a.text(X0 + 360, 248, "La IP nueva queda fija.", 17, a.OK, a.SANS, 700) + a.text(X0 + 360, 272, "El contador se detiene.", 16, a.TXT, a.SANS, 500), 30, 100, 1)
# carril 2: sin conexión
mv2 = a.move([(0, X0, 460), (50, X0, 460), (90, X1, 460), (100, X1, 460)])
a.add(a.group(dot(a, 0, 0, 12, a.AMB), mv2, a.show(50, 100), still=0))
at(a, a.box(X0 + 300, 360, 330, 44, a.BADBG, a.BAD, rx=10, sw=2) + a.text(X0 + 320, 389, "sesión SSH cortada: no hay Enter", 16, a.BAD, a.SANS, 700), 56, 100, 1)
at(a, a.box(X1 - 330, 516, 330, 64, a.OKBG, a.OK, rx=12, sw=2) + a.text(X1 - 312, 544, "Vuelve la configuración anterior", 16, a.OK, a.SANS, 700)
   + a.text(X1 - 312, 568, "y podés volver a entrar.", 16, a.INK, a.SANS, 500), 90, 100, 1)
caption(a, 625, [(0, 25, "try aplica igual que apply, pero deja una red de seguridad.", None),
                 (25, 50, "Confirmás con Enter solo si seguís conectado: esa es la prueba.", a.OK),
                 (50, 75, "Un gateway mal cargado o una máscara equivocada te cortan la sesión.", a.AMB),
                 (75, 100, "netplan apply no tiene esta vuelta; en Debian con ifupdown, consola a mano.", a.OK)], still=3)
write(a, "6-t2.svg", "netplan try: si no confirmás, vuelve solo",
      "Animación en cuatro tiempos con dos líneas de tiempo de 0 a 120 segundos. Arriba, un cambio que anda: 1: netplan try aplica la IP nueva y empieza a contar. "
      "2: el técnico sigue conectado, aprieta Enter y la IP nueva queda fija. Abajo, un cambio que deja afuera: 3: la sesión SSH se corta y no hay forma de apretar Enter. "
      "4: el contador llega a 120 segundos y netplan vuelve solo a la configuración anterior, y se puede volver a entrar. Se aclara que netplan apply no tiene esta vuelta y que en Debian con ifupdown hace falta la consola.")
