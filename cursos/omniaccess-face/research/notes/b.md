# Notas b: fuentes web (raw/web)

## Colocación y foto (T03, T08)
- Control iD (https://www.controlid.com.br/docs/access-api-en/facial-recognition/recommendations-photos-install/): foto JPG o PNG, una sola cara, luz uniforme, sin barbijo, lentes recetados sí, de sol no; mínimo 160x160, máximo 1920x1080 píxeles en total; terminal a unos 1,30 m del piso; evitar sol directo sobre la cámara y contraluz fuerte; ajustar la región de interés. [T03, T08]
- Synerion GT8/GT10 (https://help.synerion.com/agile/knowledge-base/gt-installation-guidelines): cámara a 148 cm; detecta personas de 150 a 200 cm paradas a unos 50 cm; brazo VESA para sillas de ruedas o alturas fuera de rango; exposición centrada desde firmware 1.10.0; no instalar con luz fuerte detrás de la persona; barras de luz frontal al máximo por defecto; antispoof como disuasión, no atrapa todo; consentimiento del empleado con período de retención; limpiar la ventana de la cámara; volver a enrolar si cambia mucho la barba. [T03, T08, T15, T17]
- ClockRite C-400 (https://clockrite-support.helpscoutdocs.com/article/1259-c400-best-practice-for-installation): unos 1,1 m (mira hacia abajo), a 0,5 m para personas de 1,55 a 1,85 m; claraboyas y ventanas cambian la luz durante el día; enrolar sin barbijo. [T03] Discrepa en altura con los demás.
- Hikvision DS-K1T343 guía rápida 2025 (pinfo.hikvision.com, V1.1): evitar contraluz, sol directo e indirecto; fuente de luz cerca; altura recomendada de la persona 1,4 a 1,9 m; 0,5 m de distancia; "los productos biométricos no son 100 % aplicables a entornos de antisuplantación; para más seguridad, varios modos de autenticación". [T03, T15]
- Hikvision Import Data (enpinfo GUID-1C74…): foto frontal, sin gorro, JPG, de 640x480 a 2160x3840, entre 40 KB y 200 KB. [T08]
- Hikvision Import Person Pictures (enpinfo GUID-981B…): ZIP con JPG de hasta 200 KB nombrados "ID_Nombre"; opción "Verify by Device" para comprobar que el equipo reconoce la foto. [T08, T09]
- Speco (https://info.specotech.com/how-to-upload-images-for-facial-recognition): JPG menor a 70 KB, de 120x120 a 1920x1080. [T08] Otro límite: cada fabricante tiene el suyo.

## Umbral y errores (T15)
- Hikvision Set Biometric Parameters (enpinfo GUID-9F07…): nivel de liveness, distancia de reconocimiento, intervalo 1 a 10, WDR para exterior, nivel de seguridad 1:N y 1:1: "cuanto mayor el valor, menor la tasa de falsa aceptación y mayor la de falso rechazo". [T15, T03]
- AWS Rekognition thresholds (docs.aws.amazon.com): umbral por defecto 75 para asociar; todos los sistemas son probabilísticos; 80 % para una app de fotos familiares, 99 % o más para usos policiales. [T15]
- NIST FRTE 1:1 (https://pages.nist.gov/frvt/html/frvt11.html): FNMR es la proporción de comparaciones de la misma persona por debajo del umbral fijado para un FMR dado; FMR es la proporción de impostores en o por encima del umbral. [T15]
- NIST 2019 (https://www.nist.gov/node/1603646 y la reseña de infodocket): 189 algoritmos de 99 desarrolladores, 18,27 millones de imágenes de 8,49 millones de personas; la mayoría muestra diferencias demográficas; falsos positivos 10 a 100 veces más en algunos grupos según el algoritmo; los más equitativos están entre los más precisos. [T15, T17] Voz crítica sobre la tecnología.
- Senstar Symphony face settings (xnet.senstar.com): giro máximo recomendado 45° (máx. 70°), inclinación 20° (máx. 45°), detección de ataque de suplantación apagada por defecto. [T03, T15]

## Eventos y video (T05, T11)
- Wikipedia Webhook (https://en.wikipedia.org/wiki/Webhook): llamada HTTP que un sistema hace a otro cuando pasa algo; el receptor expone una URL. [T05]
- CIE Group sobre Akuvox Event Trigger Rules (agosto 2026): en Smart Access Cloud un evento puede disparar email, push, webhook a terceros, relé o bloqueo; hasta cinco acciones por regla. [T05] Alternativa en la nube a la Action URL local.
- go2rtc MJPEG (raw.githubusercontent.com/AlexxIT/go2rtc): puede dar stream MJPEG o snapshot JPEG por API, convertir H264 con FFmpeg; `api/stream.mjpeg?src=camera1`. [T11]
- MDN Push API (developer.mozilla.org): la app web recibe mensajes del servidor aunque no esté en primer plano, con permiso del usuario y service worker. [T11]

## Privacidad (T17)
- IMPO Ley 18.331 art. 4 (https://www.impo.com.uy/bases/leyes/18331-2008/4): literal Ñ, datos biométricos: datos obtenidos por un tratamiento técnico específico de características físicas, fisiológicas o conductuales que permitan o confirmen la identificación única, como huellas, reconocimiento de imagen o voz. Agregado por la Ley 19.924 del 18/12/2020, art. 86.
- IMPO art. 9 (…/9): consentimiento libre, previo, expreso e informado, documentado; excepciones (fuentes públicas, funciones del Estado u obligación legal, etc.).
- IMPO art. 18 (…/18): datos sensibles: nadie puede ser obligado a darlos; consentimiento expreso y escrito.
- URCDP Dictamen 3/023 (gub.uy, 14/03/2023, BPS "Fe de vida"): cita el art. 4 lit. Ñ; el art. 18 bis exige, cuando se usan datos biométricos, tener en cuenta el art. 9 y hacer una evaluación de impacto previa; la base debe inscribirse ante la URCDP (art. 6); recomienda analizar ciclo de vida de los datos, seguridad y transferencias internacionales.
- CSO Online sobre biometría en el trabajo (GDPR): en la relación laboral el consentimiento no es una base confiable por el desequilibrio de poder; hace falta una alternativa igual de cómoda para quien no acepta. [T17] Discrepa de "con un consentimiento firmado alcanza".
- MinIO lifecycle (docs.min.io): reglas de vencimiento borran objetos automáticamente a N días de creados, sobre un bucket o una ruta dentro de él (`mc ilm rule add ALIAS/PATH --expire-days`). [T17, T14]
