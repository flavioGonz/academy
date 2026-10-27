from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "¿Qué trae cada monitor de la serie S?")
rows = [
    ["S562", True, "30 V 1 A", True, True],
    ["S563", True, "30 V 2 A", True, True],
    ["S565", True, "30 V 2 A", True, True],
    ["S567", True, "30 V 2 A", True, False],
    ["S560", False, False, False, False],
]
c.add(check_table(48, 140, ["Modelo", "RS485", "Relé (carga)", "Timbre", "RJ45 extra"], rows, [150, 120, 190, 120, 150], row_h=54))
c.add(f'<rect x="52" y="{140 + 54 + 3}" width="722" height="48" rx="10" fill="none" stroke="{WARN}" stroke-width="2"/>')
c.add(legend_ok_bad(70, 500))
c.add(Note(830, 140, 320, "Es el único con relé de 1 A: un portón o una cerradura que pida más va con relé auxiliar o fuente propia.", title="S562: ojo con la carga", kind="warn"))
c.add(Note(830, 330, 320, "El de auricular: no tiene RS485, relé ni entrada de timbre. No se vende para abrir ni para domótica.", title="S560", kind="info"))
c.add(Label(48, 580, "Datos: tablas de interfaces y de carga de relé de Akuvox. Del S565 no se afirman tamaño ni sistema.", 15, 400, INK3))
c.save(out("30.svg"))

# ---------------------------------------------------------------- paso 4
c = Canvas(K + " · Paso 4", "Probá el relé con una lámpara de 12 V de banco")
m = c.add(Monitor(60, 150, "Monitor S562", "relé 30 V 1 A"))
st = c.add(Strip(400, 150, "Salida de relé", ["borne 1", "borne 2"], sub="contacto del relé", tw=96, w=280))
c.add(Arrow((m.x + m.w + 8, 230), (st.x - 8, 214), kind="logical", label="atrás", label_at=0.5))
psu = c.add(PSU(400, 470, "Fuente 12 V", "de banco"))
lamp = c.add(Lamp(900, 370, "Lámpara 12 V", "de banco"))
b1, b2 = st.port("borne 1"), st.port("borne 2")
c.add(Wire([(b1[0], psu.y), b1], kind="power+", label="+12 V", at=(b1[0], 400)))
c.add(Wire([b2, (b2[0], 370), lamp.port("a")], kind="relay", label="cuando cierra", at=(720, 356)))
c.add(Wire([lamp.port("b"), (1010, 370), (1010, 512), (psu.x + psu.w, 512)], kind="power-", label="− vuelve a la fuente", at=(800, 498)))
c.add(Step(b2[0] + 40, b2[1] + 26, 4))
c.add(Note(60, 380, 290, "Activá el relé desde el monitor: la lámpara prende mientras el contacto está cerrado.", title="Qué tiene que pasar", kind="ok"))
c.add(chips_row(60, 640, [("S562: máx. 30 V 1 A", "warn"), ("S563 · S565 · S567: máx. 30 V 2 A", "gray")]))
c.save(out("30-paso4.svg"))

# ---------------------------------------------------------------- paso 5
c = Canvas(K + " · Paso 5", "Relés externos por RS485: primero el firmware")
m = c.add(Monitor(60, 150, "Monitor S", "puerto RS485"))
mk = c.add(Generic(430, 188, "MK485", "8 salidas de relé", icon="bolt", w=250))
c.add(Cable(m.right(-10), mk.left(), kind="relay", label="RS485", label_at=0.5, label_dy=-14))
l1 = c.add(Generic(820, 130, "Luces", "domótica", icon="bolt", w=250))
l2 = c.add(Generic(820, 250, "Cortinas", "domótica", icon="bolt", w=250))
c.add(Label(430, 320, "Cada salida del MK485:", 15, 600, INK))
c.add(Label(430, 344, "C + B normal abierto · C + A normal cerrado", 15, 500, INK2, FM))
c.add(Arrow(mk.right(-12), l1.left(), kind="flow"))
c.add(Arrow(mk.right(12), l2.left(), kind="flow"))
c.add(Table(60, 400, ["Modelo", "Firmware mínimo"], [["S562", "562.30.14.204"], ["S563", "563.30.12.902"], ["S565", "565.30.10.210"], ["S567", "567.30.12.802"]], [150, 260], row_h=42, mono_cols=(1,)))
c.add(Note(530, 400, 620, "Akuvox soporta los relés externos en la web desde estas versiones. Si el tuyo es menor, actualizá primero; después, Device > External Relay y elegí el tipo (MK485 o RSAC-C1-R8).", title="Comparalo con Status antes de cablear", kind="warn"))
c.add(Note(530, 560, 620, "RSAC-C1-R8: 8 relés, 8 salidas y 8 entradas; hasta 3 por monitor, dirección por DIP.", kind="info"))
c.save(out("30-paso5.svg"))
