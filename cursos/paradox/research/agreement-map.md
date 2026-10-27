# Mapa de acuerdos: Alarmas Paradox

Cómo leer "N de M": M son las páginas con al menos una nota en el subtema del tema (incluidas las líneas Also), N las que sostienen la idea. Muchas páginas son documentación del mismo fabricante: ahí el acuerdo indica coherencia de Paradox, no consenso independiente. Temas con M menor a 3 llevan "evidencia fina".

M por subtema: T01 = 5, T02 = 3, T03 = 4, T04 = 2, T05 = 3, T06 = 1, T07 = 1, T08 = 2, T09 = 4, T10 = 6, T11 = 7, T12 = 8, T13 = 4, T14 = 6, T15 = 10, T16 = 1.

## TH01 Identificá familia y versión antes de programar (SP/MG con secciones de 3 dígitos, EVO con 4, M por app)
- Sub-topic: T01 (also T05)
- Agree: 5 de 5. Notes: a:N1, a:N2, a:N3, a:N5, a:N6, a:N28. Urls: https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf, https://www.paradox.com/web/product/m25-m25-lte/, https://www.finmon.co.za/kb/books/gsm-communicator-programming-manual/page/paradox-mg5050-and-sp6000-programming, https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/
- Disagree: none found
- Level: foundation
- Best story: SP4000 y SP65 se resetean distinto que el resto de la familia SP/MG (https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/)

## TH02 Armá el bus de a grupos y verificá en cada paso
- Sub-topic: T02 (also T13)
- Agree: 1 de 3. Notes: a:N8, a:N9. Urls: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: core
- Best story: en la puesta en marcha de una EVOHD+ solo deberían aparecer pérdida de reloj y campana ausente.

## TH03 Sumá el consumo de todo lo que cuelga de AUX antes de energizar
- Sub-topic: T04 (also T02, T08). Evidencia fina.
- Agree: 2 de 2. Notes: a:N7, a:N23, a:N25, a:N42. Urls: https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: core
- Best story: si el AUX corta por sobrecarga, la SP+ pide desconectar todo 10 segundos antes de reconectar.

## TH04 Una zona inalámbrica pisa a una de teclado o cableada con el mismo número
- Sub-topic: T02 (also T06)
- Agree: 1 de 3. Notes: a:N11. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: core

## TH05 Medí la señal del inalámbrico antes de fijarlo
- Sub-topic: T02
- Agree: 1 de 3. Notes: a:N12. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: core

## TH06 Usá EOL de 1 kΩ y decidilo para toda la central
- Sub-topic: T03
- Agree: 3 de 4. Notes: a:N14, a:N15, a:N19. Urls: https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf, https://blog.tremtech.com/blog/how-to-wire-security-alarm-zones/
- Disagree: https://blog.tremtech.com/blog/how-to-wire-security-alarm-zones/: explica EOL con valores de DSC (5,6 kΩ), no de Paradox; coincide en el principio, no en el valor.
- Level: foundation

