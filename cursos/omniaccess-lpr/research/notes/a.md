# Notes: batch a (fuentes web)
Pages read: 30. With notes: 27. Skipped: 3 (MDN Push y RFC 7826 solo aportan definiciones de fondo; hertzbeat solo confirma ISAPI con Digest).

## T01 Qué es ANPR/LPR y de dónde viene
- a:N1. ANPR nació en 1976 en la Police Scientific Development Branch del Home Office británico; había prototipos andando en 1979 y pruebas en el Dartford Tunnel para detectar autos robados.
  - Source: https://www.traffictechnologytoday.com/features/feature-who-invented-anpr-the-untold-british-story-behind-a-global-traffic-technology-revolution.html  Quote: "invented ANPR in 1976"
  - Kind: story · Level: foundation
- a:N2. Las primeras pruebas sobre video Super VHS leían entre 70 % y 90 % de las patentes en tiempo real (su dato).
  - Source: https://www.traffictechnologytoday.com/features/feature-who-invented-anpr-the-untold-british-story-behind-a-global-traffic-technology-revolution.html
  - Kind: number · Level: foundation
- a:N3. ANPR es un pipeline: detectar la patente, normalizar la imagen, segmentar y hacer OCR; si se hace en el carril tarda del orden de 250 ms (su dato).
  - Source: https://en.wikipedia.org/wiki/Automatic_number-plate_recognition
  - Kind: definition · Level: foundation · Also: T07
- a:N4. Exactitud son dos números multiplicados: tasa de captura (¿hubo imagen útil?) por tasa de lectura (¿OCR correcto?). 98 % por 95 % da cerca de 93 % (su ejemplo).
  - Source: https://www.forasoft.com/learn/video-surveillance/articles-vms/license-plate-recognition-lpr-anpr
  - Kind: rule of thumb · Level: core · Also: T16
- a:N5. La patente Mercosur empezó a emitirse en Uruguay en marzo de 2015 (Montevideo, Canelones): tres letras y cuatro números, diseño común del bloque.
  - Source: https://www.autoblog.com.uy/2015/04/ya-circulan-las-primeras-patentes.html
  - Kind: story · Level: foundation · Also: T14

## T03 Quién decide
- a:N6. Las cámaras ANPR Hikvision guardan listas en la propia cámara (Syscom: hasta 2048 placas entre listas blanca y negra) y al leer pueden activar una salida de alarma para la barrera.
  - Source: https://syscom.mx/blog/hikvision-anpr-reconocimiento-de-placas
  - Kind: technique · Level: core · Bias: distribuidor
- a:N7. La salida de alarma de la cámara abre la barrera, pero según el equipo de apertura puede hacer falta un relé o temporizador.
  - Source: https://blog.epcom.net/?p=128
  - Kind: technique · Level: core
- a:N8. Para dar acceso a un predio cerrado algunos sistemas aceptan un error de un carácter, porque es improbable que un intruso tenga una patente tan parecida.
  - Source: https://en.wikipedia.org/wiki/Automatic_number-plate_recognition
  - Kind: rule of thumb · Level: advanced
- a:N9. En parking se valida en N-1 o N-2 (uno o dos caracteres de tolerancia) como solución probabilística.
  - Source: https://www.parking.net/parking-news/survision/lets-be-accurate-about-lpr-accuracy
  - Kind: technique · Level: advanced · Bias: fabricante
- a:N10. La cámara ofrece un intervalo mínimo antes de volver a reconocer la misma patente y modos de coincidencia difusa.
  - Source: https://www.omadanetworks.com/au/support/faq/4723/
  - Kind: technique · Level: core · Also: T07

## T04 Emplazamiento
- a:N11. Guía Hikvision: patente de 130 a 300 px de ancho (óptimo 150 a 200), inclinación de la patente dentro de ±5°, ángulo vertical y horizontal hasta 30°.
  - Source: https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf
  - Kind: number · Level: core
- a:N12. DTK: patente de al menos 100 px, ángulos de hasta 30°, cámara a 3 m de altura lee desde unos 5 m; para dos carriles, cámara sobre pórtico.
  - Source: https://www.dtksoft.com/camera-installation
  - Kind: number · Level: core
- a:N13. Guía doméstica: 2,5 a 3 m de altura, 5 a 10 m del punto de lectura, vehículo a 5 a 15 mph; 2 MP alcanza.
  - Source: https://home-security-guide.readthedocs.io/en/latest/cctv/17-anpr-camera-installation-guide-uk/
  - Kind: number · Level: core
