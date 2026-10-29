#!/usr/bin/env python3
"""Lección 15 (Tonos y corte) · Resumen, "Cómo se ve en la red": las tres señales con que una línea puede avisar que el
otro colgó y el detector de la UCM para cada una, más el Ring Timeout de la entrante que no se atendió (la teoría
anima solo el tono). Fuentes: la lección (tono de ocupado con Busy Tone y Busy Tone Count; Enable Polarity Reversal con
Polarity on Answer Delay de 600 ms; Current Disconnect Threshold cada 200 ms; Ring Timeout 8000 ms; Antel no publica
cuál usa: PSTN Detection), ITU E.180 (ocupado de Uruguay 425 Hz, 0,5 s y 0,5 s)."""
from _anim_gs_red import R

g = R(T=28, fix=12, kicker="GRANDSTREAM · TONOS Y CORTE · CÓMO SE VE EN LA RED",
      title="El otro colgó: tres formas de avisarlo por el par")
g.steps([
    "Tono: la línea manda ocupado de 425 Hz; la UCM cuenta los tonos y cuelga el FXO.",
    "Polaridad: la línea invierte la tensión; con Polarity Reversal activo, la UCM corta.",
    "Corriente: la tensión cae un instante; Current Disconnect lo ve y corta.",
    "Sin atender: si pasan 8000 ms sin timbre (Ring Timeout), la entrante se da por cortada.",
])

# esquema arriba
Y, H = 184, 80
g.add(g.dev(48, Y, 230, H, "Antel", "colgó el otro", icon="antel", dark=True))
PAR = "#3B4D61"
g.add(f'<line x1="278" y1="{Y + 40}" x2="548" y2="{Y + 40}" stroke="{PAR}" stroke-width="8" stroke-linecap="round"/>'
      f'<line x1="278" y1="{Y + 40}" x2="548" y2="{Y + 40}" stroke="#F7FAFD" stroke-width="2"/>')
g.add(g.dev(548, Y, 212, H, "UCM", "FXO1 en llamada", icon="ucm", dark=True))

# señal en el par
SX, SY, SW, SH = 48, 300, 712, 220
g.add(g.box(SX, SY, SW, SH, "#03213C", None, rx=14))
g.add(g.text(SX + 20, SY + 30, "lo que llega por el par", 14, g.SKY, g.MONO))
BASE = SY + 128
g.add(f'<line x1="{SX + 20}" y1="{BASE}" x2="{SX + SW - 20}" y2="{BASE}" stroke="#2A4B6A" stroke-width="1.5" stroke-dasharray="4 6"/>')
# marca del corte
CUT = SX + 150
g.appear(f'<line x1="{CUT}" y1="{SY + 44}" x2="{CUT}" y2="{SY + SH - 16}" stroke="#FF9C86" stroke-width="2" stroke-dasharray="5 5"/>'
         + g.text(CUT - 8, SY + 58, "corte", 13, "#FF9C86", g.MONO, 600, "end"), 0, 75)
# 1 · ráfagas de tono
s1 = f'<path d="M{SX + 20} {BASE} H{CUT}" stroke="{g.MINT}" stroke-width="3" fill="none"/>'
x = CUT + 14
for k in range(4):
    s1 += f'<rect x="{x}" y="{BASE - 36}" width="56" height="72" rx="4" fill="{g.GOLD}" opacity=".85"/>'
    s1 += g.text(x + 28, BASE - 46, str(k + 1), 15, g.GOLD, g.MONO, 600, "middle")
    x += 112
s1 += g.text(SX + SW - 20, SY + 30, "425 Hz · 0,5 s y 0,5 s", 14, g.GOLD, g.MONO, 600, "end")
g.appear(s1, 0, 25)
# 2 · inversión
s2 = (f'<path d="M{SX + 20} {BASE - 50} H{CUT} V{BASE + 50} H{SX + SW - 20}" stroke="{g.MINT}" stroke-width="3" fill="none"/>'
      + g.text(SX + 30, BASE - 60, "+", 20, g.MINT, g.MONO, 600) + g.text(CUT + 14, BASE + 76, "−  polaridad invertida", 16, g.MINT, g.MONO, 600))
