# Notes: batch a
Pages read: 25. With notes: 23. Skipped: 2 (forumdacasa página 5 casi todo fuera de tema, salvo una mención al 307USB; el foro de Home Assistant solo aporta el puerto 10000 del IP150, que ya aparece en otras fuentes).

Fuentes (url exacta):
- SPI = https://www.paradox.com/Downloader/?ID=11662 (SP5500+/SP6000+/SP7000+ Installation Guide, 2022)
- SPP = https://www.paradox.com/Downloader/?ID=11650 (SP+ Programming Guide, 2022)
- IP180 = https://www.paradox.com/Downloader/?ID=12435 (IP180 V1.00.063, sept. 2026)
- IPC10 = https://www.paradox.com/Downloader/?ID=12343 (IPC10 V1.02.011, ene. 2026)
- IP150M = https://www.paradox.com/Downloader/?ID=11873 (IP150M V6.50.000, sept. 2024)
- M25 = https://www.paradox.com/web/product/m25-m25-lte/
- EVO = https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf (EVOHD+ Installation Guide, copia FIESA, 2026)
- IPR = https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Receptoras/Manual_IPR512.pdf (IPR512 V2.0, español, 2010)
- BEI = https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf (marzo 2025)
- K32 = https://store.tremtech.com/content/K32LCDPlus_Installation_Guide_En.pdf
- KBIP = https://support.paradox.com/portal/en/kb/articles/how-can-i-add-a-static-ip-site-in-blueeye
- KBSW = https://support.paradox.com/portal/en/kb/articles/i-cannot-connect-to-my-site-what-should-i-do
- KBWEB = https://support.paradox.com/portal/en/kb/articles/i-cannot-configure-the-ip150-anymore-from-the-web-interface-18-11-2022
- FIN = https://www.finmon.co.za/kb/books/gsm-communicator-programming-manual/page/paradox-mg5050-and-sp6000-programming
- PAI = https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/ip150
- PAIO = https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/overview
- OH3 = https://community.openhab.org/t/help-build-binding-for-paradox-alarm-panel-with-ip150/1712?page=3
- OH28 = https://community.openhab.org/t/paradox-evo-binding/58026?page=28
- HA = https://community.home-assistant.io/t/paradox-security-system/30004
- FC4 = https://forumdacasa.com/discussion/60287/4/alarme-paradox/
- FC5 = https://forumdacasa.com/discussion/60287/5/alarme-paradox/
- TTW = https://blog.tremtech.com/blog/how-to-wire-security-alarm-zones/
- TTR = https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/
- CSD = https://www.csd.com.au/products/PDX-IP150+
- IPVM = https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue

## T01 Líneas de centrales
- a:N1. SP+ (SP5500+, SP6000+, SP7000+): 32 zonas (cableadas, de teclado o inalámbricas), 32 usuarios, 2 particiones, hasta 15 módulos en el bus de 4 hilos, zonas en placa 5, 8 y 16 respectivamente. Versión 433 o 868 MHz.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Connect up to 15 hardwired bus modules on the 4-wire communication bus"
  - Kind: definition · Level: foundation
- a:N2. EVOHD+: 8 zonas en placa (16 con duplicación), ampliable a 192 por bus Digiplex, 999 usuarios, 8 particiones, 32 puertas, hasta 254 módulos, módulos hasta 914 m de la central.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf  Quote: "expandable to 192 zones via the 4-wire Digiplex bus"
  - Kind: definition · Level: foundation · Also: T02
- a:N3. Línea nueva M25 / M25 LTE: consola híbrida con PoE, 200 zonas, 10 particiones, 128 usuarios, inalámbrico M (914 u 868 MHz), reporte directo a la receptora en hasta 4 canales "sin dependencia de la nube", programación por BlueEye o software web; los servicios nube (Swan 4G) requieren suscripción.
  - Source: https://www.paradox.com/web/product/m25-m25-lte/  Quote: "Safe direct reporting to CMS up to 4 channels without cloud dependency"
  - Kind: definition · Level: core · Also: T16
  - Bias: página de producto del fabricante.
