import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _fxo import *

X0, SEC = 330, 130     # inicio del eje y píxeles por segundo (6 s en 780 px)


def cadencia(y, pat, color, total=6.0, h=30):
    """Barras de tono encendido sobre una línea de tiempo. pat: lista (on, off) en segundos que se repite; off=0 es continuo."""
    out = [f'<path d="M{X0} {y + h / 2}H{X0 + total * SEC}" stroke="{LINE2}" stroke-width="2"/>']
    t = 0.0
    while t < total - 1e-6:
        for on, off in pat:
            if t >= total:
                break
            w = min(on, total - t) if off else total - t
            out.append(f'<rect x="{X0 + t * SEC:.1f}" y="{y}" width="{w * SEC:.1f}" height="{h}" rx="4" fill="{color}"/>')
            t += on + off if off else total
    return "".join(out)


# ---------------------------------------------------------------- 15.svg: tonos de Uruguay
c = Canvas(K(), "En Uruguay todo suena a 425 Hz: cambia la cadencia")
filas = [("Invitación a marcar", "continuo", [(6, 0)], BLUE),
         ("Llamada", "1 s sí, 4 s no", [(1.0, 4.0)], OK),
         ("Ocupado", "0,5 s sí, 0,5 s no", [(0.5, 0.5)], WARN),
         ("Congestión", "0,25 s sí, 0,25 s no", [(0.25, 0.25)], ALERT)]
c.add(text(48, 150, "Tono · 425 Hz", 16, 600, INK3, FB))
for s in range(7):
    c.add(text(X0 + s * SEC, 150, f"{s} s", 15, 500, INK3, FM, anchor="middle"))
for i, (n, cad, pat, col) in enumerate(filas):
    y = 176 + i * 74
    c.add(text(48, y + 14, n, 18, 600, INK, FB))
    c.add(text(48, y + 38, cad, 15, 500, INK3, FM))
    c.add(cadencia(y, pat, col))
c.add(Note(48, 474, 520, "Lista de tonos nacionales de la UIT (Rec. E.180, situación al 1 de mayo de 2010). Verificalos en tu línea con PSTN Detection.", kind="info", size=16))
c.add(Note(612, 474, 540, "La UCM viene en Estados Unidos: ocupado de 480 y 620 Hz. Con eso no reconoce el ocupado uruguayo y la línea puede quedar tomada.", kind="alert", size=16))
save(c, "15.svg")

# ---------------------------------------------------------------- 15-paso1: Tone Settings en Custom
c = Canvas(K(1), "Tone Settings: Custom con los tonos de Uruguay")
c.add(Window(48, 132, 640, 330, "UCM · web", path="Analog Trunks > Antel_Linea1 > Tone Settings",
             rows=[("Busy Detection", "Yes"), ("Busy Tone Count", "4"), ("Tone Country", "Custom"),
                   ("Busy Tone", "f1=425@-50,c=500/500"), ("Congestion Tone", "f1=425@-50,c=250/250")], hl=3))
c.add(Step(48, 132, 1))
c.add(panel(730, 132, 422, 200, "Cómo se lee", "info"))
lst, _ = bullet_list(750, 196, ["f1=425: frecuencia en Hz", "@-50: nivel, el mismo del valor de fábrica", "c=500/500: ms encendido y apagado"], 392, size=16, gap=8)
c.add(lst)
c.add(Note(730, 352, 422, "Si Uruguay aparece en Tone Country, usalo. Si no, Custom con estos valores.", kind="ok", size=16))
c.add(Note(48, 494, 1104, "Busy Tone Count: el manual sugiere 4, 6 u 8 para evitar cortes al azar; más alto corta más tarde, y muy alto puede no cortar nunca.", kind="warn", size=16))
save(c, "15-paso1.svg")

