from _akx2941 import *

K = "Akuvox"

# ---------------------------------------------------------------- figura principal
c = Canvas(K, "Elegí el terminal por la credencial de la puerta")
rows = [
    ["A01S", "13,56 y 125 kHz", False, False, False, False],
    ["A02S", "13,56 y 125 kHz", True, False, False, False],
    ["A03S", "13,56 y 125 kHz", True, True, False, False],
    ["A05C", "13,56 MHz", True, True, True, True],
    ["A08S", "13,56 y 125 kHz", True, True, True, False],
]
c.add(check_table(48, 140, ["Modelo", "Tarjeta", "PIN", "Bluetooth", "QR", "Rostro"], rows, [130, 210, 90, 130, 90, 110], row_h=54))
c.add(legend_ok_bad(70, 500))
c.add(Note(840, 140, 310, "A01 a A03: 30 V 3 A.\nA05 y A08: 30 V 2 A.", title="Relé", kind="info"))
c.add(Note(840, 290, 310, "A01, A02, A03 y A08 dan 12 V 500 mA por el relé. El A05 no da: su cerradura lleva fuente propia.", title="12 V para la cerradura", kind="warn"))
c.add(Label(48, 580, "A08 (ficha): aluminio, IP65 e IK09, también NFC y BLE 5.0. Datos: tabla de métodos de acceso de Akuvox.", 15, 400, INK3))
c.save(out("33.svg"))

# ---------------------------------------------------------------- paso 4
c = Canvas(K + " · Paso 4", "¿De dónde sale la energía de la cerradura?")
c.add(Zone(40, 150, 540, 470, "A08: 12 V por el relé", OK))
c.add(Zone(620, 150, 540, 470, "A05: sin salida de 12 V", WARN))
# A08
psu = c.add(PSU(80, 190, "Fuente 12 V 1 A", "o más", w=230))
c.add(Chip(330, 238, "o PoE (hw 108.2.0.0.0+)", "gray"))
a08 = c.add(Generic(80, 340, "A08", "relé A", icon="key", w=230))
c.add(Wire([psu.bottom(), a08.top()], kind="power+"))
lk = c.add(Lock(80, 490, "Cerradura", "hasta 500 mA", w=230))
c.add(Wire([a08.bottom(), lk.top()], kind="relay", label="12 V 500 mA", at=(195, 466)))
c.add(Mark(350, 532, True))
c.add(Label(378, 538, "listo", 16, 600, OK))
# A05
a05 = c.add(Generic(660, 340, "A05", "relé: solo contacto", icon="key", w=250))
psu2 = c.add(PSU(660, 190, "Fuente propia", "para la cerradura", w=250))
lk2 = c.add(Lock(660, 490, "Cerradura", "según su consumo", w=250))
c.add(Wire([psu2.bottom(-40), a05.top(-40)], kind="power+", label="+", at=(745, 315)))
c.add(Wire([a05.bottom(-40), lk2.top(-40)], kind="relay"))
c.add(Wire([lk2.right(), (1000, lk2.right()[1]), (1000, psu2.right()[1]), psu2.right()], kind="power-", label="−", at=(1000, 390)))
c.add(Step(1080, 200, 4))
c.save(out("33-paso4.svg"))
