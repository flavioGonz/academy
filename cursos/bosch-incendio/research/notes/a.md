# Notes: batch a
Pages read: 28. With notes: 27. Skipped: 1 (docs.hsyco.com solo aporta un detalle de integración RS-232 de FPA-5000; queda como nota menor). Leída aparte sin archivar: IT-11 de la DNB (sau.org.uy responde 403 a scripts; se leyó con WebFetch, no está en raw/).

## T01 Familia de paneles
- a:N1. AVENAR panel 8000 admite 46 módulos funcionales, hasta 32 de lazo; AVENAR panel 2000 admite 6, hasta 4 de lazo. El 8000 se arma con módulos en riel; el 2000 viene como kit en gabinete.
  - Source: https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf  Quote: "46 functional modules, of which a maximum of 32 can be analog addressable loop modules"
  - Kind: number. Level: foundation. Bias: fabricante.
- a:N2. La licencia viene grabada en el controlador y no se cambia: standard o premium. Premium agrega interfaces a BMS (BIS, OPC, FSI), panel jerárquico UGM-2040 y evacuación por voz (Smart Safety Link), y es obligatoria en cada panel que deba verse en el BMS o, en el 2000, para trabajar en red.
  - Source: (System manual, misma url que a:N1)  Quote: "cannot be modified, revoked or transported"
  - Kind: rule of thumb. Level: foundation. Also: T13.
- a:N3. Paneles y teclados AVENAR y FPA-5000 (MPC-xxxx-B y -C) conviven en una red por Ethernet y CAN; para eso todos deben correr el mismo firmware 3.x. El firmware 4.x es solo para redes 100 % AVENAR. Desde 2026 el 3.x salió de mantenimiento y Bosch pide evaluación de riesgo si el panel está en Ethernet.
  - Source: System manual (a:N1) y https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/software_tools/avenar_panel_firmware/AVENAR_panel_FPA_5000_System_Networking_Guide_version_05.pdf?collection=bosch-bt-lifesafetysystems
  - Kind: rule of thumb. Level: core. Also: T13.
- a:N4. El controlador de un FPA-5000 se puede reemplazar por uno AVENAR: no usa tarjetas de dirección, exige riel corto PRS-0002-C, no tiene RS232 integrado y no admite puerta frontal (se recalienta). Con BCM-0000-A no cumple EN 54-4.
  - Source: System manual (a:N1). Kind: mistake. Level: core.
- a:N5. Versiones vigentes: firmware de panel 4.8.1 (junio 2026) con FSP-5000-RPS 5.15.27; la 4.9 está prevista para diciembre de 2026.
  - Source: https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2715_2026_TI_AVENAR_FW-4.8.1__FSO-5000-RPS_5.15.27.pdf?collection=bosch-bt-lifesafetysystems
  - Kind: number. Level: foundation. Also: T10.
- a:N6. Bosch vendió a Triton su negocio de video, acceso e intrusión y comunicaciones, pero retuvo el de sistemas de alarma de incendio, que se integra con su negocio de integración dentro de Bosch Building Technologies.
  - Source: https://www.securityinfowatch.com/industry-news/article/55249385/bosch-sells-security-and-communications-technology-business-to-triton-partners  Quote: "the fire-alarm systems product business ... will be consolidated with the integrator"
  - Kind: story. Level: foundation.
- a:N7. La web vigente de incendio de Bosch está en boschbuildingtechnologies.com (Life Safety Systems) y presenta AVENAR panel 2000 y 8000 con integración por FSI, OPC o BACnet.
  - Source: https://www.boschbuildingtechnologies.com/lifesafetysystems/en/products/fire-alarm-control-panels/
  - Kind: definition. Level: foundation. Bias: página comercial.

## T02 Normas y responsabilidad
- a:N8. El Decreto 372/023 (vigente desde enero de 2024) reglamenta las habilitaciones de Bomberos: el trámite lo ingresa un técnico registrado bajo declaración jurada, y los sistemas de detección y alarma los suministran, instalan, ponen en marcha y mantienen empresas registradas ante la DNB.
  - Source: https://impo.com.uy/bases/decretos/372-2023  Quote: "deberán ser suministrados, instalados, puestos en funcionamiento y mantenidos por empresas registradas"
  - Kind: rule of thumb. Level: foundation.
