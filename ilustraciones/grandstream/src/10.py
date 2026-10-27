import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 10.svg: el orden del diagnóstico
c = Canvas(K(), "Audio de un lado: tres pasos, siempre en este orden")
pasos = [("1", "NAT y puertos", ["External Host", "Local Network Address", "UDP 5060 y 10000-20000"], "info"),
         ("2", "SIP ALG", ["apagado en el router", "reiniciá o limpiá sesiones", "si no se apaga: TLS u otro router"], "info"),
         ("3", "Captura", ["Ethernet Capture en la UCM", "línea c= del SDP", "RTP Streams en Wireshark"], "ok")]
for i, (n_, t, items, kd) in enumerate(pasos):
    x = 48 + i * 376
    c.add(panel(x, 130, 340, 260, None, kd))
    c.add(f'<circle cx="{x + 44}" cy="174" r="22" fill="{BLUE if kd == "info" else OK}"/>')
    c.add(text(x + 44, 181, n_, 20, 700, WHITE, FD, anchor="middle"))
    c.add(text(x + 80, 182, t, 23, 600, INK, FD))
    for k, it in enumerate(items):
        c.add(text(x + 28, 248 + k * 40, it, 16, 500, INK2, FM if k < 2 and i == 0 else FB))
    if i < 2:
        c.add(arrow((x + 344, 260), (x + 372, 260)))
c.add(Note(48, 420, 540, "Llamada que se corta siempre entre los 30 y 35 segundos: casi siempre un ACK que no llega. La central lo espera 64 veces 500 ms (Timer H, 32 s) y corta.", title="El corte de los 32 segundos", kind="warn", size=16))
c.add(Note(612, 420, 540, "El manual lo repite: el audio de un solo lado casi siempre es NAT o puertos SIP y RTP en el firewall. La captura lo confirma antes de tocar nada.", title="Por qué este orden", kind="info", size=16))
c.add(text(48, 620, "No se toca un router sin una captura antes.", 18, 600, INK, FB))
save(c, "10.svg")

# ---------------------------------------------------------------- 10-paso3: leer la línea c= del SDP
c = Canvas(K(3), "La línea c= dice a dónde mandar el audio")
lines = [("v=0", "#7FA6C9"), ("o=- ... IN IP4 ...", "#7FA6C9"), ("c=IN IP4 203.0.113.10", "#7FE0A8"), ("m=audio 10044 RTP/AVP 8 0", "#7FD6F2"), ("a=rtpmap:8 PCMA/8000", "#7FA6C9")]
svg, h = codebox(48, 140, 560, lines, size=17, lh=34, title="SDP DEL INVITE O DEL 200 OK · FILTRO sip || sdp")
c.add(svg)
c.add(arrow((612, 238), (660, 238), kind="ok"))
c.add(text(672, 232, "IP pública: el otro lado", 16, 600, OK, FB))
c.add(text(672, 254, "sabe a dónde devolver el audio", 16, 500, INK2, FB))
c.add(arrow((612, 272), (660, 300), kind="flow"))
c.add(text(672, 298, "puerto RTP 10044, dentro", 16, 600, BLUE, FB))
c.add(text(672, 320, "de 10000 a 20000", 16, 500, INK2, FB))
c.add(Step(48, 140, 3))
c.add(panel(48, 380, 1104, 210, "Si ves esto hacia afuera, ahí está el problema", "alert", title_size=19))
c.add(code(72, 430, 470, "c=IN IP4 192.168.88.20", 18, "#FFB4A3", h=48))
c.add(Generic(580, 418, "Otro extremo", "manda el audio ahí", icon="phone", w=290))
c.add(Cable((874, 460), (990, 460), kind="alert", label="se pierde", label_dy=-16))
c.add(Mark(1010, 460, ok=False))
svg, _ = wrap(72, 520, "IP privada en un mensaje que sale a internet: falta External Host o la reescribió un SIP ALG. El otro lado manda el audio a una dirección que no puede alcanzar y vos no lo escuchás.", 1050, 16, 400, INK2)
c.add(svg)
save(c, "10-paso3.svg")

# ---------------------------------------------------------------- 10-paso4: RTP Streams, el audio real
c = Canvas(K(4), "RTP Streams: ¿hay audio en los dos sentidos?")
c.add(text(48, 150, "Wireshark > Telephony > RTP > RTP Streams · llamada de 20 s", 16, 600, BLUE, FM))
c.add(Table(48, 172, ["Origen", "Destino", "Paquetes"], [["UCM 192.168.88.20:10044", "remoto 198.51.100.7", "≈ 1000"], ["remoto 198.51.100.7", "UCM 192.168.88.20:10044", "0"]], [400, 400, 304], row_h=50, mono_cols=(0, 1, 2), hl_row=1))
c.add(Step(48, 172, 4))
c.add(Mark(1110, 247, ok=True))
c.add(Mark(1110, 297, ok=False))
c.add(panel(48, 360, 540, 200, "Lo que dice la tabla", "info"))
lst, _ = bullet_list(72, 420, ["Desde la central sale audio hacia el remoto.", "Del remoto no llega nada a la central: de este lado nadie lo escucha."], 500, size=16, gap=8)
c.add(lst)
c.add(panel(612, 360, 540, 200, "Qué mirar después", "ok"))
lst, _ = bullet_list(636, 420, ["A qué IP y puerto anunció la central en su c= y m=.", "Si ese puerto está reenviado en el router de la central.", "Si un ALG tocó el SDP en el camino."], 500, size=16, gap=8)
c.add(lst)
c.add(text(48, 604, "Una captura tiene números y audio reales: guardala lo justo y no la compartas fuera del soporte.", 16, 500, WARN, FB))
save(c, "10-paso4.svg")

# ---------------------------------------------------------------- 10-paso5: qué hace un SIP ALG
c = Canvas(K(5), "Un SIP ALG reescribe lo que la central mandó bien")
c.add(Generic(48, 170, "UCM", "manda bien", icon="server", w=230, dark=True))
c.add(code(48, 272, 330, "c=IN IP4 203.0.113.10", 15, "#7FE0A8", h=40))
c.add(arrow((282, 212), (430, 212)))
c.add(Generic(440, 170, "Router con SIP ALG", "reescribe SIP y SDP", icon="shield", w=300, hl=ALERT))
c.add(arrow((744, 212), (890, 212), kind="alert"))
c.add(Generic(900, 170, "Otro extremo", "recibe otra cosa", icon="phone", w=252))
c.add(code(822, 272, 330, "c=IN IP4 192.168.88.20", 15, "#FFB4A3", h=40))
c.add(text(48, 360, "Síntomas típicos:", 18, 600, INK, FB))
lst, _ = bullet_list(48, 394, [("audio de un solo lado", "alert"), ("corte a los 30 y pico segundos (ACK perdido)", "alert"), ("registra pero no entran llamadas", "alert")], 520, size=16, gap=8)
c.add(lst)
c.add(Step(440, 170, 5))
c.add(panel(612, 350, 540, 230, "Si sospechás del ALG", "ok"))
lst, _ = bullet_list(636, 410, [("Apagalo (SIP ALG o SIP Helper).", "ok"), ("Reiniciá el router o limpiá las sesiones.", "ok"), ("Repetí la captura y compará el c= con el anterior.", "ok"), ("Si no se puede apagar: TLS, otro segmento o cambiar el router.", "warn")], 500, size=16, gap=6)
c.add(lst)
c.add(text(48, 600, "Capturá en el propio equipo y compará lo que salió con lo que llegó: así se ve quién reescribió.", 16, 500, INK2, FB))
save(c, "10-paso5.svg")
