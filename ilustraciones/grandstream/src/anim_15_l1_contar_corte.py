#!/usr/bin/env python3
"""Lección 15 (Tonos y corte) · Laboratorio, paso 4: probar el corte y contar cuánto tarda el FXO1 en volver a libre.
Con el ocupado de Uruguay cargado (425 Hz, 500/500) y Busy Tone Count 4, la UCM cuelga unos cuatro segundos después de
que el otro cortó. Fuentes: la lección (Custom f1=425@-50,c=500/500; Busy Tone Count 4; "con Busy Tone Count en 4 y
ocupado de 500/500, la UCM corta unos cuatro segundos después"; si no corta, Analog Record Trace)."""
from _anim_gs_red import R

g = R(T=26, fix=70, kicker="GRANDSTREAM · TONOS Y CORTE · LABORATORIO",
      title="Contá los segundos: del corte al FXO1 libre")
g.steps([
    "Llamás desde el celular a una interna y atendés: el FXO1 está en uso.",
    "Cortás desde el celular: por la línea empieza a llegar ocupado, 0,5 s y 0,5 s.",
    "La UCM cuenta 4 tonos (Busy Tone Count 4) y cuelga: el FXO1 vuelve a libre.",
    "Repetí con una saliente. Si no vuelve a libre, grabá la línea y medí el tono.",
])

Y = 186
g.add(g.dev(48, Y, 236, 84, "Tu celular", "llama a la línea", icon="phone"))
g.add(g.dev(344, Y, 236, 84, "Interna 1001", "atiende", icon="tel"))
DX = 900
g.add(g.box(DX, Y - 4, 252, 92, g.WHITE, g.LINE, rx=14) + g.text(DX + 18, Y + 22, "Dashboard", 14, g.GREY, g.MONO))
g.appear(g.port(DX + 14, Y + 32, "FXO1", "libre", w=224), 0, 4)
g.appear(g.port(DX + 14, Y + 32, "FXO1", "uso", w=224), 4, 66)
g.appear(g.port(DX + 14, Y + 32, "FXO1", "libre", w=224), 66, 100)
g.appear(g.pillc(462, Y + 98, "en llamada", g.OK, g.OKBG, 13, 26), 4, 25)
g.appear(g.pillc(166, Y + 98, "cortaste", g.BAD, g.BADBG, 13, 26), 26, 100)
g.appear(g.pillc(462, Y + 98, "escucha ocupado", g.AMB, g.AMBBG, 13, 26), 28, 66)

# línea de tiempo desde el corte
TX0, TX1, TY = 110, 1110, 420
PS = (TX1 - TX0) / 8  # px por segundo
g.add(g.box(48, 330, 1104, 196, "#03213C", None, rx=14))
g.add(g.text(68, 360, "lo que llega por el FXO1 después del corte", 14, g.SKY, g.MONO))
g.add(f'<line x1="{TX0}" y1="{TY + 40}" x2="{TX1}" y2="{TY + 40}" stroke="#2A4B6A" stroke-width="2"/>')
for s in range(9):
    x = TX0 + s * PS
    g.add(f'<line x1="{x}" y1="{TY + 34}" x2="{x}" y2="{TY + 46}" stroke="#4E6F8E" stroke-width="2"/>' + g.text(x, TY + 68, f"{s} s", 14, g.SKY, g.MONO, 400, "middle"))
# tonos: aparecen en orden
t_cut = 26
for k in range(4):
    x = TX0 + k * PS
    t = t_cut + 4 + k * 8
    g.appear(f'<rect x="{x}" y="{TY - 26}" width="{PS / 2}" height="52" rx="4" fill="{g.GOLD}"/>'
             + g.text(x + PS / 4, TY + 7, str(k + 1), 18, "#03213C", g.MONO, 600, "middle"), t, 100)
g.appear(f'<line x1="{TX0 + 4 * PS}" y1="{TY - 40}" x2="{TX0 + 4 * PS}" y2="{TY + 48}" stroke="{g.MINT}" stroke-width="3"/>'
         + g.text(TX0 + 4 * PS + 10, TY - 30, "≈ 4 s: cuelga el FXO1", 16, g.MINT, g.MONO, 600), 64, 100)
# cabezal
cur = g.keyframes([(0, f"{TX0}px,0px"), (t_cut + 4, f"{TX0}px,0px"), (64, f"{TX0 + 4 * PS}px,0px"), (100, f"{TX0 + 4 * PS}px,0px")], "transform", "translate({})")
g.add(g.group(f'<line x1="0" y1="{TY - 44}" x2="0" y2="{TY + 48}" stroke="#FFFFFF" stroke-width="2"/>', cur, g.show(t_cut + 2, 66, 0.5), still=0))
g.appear(g.text(TX0 + 8, TY - 30, "corte", 15, "#FF9C86", g.MONO, 600), t_cut, 64)

g.add(g.note(48, 546, 540, "Busy Tone Count", ["Más alto corta más tarde: con 4 y", "500/500, unos cuatro segundos."], "info"))
g.appear(g.note(612, 546, 540, "Anotá el tiempo", ["Entrante y saliente. Si queda en uso,", "Analog Record Trace y Audacity."], "ok"), 0, 75)
g.appear(g.note(612, 546, 540, "Si no vuelve a libre", ["La línea manda otra cosa o el tono no", "coincide: grabala y medí tono y silencio."], "amb"), 75, 100)

g.done(15, "l1", "Contá los segundos: del corte al FXO1 libre",
       "Animación en cuatro tiempos con tu celular, la interna 1001 que atiende y el FXO1 en el Dashboard; abajo, una línea de tiempo de 0 a 8 segundos desde el corte con lo que llega por el FXO1. "
       "1: llamás desde el celular a una interna y atendés: el FXO1 está en uso. "
       "2: cortás desde el celular y por la línea empieza a llegar ocupado, medio segundo de tono y medio de silencio; la interna escucha ocupado. "
       "3: la UCM cuenta 4 tonos, lo que dice Busy Tone Count, y cuelga cerca de los 4 segundos: el FXO1 vuelve a libre. "
       "4: se repite con una saliente y se anota el tiempo; si no vuelve a libre, la línea manda otra cosa o el tono no coincide, y se graba con Analog Record Trace para medir tono y silencio en Audacity. "
       "Busy Tone Count más alto corta más tarde.",
       [10, 40, 62, 72, 92])
