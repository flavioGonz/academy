# Notes: batch d (lección IVR que solo anuncia)
Pages read: 14 (10 nuevas más los manuales del UCM630x y del UCM630xA, la RFC 4733 y la página de extensiones especiales de Asterisk, que ya estaban en raw/). With notes: 13. Skipped: 1 (la FAQ de FXO de Ipitomy habla de un gateway GXW410x: solo sirve para "las líneas calientes se bajan de ganancia", que ya cubre la lección Identificador y audio).
Nota de alcance: el caso real (IVR que solo anuncia, aviso de inválido por marcar internos prendido y DTMF falso de la línea) no está en ninguna fuente; los nombres de la API (dial_extension, dial_ringgroup, dial_other_extension, iloop, tloop) y el aviso "Lo siento, no lo entiendo" salen de la lectura de la configuración en el caso, no de documentación pública. Grandstream no publica qué hace la UCM por dentro con un dígito cuando el IVR no tiene teclas.

## T27 El IVR por dentro: bienvenida, espera, Timeout e Invalid
- d:N1. En el firmware actual el IVR se arma en Basic Call Features > IVR con General (Name, Extension, Auto Record, Prompt Language, Prompt), Dialed Number (Dial Other Extensions, Privilege, Dial Block/Allowlist), Timeout/Invalid Settings y Other Settings (Replace Display Name, Return IVR Menu, Alert-info).
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/  Quote: "Initial tone that plays when the user enters the IVR."
  - Kind: definition
  - Level: foundation
  - Bias: fabricante
- d:N2. Prompt es la bienvenida del IVR (el manual la llama también Welcome Prompt cuando explica Custom Prompt); se pueden poner hasta 5 por IVR. La UCM admite hasta 500 IVR, con hasta 64 niveles.
  - Source: https://documentation.grandstream.com/knowledge-base/how-to-use-ivr/  Quote: "Up to 5 welcome prompts can be configured per IVR."
  - Kind: number
  - Level: foundation
  - Bias: fabricante
- d:N3. Timeout/Invalid Settings: Digit Timeout (s), 3 de fábrica, es el tiempo entre dígitos; Response Timeout (s), 10 de fábrica, es lo que espera después de los prompts; Response Timeout Prompt y Response Timeout Prompt Repeats (3); Invalid Input Prompt e Invalid Input Prompt Repeats (3). Al terminar las repeticiones va al destino de Timeout o de Invalid si está configurado, o corta.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/  Quote: "When the loop ends, it will go to the timeout destination if configured, or hang up."
  - Kind: definition
  - Level: core
  - Also: T08
  - Bias: fabricante
- d:N4. La guía de IVR repite lo mismo con otras palabras: después de la última repetición, la llamada va al destino de Timeout o de Invalid, o se cae.
  - Source: https://documentation.grandstream.com/knowledge-base/how-to-use-ivr/  Quote: "After the final repeat, calls will be redirected to the Timeout destination (if configured) or dropped."
  - Kind: rule of thumb
  - Level: core
  - Bias: fabricante
