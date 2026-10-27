# Mapa de acuerdos (versión compacta)
Notas: research/notes/a.md (web) y research/notes/b.md (producto). M cuenta páginas web que tocan el subtema; el producto se marca aparte porque es la fuente de verdad de pantallas y flujos.

## TH01 Entendé ANPR como un pipeline: capturar, limpiar, leer, validar contra una lista
- Sub-topic: T01 (also T07)
- Agree: 3 of 3. Notes: a:N3, a:N4, a:N21. Urls: https://en.wikipedia.org/wiki/Automatic_number-plate_recognition https://www.forasoft.com/learn/video-surveillance/articles-vms/license-plate-recognition-lpr-anpr https://ipcamtalk.com/threads/get-passed-license-plate-numbers-using-isapi.79032/post-888496
- Disagree: none found
- Level: foundation
- Best story: Dartford Tunnel 1979, https://www.traffictechnologytoday.com/features/feature-who-invented-anpr-the-untold-british-story-behind-a-global-traffic-technology-revolution.html

## TH02 Medí la exactitud como captura por lectura, nunca un solo número
- Sub-topic: T16 (also T01)
- Agree: 5 of 6. Notes: a:N4, a:N34, a:N36, a:N37, a:N9. Urls: forasoft LPR, techspot, intertraffic, perceptics, parking.net
- Disagree: https://home-security-guide.readthedocs.io/en/latest/cctv/17-anpr-camera-installation-guide-uk/: promete 95 % de noche bien instalada, sin separar captura y lectura.
- Level: core
- Best story: Roseville 71 %, https://www.techspot.com/community/topics/one-california-town-found-flocks-license-plate-cameras-were-wrong-71-of-the-time.298313/

## TH03 No uses LPR como única credencial: siempre hay un camino de respaldo y un humano que verifica
- Sub-topic: T03 (also T16)
- Agree: 3 of 4. Notes: a:N34, a:N35, a:N36. Producto: b:N10 (Denegado se verifica con el residente).
- Disagree: https://syscom.mx/blog/hikvision-anpr-reconocimiento-de-placas presenta la apertura por lista en cámara como solución completa.
- Level: core

## TH04 La decisión vive en dos lugares: lista en la lectora (relé) y credencial en el servidor
- Sub-topic: T03
- Agree: 2 of 2 web (a:N6, a:N7) + producto b:N6, b:N7. thin evidence en web.
- Level: core

## TH05 Antirrebote y tolerancia: la misma patente no se cuenta dos veces y un carácter de error se trata con criterio
- Sub-topic: T03 (also T07)
- Agree: 3 of 3. Notes: a:N8, a:N9, a:N10. Producto: b:N8, b:N11.
- Level: advanced

## TH06 Ángulo hasta 30° vertical y horizontal
- Sub-topic: T04
- Agree: 4 of 4. Notes: a:N11, a:N12, a:N13. Producto b:N29.
- Disagree: la guía doméstica UK sugiere 15 a 30° de costado para reducir reflejo del IR.
- Level: core

## TH07 Patente de al menos 100 a 130 px de ancho, medida en el cuadro real
- Sub-topic: T04
- Agree: 3 of 3 (a:N11, a:N12) + producto (100 a 300 px). Disagree: Hikvision pone el mínimo en 130 px, DTK en 100 px.
- Level: core

## TH08 Un carril por cámara y zona de lectura solo sobre el carril
- Sub-topic: T04 (also T09)
- Agree: 3 of 3. Notes: a:N12, a:N14. Producto b:N26, b:N29.
- Level: core

## TH09 Leé donde el vehículo va lento, antes de la barrera, con poste firme
- Sub-topic: T04
- Agree: 3 of 3. Notes: a:N13, a:N15. Producto b:N29.
- Level: core

## TH10 Probá de noche antes de entregar
- Sub-topic: T05
- Agree: 3 of 3. Notes: a:N20 + producto b:N29, b:N59.
- Level: core

## TH11 IR dedicado con patente retrorreflectiva; si se quema, bajá el IR o subí el obturador
- Sub-topic: T05
- Agree: 4 of 5. Notes: a:N16, a:N17, a:N18, a:N19.
- Disagree: https://support.reolink.com/hc/en-us/articles/900002181186-Can-t-See-License-Plate-at-Night: con cámara genérica apagar el IR y usar luz blanca.
- Level: core

## TH12 Obturador: rápido para cortar faros (1/1000) o 1/500 en tráfico lento de barrio
- Sub-topic: T05 (also T09)
- Agree: split. a:N16 (1/1000) contra producto b:N27 (1/500).
- Level: advanced

