# Plan: Alarmas Paradox, de la central al monitoreo

Público: técnicos instaladores y de soporte de IES Training, con base de redes. Nivel inicial a intermedio. 16 lecciones en 4 arcos de 4 (el pedido permitía 12 a 16 en 3 o 4 partes; el temario de centrales, comunicadores y monitoreo no entraba en 12 sin dejar huecos de obra).

Fuentes: 25 páginas en raw/web. Oficiales de Paradox: guías de instalación y programación SP+ (2022), manuales IP180 V1.00.063 (septiembre 2026), IPC10 V1.02.011 (enero 2026) e IP150M V6.50, página de la M25, tres artículos de la base de conocimiento, y copias del distribuidor FIESA de la guía EVOHD+ (2026), el manual del receptor IPR512 en español y la guía del menú instalador de BlueEye V2.0 (marzo 2025). Terceros: finmon (comunicadores), PAI (software libre de integración), foros de openHAB, Home Assistant, Fórum da Casa e IPVM, blog y guía de TremTech, ficha de CSD.

Versiones (octubre 2026): el parque instalado es Spectra SP y SP+, Magellan MG y MG+, EVO192 y EVOHD+; la línea nueva es M (M25). Los comunicadores están en transición del legado (IP150, IP150+, PCS265 V7, protocolo "TURN") a MQTT (IP180, IP150+MQ, IP150M, PCS265 V8) con receptor IPC10. Cada tarjeta dice a qué generación aplica.

Cómo leer "N de M": M son las páginas que tocan el subtema, N las que sostienen la idea. Casi todo es documentación de Paradox: el acuerdo es coherencia del fabricante, y cada lección lo dice. Donde hay una sola fuente, la tarjeta lo aclara.

## Arco 1. La central bien parada
Por qué este arco: antes de programar nada, la central tiene que estar identificada, con el bus armado, las zonas cableadas con la resistencia correcta y la energía calculada. Cierra con una central de banco que enciende sin fallas de cableado.

### Lección 1. Leer la central
- Quién lo dice: 5 de 5 (TH01).
- Idea: SP/MG programan con secciones de tres dígitos y código 0000; EVO con cuatro dígitos y 000000; la M25 se programa por app. La versión se lee en la sección 980.
- Por qué importa: la mitad de los errores de soporte es aplicar el manual de otra familia.
- Historia: SP4000 y SP65 se resetean con un puente entre PG1 y zona 1, el resto con el botón. https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/
- Laboratorio: Rápido, 10 min. Leer modelo en la placa, versión en 980, anotar en la ficha.
- Regla: antes de tocar una sección, sé qué central y qué versión tenés delante.

### Lección 2. Bus de a grupos
- Quién lo dice: 1 de 3 (TH02), 1 de 3 (TH04, TH05). Evidencia del fabricante.
- Idea: bus de 4 hilos, sin energía al conectar, de a grupos; zona de teclado; inalámbrica pisa a cableada; medir señal.
- Historia: en la EVOHD+ solo deberían aparecer pérdida de reloj y campana ausente al energizar. https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Laboratorio: Campo, 20 min. Central, K32LCD+ y ZX8 de banco; agregar de a uno; zona de teclado.
- Regla: un módulo por vez y sin energía.

### Lección 3. Resistencia al final
- Quién lo dice: 3 de 4 (TH06), 2 de 4 (TH07), 1 de 4 (TH08), 2 de 4 (TH09). Discrepa TremTech en el valor (DSC).
- Idea: EOL de 1 kΩ en 706 opción 2 para toda la central; ATZ en 705 con 1 kΩ y 2,2 kΩ solo donde el modelo lo admite (SP6000+ en la serie plus); tamper en 705; fuego normalmente abierto.
- Historia: la duda del foro sobre ATZ y tamper. https://forumdacasa.com/discussion/60287/4/alarme-paradox/
- Laboratorio: Foco, 20 min. Tester y resistencias; cablear zona con EOL y una doble con ATZ.
- Regla: una central, un criterio de resistencia, anotado en la tapa.

### Lección 4. Cuentas de energía
- Quién lo dice: 2 de 2 (TH03, TH10, TH11), evidencia fina.
- Idea: 16,5 Vac 40 VA; AUX hasta 700 mA sumados en SP5500+; batería de 7 Ah; umbrales 10,5 / 9,1 / 8,5 V; 1 kΩ en campana si no hay sirena; tierra.
- Historia: la tabla de consumos (TM70 250 mA más 80) y la autonomía de la EVOHD+. https://www.paradox.com/Downloader/?ID=11662
- Laboratorio: Admin, 15 min. Planilla de consumo y autonomía.
- Regla: si no sumaste el AUX, no energizás.

## Arco 2. Programar con método
Por qué este arco: es el trabajo de cada obra: entrar a programación sin romper, definir zonas, particiones y usuarios, y sacar salidas útiles. Cierra con una central de banco programada como una casa real con portón.