- a:N14. La zona de reconocimiento cubre solo el carril; la línea de disparo va donde la patente tiene buen ángulo; incluir zonas ajenas causa lecturas de otros carriles.
  - Source: https://www.omadanetworks.com/au/support/faq/4723/
  - Kind: technique · Level: core · Also: T09
- a:N15. Postes que vibran con camiones arruinan la lectura; amaneceres y atardeceres de frente queman la imagen.
  - Source: https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf
  - Kind: mistake · Level: core

## T05 Iluminación y noche
- a:N16. Hikvision recomienda obturador rápido de noche (del orden de 1/1000) para cortar la luz de los faros, y bajar el IR si la patente se quema.
  - Source: https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf
  - Kind: technique · Level: core
- a:N17. La patente es retrorreflectiva: devuelve la luz hacia la fuente. Con IR en el eje de la cámara una cámara común la ve como un brillo blanco.
  - Source: https://support.reolink.com/hc/en-us/articles/900002181186-Can-t-See-License-Plate-at-Night
  - Kind: definition · Level: foundation · Bias: fabricante de cámaras genéricas
- a:N18. Milestone: IR con filtro de paso IR funciona bien justamente con patentes retrorreflectivas; evitar la ganancia alta porque mete ruido.
  - Source: https://www.milestonesys.com/globalassets/techcomm/ltsb/provms/english-united-states/10900.htm
  - Kind: technique · Level: core
- a:N19. Omada sugiere probar WDR prendido y apagado y decidir en el lugar; bajar el obturador si los faros encandilan.
  - Source: https://www.omadanetworks.com/au/support/faq/4723/
  - Kind: technique · Level: core
- a:N20. Ajustado de día, esperá la noche y mirá qué pasa (y al revés).
  - Source: https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf
  - Kind: rule of thumb · Level: core

## T06/T07 Alta, eventos e integración
- a:N21. Lo que manda la cámara por HTTP Listening: POST multipart con `anpr.xml` (EventNotificationAlert, eventType ANPR, licensePlate, confidenceLevel, macAddress, dateTime) más las fotos.
  - Source: https://ipcamtalk.com/threads/get-passed-license-plate-numbers-using-isapi.79032/post-888496
  - Kind: template · Level: core
- a:N22. Un integrador con cámaras detrás de NAT no podía saber de qué cámara venía cada POST: el contenido trae pocos campos; al cambiar a "vehículos mixtos" la cámara dejó de enviar.
  - Source: https://ipcamtalk.com/threads/assistance-with-hikvision-ds-2cd7a26g0-p-izs-integration-using-http-listening.79674/post-897038
  - Kind: story · Level: core · Also: T16
- a:N23. Si la cámara no lee, igual saca la foto y la marca "NO PLATE".
  - Source: https://blog.epcom.net/?p=128
  - Kind: definition · Level: core · Also: T16
- a:N24. ISAPI se consulta por HTTP con autenticación Digest y respuestas XML; sirve para sondear salud de equipos Hikvision.
  - Source: https://hertzbeat.incubator.apache.org/docs/help/hikvision_isapi
  - Kind: definition · Level: core · Also: T16
- a:N25. ONVIF Profile M estandariza metadatos y eventos de analíticas (incluida LPR); Profile S es streaming; Profile T suma H.264/H.265; Profile D cubre periféricos de acceso como cámaras LPR.
  - Source: https://www.onvif.org/blog/2021/08/04/do-you-know-your-onvif-profiles/
  - Kind: definition · Level: core
- a:N26. El OCR, el umbral de confianza y las reglas de sintaxis regional son del fabricante; ONVIF no los garantiza.
  - Source: https://www.forasoft.com/learn/video-surveillance/articles-vms/license-plate-recognition-lpr-anpr
  - Kind: rule of thumb · Level: advanced
- a:N27. go2rtc toma fuentes RTSP y las entrega al navegador en varios formatos; la conexión activa muestra IP, formato y bytes.
  - Source: https://pkg.go.dev/github.com/AlexxIT/go2rtc
  - Kind: definition · Level: core · Also: T08

## T08 Hora y grabación
- a:N28. Sin hora confiable la grabación pierde valor de prueba; los relojes de PC derivan; NTP es el estándar y en redes cerradas conviene un servidor de hora local.
  - Source: https://mobatime.com/support/faq/why-is-time-important-for-cctv
  - Kind: rule of thumb · Level: core · Bias: vende servidores de hora
