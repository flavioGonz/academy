# Notes: batch d
Pages read: 17. With notes: 17. Skipped: 0. (Catálogo: menú de productos, guías de selección de porteros y monitores, fichas de X915, R29, R49G, EC33, A08 y WR01, página de software de akuvox.com; tablas transversales de la Knowledge Base: alimentación, carga de relé, métodos de acceso, salida de 12 V, interfaces de monitores, acceso a la web por modelo, firmware por modelo y ascensores.)

Nota de lectura: las páginas de akuvox.com no tienen fecha; se toman como el catálogo publicado al 27 de octubre de 2026, día en que se guardaron. "Vigente" en este curso quiere decir "listado en el menú de productos de akuvox.com ese día"; "fuera de catálogo" quiere decir que el modelo aparece en tablas o guías de la Knowledge Base pero no en ese menú. Ninguna página leída publica una lista oficial de discontinuados.

## T21 Porteros de calle
- d:N1. Menú de porteros vigente: S539, S538, S535 (con módulos de huella, LTE, lector QR y lazo de inducción), S532 (estándar, IP, lazo de inducción), X916 (estándar y LTE), X915 (estándar, HID iClass, HID Prox, venas de la palma), X912 (estándar y teclado físico), X910, R29 (estándar, Bluetooth con doble cámara, LTE, huella), R28 (estándar y lazo de inducción), R25K, R20K, R20K-L, R20B, MD12, MD06, E21, R25A, R20A, E18 (estándar y LTE), E16, E13S, E12, E20S.
  - Source: https://www.akuvox.com/products  Quote: "S535 with Fingerprint Expansion Unit"
  - Kind: definition
  - Level: foundation
- d:N2. Guía de selección de porteros (pantalla, sistema, Wi-Fi, biometría, Wiegand, IP): S539 10" Android IP66; S535 5" Linux IP66; X916 13" Android IP65; X915 8" Android IP65; X912 Linux IP65; X910 sin pantalla, Linux, IP66; R29 7" Android IP65; R28 4,3" sin táctil, Linux IP65; R20K, R20K-L, R20B, R25A sin pantalla, Linux IP65; E21 acero, sin PIN ni tarjeta ni Wiegand, IP65; E18 táctil, plástico, Linux IP65; E16 5" plástico Linux IP65; E13S sin pantalla IP65; E12 único con Wi-Fi en la tabla. Todos PoE y SIP, todos con cámara y ONVIF. Solo los Android admiten apps de terceros.
  - Source: https://www.akuvox.com/productSelectionGuide?cid=3  Quote: "3rd-party Apps"
  - Kind: definition
  - Level: foundation
- d:N3. X915 V2.0 en la ficha: frente de acero inoxidable, 8" táctil, doble cámara, lector 13,56 MHz y 125 kHz (o HID iClass, o HID Prox), PoE+, Bluetooth, Android, IP66 e IK10; X915P suma venas de la palma. La guía de selección dice IP65 para el X915: las dos páginas no coinciden.
  - Source: https://www.akuvox.com/productsDisp?pid=37  Quote: "IP66 & IK10"
  - Kind: number
  - Level: core
- d:N4. R29 en la ficha: aluminio, 7" táctil, Android, PoE o fuente, montaje de superficie y embutido, IP65 e IK06; R29S una cámara, R29C doble cámara y Bluetooth, R29C-L con módulo LTE, R29C-T con huella. Accesorios: cubiertas de lluvia y soportes para pared y embutir.
  - Source: https://www.akuvox.com/productsDisp?pid=17  Quote: "IP65 / IK06"
  - Kind: number
  - Level: core
  - Also: T24
- d:N5. Métodos de acceso por modelo: PIN en S539, S538, S535, S532, X916S, X915S, X912S, R29, R28A, R27A, R20K, E18C, E16, A02S, A03S, A05C, A08, A15, A095; sin PIN en X910, R25, R20A, R20B, E21, E20S, E13, E12, A01S, WR01. Tarjeta 13,56 y 125 kHz en casi toda la línea; solo 13,56 en X910, R20K-L, E16, E13, E12, A05C, A15. Rostro en S539, S538, S535, X916S, X915S, X912S, R29, E18C, E16, A05C, A15. Huella solo en R29CT y como opción en S535. Venas de la palma en X915P y E16P.
  - Source: https://knowledge.akuvox.com/docs/access-methods-supported-by-door-phones  Quote: "Supported on X915P."
  - Kind: definition
  - Level: core
  - Also: T23