- a:N9. El mismo decreto: el técnico registrado redacta el proyecto y verifica las medidas; el propietario mantiene; las empresas responden por suministro, instalación y mantenimiento con declaraciones juradas, y hay multas de 10 a 200 UR para empresas.
  - Source: https://impo.com.uy/bases/decretos/372-2023. Kind: number. Level: core.
- a:N10. La DNB anunció el 31/07/2026 consulta pública de la nueva IT11 "Sistemas de detección y alarma de incendios", con vigencia prevista en 2027; aclara que los borradores no autorizan su uso para proyectos hasta que entren en vigencia.
  - Source: https://www.gub.uy/ministerio-interior/comunicacion/noticias/comunicado-tecnicos-registrados-ciudadania-general
  - Kind: story. Level: foundation.
- a:N11. EN 54 es una serie de normas de producto (más guías de aplicación como la CEN/TS 54-14) y se usa también fuera de Europa, incluida Latinoamérica.
  - Source: https://en.wikipedia.org/wiki/EN_54. Kind: definition. Level: foundation.
- a:N12. Partes útiles en obra: EN 54-2 central, EN 54-4 fuente, EN 54-5 calor, EN 54-7 humo, EN 54-13 compatibilidad, EN 54-29 multisensor humo y calor.
  - Source: https://www.fia.uk.com/resources/british-standards/bs-en-54-series-fire-detection-alarm-systems.html. Kind: definition. Level: foundation.
- a:N13. Bosch dice en su wiring guide y en el System manual que las normas nacionales y las autoridades regionales (bomberos) mandan sobre la planificación, y que el planificador e integrador son responsables de aplicarlas.
  - Source: System manual (a:N1)  Quote: "The regulations issued by regional authorities and institutions (e.g. fire service) must be adhered to."
  - Kind: rule of thumb. Level: foundation.
- (Leída sin archivar) IT-11 de la DNB, 17/11/2010: cita UNIT 962, pide batería de 24 h en supervisión y 15 min en alarma, pulsador a no más de 30 m, preseñal de hasta 2 min en locales concurridos, y una ART firmada por el técnico responsable. No citar url.

## T03 Lazo LSN improved
- a:N14. Por módulo: hasta 254 elementos LSN improved o 127 classic; LSN 0300 A da 300 mA y hasta 1600 m; LSN 1500 A da hasta 1500 mA y 3000 m. Si hay un solo elemento classic, el lazo queda en 127.
  - Source: System manual (a:N1). Kind: number. Level: foundation.
- a:N15. Llave rotativa 000 = direccionamiento automático (de fábrica, sin T-tap); 001 a 254 = manual (permite T-tap); CL 0 0 = modo classic. Si se elige manual, se marca T-tap en FSP-5000-RPS sea cual sea la topología.
  - Source: System manual (a:N1)  Quote: "If you decide on manual address setting, then you have to select T-tap in FSP-5000-RPS."
  - Kind: technique. Level: foundation.
- a:N16. LSNi admite lazo, ramal, T-tap y estructura mixta, cable blindado o no, y aisladores de cortocircuito en cada equipo.
  - Source: https://media.boschbuildingtechnologies.com/fs/media/pb/images/news/rethink_the_magazine/avenar_detector_4000_series/Selection_Guide_.pdf?collection=bosch-bt-lifesafetysystems
  - Kind: definition. Level: foundation. Bias: folleto del fabricante.
- a:N17. Si se usa blindaje: a tierra funcional solo en el panel (dos puntos en lazo, uno en ramal), continuado en cada equipo, sin otras conexiones.
  - Source: System manual (a:N1). Kind: technique. Level: core.

## T04 Topologías y aisladores
- a:N18. En lazo, cada elemento tiene aislador entre b1 y b2; ante corte o corto el lazo se parte en dos ramales alimentados por LSN1 y LSN2 y sigue andando. En ramal se pierde todo lo que queda detrás de la falla. Bosch recomienda lazo siempre que se pueda.
  - Source: System manual (a:N1)  Quote: "prefer the loop topology"
  - Kind: rule of thumb. Level: foundation.
- a:N19. Un ramal de un solo elemento conectado solo a b1 no aísla: entre dos elementos que aíslan queda una "zona" que cae entera ante un corto. Las autoridades pueden limitar cuántos elementos se pierden por una falla.
  - Source: System manual (a:N1). Kind: mistake. Level: core.
