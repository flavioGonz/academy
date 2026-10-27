"""Teoría lección 3: qué hace Test-NetConnection -Port por dentro (inicio de conexión TCP)."""
from _awin import *

a = new(20, "Test-NetConnection -Port: tres respuestas posibles")
a.steps(["Tu equipo manda SYN al puerto 554: quiero conectar.",
         "El servicio escucha y contesta SYN/ACK: True.",
         "Nadie escucha en 8443: vuelve RST, False enseguida.",
         "Un firewall descarta el SYN: silencio, False por tiempo."], still=1)
XL, XR = 330, 880
a.add(card(a, 48, 190, 230, 96, "Tu equipo", "Test-NetConnection", dark=True))
a.add(card(a, 922, 190, 230, 96, "Cámara", "192.168.88.20"))
a.add(line(a, f"M{XL} 210V560", a.LINE, 2, "6 6") + line(a, f"M{XR} 210V560", a.LINE, 2, "6 6"))


def msg(y, label, color, s, e, back=False, still=0, x2=None):
    x1, xe = (XR, XL + 8) if back else (XL, (x2 or XR) - 8)
    at(a, a.arrow(f"M{x1} {y}H{xe}", color, 4) + a.text((XL + XR) / 2, y - 12, label, 16, color, a.MONO, 600, "middle"), s, e, still)


def result(y, label, kind, s, e, still=0):
    at(a, chip(a, 1152, y - 20, label, kind, size=16, anchor="end"), s, e, still)


# 1 y 2: puerto abierto
msg(270, "SYN → 554", a.BLUE, 0, 50, still=1)
msg(330, "SYN/ACK", a.OK, 25, 50, back=True, still=1)
result(350, "TcpTestSucceeded : True", "ok", 27, 50, still=1)
# 3: puerto cerrado
msg(420, "SYN → 8443", a.BLUE, 50, 75)
msg(480, "RST · nadie escucha", a.BAD, 53, 75, back=True)
result(500, "False, al instante", "bad", 55, 75)
# 4: firewall que descarta
msg(420, "SYN → 8443", a.BLUE, 75, 100, x2=760)
at(a, a.box(770, 380, 36, 90, a.BAD, None, rx=8) + a.text(788, 434, "×", 28, "#fff", a.SANS, 700, "middle")
   + a.text(788, 494, "firewall", 15, a.BAD, a.MONO, 600, "middle"), 77, 100, 0)
at(a, a.text(600, 540, "… espera … sin respuesta …", 17, a.GREY, a.MONO, 600, "middle"), 80, 100, 0)
result(580, "False, por tiempo", "bad", 85, 100)
caption(a, 630, [(0, 25, "Es el mismo inicio de conexión que usa el VMS o el navegador, pero sin abrir sesión.", None),
                 (25, 50, "True: hay un programa escuchando ese puerto y la red deja pasar.", a.OK),
                 (50, 75, "Un RST dice que el equipo está, pero ese servicio no: revisá el puerto o el servicio.", a.BAD),
                 (75, 100, "El silencio suele ser un firewall en el medio o en el equipo: revisá reglas.", a.BAD)], still=1)
write(a, "3-t1.svg", "Test-NetConnection -Port: tres respuestas posibles",
      "Animación en cuatro tiempos entre tu equipo y una cámara 192.168.88.20. 1: tu equipo manda un SYN al puerto 554 para iniciar la conexión TCP. "
      "2: el servicio escucha y contesta SYN/ACK, y Test-NetConnection muestra TcpTestSucceeded True. 3: al puerto 8443, donde nadie escucha, la cámara contesta RST y el resultado es False al instante. "
      "4: si un firewall descarta el SYN no vuelve nada, Test-NetConnection espera y da False por tiempo. El cuadro fijo muestra el caso True.")