- d:N6. Alimentación de porteros: PoE+ (802.3at) en S539, S535, S532, X916S, X915S, X912S; 802.3at en S538, R29 y R29S; 802.3af en X910, R29C-B, R29CT, R28A, R27A, R20A, R20K, R20B, R25, E21, E20S, E18C, E16C V2/V3, E12, DB01. R29C-L con LTE no admite PoE. Fuentes recomendadas: 24 V 2 A en X915S, 12 V 1 A en los R20, E16 y E12, 48 V 1,25 A en los de 2 hilos.
  - Source: https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices  Quote: "R29C-L (with LTE module) | X"
  - Kind: number
  - Level: core
  - Also: T22, T23
- d:N7. Carga resistiva de los relés: X916 30 V 5 A; S539, S538, S532, X915, X912, R29, R28, R27, E21 30 V 3 A; S535, X910, R20, R25, R20-2, E18, E16, E12, E13, DB01 30 V 2 A.
  - Source: https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors  Quote: "X916 | 30V 5A"
  - Kind: number
  - Level: core
  - Also: T22, T23
- d:N8. Salida de 12 V para cerradura o relé externo: X915S y X912S 12 V 1 A por relé; S538 y R28 tienen borne propio; R20K V3.0, R20A V5.0, R20B V2.0 y R29 V1.1 dan 12 V 500 mA, con PoE solo desde 320.30.11.42 y afectada por el volumen; E21, E20S, E18C, E16C, E12 y DB01 no tienen. Modo Always (NC, corta al abrir) o Triggered by Open Relay (NO, alimenta al abrir).
  - Source: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output  Quote: "the power supply is affected by the device's"
  - Kind: number
  - Level: core
  - Also: T18
- d:N9. Cómo sacar la IP según la familia: S539, S538, S535, X915, X916 y R29 con 9999, Dial, 3888; R27, R28 y S532 con asterisco 2396 numeral; E16 y E18 manteniendo la pantalla y PIN de sistema (admin hasta 216.30.10.121 en E16 y 18.30.10.211 en E18, Admin321 después); X912 con 2396; R20A, R25A, E11, E12, E13 y X910 manteniendo el botón 5 s; R20K y R25K con asterisco 3258 asterisco; E21 y DB01 con el pulsador; E20S solo con alimentarlo.
  - Source: https://knowledge.akuvox.com/docs/before-entering-device-web-interface  Quote: "Hold the Call button for about five seconds."
  - Kind: technique
  - Level: foundation
  - Also: T22, T23
- d:N10. El número A del firmware identifica el modelo (29 R29, 915 X915, 320 R20V5, 216 E16V2, 416 E16V3, 116 E16, 111 E11, 120 E20, 27 R27...). Tienen dos versiones de hardware E12, R28, X915 y C313; tres, la serie R20, E16 y E21.
  - Source: https://knowledge.akuvox.com/docs/upgrade-devices  Quote: "Devices that have three hardware versions include"
  - Kind: definition
  - Level: core
  - Also: T24

## T22 Monitores interiores
- d:N11. Menú de monitores vigente: X937, X933, S567, S565, S563, S562, S560, IT88, C319, C316, C313; aparte, "Agentic Panel" AKClaw Panel.
  - Source: https://www.akuvox.com/products  Quote: "AKClaw Panel"
  - Kind: definition
  - Level: foundation
- d:N12. Guía de selección de monitores: X937 15,6" aluminio Android 14; X933 7" Android; S567 10" Android; S563 8" Android; S562 7" Linux; IT88 10" aluminio Android; C319 10" Android; C316 7" Android; C313 7" Linux. Todos táctiles, PoE y SIP. Las columnas de cámara y Wi-Fi de esta tabla vienen desalineadas y no se usan.
  - Source: https://www.akuvox.com/productSelectionGuide?cid=4  Quote: "Android OS 14"
  - Kind: definition
  - Level: foundation
- d:N13. Interfaces: S567, S565, S563, S562 y C316 con 1 RS485, 1 salida de relé y 1 entrada de timbre; IT88S, C319S, X933S y X937A con 2 relés; S560 y C310 sin RS485 ni relé; S565, S563, S562 y C313S con un RJ45 extra además del PoE; X937A con dos RJ45 extra; C313W-2 solo RJ45 (2 hilos).
  - Source: https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors  Quote: "PoE x1; RJ45 ×2"
  - Kind: definition
  - Level: core
- d:N14. Relé de monitores: 30 V 2 A en X937, S567, S565, S563, IT88, IT83, C313, C313-2, C315; 30 V 1 A en S562; 24 V 1 A en C319 y X933; el S560 no tiene.
  - Source: https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors  Quote: "S560 | X"
  - Kind: number
  - Level: core