- a:N20. Prohibido armar mallas (mesh) dentro de lazo o ramal.
  - Source: System manual (a:N1). Kind: mistake. Level: foundation.
- a:N21. EN 54-2: no más de 512 detectores y pulsadores pueden fallar por una falla de componente; con más de 512 en un panel se exige controlador redundante (en el 8000, otro controlador o un keypad 8000).
  - Source: System manual (a:N1). Kind: number. Level: core. Also: T01.
- a:N22. En NFPA 72 la clase describe el desempeño: clase B pierde lo que está aguas abajo de un corte; clase A vuelve al panel y sobrevive a un corte; clase X sobrevive además a un corto gracias a aisladores. NFPA no dice qué clase usar: lo decide la especificación, el diseñador o la autoridad.
  - Source: https://open-exam-prep.com/study-guides/cfps-fire/detection-and-alarm/fire-alarm-system-fundamentals
  - Kind: definition. Level: foundation. Bias: sitio de preparación de examen.

## T05 Caída y consumo
- a:N23. El largo posible depende de resistencia del cable, cantidad y consumo de elementos y su distribución; la fórmula supone todo concentrado al final (conservadora). Datos: 30 V en bornes, 15 V mínimo al final, 0,8 mm (0,503 mm²), RFET 0,35 Ω en improved.
  - Source: System manual (a:N1)  Quote: "UEnd = bus end voltage = 15 volt (must not fall below this limit!)"
  - Kind: template. Level: core.
- a:N24. Ejemplos del manual: LSN classic con LSN 0300 A, 50 elementos a 3 mA, unos 840 m; LSN improved con LSN 1500 A, 120 elementos a 0,5 mA, unos 1950 m; 1000 m a 2 mA, 73 elementos.
  - Source: System manual (a:N1). Kind: number. Level: core.
- a:N25. El cable no aislado (entradas de FLM, línea NAC del FLM-420-NAC, indicadores remotos) no puede sumar más de 500 m. Cable recomendado J-Y(St)Y 2x2x0,8 mm rojo.
  - Source: System manual (a:N1). Kind: number. Level: core.
- a:N26. Safety Systems Designer (SSD) calcula largos, energía y cantidades; Bosch exige SSD para planificar instalaciones AVENAR nuevas con zonas de energía.
  - Source: https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2716_2026_TI_EN_AVENAR_Panel_Energy_Information.pdf?collection=bosch-bt-lifesafetysystems
  - Kind: rule of thumb. Level: core. Also: T09.

## T06 Detectores
- a:N27. La serie AVENAR detector 4000 tiene nueve variantes: térmico FAH-425-T-R, ópticos FAP-425-O y O-R, doble óptico DO-R, multisensores OT, OT-R, DOT-R, DOTC-R y DOTCO-R. Las "-R" tienen llaves rotativas (manual o automático).
  - Source: https://www.boschbuildingtechnologies.com/lifesafetysystems/en/products/fire-detection/avenar-detector-4000-series/
  - Kind: definition. Level: foundation. Bias: comercial.
- a:N28. ISP: algoritmos entrenados con más de 5000 patrones de fuego reales (su afirmación); doble óptico con LED infrarrojo y azul; aislador en todos los detectores; CO con celda de 10 años en DOTCO.
  - Source: (página a:N27). Kind: number. Level: foundation. Bias: comercial.
- a:N29. Hoja de datos en español: el térmico dispara por máximo de 54 °C o 69 °C o por gradiente; el sensor de CO también ve hidrógeno y monóxido de nitrógeno; la contaminación se reporta como avería en lugar de falsa alarma.
  - Source: https://cdn.tvc.mx/media/33158/FAP_425_Data-sheet-esES_1811112146443.pdf
  - Kind: definition. Level: core.
- a:N30. Fin de soporte: el firmware 4.8 es la última versión que soporta O400, OT400, OC410, OTC410, T400 y NEV300; desde la cuenta 4.8, RPS ya no ofrece FAP-O500 y FAP-OC500. Bosch pide planificar reemplazos.
  - Source: TI 2715 (a:N5)  Quote: "Plan now for replacements in systems where these devices are still in use."
  - Kind: rule of thumb. Level: core.
