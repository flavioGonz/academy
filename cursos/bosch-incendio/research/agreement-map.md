# Mapa de acuerdos: Detección de incendio Bosch (versión compacta)

Fuentes: 28 páginas en raw/web (11 de Bosch entre manuales, TI, folleto y web; 1 guía Bosch alojada por distribuidor; 1 hoja de datos en español de distribuidor; 15 externas: BRE, FIA x3, pbctoday, professional-electrician, Security Sales x3, Minnesota DOH, open-exam-prep, Wikipedia, SecurityInfoWatch, IMPO, gub.uy, hsyco). Notas: research/notes/a.md. Conteo N de M por páginas, no por notas. Muchas preguntas de producto solo las responde Bosch: ahí M es chico y se marca "evidencia escasa" aunque la fuente sea primaria.

## TH01 Elegí 2000 o 8000 por cantidad de lazos y por licencia, no por precio de lista
- Sub-topic: T01. Agree: 2 of 2 (System manual, web de paneles). Notes: a:N1, a:N2, a:N7. Disagree: none found. Level: foundation. Evidencia escasa (solo fabricante).
- Best story: la licencia premium es por panel y está grabada; un 2000 standard no se puede poner en red.

## TH02 En redes mixtas con FPA-5000 todo corre el mismo 3.x; en redes solo AVENAR, 4.x
- Sub-topic: T01 (also T13). Agree: 3 of 3 (System manual, Networking guide, TI 2715). Notes: a:N3, a:N5. Disagree: none. Level: core.

## TH03 Bosch sigue siendo el dueño de incendio; video, acceso e intrusión pasaron a Keenfinity (Triton)
- Sub-topic: T01. Agree: 1 of 1 (SecurityInfoWatch). Notes: a:N6. Level: foundation. Evidencia escasa.

