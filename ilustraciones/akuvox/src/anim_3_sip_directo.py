#!/usr/bin/env python3
"""Lección 3 · teoría: la llamada SIP directa mensaje por mensaje (INVITE, 180, 200 OK, ACK, RTP, DTMF)."""
from _anim_akuvox import Anim, A, draw_arrow, token, chip, lane, note, appear, finish

a = Anim(T=24, kicker="AKUVOX · LLAMADA DIRECTA", title="Una llamada directa, mensaje por mensaje")
a.steps([
    "El portero manda INVITE al 5060 del monitor, con su oferta SDP.",
    "El monitor avisa que está sonando: 180 Ringing.",
    "El residente atiende: 200 OK con los codecs y puertos del monitor.",
    "El portero confirma con ACK. Audio y video van por RTP, directo.",
    "La tecla de apertura viaja como DTMF y el portero dispara el relé.",
], still=3)

XP, XM = 200, 700
lane(a, XP, 176, 650, "Portero", "192.168.88.21")
lane(a, XM, 176, 650, "Monitor", "192.168.88.31")


def label(y, s, color, t0, size=16):
    appear(a, a.text((XP + XM) / 2, y - 12, s, size, color, A.MONO, 600, "middle"), t0, 100, still=1)


# 1 INVITE
label(282, "INVITE sip:192.168.88.31:5060", A.BLUE, 8.5)
draw_arrow(a, [(XP, 282), (XM, 282)], 3, 9)
token(a, [(XP, 282), (XM, 282)], 3, 9, chip(a, "INVITE + SDP"))
# 2 180
label(336, "180 Ringing", A.GREY, 26.5)
draw_arrow(a, [(XM, 336), (XP, 336)], 22, 27, A.GREY)
# 3 200 OK
label(390, "200 OK + SDP del monitor", A.OK, 47.5)
draw_arrow(a, [(XM, 390), (XP, 390)], 42, 48, A.OK)
token(a, [(XM, 390), (XP, 390)], 42, 48, chip(a, "200 OK", bg=A.OK))
# 4 ACK + RTP
label(444, "ACK", A.BLUE, 65.5)
draw_arrow(a, [(XP, 444), (XM, 444)], 62, 66)
appear(a, a.box(XP, 476, XM - XP, 44, "#E4F5FB", None, rx=8)
       + a.text((XP + XM) / 2, 504, "RTP · UDP · audio y video", 16, A.CYAN, A.MONO, 600, "middle"), 66, 100, still=1)
pk = '<rect x="-14" y="-6" width="28" height="12" rx="4" fill="#17A8D4"/>'
for i in range(8):
    t0 = 67 + i * 4
    token(a, [(XP + 20, 470), (XM - 20, 470)], t0, t0 + 4, pk, hold=t0 + 4.2)
    token(a, [(XM - 20, 527), (XP + 20, 527)], t0 + 2, min(t0 + 6, 99.5), pk, hold=min(t0 + 6.2, 99.8))
# 5 DTMF + relé
label(586, "tecla de apertura · DTMF", A.AMB, 86.5)
draw_arrow(a, [(XM, 586), (XP, 586)], 82, 87, A.AMB)
appear(a, a.pill(XP, 610, "dispara el relé", A.OK, A.OKBG, 15, 30, "middle"), 88, 100, still=1)

# panel lateral: qué lleva cada mensaje
PX, PY, PW = 830, 250, 322
panels = [
    ("Adentro del INVITE", ["SDP: los codecs de audio y", "video que ofrece el portero", "y el puerto donde espera", "recibir el medio."], "info"),
    ("180 Ringing", ["El monitor está sonando.", "Todavía nadie atendió."], "info"),
    ("200 OK + SDP", ["El monitor responde con sus", "propios codecs y puertos.", "Los dos ya saben a dónde", "mandar el medio."], "ok"),
    ("RTP sobre UDP", ["Audio y video van directo", "entre las dos IP. Misma", "subred: ni router ni NAT", "en el medio."], "info"),
    ("Abrir", ["El monitor manda el código", "DTMF dentro de la llamada.", "El portero dispara el relé", "configurado (lección 6)."], "amb"),
]
for i, (t, ls, k) in enumerate(panels):
    s, h = note(a, PX, PY, PW, t, ls, k)
    appear(a, s, i * 20 + 1, (i + 1) * 20, still=1 if i == 3 else 0, fade=0.8)
s, _ = note(a, PX, 470, PW, None, ["Sin central: el botón del portero", "decide a quién llama."], "info", size=15)
a.add(s)

finish(a, "3-t1.svg", "Llamada SIP directa entre portero y monitor",
       "Animación en cinco tiempos sobre dos líneas de vida, portero 192.168.88.21 y monitor 192.168.88.31. "
       "1: el portero manda INVITE a sip:192.168.88.31:5060 con una oferta SDP, los codecs de audio y video y el puerto donde espera el medio. "
       "2: el monitor responde 180 Ringing, está sonando. 3: el residente atiende y el monitor responde 200 OK con su propio SDP. "
       "4: el portero confirma con ACK y el audio y el video viajan por RTP sobre UDP directo entre las dos IP, en los dos sentidos. "
       "5: el monitor manda la tecla de apertura como DTMF dentro de la llamada y el portero dispara el relé.",
       [8, 30, 50, 75, 95])
