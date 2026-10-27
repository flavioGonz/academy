#!/usr/bin/env python3
"""Lección 42 · Teoría · Cuenta activa o vencida: qué deja de sonar.
Sale de teoria_md (Cómo funciona): vinculado a la nube el tipo de conexión pasa a Cloud y la cuenta SIP 1
queda para SmartPlus; sale por puertos salientes (443, 5070, 8501, 9999, RTP); cada cuenta de app tiene estado
y vencimiento; si no está activa la app no llama y portero y monitor siguen por SIP en la LAN; los servicios
se activan desde Subscription (distribuidor o instalador con permiso)."""
from _anim_akuvox_29_42 import new, out, box, travel, when

a = new(24, "LICENCIAS · SMARTPLUS", "Cuenta activa o vencida: qué deja de sonar")
a.steps([
    "Vinculado: la cuenta SIP 1 va a SmartPlus por puertos salientes.",
    "Llega una visita: suena el monitor por la LAN y la app por la nube.",
    "La cuenta de la app vence: la app no llama. Portero y monitor siguen.",
    "Se renueva en Subscription: la app vuelve a sonar.",
], still=2)

# enlaces
a.add(f'<path d="M163 400 V222 H470" fill="none" stroke="{a.BLUE}" stroke-width="3"/>')
a.add(a.text(318, 210, "443 · 5070 · 8501 · 9999 · RTP", 15, a.BLUE, a.MONO, 600, "middle"))
a.add(a.text(180, 252, "solo salientes", 15, a.GREY, a.MONO, 600))
a.add(f'<path d="M730 222 H900" fill="none" stroke="{a.BLUE}" stroke-width="3" stroke-dasharray="7 6"/>')
a.add(f'<path d="M278 442 H900" fill="none" stroke="{a.OK}" stroke-width="4"/>')
a.add(a.text(589, 476, "SIP en la LAN · sin licencia", 15, a.OK, a.MONO, 600, "middle"))

a.add(box(470, 180, 260, 84, "Nube", "SmartPlus", "cloud", dark=True))
a.add(box(900, 180, 252, 84, "App", "residente", "phone"))
a.add(box(48, 400, 230, 84, "Portero", "SIP 1 → nube", "bell"))
a.add(box(900, 400, 252, 84, "Monitor", "en el apartamento", "laptop"))

# tarjeta de la cuenta
a.add(a.box(470, 292, 260, 110, a.WHITE, a.LINE, rx=16))
a.add(a.text(490, 322, "Cuenta de la app", 17, a.INK, a.SANS, 600))
a.add(a.text(490, 346, "estado y vencimiento", 15, a.GREY, a.MONO))
when(a, a.pill(490, 360, "activa", a.OK, a.OKBG, 15, 28), 0, 50, still=0)
when(a, a.pill(490, 360, "vencida", a.BAD, a.BADBG, 15, 28), 51, 76, still=1)
when(a, a.pill(490, 360, "renovada · activa", a.OK, a.OKBG, 15, 28), 77, 100)
when(a, f'<rect x="468" y="290" width="264" height="114" rx="17" fill="none" stroke="{a.BAD}" stroke-width="3"/>', 51, 76, still=1)

# t1: registro saliente
travel(a, (163, 392), (163, 230), 3, 9, None, bg=a.CYAN, dot=9, hold=0.2)
travel(a, (170, 222), (462, 222), 9, 15, "registro", a.WHITE, a.BLUE, hold=6)


def visita(t, app_ok):
    travel(a, (290, 442), (890, 442), t, t + 6, "INVITE", a.WHITE, a.OK, hold=1)
    when(a, a.pill(1026, 492, "suena", a.OK, a.OKBG, 15, 28, "middle"), t + 6, t + 18, still=1 if not app_ok else 0)
    travel(a, (163, 392), (163, 230), t, t + 3, None, bg=a.CYAN, dot=9, hold=0.2)
    travel(a, (170, 222), (462, 222), t + 3, t + 6, None, bg=a.CYAN, dot=9, hold=0.2)
    if app_ok:
        travel(a, (738, 222), (892, 222), t + 7, t + 11, None, bg=a.CYAN, dot=9, hold=0.2)
        when(a, a.pill(1026, 272, "suena", a.OK, a.OKBG, 15, 28, "middle"), t + 11, t + 21)
    else:
        when(a, f'<circle cx="815" cy="222" r="16" fill="{a.BADBG}" stroke="{a.BAD}" stroke-width="2"/>'
             f'<path d="M809 216 l12 12 M821 216 l-12 12" stroke="{a.BAD}" stroke-width="3" stroke-linecap="round"/>'
             + a.pill(1026, 272, "no llama", a.BAD, a.BADBG, 15, 28, "middle"), t + 7, t + 21, still=1)


visita(28, True)
visita(53, False)
visita(78, True)

a.add(a.text(48, 560, "Sin licencia en la LAN: llamada al monitor, relés, RTSP al NVR y apertura por HTTP.", 18, a.INK, a.SANS, 600))
a.add(a.text(48, 590, "La nube se cobra por servicio, con estado y vencimiento: app maestra, familiares extra,", 17, a.TXT, a.SANS, 600))
a.add(a.text(48, 616, "desvío a teléfono, video en la nube. Los activa el distribuidor o el instalador con permiso.", 17, a.TXT, a.SANS, 600))

out(a, 42, 1, "Cuenta activa o vencida: qué deja de sonar",
    "Animación con un portero, un monitor en el apartamento, la nube SmartPlus, la app del residente y una tarjeta con el estado de la cuenta de la app. "
    "Tiempo 1: el portero vinculado usa la cuenta SIP 1 para SmartPlus y se conecta hacia la nube por puertos salientes, 443, 5070, 8501, 9999 y RTP. "
    "Tiempo 2: llega una visita; el portero llama al monitor por SIP en la LAN y la nube hace sonar la app. "
    "Tiempo 3: la cuenta de la app está vencida; el monitor suena igual, pero la nube no llama a la app. "
    "Tiempo 4: la cuenta se renueva en Subscription y la app vuelve a sonar. "
    "Abajo: en la LAN no hace falta licencia; la nube se cobra por servicio, con estado y vencimiento.",
    [8, 40, 66, 92])
