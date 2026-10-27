"""Genera /home/claude/ies-training/ilustraciones/bosch-incendio/manifest.json (figuras, pasos, conceptos, teoría y figuras de teoría).

Valida: anclas `after` únicas en el laboratorio publicado (fuera de bloques de código y en el paso correcto),
anclas de teoría únicas y fuera de títulos, 250 a 450 palabras de teoría, 2 a 4 conceptos y nada de guiones largos.
Las lecciones 6 y 16 no tienen pasos numerados en el laboratorio: llevan principal y teoría, sin figuras de paso.
"""
import json, re, sys

M = {}

# =====================================================================================  1
M["1"] = {
    "fig": {"file": "1.svg",
            "alt": "Mapa de la familia de centrales Bosch. Arriba, la generación AVENAR vigente: AVENAR panel 2000, con 6 módulos y hasta 4 lazos, que viene como kit en gabinete; AVENAR panel 8000, con 46 módulos y hasta 32 lazos, en riel y ampliable; AVENAR keypad 8000 (FPE-8000-FMR), que opera a distancia o hace de controlador redundante del 8000. Abajo, la generación anterior: FPA-5000, red de hasta 32 paneles y teclados, y FPA-1200, un panel con hasta 3 teclados remotos y sin controlador redundante. Una tarjeta aclara que todos hablan LSN. Dos notas: la licencia standard o premium viene grabada y no se cambia; el firmware 4.x es solo para redes 100 % AVENAR y con un FPA en la red todos corren el mismo 3.x.",
            "caption": "Modelo, licencia y firmware: las tres cosas que definen qué se puede ampliar."},
    "steps": [
        {"file": "1-paso1.svg", "step": 1, "after": "Leé la etiqueta del controlador",
         "alt": "Etiqueta de ejemplo FPE-2000-PPC con FPE-2000 subrayado como familia y tamaño y PPC subrayado en verde como licencia. Tabla de códigos: FPE-2000-SPC y FPE-8000-SPC son standard, FPE-2000-PPC y FPE-8000-PPC son premium, FPE-8000-FMR es el AVENAR keypad 8000. Notas: la licencia no se puede modificar, revocar ni transportar; premium agrega BMS, UGM-2040, evacuación por voz y, en el 2000, la red.",
         "caption": "SPC es standard y PPC es premium: lo que dice la etiqueta no se cambia en obra."},
        {"file": "1-paso2.svg", "step": 2, "after": "Tocá el logo de Bosch en la pantalla",
         "alt": "Esquema genérico del frente del controlador AVENAR: pantalla táctil con un recuadro marcado como logo para tocar y una ventana con la versión de firmware 4.8.1 de ejemplo; a la izquierda, 18 LED de estado; abajo, 6 botones fijos y 3 teclas de función. Notas: rojo es alarma, amarillo titilando es falla, amarillo fijo es algo deshabilitado y verde es normal; el controlador se apaga con su botón antes de quitar la alimentación.",
         "caption": "La versión exacta sale de la pantalla; los LED dicen el estado de un vistazo."},
        {"file": "1-paso3.svg", "step": 3, "after": "Contá los módulos del riel",
         "alt": "Riel de ejemplo con seis lugares: FPE-8000-BCM de baterías, dos LSN 1500 A y un LSN 0300 A numerados 1, 2 y 3 como lazos, un IOS 0020 A como otro módulo y un lugar libre. Abajo, la ficha completa: LSN 0300 A x 1, LSN 1500 A x 2, BCM x 1, otros IOS 0020 A; cada módulo LSN maneja un lazo o hasta dos ramales. Nota: en obra nueva desde el 02/05/2026 el módulo de baterías es el FPE-8000-BCM y no se mezcla con el BCM-0000-B.",
         "caption": "Cada módulo LSN es un lazo; el de baterías también va en la ficha."},
    ],
    "concepts": [
        {"name": "Licencia standard o premium",
         "para_que": "Bosch separa en el hardware lo que un panel puede hacer hacia afuera: integrarse con un BMS, depender de un panel jerárquico, manejar evacuación por voz o, en el 2000, trabajar en red. Así el precio acompaña al tipo de obra, pero la decisión queda fija desde la compra.",
         "como": "La licencia viene grabada en el controlador: SPC es standard y PPC es premium. Según el manual no se puede modificar, revocar ni transportar. Premium es obligatoria en cada panel que tenga que verse en el BMS. Por eso la licencia se releva antes de prometer cualquier integración.",
         "ejemplo": "Un hotel en Punta del Este pide ver las alarmas en su BMS. El panel es un FPE-2000-SPC: no hay código que lo resuelva, hay que cotizar un controlador premium. Mejor descubrirlo en el relevamiento que el día de la puesta en marcha."},
        {"name": "Ramas de firmware 3.x y 4.x",
         "para_que": "Los paneles en red tienen que hablar el mismo idioma. La rama 3.x sostiene las redes donde todavía hay un FPA; la 4.x trae las novedades, pero solo para redes donde todos los nodos son AVENAR.",
         "como": "Todos los paneles conectados corren la misma versión. La 3.x estuvo en mantenimiento hasta fines de 2025: desde entonces, con el panel en Ethernet, Bosch pide una evaluación de riesgo. La vigente en 4.x es la 4.8.1, de junio de 2026, y la 4.9 está anunciada para diciembre.",
         "ejemplo": "Un edificio en Pocitos con un FPA-5000 y dos AVENAR en red: los tres siguen en 3.x. Si el cliente quiere la 4.x, primero hay que pasar el FPA a controlador AVENAR."},
        {"name": "Reemplazo del controlador FPA por AVENAR",
         "para_que": "Permite modernizar una instalación FPA sin cambiar todo el gabinete ni los lazos, porque el campo LSN es el mismo.",
         "como": "Se cambia solo el controlador. Ojo con lo que cambia: el AVENAR no usa tarjetas de dirección, pide el riel corto PRS-0002-C, no trae RS232 integrado y no admite puerta frontal porque se recalienta. Con un BCM-0000-A no cumple EN 54-4.",
         "ejemplo": "Un depósito en Canelones con un FPA-5000 en red que queda en 3.x: cambiar ese controlador por uno AVENAR permite llevar toda la red a 4.x, si el resto del hardware acompaña."},
    ],
    "teoria_md": """### Un poco de historia

Bosch fabrica centrales de incendio modulares desde hace varias generaciones. La familia FPA, con el FPA-5000 para redes grandes y el FPA-1200 para sitios chicos, es la generación anterior. La actual es AVENAR: el panel 2000, que viene como kit, y el 8000, que se arma con módulos en riel. Las dos generaciones comparten lo más caro de la obra: el lazo LSN y los detectores.

Los firmwares cuentan esa transición. La rama 3.x es la que permite redes mixtas con FPA; Bosch la tuvo en modo mantenimiento entre enero de 2022 y diciembre de 2025, solo con arreglos críticos. Desde 2026, un panel 3.x conectado a Ethernet pide evaluación de riesgo. La rama 4.x es solo para redes AVENAR: la vigente es la 4.8.1, de junio de 2026.

Hay un dato de contexto útil: en diciembre de 2024 Bosch anunció la venta de su negocio de video, acceso, intrusión y comunicaciones a Triton, pero se quedó con incendio. Por eso los paneles siguen saliendo de Bosch Building Technologies.

### Cómo funciona

Tres cosas definen lo que un panel puede hacer. La primera es el modelo: el 2000 admite 6 módulos y hasta 4 lazos; el 8000, 46 módulos y hasta 32 lazos. La segunda es la licencia, grabada en el controlador: standard o premium. Premium habilita BMS, panel jerárquico UGM y evacuación por voz, y en el 2000 es la condición para trabajar en red. Un AVENAR 2000 standard queda en un panel con hasta 3 teclados remotos, igual que un FPA-1200.

La tercera es el firmware. En una red, todos los nodos tienen que tener la misma versión. Si hay al menos un FPA, toda la red queda en 3.x; si todos son AVENAR, conviene la última 4.x. Para salir de 3.x, se cambia el controlador FPA por uno AVENAR: el campo se conserva.

Por eso el relevamiento empieza por la etiqueta, la pantalla y el riel. Con modelo, licencia, firmware y módulos anotados, cualquier ampliación se cotiza sabiendo qué permite el equipo.""",
    "teoria_figs": [
        {"file": "1-t1.svg", "after": "todos los nodos tienen que tener la misma versión",
         "alt": "Animación en cuatro tiempos. 1: tres paneles AVENAR en red corren firmware 4.8.1. 2: se suma un FPA-5000 a la red y todos los nodos pasan a la misma versión 3.x. 3: la rama 3.x está fuera de mantenimiento desde 2026 y, con la red en Ethernet, aparece el aviso de evaluación de riesgo. 4: se cambia el controlador del FPA por uno AVENAR, el campo LSN se conserva y la red vuelve a 4.x.",
         "caption": "Un FPA en la red arrastra a todos a 3.x; cambiar su controlador libera la red."},
    ],
}

# =====================================================================================  2
M["2"] = {
    "fig": {"file": "2.svg",
            "alt": "Jerarquía de quién decide en una obra de incendio, de arriba hacia abajo, con una flecha que indica que más arriba manda más: autoridad (Bomberos, DNB, con el Decreto 372/023 y la IT-11 vigente de 2010 que remite a UNIT 962); proyecto firmado por el técnico registrado; normas de referencia EN 54 y NFPA 72; manual del fabricante; y este curso, que ayuda a entender pero no decide. Al costado, quién hace qué según el decreto: el técnico registrado redacta el proyecto, ingresa el trámite y verifica; la empresa registrada suministra, instala, pone en marcha y mantiene; el propietario responde por mantener. Al pie: si el proyecto y el manual no coinciden, se para y se consulta.",
            "caption": "Arriba manda la autoridad y el proyecto firmado; el manual y el curso explican."},
    "steps": [
        {"file": "2-paso2.svg", "step": 2, "after": "Completá la ficha:",
         "alt": "Línea de tiempo: 2010, IT-11 de Bomberos vigente que remite a UNIT 962; enero de 2024, Decreto 372/023 rige habilitaciones y registros; 31/07/2026, consulta pública del borrador de la nueva IT11; 2027, vigencia prevista. Recuadro con lo que pide la IT-11 vigente, entre otras cosas: 24 h de batería en reposo, 15 min en alarma, pulsador a no más de 30 m y preseñal de hasta 2 min en locales concurridos. Nota: los borradores en consulta no autorizan su uso hasta que entren en vigencia.",
         "caption": "En la ficha va el instructivo que rige hoy, no el borrador en consulta."},
        {"file": "2-paso3.svg", "step": 3, "after": "Si hay diferencias, anotalas",
         "alt": "Diagrama de decisión. El proyecto firmado dice subsuelo en ramal clase B y el manual Bosch recomienda lazo siempre que se pueda: ejemplo de obra. Si coinciden, seguís instalando con el proyecto como guía. Si no, parás: anotás la diferencia en la ficha, consultás al técnico registrado y él decide y lo deja por escrito. Nota: cambiar ubicación, cantidad o tipo de dispositivos respecto de lo certificado queda bajo responsabilidad de quien lo cambia.",
         "caption": "Ante una diferencia, la decisión vuelve al técnico registrado, por escrito."},
    ],
    "concepts": [
        {"name": "Técnico registrado y empresa registrada",
         "para_que": "El Decreto 372/023 separa responsabilidades para que cada decisión de seguridad de vida tenga un responsable identificado ante Bomberos. Antes de saber quién firma, no se sabe a quién consultar.",
         "como": "El técnico registrado redacta el proyecto, ingresa el trámite con declaración jurada y verifica las medidas. Los sistemas de detección los suministran, instalan, ponen en marcha y mantienen empresas registradas ante la DNB. El propietario responde por mantener. Hay multas de 10 a 200 UR para empresas.",
         "ejemplo": "En un edificio en obra en Pocitos, el plano marca un pulsador detrás de una puerta que ahora es un depósito. El técnico de campo no lo mueve: lo anota y llama al técnico registrado, que decide y deja constancia."},
        {"name": "IT-11 y su revisión",
         "para_que": "El instructivo técnico de Bomberos baja los criterios de diseño a números concretos, para que proyectista, instalador e inspector midan con la misma regla.",
         "como": "La IT-11 vigente es de 2010 y remite a UNIT 962. Pide, entre otras cosas, 24 h de batería en reposo, 15 min en alarma, pulsador a no más de 30 m y preseñal de hasta 2 min en locales concurridos. La DNB puso en consulta pública una nueva IT11 en julio de 2026, con vigencia prevista en 2027, y aclaró que el borrador no se usa hasta que rija.",
         "ejemplo": "Un proyectista cita en 2026 un criterio del borrador nuevo. Si no coincide con la IT-11 vigente, se anota en la ficha y se consulta: el borrador todavía no autoriza nada."},
        {"name": "EN 54 y NFPA 72 como referencia",
         "para_que": "Son las dos grandes familias de normas del sector: explican cómo se ensaya cada equipo y cuáles son las buenas prácticas, y por eso aparecen en manuales y hojas de datos.",
         "como": "EN 54 es una serie europea de normas de producto: EN 54-2 central, EN 54-4 fuente, EN 54-7 humo, EN 54-5 calor, EN 54-13 compatibilidad. NFPA 72 es el código estadounidense de alarma de incendio. En Uruguay explican, pero mandan el proyecto firmado y la autoridad.",
         "ejemplo": "La hoja del detector dice que cumple EN 54-7. Eso garantiza cómo responde al humo en ensayo, no que esté bien ubicado en ese pasillo: la ubicación es del proyecto."},
    ],
    "teoria_md": """### Un poco de historia

La normalización europea de detección de incendio empezó en los años setenta: según el registro de la serie, EN 54-1 y EN 54-5 salieron en 1976, preparadas por el comité CEN/TC 72. Con los años la serie creció hasta cubrir centrales, fuentes, detectores, pulsadores, sirenas, aisladores y compatibilidad. Muchas partes son normas armonizadas bajo el Reglamento de Productos de Construcción de la Unión Europea, y la serie se usa también fuera de Europa, en Latinoamérica incluida.

En Estados Unidos el equivalente es NFPA 72, el código de alarma de incendio y señalización, que se revisa por ediciones. La de 2013, por ejemplo, incorporó la preverificación de alarmas por la central de monitoreo.

En Uruguay manda Bomberos. La IT-11, el instructivo de detección y alarma, es del 17 de noviembre de 2010 y remite a UNIT 962. El Decreto 372/023, vigente desde enero de 2024, reglamentó las habilitaciones y los registros de técnicos y empresas. El 31 de julio de 2026 la DNB abrió la consulta pública de una nueva IT11, con vigencia prevista para 2027.

### Cómo funciona

Cada documento responde una pregunta distinta. EN 54 responde cómo se ensaya un equipo: la central bajo EN 54-2, la fuente bajo EN 54-4, el detector de humo bajo EN 54-7. Por eso una hoja de datos dice que un detector cumple EN 54-7, y eso no dice nada de dónde va.

Dónde va lo dice el proyecto. El técnico registrado lo redacta, lo firma e ingresa el trámite con declaración jurada. La empresa registrada suministra, instala, pone en marcha y mantiene. El propietario responde por mantener. Y la autoridad verifica.

El manual del fabricante explica cómo funciona y se instala el equipo, y el mismo manual de Bosch dice que las reglas de la autoridad local mandan sobre la planificación. Cuando el proyecto y el manual no coinciden, no hay que elegir: se para, se anota y se consulta al técnico registrado.""",
    "teoria_figs": [
        {"file": "2-t1.svg", "after": "El técnico registrado lo redacta, lo firma",
         "alt": "Animación en cuatro tiempos sobre una obra. 1: el técnico registrado firma el proyecto e ingresa el trámite ante la DNB con declaración jurada. 2: la empresa registrada suministra, instala y pone en marcha el sistema según el proyecto. 3: en obra aparece una diferencia con el proyecto; vuelve al técnico registrado, que decide por escrito. 4: con el sistema habilitado, el propietario mantiene con una empresa registrada.",
         "caption": "Cada decisión vuelve a quien firma: el técnico registrado."},
        {"file": "2-t2.webp", "after": "EN 54 responde cómo se ensaya un equipo",
         "alt": "Diagrama con la central en el centro, bajo EN 54-2, y su fuente bajo EN 54-4. Alrededor, cada pieza con su parte de la norma: detector de humo puntual EN 54-7, de calor puntual EN 54-5, multisensor de humo y calor EN 54-29, pulsador EN 54-11, aislador de cortocircuito EN 54-17 y sirena EN 54-3. Abajo, EN 54-13 para la compatibilidad entre componentes. Al pie: son normas de producto; dónde va cada equipo lo dice el proyecto.",
         "caption": "Una parte de EN 54 por cada tipo de equipo; la ubicación es del proyecto."},
    ],
}

