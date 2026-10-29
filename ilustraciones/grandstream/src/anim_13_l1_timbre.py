#!/usr/bin/env python3
"""Lección 13 (Qué trae el par) · Laboratorio, paso 4: llamar a la línea desde un celular con el teléfono de prueba
enchufado. Lo que pasa en el par y lo que escucha quien llama: el timbre de unos 70 V en ráfagas, el tono de llamada
del lado del celular, el número si la línea tiene el servicio y el teléfono pantalla, y el lazo que se cierra al
atender. Fuentes: la lección (timbre alterna de unos 70 V según innovaphone; al descolgar circula corriente y la
tensión cae; identificador si está contratado; no tocar los contactos mientras suena), ITU E.180 (tono de llamada de
Uruguay 425 Hz, 1 s y 4 s)."""
from _anim_gs_red import R

g = R(T=26, fix=62, kicker="GRANDSTREAM · QUÉ TRAE EL PAR · LABORATORIO",
      title="Llamar a la línea: lo que pasa en cada punta")
g.steps([
    "Llamás desde el celular: Antel le manda a la línea el timbre, una alterna en ráfagas.",
    "Mientras suena, del lado del celular se escucha el tono de llamada: 425 Hz, 1 s y 4 s.",
    "Con pantalla y el servicio contratado, el teléfono de prueba muestra el número.",
    "Descolgás: el lazo se cierra, el timbre se corta y la llamada queda armada.",
])

PAR = "#3B4D61"
def par(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PAR}" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#F7FAFD" stroke-width="2" stroke-linecap="round"/>')

Y, H = 200, 96
YL = Y + H / 2
g.add(g.dev(48, Y, 240, H, "Tu celular", "llamando a la línea", icon="phone"))
g.add(g.cloud(318, Y + 14, 120, 68, "red"))
g.add(g.dev(468, Y, 250, H, "Central de Antel", "FXS de la línea", icon="antel", dark=True))
g.add(par(718, YL, 900, YL))
g.add(g.text(809, YL - 16, "par", 15, g.GREY, g.MONO, 400, "middle"))
g.add(g.dev(900, Y, 252, H, "Teléfono de prueba", "en la ficha RJ11", icon="tel"))
g.add(g.wire(288, YL, 318, YL, g.BLUE))
g.add(g.wire(438, YL, 468, YL, g.BLUE))

# ráfagas de timbre en el par
for k in range(3):
    t = 4 + k * 23
    if t > 70:
        break
    g.appear(g.pillc(809, Y + H + 12, "timbre: 70 V alterna", g.BAD, g.BADBG, 13, 26), t, t + 6)
g.appear(g.pillc(1026, Y + H + 12, "suena", g.CYAN, "#E3F4FA", 13, 26), 4, 10)
g.appear(g.pillc(1026, Y + H + 12, "suena", g.CYAN, "#E3F4FA", 13, 26), 27, 33)
g.appear(g.pillc(1026, Y + H + 12, "suena", g.CYAN, "#E3F4FA", 13, 26), 50, 56)
# tono de llamada del lado del celular
for k in range(3):
    t = 27 + k * 6
    g.token([(560, Y - 10), (168, Y - 10)], t, t + 5, g.chip("tono de llamada", bg=g.CYAN, size=13, h=24), hold=t + 5.2)
# pantalla
SX, SY = 900, 360
g.add(g.box(SX, SY, 252, 120, "#03213C", None, rx=14))
g.add(g.text(SX + 18, SY + 30, "pantalla del teléfono", 14, g.SKY, g.MONO))
g.appear(g.text(SX + 18, SY + 74, "llamada entrante", 18, "#D9E9F8", g.MONO, 600), 4, 50)
g.appear(g.text(SX + 18, SY + 74, "09X XXX XXX", 22, g.MINT, g.MONO, 600)
         + g.text(SX + 18, SY + 102, "si hay servicio", 14, g.SKY, g.MONO), 50, 75)
g.appear(g.text(SX + 18, SY + 74, "en llamada", 18, g.MINT, g.MONO, 600), 75, 100)
# lazo
g.appear(g.box(718, YL - 6, 182, 12, g.OK, None, rx=6), 77, 100)
g.appear(g.pillc(809, Y + H + 12, "lazo cerrado", g.OK, g.OKBG, 13, 26), 77, 100)
g.appear(g.pillc(1026, Y + H + 12, "descolgado", g.OK, g.OKBG, 13, 26), 77, 100)

# lo que anota
FX, FY = 48, 360
g.add(g.box(FX, FY, 820, 120, g.WHITE, g.LINE, rx=14))
g.add(g.text(FX + 20, FY + 30, "ficha de la línea", 15, g.GREY, g.MONO))
g.add(g.text(FX + 20, FY + 66, "Timbre:", 17, g.INK, g.MONO, 600) + g.text(FX + 300, FY + 66, "Identificador en display:", 17, g.INK, g.MONO, 600))
g.appear(g.text(FX + 110, FY + 66, "sí", 17, g.OK, g.MONO, 600), 10, 100)
g.appear(g.text(FX + 580, FY + 66, "sí", 17, g.OK, g.MONO, 600), 56, 100)
g.add(g.text(FX + 20, FY + 100, "Sin número en pantalla: puede faltar el servicio o el teléfono no tiene display.", 15, g.TXT, g.SANS))

g.add(g.note(48, 504, 1104, "Cuidado", ["Con la línea sonando hay unos 70 V de alterna en los contactos: no se tocan mientras suena."], "bad"))

g.status(636, [
    (0, 25, "El timbre llega en ráfagas: suena, para, vuelve a sonar.", g.INK),
    (25, 50, "El celular escucha el tono de llamada mientras el teléfono suena.", g.INK),
    (50, 75, "Si acá no aparece el número, la UCM tampoco lo va a ver.", g.AMB),
    (75, 100, "Al atender, la tensión cae al valor de descolgado y el timbre se corta.", g.OK),
])

g.done(13, "l1", "Llamar a la línea: lo que pasa en cada punta",
       "Animación en cuatro tiempos con tu celular, la red, la central de Antel, que hace de FXS y da tensión y timbre, el par y el teléfono de prueba enchufado en la ficha RJ11, con su pantalla y la ficha de la línea. "
       "1: llamás desde el celular y Antel le manda a la línea el timbre, una alterna de unos 70 V en ráfagas: el teléfono suena, para y vuelve a sonar. "
       "2: mientras suena, del lado del celular se escucha el tono de llamada, que en Uruguay es de 425 Hz con 1 segundo de tono y 4 de silencio. "
       "3: si el teléfono tiene pantalla y la línea tiene el servicio de identificación contratado, aparece el número; si acá no aparece, la UCM tampoco lo va a ver. "
       "4: al descolgar, el lazo se cierra, la tensión cae al valor de descolgado, el timbre se corta y la llamada queda armada. "
       "Cuidado: con la línea sonando hay unos 70 V de alterna en los contactos.",
       [8, 32, 62, 90])