## TH04 La norma local y el proyecto firmado mandan sobre el manual del fabricante
- Sub-topic: T02. Agree: 4 of 4 (System manual, IMPO 372/023, gub.uy comunicado, open-exam-prep sobre NFPA). Notes: a:N8, a:N9, a:N10, a:N13, a:N22. Disagree: none. Level: foundation.
- Best story: la DNB aclara que el borrador de la nueva IT11 no autoriza proyectos hasta entrar en vigencia (https://www.gub.uy/ministerio-interior/comunicacion/noticias/comunicado-tecnicos-registrados-ciudadania-general).

## TH05 En Uruguay instala y mantiene una empresa registrada; el proyecto lo firma un técnico registrado
- Sub-topic: T02. Agree: 1 of 1 (IMPO). Notes: a:N8, a:N9. Level: foundation. Evidencia escasa pero primaria.

## TH06 Conocé las partes de EN 54 que tocás en obra (2, 4, 5, 7, 13, 29)
- Sub-topic: T02. Agree: 2 of 2 (Wikipedia, FIA EN 54). Notes: a:N11, a:N12. Level: foundation.

## TH07 LSN improved: 254 elementos por lazo, 127 en cuanto entra un classic
- Sub-topic: T03. Agree: 2 of 2 (System manual, Selection guide). Notes: a:N14, a:N16. Level: foundation.

## TH08 Dirección automática (000) para lazo simple; manual (001 a 254) cuando hay T-tap, y entonces T-tap en RPS
- Sub-topic: T03. Agree: 2 of 2 (System manual, guía detector 4000). Notes: a:N15, a:N32. Level: foundation.

## TH09 Cableá en lazo siempre que puedas: sobrevive a un corte o un corto
- Sub-topic: T04. Agree: 3 of 3 (System manual, Selection guide, open-exam-prep). Notes: a:N18, a:N16, a:N22. Disagree: open-exam-prep: NFPA no impone clase y la B es la más común; la decisión es del diseñador. Level: foundation.

## TH10 No hagas ramales de un elemento ni mallas: rompen el aislamiento
- Sub-topic: T04. Agree: 1 of 1 (System manual). Notes: a:N19, a:N20. Level: core. Evidencia escasa.

## TH11 Más de 512 puntos de alarma en un panel pide controlador redundante
- Sub-topic: T04 (also T01). Agree: 2 of 2 (System manual, Networking guide). Notes: a:N21, a:N54. Level: core.

## TH12 Calculá el lazo para que el último elemento vea 15 V o más
- Sub-topic: T05. Agree: 1 of 1 (System manual). Notes: a:N23, a:N24. Level: core. Evidencia escasa (fabricante).

## TH13 Sumá el cable no aislado: máximo 500 m
- Sub-topic: T05. Agree: 1 of 1. Notes: a:N25. Level: core.

## TH14 Planificá con Safety Systems Designer, no a ojo
- Sub-topic: T05 (also T09). Agree: 2 of 2 (System manual, TI 2716). Notes: a:N26. Level: core.

## TH15 Elegí el detector por el riesgo de fuego y después por lo que no es fuego
- Sub-topic: T06 (also T07). Agree: 4 of 5 (FIA selección, professional-electrician, web AVENAR 4000, hoja tvc). Notes: a:N27, a:N29, a:N36, a:N37. Disagree: pbctoday: el multisensor rechaza mejor en todos los casos probados, lo que tienta a ponerlo en todos lados. Level: core.

## TH16 Planificá el reemplazo de la serie 400 y 500 viejas antes de actualizar a 4.8 o más
- Sub-topic: T06. Agree: 1 of 1 (TI 2715). Notes: a:N30. Level: core.

## TH17 El modo de aplicación en RPS es parte del detector: documentalo
- Sub-topic: T07. Agree: 3 of 3 (guía detector 4000, FIA selección, hoja tvc). Notes: a:N32, a:N33, a:N36, a:N29. Level: core.

## TH18 Multisensor reduce falsas alarmas porque espera; esa espera es el costo
- Sub-topic: T07. Agree: 3 of 4 (BRE, pbctoday, FIA estrategia). Notes: a:N34, a:N35, a:N59. Disagree: professional-electrician: con vapor y aerosol el CO supera al multisensor óptico/térmico. Level: core.
- Best story: la tostada de BRE (https://bregroup.com/documents/d/bre-group/_6-2018-march-multi-sensors-in-fire-and-false-alarm-tests).

## TH19 Cada entrada que puede dar alarma consume un punto; contá los FLM
- Sub-topic: T08. Agree: 2 of 2 (System manual, TI 2715). Notes: a:N38. Level: core.

## TH20 Silenciar y reponer avisadores es manual en EN 54-2
- Sub-topic: T08. Agree: 1 of 1 (TI 2715). Notes: a:N41. Level: core.

## TH21 Extinción: el RLE-S y VdS 2496 piden diseño redundante y cuidado con versiones de RPS
- Sub-topic: T08 (also T14). Agree: 2 of 2 (System manual, TI 2715). Notes: a:N39, a:N69. Level: advanced.

## TH22 Desde mayo de 2026: zonas de energía con FPE-8000-BCM en obra nueva
- Sub-topic: T09. Agree: 1 of 1 (TI 2716). Notes: a:N42. Level: core.

## TH23 Calculá la batería con margen: 24 h más alarma, por un factor
- Sub-topic: T09. Agree: 3 of 3 (open-exam-prep, Security Sales baterías, TI 2715 30 h). Notes: a:N44, a:N45, a:N46. Disagree: factor 1,20 (open-exam-prep) frente a 1,25 (Security Sales); 5 min de alarma en NFPA frente a 15 min en la IT-11 uruguaya de 2010 (leída sin archivar). Level: core.

## TH24 Probá red y batería por separado en la puesta en marcha
- Sub-topic: T09 (also T15). Agree: 2 of 2 (System manual, Security Sales baterías). Notes: a:N47, a:N46. Level: core.

## TH25 Un truco temporal de RPS se documenta y se deshace
- Sub-topic: T09. Agree: 1 of 1 (TI 2739). Notes: a:N43. Level: advanced.

## TH26 Usá la versión de RPS vigente y sincronizá la hora antes de descargar
- Sub-topic: T10. Agree: 2 of 2 (TI 2715, TI 2739). Notes: a:N48, a:N49, a:N50, a:N52. Level: core.

## TH27 Seguí la secuencia de commissioning y guardá el diagnóstico como acta
- Sub-topic: T10 (also T15). Agree: 1 of 1 (System manual). Notes: a:N51. Level: foundation.

## TH28 La dirección lógica (grupo y subdirección) es la llave de reglas, textos e integraciones
- Sub-topic: T11. Agree: 3 of 3 (System manual, TI 2715, hsyco). Notes: a:N53, a:N55, a:N56. Level: core.

## TH29 Todo retardo o verificación se acuerda con la autoridad y no aplica al pulsador
- Sub-topic: T12. Agree: 3 of 4 (FIA estrategia, Security Sales verificación, System manual). Notes: a:N57, a:N59, a:N60. Disagree: Security Sales verificación recoge a quienes ven en la preverificación una demora riesgosa (flashover). Level: core.

## TH30 Día y noche cambia la respuesta, no la protección
- Sub-topic: T12. Agree: 3 of 3 (System manual, FIA estrategia, guía detector 4000). Notes: a:N58, a:N59, a:N32. Level: core.

## TH31 Red de incendio aparte; el último octeto es el nodo
- Sub-topic: T13. Agree: 1 of 1 (Networking guide). Notes: a:N62, a:N63, a:N64. Level: core.

## TH32 Remoto con gateway e IPsec, nunca abriendo puertos del panel
- Sub-topic: T13. Agree: 2 of 2 (Networking guide, web Remote). Notes: a:N65, a:N66. Level: advanced.

## TH33 Antes de probar: avisar al monitoreo y a la gente, aislar lo que acciona
- Sub-topic: T14. Agree: 3 of 3 (Minnesota, System manual, guía detector 4000). Notes: a:N67, a:N68, a:N70. Level: foundation.

## TH34 Probá en modo revisión y dale tiempo al detector
- Sub-topic: T15. Agree: 2 of 2 (guía detector 4000, TI 2706). Notes: a:N70, a:N72, a:N61. Level: core.

## TH35 Mantenimiento con registros: frecuencia, sensibilidad, contaminación y reloj
- Sub-topic: T16. Agree: 4 of 4 (System manual, Security Sales sensibilidad, Minnesota, TI 2715). Notes: a:N73, a:N74, a:N75, a:N76, a:N77. Level: core.

## The big splits
- Multisensor u óptico: BRE y pbctoday (más tarde ante falsas, igual ante fuego) frente a la FIA (todo filtro demora un fuego real) y BS 5839 Anexo E vía professional-electrician (CO mejor con vapor). Gira en torno a si la demora es aceptable en ese ambiente.
- Clase A o B: Bosch recomienda lazo; NFPA no impone y la B es la más común. Gira en torno al costo de cable y canalización frente a cuántos elementos se aceptan perder por una falla.
- Factor de batería 1,20 o 1,25, y 5 o 15 minutos de alarma: gira en torno a qué norma adopta la autoridad.
- Verificación de alarma: reducción de despachos inútiles frente a riesgo de demora.

## Coverage gaps
- No hay acceso público a la ayuda de FSP-5000-RPS ni a la guía de operación AVENAR vigente (el CDN de documentos de Bosch no responde a scripts); la programación se apoya en TI y en la guía del detector de 2014.
- Licenciamiento de RPS (registro en extranet) no está documentado públicamente.
- La IT-11 vigente (2010) y la UNIT 962 no están en raw/; la IT-11 se leyó fuera del scraper.
- No hay foros de instaladores Bosch accesibles sin JavaScript (la comunidad de Bosch y Mike Holt bloquean scripts).
- No existe "AVENAR detector 5000" en las fuentes.