# ---------------------------------------------------------------- 15-paso2: PSTN Detection
c = Canvas(K(2), "PSTN Detection: una llamada real de un minuto")
c.add(panel(48, 132, 540, 330, "Con una línea: Semi-auto Detect", "info", title_size=18))
u1 = dev(76, 196, "UCM · FXO1", "Source Channel", icon="central", w=230, h=76, dark=True)
c.add(u1)
c.add(dev(330, 196, "Tu celular", "Destination", icon="phone", w=236, h=76))
c.add(Arrow((306, 234), (330, 234), kind="flow"))
lst, _ = bullet_list(76, 316, ["Destination Number: tu celular.", "La UCM llama a tu celular.", "La web te avisa: atendé.", "Después te avisa: cortá.", "Mide ocupado, polaridad y corte."], 480, size=16, gap=6)
c.add(lst)
c.add(panel(612, 132, 540, 330, "Con dos líneas: Auto Detect", "ok", title_size=18))
c.add(dev(640, 196, "UCM · FXO1", "Source Channel", icon="central", w=230, h=76, dark=True))
c.add(dev(894, 196, "UCM · FXO2", "Destination", icon="central", w=236, h=76, dark=True))
c.add(Arrow((870, 234), (894, 234), kind="ok"))
lst, _ = bullet_list(640, 316, ["Destination Channel: FXO2.", "Destination Number: el número real de la línea 2.", "La UCM atiende y corta sola.", "Las dos líneas, libres antes de empezar."], 480, size=16, gap=8)
c.add(lst)
c.add(Step(48, 132, 2))
c.add(Note(48, 484, 1104, "El resultado llena Busy Tone, Polarity Reversal y Current Disconnect en la troncal. Activá la polaridad solo si la detección la encontró.", kind="ok", size=16))
c.add(Note(48, 576, 1104, "La línea queda ocupada alrededor de un minuto: hacelo fuera del horario de atención.", kind="warn", size=16))
save(c, "15-paso2.svg")

# ---------------------------------------------------------------- 15-paso5: medir el tono grabado
c = Canvas(K(5), "Si no corta: grabá la línea y medí el tono")
c.add(codebox(48, 132, 520, [("Maintenance > Signaling Troubleshooting", "#7FD6F2"), "Analog Record Trace · Puerto: FXO1", "Start · llamada · cortá del otro lado", "esperá 10 s · Stop · Download"], size=16, lh=30, title="EN LA UCM")[0])
c.add(codebox(612, 132, 540, [("Audacity > File > Import > Raw Data", "#7FD6F2"), "Signed 16-bit PCM · 1 canal (Mono)", "Sample rate: 8000 Hz", "Analyze > Plot Spectrum: frecuencia"], size=16, lh=30, title="EN LA NOTEBOOK")[0])
c.add(Step(48, 132, 5))
# onda: voz, corte, tono 500/500
c.add(text(48, 330, "Lo que vas a ver en el archivo después de cortar desde el celular:", 17, 600, INK, FB))
wy, wx = 430, 60
import math
pts = []
for i in range(0, 300):
    x = wx + i
    a = 34 * abs(math.sin(i * 0.37)) * (0.5 + 0.5 * abs(math.sin(i * 0.05)))
    pts.append((x, a))
d = "".join(f"M{x:.1f} {wy - a:.1f}V{wy + a:.1f}" for x, a in pts[::2])
c.add(f'<path d="{d}" stroke="{INK3}" stroke-width="1.6"/>')
c.add(text(wx + 150, wy + 66, "conversación", 15, 500, INK3, FB, anchor="middle"))
x = wx + 320
c.add(f'<path d="M{x - 10} {wy - 50}V{wy + 50}" stroke="{ALERT}" stroke-width="2" stroke-dasharray="5 4"/>')
c.add(text(x - 4, wy - 58, "corte del otro lado", 15, 600, ALERT, FB, anchor="middle"))
for k in range(5):
    bx = x + 20 + k * 140
    tone = "".join(f"M{bx + j * 3.5:.1f} {wy - 28}V{wy + 28}" for j in range(21))
    c.add(f'<path d="{tone}" stroke="{WARN}" stroke-width="2"/>')
c.add(f'<path d="M{x + 20} {wy + 44}H{x + 90}" stroke="{INK}" stroke-width="2.5"/><path d="M{x + 90} {wy + 44}H{x + 160}" stroke="{INK3}" stroke-width="2" stroke-dasharray="4 4"/>')
c.add(text(x + 55, wy + 68, "500 ms", 15, 600, INK, FM, anchor="middle"))
c.add(text(x + 125, wy + 68, "500 ms", 15, 600, INK3, FM, anchor="middle"))
c.add(text(x + 380, wy + 68, "tono 425 Hz · silencio · tono · silencio", 15, 500, WARN, FB, anchor="middle"))
c.add(Note(48, 528, 1104, "Tono y silencio de 500 ms a 425 Hz es el ocupado de la lista UIT. Si medís otra cosa, cargá lo que mediste en Custom: c=encendido/apagado en ms.", kind="info", size=16))
save(c, "15-paso5.svg")
