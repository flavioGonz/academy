"""Genera ilustraciones/bosch-incendio/glosario-propuesta.json y lo prueba sobre una copia combinada del glosario.

  python3 glosario_bi.py     # escribe la propuesta y valida la copia en el scratchpad

- terms: entradas nuevas completas (id, term, aliases, cat, short, long, year si corresponde, case).
- alias_agregar: alias nuevos para entradas que ya existen (EOL: los módulos de fin de línea de Bosch).
- modificar: ninguno.
No toca site2/data/glosario.json. Ya existen y no se duplican: EOL, retardo de transmisión, RSTP, IPsec, UPS, LED,
relé, NO, NC, gateway, IGMP (multicast), modelo OSI, EN 50131, ISO/IEC.
"""
import json, os, subprocess, sys

I = "Incendio"
T = [
    {"id": "avenar", "term": "AVENAR", "aliases": ["AVENAR panel", "AVENAR panel 2000", "AVENAR panel 8000", "AVENAR keypad 8000", "FPE-2000", "FPE-8000"], "cat": I,
     "short": "La línea vigente de centrales de incendio modulares de Bosch: AVENAR panel 2000 (hasta 4 lazos) y 8000 (hasta 32 lazos), con su teclado remoto.",
     "long": "El 2000 admite 6 módulos y viene como kit; el 8000 admite 46 módulos en riel. La licencia viene grabada en el controlador: SPC es standard y PPC es premium, que habilita BMS, panel jerárquico, voz y, en el 2000, la red. Las redes solo AVENAR corren firmware 4.x.",
     "case": True},
    {"id": "fpa-bosch", "term": "FPA", "aliases": ["FPA-5000", "FPA-1200", "MPC"], "cat": I,
     "short": "La generación anterior de centrales de incendio Bosch: FPA-5000 para redes y FPA-1200 para sitios chicos.",
     "long": "Comparten el lazo LSN con AVENAR. Una red con al menos un FPA corre toda el mismo firmware 3.x, que salió de mantenimiento a fines de 2025. Se puede modernizar cambiando solo el controlador por uno AVENAR.",
     "case": True},
    {"id": "lsn", "term": "LSN", "aliases": ["Local Security Network", "LSN improved", "LSN classic", "LSNi", "lazo LSN"], "cat": I,
     "short": "Local Security Network: el bus de campo de Bosch que lleva alimentación y datos a detectores, pulsadores, sirenas y módulos por un solo par.",
     "long": "LSN improved admite 254 elementos por módulo de lazo; con un solo elemento classic baja a 127 y sin T-tap. El módulo LSN 0300 A da 300 mA y hasta 1600 m; el LSN 1500 A, hasta 1500 mA y 3000 m. Cada elemento trae aislador entre b1 y b2.",
     "case": True},
    {"id": "t-tap", "term": "T-tap", "aliases": ["derivación T-tap", "derivaciones"], "cat": I,
     "short": "Derivación en cualquier punto de una línea LSN improved, que permite ramas sin volver al panel.",
     "long": "Solo es posible con dirección manual (perillas 001 a 254) y con T-tap marcado en FSP-5000-RPS. Nunca se arman mallas: una derivación no vuelve a unirse con otra parte del lazo.",
     "case": False},
    {"id": "aislador-corto", "term": "aislador de cortocircuito", "aliases": ["aislador", "aisladores", "short-circuit isolator", "EN 54-17"], "cat": I,
     "short": "Componente que abre la línea a ambos lados de un corto, para que el resto del lazo siga funcionando.",
     "long": "En LSN viene integrado en cada elemento, entre b1 y b2. Ante un corto, el panel parte el lazo en dos ramales alimentados desde cada extremo. La norma de producto europea es EN 54-17, de 2005.",
     "case": False},
    {"id": "clases-circuito", "term": "clase A, B y X", "aliases": ["clase A", "clase B", "clase X", "Class A", "Class B", "Class X"], "cat": I,
     "short": "Clasificación de NFPA 72 que describe qué pasa con la detección ante una falla del cableado.",
     "long": "Clase B pierde lo que queda detrás de un corte; clase A vuelve al panel y sobrevive a un corte; clase X sobrevive también a un corto gracias a los aisladores. La norma no impone una clase: la elige el proyecto o la autoridad.",
     "case": True},
    {"id": "fsp-5000-rps", "term": "FSP-5000-RPS", "aliases": ["RPS", "Remote Programming System", "FSP"], "cat": "Herramientas",
     "short": "El programa de Bosch para configurar, validar y descargar las centrales FPA y AVENAR desde una laptop.",
     "long": "Se baja de la extranet de Bosch. A octubre de 2026 la versión vigente es la 5.15.28, en Windows 11 24H2 de 64 bits. La cuenta de configuración 4.8 agregó Uruguay como país. Antes de cada descarga conviene Set Panel Time y un chequeo de consistencia sin errores.",
     "case": True},
    {"id": "ssd-bosch", "term": "Safety Systems Designer", "aliases": ["SSD"], "cat": "Herramientas",
     "short": "La herramienta de planificación de Bosch que calcula largos de lazo, energía, baterías y cantidades.",
     "long": "Bosch la exige para planificar instalaciones AVENAR nuevas con zonas de energía (versión 3.6 o más). La cuenta de banco del manual sirve para detectar un lazo en el límite; el cálculo de obra se hace en SSD.",
     "case": True},
    {"id": "pna", "term": "PNA", "aliases": ["número de nodo", "nodo físico"], "cat": I,
     "short": "Número de nodo físico de un panel Bosch en la red, cargado en el panel y en RPS.",
     "long": "En las redes Ethernet de Bosch, la IP por defecto es 192.168.1.x con x igual al PNA. Tiene que coincidir en el panel, en la IP y en la configuración de RPS.",
     "case": True},
    {"id": "bcm-bosch", "term": "BCM", "aliases": ["FPE-8000-BCM", "BCM-0000-B", "módulo de baterías"], "cat": I,
     "short": "El módulo de fuente y baterías de las centrales Bosch modulares.",
     "long": "Desde el 02/05/2026 la obra nueva usa el FPE-8000-BCM con zonas de energía; no se mezcla con el BCM-0000-B en un mismo panel. Pide firmware 4.7.0, RPS 5.14.17 y SSD 3.6 o más.",
     "case": True},
    {"id": "zona-energia", "term": "zona de energía", "aliases": ["zonas de energía", "energy zone"], "cat": I,
     "short": "Parte de un panel AVENAR con su propio FPE-8000-BCM y sus baterías, separada del resto.",
     "long": "Las zonas se separan quitando el cable rojo entre dos rieles largos, y los módulos de alto consumo van al lado del BCM. Si falla un BCM o sus baterías, las otras zonas siguen funcionando.",
     "case": False},
    {"id": "flm", "term": "FLM", "aliases": ["FLM-420", "FLM-430", "FLM-420/4-CON", "FLM-430-I2M1", "FLM-430-I4R2", "FLM-420-RLE-S", "FLM-420-NAC"], "cat": I,
     "short": "Los módulos de interfaz de Bosch que conectan entradas, salidas y zonas convencionales al lazo LSN.",
     "long": "Por ejemplo, el FLM-430-I2M1 tiene 2 entradas y 1 salida supervisada, el FLM-420/4-CON conecta dos zonas convencionales y el FLM-420-RLE-S controla extinción. Cada entrada programada como alarma consume un punto del panel.",
     "case": True},
    {"id": "avenar-detector-4000", "term": "AVENAR detector 4000", "aliases": ["FAP-425", "FAH-425", "FAP", "FAH", "DOTC", "DOTCO", "FAP-425-DOT-R", "FAP-425-DOTC-R"], "cat": I,
     "short": "La serie vigente de detectores puntuales Bosch para LSN, con nueve variantes ópticas, térmicas y multisensor.",
     "long": "Van del térmico FAH-425-T-R al multisensor FAP-425-DOTCO-R. Las letras dicen los sensores: O óptico, DO doble óptico, T térmico, C químico (CO); -R indica perillas de dirección. Todos traen aislador. El firmware 4.8 es el último que soporta la serie 400 anterior.",
     "case": True},
    {"id": "fnx-425u", "term": "FNX-425U", "aliases": ["FNX", "FNM-420", "FNM"], "cat": I,
     "short": "Sirenas y balizas Bosch que se alimentan y comandan desde el lazo LSN.",
     "long": "La FNX-425U admite hasta 84 por lazo si hay detectores y 127 si no. Desde el firmware 4.8.1 reporta horas, batería y avería a NEXOSPACE. Una sirena no consume punto de alarma.",
     "case": True},
    {"id": "fmc-420", "term": "FMC-420RW", "aliases": ["FMC", "pulsador manual", "pulsador de incendio"], "cat": I,
     "short": "Pulsador manual de alarma de incendio Bosch para el lazo LSN.",
     "long": "Consume un punto de alarma. Nunca lleva retardo: un pulsador anula cualquier alarma demorada. La IT-11 uruguaya de 2010 pide pulsador a no más de 30 m.",
     "case": True},
    {"id": "nac", "term": "NAC", "aliases": ["Notification Appliance Circuit", "línea NAC"], "cat": I,
     "short": "Notification Appliance Circuit: el circuito que alimenta sirenas y balizas convencionales.",
     "long": "En Bosch, por ejemplo, la línea NAC del FLM-420-NAC; su cable cuenta en el tope de 500 m de cable no aislado. En EN 54-2, silenciar avisadores es manual: un temporizador de duración solo vale para señales que no son EN 54.",
     "case": True},
    {"id": "punto-alarma", "term": "punto de alarma", "aliases": ["puntos de alarma", "punto lógico", "puntos lógicos"], "cat": I,
     "short": "Cada elemento o entrada que puede dar alarma en un panel Bosch, contado para límites y redundancia.",
     "long": "Desde la cuenta 4.5 se separan los puntos de alarma, que deciden si hace falta controlador redundante, de los puntos lógicos, con tope de 4096 en panel solo y 2048 por panel en red. EN 54-2 limita a 512 los detectores y pulsadores que puede dejar fuera una falla.",
     "case": False},
    {"id": "direccion-logica", "term": "dirección lógica", "aliases": ["zona lógica", "grupo y subdirección", "subdirección"], "cat": I,
     "short": "El nombre estable de un elemento en un panel Bosch: grupo y subdirección, como 3.4.",
     "long": "Se elige en RPS, sin repetir. El panel la muestra en cada mensaje junto con el tipo y la ubicación, y las integraciones la heredan. La dirección física, en cambio, es el lugar en el lazo.",
     "case": False},
    {"id": "matriz-causa-efecto", "term": "matriz de causa y efecto", "aliases": ["matriz causa efecto", "matriz de control"], "cat": I,
     "short": "Tabla que define qué efecto produce cada causa en un sistema de incendio, antes de programarlo.",
     "long": "Filas con causas (detectores, pulsadores, entradas técnicas) y columnas con efectos (sirenas, puertas, ventilación, transmisión). Es parte del proyecto, la firma el técnico responsable y cada cruce se programa como una regla.",
     "case": False},
    {"id": "modo-revision", "term": "modo revisión", "aliases": ["walk test", "walktest", "revision mode", "walk test secuencial", "walk test simultáneo"], "cat": I,
     "short": "Estado de prueba de una zona en un panel Bosch: el detector se prepara para responder al estímulo de prueba.",
     "long": "Con aerosol, el detector dispara en hasta 10 s (hasta 20 s en multisensor). En walk test simultáneo, la alarma aparece solo si dispararon todos los sensores. Un detector en revisión no da alarma de fuego normal: la zona sale de revisión al terminar.",
     "case": False},
    {"id": "alarma-demorada", "term": "alarma demorada", "aliases": ["prealarma", "preseñal", "alarma confirmada", "modo día", "modo noche", "día y noche"], "cat": I,
     "short": "Estrategia para investigar una alarma de detector antes de evacuar, con un tiempo máximo.",
     "long": "BS 5839-1 limita la demora a 6 minutos y un pulsador la anula; la IT-11 uruguaya de 2010 admite preseñal de hasta 2 minutos en locales concurridos. En modo noche el primer detector va directo a alarma general. Solo con acuerdo de la autoridad y del proyecto firmado.",
     "case": False},
    {"id": "en-54", "term": "EN 54", "aliases": ["EN54", "EN 54-2", "EN 54-4", "EN 54-5", "EN 54-7", "EN 54-13", "EN 54-29"], "cat": "Normas",
     "short": "La serie de normas europeas de producto para detección y alarma de incendio, del comité CEN/TC 72.",
     "long": "Empezó en los años setenta: EN 54-1 y EN 54-5 salieron en 1976. Cada parte cubre un tipo de equipo: EN 54-2 central, EN 54-4 fuente, EN 54-7 humo, EN 54-5 calor, EN 54-13 compatibilidad. Dice cómo se ensaya un equipo, no dónde va.",
     "year": 1976, "case": True},
    {"id": "nfpa-72", "term": "NFPA 72", "aliases": ["NFPA", "National Fire Alarm and Signaling Code"], "cat": "Normas",
     "short": "El código estadounidense de alarma de incendio y señalización de la NFPA.",
     "long": "Se revisa por ediciones; la de 2013 sumó la preverificación por la central de monitoreo, con 90 s como máximo. Define las clases A, B y X y el cálculo de baterías con 24 h de reposo y 5 min de alarma. En Uruguay se usa como referencia.",
     "case": True},
    {"id": "dnb", "term": "DNB", "aliases": ["Dirección Nacional de Bomberos", "Bomberos"], "cat": "Normas",
     "short": "Dirección Nacional de Bomberos de Uruguay: la autoridad que habilita los sistemas de protección contra incendio.",
     "long": "Registra técnicos y empresas, recibe los trámites y publica los instructivos técnicos, como la IT-11 de detección y alarma. En julio de 2026 abrió la consulta pública de una nueva IT11.",
     "case": True},
    {"id": "decreto-372-023", "term": "Decreto 372/023", "aliases": ["372/023", "decreto de habilitaciones"], "cat": "Normas",
     "short": "Decreto uruguayo que reglamenta las habilitaciones de Bomberos, vigente desde enero de 2024.",
     "long": "El proyecto lo redacta y firma un técnico registrado, que ingresa el trámite bajo declaración jurada; los sistemas de detección los suministran, instalan, ponen en marcha y mantienen empresas registradas ante la DNB. Prevé multas de 10 a 200 UR para empresas.",
     "year": 2023, "case": True},
    {"id": "it-11", "term": "IT-11", "aliases": ["IT11", "instructivo técnico 11"], "cat": "Normas",
     "short": "El instructivo técnico de Bomberos de Uruguay para sistemas de detección y alarma de incendio.",
     "long": "La vigente es del 17/11/2010 y remite a UNIT 962. Pide, entre otras cosas, 24 h de batería en reposo y 15 min en alarma, y pulsador a no más de 30 m. Su revisión está en consulta pública con vigencia prevista en 2027; el borrador no se usa hasta que rija.",
     "year": 2010, "case": True},
    {"id": "unit-uy", "term": "UNIT", "aliases": ["Instituto Uruguayo de Normas Técnicas", "UNIT 962"], "cat": "Normas",
     "short": "Instituto Uruguayo de Normas Técnicas, el organismo de normalización de Uruguay.",
     "long": "La IT-11 de Bomberos remite a la norma UNIT 962 para detección y alarma de incendio.",
     "case": True},
    {"id": "tecnico-registrado", "term": "técnico registrado", "aliases": ["técnicos registrados", "empresa registrada", "empresas registradas"], "cat": "Normas",
     "short": "Profesional registrado ante la DNB que redacta y firma el proyecto de protección contra incendio.",
     "long": "Según el Decreto 372/023, ingresa el trámite y verifica las medidas. La instalación y el mantenimiento los hacen empresas registradas. Cuando el proyecto y el manual no coinciden, se consulta al técnico registrado.",
     "case": False},
    {"id": "vds", "term": "VdS", "aliases": ["VdS 2496", "VdS 2540", "VdS 3860"], "cat": "Normas",
     "short": "Organismo alemán de certificación de seguridad, cuyas directivas usa Bosch en extinción, redes y autotest.",
     "long": "VdS 2496 define la interfaz de control de extinción (FLM-420-RLE-S); VdS 2540 pide fibra en las redes de paneles en Alemania. Son referencias técnicas, no exigencias uruguayas.",
     "case": True},
    {"id": "bs-5839", "term": "BS 5839-1", "aliases": ["BS 5839", "BS"], "cat": "Normas",
     "short": "Código británico de práctica para sistemas de detección y alarma de incendio en edificios.",
     "long": "Limita la alarma demorada a 6 minutos y deja que un pulsador la anule. Su anexo E trae el ejemplo de la habitación de hotel con ducha, donde frente al vapor queda mejor el detector de CO.",
     "case": True},
    {"id": "fia", "term": "FIA", "aliases": ["Fire Industry Association"], "cat": "Normas",
     "short": "Fire Industry Association: la asociación británica de la industria de protección contra incendio.",
     "long": "Propone elegir el detector en dos pasos, riesgo de fuego y fenómenos engañosos, y describe estrategias contra falsas alarmas, con la advertencia de que todo filtrado demora la respuesta a un fuego real.",
     "case": True},
    {"id": "bre", "term": "BRE", "aliases": ["Building Research Establishment", "BRE Group"], "cat": "Normas",
     "short": "Organismo británico de investigación de la construcción, autor de ensayos de detectores.",
     "long": "En 2018 publicó ensayos con 35 multisensores y 2 ópticos: ante fuegos rindieron parecido; ante tostadas, vapor, polvo y aerosol, los multisensores dispararon más tarde.",
     "case": True},
    {"id": "cen", "term": "CEN", "aliases": ["Comité Europeo de Normalización", "CEN/TC 72"], "cat": "Normas",
     "short": "Comité Europeo de Normalización, que publica las normas EN.",
     "long": "Su comité técnico CEN/TC 72 prepara la serie EN 54 de detección y alarma de incendio.",
     "case": True},
    {"id": "co-monoxido", "term": "CO", "aliases": ["monóxido de carbono", "sensor de CO", "celda de CO"], "cat": I,
     "short": "Monóxido de carbono: gas que aparece temprano en fuegos latentes y que miden los detectores químicos.",
     "long": "En el AVENAR detector 4000 lo mide la celda química de los DOTC y DOTCO (en el DOTCO, de 10 años). Según la hoja de datos, también reacciona a hidrógeno y monóxido de nitrógeno.",
     "case": True},
    {"id": "bms", "term": "BMS", "aliases": ["Building Management System", "sistema de gestión del edificio"], "cat": "Web e integración",
     "short": "Building Management System: el sistema que supervisa las instalaciones de un edificio desde un puesto central.",
     "long": "Un panel AVENAR se integra por OPC, FSI o BACnet, con licencia premium en cada panel visible. Si Ethernet se usa solo para eso, se desactiva la comunicación panel a panel por TCP/IP.",
     "case": True},
    {"id": "opc", "term": "OPC", "aliases": ["servidor OPC", "OPC server"], "cat": "Web e integración",
     "short": "Estándar de intercambio de datos industriales; en Bosch, el servidor que expone los paneles al BMS.",
     "long": "El servidor OPC es un nodo más de la red de incendio y separa la red del cliente de la de los paneles.",
     "case": True},
    {"id": "bacnet", "term": "BACnet", "aliases": ["ASHRAE 135"], "cat": "Web e integración",
     "short": "Protocolo de comunicación para automatización de edificios, publicado por ASHRAE como norma 135.",
     "long": "La primera versión es de 1995. Es una de las interfaces con las que un panel AVENAR premium se integra a un BMS.",
     "year": 1995, "case": False},
    {"id": "fsi-bosch", "term": "FSI", "aliases": ["Fire System Interface"], "cat": "Web e integración",
     "short": "Interfaz de Bosch para integrar sus paneles de incendio con sistemas de gestión.",
     "long": "Aparece junto con OPC y BACnet entre las integraciones a BMS, que requieren licencia premium en cada panel.",
     "case": True},
    {"id": "ugm", "term": "UGM", "aliases": ["UGM-2040", "panel jerárquico"], "cat": I,
     "short": "Panel jerárquico de Bosch que concentra varias centrales de incendio.",
     "long": "La conexión a un UGM es una de las funciones que habilita la licencia premium del AVENAR.",
     "case": True},
    {"id": "can-bus", "term": "CAN", "aliases": ["CAN bus", "Controller Area Network", "CAN1", "CAN2"], "cat": "Redes",
     "short": "Controller Area Network: bus de comunicación que Bosch presentó en 1986 para los autos.",
     "long": "Los controladores AVENAR traen dos interfaces CAN para armar redes de paneles, como alternativa o complemento de Ethernet.",
     "year": 1986, "case": True},
    {"id": "ti-bosch", "term": "TI", "aliases": ["Technical Information", "hoja técnica", "TI 2715", "TI 2716", "TI 2739"], "cat": I,
     "short": "Technical Information: las hojas técnicas numeradas con que Bosch anuncia versiones, cambios y fallas conocidas.",
     "long": "Por ejemplo, la TI 2715 de 2026 trae el firmware 4.8.1, la 2716 lanza las zonas de energía y la 2739 explica la falla de validación de autonomía de RPS con su truco temporal.",
     "case": True},
    {"id": "ur-uy", "term": "UR", "aliases": ["Unidad Reajustable"], "cat": "Normas",
     "short": "Unidad Reajustable: unidad de cuenta uruguaya que se usa, entre otras cosas, para fijar multas.",
     "long": "El Decreto 372/023 fija multas de 10 a 200 UR para empresas.",
     "case": True},
    {"id": "sau", "term": "SAU", "aliases": ["Sociedad de Arquitectos del Uruguay"], "cat": "Normas",
     "short": "Sociedad de Arquitectos del Uruguay.",
     "long": "En el curso aparece como el sitio donde se leyó el texto de la IT-11 de Bomberos.",
     "case": True},
    {"id": "html", "term": "HTML", "aliases": ["HyperText Markup Language"], "cat": "Web e integración",
     "short": "HyperText Markup Language: el lenguaje de las páginas web.",
     "long": "En el curso aparece porque la ayuda de FSP-5000-RPS pasó a formato HTML desde la versión 5.15.27.",
     "case": True},
]