- a:N4. En la línea M el alta la hace un instalador registrado con ID de empresa de servicio (PCI) y existe un "Service Company Lock" que se activa con la suscripción Swan.
  - Source: https://www.paradox.com/web/product/m25-m25-lte/  Quote: "Service Company Lock Auto-enabled with Swan subscription"
  - Kind: definition · Level: advanced · Also: T15
- a:N5. MG5050 y SP6000 comparten el mapa de secciones de reporte (810, 811, 812, 815, 817): un mismo instructivo de monitoreo sirve para ambas.
  - Source: https://www.finmon.co.za/kb/books/gsm-communicator-programming-manual/page/paradox-mg5050-and-sp6000-programming  Quote: "Paradox MG5050 and SP6000 Programming"
  - Kind: rule of thumb · Level: foundation · Also: T11
  - Bias: empresa de comunicadores GSM (finmon) que vende su propio equipo.
- a:N6. SP4000 y SP65 son la gama baja con procedimiento de reseteo distinto (puente entre PG1 y zona 1, con el bloqueo de instalador apagado); el resto de SP y MG se resetea con el botón.
  - Source: https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/  Quote: "For SP4000 / SP65 panels: Verify that the installer lock is disabled."
  - Kind: technique · Level: core · Also: T15
  - Bias: tienda (TremTech) que vende Paradox.

## T02 Bus, teclados y expansores
- a:N7. Consumos de módulos en el bus: K32+ hasta 148 mA, K32LCD+ hasta 86 mA, K35 hasta 70 mA, K636 hasta 30 mA, TM50 150 mA más 80 de sirena, TM70 250 mA más 80, ZX8 31 mA, IP150+ 100 mA, PCS265LTE hasta 300 mA.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Modules Current Consumption List"
  - Kind: number · Level: core · Also: T04
- a:N8. Antes de conectar un módulo al bus Digiplex, sacar AC y batería; bus en estrella o cadena, total hasta 914 m; en ambientes ruidosos cable blindado con la malla a tierra de un solo lado.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf  Quote: "Before connecting a module to the Digiplex bus, remove AC and battery power"
  - Kind: rule of thumb · Level: foundation
- a:N9. Puesta en marcha recomendada: conectar un grupo chico de módulos con un teclado, dar energía, entrar a la sección [4000]; solo deberían aparecer las fallas de pérdida de reloj y campana ausente; seguir de a grupos; usar el voltímetro del teclado LCD en distintos puntos.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf  Quote: "Only the Clock Loss trouble and/or Bell Absent trouble should appear."
  - Kind: technique · Level: core · Also: T13
- a:N10. Zona de teclado: cada teclado tiene una entrada; en SP+ se asigna con ENTER, código de instalador, mantener la tecla de acción tres segundos y número de zona de dos dígitos (K32+, K32LCD+). En EVO la zona de teclado no admite ATZ ni reconoce tamper.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Configuring the Keypad Zone Number"
  - Kind: technique · Level: core · Also: T03
- a:N11. En la tabla de reconocimiento de zonas, una zona inalámbrica pisa a una de teclado o cableada en el mismo número, y una de teclado pisa a una cableada.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "a wireless zone will overwrite a keypad/hardwire zone"
  - Kind: mistake · Level: core · Also: T06
- a:N12. Fuerza de señal de inalámbricos y PGM inalámbricas: 8 a 10 (3 pitidos) es buena, 1 a 4 (1 pitido) conviene reubicar.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "1 to 4 / 1 beep = Weak signal (Relocate)"
  - Kind: test · Level: core
- a:N13. En la línea M no hay bus de 4 hilos: la M25 suma hasta 75 nodos inalámbricos (máximo 4 repetidores) y hasta 45 dispositivos por Ethernet, y los agrega por autoaprendizaje, QR o número de serie.
  - Source: https://www.paradox.com/web/product/m25-m25-lte/  Quote: "Ethernet Expansion Devices Up to 45"
  - Kind: definition · Level: advanced · Also: T16

## T03 Cableado de zonas
- a:N14. EOL en SP+: sección [706] opción 2; vale para todas las zonas de la central y usa resistencias de 1 kΩ. Por defecto está apagada (zonas NC sin resistencia).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "require 1K end of line resistors, enable option [2] in section [706]"
  - Kind: technique · Level: foundation