## TH07 ATZ duplica la entrada (1 kΩ y 2,2 kΩ) solo en los modelos que lo admiten
- Sub-topic: T03
- Agree: 2 de 4. Notes: a:N15, a:N10. Urls: https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: core
- Best story: un usuario de foro pregunta si con ATZ entra un segundo tamper y si sin ATZ hacen falta resistencias (https://forumdacasa.com/discussion/60287/4/alarme-paradox/)

## TH08 Definí qué hace un tamper armado y desarmado, también en zonas anuladas
- Sub-topic: T03 (also T13)
- Agree: 1 de 4. Notes: a:N16, a:N17. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: core

## TH09 Zona de fuego: normalmente abierta, con EOL, no anulable, reset con CLEAR más ENTER
- Sub-topic: T03 (also T06, T08)
- Agree: 2 de 4. Notes: a:N18, a:N36. Urls: https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: core

## TH10 Transformador de 16,5 Vac 40 VA y batería de 7 Ah, con los umbrales a mano
- Sub-topic: T04. Evidencia fina.
- Agree: 2 de 2. Notes: a:N21, a:N22, a:N25. Urls: https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: foundation
- Best story: SP+ marca batería baja a 10,5 V y se apaga a 8,5 V.

## TH11 Si no hay sirena, resistencia de 1 kΩ en la salida de campana
- Sub-topic: T04 (also T13). Evidencia fina.
- Agree: 2 de 2. Notes: a:N24. Urls: https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: foundation

## TH12 Tierra de zonas y discador a la caja y a jabalina
- Sub-topic: T04. Evidencia fina.
- Agree: 1 de 2. Notes: a:N26. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: foundation

## TH13 Entrá a programación con método y mirá la sección antes de cambiarla
- Sub-topic: T05
- Agree: 3 de 3. Notes: a:N27, a:N28, a:N29, a:N30, a:N31. Urls: https://www.paradox.com/Downloader/?ID=11650, https://www.paradox.com/Downloader/?ID=11662, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: foundation

## TH14 Cada zona es definición de dos dígitos, partición y opciones
- Sub-topic: T06. Evidencia fina.
- Agree: 1 de 1. Notes: a:N32. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: foundation

## TH15 Retardo para la puerta, seguimiento para el sensor del teclado, instantánea para el perímetro
- Sub-topic: T06. Evidencia fina.
- Agree: 1 de 1. Notes: a:N33, a:N34. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: foundation

## TH16 Usá Intellizone y el retardo de transmisión donde hay falsas alarmas
- Sub-topic: T06. Evidencia fina.
- Agree: 1 de 1. Notes: a:N35. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: core

## TH17 Particionar es una decisión: zonas y usuarios se asignan a cada partición
- Sub-topic: T07. Evidencia fina.
- Agree: 1 de 1. Notes: a:N37, a:N38. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: core

## TH18 Al cambiar el largo del código, revisá todos los códigos
- Sub-topic: T07. Evidencia fina.
- Agree: 1 de 1. Notes: a:N39. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: core
- Best story: 1234 se convierte en 123412.

## TH19 PGM = evento de activación más desactivación o tiempo, con relé externo para cargas
- Sub-topic: T08. Evidencia fina.
- Agree: 2 de 2. Notes: a:N40, a:N41, a:N42, a:N43. Urls: https://www.paradox.com/Downloader/?ID=11662, https://www.paradox.com/Downloader/?ID=11650
- Disagree: none found
- Level: core

## TH20 BabyWare por 307USB, con ID de panel y contraseña de PC propios
- Sub-topic: T09
- Agree: 2 de 4. Notes: a:N44, a:N45, a:N46. Urls: https://www.paradox.com/Downloader/?ID=11662, https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue
- Disagree: los manuales de IP180 e IP150M y la guía de BlueEye siguen dando 0000 como contraseña de PC de fábrica (https://www.paradox.com/Downloader/?ID=12435), mientras la guía SP+ dice que BabyWare obliga a cambiarla en la primera conexión.
- Level: core

## TH21 El módulo IP atiende una conexión a la vez
- Sub-topic: T09 (also T14)
- Agree: 1 de 4. Notes: a:N47. Urls: https://community.openhab.org/t/help-build-binding-for-paradox-alarm-panel-with-ip150/1712?page=3
- Disagree: none found
- Level: core

## TH22 Elegí el comunicador por generación: legado (TURN) o MQTT, sin mezclar
- Sub-topic: T10 (also T11, T12)
- Agree: 4 de 6. Notes: a:N49, a:N51, a:N52, a:N54. Urls: https://www.paradox.com/Downloader/?ID=12435, https://www.paradox.com/Downloader/?ID=11873, https://www.csd.com.au/products/PDX-IP150+, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf
- Disagree: none found
- Level: core
- Best story: pasar un IP150 a MQTT es irreversible y exige sitio Swan pago.

## TH23 Dejá salir los puertos que el módulo necesita (8883, 443, 53, 123, 5683)
- Sub-topic: T10 (also T14)
- Agree: 2 de 6. Notes: a:N50. Urls: https://www.paradox.com/Downloader/?ID=12435, https://www.paradox.com/Downloader/?ID=11873
- Disagree: none found
- Level: core

## TH24 Configurá IP150+ e IP180 desde el menú instalador de BlueEye
- Sub-topic: T10 (also T12)
- Agree: 3 de 6. Notes: a:N53, a:N54, a:N49. Urls: https://support.paradox.com/portal/en/kb/articles/i-cannot-configure-the-ip150-anymore-from-the-web-interface-18-11-2022, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf, https://www.paradox.com/Downloader/?ID=12435
- Disagree: el IP150 por debajo de V6 todavía se configura por web, y en red cerrada el IP180 abre su web (misma guía BlueEye y manual IP180).
- Level: core

## TH25 Contact ID como formato, y número de abonado en cada partición
- Sub-topic: T11
- Agree: 4 de 7. Notes: a:N55, a:N56, a:N58, a:N59. Urls: https://www.paradox.com/Downloader/?ID=11650, https://www.finmon.co.za/kb/books/gsm-communicator-programming-manual/page/paradox-mg5050-and-sp6000-programming, https://www.paradox.com/Downloader/?ID=12435, https://www.paradox.com/Downloader/?ID=12343
- Disagree: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Receptoras/Manual_IPR512.pdf: el IPR512 acepta CID y SIA; https://www.paradox.com/Downloader/?ID=11662: la SP+ soporta SIA por teléfono.
- Level: core
- Best story: finmon insiste en cargar el abonado en 811 y en 812.

## TH26 Elegí la receptora según el módulo (IPR512 legado o IPC10 MQTT) y acordá el perfil de supervisión
- Sub-topic: T11 (also T10)
- Agree: 5 de 7. Notes: a:N57, a:N58, a:N59, a:N60, a:N54. Urls: https://www.paradox.com/Downloader/?ID=11650, https://www.paradox.com/Downloader/?ID=12435, https://www.paradox.com/Downloader/?ID=12343, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Receptoras/Manual_IPR512.pdf, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf
- Disagree: none found
- Level: core

## TH27 Programá la prueba periódica y el retardo de falla de AC
- Sub-topic: T11 (also T13)
- Agree: 1 de 7. Notes: a:N61, a:N62. Urls: https://www.paradox.com/Downloader/?ID=11662
- Disagree: none found
- Level: core

## TH28 BlueEye reemplaza a Insite Gold y Swan es el camino por defecto
- Sub-topic: T12
- Agree: 4 de 8. Notes: a:N63, a:N65, a:N51, a:N52. Urls: https://support.paradox.com/portal/en/kb/articles/i-cannot-connect-to-my-site-what-should-i-do, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf, https://www.paradox.com/Downloader/?ID=11873, https://www.csd.com.au/products/PDX-IP150+
- Disagree: https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/ip150: no recomienda Swan por una vulnerabilidad documentada.
- Level: core
- Best story: el usuario que pagó Swan y a los días la app no conectaba (https://forumdacasa.com/discussion/60287/4/alarme-paradox/).

## TH29 En módulos legado, la IP estática sin Swan sigue siendo una opción
- Sub-topic: T12
- Agree: 4 de 8. Notes: a:N64, a:N65, a:N52, a:N67. Urls: https://support.paradox.com/portal/en/kb/articles/how-can-i-add-a-static-ip-site-in-blueeye, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf, https://www.csd.com.au/products/PDX-IP150+, https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/ip150
- Disagree: https://www.paradox.com/Downloader/?ID=11873: con IP150M V6.50 todo pasa por Swan pago; la guía BlueEye dice que los módulos MQTT no admiten conexión por IP estática.
- Level: core

## TH30 Ante cualquier queja, primero la tecla TBL
- Sub-topic: T13
- Agree: 4 de 4. Notes: a:N68, a:N69, a:N70, a:N71, a:N9. Urls: https://www.paradox.com/Downloader/?ID=11662, https://www.paradox.com/Downloader/?ID=11650, https://store.tremtech.com/content/K32LCDPlus_Installation_Guide_En.pdf, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Disagree: none found
- Level: core

## TH31 Comunicación caída: estado de registro, puertos, reinicio de módulo y paciencia con el sondeo
- Sub-topic: T14
- Agree: 4 de 6. Notes: a:N57, a:N72, a:N73, a:N47. Urls: https://www.paradox.com/Downloader/?ID=11650, https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf, https://www.paradox.com/Downloader/?ID=12435, https://community.openhab.org/t/help-build-binding-for-paradox-alarm-panel-with-ip150/1712?page=3
- Disagree: none found
- Level: core

## TH32 Cambiá los códigos de fábrica el primer día
- Sub-topic: T15 (also T05, T09)
- Agree: 4 de 10. Notes: a:N27, a:N44, a:N46, a:N79. Urls: https://www.paradox.com/Downloader/?ID=11650, https://www.paradox.com/Downloader/?ID=11662, https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue, https://forumdacasa.com/discussion/60287/4/alarme-paradox/
- Disagree: none found
- Level: foundation
- Best story: foros donde se sugiere entrar a la central de otro con los códigos de fábrica.

## TH33 Bloqueo de instalador y reseteo: usarlos sabiendo qué borran y qué no
- Sub-topic: T15
- Agree: 2 de 10. Notes: a:N75, a:N45, a:N6. Urls: https://www.paradox.com/Downloader/?ID=11662, https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/
- Disagree: none found
- Level: core

## TH34 Puerto serie para terceros: bloqueado desde firmware 7.50, con desbloqueo oficial pago
- Sub-topic: T15
- Agree: 1 de 10. Notes: a:N76. Urls: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf
- Disagree: https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/overview: recomienda no actualizar EVO a 7.50 o más para no perder la conexión serie.
- Level: advanced

## TH35 La línea M cambia el modelo: PoE, app, reporte directo y suscripción
- Sub-topic: T16. Evidencia fina.
- Agree: 1 de 1. Notes: a:N3, a:N4, a:N13. Urls: https://www.paradox.com/web/product/m25-m25-lte/
- Disagree: none found
- Level: advanced

## The big splits
- Nube o local: Paradox empuja Swan (IP150M V6.50 lo vuelve obligatorio y pago; IP180 solo BlueEye) frente a IP estática con port forward en el KB oficial y frente a PAI, que desaconseja Swan. Gira en qué módulo hay (legado o MQTT), si el cliente acepta suscripción y si hay IP pública.
- Formato de reporte: Contact ID es lo único que pasa por IP/GPRS y por IPC10; SIA solo por línea telefónica o IPR512 legado. Gira en qué receptora tiene la empresa de monitoreo.
- Puerto serie: bloqueo desde 7.50 con desbloqueo pago (Paradox) contra "no actualices" (PAI). Gira en si hay integraciones de terceros.
- Contraseña de PC de fábrica: guía SP+ dice que BabyWare obliga a cambiarla; IP180/IP150M/BlueEye siguen hablando de 0000.

## Coverage gaps
- Definición de zonas, particiones y usuarios: una sola fuente (la guía SP+), sin practicantes.
- PCS265 LTE/V7/V8: solo menciones indirectas (consumo, serie 2, reinicio); sin manual propio leído.
- Magellan inalámbrico (MG5050, RTX3, sensores Magellan) y teclados K656/K641: mencionados, sin manual propio leído.
- Línea M: solo la página de producto; el manual de la M25 no se leyó.
- No hubo foros de instaladores en español sobre Paradox que se pudieran leer (los foros grandes bloquean scripts).