### Lección 5. Entrar con método
- Quién lo dice: 3 de 3 (TH13), 4 de 10 (TH32).
- Idea: ENTER, código, sección, dato; decimal, hexa y opciones; ENTER antes de cargar para ver; desarmado para entrar; cambiar 0000 y 1234 el primer día.
- Historia: el foro donde se sugiere entrar con códigos de fábrica a la central de otro. https://forumdacasa.com/discussion/60287/4/alarme-paradox/
- Laboratorio: Rápido, 10 min. Entrar, ver 980 y 710, cambiar 397 y 399.
- Regla: miro la sección antes de escribirla.

### Lección 6. Cada zona su tipo
- Quién lo dice: 1 de 1 (TH14, TH15, TH16), evidencia fina, solo la guía SP+.
- Idea: 001 a 032 = definición, partición, opciones. Retardo en la puerta, seguimiento en el sensor del teclado, instantánea en el perímetro, fuego no anulable; Intellizone y retardo de transmisión contra falsas alarmas.
- Historia: el sensor que mira el teclado como seguimiento. https://www.paradox.com/Downloader/?ID=11662
- Laboratorio: Foco, 20 min. Programar zonas 1 a 4 de una casa tipo.
- Regla: el tipo de zona sale del recorrido de entrada, no de la costumbre.

### Lección 7. Partición y usuarios
- Quién lo dice: 1 de 1 (TH17, TH18), evidencia fina.
- Idea: 700 opción 1; tercer dígito de la zona; usuarios 404 a 432 con opciones; coacción; 4 o 6 dígitos.
- Historia: 1234 que pasa a 123412. https://www.paradox.com/Downloader/?ID=11662
- Laboratorio: Foco, 15 min. Casa con taller: dos particiones y tres usuarios.
- Regla: cada usuario con la partición y las opciones mínimas que necesita.

### Lección 8. Salida con evento
- Quién lo dice: 2 de 2 (TH19), evidencia fina.
- Idea: activación, desactivación o tiempo, opciones; PGM1 de fábrica con el botón B del control; 100 a 150 mA, relé externo.
- Historia: los valores de fábrica de la PGM1 y PGM2 para remotos. https://www.paradox.com/Downloader/?ID=11650
- Laboratorio: Campo, 20 min. Portón por control remoto y luz de falla de AC.
- Regla: la PGM manda, el relé carga.

## Arco 3. Comunicación y monitoreo
Por qué este arco: una alarma que no avisa no sirve. Este arco conecta la central a la PC, a internet, a la receptora y a la app, sabiendo qué generación de módulo hay. Cierra con una central reportando a monitoreo y visible en BlueEye.

### Lección 9. BabyWare primero
- Quién lo dice: 2 de 4 (TH20), 1 de 4 (TH21). Discrepan los manuales nuevos en la contraseña de fábrica.
- Idea: 307USB al serie, ID de panel 910 y contraseña de PC 911 propios; el reset no los borra; el módulo atiende una conexión a la vez.
- Historia: la MG5050 recuperada por BabyWare con ID y contraseña de fábrica. https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue
- Laboratorio: Campo, 15 min. Conectar, leer, guardar copia de la programación.
- Regla: antes de cambiar nada, copia de la central en BabyWare.

### Lección 10. Comunicador por generación
- Quién lo dice: 4 de 6 (TH22), 2 de 6 (TH23), 3 de 6 (TH24).
- Idea: legado (IP150, IP150+, PCS265 V7) con IPR512 e IP estática; MQTT (IP180, IP150+MQ, IP150M, PCS265 V8) con IPC10 y BlueEye; no mezclar; puertos de salida.
- Historia: IP150M V6.50, irreversible y con Swan pago. https://www.paradox.com/Downloader/?ID=11873
- Laboratorio: Admin, 15 min. Inventario de módulo y checklist de red.
- Regla: primero sé qué generación de módulo hay, después actualizás.

### Lección 11. Abonado y receptora
- Quién lo dice: 4 de 7 (TH25), 5 de 7 (TH26), 1 de 7 (TH27). Discrepan IPR512 y la guía de instalación en SIA.
- Idea: 810 = 4 Contact ID; abonado por partición 811/812 y 918/919; receptora 929 a 935; perfiles 01 a 04; prueba 840/850.
- Historia: finmon y el abonado en las dos particiones. https://www.finmon.co.za/kb/books/gsm-communicator-programming-manual/page/paradox-mg5050-and-sp6000-programming
- Laboratorio: Foco, 20 min. Programar reporte IP y registrar con ARM.
- Regla: el abonado va en cada partición y en cada canal.

