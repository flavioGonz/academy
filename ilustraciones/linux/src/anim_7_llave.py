"""Teoría lección 7: autenticación con llave; la privada no viaja."""
from _alnx import *

a = new(20, "Entrar con llave: lo que viaja y lo que no")
a.steps(["El cliente se conecta y ofrece su llave pública.",
         "El servidor la encuentra en authorized_keys y pide la prueba.",
         "El cliente firma datos de esta sesión con la privada.",
         "El servidor verifica la firma con la pública: adentro."], still=3)

# notebook y servidor
a.add(card(a, 48, 176, 380, 330, "Notebook", "tecnico@notebook-2026"))
a.add(a.box(72, 262, 332, 64, a.BADBG, a.BAD, rx=12, sw=2) + mono(a, 92, 290, "id_ed25519", 17, a.BAD, 700)
      + a.text(92, 314, "privada: se queda acá", 15, a.INK, a.SANS, 600))
a.add(a.box(72, 342, 332, 64, a.OKBG, a.OK, rx=12, sw=2) + mono(a, 92, 370, "id_ed25519.pub", 17, a.OK, 700)
      + a.text(92, 394, "pública", 15, a.INK, a.SANS, 600))
a.add(card(a, 772, 176, 380, 330, "Servidor", "192.168.88.50 · ssh"))
a.add(a.box(796, 262, 332, 64, a.OKBG, a.OK, rx=12, sw=2) + mono(a, 816, 290, "authorized_keys", 17, a.OK, 700)
      + a.text(816, 314, "copia de la pública", 15, a.INK, a.SANS, 600))
# canal
a.add(line(a, "M428 340H772", a.LINE, 6, "10 8"))
a.add(a.text(600, 324, "red", 15, a.GREY, a.MONO, 600, "middle"))

# 1: pública viaja
mv = a.move([(0, 470, 300), (2, 470, 300), (20, 730, 300), (100, 730, 300)])
a.add(a.group(pkt(a, "pública", a.OK), mv, a.show(1, 24), still=0))
# 2: servidor la encuentra y pide prueba
at(a, a.box(796, 262, 332, 64, "none", a.CYAN, rx=12, sw=4), 25, 50, 0)
mv2 = a.move([(0, 730, 380), (27, 730, 380), (45, 470, 380), (100, 470, 380)])
a.add(a.group(pkt(a, "probalo", a.BLUE), mv2, a.show(27, 48), still=0))
# 3: firma local
at(a, a.box(72, 262, 332, 64, "none", a.CYAN, rx=12, sw=4), 50, 75, 0)
at(a, a.box(72, 426, 332, 56, a.SLATE, None, rx=12) + a.text(92, 461, "firma = privada + datos de la sesión", 15, a.INK, a.SANS, 600), 52, 100, 1)
mv3 = a.move([(0, 470, 300), (60, 470, 300), (74, 730, 300), (100, 730, 300)])
a.add(a.group(pkt(a, "firma", a.CYAN), mv3, a.show(60, 76), still=0))
at(a, a.text(600, 400, "la privada no viaja", 16, a.BAD, a.SANS, 700, "middle"), 52, 100, 1)
# 4: verificada
at(a, a.box(796, 342, 332, 140, a.OKBG, a.OK, rx=12, sw=2) + a.text(816, 376, "Firma válida con la pública", 17, a.OK, a.SANS, 700)
   + mono(a, 816, 410, "Accepted publickey", 15, a.OK, 700) + mono(a, 816, 434, "for tecnico", 15, a.OK, 700)
   + a.text(816, 466, "sin contraseña", 15, a.INK, a.SANS, 600), 77, 100, 1)

caption(a, 600, [(0, 25, "Lo que viaja primero es la pública: no sirve para entrar sin la privada.", None),
                 (25, 50, "Si la pública no está en authorized_keys, no hay prueba posible.", None),
                 (50, 75, "La frase de paso solo descifra la privada en tu notebook: tampoco viaja.", a.AMB),
                 (75, 100, "No hay contraseña que adivinar: la fuerza bruta no tiene por dónde entrar.", a.OK)], still=3)
write(a, "7-t1.svg", "Entrar con llave: lo que viaja y lo que no",
      "Animación en cuatro tiempos con la notebook a la izquierda, con la llave privada id_ed25519 en rojo y la pública en verde, y el servidor a la derecha, con authorized_keys. "
      "1: la llave pública viaja por la red hacia el servidor. 2: el servidor la encuentra en authorized_keys y devuelve un pedido de prueba. "
      "3: en la notebook se resalta la privada y se arma la firma con la privada y los datos de la sesión; viaja solo la firma, con la leyenda la privada no viaja. "
      "4: el servidor verifica la firma con la pública y registra Accepted publickey for tecnico, sin contraseña.")
