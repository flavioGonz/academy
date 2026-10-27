# Plan de lecciones: Detección de incendio Bosch, AVENAR y paneles modulares

Nivel: inicial a intermedio. Público: técnicos instaladores y de soporte de IES. 16 lecciones en 4 arcos de 4 (el pedido admite 12 a 16 en 3 o 4 partes; el temario pedido no entra en 12 sin mezclar temas de seguridad de vida). Fuentes: 28 páginas en raw/web. Los conteos salen de research/agreement-map.md.

Versiones a octubre de 2026: firmware de panel AVENAR 4.8.1 (junio 2026; 4.9 anunciada para diciembre), FSP-5000-RPS 5.15.28, cuenta de configuración 4.8 (agrega Uruguay como país). El fabricante es Bosch Building Technologies (Life Safety Systems): Bosch vendió video, acceso, intrusión y comunicaciones a Triton (hoy Keenfinity) pero se quedó con incendio.

Regla transversal: en cada lección de seguridad de vida se dice que la norma local, la autoridad (DNB) y el proyecto firmado por el técnico registrado mandan sobre lo que diga el curso o el manual.

## Arco 1. Conocer el sistema (lecciones 1 a 4)
Por qué este arco: antes de tocar una central hay que saber qué familia es, quién manda en el diseño y cómo se comporta el lazo ante una falla. Termina con un lazo LSN entendido de punta a punta.

