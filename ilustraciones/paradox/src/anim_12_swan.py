"""Teoría lección 12: Swan conecta app y módulo; el monitoreo va por otro canal."""
from _apdx import *

a = new(20, "Swan en el medio: qué pasa si vence la suscripción")
a.steps(["El módulo sale a internet y se anota en Swan.",
         "La app pide el sitio a Swan, que la conecta con el módulo.",
         "Vence la suscripción: los servicios de app por Swan se cortan.",
         "El monitoreo, por su canal propio a la receptora, sigue avisando."], still=1)
a.add(card(a, 48, 200, 240, 110, "BlueEye", "app del cliente"))
a.add(card(a, 480, 200, 260, 110, "Swan", "servidor de Paradox"))
a.add(card(a, 912, 200, 240, 110, "Módulo IP", "en la central"))
a.add(card(a, 912, 400, 240, 110, "Central", "abonado 1A01", dark=True))
a.add(card(a, 480, 400, 260, 110, "Receptora", "monitoreo"))
a.add(line(a, "M1032 310V400", a.BLUE, 4))
at(a, a.arrow("M906 240H746", a.BLUE, 4) + a.text(826, 228, "se anota", 14, a.BLUE, a.MONO, 700, "middle"), 0, 50, 1)
at(a, a.arrow("M288 270H474", a.CYAN, 4) + a.arrow("M746 270H906", a.CYAN, 4), 25, 50, 1)
at(a, line(a, "M288 270H474", a.BAD, 4, "6 8") + chip(a, 381, 330, "sin suscripción", "bad", anchor="middle"), 50, 100, 0)
at(a, a.box(480, 200, 260, 110, "none", a.BAD, rx=14, sw=3), 50, 75, 0)
at(a, a.arrow("M906 455H746", a.OK, 4) + chip(a, 826, 520, "Contact ID", "ok", anchor="middle"), 75, 100, 0)
at(a, a.arrow("M906 455H746", a.OK, 3, "4 6"), 0, 75, 1)
caption(a, 600, [(0, 25, "El módulo sondea a Swan cada tanto: el IP150+ cada 15 min, según su ficha.", None),
                 (25, 50, "El sitio Swan tiene días de suscripción y fecha de renovación: anotá quién paga.", None),
                 (50, 75, "Ojo con el IP150M: según su manual, sin Swan pago no hay ninguna comunicación.", a.BAD),
                 (75, 100, "Por eso el monitoreo se programa por un canal independiente de la app.", a.OK)], still=1)
write(a, "12-t1.svg", "Swan en el medio: qué pasa si vence la suscripción",
      "Animación en cuatro tiempos con la app BlueEye, el servidor Swan, el módulo IP, la central y la receptora. 1: el módulo sale a internet y se anota en Swan. "
      "2: la app pide el sitio a Swan, que la conecta con el módulo. 3: vence la suscripción y la conexión de la app se corta. "
      "4: el reporte Contact ID de la central a la receptora sigue por su propio canal. Aviso: con el IP150M, según su manual, sin Swan pago no hay ninguna comunicación.")
