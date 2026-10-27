from _akv import *

# ---------- 6.svg: tres maneras de viajar el código
c = Canvas("Akuvox · Lección 6", "El código 731 puede viajar de tres maneras")
lanes = [("Inband", "dentro del audio", "warn", "se degrada con G.729", "audio"),
         ("RFC 2833", "evento en paquetes RTP", "ok", "la más compatible", "rtp"),
         ("SIP INFO", "mensaje de señalización", "warn", "la central no siempre lo pasa", "sip")]
for i, (ttl, sub, kd, verdict, style) in enumerate(lanes):
    y = 140 + i * 160
    bg, fg = KC[kd]
    c.add(f'<rect x="48" y="{y}" width="1104" height="136" rx="18" fill="{WHITE}" stroke="{fg if kd == "ok" else LINE2}" stroke-width="{2.5 if kd == "ok" else 1.5}"/>')
    c.add(text(72, y + 50, ttl, 22, 600, INK, FD))
    c.add(text(72, y + 78, sub, 15, 500, INK3, FM))
    c.add(Chip(72, y + 114, verdict, kd, mono=False))
    c.add(Generic(380, y + 26, "Monitor", "tecla", icon="laptop", w=170))
    c.add(Generic(930, y + 26, "Portero", "relé A", icon="bell", w=170))
    x1, x2, ym = 556, 924, y + 68
    if style == "audio":
        d = f"M{x1} {ym}" + "".join(f"q 11 {-16 if k % 2 == 0 else 16} 22 0" for k in range(int((x2 - x1) / 22)))
        c.add(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="3"/>')
        c.add(pill(740, ym + 6, "731 mezclado en la voz", WARN, WARN_BG))
    elif style == "rtp":
        for k in range(8):
            px = x1 + 12 + k * 40
            hl = k == 4
            c.add(f'<rect x="{px}" y="{ym - 14}" width="30" height="28" rx="5" fill="{OK if hl else SOFT}" stroke="{OK if hl else LINE2}" stroke-width="1.5"/>')
        c.add(pill(740, ym - 26, "evento 731", OK, OK_BG))
        c.add(Arrow((x2 - 30, ym), (x2, ym), kind="ok"))
    else:
        c.add(f'<path d="M{x1} {ym + 18}H{x2}" stroke="{LINE2}" stroke-width="6"/>')
        c.add(text(740, ym + 40, "audio", 14, 500, INK3, FM, anchor="middle"))
        c.add(Arrow((x1, ym - 12), (x2, ym - 12), kind="logical"))
        c.add(pill(740, ym - 20, "SIP INFO 731", WARN, WARN_BG))
save(c, "6.svg")

# ---------- 6-paso4.svg: mismo tipo y mismo código en las tres puntas
c = Canvas("Akuvox · Lección 6 · Paso 4", "Mismo tipo y mismo código en las tres puntas")
c.add(Window(48, 140, 352, 250, "Portero", rows=[("DTMF Type", "RFC2833"), ("DTMF Mode", "3 dígitos"), ("Relay A", "731")], hl=2))
c.add(text(66, 340, "Account > Advanced > DTMF", 15, 500, BLUE, FM))
c.add(text(66, 364, "Access Control > Relay", 15, 500, BLUE, FM))
c.add(Window(424, 140, 352, 250, "Central (si hay)", rows=[("DTMF ext. 201", "RFC 2833"), ("DTMF ext. 202", "RFC 2833")], hl=None))
c.add(text(442, 364, "menú según la central", 15, 500, INK3, FM))
c.add(Window(800, 140, 352, 250, "Monitor", rows=[("DTMF Type", "RFC2833"), ("Remote Relay", "731"), ("SoftKey", "Remote Relay DTMF")], hl=1))
c.add(text(818, 340, "Account > Advanced > DTMF", 15, 500, BLUE, FM))
c.add(text(818, 364, "Device > Relay", 15, 500, BLUE, FM))
for x in (376, 752, 1128):
    c.add(Mark(x, 140, ok=True))
flow = [("Tecla en el monitor", "en la llamada"), ("731 por RFC 2833", "viaja en el RTP"), ("El portero compara", "código y tipo"), ("Relé A abre", "5 s (lección 4)")]
for i, (a, b) in enumerate(flow):
    x = 48 + i * 282
    kd = "ok" if i == 3 else "info"
    bg, fg = KC[kd]
    c.add(f'<rect x="{x}" y="440" width="250" height="90" rx="14" fill="{bg}" stroke="{fg if kd == "ok" else LINE2}" stroke-width="1.5"/>')
    c.add(text(x + 20, 478, a, 18, 600, INK))
    c.add(text(x + 20, 506, b, 15, 500, INK3, FM))
    if i < 3:
        c.add(Arrow((x + 254, 485), (x + 278, 485)))
c.add(Step(48, 440, 4))
c.add(text(48, 580, "Una punta en SIP INFO y las otras en RFC 2833: atienden, ven a la persona y no abre (paso 5).", 16, 500, WARN))
save(c, "6-paso4.svg")

# ---------- 6-paso6.svg: lista blanca DTMF
c = Canvas("Akuvox · Lección 6 · Paso 6", "La lista blanca decide quién puede marcar 731")
po = c.add(Intercom(520, 150, "Portero", "Only Contacts List"))
a = c.add(Generic(60, 170, "Monitor 202", "está en contactos", icon="laptop", w=280, hl=OK))
b = c.add(Generic(60, 390, "Número desconocido", "no está en contactos", icon="phone", w=280, hl=ALERT))
c.add(Arrow(a.right(), (510, 230), kind="ok", label="731", label_dy=-12))
c.add(Arrow(b.right(), (510, 340), kind="alert", label="731", label_dy=-12))
c.add(Chip(760, 230, "abre el relé A", "ok", mono=False))
c.add(Chip(760, 340, "código ignorado", "alert", mono=False))
c.add(Mark(735, 222, ok=True))
c.add(Mark(735, 332, ok=False))
c.add(Window(760, 400, 392, 130, "Web del portero", path="Access Control > Relay", rows=[("Open Relay Via DTMF", "Only Contacts List")], hl=0))
c.add(Step(60, 170, 6))
save(c, "6-paso6.svg")