# =====================================================================================  3
M["3"] = {
    "fig": {"file": "3.svg",
            "alt": "Un módulo de lazo, LSN 0300 A o LSN 1500 A, del que sale un par de cables a y b por LSN1, recorre detectores, un pulsador y una sirena, y vuelve por LSN2. Tres tarjetas al costado: LSN improved admite 254 elementos por módulo, pero con un solo elemento classic baja a 127 y sin derivaciones T-tap; el LSN 0300 A da hasta 300 mA y 1600 m de cable; el LSN 1500 A da hasta 1500 mA con elementos improved, 3000 m de cable y 300 mA si hay classic.",
            "caption": "Un par de cables, ida y vuelta, y los límites de cada módulo."},
    "steps": [
        {"file": "3-paso1.svg", "step": 1, "after": "cablealos en lazo",
         "alt": "Cableado de banco: el módulo LSN 0300 A con bornes LSN1 a− y b+ a la izquierda y LSN2 a− y b+ a la derecha. La línea b sale de LSN1 b+, entra al detector 1 por b1+, sale por b2+, sigue al detector 2 y al 3 de la misma forma y vuelve a LSN2 b+. La línea a sale de LSN1 a−, toca el borne a− de cada detector y vuelve a LSN2 a−. Cada detector FAP-425-O-R tiene sus perillas en 000. Notas: b atraviesa el aislador de cada elemento y a es común; con 000 el panel numera solo por orden de cable.",
         "caption": "b entra por b1+ y sale por b2+, con el aislador en el medio; a es común."},
        {"file": "3-paso3.svg", "step": 3, "after": "Desenergizá el lazo y cambiá las perillas",
         "alt": "Tres detectores, cada uno con sus tres perillas de centenas, decenas y unidades: el detector 1 en 0 0 1, el 2 en 0 0 2 y el 3 en 0 0 3. Tabla de modos: 0 0 0 es automático, de fábrica y sin T-tap; 001 a 254 es manual y permite T-tap; CL 0 0 es modo classic. Notas: se cambian con el lazo desenergizado y después se marca T-tap en RPS y se vuelve a autodetectar; más de 254 no está permitido y en un lazo no se mezcla automático con manual.",
         "caption": "Centenas, decenas y unidades: 001 a 254 es manual y habilita T-tap."},
    ],
    "concepts": [
        {"name": "LSN improved y classic",
         "para_que": "LSN es el bus de Bosch que lleva alimentación y datos a todo el campo por un solo par. La versión improved amplió lo que admitía la classic: más elementos por lazo y topologías con derivaciones.",
         "como": "Con elementos improved, un módulo admite 254 elementos. Si aparece un solo classic, el lazo entero baja a 127 y se pierden los T-tap. El LSN 0300 A da 300 mA y hasta 1600 m; el LSN 1500 A, hasta 1500 mA con improved y 3000 m.",
         "ejemplo": "En la ampliación de un shopping en Montevideo, alguien reutiliza un detector viejo classic en un lazo de 180 elementos improved. El lazo pasa a 127 y el panel no los acepta a todos: el relevamiento previo evita ese susto."},
        {"name": "Dirección automática o manual",
         "para_que": "La automática ahorra tiempo en un lazo simple; la manual da direcciones que no dependen del orden del cable y permite derivaciones.",
         "como": "Con las perillas en 000, el panel numera solo según el lugar en el cable. Con 001 a 254, cada elemento responde con la dirección que le pusiste y en RPS se marca T-tap, sea cual sea la topología. En un mismo lazo no se mezclan los dos modos.",
         "ejemplo": "En un edificio de oficinas en Ciudad Vieja, un lazo con derivaciones por piso se direcciona todo a mano, del 1 al 254, y cada dirección queda anotada en el plano."},
        {"name": "Blindaje del cable",
         "para_que": "El cable blindado protege la comunicación del lazo de interferencias. LSN improved admite cable blindado o no, pero si hay blindaje, mal conectado hace más daño que bien.",
         "como": "La tierra funcional va solo en el panel: dos puntos en un lazo, uno en un ramal. En cada equipo el blindaje se continúa, sin otras conexiones a tierra. El cable recomendado por Bosch es J-Y(St)Y 2x2x0,8 mm rojo.",
         "ejemplo": "En una planta industrial con variadores cerca de la bandeja, se usa cable blindado y se revisa que la malla no toque ninguna caja metálica en el recorrido."},
    ],
    "teoria_md": """### Un poco de historia

LSN significa Local Security Network: es el bus de campo de Bosch para incendio. La primera versión, hoy llamada LSN classic, admitía hasta 127 elementos por lazo. Después llegó LSN improved, que duplicó la capacidad a 254 elementos y sumó topologías con derivaciones. La compatibilidad hacia atrás se mantuvo: según la guía del AVENAR detector 4000, estos detectores pueden trabajar en modo classic en centrales viejas como BZ 500 LSN, UEZ 2000 LSN y UGM 2020, con los límites de esas centrales.

Desde la versión 1.0.35 del software del módulo LSN, los elementos classic e improved pueden convivir en el mismo lazo, con una condición: si hay uno solo classic, el lazo vuelve a 127 y no admite T-tap.

### Cómo funciona

El lazo es un par de cables, a y b, que sale del módulo por LSN1 y vuelve por LSN2. Por ese mismo par viajan la alimentación y los datos de cada elemento. La línea b atraviesa cada elemento entre sus bornes b1 y b2, donde está el aislador; la línea a es común.

Cada elemento necesita una dirección para que el panel sepa quién habla. Hay dos formas. Con las tres perillas en 000, el panel las asigna solo al autodetectar, recorriendo el cable: el primero que encuentra es el 1, el siguiente el 2, y así. Con las perillas en 001 a 254, cada elemento responde con la dirección que le pusiste, sin importar dónde está en el cable. La posición CL 0 0 lo pasa a modo classic.

La dirección manual es la que habilita los T-tap, las derivaciones en cualquier punto de la línea. En RPS se marca T-tap siempre que se use dirección manual, aunque el cableado sea un lazo simple. Lo que no se puede es mezclar: en un lazo, o todos automáticos o todos manuales del 1 al 254. Y nada de mallas: una derivación nunca vuelve a unirse con otra parte del lazo.""",
    "teoria_figs": [
        {"file": "3-t1.svg", "after": "el panel las asigna solo al autodetectar",
         "alt": "Animación en cuatro tiempos sobre un lazo con tres detectores. 1: el panel lanza la autodetección desde LSN1. 2: con perillas en 000, cada detector recibe la dirección según su lugar en el cable: 1, 2 y 3. 3: con perillas manuales, cada detector responde con la suya, 17, 4 y 9, sin importar el orden del cable. 4: aparece una derivación T-tap con un cuarto detector; solo es posible con dirección manual y T-tap marcado en RPS.",
         "caption": "Automático numera por orden de cable; manual respeta las perillas y permite T-tap."},
    ],
}

# =====================================================================================  4
M["4"] = {
    "fig": {"file": "4.svg",
            "alt": "Dos paneles comparados ante un corte del cable entre el elemento 2 y el 3. A la izquierda, un lazo, clase A o X por los aisladores: los elementos 1 y 2 quedan alimentados por LSN1 y los 3, 4 y 5 por LSN2; hay avería pero todos detectan. A la derecha, un ramal, clase B: los elementos 1 y 2 siguen, el 3 y el 4 quedan sin detección detrás del corte. Al pie: cada elemento LSN trae aislador entre b1 y b2 y el panel parte el lazo en dos; la clase la decide el proyecto y Bosch recomienda lazo siempre que se pueda.",
            "caption": "En lazo, un corte es una avería; en ramal, una zona sin detección."},
    "steps": [
        {"file": "4-paso2.svg", "step": 2, "after": "Desconectá un conductor entre",
         "alt": "Lazo de banco con el módulo LSN arriba y tres detectores. Un conductor desconectado entre el detector 1 y el 2, marcado con una cruz roja. El tramo del detector 1 queda resaltado como alimentado por LSN1 y el de los detectores 2 y 3 como alimentado por LSN2. Recuadro: en el panel aparece avería del lazo; anotá el mensaje tal cual. Nota: en modo revisión, con aerosol, los tres dan alarma porque el lazo se partió en dos ramales.",
         "caption": "Un corte parte el lazo en dos: cada mitad se alimenta desde un extremo."},
        {"file": "4-paso5.svg", "step": 5, "after": "Desconectá el retorno del lazo en el panel",
         "alt": "El mismo banco con el retorno desconectado en LSN2, así que el cableado es un ramal. Con el mismo corte entre el detector 1 y el 2, solo el detector 1 queda alimentado; el 2 y el 3 quedan sin alimentación. Resultado esperado del paso 6: lazo con corte, avería y 3 de 3 detectores activos; ramal con corte, avería y 1 de 3. Paso 7: volvé a cerrar el lazo y reponé; en obra real, abrir el lazo pide aviso al monitoreo.",
         "caption": "Sin retorno, el mismo corte deja dos detectores fuera."},
    ],
    "concepts": [
        {"name": "Aislador de cortocircuito",
         "para_que": "Un corto en un lazo sin aisladores tira abajo todo el lazo. El aislador encierra la falla entre los dos elementos más cercanos, para que el resto siga detectando.",
         "como": "Cada elemento LSN trae un aislador entre b1 y b2, por donde pasa la corriente del lazo. Ante un corto, los aisladores que rodean la falla se abren y el panel alimenta cada mitad desde su extremo. Para que funcione, la línea b tiene que entrar por b1 y salir por b2.",
         "ejemplo": "Un electricista engrampa el cable del lazo en el techo de un supermercado y lo pone en corto. El panel marca avería, aísla ese tramo y el resto del local sigue cubierto mientras se repara."},
        {"name": "Lazo, ramal y clases",
         "para_que": "La clase describe qué pasa con la detección ante una falla del cable, para que el proyecto elija cuánto riesgo acepta.",
         "como": "En la terminología de NFPA 72, clase B pierde lo que queda detrás de un corte; clase A vuelve al panel y sobrevive a un corte; clase X sobrevive además a un corto, gracias a los aisladores. NFPA no impone una clase: la elige el proyecto o la autoridad. Bosch recomienda lazo siempre que se pueda.",
         "ejemplo": "Un subsuelo de estacionamiento con un solo acceso de cable: el proyecto puede justificar un ramal. Si el resto del edificio también va en ramal sin justificación, es una pregunta para el técnico registrado."},
        {"name": "Límite de 512 por falla",
         "para_que": "Que una sola falla de componente no deje sin detección a una parte demasiado grande del edificio.",
         "como": "EN 54-2 fija que una falla no puede dejar fuera más de 512 detectores y pulsadores. Un panel con más de 512 pide controlador redundante; en el AVENAR 8000 puede ser otro controlador o un keypad 8000. La autoridad local puede exigir un tope menor.",
         "ejemplo": "Un hospital con 700 puntos en un AVENAR 8000: el proyecto suma un keypad 8000 como controlador redundante."},
    ],
    "teoria_md": """### Un poco de historia

Los primeros sistemas de detección cableaban cada zona como un ramal con una resistencia al final: si el cable se cortaba, todo lo que quedaba detrás se perdía y el panel solo podía avisar la falla. El lazo que vuelve al panel nació para dar un segundo camino. El paso siguiente fueron los aisladores de cortocircuito, que en Europa tienen su propia norma de producto, EN 54-17, publicada en 2005.

En la terminología de NFPA 72, esas tres ideas son tres clases: B pierde lo que queda detrás de un corte, A sobrevive a un corte porque vuelve al panel, y X sobrevive también a un corto gracias a los aisladores. La norma no dice cuál usar: lo decide el proyecto o la autoridad, y la clase B sigue siendo común en Estados Unidos.

### Cómo funciona

En un lazo LSN, cada elemento tiene un aislador entre b1 y b2, y la corriente del lazo pasa por adentro de cada uno. En operación normal, el módulo alimenta el lazo alternando desde LSN1 y desde LSN2: según el manual, el sentido de la corriente cambia cada 10 segundos.

Cuando aparece un corte o un corto, el panel parte el lazo en dos ramales: uno queda alimentado por LSN1 y el otro por LSN2. Los elementos afectados y la línea pasan a avería y empieza una reinicialización automática, pero cada elemento sano tiene su camino y sigue detectando. En un ramal no hay segundo camino: se pierde todo lo que está detrás de la falla.

Hay dos trampas. La primera es el ramal de un solo elemento conectado solo a b1: ese elemento toma corriente pero no la hace pasar por su aislador, así que no aísla. Entre dos elementos que sí aíslan queda una zona que cae entera ante un corto. La segunda es la malla: dentro de un lazo o un ramal está prohibida.

Encima de todo está el límite de EN 54-2: una falla no puede dejar fuera más de 512 detectores y pulsadores, y la autoridad local puede pedir un número menor.""",
    "teoria_figs": [
        {"file": "4-t1.svg", "after": "Cuando aparece un corte o un corto, el panel parte el lazo",
         "alt": "Animación en cuatro tiempos sobre un lazo con cinco elementos. 1: el módulo alimenta el lazo desde LSN1. 2: diez segundos después, alimenta desde LSN2; el sentido de la corriente se alterna. 3: aparece un corto entre el elemento 2 y el 3; los aisladores de esos dos elementos se abren. 4: el lazo queda partido en dos ramales, 1 y 2 alimentados por LSN1, 3, 4 y 5 por LSN2; todos siguen detectando y el panel muestra avería.",
         "caption": "Los aisladores encierran el corto y cada mitad se alimenta desde su extremo."},
        {"file": "4-t2.webp", "after": "La primera es el ramal de un solo elemento",
         "alt": "Línea LSN con dos elementos que aíslan en los extremos y tres detectores colgados en derivaciones de un solo elemento, conectados solo a b1. Un recuadro punteado ámbar marca la zona entre los dos aisladores: un corto adentro la tira entera. Notas: el elemento conectado solo a b1 toma corriente pero no la deja pasar por su aislador; las mallas están prohibidas y la autoridad puede limitar cuántos elementos caen por una falla.",
         "caption": "Entre dos aisladores, lo que no aísla cae junto ante un corto."},
    ],
}