- a:N31. No existe en las fuentes un "AVENAR detector 5000": la línea vigente es la 4000 y la serie 500/520 (invisibles).
  - Source: página a:N27 y Selection guide (a:N16). Kind: definition. Level: foundation.

## T07 Modos de aplicación
- a:N32. Los FAP-425 se programan eligiendo el lugar de instalación en RPS; eso fija el campo característico. Por defecto: DOTC-R en "Oficina (fumadores)/sala de espera/restaurante", OT y DOT en "Oficina (modo día)", ópticos en sensibilidad media, térmico en A2R.
  - Source: https://armosystems.ru/upload/iblock/a58/a58a375f59a20cf60064da272d2b6fd9.pdf  (guía de operación Bosch alojada por un distribuidor)
  - Kind: technique. Level: core.
- a:N33. En multisensores se pueden apagar sensores (solo óptico, solo térmico diferencial A2R, solo máximo A2S). "Cocina en operación" deja al OT/DOT como térmico. Algunas combinaciones del DOTC-R no cumplen EN 54-7.
  - Source: guía a:N32. Kind: technique. Level: core.
- a:N34. BRE (35 multisensores contra 2 ópticos): ante fuegos reales rinden parecido; ante tostadas, vapor, polvo y aerosol los multisensores disparan más tarde. En la prueba de tostada, en promedio un minuto antes de que la tostada prenda pero 40 s después que los ópticos.
  - Source: https://bregroup.com/documents/d/bre-group/_6-2018-march-multi-sensors-in-fire-and-false-alarm-tests
  - Kind: number. Level: core. Bias: financiado por la FIA y fabricantes.
- a:N35. Resumen de la misma investigación: cuanto más sofisticado el multisensor, menos falsas alarmas; pero la respuesta a fuegos depende sobre todo de la sensibilidad, no del tipo.
  - Source: https://www.pbctoday.co.uk/news/health-safety-news/reduction-of-false-alarms-when-multi-sensor-detectors-used/40842/
  - Kind: story. Level: core.
- a:N36. Elegir detector en dos pasos: primero el riesgo de fuego, después los fenómenos que no son fuego del lugar (vapor, polvo, aerosol); y dejar registrado el porqué, porque el modo de un multisensor no se ve desde afuera.
  - Source: https://www.fia.uk.com/news/blogs/how-to-select-the-right-detector-for-the-job-a-walkthrough-guide-to-fire-detection-and-alarms.html
  - Kind: technique. Level: core.
- a:N37. Ejemplo de BS 5839-1 Anexo E: habitación de hotel con ducha; ópticos y multisensores detectan el fuego latente, pero frente a vapor y aerosol el que mejor queda es el de CO.
  - Source: https://professional-electrician.com/?p=36535
  - Kind: story. Level: core.

## T08 Avisadores, sirenas y módulos
- a:N38. Módulos de interfaz en LSN: FLM-420/4-CON (dos zonas convencionales), FLM-420-NAC, FLM-430-I2M1 (2 entradas, 1 salida supervisada), FLM-430-I4R2 (4 entradas, 2 relés), FLM-420-RLE-S (extinción). Cada entrada que puede dar alarma consume un punto.
  - Source: System manual (a:N1) y TI 2715 (a:N5). Kind: definition. Level: core.
- a:N39. Para controlar extinción según VdS 2496 se usa el FLM-420-RLE-S (hasta 8 por lazo); con el uso "Extinguishing interface VdS 2496" la resistencia de entrada queda fija en 3K3||680/3K3. RPS 5.14.17 y 5.15.27 borraban sin aviso la entrada de realimentación 5 al abrir configuraciones viejas.
  - Source: TI 2715 (a:N5) y System manual. Kind: mistake. Level: advanced.
- a:N40. FNX-425U (sirena y baliza): hasta 84 por lazo con detector, 127 sin; desde 4.8.1 reporta horas, batería y avería a NEXOSPACE.
  - Source: System manual (a:N1) y TI 2715. Kind: number. Level: core.
- a:N41. Un timer de duración en salidas NAC sirve solo para señales no EN 54: EN 54-2 exige acción manual para silenciar o reponer avisadores.
  - Source: TI 2715 (a:N5). Kind: rule of thumb. Level: core.

