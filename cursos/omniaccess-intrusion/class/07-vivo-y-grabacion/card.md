# Lección 7. Vivo y grabación

**Escuchá:** vivo-y-grabacion.mp3 (2 min)

**La idea, en tres líneas**
- En el canal, el botón rojo de video abre **Ver en vivo (incluye grabación y evidencia)** con tres pestañas: **Vivo**, **Grabación** y **Evidencia**. El vivo pasa por go2rtc; **SD** usa el flujo secundario y **HD** el principal. Si el nombre de la cámara dice PTZ, se mueve arrastrando y con la rueda.
- **Seguimiento visual**: en el vivo ponés íconos de las cámaras vecinas en el punto de la escena por donde se pasa a cada una; tocando el ícono seguís al intruso. El ícono rebota en rojo si esa cámara tiene eventos.
- **Grabación** reproduce el NVR en una línea de tiempo con zoom y velocidad 1, 2, 4 u 8, con los eventos marcados. Hace falta la cámara vinculada a su NVR y canal. El botón de descarga baja el clip (10 s antes y 10 s después) o lo manda por WhatsApp.

**Impacto:** el operador sabe qué pasó antes del cruce y hacia dónde fue, sin salir de la ficha.

**Quién lo dice:** 2 de 3 fuentes explican el camino del video: RTSP desde la cámara y un servidor como go2rtc que lo adapta al navegador y transcodifica solo si hace falta. Lo de OmniAccess sale del código.

**Laboratorio** · Foco · 20 min
1. En **Monitor Intrusión**, tocá el botón rojo de video de "Perímetro Norte 12". Esperá "En vivo" y probá **SD** y **HD**: anotá cuánto tarda cada uno.
2. Tocá el lápiz (**Editar seguimiento visual**) → **Agregar cámara** → "Perímetro Sur 07". Arrastrá el ícono al punto del cuadro por donde se pasa a esa cámara y terminá la edición.
3. Tocá el ícono: el vivo salta a la otra cámara y la anterior queda en una ventanita.
4. Pestaña **Grabación**: elegí la hora del último cruce con la línea de tiempo, retrocedé 10 segundos y mirá a velocidad 2.
5. Tocá la descarga (**Descargar o enviar por WhatsApp**) y bajá un clip de 10 s antes y 10 s después. Si la instalación tiene WhatsApp, probá mandarlo a un destinatario de prueba.
6. Pestaña **Evidencia**: las últimas detecciones de esa cámara con su foto.

⚠️ "Sin NVR/canal para reproducir grabación." quiere decir que falta vincular la cámara a su NVR y canal en Dispositivos. "Sin grabación en este horario" es otra cosa: el NVR no tiene video de ese momento.

**Regla para quedarse**
Antes de decir "no hay nada", mirá los 10 segundos de antes en la grabación.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- go2rtc: entrada de decenas de protocolos y transcodificación solo si hace falta: https://pkg.go.dev/github.com/AlexxIT/go2rtc
- RTSP 2.0, el protocolo con el que se pide el video a la cámara (RFC 7826): https://datatracker.ietf.org/doc/html/rfc7826
- Perfil ONVIF S, video por IP entre cámara y cliente: https://www.onvif.org/profiles/profile-s/