ALIAS = {"eol": ["FLM-420-EOL4W", "FLM-320-EOL4W-S", "módulo de fin de línea"]}

GLOS = "/home/claude/ies-training/site2/data/glosario.json"
OUT = "/home/claude/ies-training/ilustraciones/bosch-incendio/glosario-propuesta.json"
COMB = "/tmp/claude-0/-home-claude/e7efb7ec-f4b7-5f80-a457-304e3488cc08/scratchpad/glosario-bosch-incendio.json"

g = json.load(open(GLOS, encoding="utf-8"))
by = {t["id"]: t for t in g["terms"]}
P = {"nota": "Propuesta para el curso Bosch Incendio. terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes. modificar: ninguno. Probada sobre una copia combinada con glosario_check.py.",
     "terms": T, "alias_agregar": ALIAS, "modificar": {}}
json.dump(P, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

dup = [t["id"] for t in T if t["id"] in by]
if dup:
    sys.exit(f"ids que ya existen en el glosario: {dup}")
names = {}
for t in g["terms"]:
    for n in [t["term"]] + t.get("aliases", []):
        names[n.lower()] = t["id"]
choque = [(n, t["id"], names[n.lower()]) for t in T for n in [t["term"]] + t["aliases"] if n.lower() in names]
if choque:
    sys.exit(f"términos o alias que ya usa otra entrada: {choque}")
n0 = len(g["terms"])
g["terms"] += T
for k, al in ALIAS.items():
    by[k]["aliases"] += [x for x in al if x not in by[k]["aliases"]]
os.makedirs(os.path.dirname(COMB), exist_ok=True)
json.dump(g, open(COMB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(P, ensure_ascii=False)
print("ok", OUT, len(T), "entradas;", "guiones largos:", "—" in s or "–" in s, "; glosario actual:", n0, "; combinado:", len(g["terms"]))
r = subprocess.run([sys.executable, "/home/claude/ies-training/tools/glosario_check.py", "bosch-incendio", "--glosario", COMB], capture_output=True, text=True)
print(r.stdout[-2500:], r.stderr, "exit", r.returncode)