- d:N15. Alimentación de monitores: S567 802.3af y 12 V 1,5 A; la mayoría 12 V 1 A; X937 PoE+ 802.3at y 12 V 2 A; C313-2 sin PoE, se alimenta del NS-2 o de 48 V.
  - Source: https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices  Quote: "power supply via NS-2"
  - Kind: number
  - Level: core
- d:N16. IP en monitores: C313 More > Status > Network; C310 Settings > Status > Network; C315 More > System Info > Network; C316, C319, S567, S563, S562, IT88, IT83, X933 y X937 Settings > System Info > Network; S565 More > Settings > System Info > Network; S560 manteniendo numeral 5 s anuncia la IP.
  - Source: https://knowledge.akuvox.com/docs/before-entering-device-web-interface  Quote: "press the # key for about 5 seconds"
  - Kind: technique
  - Level: foundation

## T23 Control de acceso, ascensores y 2 hilos
- d:N17. Menú de control de acceso vigente: WR01, A15, A095, EC33, A094 (estándar y sin adaptador AC-DC), A08 (estándar, HID Prox, sin lector QR), A05, A03, A02, A01, lectores ACR-CRP12, ACR-CID12, ACR-CID01, tarjeta UHF-TAG11, Bkey, SR01, KF01, KF02, KF03.
  - Source: https://www.akuvox.com/products  Quote: "Zero AC-to-DC adaptor version"
  - Kind: definition
  - Level: foundation
- d:N18. A08 en la ficha: marco de aluminio, teclado táctil, lector QR, 13,56 y 125 kHz más NFC, BLE 5.0, PoE o fuente, pared o embutido, IP65 e IK09; A08K sin QR ni BLE.
  - Source: https://www.akuvox.com/productsDisp?pid=92  Quote: "IP65 & IK09"
  - Kind: number
  - Level: core
- d:N19. Alimentación y 12 V en acceso: A094 sin PoE, 100 a 240 VAC, 4 salidas de 12 V 800 mA; A095 PoE 802.3at o 12 V 5 A, 8 salidas de 12 V (500 mA con fuente, 0,2 a 0,4 A con PoE+ según lectores); A15 PoE 802.3at, 12 V 500 mA con PoE+ o 1 A con fuente; A08 12 V 500 mA, PoE desde hardware 108.2.0.0.0; A01 a A03 12 V 500 mA; A05 no da 12 V.
  - Source: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output  Quote: "4 ports"
  - Kind: number
  - Level: core
- d:N20. EC33 en la ficha: controlador IP de ascensor, 32 relés ampliables a 64, lectores Wiegand 26/34, 20.000 tarjetas y 100.000 registros, TCP/IP y RS485; trabaja con todos los intercom y terminales de Akuvox. Alimentación 100 a 240 VAC o 802.3at; relé 30 V 3 A.
  - Source: https://www.akuvox.com/productsDisp?pid=83  Quote: "32 relays (expandable to 64)"
  - Kind: number
  - Level: core
- d:N21. EC33 en obra: dos escenarios. Acceso directo al piso (relé del EC33 en paralelo con el botón del piso) o liberar botones para elegir (relé en serie con el común o la línea de autorización). Todos los porteros y terminales lo integran salvo A094 y E20. Se pueden configurar dos EC33 (desbloqueo y llamado). Floor Starts From y Ground Floor para sótanos.
  - Source: https://knowledge.akuvox.com/docs/configure-lift-control-1  Quote: "Except for A094 and E20"
  - Kind: technique
  - Level: advanced
- d:N22. Menú de 2 hilos vigente: R20K-2, R20A-2, E12S-2, S562W-2, C313W-2, NS-2, NC-2, NX-2. Los porteros de 2 hilos no tienen PoE y van a 48 V DC 1,25 A; el C313-2 se alimenta del NS-2.
  - Source: https://www.akuvox.com/products  Quote: "2-Wire Intercom"
  - Kind: definition
  - Level: core

## T24 Teléfonos, accesorios, software y parque instalado
- d:N23. R49G, teléfono de video Android: 7" táctil, una cámara, dos puertos Gigabit conmutados, Bluetooth, USB, PoE y Wi-Fi, Android 9, de escritorio.
  - Source: https://www.akuvox.com/productsDisp?pid=48  Quote: "Dual switched 10/100/1000Mbps Ethernet ports"
  - Kind: number
  - Level: core
