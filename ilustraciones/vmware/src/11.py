import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/vmware/src")
from _vmw import *

# ---------------------------------------------------------------- 11.svg: qué mirar en cada pantalla
c = Canvas(K(), "\"Anda lento\": una tecla por sospechoso en esxtop")
c.add(NOLIG)
cards = [("c", "CPU", "%RDY", "tiempo que la VM esperó una CPU física libre", "alto = fila de CPU, no falta de vCPU"),
         ("m", "Memoria", "MCTLSZ · SWCUR", "balloon y swap del host", "si crecen, al host le falta memoria"),
         ("u", "Disco", "DAVG · KAVG · GAVG", "latencia del almacenamiento y del host", "DAVG alto: storage · KAVG alto: cola del host"),
         ("n", "Red", "%DRPTX · %DRPRX", "paquetes descartados", "mayores a cero: mirar NIC y vSwitch")]
for i, (k, t, f, d, r) in enumerate(cards):
    col, row = i % 2, i // 2
    x, y = 48 + col * 564, 124 + row * 200
    c.add(panel(x, y, 540, 180, None, "info"))
    s, w = keycap(x + 20, y + 22, k, 22, w=52)
    c.add(s)
    c.add(text(x + 88, y + 52, t, 21, 600, INK, FD))
    c.add(rect(x + 230, y + 24, 290, 38, SOFT, CYAN, rx=10, sw=1.5))
    c.add(text(x + 375, y + 49, f, 15, 700, BLUE, FM, anchor="middle"))
    c.add(text(x + 20, y + 104, d, 16, 400, INK2, FB))
    sv, _ = wrap(x + 20, y + 140, r, 500, 16, 600, WARN)
    c.add(sv)
c.add(Note(48, 530, 540, "Ninguna fuente da un umbral universal: compará contra los valores de un día normal del mismo cliente.", title="Sin número mágico", kind="info"))
c.add(Note(612, 530, 540, "Y antes de opinar, vmkernel.log y vmkwarning.log en /var/run/log.", title="Los logs del host", kind="info"))
save(c, "11.svg")

# ---------------------------------------------------------------- 11-paso2: un minuto en modo batch
c = Canvas(K(2), "Un minuto de esxtop guardado en un CSV")
c.add(NOLIG)
c.add(Step(48, 140, 2))
c.add(code(48, 168, 1104, "esxtop -b -a -d 5 -n 12 > /vmfs/volumes/datastore1/esxtop-$(hostname)-$(date +%Y%m%d-%H%M).csv", 15.5, h=50))
parts = [("-b", "modo batch", "escribe en vez de mostrar"), ("-a", "todos los contadores", "no solo los visibles"),
         ("-d 5", "cada 5 segundos", "una muestra"), ("-n 12", "12 muestras", "12 × 5 s = 1 minuto"),
         ("> …csv", "al datastore", "con host, fecha y hora")]
for i, (p, t, s) in enumerate(parts):
    x = 48 + i * 224
    c.add(panel(x, 250, 208, 150, None, "info"))
    c.add(text(x + 20, 290, p, 20, 700, BLUE, FM))
    c.add(text(x + 20, 330, t, 16, 600, INK, FB))
    c.add(text(x + 20, 358, s, 15, 400, INK2, FB))
# timeline 12 muestras
c.add(text(48, 448, "12 muestras, una cada 5 segundos", 17, 600, INK, FD))
for k in range(12):
    x = 48 + k * 92
    c.add(rect(x, 466, 80, 36, SOFT, BLUE, rx=8, sw=1.5))
    c.add(text(x + 40, 490, f"{(k + 1) * 5} s", 14, 600, BLUE, FM, anchor="middle"))
c.add(Note(48, 528, 1104, "Ese CSV es la prueba: se abre después con calma y se compara con el de un día normal (paso 4, la línea base).", kind="ok"))
save(c, "11-paso2.svg")

# ---------------------------------------------------------------- 11-paso3: logs del host
c = Canvas(K(3), "Dónde buscar errores: /var/run/log del host")
c.add(NOLIG)
c.add(Step(48, 140, 3))
files = [("vmkernel.log", "el núcleo: discos, rutas, red, drivers", "primero"), ("vmkwarning.log", "solo las advertencias del núcleo", "segundo"),
         ("hostd.log", "el agente del host (Host Client, tareas)", "si hace falta")]
for i, (f, d, o) in enumerate(files):
    y = 170 + i * 92
    c.add(filebox(48, y, 520, f"/var/run/log/{f}", d, "soft" if i < 2 else "info", h=72, size=16))
    c.add(tag(560, y + 44, o, "info" if i < 2 else "gray", anchor="end"))
t = Terminal(612, 170, 540, [("$ grep -i -E \"error|fail|lost\" \\", "#9FE3F7"), ("    /var/run/log/vmkernel.log | tail -n 30", "#9FE3F7"),
                             ("$ tail -n 50 /var/run/log/vmkwarning.log", "#9FE3F7")], title="SSH AL HOST")
c.add(t)
c.add(Note(612, 340, 540, "En vCenter el equivalente es vpxd. En el host, estos tres.", kind="info"))
c.add(Note(48, 460, 1104, "Si el host arranca de SD o USB, estos logs viven en memoria y se pierden al reiniciar: otro motivo para un disco de arranque persistente.", title="Ojo con los reinicios", kind="warn"))
save(c, "11-paso3.svg")