## T09 Fuente y baterías
- a:N42. Desde el 02/05/2026 las instalaciones nuevas usan zonas de energía con FPE-8000-BCM; no se mezcla con BCM-0000-B en un panel; requiere firmware 4.7.0 o más, RPS 5.14.17 o más y SSD 3.6 o más; módulos de alto consumo al lado del BCM y zonas separadas quitando el cable rojo entre rieles largos.
  - Source: TI 2716 (a:N26). Kind: rule of thumb. Level: core.
- a:N43. Falla conocida: RPS valida la autonomía con la corriente de alarma de los elementos LSN y da sobrecorriente falsa en zonas con muchas sirenas; Bosch propone un truco temporal (1 h de reposo y 26 Ah) hasta un RPS corregido a fines de 2026, y pide volver a los valores reales después.
  - Source: https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2739_2026_TI_2739_2026_TI_FSP-5000-RPS_EN.pdf?collection=bosch-bt-lifesafetysystems
  - Kind: story. Level: advanced.
- a:N44. RPS cambió el tiempo de reposo por defecto de 24 a 30 horas.
  - Source: TI 2715 (a:N5). Kind: number. Level: core.
- a:N45. NFPA 72: 24 h de reposo y luego 5 min de alarma (15 con evacuación por voz); fórmula C = (Ireposo x Treposo + Ialarma x Talarma) x 1,20.
  - Source: https://open-exam-prep.com/study-guides/cfps-fire/detection-and-alarm/fire-alarm-system-fundamentals
  - Kind: template. Level: core.
- a:N46. Otra práctica: misma base de 24 h y 5 min, pero con factor de envejecimiento 1,25; fechar la batería por su fabricación; vida típica de 3 a 5 años; probar con carga, no solo con tester.
  - Source: https://www.securitysales.com/insights/proper-backup-power-best-practices/130905/
  - Kind: rule of thumb. Level: core.
- a:N47. Puesta en marcha Bosch: batería entre 12,0 y 14,1 V (o 24 a 28,2 V); probar falta de red y de batería con aviso a unos 25 min; la falla de batería puede tardar hasta 15 min en aparecer.
  - Source: System manual (a:N1). Kind: test. Level: core. Also: T15.

## T10 FSP-5000-RPS
- a:N48. RPS 5.15.27 corre en Windows 11 24H2 de 64 bits; el driver USB puede no ser de confianza en Windows 11; la cuenta 4.8 agrega Uruguay como país; se pasa de 3.x a 4.x en tres pasos (subir a 3.5, cambiar nodos a AVENAR, subir a 4.x).
  - Source: TI 2715 (a:N5). Kind: technique. Level: core.
- a:N49. Antes de descargar, sincronizar la hora con "Set Panel Time": si no, RPS puede pedir una descarga completa sin cambios. RPS 5.15.27 nuevo: chequeo de consistencia con pistas, ayuda en HTML.
  - Source: TI 2715. Kind: mistake. Level: core.
- a:N50. RPS 5.15.28 figura como versión afectada y vigente en la TI de septiembre 2026 (validación de autonomía).
  - Source: TI 2739 (a:N43). Kind: number. Level: core.
- a:N51. Commissioning: alimentar, calibrar pantalla, cargar hora, fecha, PNA y Ethernet, reiniciar, conectar por USB, autoconfiguración, editar, descargar, walk test, pruebas, guardar el archivo de diagnóstico como acta.
  - Source: System manual (a:N1). Kind: template. Level: foundation. Also: T15.
- a:N52. Bosch pide enviar firmware y RPS siempre como el .zip completo, sin renombrar.
  - Source: TI 2715. Kind: rule of thumb. Level: core.

## T11 Zonas lógicas y reglas
- a:N53. Los periféricos se agrupan por software en zonas lógicas; el panel muestra tipo de mensaje, tipo de elemento, ubicación y zona lógica con subdirección.
  - Source: System manual (a:N1). Kind: definition. Level: foundation.
- a:N54. Desde la cuenta 4.5, "puntos de alarma" (deciden si hace falta redundancia) y "puntos lógicos" (límites por panel: 4096 solo, 2048 en red) reemplazan a los puntos de detección.
  - Source: TI 2715 y Networking guide (a:N3). Kind: number. Level: core.
- a:N55. Las salidas se gobiernan con reglas por evento y reglas dependientes de estado, contadores y estados compuestos; copiar y pegar detectores asigna la siguiente subdirección del mismo grupo.
  - Source: TI 2715 (a:N5). Kind: technique. Level: core.
