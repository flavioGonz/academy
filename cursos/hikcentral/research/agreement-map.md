# Mapa de acuerdos: HikCentral Professional

M = páginas distintas con al menos una nota en el subtema (incluye líneas Also). N = cuántas de esas M sostienen el tema. Con M menor a 3 se marca "evidencia fina". Fuente casi toda oficial de Hikvision (manual Web Client V2.x, Quick Start, FAQ V2.5.500, Communication Matrix V2.4.1, System Requirements V2.4.510, KB de Hikvision USA); por eso el acuerdo alto refleja coherencia del fabricante más que consenso independiente.

URLs abreviadas usadas abajo:
- QSG = https://pinfo.hikvision.com/hkwsen/unzip/20230911113416_60121_doc/pdf.pdf
- FAQ = https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
- REQ = https://pinfo.hikvision.com/hkwsen/unzip/20230911113613_29615_doc/HikCentral%20Professional_System%20Requirements%20and%20Performance_V2.4.510_20230907.pdf
- MATRIX = https://pinfo.hikvision.com/hkwsen/unzip/20230511205434_28997_doc/HikCentral%20Professional_Communication%20Matrix_V2.4.1_20230511.pdf
- ADD-IP = https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-76D11646-EA40-4EDA-88DD-38821CB5826E.html
- ADD-ISUP = https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-5A97A28D-C1DB-4653-B440-FAAC67F3FDE2.html
- ADD-HC = https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-8F21FBEB-1F47-4246-A13A-0804154D9DFE.html
- LIC-OFF = https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-5B61A8EA-30BC-45DB-9102-A17602B8E976.html
- APPLY = https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-3F50D8C7-95C9-478B-B4D5-189A09C3D708.html
- ROLE = https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-6C43765F-0DD8-43CF-ADF0-5918B47787D1.html
- EVT = https://pinfo.hikvision.com/hkwsen/unzip/20240822164538_35347_doc/GUID-7C8C6C1B-5438-4C6B-8C71-B042A25AE1BB.html
- BKP = https://pinfo.hikvision.com/hkwsen/unzip/20240822164538_35347_doc/GUID-1AF31681-DD4C-4819-B85A-74A0178F87E8.html
- TA = https://supportusa.hikvision.com/support/solutions/articles/17000120924-time-and-attendance-setup-on-hikcentral
- HCOFF = https://supportusa.hikvision.com/support/solutions/articles/17000146654-troubleshooting-platform-access-offline-on-device
- HCOFF2 = https://supportusa.hikvision.com/support/solutions/articles/17000128685-why-is-my-platform-access-offline-
- STREAMS = https://supportusa.hikvision.com/support/solutions/articles/17000135582-how-to-see-the-number-of-streams-from-an-nvr-error-maximum-number-of-streams
- HTTPS = https://supportusa.hikvision.com/support/solutions/articles/17000110020-how-to-generate-and-install-https-certificate-for-hikcentral
- VXG = https://www.videoexpertsgroup.com/glossary/hikcentral-professional
- SI = https://www.securityinformed.com/hikvision-hikcentral-access-control-software-technical-details.html
- LC-PORTS = https://learncctv.com/default-ports-for-hikvision-dvr/
- LC-PF = https://learncctv.com/hikvision-port-forwarding/
- LC-SEC = https://learncctv.com/hikvision-cameras-removed-us-army-base-security-issues/

## TH01 Elegí el producto de la familia por alcance: Professional cuando hay video, acceso y alarmas juntos; la versión liviana de acceso alcanza para pocas puertas
- Sub-topic: T01 (also T10)
- Agree: 2 of 2. Notes: a:N1, a:N2. Urls: SI, VXG
- Disagree: none found
- Level: foundation
- Best story: versión de acceso gratis hasta 4 puertas y 50 empleados, ampliable a Professional (SI). Evidencia fina.

## TH02 Pensá el sistema en capas: SYS gestiona, el streaming reenvía, el Web Client configura, el Control Client opera
- Sub-topic: T02
- Agree: 3 of 4. Notes: a:N3, a:N4, a:N5. Urls: QSG, FAQ, REQ
- Disagree: none found
- Level: foundation
- Best story: el SYS trae un Streaming Gateway que sirve hasta 200 cámaras; por eso el Streaming Server va en otra máquina (FAQ).

## TH03 Sumá un Streaming Server cuando pasás de unas 200 cámaras reenviadas o cuando el NVR llega a su tope de conexiones
- Sub-topic: T02 (also T16)
- Agree: 2 of 4. Notes: a:N4, a:N64. Urls: FAQ, STREAMS
- Disagree: none found
- Level: core
- Best story: NVR con tope de 128 conexiones remotas; conexiones no es lo mismo que ancho de banda (STREAMS).