- d:N5. Key Pressing Events en modo Standard define teclas de un dígito (0 a 9, * y #), cada una con hasta cinco destinos por horario; además están Timeout ("cuando termina el Timeout Repeat Loop") e Invalid ("cuando termina el Invalid Repeat Loop"), y End Key (# o *). Entre los destinos posibles hay Custom Prompt, Hang-up y Announcement.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/  Quote: "Configures the destination when the Timeout Repeat Loop is done."
  - Kind: definition
  - Level: core
  - Bias: fabricante
- d:N6. Asterisk, que está debajo de la UCM, usa Background() para el prompt que escucha DTMF: reproduce el audio, escucha teclas y busca una extensión que coincida con lo marcado; WaitExten() agrega unos segundos de espera después del audio.
  - Source: https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Background-and-WaitExten-Applications/  Quote: "plays a sound prompt, but listens for DTMF input"
  - Kind: definition
  - Level: advanced
  - Bias: none
- d:N7. Extensiones especiales: si Asterisk no encuentra una extensión que coincida con los dígitos marcados durante Background() o WaitExten(), manda la llamada a i (Invalid entry); si el que llama no marca nada a tiempo, a t (Response timeout).
  - Source: https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/  Quote: "If Asterisk can't find an extension in the current context that matches the digits dialed"
  - Kind: definition
  - Level: core
  - Bias: none
- d:N8. El ejemplo de Asterisk de menú con i y t: un 3 que no existe dispara "Invalid extension '3'", suena option-is-invalid y el menú vuelve a empezar; sin marcar nada, a los diez segundos va a t.
  - Source: https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Handling-Special-Extensions  Quote: "Invalid extension '3' in context 'demo-menu'"
  - Kind: story
  - Level: core
  - Bias: none
- d:N9. En FreePBX 2.10 un integrador no lograba que el aviso de inválido volviera al menú: sonaba el aviso, se quedaba esperando y caía en el de timeout hasta cortar. La respuesta: los destinos i y t se configuran aparte y la grabación de reintento solo suena antes de ir al destino.
  - Source: https://community.freepbx.org/t/ivr-invalid-and-timeout-routing-issues/15994  Quote: "The IVR 'invalid option' announcement plays then just sits there"
  - Kind: story
  - Level: core
  - Bias: none

## T28 Marcar internos desde el IVR y la alternativa Announcement
- d:N10. Dial Other Extensions elige a qué destinos puede marcar directo el que llama (Extension, External Number, Meeting, IVR, Call Queue, Ring Group, Paging/Intercom, Voicemail Groups, Fax, Dial By Name) además de lo que está en Key Pressing Events. Prendido, el que llama puede discar un número y el IVR lo manda ahí.
  - Source: https://documentation.grandstream.com/knowledge-base/how-to-use-ivr/  Quote: "callers can dial an extension number when accessing IVR"
  - Kind: definition
  - Level: core
  - Also: T08
  - Bias: fabricante
- d:N11. En los ejemplos de la guía, Dial Other Extensions queda apagado a propósito: así solo valen los destinos de Key Pressing Events. Las teclas numeradas funcionan sin esa opción.
  - Source: https://documentation.grandstream.com/knowledge-base/how-to-use-ivr/  Quote: "only configured destinations in Key Pressing Events are authorized"
  - Kind: rule of thumb
  - Level: core
  - Bias: fabricante
- d:N12. En versiones anteriores del firmware la opción de marcar por troncal era una casilla aparte (Dial Trunk); en el UCM630xA 1.0.19 pasó a llamarse Dial External Number y se movió dentro de Dial Other Extensions.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/  Quote: "option has been renamed to Dial External Number and moved to the Dial Other Extensions section"
  - Kind: definition
  - Level: advanced
  - Bias: fabricante
- d:N13. Advanced Call Features > Announcement (distinto de Announcement Paging y de Announcement Center): un audio que no se puede saltear y después pasa solo a un destino (extensión, grupo, cola, IVR, buzón, número externo, Hang-up). Se usa como destino de una ruta entrante. Campos: Name, Prompt (existente, subido o TTS), Default Destination y Call Privileges si el destino es externo; el permiso para externos se sumó en el firmware 1.0.35.8.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/  Quote: "allows users to set an unskippable audio prompt to play to callers before automatically routing them"
  - Kind: technique
  - Level: core
  - Bias: fabricante
- d:N14. La misma función figura en el manual del UCM630x actual, con la misma ruta de menú.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/  Quote: "Announcements can be assigned as a destination in the Inbound Routes page."
  - Kind: definition
  - Level: core
  - Bias: fabricante
- d:N15. Custom Prompt acepta mp3, wav, ulaw, alaw y gsm, hasta 30 MB; el WAV va PCM de 16 bits, mono, 8000 Hz. Un prompt subido queda disponible en cualquier campo de prompt del IVR, también en Response Timeout Prompt.
  - Source: https://documentation.grandstream.com/knowledge-base/how-to-use-ivr/  Quote: "PCM encoded, 16-bit, mono, 8000 Hz"
  - Kind: template
  - Level: foundation
  - Bias: fabricante

## T29 DTMF falso en líneas analógicas
- d:N16. Falsing es cuando un decodificador de señales detecta una entrada válida que nadie quiso mandar; cuando la voz pega justo en la frecuencia del detector se llama talk-off.
  - Source: https://en.wikipedia.org/wiki/Falsing  Quote: "a condition called talk-off"
  - Kind: definition
  - Level: core
  - Bias: none
- d:N17. Como el DTMF viaja dentro de la banda de voz, la norma pone límites estrictos de duración mínima, espacio entre dígitos, desvío de frecuencia y diferencia de nivel entre los dos tonos (twist): son los filtros que usa el detector para no confundir voz con teclas. Touch-Tone salió al público el 18 de noviembre de 1963; la norma es la UIT-T Q.23.
  - Source: https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling  Quote: "strict limits for timing (minimum duration and interdigit spacing)"
  - Kind: definition
  - Level: advanced
  - Also: T20
  - Bias: none
- d:N18. RFC 4733 (2006) lleva las teclas como eventos en RTP; un equipo que atiende líneas analógicas recibe tonos en el audio y manda eventos, o sea que la detección en el cobre la hace él.
  - Source: https://datatracker.ietf.org/doc/html/rfc4733  Quote: "an end system serving analogue lines"
  - Kind: definition
  - Level: advanced
  - Bias: none
- d:N19. El caso de Asterisk por FXO: un IVR conectado a una línea analógica recibía "random digits"; el técnico probó dtmfmode inband y relaxdtmf sin resultado. Se cerró como consulta de soporte, sin solución publicada.
  - Source: https://issues-archive.asterisk.org/ASTERISK-22433  Quote: "I am able to get random digits on the IVR"
  - Kind: story
  - Level: core
  - Bias: none
- d:N20. El mismo técnico en el foro: marcó 211 y el sistema detectó solo un 1, y no siempre el mismo dígito; con un teléfono de otra compañía andaba. La respuesta: activar el registro de DTMF y mirar qué llega, porque los ajustes de sip.conf no tocan los canales analógicos.
  - Source: https://community.asterisk.org/t/my-elastix-stopped-detecting-dtmf-tones-over-digium-fxo-port/43785  Quote: "The DTMF log is very handy if you have issues with IVR's"
  - Kind: story
  - Level: core
  - Also: T22
  - Bias: none
- d:N21. El problema inverso en FreePBX con una placa de cuatro FXO: las teclas no se detectaban mientras sonaba la bienvenida, solo en silencio. Primero se sospechó de niveles y del híbrido (fxotune); se arregló con relaxdtmf=yes en chan_dahdi.conf. El audio que vuelve por la línea mientras suena el prompt cambia lo que ve el detector.
  - Source: https://community.freepbx.org/t/dtmf-in-ivr-on-analog-lines/14916  Quote: "Unless they are pressed during a silent period in the IVR"
  - Kind: story
  - Level: core
  - Also: T20
  - Bias: none
- d:N22. En la UCM630xA, Enable Relaxed DTMF está en PBX Settings > SIP Settings (de fábrica en No); el manual lo describe para SIP, no para los FXO.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/  Quote: "Select to enable relaxed DTMF handling."
  - Kind: definition
  - Level: advanced
  - Bias: fabricante

## T30 Medir y verificar: CDR y llamada de prueba
- d:N23. El CDR de la UCM muestra por llamada Status, Call From, Call To, Action Type (DIAL, IVR y otros), Start Time, Call Time (de que empieza a que se corta) y Talk Time (tiempo conectado entre las partes).
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/  Quote: "Displays the mechanism/destination type used for the call (e.g., DIAL, IVR, WAKEUP, MEETING)."
  - Kind: test
  - Level: core
  - Also: T22
  - Bias: fabricante
- d:N24. Analog Record Trace (Maintenance > Signaling Troubleshooting) graba el audio de un puerto FXO para revisar problemas de la línea analógica; el manual lo propone para el identificador de llamadas.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-audio-series-user-manual/  Quote: "Analog record trace can be used to troubleshoot analog trunk issue"
  - Kind: test
  - Level: core
  - Also: T22
  - Bias: fabricante

- d:N25. El manual del UCM630x dice que la central está basada en Asterisk 16, y que los FXO y FXS se manejan con DAHDI (Digium Asterisk Hardware Device Interface): por eso la teoría de Background(), i y t de Asterisk sirve para leer el IVR de la UCM.
  - Source: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/  Quote: "Based on Asterisk version 16"
  - Kind: definition
  - Level: advanced
  - Also: T27
  - Bias: fabricante

## Disagreements seen
- Qué hace la UCM con un dígito cuando el IVR no tiene teclas: ni el manual ni la guía lo dicen. Asterisk manda a i todo lo que no coincide (https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/); en el caso real, con Dial Other Extensions apagado el aviso dejó de sonar. Queda como observación del caso, a verificar en cada firmware.
- Relaxed DTMF: en FreePBX arregló un FXO que no detectaba teclas durante el prompt (https://community.freepbx.org/t/dtmf-in-ivr-on-analog-lines/14916); en el caso de Asterisk con dígitos al azar no cambió nada (https://issues-archive.asterisk.org/ASTERISK-22433). En la UCM la opción figura en SIP Settings, no en las troncales analógicas.
- IVR o Announcement para "bienvenida y al grupo": la guía de IVR enseña IVR con menú; el manual actual tiene Announcement, que no se saltea. Ninguna fuente compara las dos.

## Best stories
- El técnico de Asterisk con "random digits" en un IVR por FXO (https://issues-archive.asterisk.org/ASTERISK-22433).
- El 211 que llegó como un 1 y el consejo de prender el registro de DTMF (https://community.asterisk.org/t/my-elastix-stopped-detecting-dtmf-tones-over-digium-fxo-port/43785).
- Las teclas que solo se detectaban en el silencio del prompt, arregladas con relaxdtmf (https://community.freepbx.org/t/dtmf-in-ivr-on-analog-lines/14916).
- El ejemplo de Asterisk: "Invalid extension '3'", option-is-invalid y el menú otra vez (https://docs.asterisk.org/Deployment/Basic-PBX-Functionality/Auto-attendant-and-IVR-Menus/Handling-Special-Extensions).