# =====================================================================================  5
M["5"] = {
    "fig": {"file": "5.svg",
            "alt": "El módulo LSN entrega 30 V en sus bornes. Un par de cables de ida y vuelta, de 0,8 mm o 0,503 mm² de cobre, resta tensión en cada metro hasta un grupo de seis detectores dibujados juntos al final, el cálculo pesimista del manual; ahí tienen que llegar 15 V o más. Lista de lo que resta tensión: el largo del cable, la cantidad de elementos y su consumo, y las sirenas y módulos que consumen más. Recuadro de límites: 1600 m con LSN 0300 A, 3000 m con LSN 1500 A y como máximo 500 m de cable no aislado.",
            "caption": "Sale con 30 V y al último elemento le tienen que llegar al menos 15 V."},
    "steps": [
        {"file": "5-paso2.svg", "step": 2, "after": "Probá con L = 600 m",
         "alt": "Planilla resuelta para 600 m, 60 elementos y 0,5 mA: R cable igual a 2 por 600 por 0,0178 dividido 0,503, 42,5 ohm; R de equipos 60 por 0,35, 21 ohm; corriente total 60 por 0,0005 más 0,012 más 0,018, 0,060 A; caída 0,060 por 63,5, 3,8 V; quedan 26,2 V al final, más de 15 V. Notas: es la cuenta de banco del manual, siempre pesimista, y el cálculo de la obra se hace en Safety Systems Designer; con 2 mA por elemento quedan unos 20,5 V.",
         "caption": "Con 0,5 mA por elemento, al final del lazo quedan 26,2 V."},
        {"file": "5-paso4.svg", "step": 4, "after": "Buscá el largo donde la tensión final",
         "alt": "Gráfico de tensión al final del lazo contra largo de cable, de 0 a 1600 m, para 60 elementos. La recta de 0,5 mA baja de unos 29 V a unos 22 V en 1600 m sin cruzar los 15 V: manda el largo máximo del LSN 0300 A. La recta de 2 mA cruza la línea roja de 15 V en unos 1116 m: manda la tensión. Debajo de 15 V, zona de avería. Al pie: si la cuenta da más largo que el gráfico del manual, confiá en el gráfico y en SSD.",
         "caption": "Con 2 mA el lazo llega a 15 V cerca de los 1100 m; con 0,5 mA manda el largo máximo."},
    ],
    "concepts": [
        {"name": "Tensión mínima de 15 V",
         "para_que": "Cada elemento del lazo necesita una tensión mínima para funcionar y comunicarse. Por debajo, aparecen averías intermitentes que cuesta mucho diagnosticar en obra.",
         "como": "El módulo entrega 30 V en bornes y al último elemento tienen que llegarle 15 V o más. Lo que se pierde en el camino depende de la resistencia del cable, de cuántos elementos hay y de cuánto consume cada uno. El cálculo del manual pone todos los elementos al final, que es el peor caso.",
         "ejemplo": "Un lazo largo en un parque logístico funciona en reposo, pero al activar las sirenas aparecen averías de comunicación en los últimos detectores: la tensión cae debajo del mínimo cuando sube el consumo."},
        {"name": "Cable no aislado: 500 m",
         "para_que": "Hay tramos que cuelgan de un módulo sin pasar por un aislador: un corto ahí no lo encierra nadie. Limitar su largo total limita ese riesgo.",
         "como": "La suma de cable no aislado no puede pasar de 500 m. Cuentan las entradas de los módulos FLM (por ejemplo FLM-420-I2 o FLM-420-RLE-S), la línea NAC del FLM-420-NAC y los cables a indicadores remotos. No cuentan las líneas convencionales del FLM-420/4-CON ni las de contactos de relé.",
         "ejemplo": "Un local con muchos indicadores remotos en las puertas de habitaciones: se suman los metros de cada indicador y se verifica que el total no supere 500 m."},
        {"name": "Safety Systems Designer",
         "para_que": "La cuenta de banco sirve para detectar un lazo en el límite, pero no contempla la distribución real de los elementos ni todos los consumos. SSD hace el cálculo completo de largos, energía y cantidades.",
         "como": "Bosch exige SSD para planificar instalaciones AVENAR nuevas con zonas de energía (versión 3.6 o más). El resultado se guarda en la carpeta de obra junto con el plano.",
         "ejemplo": "Antes de tirar cable en un liceo, el cálculo de SSD muestra que un lazo de dos pisos conviene partirlo en dos módulos: se resuelve en el escritorio, no en el techo."},
    ],
    "teoria_md": """### Un poco de historia

La cuenta de este laboratorio es la ley de Ohm, que Georg Ohm publicó en 1827: la caída de tensión es la corriente por la resistencia. Lo que agrega el manual de Bosch son los parámetros del lazo LSN y unos gráficos para leer el largo máximo sin hacer cuentas. En 2026 Bosch sumó una exigencia: las instalaciones AVENAR nuevas se planifican con Safety Systems Designer, que hace este cálculo con los datos reales de cada elemento.

### Cómo funciona

El módulo entrega 30 V en sus bornes. La corriente que piden los elementos recorre el par de ida y de vuelta, y cada metro de cobre resta un poco de tensión. Además, cada elemento improved tiene una resistencia interna de 0,35 ohm en el camino, porque la corriente pasa por su aislador. Al último elemento tienen que llegarle al menos 15 V.

La cuenta del manual es pesimista a propósito: supone que todos los elementos están al final del cable. Con cable de 0,8 mm (0,503 mm²) y cobre de 0,0178 ohm mm²/m, la resistencia del cable es 2 x L x 0,0178 / 0,503. A la corriente de los elementos se le suman 0,012 A de transmisión y 0,018 A de destello. La caída es la corriente total por la resistencia total, y lo que queda es 30 menos esa caída.

Con 600 m y 60 elementos de 0,5 mA quedan unos 26 V. Si los elementos consumen 2 mA, porque hay sirenas y módulos, quedan unos 20 V. El consumo pesa tanto como el largo: con 2 mA, la tensión cruza los 15 V cerca de los 1100 m, mientras que con 0,5 mA manda el largo máximo del módulo, 1600 m con LSN 0300 A.

Los gráficos del manual dan referencias: 120 elementos de 0,5 mA llegan a unos 1950 m con LSN 1500 A, pero a 2 mA en 1000 m entran unos 73. Si tu cuenta da más largo que el gráfico, confiá en el gráfico y en SSD. Y aparte, la suma de cable no aislado no puede pasar de 500 m.""",
    "teoria_figs": [
        {"file": "5-t1.svg", "after": "La cuenta del manual es pesimista a propósito",
         "alt": "Animación en cuatro tiempos sobre un lazo de 600 m con 60 elementos al final. 1: el módulo entrega 30 V en sus bornes. 2: la corriente recorre la ida y la vuelta del cable y los 60 elementos; la tensión baja a lo largo del recorrido. 3: con 0,5 mA por elemento, al final llegan unos 26,2 V, dentro del margen. 4: con 2 mA por elemento, por sirenas y módulos, llegan unos 20,5 V; si además el cable se alarga, la tensión baja de 15 V y aparece avería.",
         "caption": "El consumo pesa tanto como el largo: con 2 mA el margen se achica rápido."},
    ],
}

# =====================================================================================  6
M["6"] = {
    "fig": {"file": "6.svg",
            "alt": "Selección del detector en tres pasos encadenados. 1, riesgo de fuego: fuego latente con humo, fuego rápido con llama o combustión con poco humo. 2, lo que no es fuego: vapor de ducha o cocina, polvo y aerosoles. 3, modelo y porqué: el detector que ve ese fuego, no confunde ese fenómeno y queda escrito en la tabla. Ejemplo del laboratorio: habitación de hotel, riesgo latente por tapizados, engañosos vapor y aerosol, detector FAP-425-DOTC-R, porque el CO rechaza el vapor. Notas: el firmware 4.8 es el último que soporta la serie 400; la línea vigente es AVENAR detector 4000 y un detector 5000 no aparece en las fuentes de Bosch.",
            "caption": "Primero el fuego que puede haber, después lo que lo imita, y el porqué por escrito."},
    "steps": [],
    "concepts": [
        {"name": "Selección en dos pasos",
         "para_que": "Elegir el detector por costumbre (óptico en todos lados) lleva a falsas alarmas o a detecciones tardías. Pensar primero el fuego y después los engañosos ordena la decisión.",
         "como": "Paso uno: qué fuego es probable en ese lugar, latente con humo, rápido con llama o con poco humo. Paso dos: qué fenómenos que no son fuego hay, como vapor, polvo, aerosoles o humo de cocina. El detector elegido y su porqué quedan escritos, porque el modo de un multisensor no se ve desde afuera.",
         "ejemplo": "En la cocina de un restaurante de Punta Carretas, el humo de cocción es rutina: un óptico daría falsas alarmas todos los días. La tabla deja escrito por qué ahí va otra cosa, y qué dice el proyecto."},
        {"name": "Óptico, térmico y CO",
         "para_que": "Cada sensor mira una huella distinta del fuego. Combinarlos permite detectar fuegos distintos y rechazar mejor lo que solo se parece.",
         "como": "El óptico mide la luz que dispersan las partículas de humo; el doble óptico usa un LED infrarrojo y uno azul para distinguir humo de polvo y vapor. El térmico dispara por máximo de 54 °C o 69 °C o por gradiente. El químico mide CO, y también reacciona a hidrógeno y monóxido de nitrógeno.",
         "ejemplo": "En un estacionamiento subterráneo, los gases de escape tienen CO: por eso la guía de Bosch trae un modo garaje, y por eso ahí se mira con lupa qué sensor dispara."},
        {"name": "Fin de soporte de la serie 400",
         "para_que": "Saber qué detectores quedan sin soporte evita una actualización de firmware que deje equipos instalados fuera de juego.",
         "como": "El firmware 4.8 es el último que soporta O400, OT400, OC410, OTC410, T400 y NEV300. Desde la cuenta 4.8, RPS ya no ofrece FAP-O500 ni FAP-OC500. Bosch pide planificar los reemplazos donde sigan instalados.",
         "ejemplo": "Antes de pasar un edificio a 4.9 cuando salga, se releva el lazo: si aparecen OT400, se cotiza el reemplazo por AVENAR detector 4000 antes de actualizar."},
    ],
    "teoria_md": """### Un poco de historia

La detección puntual se fue especializando con los años, y las normas lo muestran. En la serie EN 54, el detector de calor puntual es la parte 5 (vigente de 2017) y el de humo puntual la parte 7 (vigente de 2018). Los multisensores llegaron después y tienen sus propias partes: EN 54-29 para humo y calor, de 2015, y EN 54-26 para CO, también de 2015.

Bosch resume su línea vigente en AVENAR detector 4000: nueve variantes, del térmico FAH-425-T-R al multisensor FAP-425-DOTCO-R. Según el fabricante, sus algoritmos se entrenaron con más de 5000 patrones de fuegos reales. La línea anterior, la serie 400, se despide: el firmware 4.8 es el último que la soporta. Y conviene aclararlo: un AVENAR detector 5000 no aparece en ninguna fuente de Bosch.

### Cómo funciona

El óptico tiene una cámara oscura con un LED y un receptor que no se ven de frente. Cuando entra humo, las partículas dispersan la luz hacia el receptor. El doble óptico usa dos colores, infrarrojo y azul: comparando cuánto dispersa cada uno, estima el tamaño de las partículas y distingue humo de polvo y vapor.

El térmico mide temperatura. Puede disparar por máximo, a 54 °C o 69 °C según la clase, o por gradiente, cuando la temperatura sube rápido. El químico mide CO, que aparece temprano en fuegos latentes; la hoja de datos avisa que también reacciona a hidrógeno y monóxido de nitrógeno.

El multisensor combina las señales con un algoritmo, y eso le da estabilidad frente a fenómenos engañosos. La elección se hace en dos pasos: primero el riesgo de fuego del lugar, después lo que no es fuego. El ejemplo clásico de BS 5839-1 es la habitación de hotel con ducha: ópticos y multisensores ven el fuego latente, pero frente al vapor y al aerosol el que mejor queda es el de CO. Y en todos los detectores, la contaminación se reporta como avería, no como falsa alarma.""",
    "teoria_figs": [
        {"file": "6-t1.svg", "after": "El óptico tiene una cámara oscura con un LED",
         "alt": "Animación en cuatro tiempos con un multisensor y sus tres sensores. 1: el humo entra a la cámara óptica y las partículas dispersan la luz del LED hacia el receptor. 2: el calor sube y el térmico lo mide por máximo, 54 °C o 69 °C, o por gradiente. 3: el CO de un fuego latente llega a la celda química. 4: el algoritmo combina las tres señales y decide si es fuego; el vapor solo afecta al óptico y no alcanza.",
         "caption": "Cada sensor mira una huella del fuego; el multisensor las combina."},
        {"file": "6-t2.webp", "after": "El multisensor combina las señales con un algoritmo",
         "alt": "Tabla de las nueve variantes AVENAR detector 4000 con los sensores de cada una. FAH-425-T-R: térmico. FAP-425-O y FAP-425-O-R: óptico. FAP-425-DO-R: doble óptico. FAP-425-OT y FAP-425-OT-R: óptico y térmico. FAP-425-DOT-R: doble óptico y térmico. FAP-425-DOTC-R y FAP-425-DOTCO-R: doble óptico, térmico y químico, el DOTCO con celda de CO de 10 años. Al pie: -R indica perillas de dirección, el doble óptico usa LED infrarrojo y azul y todos traen aislador.",
         "caption": "Nueve variantes: la letra del modelo dice qué sensores trae."},
    ],
}