## TH04 Mantené el Control Client en la misma versión exacta que el SYS y fuera de máquinas virtuales
- Sub-topic: T02 (also T03, T16)
- Agree: 2 of 4. Notes: a:N5, a:N6. Urls: REQ, FAQ
- Disagree: none found
- Level: core
- Best story: error VSM217 por versión distinta (FAQ).

## TH05 Dimensioná el SYS con la guía de requisitos: perfil bajo i5 con 8 GB y 650 GB de disco; 16 a 32 GB y Xeon para cargas altas
- Sub-topic: T03
- Agree: 2 of 4. Notes: a:N9, a:N10. Urls: REQ, FAQ
- Disagree: VXG: el costo real es la infraestructura y su mantenimiento, no el hardware inicial.
- Level: foundation
- Best story: hasta 2.048 encoders y 10.000 cámaras por sitio (FAQ, their claim).

## TH06 Virtualizá el SYS sin migrarlo en caliente: la migración de VM rompe la licencia
- Sub-topic: T03 (also T05)
- Agree: 2 of 4. Notes: a:N11, a:N21. Urls: REQ, LIC-OFF
- Disagree: none found
- Level: core
- Best story: none

## TH07 Instalá como administrador, con modo típico para un solo servidor y personalizado para separar módulos; verificá el MD5 si el instalador falla
- Sub-topic: T04
- Agree: 2 of 2. Notes: a:N14, a:N15. Urls: QSG, FAQ
- Disagree: none found
- Level: foundation
- Best story: none. Evidencia fina.

## TH08 Usá el Service Manager para ver servicios y puertos; puerto en rojo es conflicto con otro proceso
- Sub-topic: T04 (also T16)
- Agree: 2 of 2. Notes: a:N16, a:N65. Urls: QSG, FAQ
- Disagree: none found
- Level: core
- Best story: netstat y tasklist para encontrar quién tomó el puerto (FAQ). Evidencia fina.

## TH09 Creá la contraseña del admin en el primer ingreso y registrá el email del admin al activar
- Sub-topic: T04 (also T05, T13)
- Agree: 2 of 2. Notes: a:N17, a:N23. Urls: QSG, LIC-OFF
- Disagree: none found
- Level: foundation
- Best story: el email recupera el código de activación si se pierden contraseña y código (LIC-OFF).

## TH10 Activá siempre una licencia base antes que cualquier expansión
- Sub-topic: T05
- Agree: 2 of 5. Notes: a:N18, a:N20. Urls: QSG, FAQ
- Disagree: none found
- Level: foundation
- Best story: error 1113, expansión sin base (FAQ).

## TH11 En sitios sin internet, activá offline con archivo de pedido y respuesta dentro de las 24 horas y con la hora del servidor correcta
- Sub-topic: T05
- Agree: 2 of 5. Notes: a:N19, a:N20. Urls: LIC-OFF, FAQ
- Disagree: none found
- Level: core
- Best story: error 1105 por respuesta vieja o por hacer doble clic al exportar el pedido (FAQ).

## TH12 Desactivá la licencia antes de cambiar hardware o mover el servidor
- Sub-topic: T05 (also T03, T16)
- Agree: 4 of 5. Notes: a:N11, a:N21, a:N22, a:N20. Urls: REQ, LIC-OFF, FAQ, QSG
- Disagree: none found
- Level: core
- Best story: SYS alternando Starting y Stopped tras cambio de hardware (FAQ).

## TH13 Leé el código de error de activación antes de llamar a soporte (1103 red, 1108 código en uso, 1114 hora, 1116 cupo)
- Sub-topic: T05 (also T16)
- Agree: 1 of 5. Notes: a:N20. Urls: FAQ
- Disagree: none found
- Level: core
- Best story: none

## TH14 Agregá por IP/dominio cuando hay IP fija: puerto 8000, 8443 cifrado, NTP antes
- Sub-topic: T06 (also T15)
- Agree: 3 of 7. Notes: a:N24, a:N57, a:N59. Urls: ADD-IP, MATRIX, LC-PORTS
- Disagree: none found
- Level: foundation
- Best story: none

## TH15 Usá ISUP para equipos sin IP fija: habilitá el registro ISUP en la plataforma y configurá Device ID y clave en el equipo
- Sub-topic: T06 (also T15)
- Agree: 2 of 7. Notes: a:N26, a:N57. Urls: ADD-ISUP, MATRIX
- Disagree: LC-PF enseña port forwarding directo como forma de acceso remoto.
- Level: core
- Best story: ISUP presentado como la opción "costo efectiva" sin IP fija (ADD-ISUP).