### Lección 12. La app y la nube
- Quién lo dice: 4 de 8 (TH28), 4 de 8 (TH29). Discrepa PAI sobre Swan.
- Idea: BlueEye reemplaza a Insite Gold; Swan es sitio con suscripción; IP estática con port forward en módulos legado; MQTT solo por Swan.
- Historia: el usuario que pagó Swan y a los días la app no conectaba. https://forumdacasa.com/discussion/60287/4/alarme-paradox/
- Laboratorio: Campo, 15 min. Menú instalador de BlueEye: sitio o cuenta de panel, detalles de sitio.
- Regla: antes de vender la app, explicá quién paga la suscripción y qué pasa si vence.

## Arco 4. Diagnóstico y cuidado
Por qué este arco: lo que más llamadas genera son fallas y comunicación caída, y lo que más daño hace son los códigos de fábrica. Cierra con un método de diagnóstico y una ficha de entrega.

### Lección 13. Primero el TBL
- Quién lo dice: 4 de 4 (TH30).
- Idea: TBL y sus grupos; 2.2 AC, 2.1 batería, 8 reloj, 4 comunicación, 5 tamper, 10 módulos con 955; LED de estado; 839 retrasa el reporte de AC.
- Historia: puesta en marcha EVOHD+ con solo reloj y campana. https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Laboratorio: Campo, 20 min. Provocar fallas en banco y leerlas.
- Regla: ningún diagnóstico arranca sin mirar el TBL.

### Lección 14. Cuando no reporta
- Quién lo dice: 4 de 6 (TH31).
- Idea: estado de registro en 935 con ARM; errores de programación y registro; reinicio de módulo con espera de 5 o 15 min; una conexión a la vez; hotspot del IP180.
- Historia: "cuenta ya registrada con otra MAC". https://www.paradox.com/Downloader/?ID=11650
- Laboratorio: Foco, 20 min. Recorrer la tabla de estados con errores provocados.
- Regla: de la central hacia afuera: serie, red, puertos, receptora.

### Lección 15. Llaves de la central
- Quién lo dice: 4 de 10 (TH32), 2 de 10 (TH33).
- Idea: instalador, mantenimiento, maestro, ID de panel, contraseña de PC y contraseña del módulo; bloqueo de instalador 395 = 147; qué borra el reset; camino legítimo si se perdió un código.
- Historia: IPVM, la MG5050 sin código. https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue
- Laboratorio: Admin, 15 min. Ficha de llaves y entrega al cliente.
- Regla: ninguna central sale de obra con un código de fábrica.

### Lección 16. Parque y línea M
- Quién lo dice: 1 de 1 (TH35), 1 de 10 (TH34) con PAI en contra.
- Idea: la M25 (PoE, app, reporte directo, suscripción) convive con un parque grande de SP/MG/EVO; el puerto serie bloqueado desde 7.50 con desbloqueo oficial; decidir por sitio.
- Historia: PAI pide no actualizar EVO a 7.50 si hay integración serie. https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/overview
- Laboratorio: Admin, 15 min. Matriz de decisión por sitio.
- Regla: actualizo firmware sabiendo qué integración se puede cortar.

## Divisiones
- Nube o local: Paradox empuja Swan (IP150M V6.50 lo vuelve obligatorio y pago, IP180 solo BlueEye); el KB oficial sigue documentando IP estática con port forward para módulos legado; PAI desaconseja Swan por una vulnerabilidad documentada. Decidir: con módulo MQTT no hay opción, es Swan; con legado y sin suscripción, IP estática por VPN o port forward acotado; en todos los casos, reporte a monitoreo independiente de la app.
- Contact ID o SIA: por IP/GPRS y con IPC10 solo Contact ID; SIA por línea o con IPR512 legado. Decidir según la receptora de la empresa de monitoreo.
- Puerto serie bloqueado: desde firmware 7.50 hay que comprar un desbloqueo oficial para terceros; PAI recomienda no actualizar. Decidir: si hay integración que vale, desbloqueo oficial; nunca dejar una central sin parches solo por la integración sin evaluarlo.
- Contraseña de PC de fábrica: la guía SP+ dice que BabyWare obliga a cambiar 0000; los manuales de IP180/IP150M y BlueEye siguen nombrando 0000. Decidir: tratarla como cambiada siempre, anotarla en la ficha.
- Configuración del módulo: IP150+ desde 5.3.0 e IP180 solo por BlueEye; IP150 viejo y red cerrada por web. Decidir según firmware.

## Huecos
- Zonas, particiones y usuarios con una sola fuente (guía SP+). EVO tiene secciones de 4 dígitos y más opciones que no se cubren en detalle.
- PCS265 (LTE, V7, V8) sin manual propio leído.
- Magellan inalámbrico (MG5050, RTX3, sensores) y teclados K656/K641+ sin manual propio leído.
- Manual de la M25 no leído (solo la página de producto).
- No se pudieron leer foros grandes de instaladores (bloquean scripts); no hay voces de practicantes en español.

## Entrega
16 carpetas en class/ con script.txt, card.md y quiz.json; course.json con la ficha. Sin audio: el portal muestra el guion como "La charla".