### 1. Mapa AVENAR
- 3 de 3 fuentes (TH01, TH02, TH03).
- Idea: AVENAR panel 2000 (hasta 4 lazos) y 8000 (hasta 32), keypad 8000; FPA-5000 y FPA-1200 son la generación anterior. La licencia standard o premium viene grabada y define red e integraciones. Firmware 4.x solo para redes AVENAR; 3.x para redes con FPA.
- Historia: la licencia "no se puede modificar, revocar ni transportar" (https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf). Bosch retuvo incendio al vender el resto (https://www.securityinfowatch.com/industry-news/article/55249385/bosch-sells-security-and-communications-technology-business-to-triton-partners).
- Laboratorio: Admin, 10 min. Relevar un panel: modelo, licencia, firmware, módulos.
- Regla: antes de cotizar una ampliación, licencia y firmware de cada panel.

### 2. Quién manda
- 4 de 4 fuentes (TH04, TH05, TH06).
- Idea: Decreto 372/023: técnico registrado firma y gestiona; empresas registradas instalan y mantienen. IT-11 de 2010 vigente con revisión en consulta pública para 2027. EN 54 y NFPA 72 son referencias, no reemplazan lo que exige la DNB y el proyecto.
- Historia: el comunicado de la DNB del 31/07/2026 (https://www.gub.uy/ministerio-interior/comunicacion/noticias/comunicado-tecnicos-registrados-ciudadania-general).
- Laboratorio: Admin, 15 min. Armar la ficha normativa de una obra.
- Regla: si el proyecto firmado y el manual no coinciden, se para y se consulta al técnico registrado.

### 3. Lazo LSN
- 2 de 2 fuentes (TH07, TH08).
- Idea: 254 elementos improved por lazo o 127 si hay uno classic; 000 automático, 001 a 254 manual con T-tap marcado en RPS.
- Historia: la tabla de llaves rotativas del System manual.
- Laboratorio: Foco, 15 min. Direccionar tres detectores y leer el lazo.
- Regla: lazo con T-tap, todo manual y anotado en plano.

### 4. Lazo cerrado
- 3 de 3 fuentes (TH09, TH10, TH11).
- Idea: aislador en cada elemento; el lazo sobrevive a un corte o corto; el ramal no. Ramales de un elemento y mallas rompen el aislamiento. Más de 512 puntos de alarma por panel pide redundancia.
- División: Bosch recomienda lazo; NFPA no impone clase y la B es común (https://open-exam-prep.com/study-guides/cfps-fire/detection-and-alarm/fire-alarm-system-fundamentals).
- Laboratorio: Foco, 15 min. Abrir el lazo en banco y ver la falla y la recuperación.
- Regla: lazo siempre que se pueda; ramal solo si el proyecto lo justifica.

## Arco 2. Diseñar el campo (lecciones 5 a 8)
Por qué este arco: con el sistema entendido, se elige qué va en cada lugar y se asegura que tenga tensión y batería. Termina con un lazo calculado y una autonomía defendible.

### 5. Quince voltios
- 1 de 1 fuente, evidencia escasa pero primaria (TH12, TH13, TH14).
- Idea: 30 V en bornes, 15 V mínimo al final; 1600 m con LSN 0300 A, 3000 m con LSN 1500 A; 500 m de cable no aislado como máximo. SSD para el cálculo real.
- Historia: 1000 m a 2 mA por elemento dan unos 73 elementos con LSN 1500 A según el manual.
- Laboratorio: Foco, 20 min. Hacer la cuenta en planilla y comparar con el gráfico.
- Regla: ningún lazo sin cálculo de caída guardado en la carpeta de obra.

### 6. Elegir detector
- 4 de 5 fuentes (TH15, TH16).
- Idea: nueve variantes AVENAR detector 4000; se elige por riesgo y por fenómenos que no son fuego. No hay "detector 5000"; la serie 400 queda sin soporte después del firmware 4.8.
- Historia: el hotel con ducha del Anexo E de BS 5839-1 (https://professional-electrician.com/?p=36535).
- Laboratorio: Rápido, 10 min. Tabla de selección de cinco ambientes.
- Regla: cada detector con su porqué escrito.

### 7. Entradas y salidas
- 2 de 2 fuentes (TH19, TH20, TH21).
- Idea: FMC (pulsadores), FNM/FNX (sirenas, balizas), FLM-420/430 (entradas, salidas, convencionales), RLE-S (extinción). Cada entrada de alarma suma un punto; silenciar es manual en EN 54-2.
- Historia: RPS 5.14.17 y 5.15.27 borraban una entrada del RLE-S al abrir configuraciones viejas (TI 2715).
- Laboratorio: Foco, 15 min. Inventario de puntos de una obra chica.
- Regla: toda salida que mueve algo físico queda identificada y con forma de aislarla.

### 8. Zona de energía
- 3 de 3 fuentes (TH22, TH23, TH24, TH25).
- Idea: FPE-8000-BCM y zonas de energía desde el 02/05/2026; cálculo 24 h (RPS trae 30 h) más alarma, por factor; la IT-11 pedía 15 min de alarma.
- División: factor 1,20 frente a 1,25 (https://www.securitysales.com/insights/proper-backup-power-best-practices/130905/).
- Historia: la sobrecorriente falsa de RPS y el truco de 1 h y 26 Ah (TI 2739).
- Laboratorio: Foco, 15 min. Calcular baterías con las dos variantes.
- Regla: la batería se calcula con la norma que pide el proyecto y se escribe la fecha de fabricación.

## Arco 3. Programar con FSP-5000-RPS (lecciones 9 a 12)
Por qué este arco: el panel hace lo que dice la configuración. Termina con un proyecto que se puede descargar, leer y defender.

### 9. Primer proyecto
- 2 de 2 fuentes (TH26, TH27).
- Idea: RPS 5.15.28 en Windows 11 24H2; cuenta 4.8 con país Uruguay; commissioning: hora, PNA, IP, USB, autodetección, editar, consistencia, descarga, walk test, diagnóstico.
- Historia: RPS pide descarga completa si la hora del panel no coincide (TI 2715).
- Laboratorio: Admin, 20 min. Crear la configuración de un AVENAR 2000 en RPS sin panel.
- Regla: Set Panel Time antes de cada descarga y copia de la configuración antes y después.

### 10. Zonas y reglas
- 3 de 3 fuentes (TH28).
- Idea: zonas lógicas (grupo y subdirección), puntos de alarma y lógicos, reglas por evento y por estado, contadores; la matriz de control vive en reglas.
- Historia: la integración RS-232 ve "línea.grupo.subdirección" (https://docs.hsyco.com/docs/io-servers/boschfpa).
- Laboratorio: Foco, 20 min. Escribir la matriz causa y efecto de un piso.
- Regla: primero la matriz en papel, después las reglas.

### 11. Modo del detector
- 3 de 3 fuentes (TH17, TH18).
- Idea: el lugar de instalación en RPS fija la sensibilidad; se pueden apagar sensores; multisensor espera más ante falsas.
- División: multisensor u óptico (https://bregroup.com/documents/d/bre-group/_6-2018-march-multi-sensors-in-fire-and-false-alarm-tests).
- Laboratorio: Rápido, 10 min. Revisar modos por defecto en una configuración.
- Regla: ningún detector queda en el modo por defecto sin mirarlo.

### 12. Día y noche
- 3 de 4 fuentes (TH29, TH30).
- Idea: retardo de transmisión, dependencia tipo A/B/C, alarma demorada (máx. 6 min en BS 5839-1, el pulsador la anula), día/noche; la verificación del monitoreo es otra cosa.
- División: verificación (https://www.securitysales.com/contributed/alarm-verification-remains-a-polarizing-proposition/).
- Laboratorio: Foco, 15 min. Diseñar en papel el modo día y el modo noche de un local.
- Regla: ningún retardo sin firma del técnico registrado ni sobre pulsadores.

## Arco 4. Conectar, probar y mantener (lecciones 13 a 16)
Por qué este arco: lo que separa un sistema que pasó la habilitación de uno que funciona en cinco años. Termina con una visita de mantenimiento documentada.

### 13. Paneles en red
- 2 de 2 fuentes (TH31, TH32).
- Idea: hasta 32 nodos; Ethernet con RSTP o CAN; PNA es el último octeto; red física dedicada; BMS por OPC, FSI o BACnet con licencia premium por panel; remoto por gateway con IPsec.
- Historia: desactivar TCP/IP panel a panel si Ethernet es solo para BMS (Networking guide).
- Laboratorio: Admin, 15 min. Plan de direcciones de una red de tres paneles.
- Regla: la red de incendio no comparte switch con nada.

### 14. Aislar y avisar
- 3 de 3 fuentes (TH33, TH21).
- Idea: avisar al monitoreo y a ocupantes; deshabilitar salidas de control (extinción, ascensores, puertas, transmisión) antes de probar; reaceptación tras cambios.
- Historia: 100 % de lo afectado y 10 % hasta 50 iniciadores tras cambiar software (https://www.health.mn.gov/facilities/regulation/engineering/lscfatesting24.pdf).
- Laboratorio: Campo, 10 min. Checklist previo a pruebas.
- Regla: no se dispara nada sin monitoreo avisado y salidas aisladas.

### 15. Probar detectores
- 2 de 2 fuentes (TH34).
- Idea: modo revisión, walk test secuencial o simultáneo, tiempos de 10 a 60 s, Testifire, LSN test tool.
- Historia: con dependencia de dos detectores se prueba fuera de revisión y el óptico puede tardar un minuto (https://armosystems.ru/upload/iblock/a58/a58a375f59a20cf60064da272d2b6fd9.pdf).
- Laboratorio: Campo, 20 min. Walk test de un lazo de banco.
- Regla: cada detector probado queda con hora y resultado.

### 16. Mantener y registrar
- 4 de 4 fuentes (TH35).
- Idea: inspección anual mínima (Bosch), frecuencias NFPA como referencia, sensibilidad, valor de contaminación, reloj, trazas, autotest remoto.
- Historia: el reloj que se corría 80 minutos por año, ahora 10 (TI 2715).
- Laboratorio: Admin, 15 min. Plantilla de informe de mantenimiento.
- Regla: lo que no está registrado no se hizo.

## Divisiones
- Multisensor u óptico: BRE y pbctoday a favor del multisensor por rechazo de falsas; FIA advierte que toda demora retrasa un fuego real; BS 5839 Anexo E prefiere CO en ciertos ambientes. Cómo decidir: riesgo de fuego primero, fenómenos del lugar después, y la demora aceptable la define el proyecto.
- Clase A o B: Bosch recomienda lazo; NFPA no impone. Cómo decidir: lo que pida el proyecto y la autoridad; con LSN el lazo cuesta poco cable extra y gana tolerancia a fallas.
- Factor de batería y tiempo de alarma: 1,20 o 1,25; 5 o 15 minutos. Cómo decidir: la norma que adopte el proyecto; ante la duda, el más exigente.
- Verificación de alarma y retardos: menos despachos inútiles frente a demora. Cómo decidir: solo con acuerdo de la autoridad y nunca sobre pulsadores.

## Huecos
- Ayuda de FSP-5000-RPS y guía de operación AVENAR vigente no accesibles sin extranet; la programación se enseña a nivel de conceptos y con las TI.
- IT-11 vigente leída fuera del scraper (sau.org.uy bloquea scripts) y UNIT 962 no consultada.
- No hay foros de instaladores Bosch legibles sin JavaScript.

## Entrega
Cada lección en class/NN-<handle>/ con script.txt (charla opcional, sin audio), card.md y quiz.json; ficha en class/course.json.