# =====================================================================================  7
M["7"] = {
    "fig": {"file": "7.svg",
            "alt": "Un lazo LSN del que cuelgan cinco elementos que no son detectores. Pulsador FMC-420RW: 1 punto. Sirena y baliza FNX-425U: 0 puntos, hasta 84 por lazo con detectores y 127 sin detectores. Módulo FLM-430-I2M1, con 2 entradas y 1 salida supervisada: 2 puntos. Módulo FLM-420/4-CON con una zona convencional de dos detectores que termina en un elemento de fin de línea. Módulo FLM-420-RLE-S para extinción, hasta 8 por lazo. Notas: cada entrada programada para dar alarma consume un punto; en EN 54-2 silenciar o reponer avisadores es manual.",
            "caption": "Pulsadores, sirenas y módulos van en el mismo lazo; las entradas de alarma suman puntos."},
    "steps": [
        {"file": "7-paso1.svg", "step": 1, "after": "Contá un punto por cada entrada",
         "alt": "Un módulo de ejemplo con 8 entradas: las entradas 1, 2 y 3 programadas como alarma suman un punto cada una; las 4 y 5 como falla técnica, la 6 como estado y las 7 y 8 sin usar suman cero. Tabla de una obra de ejemplo: 20 detectores, 20 puntos; 4 pulsadores, 4 puntos; 6 sirenas, 0 puntos; el módulo con 3 entradas de alarma, 3 puntos; total 27. Nota: una sirena avisa pero no da alarma, y un módulo de ocho entradas puede sumar hasta ocho.",
         "caption": "Suma un punto cada entrada programada como alarma; las sirenas no suman."},
        {"file": "7-paso2.svg", "step": 2, "after": "Marcá en rojo cada salida",
         "alt": "El panel AVENAR en el centro con sus salidas por reglas. En rojo, las que mueven algo físico: extinción por gas con FLM-420-RLE-S, retención de puertas, ascensores y ventilación, cada una con módulo de salida. En azul, las que avisan: sirenas y balizas, y transmisión al monitoreo. Al pie: rojo significa que mueve algo y necesita una forma documentada de aislarla antes de probar.",
         "caption": "Lo que mueve algo físico va en rojo y con su forma de aislarlo."},
    ],
    "concepts": [
        {"name": "Punto de alarma",
         "para_que": "El panel tiene límites de cuántos puntos maneja y de cuántos pueden caer por una falla. Contarlos bien evita quedarse corto a mitad de obra o necesitar redundancia sin haberla cotizado.",
         "como": "Cada elemento o entrada que puede dar alarma consume un punto. Una entrada de módulo cuenta como punto si en RPS se programa como alarma. Una sirena avisa pero no da alarma, así que no suma.",
         "ejemplo": "Un depósito con 30 sensores de flujo y presostatos conectados a módulos: si todos se programan como alarma, son 30 puntos más que el plano de detectores no mostraba."},
        {"name": "Fin de línea",
         "para_que": "Una línea con solo contactos o detectores convencionales no puede distinguir entre un cable cortado y una línea en reposo. El elemento de fin de línea hace que el reposo tenga una corriente conocida, y su falta se vuelve avería.",
         "como": "Las zonas convencionales del FLM-420/4-CON terminan en una resistencia o un módulo de fin de línea; las entradas supervisadas usan resistencias de fin de línea según la hoja del módulo. Para supervisión extendida, Bosch usa módulos como el FLM-420-EOL4W al final de un lazo o un ramal.",
         "ejemplo": "En la ampliación de un colegio se conectan detectores convencionales viejos a un FLM-420/4-CON. Si alguien olvida el fin de línea en la última caja, la zona queda en avería y es lo primero que hay que revisar."},
        {"name": "Silenciar es manual",
         "para_que": "Que una alarma real no quede callada por un temporizador mientras todavía hay gente adentro.",
         "como": "En EN 54-2, silenciar o reponer avisadores es una acción manual. Un temporizador de duración en salidas NAC solo vale para señales que no son EN 54. La sirena FNX-425U, desde el firmware 4.8.1, además reporta horas, batería y avería a NEXOSPACE.",
         "ejemplo": "Un cliente pide que las sirenas se corten solas a los cinco minutos. Para la alarma de incendio no corresponde; se le explica y, si quiere un aviso técnico temporizado, va por otra salida."},
    ],
    "teoria_md": """### Un poco de historia

La serie EN 54 tiene una parte para cada cosa que cuelga del lazo además de los detectores: los pulsadores en EN 54-11 (2001), las sirenas en EN 54-3 (vigente de 2014), las balizas en EN 54-23 (2010) y los módulos de entrada y salida en EN 54-18 (2005). Para extinción, Bosch se apoya en la interfaz VdS 2496 con su módulo FLM-420-RLE-S.

Las versiones de software también dejan historias. Según la hoja técnica de junio de 2026, RPS 5.14.17 y 5.15.27 borraban sin aviso la entrada de realimentación 5 del RLE-S al abrir configuraciones viejas. Por eso, con extinción en la obra, la versión de RPS importa.

### Cómo funciona

El lazo LSN no lleva solo detectores. Lleva pulsadores como el FMC-420RW, sirenas y balizas como la FNX-425U, que se alimenta del lazo, y módulos FLM que traducen el mundo de afuera al lazo: el FLM-430-I2M1 tiene 2 entradas y 1 salida supervisada, el FLM-430-I4R2 tiene 4 entradas y 2 relés, el FLM-420/4-CON conecta dos zonas convencionales, y el FLM-420-RLE-S maneja extinción, hasta 8 por lazo.

Las líneas que salen de un módulo hacia contactos o detectores convencionales se supervisan con un elemento de fin de línea. En reposo, por la línea circula una corriente conocida a través de esa resistencia. Si un detector convencional entra en alarma, la corriente sube; si el cable se corta, la corriente desaparece y el panel marca avería. Sin fin de línea, un cable cortado y una línea en reposo se verían iguales.

Cada entrada programada como alarma consume un punto del panel, y esos puntos cuentan para los límites y para la redundancia. Las sirenas no suman puntos, pero sí tienen su propio límite: hasta 84 FNX-425U por lazo si hay detectores, 127 si no.

Y una regla de EN 54-2 que se olvida: silenciar o reponer los avisadores es una acción manual. Un temporizador de duración solo vale para señales que no son EN 54.""",
    "teoria_figs": [
        {"file": "7-t1.svg", "after": "En reposo, por la línea circula una corriente conocida",
         "alt": "Animación en cuatro tiempos sobre una zona convencional de un FLM-420/4-CON con dos detectores y una resistencia de fin de línea. 1: en reposo circula una corriente chica a través del fin de línea y el módulo informa normal. 2: un detector entra en alarma y la corriente sube; el módulo informa alarma de la zona. 3: se repone y la corriente vuelve al valor de reposo. 4: se corta el cable antes del fin de línea, la corriente desaparece y el módulo informa avería.",
         "caption": "La corriente por el fin de línea dice si la zona está en reposo, en alarma o cortada."},
    ],
}

# =====================================================================================  8
M["8"] = {
    "fig": {"file": "8.svg",
            "alt": "Dos rieles de módulos, cada uno en su zona de energía. Zona 1: FPE-8000-BCM de baterías, ENO 0000 B y NZM 0002 A de alto consumo y un LSN 1500 A. Zona 2: FPE-8000-BCM y dos LSN 1500 A. Entre las zonas, el cable rojo entre rieles quitado para separarlas. Cada FPE-8000-BCM tiene sus baterías: si falla uno, o sus baterías, las otras zonas siguen. Recuadros: el orden en el riel pide al lado del BCM los módulos de alto consumo o sensibles (ENO 0000 B, CZM 0004 A, NZM 0002 A, RML 0008 A, IOS 0020 A, RMH 0002 A); en obra nueva desde el 02/05/2026, FPE-8000-BCM sin mezclar con BCM-0000-B, firmware 4.7.0 o más, RPS 5.14.17 o más y SSD 3.6 o más.",
            "caption": "Cada zona de energía con su BCM y sus baterías: si cae una, las otras siguen."},
    "steps": [
        {"file": "8-paso1.svg", "step": 1, "after": "Calculá las dos variantes",
         "alt": "Cálculo con corriente de reposo 0,6 A y de alarma 2,5 A. Variante A, guía NFPA 72: 0,6 por 24 más 2,5 por 5/60, por 1,20, da 17,5 Ah. Variante B, más exigente: 0,6 por 30 más 2,5 por 15/60, por 1,25, da 23,3 Ah. Barras comparativas donde casi todo es reposo con factor y una franja roja chica es la alarma, que es la que tiene que funcionar al final. Nota: redondeá hacia arriba a una capacidad comercial, anotá la variante del proyecto y rotulá las baterías con su fecha de fabricación.",
         "caption": "Misma fórmula, distinta exigencia: 17,5 Ah contra 23,3 Ah."},
        {"file": "8-paso3.svg", "step": 3, "after": "medí cada batería",
         "alt": "Dos baterías de 12 V en serie, de 24 a 28,2 V en total, y cada una entre 12,0 y 14,1 V en la puesta en marcha. Prueba 1, falta de red: se corta la alimentación de red, el panel sigue con baterías y avisa la falla. Prueba 2, falta de batería: con red presente se desconectan las baterías y el aviso puede demorar hasta 15 minutos. Nota: medir tensión no alcanza; la práctica es probar con carga, fechar por fabricación y contar con una vida típica de 3 a 5 años.",
         "caption": "Cada batería entre 12,0 y 14,1 V; el aviso de batería puede tardar 15 minutos."},
    ],
    "concepts": [
        {"name": "Zona de energía",
         "para_que": "Que la falla de una fuente o de sus baterías no apague todo el panel. Separar la energía en zonas limita lo que se pierde.",
         "como": "Desde el 02/05/2026, las instalaciones AVENAR nuevas usan FPE-8000-BCM y zonas de energía. Las zonas se separan quitando el cable rojo entre dos rieles largos, y los módulos de alto consumo o sensibles a la tensión van al lado del BCM. No se mezcla con BCM-0000-B en un panel; pide firmware 4.7.0, RPS 5.14.17 y SSD 3.6 o más.",
         "ejemplo": "Un AVENAR 8000 de un hospital con dos zonas de energía: una batería que se seca en la zona 2 da avería, pero los lazos de la zona 1 siguen alimentados."},
        {"name": "Cálculo de baterías con factor",
         "para_que": "La batería tiene que aguantar el reposo sin red y, al final, la alarma. El factor cubre el envejecimiento y la incertidumbre del cálculo.",
         "como": "Capacidad = (I reposo x horas de reposo + I alarma x tiempo de alarma) x factor. La guía sobre NFPA 72 usa 24 h, 5 min y 1,20; Security Sales usa 1,25; la IT-11 uruguaya de 2010 pide 15 min de alarma; RPS trae 30 h por defecto. Manda la norma que adopte el proyecto; ante la duda, la variante más exigente.",
         "ejemplo": "Con 0,6 A de reposo y 2,5 A de alarma, la variante NFPA da 17,5 Ah y la más exigente 23,3 Ah. Si el proyecto cita la IT-11, el tiempo de alarma es 15 minutos."},
        {"name": "Truco temporal de la TI 2739",
         "para_que": "Poder descargar una configuración mientras RPS tiene un error conocido, sin perder de vista que es un parche.",
         "como": "RPS valida la autonomía de cada zona con la corriente de alarma de los elementos LSN y marca sobrecorriente falsa donde hay muchas sirenas. Bosch propone bajar el reposo a 1 h y poner 26 Ah hasta la versión corregida, prevista para fin de 2026. Se deja escrito en la carpeta y en el panel, y se deshace después.",
         "ejemplo": "En un shopping con muchas sirenas por zona, RPS no deja descargar. Se aplica el truco, se rotula el panel con la fecha y la TI, y queda agendado volver a los valores reales."},
    ],
    "teoria_md": """### Un poco de historia

El cálculo de baterías es viejo y casi universal: reposo más alarma, por un factor. Lo que cambia según la norma es cuánto. La guía sobre NFPA 72 pide 24 horas de reposo y después 5 minutos de alarma, o 15 con evacuación por voz, con un factor de 1,20. La IT-11 uruguaya de 2010 pide 24 horas y 15 minutos de alarma. RPS cambió hace poco su valor por defecto de reposo de 24 a 30 horas.

En 2026 Bosch cambió la forma de alimentar el AVENAR. La hoja técnica 2716, del 8 de abril, lanzó el concepto de zonas de energía con el FPE-8000-BCM, obligatorio en obra nueva desde el 2 de mayo de 2026. Y la hoja 2739, de septiembre, reconoció un error de RPS en la validación de autonomía, con un truco temporal hasta la versión corregida.

### Cómo funciona

La batería tiene que aguantar dos momentos. Primero, el reposo: horas sin red alimentando el panel, los lazos y los módulos. Después, al final de ese tiempo, la alarma: sirenas y salidas activas durante los minutos que pida la norma. La fórmula es (I reposo x horas + I alarma x tiempo de alarma) x factor, y el factor cubre el envejecimiento: Security Sales recomienda 1,25 y fechar cada batería por su fabricación.

Con zonas de energía, el panel se divide en partes que tienen su propio FPE-8000-BCM y sus propias baterías. Se separan quitando el cable rojo entre dos rieles largos, y los módulos que consumen mucho o son sensibles a la tensión van pegados al BCM. Si falla un BCM o sus baterías, las otras zonas siguen funcionando.

SSD y RPS calculan el consumo de cada zona y verifican la capacidad, la carga y los tiempos. Ahí está el error conocido: RPS usa la corriente de alarma de los elementos LSN para validar el reposo y, en zonas con muchas sirenas, marca una sobrecorriente que no existe. El truco de Bosch, 1 hora de reposo y 26 Ah, permite descargar; después se vuelve a los valores reales.

En la puesta en marcha se mide cada batería y se prueban por separado la falta de red y la falta de batería.""",
    "teoria_figs": [
        {"file": "8-t1.svg", "after": "La batería tiene que aguantar dos momentos",
         "alt": "Animación en cuatro tiempos con un indicador de carga de batería. 1: con red presente, la fuente alimenta el panel y mantiene cargadas las baterías. 2: se corta la red y las baterías toman el reposo: 24 h según NFPA 72 y la IT-11, 30 h por defecto en RPS; la carga baja despacio. 3: al final del reposo llega la alarma: sirenas y salidas durante 5 min según NFPA o 15 min según la IT-11; la carga baja rápido. 4: lo que sobra es el margen del factor, 1,20 o 1,25, para el envejecimiento de la batería.",
         "caption": "Primero horas de reposo, después minutos de alarma, y el factor de margen."},
    ],
}

