from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Equipo viejo en la pared: identificar, asegurar, reemplazar")
c.add(card(40, 150, 350, 160, "Identificar", "Sacá la IP y leé el firmware A.B.C.D. El bloque A dice el modelo; un C de 10 o más, alta seguridad.", n="1"))
c.add(card(425, 150, 350, 160, "Asegurar", "Mientras siga instalado: firmware al día, clave propia y VLAN de porteros, sin puertos abiertos a internet.", n="2"))
c.add(card(810, 150, 350, 160, "Reemplazar", "Buscá en el menú vigente un equipo del mismo tipo y verificá credenciales y alimentación.", n="3"))
c.add(Arrow((392, 230), (423, 230), kind="flow"))
c.add(Arrow((777, 230), (808, 230), kind="flow"))
c.add(Label(40, 375, "Parque que sigue en las paredes (en tablas de Akuvox, no en el menú de octubre de 2026):", 16, 600, INK))
c.add(chips_row(40, 421, ["E11", "R27", "R26", "DB01", "E20", "C315", "C310", "IT83", "A092"], kind="gray", mono=True))
c.add(Note(40, 470, 1120, "El E11 es el modelo de las 13 vulnerabilidades publicadas por Claroty en marzo de 2023: si sigue en una pared, va primero en la lista de revisión.", title="Primero el E11", kind="alert"))
c.save(out("41.svg"))

# ---------------------------------------------------------------- paso 2
c = Canvas(K + " · Paso 2", "El bloque A del firmware dice qué equipo es")
rows = [["111.", "E11", "portero"], ["120.", "E20", "portero (no se integra con EC33)"], ["27.", "R27", "portero"],
        ["83.", "IT83", "monitor"], ["115.", "C315", "monitor"], ["310.", "C310", "monitor"], ["92.", "A092 / A094", "control de acceso"]]
c.add(Table(40, 140, ["Bloque A", "Modelo", "Tipo"], rows, [170, 220, 360], row_h=50, mono_cols=(0,)))
c.add(Note(830, 140, 330, "El 92. es compartido: A092 (viejo) y A094 (vigente). Confirmá con la etiqueta o la web.", title="Ojo con el 92.", kind="warn"))
c.add(Note(830, 330, 330, "Si el C es 10 o más, el equipo está en la rama de alta seguridad. Si es menor, el HTTP viejo puede seguir activo.", title="Y el bloque C", kind="info"))
c.save(out("41-paso2.svg"))

# ---------------------------------------------------------------- paso 5
c = Canvas(K + " · Paso 5", "Mientras siga instalado: VLAN de porteros")
c.add(Zone(350, 150, 470, 300, "VLAN porteros 10.10.10.0/24", CYAN))
e = c.add(Generic(380, 200, "E11R", "portero viejo", icon="bell", w=200))
m = c.add(Generic(600, 200, "C315S", "monitor viejo", icon="laptop", w=200))
c.add(Label(380, 350, "firmware al día · clave propia", 16, 600, INK2))
inet = c.add(Internet(40, 200, "Internet", "WAN", w=230))
cen = c.add(Server(900, 160, "Central", "10.10.20.10", w=250))
nvr = c.add(Server(900, 300, "NVR", "10.10.30.10", w=250))
c.add(Arrow((820, 220), cen.left(), kind="ok", label="SIP", label_at=0.5))
c.add(Arrow((820, 330), nvr.left(), kind="ok", label="RTSP 554", label_at=0.5, label_dy=24))
c.add(Cable(inet.right(), (346, inet.right()[1]), kind="alert", arrow=True))
c.add(Mark(306, inet.right()[1] + 40, False))
c.add(Label(40, 330, "desde internet:", 16, 600, ALERT))
c.add(Label(40, 354, "sin reenvío de puertos", 16, 600, ALERT))
c.add(Note(40, 500, 1110, "Todo lo demás, denegado. Ningún reenvío de puertos desde la WAN (lección 11).", kind="warn"))
c.save(out("41-paso5.svg"))