- a:N15. ATZ (duplicación de zona): sección [705] opción 1; en la serie plus solo la SP6000+; [705] opción 2 elige serie o paralelo. En el dibujo del manual EVOHD+, el detector 1 va con 1 kΩ y el detector 2 con 2,2 kΩ sobre el mismo par.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "ATZ is only supported on the SP6000+."
  - Kind: technique · Level: core
  - Also: EVO (figura 9 del manual EVOHD+)
- a:N16. Tamper: [705] opciones 3 y 4 definen si un tamper de zona da solo falla, alarma audible desarmado o sigue el tipo de alarma armado; [705] opción 5 hace que los tampers de zonas anuladas igual se vean (por defecto encendida).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Will generate a tamper if detected on a bypassed zone (default)"
  - Kind: technique · Level: core · Also: T13
- a:N17. Con ZX8/ZX82 se puede convertir la primera zona de cada expansor en entrada de tamper ([706] opciones 4, 5 y 6).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Tamper Input on ZX8/ZX82 ID A (Panel + 1)"
  - Kind: technique · Level: advanced
- a:N18. Zonas de fuego: quedan normalmente abiertas y con EOL; en SP+ la zona 1 puede volverse entrada de humo de 2 hilos ([706] opción 3); reset con CLEAR más ENTER tres segundos; en 4 hilos se corta la alimentación del detector con una PGM.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "the zone becomes normally open and requires an EOL resistor"
  - Kind: technique · Level: core · Also: T08
- a:N19. Comparación genérica: NC sin EOL no supervisa corte ni cortocircuito; una EOL detecta corto; doble EOL distingue normal, violada, corte y corto. Ojo que los valores del ejemplo (5,6 kΩ) son de DSC, no de Paradox.
  - Source: https://blog.tremtech.com/blog/how-to-wire-security-alarm-zones/  Quote: "Normally Closed Loops (no EOL – not recommended)"
  - Kind: rule of thumb · Level: foundation
  - Bias: tienda.
- a:N20. Un usuario de foro pregunta si con ATZ puede poner dos tamper en la misma zona y si sin ATZ hacen falta resistencias: la duda típica de quien cablea por primera vez una SP6000.
  - Source: https://forumdacasa.com/discussion/60287/4/alarme-paradox/  Quote: "Caso nao active o ATZ é necessário resistências"
  - Kind: story · Level: foundation

## T04 Alimentación
- a:N21. Transformador de 16,5 Vac y 40 VA mínimo, sin enchufe con llave; batería de 12 V 4 o 7 Ah; con la batería al revés se quema el fusible de batería.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "rated output voltage of 16.5 Vac and rated power of 40 VA (minimum)"
  - Kind: rule of thumb · Level: foundation
- a:N22. Umbrales de batería en SP+: falla de batería baja a 10,5 V; desconexión de protección a 9,1 V; apagado total a 8,5 V; señal de falla si la salida baja de 11,3 V.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "At 8.5V or lower, the panel shuts down"
  - Kind: number · Level: core · Also: T13
- a:N23. Salida auxiliar: protección sin fusible que corta a 1,1 A en SP5500+; el consumo combinado conviene que no pase de 700 mA; si corta, desconectar todas las cargas al menos 10 segundos.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "should not exceed 700mA"
  - Kind: number · Level: core · Also: T13
- a:N24. Salida de campana: 12 V, una sirena de 30 W o dos de 20 W, corta a 3 A; si no se usa, una resistencia de 1 kΩ entre BELL+ y BELL- evita la falla de campana desconectada.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "connect a 1K resistor across the BELL terminals"
  - Kind: technique · Level: foundation · Also: T13
- a:N25. EVOHD+: tabla de autonomía, con 7 Ah y 130 mA de accesorios da 30 h de respaldo; con 17 Ah, 470 mA para 30 h. Batería baja a 11,7 V.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf  Quote: "7AHr 130mA"
  - Kind: number · Level: core
- a:N26. Tierra: los bornes de tierra de zonas y de discador a la caja metálica y a caño de agua o jabalina; para rayos, tierras separadas.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "use separate earth grounds for the zone and dialer grounds"
  - Kind: rule of thumb · Level: foundation

