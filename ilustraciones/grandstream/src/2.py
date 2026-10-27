import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *

# ---------------------------------------------------------------- 2.svg: cinco ajustes, cinco problemas que evitan
c = Canvas(K(), "Cada ajuste de la extensión evita un problema")
rows = [("Contraseña SIP", "aleatoria"), ("Concurrent Registrations", "1 o 2"), ("NAT", "activado"), ("Direct Media", "desactivado"), ("DTMF Mode", "RFC4733")]
c.add(Window(48, 130, 560, 290, "UCM · extensión 1001", rows=rows, path="Extension/Trunk > Extensions"))
evita = [("Nadie adivina la cuenta para llamar gratis", "ok"),
         ("Menos equipos usando la misma cuenta (fábrica: 3)", "ok"),
         ("El teléfono detrás de un router recibe respuesta", "ok"),
         ("El audio pasa por la central y cruza el NAT", "ok"),
         ("Buzón e IVR reconocen las teclas", "ok")]
for i, (s, kd) in enumerate(evita):
    y = 212 + i * 38 + 18
    c.add(arrow((614, y - 5), (652, y - 5)))
    c.add(text(664, y, s, 17, 500, INK, FB))
c.add(text(664, 170, "QUÉ EVITA", 14, 600, INK3, FM, ls=1.5))
c.add(Note(48, 452, 540, "Ninguno de estos valores se ve desde afuera: la extensión anda igual. La diferencia aparece el día que alguien prueba contraseñas o el audio se corta de un lado.", title="Por qué importa", kind="info", size=16))
c.add(Note(612, 452, 540, "La mayoría de los audios cortados y de los fraudes empiezan en una extensión floja, no en el troncal.", title="Dónde empiezan los problemas", kind="warn", size=16))
save(c, "2.svg")

# ---------------------------------------------------------------- 2-paso1: la contraseña la genera la central
c = Canvas(K(1), "La contraseña SIP la genera la central")
c.add(Window(48, 132, 520, 160, "UCM · web", path="PBX Settings > General Settings", rows=[("Enable Random Password", "Sí")], hl=0))
c.add(Step(48, 132, 1))
c.add(arrow((308, 298), (308, 340)))
c.add(Window(48, 346, 520, 200, "Extensión nueva 1001", rows=[("Extension", "1001"), ("SIP/IAX Password", "se completa sola"), ("Quién la carga", "el teléfono")], hl=1))
c.add(panel(612, 132, 540, 200, "Lo que pide la central", "ok"))
lst, _ = bullet_list(636, 196, [("10 caracteres o más", "ok"), ("mayúscula y minúscula", "ok"), ("al menos un número y un especial", "ok"), ("sin secuencias como 1234 o abcd", "ok")], 500, size=17, gap=8)
c.add(lst)
c.add(panel(612, 356, 540, 190, "Lo que no", "alert"))
c.add(Mark(650, 446, ok=False))
c.add(text(684, 452, "contraseña 1001 en la extensión 1001", 16, 600, ALERT, FM))
c.add(Mark(650, 500, ok=False))
c.add(text(684, 506, "una clave que inventa una persona", 16, 600, ALERT, FB))
save(c, "2-paso1.svg")

# ---------------------------------------------------------------- 2-paso3: Direct Media apagado contra encendido
c = Canvas(K(3), "Direct Media apagado: el audio pasa por la central")
for j, (ttl, kd) in enumerate([("Direct Media: desactivado (como viene)", "ok"), ("Direct Media: activado", "alert")]):
    x0 = 48 + j * 564
    c.add(panel(x0, 130, 540, 456, ttl, kd, title_size=19))
    u = Generic(x0 + 150, 186, "UCM", "192.168.88.20", icon="server", w=240, dark=True)
    c.add(u)
    a = DeskPhone(x0 + 30, 380, "Interna 1001", "oficina")
    c.add(a)
    c.add(f'<rect x="{x0 + 310}" y="356" width="212" height="214" rx="18" fill="none" stroke="{WARN}" stroke-width="2" stroke-dasharray="7 7"/>')
    c.add(pill(x0 + 470, 364, "NAT remoto", WARN, WARN_BG, size=14))
    b = DeskPhone(x0 + 330, 390, "Interna 1002", "otra red")
    c.add(b)
    if j == 0:
        c.add(arrow((x0 + 115, 376), (x0 + 210, 274), kind="ok", label="RTP", label_at=0.45, label_dy=-6))
        c.add(arrow((x0 + 330, 274), (x0 + 415, 386), kind="ok", label="RTP", label_at=0.55, label_dy=-6))
        c.add(Mark(x0 + 270, 316, ok=True))
    else:
        c.add(Cable((x0 + 200, 450), (x0 + 330, 450), kind="alert", label="RTP directo", label_at=0.5, label_dy=-34))
        c.add(Mark(x0 + 292, 450, ok=False))
        c.add(text(x0 + 270, 316, "la central solo arma la llamada", 15, 500, INK2, FB, anchor="middle"))
c.add(text(48, 624, "Con Direct Media apagado, la central atiende el audio de los dos lados; activado, los teléfonos intentan hablarse directo y el NAT lo corta.", 16, 500, INK2, FB))
c.add(Step(48, 130, 3))
save(c, "2-paso3.svg")