# =====================================================================================  9
M["9"] = {
    "fig": {"file": "9.svg",
            "alt": "Secuencia de puesta en marcha en tres bloques numerados del 1 al 11. En el panel: 1 alimentar, 2 calibrar la pantalla, 3 fecha, hora, PNA y red, 4 reiniciar. Con FSP-5000-RPS: 5 conectar por USB, 6 autodetección, 7 editar la configuración, 8 descargar. Cerrar: 9 walk test, 10 pruebas funcionales, 11 diagnóstico como acta. Notas: la versión vigente a octubre de 2026 es RPS 5.15.28 en Windows 11 24H2 de 64 bits, bajada de la extranet de Bosch; en un sitio ocupado, la descarga va con el monitoreo avisado y prueba funcional después.",
            "caption": "Panel, RPS y cierre: el orden de la puesta en marcha según el manual."},
    "steps": [
        {"file": "9-paso2.svg", "step": 2, "after": "Creá una configuración nueva",
         "alt": "Árbol de la configuración de práctica, de arriba abajo: versión de cuenta AVENAR panel 4.8; país Uruguay; nodo 1, AVENAR panel 2000 con PNA 1; riel, primera posición, LSN 0300 A; lazo con dirección manual y T-tap marcado; 10 detectores FAP-425-O-R en las direcciones 1 a 10. Notas: la cuenta 4.8 corresponde al firmware 4.8 y agrega Uruguay; con dirección manual se marca T-tap. Aclaración: son los datos del laboratorio, no una captura de RPS.",
         "caption": "Cuenta 4.8, país Uruguay, un nodo, un módulo y diez detectores en manual."},
        {"file": "9-paso3.svg", "step": 3, "after": "Corré el chequeo de consistencia",
         "alt": "Tres columnas del chequeo de consistencia. Errores, en rojo: se corrigen antes de descargar; la regla de obra es consistencia sin errores. Advertencias, en ámbar: se leen una por una y se anota por qué queda así. Pistas: novedad de RPS 5.15.27, ayudan a ubicar qué corregir. Notas: anotá cada uno tal cual aparece con el elemento al que se refiere; en el paso 4, guardá y exportá con la fecha en el nombre del archivo.",
         "caption": "Errores se corrigen, advertencias se deciden y las pistas ayudan a ubicarlos."},
    ],
    "concepts": [
        {"name": "FSP-5000-RPS y la cuenta de configuración",
         "para_que": "El panel hace lo que dice su configuración, y RPS es la herramienta que la arma, la valida y la descarga. La cuenta de configuración ata ese archivo a una versión de firmware.",
         "como": "RPS se baja de la extranet de Bosch con un usuario habilitado; la versión vigente a octubre de 2026 es la 5.15.28 y corre en Windows 11 24H2 de 64 bits. La cuenta 4.8 corresponde al firmware 4.8 y agrega Uruguay a los países. Bosch pide mandar firmware y RPS como el .zip completo, sin renombrar.",
         "ejemplo": "Un técnico abre en la oficina una configuración con una versión vieja de RPS y aparecen diferencias raras. Primero se alinea la versión de RPS con la del panel y la cuenta; después se edita."},
        {"name": "Set Panel Time antes de descargar",
         "para_que": "RPS compara la configuración con la del panel. Si la hora del panel no coincide, puede pedir una descarga completa aunque no haya cambios, y eso alarga y complica la intervención.",
         "como": "Antes de cada descarga se sincroniza la hora con Set Panel Time. El checklist completo: copia de la configuración del panel, Set Panel Time, chequeo de consistencia sin errores, descarga, walk test y pruebas, diagnóstico guardado como acta y copia final.",
         "ejemplo": "En un mantenimiento en Maldonado, el panel atrasaba varios minutos y RPS pidió descarga completa. Con la hora sincronizada, el siguiente cambio se descargó normal."},
        {"name": "De 3.x a 4.x en tres pasos",
         "para_que": "Pasar una red vieja a la rama vigente sin dejar nodos que no se entienden entre sí a mitad de camino.",
         "como": "Según la hoja técnica de junio de 2026: primero se sube la red a 3.5, después se cambian los nodos a AVENAR y recién entonces se sube a 4.x. Los paneles conectados tienen que quedar con la misma versión.",
         "ejemplo": "Una red de tres paneles en un complejo de viviendas: el plan de trabajo arma las tres etapas, con copia de configuración antes de cada una y aviso al monitoreo."},
    ],
    "teoria_md": """### Un poco de historia

FSP-5000-RPS (Remote Programming System) es el programa con el que se configuran los paneles FPA y AVENAR desde una laptop. Va de la mano del firmware: cada versión de panel tiene su cuenta de configuración. La cuenta 4.8 corresponde al firmware 4.8 y fue la que sumó Uruguay a la lista de países.

Las versiones recientes dejan marcas. RPS 5.15.27 trajo un chequeo de consistencia con pistas y ayuda en HTML. RPS 5.14.17 y 5.15.27 tenían un problema con el FLM-420-RLE-S, y la 5.15.28 figura como vigente en la hoja técnica de septiembre de 2026. Para pasar una red de la rama 3.x a la 4.x, Bosch indica tres pasos: subir a 3.5, cambiar los nodos a AVENAR y subir a 4.x.

### Cómo funciona

La puesta en marcha tiene un orden. En el panel: se alimenta, se calibra la pantalla, se cargan fecha, hora, número de nodo (PNA) y datos de red, y se reinicia. Con RPS: se conecta por USB, se autodetecta lo que hay en los lazos, se edita la configuración y se descarga. Y se cierra con el walk test, las pruebas funcionales y el archivo de diagnóstico guardado como acta.

La configuración se arma de arriba abajo: cuenta, país, nodos, módulos en su lugar del riel, lazos y elementos. Antes de descargar, el chequeo de consistencia revisa que todo cierre: los errores se corrigen, las advertencias se leen y se deciden, y las pistas ayudan a encontrar qué tocar.

Hay un detalle que ahorra tiempo: RPS compara lo que tiene con lo que hay en el panel, y si la hora del panel no coincide puede pedir una descarga completa aunque no haya cambios. Por eso el checklist de cada descarga empieza con una copia de la configuración del panel y Set Panel Time, y termina con una copia de la configuración final.

Una descarga cambia un sistema de seguridad de vida. En un sitio ocupado se hace con el monitoreo avisado y con prueba funcional después. Las rutas exactas de menú de cada opción están en la ayuda de RPS, que se baja de la extranet.""",
    "teoria_figs": [
        {"file": "9-t1.svg", "after": "RPS compara lo que tiene con lo que hay en el panel",
         "alt": "Animación en cuatro tiempos con una laptop con RPS y un panel. 1: antes de tocar, se guarda una copia de la configuración del panel. 2: la hora del panel difiere de la de la laptop; con Set Panel Time quedan iguales. 3: el chequeo de consistencia termina sin errores. 4: la descarga pasa al panel y se cierra con walk test, diagnóstico guardado como acta y copia final.",
         "caption": "Copia, hora, consistencia, descarga y acta: el orden de cada descarga."},
    ],
}

# =====================================================================================  10
M["10"] = {
    "fig": {"file": "10.svg",
            "alt": "Un detector FAP-425-O-R en el centro con dos direcciones. A la izquierda, la dirección física: su lugar en el lazo, módulo, lazo y elemento 17, que sale de las perillas o del orden de cable. A la derecha, la dirección lógica: grupo y subdirección, 3.4, que se elige en RPS sin repetir. Abajo, tres usos de la dirección lógica: el mensaje del panel muestra tipo, elemento, ubicación y 3.4; una integración por RS-232 ve línea.3.4; el técnico de mantenimiento busca 3.4 en el plano. Al pie: desde la cuenta 4.5 hay puntos de alarma, que deciden si hace falta redundancia, y puntos lógicos, 4096 en panel solo y 2048 por panel en red.",
            "caption": "La dirección física dice dónde está; la lógica, cómo lo ven todos."},
    "steps": [
        {"file": "10-paso2.svg", "step": 2, "after": "Marcá cada cruce con",
         "alt": "Matriz de causa y efecto del laboratorio, con causas detector grupo 3 con un equipo, con dos equipos, pulsador piso 3 y flujo de rociadores piso 3, y efectos sirenas del piso, retención de puertas, ventilación y transmisión. Todas las celdas vacías salvo un ejemplo: el pulsador activa las sirenas del piso. Leyenda de las tres marcas posibles: activa, no activa y solo en modo noche. Nota: la matriz es parte del proyecto y la firma el técnico responsable.",
         "caption": "Activa, no activa o solo en modo noche: tres marcas posibles por cruce."},
        {"file": "10-paso3.svg", "step": 3, "after": "Asigná direcciones lógicas sin repetir",
         "alt": "Cuatro grupos lógicos separados: grupo 3, subdirecciones 1 a 20, detectores del piso 3; grupo 30, subdirecciones 1 a 4, pulsadores del piso 3; grupo 300, entradas técnicas de flujo y presión; grupo propio para las teclas de función. Notas: si una tecla de función y un grupo de entradas comparten dirección, RPS puede no avisar; copiar y pegar detectores les da la siguiente subdirección del mismo grupo.",
         "caption": "Un grupo para cada cosa y ninguna dirección lógica repetida."},
    ],
    "concepts": [
        {"name": "Dirección lógica",
         "para_que": "La dirección física cambia si se recablea o se agrega un elemento; la lógica es el nombre estable que ven el operador, las integraciones y el técnico.",
         "como": "En RPS cada elemento recibe un grupo y una subdirección. El panel muestra en cada mensaje el tipo de mensaje, el tipo de elemento, la ubicación y la zona lógica con subdirección. Una integración por RS-232 ve los eventos como línea, grupo y subdirección.",
         "ejemplo": "El guardia de un edificio corporativo ve \"Alarma 3.4, sala de reuniones piso 3\" y el BMS muestra lo mismo: nadie tiene que traducir números de lazo."},
        {"name": "Matriz de causa y efecto",
         "para_que": "Deja por escrito qué hace el sistema ante cada evento antes de programarlo, para que la lógica sea revisable y se pueda firmar.",
         "como": "Filas con causas (detectores, pulsadores, entradas técnicas), columnas con efectos (sirenas, puertas, ventilación, transmisión) y en cada cruce una marca: activa, no activa o solo en modo noche. La define y firma el técnico responsable; después cada cruce se vuelve una regla en RPS.",
         "ejemplo": "En una torre de oficinas, la matriz dice que dos detectores del mismo piso liberan las puertas y uno solo no. Cuando el cliente pregunta por qué, la respuesta está firmada."},
        {"name": "Reglas, contadores y estados",
         "para_que": "Traducir la matriz a lo que el panel ejecuta: qué salida se activa, con qué condición y por cuánto.",
         "como": "RPS ofrece reglas por evento, reglas dependientes de estado, contadores y estados compuestos. Un contador permite, por ejemplo, actuar recién con dos detectores del mismo grupo. Cada regla lleva un nombre que se puede rastrear hasta su cruce de la matriz.",
         "ejemplo": "La regla \"P3 2 det puertas\" se lee y se encuentra en la matriz: grupo 3, dos equipos, retención de puertas."},
    ],
    "teoria_md": """### Un poco de historia

Durante años, los paneles Bosch contaron sus límites en puntos de detección. Desde la cuenta de configuración 4.5 la cuenta se partió en dos: puntos de alarma, que deciden si hace falta redundancia, y puntos lógicos, que tienen un tope por panel de 4096 si está solo y 2048 si está en red. La idea de dirección lógica viene de antes: los integradores que leen un FPA-5000 por RS-232 ya veían cada evento como línea, grupo y subdirección.

La hoja técnica de junio de 2026 sumó dos detalles prácticos: al copiar y pegar detectores, RPS les da la siguiente subdirección del mismo grupo; y si una tecla de función y un grupo de entradas comparten dirección, RPS puede no avisar.

### Cómo funciona

Cada elemento tiene dos direcciones. La física es su lugar en el lazo: la dan las perillas o el orden de cable. La lógica la elegís en RPS: un grupo y una subdirección, como 3.4. El panel muestra la lógica en cada mensaje, junto con el tipo de mensaje, el tipo de elemento y la ubicación, y las integraciones la heredan. Por eso la lógica es la llave de todo lo que viene después.

Las salidas no se programan elemento por elemento: se gobiernan con reglas. Una regla por evento reacciona cuando algo pasa, por ejemplo una alarma del grupo 3. Una regla dependiente de estado mira cómo están las cosas, por ejemplo si el panel está en modo noche. Los contadores cuentan cuántos elementos de un grupo están en alarma, y los estados compuestos combinan condiciones.

La matriz de causa y efecto ordena todo eso antes de abrir RPS. Cada fila es una causa, cada columna un efecto y cada cruce una decisión: activa, no activa o solo en modo noche. La matriz es parte del proyecto, la firma el técnico responsable, y cada cruce se traduce a una regla con un nombre que se pueda rastrear.

La disciplina que más ahorra: un grupo para cada tipo de cosa y ninguna dirección lógica repetida.""",
    "teoria_figs": [
        {"file": "10-t1.svg", "after": "Una regla por evento reacciona cuando algo pasa",
         "alt": "Animación en cuatro tiempos de causa a efecto. 1: el detector 3.4 entra en alarma y genera un evento. 2: la regla por evento del grupo 3 activa las sirenas del piso 3. 3: un segundo detector del grupo 3, el 3.7, entra en alarma; el contador del grupo llega a 2 y activa el efecto que la matriz define para dos equipos. 4: el mensaje del panel y el BMS muestran la misma dirección lógica, 3.4, con su ubicación.",
         "caption": "El evento dispara la regla; el contador espera al segundo detector."},
    ],
}