- a:N29. "Sync with PC" pone la hora una vez y después deriva; NTP la corrige a intervalos.
  - Source: https://www.cctvcameraworld.com/security-cameras-must-show-accurate-time-for-court/
  - Kind: technique · Level: core
- a:N30. Unos segundos de deriva desalinean dos cámaras y arruinan la reconstrucción de un incidente.
  - Source: https://www.forasoft.com/learn/video-surveillance/glossary/terms-vms/time-sync
  - Kind: rule of thumb · Level: core
- a:N31. MinIO expira objetos por regla de ciclo de vida en días por bucket.
  - Source: https://min.io/docs/minio/linux/administration/object-management/create-lifecycle-management-expiration-rule.html
  - Kind: technique · Level: advanced

## T13/T15 Avisos
- a:N32. Telegram Bot API: el bot manda mensajes y fotos por HTTP con su token; fotos hasta 10 MB.
  - Source: https://core.telegram.org/bots/api
  - Kind: definition · Level: core
- a:N33. Web Push: el service worker recibe el mensaje aunque la app no esté abierta; la suscripción tiene un endpoint que conviene mantener secreto.
  - Source: https://developer.mozilla.org/en/docs/Web/API/Push_API
  - Kind: definition · Level: core

## T16 Exactitud real y voces que discrepan
- a:N34. Roseville (California): de 1427 alertas de vehículo buscado, 71 % fueron lecturas equivocadas (un 9 leído como 8 seis veces); nadie fue detenido porque los policías verificaban cada alerta.
  - Source: https://www.techspot.com/community/topics/one-california-town-found-flocks-license-plate-cameras-were-wrong-71-of-the-time.298313/
  - Kind: story · Level: core · Also: T13
- a:N35. "LPR es una conjetura, no una credencial": un residente con auto prestado queda afuera; la exactitud publicada descarta casos difíciles.
  - Source: https://gatesentry.com/blog/license-plate-recognition-hoa-gates/
  - Kind: story · Level: core · Bias: vende credenciales móviles
- a:N36. Las cifras de 99 % son sobre patentes legibles; en un acceso que depende solo de LPR, unos pocos puntos de fallo son un problema en la fila.
  - Source: https://www.intertraffic.com/news/parking/automatic-number-plate-recognition-read-rate
  - Kind: rule of thumb · Level: core
- a:N37. Definí qué es "patente legible" antes de medir exactitud; patentes dobladas, tapadas o con portapatente no cuentan igual.
  - Source: https://perceptics.com/measuring-license-plate-recognition-accuracy/
  - Kind: test · Level: core · Bias: fabricante

## Disagreements seen
- Obturador nocturno: Hikvision pide del orden de 1/1000 (https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf); el perfil barrio-noche de OmniAccess usa 1/500 para tráfico lento (producto, notes b).
- WDR: Omada propone probar con y sin (https://www.omadanetworks.com/au/support/faq/4723/); OmniAccess lo apaga por defecto en el perfil nocturno.
- Píxeles: 100 px mínimo (https://www.dtksoft.com/camera-installation) contra 130 px mínimo (Hikvision) y 100 a 300 px (Manual del Instalador).
- LPR como credencial: https://gatesentry.com/blog/license-plate-recognition-hoa-gates/ dice que no alcanza sola; Syscom y Epcom la usan para abrir barreras.
- IR: Reolink dice que el IR quema la patente; Milestone dice que el IR con filtro es lo mejor para patentes retrorreflectivas (la diferencia es cámara dedicada o genérica).

## Best stories
- Roseville: 71 % de alertas equivocadas, un 9 leído como 8: https://www.techspot.com/community/topics/one-california-town-found-flocks-license-plate-cameras-were-wrong-71-of-the-time.298313/
- Dartford Tunnel 1979, primeras pruebas: https://www.traffictechnologytoday.com/features/feature-who-invented-anpr-the-untold-british-story-behind-a-global-traffic-technology-revolution.html
- La residente con el auto del taller frente al portón: https://gatesentry.com/blog/license-plate-recognition-hoa-gates/
- Las cámaras detrás de NAT que no decían quién eran: https://ipcamtalk.com/threads/assistance-with-hikvision-ds-2cd7a26g0-p-izs-integration-using-http-listening.79674/post-897038
- Patente Mercosur en Montevideo, 2015: https://www.autoblog.com.uy/2015/04/ya-circulan-las-primeras-patentes.html