## T05 Programación por teclado
- a:N27. SP/MG: ENTER, código de instalador (fábrica 0000), sección de tres dígitos, datos. Código de mantenimiento vacío de fábrica; maestro del sistema 1234. El de mantenimiento no toca comunicación ([395], [397], [398], [815] a [817], [910], [911], [918] a [949]).
  - Source: https://www.paradox.com/Downloader/?ID=11650  Quote: "The default installer code is 0000."
  - Kind: definition · Level: foundation · Also: T15
- a:N28. EVO/EVOHD+: mantener la tecla 0, código de instalador (fábrica 000000), sección de cuatro dígitos.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf  Quote: "Key in the [INSTALLER CODE] (default = 000000)"
  - Kind: definition · Level: foundation
- a:N29. Tres formas de cargar datos: dígito a dígito decimal (000 a 255), hexadecimal (0 cuenta como A, y teclas de función para B a F) y selección de opciones 1 a 8 con ENTER para guardar. CLEAR sale sin guardar. ENTER antes de cargar entra a modo visualización.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Feature Select Programming Method"
  - Kind: technique · Level: foundation
- a:N30. Para entrar a programación las particiones tienen que estar desarmadas y StayD apagado; [980] muestra la versión de la central dígito a dígito.
  - Source: https://www.paradox.com/Downloader/?ID=11650  Quote: "all zones must be disarmed and StayD mode deactivated"
  - Kind: mistake · Level: foundation
- a:N31. Los manuales recomiendan TM50/TM70 para programar; en SP+ el teclado sale de programación a los cinco minutos.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "after five minutes, the keypad exits programming mode"
  - Kind: rule of thumb · Level: foundation

## T06 Definición de zonas
- a:N32. Secciones [001] a [032]: dos dígitos de definición (01 retardo 1, 05 seguimiento, 08 instantánea, 11 fuego instantáneo, 16 robo 24 h, 22 pánico 24 h...), un dígito de partición (1, 2 o 3 para ambas) y opciones 1 a 8.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "There are 26 available Zone Definitions."
  - Kind: template · Level: foundation
- a:N33. Tiempos de fábrica en SP+: retardo de entrada 1 y 2 de 45 s ([710], [711]); salida 60 s ([745] y [746] por partición); corte de campana 4 min ([747]); Flex-Instant 15 s ([720]).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Default = 45 seconds"
  - Kind: number · Level: foundation
- a:N34. Seguimiento es para el sensor que cuida el teclado: si primero abre la puerta de retardo, espera; si abre solo, dispara.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "commonly used when a motion detector is protecting the area occupied by the entry point keypad"
  - Kind: rule of thumb · Level: foundation
- a:N35. Contra falsas alarmas: Intellizone (48 s por defecto en [713]) y retardo de transmisión ([833]) que suena pero no reporta si se desarma a tiempo; apagado automático de zona tras 5 alarmas ([712]).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "This feature reduces the possibility of false alarms."
  - Kind: technique · Level: core
- a:N36. Una zona de fuego no se puede anular.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "A fire zone cannot be bypassed."
  - Kind: rule of thumb · Level: foundation

## T07 Particiones y usuarios
- a:N37. Particionado en [700] opción 1; sin particionar, todo es partición 1 y las zonas asignadas a la 2 dejan de funcionar; zonas en ambas particiones se arman cuando las dos están armadas.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Zones that have been manually assigned to partition 2 will no longer function."
  - Kind: mistake · Level: core
- a:N38. Opciones de usuario [404] a [432]: 1 y 2 particiones, 3 anulación, 4 Stay/Sleep, 5 forzado, 6 solo armar, 7 solo PGM, 8 coacción. Un usuario sin partición 1 en un sistema no particionado queda deshabilitado.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "the user access code will be considered disabled"
  - Kind: template · Level: core · Also: T08
- a:N39. Largo de código 4 o 6 dígitos ([701] opción 1); al pasar a 6, la central completa con los dos primeros dígitos (1234 pasa a 123412).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "the code will become 123412"
  - Kind: mistake · Level: core

## T08 PGM y salidas
- a:N40. Cada PGM tiene evento de activación y de desactivación (grupo, subgrupo, partición), temporizador [281] a [296] (5 s por defecto) y opciones [261] a [276] (base en segundos o minutos, NA o NC, pulso).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Default = 5 seconds"
  - Kind: template · Level: core
