"""Teoría lección 4: en OpenSSH gana el primer valor leído; el snippet .d va primero."""
from _alnx import *

a = new(20, "En SSH gana el primer valor que se lee")
a.steps(["sshd empieza por sshd_config: la primera línea es el Include.",
         "10-ies.conf va primero (orden alfabético): queda no.",
         "50-cloud-init y el archivo principal dicen yes: se ignoran.",
         "sshd -T muestra el valor que quedó en uso: no."], still=3)

files = [(176, "/etc/ssh/sshd_config", ["Include /etc/ssh/sshd_config.d/*.conf"], None),
         (262, "sshd_config.d/10-ies.conf", ["PasswordAuthentication no"], "ok"),
         (348, "sshd_config.d/50-cloud-init.conf", ["PasswordAuthentication yes"], "bad"),
         (434, "/etc/ssh/sshd_config (sigue)", ["PasswordAuthentication yes"], "bad")]
for i, (y, f, ls, kind) in enumerate(files):
    ind = 36 if i in (1, 2) else 0
    a.add(a.box(48 + ind, y, 700 - ind, 74, a.WHITE, a.LINE, rx=12))
    a.add(mono(a, 68 + ind, y + 27, f, 15, a.BLUE, 600))
    a.add(mono(a, 68 + ind, y + 56, ls[0], 17, a.INK, 600))
    if kind == "ok":
        at(a, a.box(48 + ind, y, 700 - ind, 74, "none", a.OK, rx=12, sw=3), 26, 100, 1)
        at(a, chip(a, 730, y + 23, "se usa", "ok", anchor="end"), 30, 100, 1)
    elif kind == "bad":
        at(a, a.box(48 + ind, y, 700 - ind, 74, a.BG, None, rx=12, extra='fill-opacity="0.6"'), 52 + (i - 2) * 6, 100, 1)
        at(a, chip(a, 730, y + 23, "ignorado", "bad", anchor="end"), 52 + (i - 2) * 6, 100, 1)
# cursor de lectura
mv = a.move([(0, 36, 213), (14, 36, 213), (24, 36, 299), (48, 36, 299), (56, 36, 385), (64, 36, 471), (100, 36, 471)])
a.add(a.group('<path d="M-12 -10L4 0L-12 10z" fill="#17A8D4"/>', mv, a.show(0, 75), still=0))

# panel de resultado
a.add(card(a, 790, 176, 362, 332, "Valor que queda", None))
a.add(mono(a, 812, 252, "PasswordAuthentication", 16, a.GREY, 600))
at(a, mono(a, 812, 300, "(todavía sin valor)", 17, a.GREY, 500), 0, 25, 0)
at(a, a.box(812, 270, 120, 50, a.OKBG, a.OK, rx=12, sw=2) + mono(a, 872, 303, "no", 24, a.OK, 700, "middle"), 26, 100, 1)
at(a, a.text(812, 360, "Los yes que vienen después", 16, a.TXT, a.SANS, 500) + a.text(812, 384, "no cambian nada.", 16, a.TXT, a.SANS, 500), 52, 100, 1)
at(a, term(a, 806, 400, 332, ["$ sudo sshd -T | grep -i passw", ("passwordauthentication no", T_OK)], size=15, lh=26), 76, 100, 1)

caption(a, 600, [(0, 25, "El Include está arriba: los snippets se leen antes que el resto del archivo.", None),
                 (25, 50, "Por eso tu cambio va en un archivo .d con número bajo.", a.OK),
                 (50, 75, "En SSH, repetir una opción más abajo no la cambia: vale la primera.", a.AMB),
                 (75, 100, "sshd -T imprime la configuración efectiva: la prueba de qué quedó.", a.OK)], still=3)
write(a, "4-t1.svg", "En SSH gana el primer valor que se lee",
      "Animación en cuatro tiempos. A la izquierda, cuatro bloques en el orden en que sshd los lee: la primera línea de /etc/ssh/sshd_config con el Include de sshd_config.d, el snippet 10-ies.conf con PasswordAuthentication no, el snippet 50-cloud-init.conf con PasswordAuthentication yes, y el resto del archivo principal con PasswordAuthentication yes. "
      "1: un cursor marca la línea del Include. 2: el cursor baja a 10-ies.conf, que se marca en verde, y el panel de la derecha fija el valor no. "
      "3: los dos bloques que dicen yes se apagan con la etiqueta ignorado. 4: el comando sshd -T con grep muestra passwordauthentication no. El cuadro fijo muestra el resultado final.")