g.appear(s2, 25, 50)
# 3 · caída breve
s3 = (f'<path d="M{SX + 20} {BASE - 50} H{CUT} V{BASE} H{CUT + 90} V{BASE - 50} H{SX + SW - 20}" stroke="{g.MINT}" stroke-width="3" fill="none"/>'
      + g.text(CUT + 100, BASE + 26, "cae un instante", 16, g.MINT, g.MONO, 600))
g.appear(s3, 50, 75)
# 4 · timbre que no vuelve
s4 = ""
x = SX + 30
for k in range(2):
    s4 += "".join(f'<line x1="{x + i * 6}" y1="{BASE - 40}" x2="{x + i * 6 + 3}" y2="{BASE + 40}" stroke="{g.GOLD}" stroke-width="2"/>' for i in range(10))
    x += 140
s4 += f'<path d="M{x} {BASE} H{SX + SW - 20}" stroke="{g.MINT}" stroke-width="3"/>'
s4 += g.text(x + 10, BASE - 16, "sin timbre: 8000 ms", 16, g.MINT, g.MONO, 600)
s4 += g.text(SX + SW - 20, SY + 30, "timbre que no vuelve", 14, g.GOLD, g.MONO, 600, "end")
g.appear(s4, 75, 100)

# detectores
DX, DY, DW = 788, 184, 364
g.add(g.box(DX, DY, DW, 336, g.WHITE, g.LINE, rx=16))
g.add(g.text(DX + 20, DY + 32, "Detectores de la troncal", 17, g.INK, g.SANS, 600))
rows = [("Busy Detection", "Busy Tone Count: tonos", "antes de colgar"),
        ("Enable Polarity Reversal", "ignora 600 ms después", "de atender"),
        ("Current Disconnect", "mira cada 200 ms", "si la tensión cayó"),
        ("Ring Timeout", "8000 ms sin timbre", "en una entrante")]
for k, (n, a, b) in enumerate(rows):
    y = DY + 52 + k * 70
    g.add(g.box(DX + 14, y, DW - 28, 62, g.SLATE, None, rx=10))
    g.add(g.text(DX + 30, y + 24, n, 15, g.INK, g.MONO, 600) + g.text(DX + 30, y + 46, f"{a} {b}", 14, g.TXT, g.SANS))
    g.appear(g.box(DX + 14, y, DW - 28, 62, "none", g.OK, rx=10, sw=3), k * 25 + 4, (k + 1) * 25)

g.appear(g.pillc(660, Y + H + 14, "cuelga el FXO1", g.OK, g.OKBG, 13, 26), 10, 25)
g.appear(g.pillc(660, Y + H + 14, "cuelga el FXO1", g.OK, g.OKBG, 13, 26), 32, 50)
g.appear(g.pillc(660, Y + H + 14, "cuelga el FXO1", g.OK, g.OKBG, 13, 26), 57, 75)
g.appear(g.pillc(660, Y + H + 14, "da por cortada", g.OK, g.OKBG, 13, 26), 86, 100)

g.add(g.note(48, 542, 1104, None, ["Antel no publica cuál usa cada línea: PSTN Detection lo mide con una llamada real. Si el detector no reconoce la señal, la línea queda tomada."], "amb"))

g.done(15, "r1", "El otro colgó: tres formas de avisarlo por el par",
       "Animación en cuatro tiempos con Antel, la otra punta que colgó, el par y el FXO1 de la UCM en llamada; abajo, lo que llega por el par después del corte, y a la derecha los detectores de la troncal. "
       "1: tono: la línea manda ocupado de 425 Hz con 0,5 segundos de tono y 0,5 de silencio; Busy Detection cuenta los tonos que dice Busy Tone Count y la UCM cuelga el FXO1. "
       "2: polaridad: la línea invierte la tensión; con Enable Polarity Reversal la UCM lo toma como corte, salvo en los primeros 600 ms después de atender. "
       "3: corriente: la tensión cae un instante; Current Disconnect, que mira cada 200 ms, lo detecta y corta. "
       "4: en una entrante sin atender, si pasan 8000 ms sin timbre, Ring Timeout la da por cortada. "
       "Antel no publica cuál usa cada línea: PSTN Detection lo mide con una llamada real; si el detector no reconoce la señal, la línea queda tomada.",
       [12, 36, 62, 90])