- a:N41. Por defecto la PGM1 se activa con el botón B de cualquier control remoto (08/99/99) y la PGM2 con el C: el caso típico de portón.
  - Source: https://www.paradox.com/Downloader/?ID=11650  Quote: "PGM 1 activation event: default = option B remote assignment"
  - Kind: definition · Level: core
- a:N42. Las PGM en placa son salidas de baja corriente (100 a 150 mA): para un portón o una sirena extra, relé externo; si se alimentan del AUX, entran en la cuenta de 700 mA.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "All on-board PGMS are 100 mA low-current outputs"
  - Kind: rule of thumb · Level: core · Also: T04
- a:N43. Eventos útiles de la lista: 44/01 falla de AC, 44/06 pérdida de reloj, 02/12 armado de partición, 06/01 CLEAR más ENTER (reset de humo), 36 zona en alarma.
  - Source: https://www.paradox.com/Downloader/?ID=11650  Quote: "Clock loss"
  - Kind: template · Level: core

## T09 BabyWare y conexión local
- a:N44. BabyWare conecta local con 307USB (o CV4USB) al puerto serie, o remoto por IP o PCS; verifica ID de panel [910] y contraseña de PC [911]; en la primera conexión obliga a cambiarlos si siguen en 0000.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Upon first connection, BabyWare will force a change to the default value if previously set to 0000."
  - Kind: technique · Level: core
- a:N45. El reseteo por botón vuelve todo a fábrica salvo ID de panel y contraseña de PC, y no borra el buffer de eventos.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "except for the Panel ID and PC Password"
  - Kind: definition · Level: core · Also: T15
- a:N46. Practicante: para recuperar el acceso a una MG5050 sin el código de instalador, conectar con BabyWare usando ID de panel y contraseña de PC (si siguen de fábrica) por cable serie o IP150; otro responde con los códigos de fábrica 0000/000000.
  - Source: https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue  Quote: "Different to installer code and installer lock"
  - Kind: story · Level: core · Also: T15
- a:N47. El módulo IP150 acepta una conexión a la vez: si una integración está conectada, BabyWare o la app quedan afuera.
  - Source: https://community.openhab.org/t/help-build-binding-for-paradox-alarm-panel-with-ip150/1712?page=3  Quote: "it only allows 1 connection at a time"
  - Kind: mistake · Level: core · Also: T14
  - Bias: foro de domótica, su claim.
- a:N48. El puerto de software del IP150 es el 10000 (también por defecto en [920] y en los receptores).
  - Source: https://community.home-assistant.io/t/paradox-security-system/30004  Quote: "usually port 10000"
  - Kind: number · Level: core · Also: T10

## T10 Comunicadores
- a:N49. IP180: Ethernet y Wi-Fi, MQTT, reporta solo a IPC10/VIPC20 en Contact ID, solo con BlueEye (Insite Gold no conecta), va en el serie 1 de las plus; PCS265 V8 en el serie 2; no mezclar MQTT con legado.
  - Source: https://www.paradox.com/Downloader/?ID=12435  Quote: "Do not mix MQTT reporting devices and Legacy reporting versions."
  - Kind: rule of thumb · Level: core · Also: T11
- a:N50. Puertos que el IP180/IP150M necesitan abiertos de salida: UDP 53, UDP 123, UDP 5683, TCP 8883 (MQTT, Swan e IPC10), TCP 443 (firmware), 465/587 correo.
  - Source: https://www.paradox.com/Downloader/?ID=12435  Quote: "TCP 8883 MQTT port SWAN and IPC10/VIPC20 converter"
  - Kind: template · Level: core · Also: T14
- a:N51. IP150M (IP150 pasado a MQTT, V6.50): exige sitio Swan pago para toda comunicación, incluido BabyWare remoto; la actualización es irreversible; Insite Gold no conecta.
  - Source: https://www.paradox.com/Downloader/?ID=11873  Quote: "PAID Swan SITE required with IP150 V6.50.000 for all communications"
  - Kind: number · Level: advanced · Also: T12
- a:N52. IP150+ (legado): reemplazo directo del IP150, actualización segura con vuelta atrás, sondeo a Swan cada 15 min, opción de deshabilitar Swan en redes cerradas, reporta al IPR512.
  - Source: https://www.csd.com.au/products/PDX-IP150+  Quote: "Swan disable feature for communication in closed networks"
  - Kind: definition · Level: core · Also: T12
  - Bias: distribuidor que lo vende.