# =====================================================================================  11
M["11"] = {
    "fig": {"file": "11.svg",
            "alt": "Tabla con algunos lugares de instalación del FAP-425-DOTC-R según la guía de operación y la sensibilidad de cada sensor, dibujada como barras de uno a tres. Oficina fuera de horario: térmico alta, óptico alta, químico alta. Oficina con fumadores o sala de espera, marcada como de fábrica: térmico alta, óptico baja, químico baja. Oficina modo día: térmico baja, óptico media, químico alta. Garaje: térmico alta, óptico baja, químico baja. Cocina o restaurante en operación: térmico baja, óptico baja, químico baja. Nota: con el óptico en baja, el DOTC-R solo dispara si además del humo sube el CO o la temperatura.",
            "caption": "Elegir el lugar de instalación es elegir cuánto pesa cada sensor."},
    "steps": [
        {"file": "11-paso3.svg", "step": 3, "after": "Marcá los que quedaron en el modo de fábrica",
         "alt": "Tabla de detectores con dirección, modelo, lugar programado, si fue elegido o quedó de fábrica y ambiente real. Fila 3.1 resaltada: FAP-425-OT-R en oficina modo día, de fábrica, instalado en la cocina del piso, marcado como no coincide. Fila 3.2: FAP-425-DOTC-R en oficina con fumadores, de fábrica, en sala de espera. Fila 3.3: FAP-425-O-R en sensibilidad media, elegido, en oficina. Notas: el problema no es estar de fábrica sino que nadie lo decidió; valores de fábrica según la guía: OT y DOT en oficina modo día, DOTC en oficina con fumadores, ópticos en media y térmico en A2R.",
         "caption": "El de fábrica en un ambiente que no se le parece va a la lista."},
        {"file": "11-paso4.svg", "step": 4, "after": "anotá qué modo correspondería",
         "alt": "Comparación. Hoy: FAP-425-OT-R en oficina modo día en la cocina del piso, térmico baja (B) y óptico media; el vapor y el humo de cocina le llegan al óptico. Propuesta: cocina, casino o restaurante en operación; el OT queda solo con térmico máximo en B y el óptico no participa; se acuerda con el proyecto. Nota: cambiar el modo cambia la respuesta al fuego, se deja escrito y se prueba después.",
         "caption": "La propuesta sale de la guía y se acuerda con el proyecto antes de tocar."},
    ],
    "concepts": [
        {"name": "Lugar de instalación",
         "para_que": "Un mismo detector tiene que ser sensible en una oficina vacía de noche y tolerante en una cocina en servicio. El lugar de instalación ajusta eso sin cambiar el equipo.",
         "como": "En RPS se elige el lugar de instalación del FAP-425 y eso fija el campo característico: cómo pesa cada sensor. Valores de fábrica: OT y DOT en oficina modo día, DOTC en oficina con fumadores o sala de espera, ópticos en sensibilidad media y térmico en A2R.",
         "ejemplo": "En un hotel, las habitaciones y la cocina tienen el mismo modelo de multisensor, pero no el mismo lugar programado. La planilla de modos deja escrito cuál va en cada uno."},
        {"name": "Apagar sensores",
         "para_que": "Hay ambientes donde un sensor solo trae falsas alarmas. Los multisensores permiten dejarlo afuera y seguir protegiendo con el resto.",
         "como": "En OT, DOT y DOTC se puede pasar a solo óptico, solo térmico diferencial (A2R) o solo térmico máximo (A2S). El modo cocina en operación deja al OT como térmico. Algunas combinaciones del DOTC-R, como solo óptico u óptico y químico sin térmico, no cumplen EN 54-7.",
         "ejemplo": "Una cocina industrial en un frigorífico: el proyecto acepta el multisensor en modo térmico. Queda anotado que ahí el detector no ve humo."},
        {"name": "Multisensor contra óptico",
         "para_que": "El multisensor rechaza mejor las falsas alarmas; el costo es que espera más. Entender esa compensación evita tanto el óptico en todos lados como el multisensor en todos lados.",
         "como": "En el estudio de BRE, ante fuegos reales rindieron parecido; ante tostadas, vapor, polvo y aerosol, los multisensores dispararon más tarde. La FIA advierte que todo filtro demora la respuesta a un fuego real. El modo elegido se documenta con su porqué.",
         "ejemplo": "En un geriátrico, una demora de 40 segundos pesa más que una falsa alarma: la discusión va al proyecto, no se resuelve en obra."},
    ],
    "teoria_md": """### Un poco de historia

La pelea entre ópticos y multisensores se midió en laboratorio. En 2018, BRE publicó ensayos con 35 multisensores y 2 ópticos expuestos a fuegos de prueba y a fenómenos engañosos. Frente a fuegos reales, rindieron parecido. Frente a tostadas, vapor, polvo y aerosoles, los multisensores dispararon más tarde. En la prueba de la tostada, en promedio dispararon 40 segundos después que los ópticos, todavía un minuto antes de que la tostada prendiera fuego. El resumen de la misma investigación dice que, cuanto más sofisticado el multisensor, menos falsas alarmas, y que la respuesta al fuego depende sobre todo de la sensibilidad.

La FIA agrega la advertencia del otro lado: todo filtrado demora la respuesta a un fuego real.

### Cómo funciona

En los AVENAR detector 4000 no se programa una sensibilidad suelta: se elige un lugar de instalación, y eso fija cómo pesa cada sensor. En el DOTC-R, por ejemplo, oficina fuera de horario pone el térmico, el óptico y el químico en alta; oficina modo día baja el térmico a B, deja el óptico en media y el químico en alta; cocina en operación deja todo en baja.

El mecanismo que explica el rechazo al vapor está en una nota de la guía: cuando el óptico está en sensibilidad baja, el DOTC-R solo dispara si además del humo sube el CO o la temperatura. El vapor de una ducha tiene partículas que ve el óptico, pero no trae CO ni calor: el detector espera. Un fuego latente trae humo y CO juntos, y ahí sí dispara.

Los multisensores también permiten apagar sensores: solo óptico, solo térmico diferencial (A2R) o solo térmico máximo (A2S). En el OT, el modo cocina en operación deja solo el térmico máximo. Algunas combinaciones del DOTC-R no cumplen EN 54-7.

Como el modo no se ve desde afuera, se documenta. Ningún detector queda en el modo de fábrica sin que alguien lo haya decidido y escrito, y cualquier cambio se acuerda con el proyecto y se prueba.""",
    "teoria_figs": [
        {"file": "11-t1.svg", "after": "El mecanismo que explica el rechazo al vapor",
         "alt": "Animación en cuatro tiempos con un FAP-425-DOTC-R con el óptico en sensibilidad baja y tres indicadores: humo, CO y temperatura. 1: entra vapor de una ducha; sube la señal de humo, pero CO y temperatura no cambian. 2: el detector espera y no da alarma. 3: empieza un fuego latente; suben juntos el humo y el CO. 4: con humo más CO, el detector da alarma.",
         "caption": "Con el óptico en baja, el DOTC necesita humo más CO o calor para disparar."},
    ],
}

# =====================================================================================  12
M["12"] = {
    "fig": {"file": "12.svg",
            "alt": "Respuesta del mismo detector en dos modos. Modo día, hay gente para investigar: un detector da prealarma al personal, que investiga durante el tiempo que fija el proyecto; si confirma o vence el tiempo, alarma general. Modo noche, nadie investiga: un detector da alarma general y transmisión. Abajo, en rojo: el pulsador da alarma general inmediata de día y de noche y anula cualquier retardo. Al costado, tres teclas de función del panel, una marcada día y noche: una tecla programable o un horario pasa de día a noche o a sensibilidad alternativa.",
            "caption": "De día se investiga, de noche va directo; el pulsador nunca espera."},
    "steps": [
        {"file": "12-paso1.svg", "step": 1, "after": "Completá cada celda con la acción",
         "alt": "Tabla del laboratorio con evento, modo día y modo noche. Un detector: de día, prealarma y el personal investiga 3 minutos; de noche, alarma general más transmisión. Dos detectores y falla de red: vacías para completar. Un pulsador: alarma general inmediata en los dos modos, fila resaltada. Cambio de día a noche: tecla de función u horario. Notas: BS 5839-1 limita la alarma demorada a 6 minutos y el pulsador la anula; la IT-11 de 2010 admite preseñal de hasta 2 minutos en locales concurridos; la tabla la valida el técnico registrado antes de programarla.",
         "caption": "Lo completo es el ejemplo; lo vacío lo completás vos y lo valida el técnico."},
        {"file": "12-paso2.svg", "step": 2, "after": "Verificá: ningún retardo sobre pulsadores",
         "alt": "Tres tarjetas de control. En rojo: retardo sobre un pulsador, nunca, porque un pulsador es una persona que vio fuego. En rojo: retardo mayor al del proyecto, por ejemplo 5 minutos donde el proyecto dice 3. En verde: retardos solo donde el proyecto los admite, con el tiempo que firmó el técnico registrado. Nota: un retardo mal configurado demora la evacuación en un fuego real.",
         "caption": "Sin retardos en pulsadores y ninguno más largo que el del proyecto."},
    ],
    "concepts": [
        {"name": "Alarma demorada y prealarma",
         "para_que": "Reducir evacuaciones y despachos inútiles dando a personal entrenado un tiempo corto para ver qué pasa, sin abandonar la protección.",
         "como": "Un detector da una señal de alerta al personal y arranca un tiempo; si nadie confirma que es falsa, pasa a alarma general. BS 5839-1 limita la demora a 6 minutos y cualquier pulsador la anula al instante. La IT-11 de 2010 admite preseñal de hasta 2 minutos en locales concurridos. Solo con acuerdo de la autoridad y firma del técnico registrado.",
         "ejemplo": "En el patio de comidas de un shopping a las dos de la tarde, un detector salta por humo de una plancha: la brigada llega, verifica y repone antes de evacuar a miles de personas."},
        {"name": "Modo día y noche",
         "para_que": "La respuesta correcta depende de si hay alguien para investigar. De día hay personal; de noche, no.",
         "como": "El panel ofrece el estado de modo día entre las opciones de EN 54-2, y las teclas de función programables pasan de día a noche o a sensibilidad alternativa. El cambio puede ser por tecla o por horario, y queda en la tabla del proyecto.",
         "ejemplo": "Un local comercial: de 9 a 21 un detector da prealarma al encargado; de noche, el mismo detector da alarma general y transmite al monitoreo."},
        {"name": "Verificación del monitoreo",
         "para_que": "Es otra idea: que la central de monitoreo verifique antes de despachar a bomberos, para bajar salidas inútiles.",
         "como": "NFPA 72 la admite desde la edición 2013 solo si el departamento de bomberos la pide, con 90 segundos como máximo y aviso simultáneo al despacho. Es polémica: sus críticos temen demoras en un fuego real. No es lo mismo que un retardo programado en el panel.",
         "ejemplo": "Una empresa de monitoreo propone llamar al cliente antes de avisar a Bomberos. Eso no se configura en el panel: se acuerda por escrito con la autoridad y con el proyecto."},
    ],
    "teoria_md": """### Un poco de historia

El problema es viejo: casi todo el mundo vivió una falsa alarma y muy pocos un incendio, y cada evacuación inútil erosiona la confianza en el sistema. La FIA británica describe estrategias para responder mejor sin perder seguridad: alarma demorada para investigar, alarma confirmada por un segundo detector, prealarma, transmisión informada y día y noche. BS 5839-1 limita la demora a 6 minutos y deja que un pulsador la anule al instante.

En Estados Unidos, la edición 2013 de NFPA 72 sumó la preverificación por la central de monitoreo, solo si bomberos la pide y con 90 segundos como máximo. En Uruguay, la IT-11 de 2010 admite una preseñal de hasta 2 minutos en locales concurridos. Y la advertencia de la FIA vale para todas: todo filtrado demora la respuesta a un fuego real, y en residencias de cuidado no sirve.

### Cómo funciona

El AVENAR ofrece las opciones previstas en EN 54-2: retardo de transmisión, dependencia de más de una señal (los tipos A, B y C), contador de alarmas y estado de modo día. Con las teclas de función se pasa de día a noche o a una sensibilidad alternativa.

Una alarma demorada funciona así: un detector en alarma no dispara la evacuación general, sino una alerta al personal y un temporizador. Si alguien verifica que es una falsa alarma, repone. Si se confirma o se vence el tiempo, pasa a alarma general. Un pulsador corta todo: es una persona que vio fuego, y no se demora nunca.

El modo día y noche cambia esa lógica según haya o no gente para investigar. De noche, el primer detector va directo a alarma general y transmisión.

Las dependencias tienen un efecto en las pruebas: si un detector necesita a otro para dar alarma, se prueba fuera del modo revisión, y un óptico puede tardar hasta un minuto con aerosol aplicado en ráfagas.

Todo retardo sale del proyecto firmado y aceptado por la autoridad. Ninguno sobre pulsadores.""",
    "teoria_figs": [
        {"file": "12-t1.svg", "after": "Una alarma demorada funciona así",
         "alt": "Animación en cuatro tiempos en modo día. 1: un detector entra en alarma; el panel da prealarma al personal y arranca un temporizador de 3 minutos, el ejemplo del laboratorio. 2: el personal investiga mientras corre el tiempo. 3: el tiempo se vence sin confirmación de falsa alarma y pasa a alarma general. 4: en otro caso, alguien acciona un pulsador durante la demora y la alarma general es inmediata: el pulsador anula el retardo.",
         "caption": "La demora da tiempo a investigar; un pulsador la corta en el acto."},
    ],
}