## TH13 WDR: probarlo o apagarlo de noche
- Sub-topic: T05
- Agree: split. a:N19 (probar) contra b:N27 (apagado en el perfil).
- Level: advanced

## TH14 La cámara reporta por HTTP: configurá el host de notificación y verificá que lleguen
- Sub-topic: T07 (also T06)
- Agree: 2 of 2 web (a:N21, a:N22) + producto b:N14, b:N16, b:N20.
- Level: core
- Best story: cámaras detrás de NAT, https://ipcamtalk.com/threads/assistance-with-hikvision-ds-2cd7a26g0-p-izs-integration-using-http-listening.79674/post-897038

## TH15 La foto sale aunque no haya lectura: tratá la no leída como dato, no como ruido
- Sub-topic: T07 (also T16)
- Agree: 2 of 2 (a:N23) + producto b:N18, b:N32.
- Level: core

## TH16 ISAPI con Digest es la vía de configuración y sondeo de Hikvision
- Sub-topic: T06 (also T16)
- Agree: 2 of 2 (a:N24, a:N21) + producto b:N14, b:N55.
- Level: core

## TH17 Estándares: ONVIF S/T para video, M para metadatos; el OCR sigue siendo del fabricante
- Sub-topic: T02
- Agree: 3 of 3 (a:N25, a:N26, VEG Profile M).
- Level: core

## TH18 Misma hora en cámara, NVR y servidor; preferí una fuente local
- Sub-topic: T08
- Agree: 4 of 4 (a:N28, a:N29, a:N30) + producto b:N9, b:N22, b:N23.
- Level: core

## TH19 Retención por días contra disco: calculala, no la adivines
- Sub-topic: T08
- Agree: 1 of 1 web (a:N31, thin evidence) + producto b:N5, b:N25.
- Level: advanced

## TH20 Calibrá desde el panel con perfil de partida y medí por hora
- Sub-topic: T09
- Agree: producto b:N26, b:N27, b:N28; web a:N14 apoya zona y línea. thin evidence web.
- Level: core

## TH21 El monitor se lee de lejos: verde pasa, ámbar se verifica, rojo es la alarma
- Sub-topic: T10
- Agree: producto b:N10, b:N30, b:N31. Web: a:N34 (verificar cada alerta).
- Level: foundation

## TH22 Investigá con ficha, perfil y evidencia exportada
- Sub-topic: T11
- Agree: producto b:N36 a b:N40. Web: a:N28 (valor de prueba).
- Level: core

## TH23 Merodeo y permanencia como patrones, no como alarmas sueltas
- Sub-topic: T12
- Agree: producto b:N41 a b:N43; web a:N25 (Profile M cubre loitering como metadato). thin evidence.
- Level: core

## TH24 La lista de vigilancia se carga con motivo y se verifica antes de actuar
- Sub-topic: T13
- Agree: 2 of 2 (a:N34, a:N35) + producto b:N44 a b:N46.
- Level: core

## TH25 Padrón completo: unidad, usuario, credencial, grupo
- Sub-topic: T14
- Agree: producto b:N47 a b:N51; web a:N35 (el costo del alta permanente).
- Level: core

## TH26 Avisos por Telegram, WhatsApp y push: saber qué sale y por dónde
- Sub-topic: T15
- Agree: 2 of 2 (a:N32, a:N33) + producto b:N53.
- Level: core

## TH27 "Dejaron de entrar matrículas": seguí el árbol webhooks, modo, red
- Sub-topic: T16
- Agree: producto b:N55 a b:N58; web a:N22 (cambio de modo que corta el envío).
- Level: core

## The big splits
- Obturador nocturno 1/1000 (Hikvision) contra 1/500 (perfil barrio-noche de OmniAccess): depende de la velocidad del tránsito.
- WDR prendido o apagado de noche: Omada dice probar, OmniAccess lo apaga.
- LPR como credencial única: gatesentry dice que no; distribuidores la usan sola.
- IR sí o no: depende de que la cámara sea ANPR dedicada (IR con filtro) o genérica.

## Coverage gaps
- No hay documentación pública de OmniAccess: todo lo del producto sale de manuales y código.
- No se encontró una guía oficial de Hikvision accesible por script sobre HTTP host ni sobre el conflicto ANPR/AcuSearch; se usa el manual del producto.
- Avicam LPR: el código solo tiene terminales faciales Avicam.