- a:N53. Desde firmware 5.3.0 el IP150+ se configura solo desde el menú instalador de BlueEye, no por la web.
  - Source: https://support.paradox.com/portal/en/kb/articles/i-cannot-configure-the-ip150-anymore-from-the-web-interface-18-11-2022  Quote: "can be done only from BlueEye Installer Menu, for firmware 5.3.0 and up"
  - Kind: definition · Level: core · Also: T12
- a:N54. Menú instalador de BlueEye: módulos TURN (IP150, IP150+, PCS265LTE) y MQTT no conviven en la misma central; los MQTT reportan solo a IPC10 (no a IPRS-7/IPR512) y no admiten conexión por IP estática.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf  Quote: "MQTT modules report only to IPC10 receiver (not compatible with IPRS7/IPR512)"
  - Kind: rule of thumb · Level: core · Also: T11, T12

## T11 Reporte a monitoreo
- a:N55. Formato por número de receptora en [810] (4 = Contact ID, 5 = SIA); abonado por partición [811]/[812] (4 dígitos hexa, o 3 con SLEEP); teléfonos [815], [816], respaldo [817]. SIA no está soportado por GPRS/IP.
  - Source: https://www.paradox.com/Downloader/?ID=11650  Quote: "SIA is not supported with GPRS/IP reporting"
  - Kind: template · Level: core
- a:N56. Receta de campo para MG5050/SP6000: 810 = 44 para Contact ID, abonado en 811 y 812, y si no disca revisar opciones de [800], [802], [803] y [805]; tras reprogramar sin éxito, a veces hace falta default y reprogramar.
  - Source: https://www.finmon.co.za/kb/books/gsm-communicator-programming-manual/page/paradox-mg5050-and-sp6000-programming  Quote: "Account number issues: MUST be entered at both 811 and 812"
  - Kind: technique · Level: core
  - Bias: fabricante de comunicador de terceros.
- a:N57. Reporte IP en SP/MG: abonados IP [918]/[919], receptor 1 en [929] (IP), [930] (puerto 10000), [933] contraseña (123456 de fábrica, legado), [934] perfil, [935] ARM para registrar; tabla de estados de registro con errores (sin IP, sin puerto, cuenta ya registrada con otra MAC).
  - Source: https://www.paradox.com/Downloader/?ID=11650  Quote: "Account already registered under another MAC address"
  - Kind: template · Level: core · Also: T14
- a:N58. Con IPC10 no hace falta contraseña de receptor; perfiles de supervisión fijos: 01 = 1200 s, 02 = 600 s, 03 = 300 s, 04 = 90 s. Reporte solo en Contact ID ([810] = 4 en MG/SP, [3070] = 5 en EVO).
  - Source: https://www.paradox.com/Downloader/?ID=12435  Quote: "Converter password is not needed with IPC10/VIPC20"
  - Kind: template · Level: core
- a:N59. IPC10: hasta 5000 cuentas, buffer de 20 000 eventos si cae la receptora, salida a software de monitoreo en MLR2-DG, Ademco 685 o CID-TCP, web en puerto 8080, alimentación PoE, funciona en red cerrada.
  - Source: https://www.paradox.com/Downloader/?ID=12343  Quote: "Up to 5,000 supervised accounts"
  - Kind: number · Level: core
- a:N60. IPR512 (receptor legado): hasta 512 centrales, dos WAN para dos proveedores, CID y SIA, hasta 32 perfiles con tiempo de sondeo y período de gracia, salida a software de monitoreo emulando Radionics 6500, Ademco 685 o Sur-Gard MLR2-DG. Para registrar, la receptora le da al instalador: abonado por partición, IP y puerto, contraseña y perfil.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Receptoras/Manual_IPR512.pdf  Quote: "la estación receptora debe proveer al instalador con la siguiente información"
  - Kind: template · Level: core
- a:N61. Prueba automática: [840] cada cuántos días y [850] a qué hora, con el código en [875].
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Auto Test Report"
  - Kind: technique · Level: core