# =====================================================================================  13
M["13"] = {
    "fig": {"file": "13.svg",
            "alt": "Red de incendio 192.168.1.x dentro de un recuadro punteado: paneles de las torres A, B y C con IP 192.168.1.1, .2 y .3 y PNA 1, 2 y 3, unidos en anillo Ethernet con RSTP; un servidor OPC 192.168.1.4, nodo 4, conectado por el switch del gabinete. La red del cliente con el BMS está afuera, en otra subred, y se conecta solo a través del servidor OPC. El acceso remoto va solo por el gateway seguro de Bosch, con IPsec UDP 500 y 4500 y subredes separadas. Notas: switches y conversores dentro de los gabinetes, puertos 25001 a 25008; en cada controlador los puertos 1 y 2 son para la red de paneles, el 3 para BMS, UGM o voz y el 4 para servicios remotos; hasta 32 nodos.",
            "caption": "La red de incendio va aparte; el BMS y el acceso remoto entran por puertas controladas."},
    "steps": [
        {"file": "13-paso2.svg", "step": 2, "after": "Verificá que el PNA de cada panel",
         "alt": "Tres tarjetas verdes iguales entre sí: en el panel, PNA 2; en la IP, 192.168.1.2, donde el último octeto es el nodo; en RPS, nodo 2. Debajo, en rojo, lo que no tiene que pasar: PNA 3 con IP 192.168.1.2 y nodo 2 en RPS; un número que no coincide es un panel que no aparece en la red o que choca con otro. Datos del ejemplo: gateway 192.168.1.254, multicast 239.192.0.1 y licencia premium en cada panel que tenga que verse en el BMS.",
         "caption": "PNA, último octeto y nodo en RPS: el mismo número en los tres lugares."},
        {"file": "13-paso3.svg", "step": 3, "after": "Marcá dónde van los conversores a fibra",
         "alt": "Dos gabinetes, torre A y torre B, cada uno con su panel y un conversor de medios adentro, unidos por fibra óptica de 180 m de ejemplo. Recuadro: por cobre, menos de 100 m de nodo a nodo; si no, conversor aprobado por Bosch y fibra. Nota: los switches RSTP externos y los conversores se instalan dentro del gabinete del panel; afuera la instalación no cumple EN 54.",
         "caption": "Más de 100 m entre nodos: conversor dentro de cada gabinete y fibra."},
    ],
    "concepts": [
        {"name": "Red de incendio dedicada",
         "para_que": "Que el tráfico, las fallas o un ataque en la red del cliente no afecten la comunicación entre paneles, y que el sistema cumpla EN 54.",
         "como": "La red de incendio es física y dedicada: switches y conversores aprobados, dentro de los gabinetes. La PC de servicio se desconecta de la red de incendio antes de conectarse a internet. Si Ethernet se usa solo para BMS, OPC o servicios remotos, se desactiva la comunicación panel a panel por TCP/IP en RPS.",
         "ejemplo": "En un edificio de tres torres, el cliente ofrece su red de datos para unir los paneles. La respuesta es no: se tiende cable o fibra propia entre gabinetes."},
        {"name": "Número de nodo (PNA)",
         "para_que": "Cada panel necesita una identidad única en la red, y que coincida en el panel, en la IP y en la configuración evita errores difíciles de rastrear.",
         "como": "La IP por defecto es 192.168.1.x, donde x es el número de nodo físico (PNA) cargado en el panel y en RPS. La red admite hasta 32 nodos entre paneles, teclados y servidores OPC, FSI, BACnet o UGM, y usa los puertos 25001 a 25008.",
         "ejemplo": "Un panel nuevo no aparece en la red. Revisando, tenía PNA 3 pero IP .2: dos nodos peleando por la misma identidad."},
        {"name": "BMS y acceso remoto",
         "para_que": "Mostrar el estado del sistema al BMS del edificio y dar soporte remoto sin abrir la red de incendio.",
         "como": "El BMS se conecta por OPC, FSI o BACnet, con licencia premium en cada panel visible. El acceso remoto va solo por el gateway seguro de Bosch, con IPsec (UDP 500 y 4500) y subredes separadas del router del cliente; las licencias son S, M o L según los puntos.",
         "ejemplo": "El administrador de un shopping quiere ver las alarmas en su BMS: se cotiza el servidor OPC y se verifica que cada panel sea premium antes de prometerlo."},
    ],
    "teoria_md": """### Un poco de historia

La red de paneles Bosch tiene dos caminos. Uno es CAN, el bus de campo que la propia Bosch presentó en 1986 para los autos y que hoy usan industrias enteras. El otro es Ethernet, con RSTP (Rapid Spanning Tree, IEEE 802.1w, de 2001) para armar anillos sin bucles. Con el tiempo, los paneles sumaron interfaces para el edificio: OPC, FSI y BACnet, el protocolo de automatización de edificios que ASHRAE publicó como norma 135 en 1995.

La guía de redes de 2025 resume las reglas actuales: hasta 32 nodos, red física dedicada, y switches y conversores dentro del gabinete para cumplir EN 54. En Alemania, VdS 2540 pide fibra en todos los tramos de datos.

### Cómo funciona

Cada controlador AVENAR trae cuatro puertos Ethernet con uso asignado: el 1 y el 2 para la red de paneles, el 3 para BMS, panel jerárquico o voz, y el 4 para servicios remotos. Con el 1 y el 2 se arma un anillo. RSTP deja un enlace del anillo bloqueado para que los mensajes no den vueltas para siempre; si se corta un cable, habilita ese enlace y la red sigue comunicada por el otro lado.

La dirección de cada nodo es el PNA, el número físico cargado en el panel. La IP por defecto es 192.168.1.x, con x igual al PNA, y la configuración en RPS usa el mismo número. Los paneles hablan por los puertos 25001 a 25008. Entre nodos, el cobre llega a menos de 100 m; más lejos, conversores aprobados y fibra.

La red de incendio no comparte switch con nada. El BMS entra por un servidor OPC, en otra subred, y si Ethernet se usa solo para eso, se desactiva la comunicación panel a panel por TCP/IP para no mandar datos de incendio sin querer. El acceso remoto pasa por el gateway seguro de Bosch, con IPsec por UDP 500 y 4500.

Y una regla de la red mixta que ya viste: todos los paneles conectados corren la misma versión de firmware.""",
    "teoria_figs": [
        {"file": "13-t1.svg", "after": "RSTP deja un enlace del anillo bloqueado",
         "alt": "Animación en cuatro tiempos sobre un anillo de tres paneles, A, B y C. 1: RSTP deja bloqueado el enlace entre C y A para que no haya bucle; los mensajes van de A a B y de B a C. 2: se corta el cable entre A y B. 3: RSTP habilita el enlace que estaba bloqueado y los mensajes de A llegan a B por C. 4: el panel avisa la falla de red y todos los nodos siguen comunicados.",
         "caption": "Con un corte, el anillo usa el enlace de reserva y la red sigue."},
    ],
}

# =====================================================================================  14
M["14"] = {
    "fig": {"file": "14.svg",
            "alt": "Tres columnas de una prueba. Antes: monitoreo avisado con empresa, hora y operador; responsable y ocupantes avisados; salidas deshabilitadas en el panel; extinción bloqueada por su empresa; zona en modo revisión. Durante: se prueba lo planificado, nada que mueva algo puede activarse y cada prueba con hora y resultado. Después: zona fuera de modo revisión, todas las salidas rehabilitadas, panel en reposo sin deshabilitados y monitoreo avisado del fin. Abajo: el LED amarillo fijo del panel indica algo deshabilitado y tiene que estar apagado antes de irte.",
            "caption": "Avisar y aislar antes, rehabilitar y avisar después: el LED amarillo fijo lo delata."},
    "steps": [
        {"file": "14-paso1.svg", "step": 1, "after": "Completá la lista de salidas reales",
         "alt": "Tabla de salidas con cómo se aíslan y quién lo hace. Transmisión al monitoreo: deshabilitar en el panel y avisar, vos con el operador. Sirenas si corresponde, retención de puertas, ventilación y ascensores: deshabilitar la salida, vos. Extinción por gas, fila resaltada: central de extinción bloqueada, su empresa. Notas: con gas, la prueba se coordina con la empresa de extinción y se anota nombre y hora; si hay una salida que no sabés cómo aislar, se resuelve antes de probar.",
         "caption": "Cada salida de la obra con su forma de aislarla y su responsable."},
    ],
    "concepts": [
        {"name": "Aviso al monitoreo y a los ocupantes",
         "para_que": "Que una prueba no termine en un despacho de bomberos, una evacuación o un susto. Quien recibe la señal tiene que saber que es una prueba.",
         "como": "Antes de cualquier prueba programada se avisa a la empresa de monitoreo y a los ocupantes, como pide NFPA 72 en la sección que cita la guía de Minnesota. Se anotan empresa, teléfono, hora y operador, y al terminar se avisa el fin con la misma precisión.",
         "ejemplo": "En un edificio de viviendas en el Centro, la prueba anual empieza con una llamada a la empresa de monitoreo y un cartel en el hall; termina con otra llamada y el cartel retirado."},
        {"name": "Aislar salidas",
         "para_que": "Un sistema de incendio no solo suena: libera puertas, manda ascensores, mueve ventilación, transmite y a veces dispara gas. Probar sin aislar es arriesgarse a activar todo eso de verdad.",
         "como": "Las salidas que mueven algo se deshabilitan en el panel o se bloquean en el equipo que comandan. La extinción por gas se prueba solo con su empresa y su central bloqueada; VdS 2496 pide además que una falla no pueda dejar fuera más de un área de extinción. Al final, todo se rehabilita y se verifica en el panel que no quede nada deshabilitado.",
         "ejemplo": "En un data center con extinción por gas, la empresa de extinción bloquea su central antes de empezar y firma la hoja con la hora. Recién ahí se pasa la zona a revisión."},
        {"name": "Prueba después de un cambio",
         "para_que": "Un cambio en la configuración puede afectar cosas que nadie tocó a propósito. Probar una muestra del resto lo detecta.",
         "como": "Según la guía de Minnesota sobre NFPA 72, tras un cambio en el software del sitio se prueba el 100 % de lo afectado y un 10 % de los iniciadores no afectados, hasta 50. Con 300 no afectados se prueban 30; con 800, el tope es 50.",
         "ejemplo": "Después de cambiar las reglas de un piso en una torre de oficinas, se prueba todo ese piso y una muestra de los demás, con la muestra anotada en el informe."},
    ],
    "teoria_md": """### Un poco de historia

Las guías de mantenimiento basadas en NFPA 72, como la que publica el Departamento de Salud de Minnesota, arrancan cualquier prueba por el mismo lugar: avisar a los ocupantes y a la empresa de monitoreo (la sección 14.2.3.1). La razón es práctica: cada prueba sin aviso puede terminar en un despacho de bomberos o en una evacuación.

El manual de Bosch agrega la otra mitad para la puesta en marcha: las salidas que comandan equipos de protección, como extinción, puertas o transmisión, se prueban una por una y a propósito. Para extinción, la interfaz VdS 2496 pide un diseño donde una falla no deje fuera más de un área de extinción: desde la segunda área hace falta un controlador redundante.

### Cómo funciona

Una prueba segura tiene tres tiempos. Antes, se avisa al monitoreo y a los ocupantes, se deshabilitan en el panel las salidas que mueven algo (transmisión, puertas, ascensores, ventilación) y la extinción por gas queda bloqueada en su propia central, por su empresa. Recién entonces la zona pasa a modo revisión.

Durante, se prueba lo planificado y se anota cada resultado con su hora. Nada que mueva algo puede activarse, porque está aislado.

Después, se saca la zona de revisión, se rehabilitan todas las salidas y se verifica en el panel que no quede nada deshabilitado. El panel ayuda: según el manual, un LED amarillo fijo indica una función deshabilitada. Ese LED apagado y el panel en reposo, sin averías nuevas, son la señal para avisar el fin al monitoreo.

El error más caro es el último: irse con una salida deshabilitada. El edificio queda sin transmisión o sin una función de seguridad y nadie lo nota hasta que hace falta.

Cuando la prueba sigue a un cambio de software, la muestra se agranda: 100 % de lo afectado y 10 % del resto de los iniciadores, hasta 50.""",
    "teoria_figs": [
        {"file": "14-t1.svg", "after": "Una prueba segura tiene tres tiempos",
         "alt": "Animación en cinco tiempos con un panel, sus salidas y el monitoreo. 1: se avisa al monitoreo y a los ocupantes. 2: se deshabilitan transmisión, puertas y ventilación y la extinción queda bloqueada por su empresa; se enciende el LED amarillo fijo. 3: se prueba un detector en modo revisión; da alarma y ninguna salida aislada se activa. 4: se rehabilitan todas las salidas y el LED amarillo fijo se apaga. 5: con el panel en reposo, se avisa el fin al monitoreo.",
         "caption": "Aislar, probar, rehabilitar: el LED amarillo fijo tiene que terminar apagado."},
        {"file": "14-t2.webp", "after": "Cuando la prueba sigue a un cambio de software",
         "alt": "Gráfico de la muestra de prueba después de un cambio de software. Con 300 iniciadores no afectados se prueban 30, el 10 %. Con 800 no afectados, el 10 % serían 80, pero el tope es 50. Recuadro: lo afectado por el cambio se prueba al 100 %. Nota: regla de la guía de Minnesota basada en NFPA 72; si el proyecto o la autoridad piden más, manda lo que pidan.",
         "caption": "Todo lo afectado y el 10 % del resto, con un tope de 50."},
    ],
}

