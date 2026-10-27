import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/omniaccess-face/src")
from _face import *

# ---------------------------------------------------------------- 7.svg: del Denegado al enrolado, con consentimiento
c = Canvas("OmniAccess Face · Lección 7", "Primero el consentimiento, después la foto")
steps_ = [("1", "Consentimiento", "leer el texto y anotar", "shield", OK),
          ("2", "Evento Denegado", "ficha → Registrar", "x", ALERT),
          ("3", "Foto revisada", "de frente, luz pareja", "user", BLUE),
          ("4", "Al terminal", "A qué equipos se manda", "server", BLUE),
          ("5", "Permitido", "con su nombre", "check", OK)]
for i, (n, t_, s_, ic, col) in enumerate(steps_):
    x = 48 + i * 226
    c.add(card(x, 140, 196, 170, stroke=col, sw=2))
    c.add(icon(x + 20, 158, ic, col, 1.5, 2))
    c.add(text(x + 20, 236, t_, 18, 600, INK, FB))
    c.add(text(x + 20, 262, s_, 15, 400, INK3, FB))
    c.add(Step(x + 172, 140, n, color=col))
    if i < 4:
        c.add(Arrow((x + 198, 225), (x + 224, 225), kind="flow", bend="straight"))
c.add(card(48, 344, 1104, 200, "Ley 18.331: lo que conviene saber en portería", fill=WHITE))
c.add(text(72, 404, "Art. 4, literal Ñ", 16, 600, BLUE, FM))
c.add(text(260, 404, "La cara usada para identificar es un dato biométrico (agregado por la Ley 19.924, 2020).", 16, 400, INK2, FB))
c.add(text(72, 444, "Art. 9", 16, 600, BLUE, FM))
c.add(text(260, 444, "Consentimiento libre, previo, expreso e informado, y documentado.", 16, 400, INK2, FB))
c.add(text(72, 484, "Art. 18 bis", 16, 600, BLUE, FM))
c.add(text(260, 484, "Con biometría, evaluación de impacto previa (según la URCDP, Dictamen 3/023).", 16, 400, INK2, FB))
c.add(text(72, 524, "Alternativa", 16, 600, OK, FM))
c.add(text(260, 524, "Quien no acepta entra con tarjeta, PIN o portería, sin castigo.", 16, 400, INK2, FB))
c.add(Note(48, 568, 1104, "La evaluación de impacto y la inscripción de la base las resuelve el responsable (administración) con su asesor; el guardia lee, anota y ofrece la alternativa.", kind="info", size=15))
save(c, "7.svg")

# ---------------------------------------------------------------- 7-paso1: texto de consentimiento de ejemplo
c = Canvas("OmniAccess Face · Lección 7 · Paso 1", "Leé el texto antes de sacar la foto")
c.add(card(48, 130, 700, 300, None, fill=WHITE, stroke=BLUE, sw=2))
c.add(icon(72, 150, "shield", BLUE, 1.4, 2))
c.add(text(120, 172, "Reconocimiento facial · Barrio Ejemplo", 19, 600, INK, FD))
body = ("Barrio Ejemplo usa reconocimiento facial en la portería peatonal. Su foto se guarda en el sistema de control de acceso "
        "y en el terminal, solo para abrir esta puerta y registrar los ingresos. Puede pedir la baja y el borrado en la "
        "administración. Si no acepta, puede entrar con tarjeta o por portería.")
s_, h_ = wrap(72, 220, body, 650, 17, 400, INK2)
c.add(s_)
c.add(text(72, 400, "Leído por: ____________   Fecha: ________   Acepta: Sí / No", 16, 500, INK3, FM))
c.add(Step(748, 130, 1))
c.add(Note(790, 140, 362, "Para qué se usa, quién lo guarda, cómo pedir la baja y qué alternativa hay.", title="Qué tiene que decir", kind="ok", size=16))
c.add(Note(790, 300, 362, "Borrador de laboratorio: el texto real lo define la administración del lugar.", kind="warn", size=16))
save(c, "7-paso1.svg")

# ---------------------------------------------------------------- 7-paso5: revisar la foto que trajo Registrar
c = Canvas("OmniAccess Face · Lección 7 · Paso 5", "La foto del evento es un borrador: revisala")
c.add(face_thumb(60, 150, 180, ok=False, bad="side"))
c.add(text(150, 360, "captura de la puerta", 16, 600, ALERT, FB, anchor="middle"))
c.add(Arrow((262, 240), (372, 240), label="Cambiar", kind="flow", label_dy=-14))
c.add(face_thumb(390, 150, 180, ok=True))
c.add(text(480, 360, "foto nueva", 16, 600, OK, FB, anchor="middle"))
c.add(Step(48, 150, 5))
checks = ["de frente, mirando a la cámara", "una sola cara", "luz pareja, sin contraluz", "sin lentes oscuros ni gorro", "JPG de menos de 200 KB"]
for i, ch in enumerate(checks):
    y = 170 + i * 52
    c.add(Mark(660, y, True))
    c.add(text(692, y + 6, ch, 17, 500, INK, FB))
c.add(Note(60, 420, 1092, "Registrar abre la ficha nueva con la foto de la captura. Si no cumple la lista, tocá Cambiar antes de mandarla al terminal.", kind="info", size=16))
save(c, "7-paso5.svg")