- a:N62. AC: la central espera el retardo de reporte de falla de energía ([839], 15 minutos por defecto) antes de mandar el código de AC.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Default = 15 minutes"
  - Kind: number · Level: core · Also: T13

## T12 App y nube
- a:N63. Insite Gold quedó reemplazada por BlueEye; los sitios se pasan sin costo; HD78/88 no están en BlueEye; BlueEye tiene un botón de reinicio de conexión.
  - Source: https://support.paradox.com/portal/en/kb/articles/i-cannot-connect-to-my-site-what-should-i-do  Quote: "We have released a new app called BlueEye"
  - Kind: definition · Level: core
- a:N64. IP estática sin Swan en BlueEye: "Use Static IP without Swan", buscar el IP150, IP local y puerto, y para afuera un port forward al puerto de software del módulo; en firmware 1.xx y 4.0.4 la contraseña del módulo tiene que estar en "paradox" de fábrica.
  - Source: https://support.paradox.com/portal/en/kb/articles/how-can-i-add-a-static-ip-site-in-blueeye  Quote: "a port forward needs to be done on the IP150/+ software port"
  - Kind: technique · Level: core
- a:N65. Crear sitio Swan desde el menú instalador exige un comunicador conectado a la central y a internet; se puede deshabilitar el sondeo Swan solo en cuentas de panel sin sitio; borrar el sitio de la app no lo borra del servidor.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf  Quote: "Deleting sites from BlueEye (Installer Menu or Site List) does not delete the site from the Swan server."
  - Kind: technique · Level: core
- a:N66. Historia de foro: un usuario pasó su IP150 a Swan con Insite Gold, pagó, y a los días la app dejó de conectar "con el servidor Swan"; terminó dependiendo de la empresa instaladora.
  - Source: https://forumdacasa.com/discussion/60287/4/alarme-paradox/  Quote: "A minha app deixou de ligar e nao comunica com o swan server"
  - Kind: story · Level: core · Also: T14
- a:N67. El proyecto PAI no recomienda Swan y cita una vulnerabilidad documentada en la infraestructura nube de Paradox; recomienda conexión directa al IP150 (firmware menor a 4.0 o 4.40.004 en adelante).
  - Source: https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/ip150  Quote: "The PAI project does not recommend using SWAN."
  - Kind: number · Level: advanced · Also: T15
  - Bias: proyecto de software libre que compite con la app oficial.

## T13 Pantalla de fallas
- a:N68. Tecla TBL: 1 batería baja de inalámbricos; 2 energía (2.1 batería de la central, 2.2 falla de AC, 2.3 sobrecarga AUX); 3 campana; 4 comunicación; 5 tamper y cableado de zona; 6 tamper de módulo; 7 lazo de fuego; 8 pérdida de reloj; 9 supervisión de inalámbricos; 10 supervisión de módulos (la del bus de teclados se limpia en [955]).
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "[8] Timer loss"
  - Kind: template · Level: core
- a:N69. La sección [955] limpia fallas de módulos de bus: después de sacar un módulo, la falla queda hasta borrarla ahí; el reset no la limpia.
  - Source: https://www.paradox.com/Downloader/?ID=11650  Quote: "Clears bus module troubles."
  - Kind: technique · Level: core
- a:N70. LED de estado de la placa: un destello por segundo normal; un segundo encendido y uno apagado, hay falla.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Flashes ON 1 sec. and OFF 1 sec.: Any trouble"
  - Kind: test · Level: foundation
- a:N71. K32LCD+: la pantalla muestra las fallas; TBL y flechas para recorrerlas.
  - Source: https://store.tremtech.com/content/K32LCDPlus_Installation_Guide_En.pdf  Quote: "The LCD screen will display all troubles when they occur."
  - Kind: technique · Level: foundation

## T14 Fallas de comunicación
- a:N72. Si la app no conecta, el menú instalador de BlueEye permite reiniciar el módulo; puede tardar hasta 5 minutos (firmware 4.xx) o 15 (5.xx) hasta el próximo sondeo.
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf  Quote: "it can take up to 15 minutes"
  - Kind: number · Level: core
- a:N73. IP180 sin Ethernet abre un hotspot "IP180" más número de serie en 192.168.180.1 para cargar el Wi-Fi; si están Ethernet y Wi-Fi, usa uno solo.
  - Source: https://www.paradox.com/Downloader/?ID=12435  Quote: "the IP180 will open a Hotspot"
  - Kind: technique · Level: core