- a:N56. Integración externa por RS-232: el integrador ve los eventos como línea.<dirección lógica>.<subdirección>, lo que muestra que el nombre lógico es la llave de todo lo que viene después.
  - Source: https://docs.hsyco.com/docs/io-servers/boschfpa. Kind: story. Level: advanced. Also: T13.

## T12 Retardos, verificación y día/noche
- a:N57. EN 54-2 opcionales que ofrece el panel: retardo de transmisión, dependencia de más de una señal (tipos A, B y C), contador de alarmas, estado de modo día.
  - Source: System manual (a:N1). Kind: definition. Level: core.
- a:N58. Las teclas de función programables pueden pasar a modo día o noche y cambiar a sensibilidad alternativa.
  - Source: System manual (a:N1). Kind: technique. Level: core.
- a:N59. Estrategias de la FIA: alarma demorada para investigar (BS 5839-1 la limita a 6 min y el pulsador la anula), alarma confirmada por segundo detector, prealarma, día/noche; advierte que todo filtro demora la respuesta a un fuego real y no sirve, por ejemplo, en residencias de cuidado.
  - Source: https://www.fia.uk.com/static/uploaded/4ddbff0f-557d-496b-b62b716a1761b77d.pdf
  - Kind: rule of thumb. Level: core.
- a:N60. NFPA 72 edición 2013 introdujo la preverificación por el monitoreo, solo si el departamento de bomberos la pide, con un máximo de 90 s y aviso simultáneo al centro de despacho; sigue siendo polémica.
  - Source: https://www.securitysales.com/contributed/alarm-verification-remains-a-polarizing-proposition/
  - Kind: story. Level: advanced.
- a:N61. Prueba fuera del modo revisión con dependencias de 2 detectores: el óptico puede tardar hasta un minuto en aerosol; aplicar en ráfagas.
  - Source: guía a:N32. Kind: test. Level: core. Also: T15.

## T13 Redes e integración
- a:N62. Red de hasta 32 nodos (paneles, teclados, servidores OPC/FSI/BACnet/UGM) por Ethernet con RSTP o por CAN; el último octeto de la IP por defecto (192.168.1.x) es la dirección física de nodo; puertos 25001 a 25008; switches y conversores dentro del gabinete para cumplir EN 54.
  - Source: Networking guide (a:N3). Kind: number. Level: core.
- a:N63. La red de incendio va en una red física dedicada; la PC de servicio se desconecta de la red de incendio antes de conectarse a internet.
  - Source: Networking guide. Quote: "the fire alarm system must not be installed in a shared network". Kind: rule of thumb. Level: core.
- a:N64. Si Ethernet se usa solo para BMS, OPC o servicios remotos, desactivar la comunicación panel a panel por TCP/IP para no mandar datos de incendio sin querer.
  - Source: Networking guide. Kind: mistake. Level: advanced.
- a:N65. Remote Connect usa un Secure Network Gateway con IPsec (UDP 500 y 4500) y subredes separadas del router del cliente; licencias S, M o L según puntos.
  - Source: Networking guide. Kind: technique. Level: advanced.
- a:N66. NEXOSPACE Fire System Explorer agrega autotest remoto de detectores puntuales Bosch con registros que, según Bosch, cumplen VdS 3860.
  - Source: https://www.boschbuildingtechnologies.com/lifesafetysystems/en/products/remote-monitoring-fire-alarm-systems/
  - Kind: story. Level: advanced. Bias: comercial.

## T14 Seguridad del técnico
- a:N67. Antes de cualquier prueba, avisar a ocupantes y a la empresa de monitoreo (NFPA 72, 14.2.3.1 en la guía de Minnesota).
  - Source: https://www.health.mn.gov/facilities/regulation/engineering/lscfatesting24.pdf
  - Kind: rule of thumb. Level: foundation.
- a:N68. Tras cambios en el software del sitio: probar al 100 % lo afectado y un 10 % de los iniciadores no afectados, hasta 50.
  - Source: guía de Minnesota (a:N67). Kind: number. Level: core.
- a:N69. VdS 2496: si falla una unidad de procesamiento no puede caer más de un área de extinción; desde la segunda área hace falta controlador redundante. Las salidas a equipos de protección (extinción, puertas, transmisión) se prueban una por una en la puesta en marcha.
  - Source: System manual (a:N1). Kind: rule of thumb. Level: advanced.

