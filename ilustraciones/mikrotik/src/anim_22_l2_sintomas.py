#!/usr/bin/env python3
"""Lección 22 · IPsec entre marcas · Laboratorio paso 6: qué significa cada síntoma del log, visto en el cable (IKEv2).
Sin respuesta (time up), respuesta NO_PROPOSAL_CHOSEN (parámetros distintos) y el intercambio sano IKE_SA_INIT + IKE_AUTH.
"""
from _anim_mk_32_39 import *

a = Anim(T=27, kicker="MIKROTIK · IPSEC ENTRE MARCAS · PASO 6", title="El log dice si no se hablan o si no se entienden")
a.steps([
    "A manda IKE_SA_INIT por UDP 500 y nadie contesta. Reintenta: \"time up\".",
    "B contesta NO_PROPOSAL_CHOSEN: ninguna propuesta coincide (acá, el grupo DH).",
    "Todo coincide: IKE_SA_INIT y IKE_AUTH van y vuelven; IKE_AUTH crea las primeras SA.",
    "time up: comunicación. No proposal: comparar la tabla con el log, local contra remoto.",
], still=2, size=17)

Y0, Y1 = 176, 468
a.add(router(a, 48, Y0, 220, 92, "Sitio A", "203.0.113.10"))
a.add(router(a, 932, Y0, 220, 92, "Sitio B", "198.51.100.20"))
a.add(a.text(158, Y0 + 122, "DH 14 (modp2048)", 15, a.INK, a.MONO, 600, "middle"))
a.add(during(a, a.text(1042, Y0 + 122, "DH 2 (modp1024)", 15, a.BAD, a.MONO, 600, "middle"), 25, 50))
a.add(during(a, a.text(1042, Y0 + 122, "DH 14 (modp2048)", 15, a.INK, a.MONO, 600, "middle"), 0, 25, still=0))
a.add(during(a, a.text(1042, Y0 + 122, "DH 14 (modp2048)", 15, a.OK, a.MONO, 600, "middle"), 50, 100, still=1))
for x in (158, 1042):
    a.add(line(x, Y0 + 140, x, Y1, a.LINE, 2.5, "6 6"))
L, R = 168, 1032


def msg(y, x1, x2, label, t, end, col, sub=None, fail=False, still=0):
    tip = x2 - 4 if x2 > x1 else x2 + 4
    stop = x1 + (x2 - x1) * 0.72 if fail else tip
    body = a.arrow(f"M{x1} {y} H{stop}", col, 3, "7 6" if fail else "") + a.text((x1 + x2) / 2, y - 12, label, 15, col, a.MONO, 600, "middle")
    if sub:
        body += a.text((x1 + x2) / 2, y + 24, sub, 15, a.TXT, a.SANS, 400, "middle")
    if fail:
        body += xmark(a, stop + (14 if x2 > x1 else -14), y, 13)
    a.add(during(a, body, t + 2, end, still=still))
    a.add(travel(a, dot(a, col, 8), [(x1, y), (stop, y)], t, t + 2.5, hold=0, fade=0.3))


# caso 1: sin respuesta
msg(330, L, R, "IKE_SA_INIT · UDP 500", 1, 25, a.BAD, fail=True)
msg(390, L, R, "IKE_SA_INIT · otra vez", 8, 25, a.BAD, fail=True)
msg(450, L, R, "IKE_SA_INIT · otra vez", 15, 25, a.BAD, fail=True)
# caso 2: no proposal
msg(330, L, R, "IKE_SA_INIT", 27, 50, a.BLUE, sub="propone AES-256 · SHA-256 · DH 14")
msg(420, R, L, "NO_PROPOSAL_CHOSEN", 33, 50, a.BAD, sub="B solo acepta DH 2")
# caso 3: sano
msg(318, L, R, "IKE_SA_INIT", 52, 100, a.BLUE, still=1)
msg(358, R, L, "IKE_SA_INIT · acepta la propuesta", 56, 100, a.BLUE, still=1)
msg(408, L, R, "IKE_AUTH · se autentica", 61, 100, a.OK, still=1)
msg(448, R, L, "IKE_AUTH · primeras SA", 65, 100, a.OK, still=1)
a.add(during(a, a.pill(600, 208, "active-peers: established · installed-sa: 2", a.OK, a.OKBG, 15, 30, "middle"), 69, 100, still=1))

# log
LY = 492
a.add(a.box(48, LY, 1104, 104, a.INK, rx=14))
a.add(a.text(66, LY + 30, '/log/print where topics~"ipsec"', 15, a.WHITE, a.MONO))
LOGS = [
    (0, 25, "phase1 negotiation failed due to time up", ROSE, "→ UDP 500/4500, IP del peer, NAT en el medio", 0, a.MONO),
    (25, 50, "no suitable proposal / NO-PROPOSAL-CHOSEN", ROSE, "→ parámetros distintos: comparar la tabla", 0, a.MONO),
    (50, 75, "Sin errores de negociación: fase 1 y fase 2 arriba.", MINT, "→ si igual no pasa tráfico: bypass de NAT y FastTrack", 1, a.SANS),
    (75, 100, "time up = no se hablan · no proposal = no se entienden", GOLD, "→ el log muestra los valores de cada lado (local:remoto)", 0, a.SANS),
]
for t0, t1, l1, c1, l2, st, fam in LOGS:
    a.add(during(a, a.text(66, LY + 62, l1, 16, c1, fam, 600) + a.text(66, LY + 88, l2, 15, SOFTW, a.SANS, 600), t0, t1, still=st))
a.add(a.text(48, 636, "Fase 1 de la tabla: IKEv2 · AES-256 · SHA-256 · DH 14 · lifetime 1d. Tiene que ser igual en las dos puntas.", 16, a.TXT, a.SANS, 600))

write(a, 22, "l2", "El log dice si no se hablan o si no se entienden",
      "Animación en cuatro tiempos entre el sitio A (203.0.113.10) y el sitio B (198.51.100.20) con IKEv2, y abajo el log con topics ipsec. "
      "1: A manda IKE_SA_INIT por UDP 500 y nadie contesta; reintenta dos veces más. El log dice phase1 negotiation failed due to time up: es un problema de comunicación (UDP 500 o 4500 bloqueado, IP del peer equivocada, NAT en el medio). "
      "2: B contesta, pero con NO_PROPOSAL_CHOSEN: A propone AES-256, SHA-256 y DH 14 y B solo acepta DH 2. El log dice no suitable proposal o NO-PROPOSAL-CHOSEN: hay que comparar la tabla de parámetros. "
      "3: con todo igual, IKE_SA_INIT va y vuelve con la propuesta aceptada e IKE_AUTH autentica y crea las primeras SA; active-peers queda established e installed-sa muestra dos SA. "
      "4: resumen: time up significa que no se hablan; no proposal, que se hablan pero no se entienden.",
      [5, 18, 32, 45, 58, 72, 88])