- d:N24. Otras líneas del menú: teléfonos IP HCP-R15P (salud) y SP-R50P (entrada), cámara IP VC50B/VC50T, radares MR03 y MR01, kits de video portero IP y de 2 hilos, kits de entrenamiento, accesorios por tipo (porteros, monitores, acceso).
  - Source: https://www.akuvox.com/products  Quote: "Akuvox VC50B/VC50T"
  - Kind: definition
  - Level: foundation
- d:N25. Software vigente: SmartPlus App (app del residente con la nube), My MobileKey (credencial Bluetooth con AES256, integra ACMS), Installer Kit Tool (sobre hardware S563W, junta la red de los equipos y sube el proyecto a la nube), ACMS (control de acceso en PC para pymes), ACMS Pro (empresa, B/S y C/S), SDMC (gestión local de comunidades: despliegue por lotes, video, acceso, mensajes).
  - Source: https://www.akuvox.com/productsSoftwareForIntercom  Quote: "The SDMC is an on-premise software for community-wide intercom system management."
  - Kind: definition
  - Level: core
- d:N26. Modelos que siguen en la documentación pero no en el menú de productos: E11 y DB01 (acceso a la web), R27 (métodos de acceso, 12 V, SR01, firmware), IT83 y C315 (relé, firmware), C310 (interfaces, alimentación, firmware), A092 (relé, Web Relay), E20 (firmware 120, excluido del EC33). El C317 no aparece en ninguna página leída.
  - Source: https://knowledge.akuvox.com/docs/upgrade-devices  Quote: "IT83 C315 Version Number"
  - Kind: definition
  - Level: core
- d:N27. ComfortClick documenta un E11R con un C315S como pareja típica del parque instalado, con RTSP en /live/ch00_0 y MJPEG en el puerto 8080.
  - Source: https://www.comfortclick.com/Support/ExampleDetails/Akuvox  Quote: "an E11R single tenant door phone and C315S Android indoor monitor"
  - Kind: story
  - Level: core
- d:N28. El E16 y el C316 siguen en el menú vigente al 27 de octubre de 2026, contra lo que podría suponerse; la guía de selección lista al C316 como monitor de 7" con Android.
  - Source: https://www.akuvox.com/products  Quote: "C316"
  - Kind: definition
  - Level: foundation

- d:N29. Las fichas de akuvox.com traen al pie una línea por producto relacionado: S539 "10'' Android Door Phone", S538 "Sleek Tri-Vision Video Door Phone", S535 "Facial Recognition Door Phone", S532 "2.8" SIP Video Door Phone", X916 "Android Doorphone with Starlight Camera", X912 "Vandal-resistant", X910 "Single-Button Package Detection Door Phone", R20K-L "Compact LTE Video Door Phone", MD06 y MD12 "Video Intercom Nametag Module", E21 "SIP Emergency Video Intercom", E20S "SIP Emergency Intercom", E18 "7" Face Recognition Door phone"; en acceso, A15 "Mullion" (para marco), A094 y A095 "4 Door Controller", ACR-CRP12 lector UHF, ACR-CID12 y ACR-CID01 lectores de escritorio, UHF-TAG11 tarjeta UHF, Bkey tarjeta Bluetooth.
  - Source: https://www.akuvox.com/productsDisp?pid=17  Quote: "Video Intercom Nametag Module"
  - Kind: definition
  - Level: foundation
  - Also: T23

## Disagreements seen
- X915: la guía de selección dice IP65 (https://www.akuvox.com/productSelectionGuide?cid=3) y la ficha del X915 V2.0 dice IP66 e IK10 (https://www.akuvox.com/productsDisp?pid=37).
- Monitores: la tabla de interfaces asigna dos relés a C319S y X933S (https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors) y la tabla de carga de relé solo da un valor por modelo (https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors). No se contradicen, pero no dicen si los dos relés soportan lo mismo.
- PoE en los R20: la tabla de alimentación dice 802.3af sin condición (https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices); la tabla de 12 V aclara que la salida de 12 V con PoE pide firmware 320.30.11.42 o más (https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output).

## Best stories
- La pareja E11R más C315S del ejemplo de ComfortClick, el parque que sigue colgado en las paredes (https://www.comfortclick.com/Support/ExampleDetails/Akuvox).
- R20A con etiqueta V3.0 que es hardware 2 (ya en a:N2) y la tabla de códigos A del firmware (https://knowledge.akuvox.com/docs/upgrade-devices).
- El X916 con relé de 5 A, el más fuerte de la línea (https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors).
- El R29C-L con LTE que no se alimenta por PoE (https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices).