## TH16 Usá Hik-Connect DDNS como atajo, sabiendo que esos equipos no graban en Hybrid SAN ni Cloud Storage
- Sub-topic: T06 (also T08)
- Agree: 2 of 7. Notes: a:N27, a:N28. Urls: ADD-HC, FAQ
- Disagree: none found
- Level: core
- Best story: none

## TH17 Importá siempre los canales a un área al agregar el equipo
- Sub-topic: T06 (also T07)
- Agree: 3 of 7. Notes: a:N25, a:N31. Urls: ADD-IP, ADD-ISUP, ADD-HC
- Disagree: none found
- Level: foundation
- Best story: equipo agregado pero sin vivo ni reproducción porque los canales no se importaron a un área (ADD-IP).

## TH18 Con cámaras de terceros, verificá el puerto ONVIF y esperá funciones reducidas
- Sub-topic: T06 (also T16)
- Agree: 2 of 7. Notes: a:N29, a:N2. Urls: FAQ, VXG
- Disagree: none found
- Level: core
- Best story: cámaras ONVIF offline por puerto 80 contra 8000 (FAQ).

## TH19 Poné cada cámara en el área donde se va a usar; las de áreas hijas no aparecen en la madre
- Sub-topic: T07
- Agree: 1 of 2. Notes: a:N31. Urls: FAQ
- Disagree: none found
- Level: foundation
- Best story: "There is no camera in this area" (FAQ). Evidencia fina.

## TH20 Usá vistas públicas para el puesto de monitoreo y privadas para cada operador
- Sub-topic: T07 (also T13)
- Agree: 1 of 2. Notes: a:N32. Urls: FAQ
- Disagree: none found
- Level: foundation
- Best story: none. Evidencia fina.

## TH21 Decidí dónde graba cada cámara al darla de alta: en el equipo o en almacenamiento central
- Sub-topic: T08
- Agree: 3 of 3. Notes: a:N33, a:N28, a:N34. Urls: ADD-IP, FAQ, EVT
- Disagree: none found
- Level: core
- Best story: pStor Cluster no hace grabación por movimiento (FAQ).

## TH22 Habilitá WAN Access en cada Recording Server que esté en LAN si vas a reproducir desde afuera
- Sub-topic: T08 (also T15)
- Agree: 1 of 3. Notes: a:N35. Urls: FAQ
- Disagree: none found
- Level: advanced
- Best story: none

## TH23 Armá eventos como disparador más acción, y convertí en alarma solo lo que alguien tiene que atender
- Sub-topic: T09
- Agree: 2 of 2. Notes: a:N36, a:N39. Urls: EVT, FAQ
- Disagree: none found
- Level: core
- Best story: más de 20 eventos con foto por segundo traban el Web Client (FAQ). Evidencia fina.

## TH24 Domá el ruido: ignorá repetidos y retrasá la alarma de cámara offline
- Sub-topic: T09 (also T16)
- Agree: 1 of 2. Notes: a:N37. Urls: EVT
- Disagree: none found
- Level: core
- Best story: Delay Alarm para que mantenimiento vea solo las cámaras realmente caídas (EVT). Evidencia fina.

## TH25 Grabá con pre y post evento y bloqueá el clip para que no se sobrescriba
- Sub-topic: T09 (also T08)
- Agree: 1 of 2. Notes: a:N38. Urls: EVT
- Disagree: none found
- Level: core
- Best story: puerta abierta y video de los segundos previos (EVT). Evidencia fina.

## TH26 Después de asignar niveles de acceso, aplicalos a los dispositivos; evitá "Apply (Initial)" en horario de uso
- Sub-topic: T10
- Agree: 1 of 3. Notes: a:N41, a:N42. Urls: APPLY
- Disagree: none found
- Level: core
- Best story: durante el aplicado inicial las puertas quedan offline y nadie pasa (APPLY).

## TH27 Elegí un único lugar de alta de personas (plataforma o equipo) y definí las reglas de ID antes de la primera alta
- Sub-topic: T10
- Agree: 1 of 3. Notes: a:N43, a:N44. Urls: FAQ
- Disagree: TA arranca la receta dando de alta en la plataforma; coincide con el criterio, no lo contradice.
- Level: core
- Best story: none

## TH28 Alineá la zona horaria de controladoras y SYS
- Sub-topic: T10 (also T11, T16)
- Agree: 1 of 3. Notes: a:N45, a:N49. Urls: FAQ
- Disagree: none found
- Level: core
- Best story: pasadas que no aparecen en vivo pero sí en el histórico (FAQ).

