"""Teoría lección 11: cuándo reinicia Windows después de actualizar, y la opción 7 en servidores."""
from _awin import *

a = new(24, "Cuándo reinicia Windows después de actualizar")
a.steps(["La actualización se descarga e instala en segundo plano.",
         "Dentro de las horas activas, Windows no reinicia.",
         "Fuera de horario y sin nadie conectado: reinicia solo.",
         "En un servidor con opción 7: avisa y espera a alguien."], still=3)
X0, W = 80, 1040


def hx(h):
    return X0 + W * h / 24


a.add(a.box(X0, 220, W, 64, a.WHITE, a.LINE, rx=12))
a.add(a.box(hx(8), 220, hx(17) - hx(8), 64, a.OKBG, a.OK, rx=12) + a.text((hx(8) + hx(17)) / 2, 258, "horas activas 8 a 17", 17, a.OK, a.SANS, 600, "middle"))
for h in range(0, 25, 4):
    a.add(a.text(hx(h), 312, f"{h:02d}:00", 14, a.GREY, a.MONO, 500, "middle"))
# reloj que avanza
mv = a.move([(0, hx(10), 0), (25, hx(10), 0), (50, hx(16), 0), (60, hx(22), 0), (75, hx(23), 0), (100, hx(23), 0)])
a.add(a.group(f'<path d="M0 200V300" stroke="{a.INK}" stroke-width="3"/><circle cx="0" cy="200" r="7" fill="{a.INK}"/>', mv, still=None))
# 1: instala
at(a, a.box(80, 390, 500, 80, "#E5F0FB", a.BLUE, rx=14, sw=2) + a.text(100, 422, "Actualización instalada", 18, a.BLUE, a.HEAD, 600)
   + a.text(100, 450, "falta reiniciar para terminar", 15, a.TXT, a.SANS, 500), 0, 100, 1)
# 2: espera
at(a, chip(a, 620, 400, "no reinicia: horas activas", "ok"), 25, 50, 0)
# 3: reinicia solo
at(a, a.box(620, 390, 532, 80, a.AMBBG, a.AMB, rx=14, sw=2) + a.text(640, 422, "Sin sesión activa: reinicia solo", 18, a.AMB, a.HEAD, 600)
   + a.text(640, 450, "solo cuentan sesiones locales o RDP activas", 15, a.TXT, a.SANS, 500), 50, 75, 0)
# 4: opción 7
at(a, a.box(620, 390, 532, 80, a.OKBG, a.OK, rx=14, sw=2) + a.text(640, 422, "Opción 7: avisar e instalar · avisar y reiniciar", 17, a.OK, a.HEAD, 600)
   + a.text(640, 450, "el técnico elige la ventana, con backup hecho", 15, a.TXT, a.SANS, 500), 75, 100, 1)
caption(a, 560, [(0, 25, "Instalar no es lo mismo que terminar: muchos cambios recién se aplican al reiniciar.", None),
                 (25, 50, "De fábrica van de 8 a 17; el rango máximo es de 18 horas.", a.OK),
                 (50, 75, "Un servidor del VMS casi nunca tiene a alguien conectado: se reinicia de madrugada.", a.AMB),
                 (75, 100, "Para servidores, Microsoft sugiere que avise antes de instalar y de reiniciar.", a.OK)], still=3)
write(a, "11-t1.svg", "Cuándo reinicia Windows después de actualizar",
      "Animación en cuatro tiempos sobre una barra de 24 horas con las horas activas de 8 a 17 marcadas en verde y un indicador de la hora que avanza. "
      "1: una actualización se descarga e instala en segundo plano y queda pendiente de reinicio. 2: mientras la hora está dentro de las horas activas, Windows no reinicia. "
      "3: fuera de ese horario y sin sesiones locales ni de escritorio remoto activas, el equipo se reinicia solo. "
      "4: en un servidor configurado con la opción 7, Windows avisa antes de instalar y de reiniciar, y el técnico elige la ventana con el backup hecho.", pcts=(12, 37, 62, 90))