# =====================================================================================  15
M["15"] = {
    "fig": {"file": "15.svg",
            "alt": "Cuatro formas de probar un detector, cada una con un detector y un cabezal de prueba. Modo revisión, óptico con aerosol, hasta 10 s: el detector se prepara solo para la prueba al pasar la zona a revisión. Walk test secuencial, multisensor un sensor por vez, hasta 20 s: aerosol, calor y en el DOTC gas de CO de 0,5 a 1 s. Walk test simultáneo, con herramienta multiestímulo, todos o nada: la alarma aparece solo si dispararon todos los sensores. Fuera de revisión, con dependencia de 2 detectores, hasta 1 min: aerosol en ráfagas, 1 s, se esperan 30 s y otra ráfaga. Al pie: el cabezal queda arriba hasta que dispare y cada prueba se anota.",
            "caption": "Cada prueba tiene su método y su tiempo de espera; se anotan los dos."},
    "steps": [
        {"file": "15-paso3.svg", "step": 3, "after": "Óptico: aerosol con el cabezal",
         "alt": "Un detector en el techo con el LED en alarma y, debajo, el cabezal con aerosol en una pértiga, que queda arriba hasta que dispare. Una escala de 0 a 10 segundos desde que se aplica: hasta 10 s, porque el aerosol tarda en distribuirse dentro de la cámara. Recuadro para anotar dirección 3.1, modelo FAP-425-O-R, modo revisión óptico, segundos, resultado y hora. Nota: antes, zona en modo revisión, monitoreo avisado y salidas aisladas, aunque sea en banco.",
         "caption": "El cabezal queda arriba hasta la alarma: con aerosol, hasta 10 segundos."},
        {"file": "15-paso4.svg", "step": 4, "after": "Multisensor, walk test secuencial",
         "alt": "Walk test secuencial en tres tarjetas encadenadas: 1, óptico con aerosol de prueba, hasta 20 s en multisensor; 2, térmico con herramienta de calor, anotá los segundos; 3, CO solo en el DOTC, gas de prueba de 0,5 a 1 s, anotá los segundos. Nota: en el FAP-425-OT-R del laboratorio hay dos sensores, óptico y térmico. Tabla para anotar dirección 3.2, modelo FAP-425-OT-R, sensor óptico y térmico, segundos y resultado.",
         "caption": "Un sensor por vez, cada uno con su estímulo y su tiempo anotado."},
    ],
    "concepts": [
        {"name": "Modo revisión",
         "para_que": "Los detectores AVENAR evalúan cómo evoluciona la señal en el tiempo, y un aerosol de prueba no se comporta como un fuego. El modo revisión los prepara para la prueba, para que respondan sin esperar como lo harían ante un fenómeno dudoso.",
         "como": "Se pasa la zona a modo revisión en el panel y el detector entra solo en operación de prueba. El cabezal queda arriba hasta que dispare: con aerosol, hasta 10 s. Al terminar, la zona sale de revisión, porque un detector en revisión no da alarma de fuego normal.",
         "ejemplo": "Un técnico apurado prueba sin revisión, el detector tarda y lo da por fallado. En revisión, el mismo detector responde en segundos: el método cambia el resultado."},
        {"name": "Walk test secuencial y simultáneo",
         "para_que": "Un multisensor tiene varios sensores, y una prueba solo con aerosol no dice si el térmico o el de CO funcionan.",
         "como": "En el secuencial se prueba un sensor por vez: aerosol, calor y, en el DOTC, gas de CO de 0,5 a 1 s; puede tardar hasta 20 s. En el simultáneo, una herramienta multiestímulo tipo Testifire estimula todos a la vez, y la alarma aparece solo si dispararon todos: si no aparece, uno falla.",
         "ejemplo": "En la recepción de un hotel, un DOTC pasa el aerosol pero no el gas de CO. La celda química está agotada: sin el secuencial, ese detector habría quedado como bueno."},
        {"name": "Prueba con dependencias",
         "para_que": "Cuando un detector necesita a otro para dar alarma, lo que se quiere ver es la lógica real, y eso se prueba fuera del modo revisión.",
         "como": "Fuera de revisión, un óptico puede tardar hasta 1 minuto con aerosol. La guía sugiere ráfagas: 1 segundo, esperar 30 y otra ráfaga. Los demás modelos se prueban con su estímulo térmico. Antes, como siempre, monitoreo avisado y salidas aisladas.",
         "ejemplo": "Una zona con dependencia de dos detectores en un depósito: se disparan dos detectores con ráfagas, se cronometra y se verifica que la regla activa lo que dice la matriz."},
    ],
    "teoria_md": """### Un poco de historia

Probar un detector parecía simple: aerosol y que suene. Pero los detectores actuales no reaccionan a un valor fijo: evalúan cómo evoluciona la señal, porque un fuego, un fenómeno engañoso y una prueba con aerosol tienen comportamientos distintos en el tiempo. Por eso la guía de operación del AVENAR detector 4000 pide pasar la zona a modo revisión antes de probar.

Las herramientas también evolucionaron. Para los multisensores existen herramientas multiestímulo, como Testifire, que generan humo, calor y CO a la vez. Para el lazo, la herramienta FME-420-LSN-TTL lee los elementos desde una PC, y en 2026 Bosch publicó un archivo nuevo para que reconozca elementos recientes como la FNX-425U, los FLM-430 y el DOTCO.

### Cómo funciona

En el panel, la zona pasa a modo revisión. El detector entra solo en operación de prueba y se prepara: ya no espera a confirmar la evolución de la señal como lo haría ante un fenómeno dudoso. Con el cabezal sobre el detector, el aerosol tarda en distribuirse dentro de la cámara: hasta 10 segundos en un óptico, hasta 20 en un multisensor.

Un multisensor tiene más de un sensor y cada uno se prueba. En el walk test secuencial va uno por vez: aerosol para el óptico, la herramienta de calor para el térmico y, en el DOTC, el gas de CO aplicado de medio segundo a un segundo. En el walk test simultáneo, la herramienta multiestímulo los activa a la vez, y el panel muestra alarma solo si dispararon todos. Si no aparece la alarma, un sensor está fallando.

Hay un caso que va fuera de revisión: cuando el detector depende de otro para dar alarma. Ahí se quiere ver la lógica real, y un óptico puede tardar hasta un minuto con aerosol aplicado en ráfagas.

Cada prueba se anota con método, segundos, resultado y hora. Y al terminar, la zona sale de revisión: un detector en revisión no da alarma de fuego normal.""",
    "teoria_figs": [
        {"file": "15-t1.svg", "after": "En el panel, la zona pasa a modo revisión",
         "alt": "Animación en cuatro tiempos con un panel y un multisensor. 1: fuera de revisión, el detector evalúa cómo evoluciona la señal y el aerosol de prueba no se parece a un fuego; el contador sigue sin alarma. 2: la zona pasa a modo revisión y el detector se prepara para la prueba. 3: aerosol con el cabezal y alarma en pocos segundos, dentro de los 10 s. 4: walk test simultáneo con un sensor que no responde: no aparece la alarma, y eso indica el sensor fallado.",
         "caption": "En revisión el detector se prepara; en simultáneo, sin todos los sensores no hay alarma."},
    ],
}

# =====================================================================================  16
M["16"] = {
    "fig": {"file": "16.svg",
            "alt": "Calendario de cinco años desde la obra con cinco filas de tareas. Bosch como mínimo, una vez por año: inspección visual y funcional, pantalla recalibrada y ventilaciones. NFPA 72 visual: semestral. NFPA 72 prueba: completa y anual. Sensibilidad de detectores: el primer año, a los dos años y luego hasta cada cinco. Hora del panel: en cada visita. Nota: en Uruguay el propietario mantiene y una empresa registrada hace el mantenimiento; las frecuencias las fija el proyecto y NFPA 72 se usa como referencia; lo que no está registrado no se hizo.",
            "caption": "Cada tarea con su frecuencia, y cada visita con su registro."},
    "steps": [],
    "concepts": [
        {"name": "Frecuencias de mantenimiento",
         "para_que": "Un sistema que pasó la habilitación se degrada: polvo, baterías, cambios en el edificio. Un calendario fijo encuentra los problemas antes que un incendio.",
         "como": "Bosch pide como mínimo una inspección visual y funcional por año, recalibrar la pantalla táctil una vez por año y mantener libres las ventilaciones. Como referencia, NFPA 72 pide inspección visual semestral, prueba completa anual y sensibilidad de detectores dentro del primer año, a los dos y luego hasta cada cinco. En Uruguay, las frecuencias las fija el proyecto.",
         "ejemplo": "Un contrato de mantenimiento de un colegio en Montevideo arma su calendario con lo que pide el proyecto y suma la revisión de hora del panel en cada visita."},
        {"name": "Valor óptico de contaminación",
         "para_que": "Saber cuándo un detector está sucio antes de que dé problemas. El polvo cambia la lectura del óptico, y el AVENAR lo convierte en un número.",
         "como": "En el diagnóstico del FAP-425: de 0 a 170 es un detector nuevo, hasta 350 normal, de 350 a 450 conviene cambiarlo pronto, de 450 a 510 cambiarlo ya, y arriba de 511 el sensor óptico queda desactivado. La contaminación se informa como avería, no como falsa alarma.",
         "ejemplo": "En la visita a un depósito con polvo, dos detectores marcan 470: se cambian en la visita o quedan como pendiente urgente en el informe, con la firma del responsable."},
        {"name": "Hora del panel y registros",
         "para_que": "El historial del panel es la evidencia de lo que pasó. Si la hora está corrida, los eventos no coinciden con el monitoreo ni con lo que cuenta el cliente.",
         "como": "El firmware 4.8 bajó el desvío del reloj de hasta 80 a 10 minutos por año, y Bosch sugiere revisarlo en cada mantenimiento con Set Panel Time. El historial guarda 10000 mensajes. El informe de cada visita deja hora, firmware, baterías, valores ópticos, pruebas y firmas.",
         "ejemplo": "Una alarma nocturna en un local: el monitoreo la tiene a las 03:12 y el panel a las 02:40. Con el reloj corregido en cada visita, esas discusiones se terminan."},
    ],
    "teoria_md": """### Un poco de historia

El mantenimiento de un sistema de incendio se ordenó alrededor de una idea simple: lo que no está registrado no se hizo. NFPA 72, en la guía de Minnesota, pide inspección visual semestral, prueba completa anual y un registro de terminación junto a la central con cada cambio. Para la sensibilidad de los detectores, la referencia es dentro del primer año, a los dos años y después hasta cada cinco, con registro de falsas alarmas.

Bosch fue sumando ayudas. El firmware 4.8 bajó el desvío del reloj del panel de hasta 80 minutos por año a 10, y Bosch sugiere revisarlo en cada mantenimiento. Los detectores AVENAR informan su valor de contaminación, sus horas de funcionamiento y su número de serie, cuya primera cifra indica el año de fabricación. Y con NEXOSPACE se sumó un autotest remoto que complementa, pero no reemplaza, lo que pida el proyecto.

### Cómo funciona

En Uruguay, el propietario mantiene y una empresa registrada hace el mantenimiento; las frecuencias las fija el proyecto. Bosch pide como mínimo una inspección visual y funcional por año, recalibrar la pantalla táctil anualmente y mantener libres las ventilaciones del gabinete.

En cada visita, el panel da datos que ningún tester da. El valor óptico de cada FAP-425 dice cuánto se ensució la cámara: de 0 a 170 es nuevo, hasta 350 normal, de 350 a 450 hay que cambiarlo pronto, de 450 a 510 cambiarlo ya, y arriba de 511 el sensor óptico se desactiva. Un detector sucio se informa como avería, no como falsa alarma.

La hora importa más de lo que parece. El historial guarda 10000 mensajes, y si el reloj está corrido los eventos no coinciden con los del monitoreo. Por eso el informe registra la hora antes de corregirla con Set Panel Time.

El informe completo deja sitio, fecha, técnico y empresa registrada, aviso al monitoreo, hora del panel, firmware y versión de RPS, tensión y fecha de las baterías, pruebas de red y batería, valores ópticos, pruebas de pulsadores, sirenas y salidas, y la confirmación de que todo quedó rehabilitado. Con las firmas del técnico y del responsable del sitio.""",
    "teoria_figs": [
        {"file": "16-t1.svg", "after": "La hora importa más de lo que parece",
         "alt": "Animación en cuatro tiempos con dos relojes, el real y el del panel. 1: con firmware anterior a 4.8, en un año el reloj del panel se puede correr hasta 80 minutos. 2: un evento de las 03:12 queda registrado en el panel con otra hora y no coincide con el monitoreo. 3: con firmware 4.8 el desvío baja a 10 minutos por año. 4: en cada visita, Set Panel Time vuelve a poner los relojes iguales y el informe registra la hora antes y después.",
         "caption": "Un reloj corrido desordena el historial; se corrige en cada visita."},
        {"file": "16-t2.webp", "after": "El valor óptico de cada FAP-425 dice cuánto se ensució",
         "alt": "Escala del valor óptico del FAP-425 en cinco tramos, no a escala: 0 a 170, nuevo; hasta 350, normal; 350 a 450, cambiar pronto; 450 a 510, cambiar ya; más de 511, sensor desactivado. Un ejemplo de 470 cae en cambiar ya, en esa misma visita. Nota: arriba de 450 se reemplaza en la visita o queda documentado como pendiente urgente; la contaminación se informa como avería, no como falsa alarma.",
         "caption": "El número de diagnóstico dice si el detector sigue, se cambia pronto o se cambia ya."},
    ],
}

# ===================================================================================== validación
OUT = "/home/claude/ies-training/ilustraciones/bosch-incendio/manifest.json"
pub = json.load(open("/home/claude/ies-training/site2/data/bosch-incendio.json", encoding="utf-8"))
labs = {str(l["id"]): l["lab"]["md"] for l in pub["lessons"]}
NUM = re.compile(r"^(\d+)\.\s")
err = []


def lab_lines(md):
    fence, step, out = False, 0, []
    for ln in md.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence; continue
        m = NUM.match(ln)
        if not fence and m:
            step = int(m.group(1))
        out.append((fence, step, ln))
    return out


for lid, m in M.items():
    s = json.dumps(m, ensure_ascii=False)
    if "—" in s or "–" in s:
        err.append(f"{lid}: guion largo")
    n = len(m["concepts"])
    if not 2 <= n <= 4:
        err.append(f"{lid}: {n} conceptos")
    th = m["teoria_md"]
    w = len(re.sub(r"[#`*]", "", th).split())
    if not 250 <= w <= 450:
        err.append(f"{lid}: teoría con {w} palabras")
    if "### Un poco de historia" not in th or "### Cómo funciona" not in th:
        err.append(f"{lid}: faltan subtítulos")
    ll = lab_lines(labs[lid])
    for st in m["steps"]:
        a = st["after"]
        hits = [(f, sp) for f, sp, ln in ll if a in ln]
        if len(hits) != 1 or hits[0][0] or hits[0][1] != st["step"] or labs[lid].count(a) != 1 or not 15 <= len(a) <= 45:
            err.append(f"{lid}: ancla de paso {st['file']} mal: {hits}")
        if not st["file"].startswith(f"{lid}-paso{st['step']}."):
            err.append(f"{lid}: nombre {st['file']}")
    tf_files = [tf["file"] for tf in m.get("teoria_figs", [])]
    if not 1 <= len(tf_files) <= 2 or not any(f.endswith(".svg") for f in tf_files):
        err.append(f"{lid}: teoria_figs {tf_files}")
    for tf in m.get("teoria_figs", []):
        a = tf["after"]
        if th.count(a) != 1 or not 15 <= len(a) <= 60:
            err.append(f"{lid}: ancla de teoría {a!r} aparece {th.count(a)} veces o largo {len(a)}")
        par = [p for p in th.split("\n\n") if a in p]
        if par and par[0].startswith("#"):
            err.append(f"{lid}: ancla de teoría en un título")
    print(lid, "palabras", w, "conceptos", n, "pasos", [x["step"] for x in m["steps"]], "teoría", tf_files)

json.dump(M, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", OUT, len(M))
if err:
    print("\n".join(err)); sys.exit(1)