- a:N74. Integración EVO: el binding falló por la contraseña de PC (no la del panel), y funcionaba con IP100; el sondeo por intervalos da demora.
  - Source: https://community.openhab.org/t/paradox-evo-binding/58026?page=28  Quote: "I did not know that there can be other password"
  - Kind: story · Level: advanced · Also: T15
  - Bias: foro de domótica.

## T15 Seguridad y mantenimiento
- a:N75. Bloqueo de instalador: [395] = 147; con eso el reseteo por botón no borra la programación; se quita con 000.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Program 147 into section [395] to lock all programming."
  - Kind: definition · Level: core
- a:N76. Desde firmware 7.50 en EVO (y luego en las plus) el puerto serie solo trabaja con dispositivos Paradox; para terceros hay un código de desbloqueo pago (5 USD) que se compra en BlueEye y se carga en [300] (MG/SP+) o [3000] (EVO).
  - Source: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf  Quote: "Each unlock code can be purchased for $5 USD."
  - Kind: number · Level: advanced
- a:N77. PAI advierte no actualizar EVO a 7.50.000 o superior si se usa conexión serie con su software.
  - Source: https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/overview  Quote: "Do not upgrade EVO to 7.50.000+"
  - Kind: mistake · Level: advanced
- a:N78. Bloqueo de teclado: tras N códigos inválidos ([717]) se bloquean los teclados por [716] minutos y se reporta.
  - Source: https://www.paradox.com/Downloader/?ID=11662  Quote: "Keypad Lockout Feature"
  - Kind: technique · Level: core
- a:N79. En un foro, usuarios sugieren entrar a BabyWare "con los códigos de fábrica" a una central instalada por otro: muestra el riesgo de dejar ID de panel y contraseña de PC de fábrica.
  - Source: https://forumdacasa.com/discussion/60287/4/alarme-paradox/  Quote: "entrar com os códigos de defeitos"
  - Kind: story · Level: core

## T16 Línea M
- (ver a:N3, a:N4, a:N13)

## Disagreements seen
- Acceso remoto: Paradox empuja Swan (y con IP150M V6.50 lo hace obligatorio y pago, https://www.paradox.com/Downloader/?ID=11873) mientras su propio KB sigue documentando IP estática con port forward (https://support.paradox.com/portal/en/kb/articles/how-can-i-add-a-static-ip-site-in-blueeye) y PAI recomienda evitar Swan (https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/ip150).
- Formato: el manual de instalación SP+ dice que soporta SIA a la receptora (https://www.paradox.com/Downloader/?ID=11662), pero la guía de programación aclara que SIA no va por GPRS/IP (https://www.paradox.com/Downloader/?ID=11650) y los módulos MQTT reportan solo Contact ID (https://www.paradox.com/Downloader/?ID=12435). El IPR512 legado sí acepta SIA (https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Receptoras/Manual_IPR512.pdf).
- Contraseña de PC: la guía SP+ dice que BabyWare obliga a cambiar 0000 en la primera conexión; los manuales de IP180/IP150M y BlueEye siguen diciendo "por defecto 0000".
- Puerto serie: Paradox lo bloquea para terceros desde firmware 7.50 con desbloqueo pago (BEI); PAI recomienda no actualizar (PAIO).
- EOL: el blog de TremTech explica EOL con valores DSC (5,6 kΩ); Paradox usa 1 kΩ y 2,2 kΩ con ATZ.

## Best stories
- EVOHD+: en la puesta en marcha solo deberían aparecer pérdida de reloj y campana ausente; cualquier otra falla es cableado: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- El usuario que pagó Swan y a los tres días la app no conectaba: https://forumdacasa.com/discussion/60287/4/alarme-paradox/
- El código que pasa de 1234 a 123412 al cambiar a 6 dígitos: https://www.paradox.com/Downloader/?ID=11662
- La MG5050 sin código de instalador que se recupera por BabyWare con ID y contraseña de fábrica: https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue
- IP150M: actualizar a MQTT es irreversible y exige sitio Swan pago: https://www.paradox.com/Downloader/?ID=11873