## T15 Puesta en marcha y prueba de detectores
- a:N70. Para probar, pasar la zona a modo revisión (walk test): el detector se prepara solo. El cabezal queda sobre el detector hasta que dispare (hasta 10 s con aerosol, hasta 20 s en multisensor). Walk test secuencial (un sensor a la vez) o simultáneo con Testifire; en simultáneo, si no aparece alarma, un sensor falla.
  - Source: guía a:N32. Kind: test. Level: core.
- a:N71. Un lote de aerosol de prueba Bosch vino con poco principio activo: la lata también falla. (Historia de TI 1917/2015, no archivada; no citar.)
- a:N72. La herramienta FME-420-LSN-TTL lee el lazo desde una PC; Bosch publicó en 2026 un XML nuevo para reconocer elementos recientes (FNX-425U, FLM-430, DOTCO).
  - Source: https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2706_2026_TI_EN_FW-Update_LSN-Test_Tool.pdf?collection=bosch-bt-lifesafetysystems
  - Kind: technique. Level: advanced.

## T16 Mantenimiento y registros
- a:N73. Bosch recomienda al menos una inspección visual y funcional por año, recalibrar la pantalla táctil una vez por año y limpiar ventilaciones.
  - Source: System manual (a:N1). Kind: rule of thumb. Level: foundation.
- a:N74. Valor óptico de contaminación: 0 a 170 nuevo, hasta 350 normal, 350 a 450 cambiar pronto, 450 a 510 cambiar ya, más de 511 sensor desactivado.
  - Source: guía a:N32. Kind: number. Level: core.
- a:N75. NFPA 72: sensibilidad de detectores dentro del primer año, a los dos años y después hasta cada cinco, con registros de falsas alarmas.
  - Source: https://www.securitysales.com/news/when-how-test-smoke-detector-sensitivity/135776/
  - Kind: number. Level: core.
- a:N76. NFPA 72 (guía Minnesota): inspección visual semestral, prueba anual completa, y un registro de terminación junto a la central con cada cambio.
  - Source: guía de Minnesota (a:N67). Kind: template. Level: core.
- a:N77. Firmware 4.8 bajó el desvío del reloj de hasta 80 a 10 minutos por año; Bosch sugiere revisarlo en cada mantenimiento.
  - Source: TI 2715 (a:N5). Kind: number. Level: core.
- a:N78. Para soporte: archivos de traza en tarjeta FAT-32 con un archivo TRACE-AUTOSTART; apagar con el botón antes de sacar la tarjeta.
  - Source: System manual (a:N1). Kind: technique. Level: advanced.

## Disagreements seen
- Multisensor frente a óptico: BRE y pbctoday muestran menos falsas alarmas con multisensor; la misma BRE aclara que la ventaja es una demora y la FIA advierte que todo filtrado demora la respuesta a un fuego real; BS 5839 (vía professional-electrician) prefiere CO en ciertos ambientes con vapor. Urls: bregroup, pbctoday, fia 4ddbff0f, professional-electrician.
- Factor de seguridad de baterías: 1,20 (open-exam-prep) frente a 1,25 por envejecimiento (securitysales 130905).
- Clase A o B: Bosch recomienda lazo siempre que se pueda; NFPA deja la elección al diseñador y la clase B sigue siendo la más común en EE. UU. (open-exam-prep).
- Verificación de alarma: la NFPA 2013 la permite con 90 s y aviso simultáneo; sus críticos temen demoras (securitysales verificación).
- Autonomía: 24 h en NFPA 72 y en la IT-11 de 2010 con 5 min frente a 15 min de alarma; RPS ahora trae 30 h por defecto.

## Best stories
- El reloj del panel que se corría hasta 80 minutos por año, ahora 10 (TI 2715).
- RPS marcando sobrecorriente falsa en zonas con muchas sirenas y el truco temporal de 1 h y 26 Ah (TI 2739).
- La tostada de BRE: el multisensor dispara 40 s después que el óptico, todavía un minuto antes del fuego.
- Uruguay entra a la lista de países de RPS en la cuenta 4.8 (TI 2715).
- La IT11 en consulta pública para 2027 (gub.uy).