## TH29 Para asistencia, seguí el orden: puntos de marca, regla general, plantilla de turno, turno, asignación
- Sub-topic: T11
- Agree: 1 of 2. Notes: a:N47, a:N48. Urls: TA
- Disagree: none found
- Level: core
- Best story: turno Man-Hour de 8 a 17 con primera entrada y última salida (TA). Evidencia fina.

## TH30 Usá E-map para planos fijos y GIS para datos geográficos vivos
- Sub-topic: T12
- Agree: 1 of 1. Notes: a:N50. Urls: FAQ
- Disagree: none found
- Level: foundation
- Best story: una cámara puede estar en hasta 6 mapas (FAQ). Evidencia fina.

## TH31 Creá roles a medida con áreas visibles y horario de permisos; no uses Administrator para operadores
- Sub-topic: T13
- Agree: 2 of 5. Notes: a:N51, a:N32. Urls: ROLE, FAQ
- Disagree: none found
- Level: foundation
- Best story: rol vencido expulsa al usuario (ROLE).

## TH32 Endurecé el acceso: contraseña fuerte, HTTPS con certificado propio, nada expuesto sin necesidad
- Sub-topic: T13 (also T15)
- Agree: 4 of 5. Notes: a:N52, a:N53, a:N54, a:N17. Urls: FAQ, HTTPS, LC-SEC, QSG
- Disagree: none found
- Level: core
- Best story: el certificado embebido da "No seguro" hasta que se sube un .pem firmado (HTTPS).

## TH33 Programá backups del sistema y copialos fuera del servidor SYS
- Sub-topic: T14
- Agree: 3 of 4. Notes: a:N55, a:N7, a:N13. Urls: BKP, FAQ, VXG
- Disagree: none found
- Level: core
- Best story: los backups quedan en el propio SYS y se guardan de 1 a 5 copias (BKP).

## TH34 Documentá los puertos del SYS y del gateway con la Communication Matrix antes de tocar el firewall
- Sub-topic: T15
- Agree: 3 of 8. Notes: a:N57, a:N58, a:N61. Urls: MATRIX, FAQ, ADD-IP
- Disagree: LC-PF y LC-PORTS enfocan en abrir puertos de los equipos, no del VMS.
- Level: core
- Best story: vivo que anda en IE pero no en Chrome por el puerto 559 (FAQ).

## TH35 Dispositivo offline: de abajo hacia arriba, cable, IP y gateway, DNS, servicio habilitado, puertos
- Sub-topic: T16
- Agree: 4 of 8. Notes: a:N62, a:N63, a:N29, a:N65. Urls: HCOFF, HCOFF2, FAQ, QSG
- Disagree: none found
- Level: core
- Best story: puertos STUN 6002, 6800, 8555, 9010, 9020 bloqueados por firewall (HCOFF).

## The big splits
- Acceso remoto: port forwarding directo (LC-PF, LC-PORTS) contra registro saliente ISUP o Hik-Connect (ADD-ISUP, ADD-HC) y la advertencia de seguridad (LC-SEC). Gira en torno a si el sitio tiene IP fija y cuánto se tolera exponer.
- Dónde grabar: en el NVR del sitio (simple, sobrevive a cortes del enlace) contra almacenamiento central (pStor, Hybrid SAN) con sus limitaciones (FAQ) y requisitos de red. Gira en torno a ancho de banda, tamaño y quién mantiene el servidor.
- On-premises vs. nube: VXG sostiene que la carga de operar el servidor es la desventaja central; Hikvision lo trata como el modelo base y ofrece AWS/Azure con limitaciones (LIC-OFF).
- Hik-Connect como vía de alta: cómodo, pero sin grabación en Hybrid SAN ni Cloud Storage (FAQ).

## Coverage gaps
- Documentación V3.x (la versión vigente a octubre 2026) no se pudo leer: hikvision.com devuelve un desafío JavaScript. Todo el curso se apoya en V2.4 a V2.6.1; las rutas de menú pueden cambiar en V3.
- No se leyó en raw/ el procedimiento de restauración ni el de plantillas de horario de acceso (se vio en el índice, no se guardó).
- Foros independientes (ipcamtalk) no se pudieron leer (responden 403 a scripts); la voz de practicantes es fina: learncctv y el KB de Hikvision USA.
- T07, T09, T11, T12 con evidencia fina (M menor a 3).
- No se cubre licenciamiento comercial (precios, SSA/mantenimiento) ni HikCentral Connect y FocSign más allá de nombrarlos.
