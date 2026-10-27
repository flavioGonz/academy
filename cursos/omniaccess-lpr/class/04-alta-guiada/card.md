# Lección 4. Alta guiada

**Escuchá:** alta-guiada.mp3 (2 min)

**La idea, en tres líneas**
- Menú lateral → Dispositivos → Agregar → Cámara LPR abre un alta por pasos: Equipo, Conexión, Ubicación, Grabación y Puesta a punto.
- En Ubicación se decide el Sentido (Entrada o Salida: la columna del monitor, si suma a "adentro" y si cierra visitas) y el Grupo de acceso; sin grupo, la cámara no deja pasar a nadie por servidor.
- Crear y poner a punto configura la cámara por ISAPI y muestra cada tarea: hora, servidor de alarmas hacia OmniAccess (HTTP host), modo ANPR, video H.264, video en vivo, cargar matrículas, vincular la grabación y calcular la retención.

**Impacto:** una cámara queda reportando, con video en vivo y con su lista cargada en un solo recorrido, sin entrar a la web de la cámara para cada cosa.

**Quién lo dice:** 2 de 2 hilos de practicantes (IPCamTalk) muestran que la cámara Hikvision reporta por HTTP con un XML y que identificarla bien es el problema típico; el recorrido de alta sale del código de OmniAccess (el Manual del Instalador lo llama "Dispositivos LPR → Agregar", en esta versión el menú es Dispositivos).

**Laboratorio** · Campo · 25 min
Cámara ANPR Hikvision de prueba con IP fija `192.0.2.21`, servidor en `192.0.2.10`, usuario del integrador creado en la cámara (no el de fábrica).
1. Dispositivos → Agregar → Cámara LPR.
2. Equipo: Fabricante Hikvision. Nombre con la convención del manual: acceso, sentido y último octeto de la IP.
```text
P1 - Entrada (21)
```
3. Conexión: IP `192.0.2.21`, usuario y contraseña del integrador, autenticación Digest.
4. Ubicación: Sentido Entrada y un grupo de acceso de prueba (por ejemplo "Residentes"). Fijate el aviso si lo dejás en Sin grupo.
5. Grabación: elegí el NVR y el canal donde se graba esta cámara (o dejá que lo busque por IP).
6. Tocá Crear y poner a punto y mirá cada tarea. Anotá cuáles quedan en verde, en error o salteadas y el detalle de cada una.
7. Abrí Configuración → Sistema → Webhooks, pasá un auto y confirmá que llega el evento con la matrícula y el nombre de la cámara.
8. Si la tarea Modo ANPR quedó en error ("está en 'smart'"), no fuerces nada todavía: es el caso que se resuelve en el diagnóstico del final del curso.
⚠️ Si después de un reset de fábrica la cámara deja de reportar, casi siempre es porque perdió el HTTP host: repetí la puesta a punto desde la ficha del equipo.

**Regla para quedarse**
Una cámara está dada de alta cuando la puesta a punto queda en verde y el primer evento aparece en Webhooks con su nombre.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Integrador con cámaras detrás de NAT que no se identificaban: https://ipcamtalk.com/threads/assistance-with-hikvision-ds-2cd7a26g0-p-izs-integration-using-http-listening.79674/post-897038
- Qué trae el POST que manda la cámara: https://ipcamtalk.com/threads/get-passed-license-plate-numbers-using-isapi.79032/post-888496
- ISAPI por HTTP con autenticación Digest: https://hertzbeat.incubator.apache.org/docs/help/hikvision_isapi
