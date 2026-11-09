# Lección 22. Video de un lado

**Escuchá:** caso-video-un-lado.mp3 (2 min)

**La idea, en tres líneas**
- El caso: el encargado de un depósito tiene un GXV3350 conectado a la central por un router 4G. En las videollamadas con recepción (GXV3480) él la ve perfecto; recepción ve negro, o la imagen del depósito congelada y a saltos. El audio anda, con algún corte.
- El video de un lado se separa en tres lugares, en este orden: no se manda (cámara, obturador, video apagado, `sendonly`, `recvonly` o `m=video 0` en el SDP), se manda y llega roto (pérdida en el camino, ancho de banda, puertos) o llega entero y no se decodifica (perfil H.264, `packetization-mode`). La captura en la UCM, que está en el medio, dice en cuál estás.
- Antes de todo, una pregunta: ¿el lado que no se ve puede mandar video? Un portero GDS371x manda y no recibe, y muchos GRP muestran solo audio o una foto JPEG: ahí "uno ve y el otro no" es lo normal.

**Impacto:** dejás de cambiar codecs al azar: en una captura sabés si el problema es el equipo que manda, el enlace o el que recibe.

**Quién lo dice:** 5 de 6 fuentes oficiales (los manuales de la UCM630x, el GXV3350, el GDS3710, la FAQ del GDS371x y la de los GXV34x0) coinciden en que el video es un flujo aparte que cada extensión y cada equipo tiene que tener habilitado, y que la resolución, el bit rate y el perfil se ajustan por equipo; Grandstream recomienda bajar a VGA y 384 kbps cuando no hay video. La RFC 3264 fija cómo se lee `sendonly`, `recvonly` y el puerto 0. Ninguna fuente compara las causas entre sí: el orden sale del método.

**Laboratorio** · Campo · 25 min
Dos videoteléfonos en una UCM de banco: la 1003 (GXV3480, "recepción") en la LAN 192.168.88.0/24 con la UCM en 192.168.88.20, y la 1004 (GXV3350, "depósito") detrás de un MikroTik que la rutea por ether3, 10.10.10.31 en 10.10.10.0/24. Un Wave en una notebook sirve si no tenés el segundo GXV. Datos de ejemplo.
1. Anotá el síntoma exacto antes de tocar nada:
```text
¿Quién no ve a quién?              recepción no ve al depósito
¿Negro desde el inicio, congelado o a saltos?
¿Con otros equipos o sedes pasa?   ¿solo con el que tiene 4G?
¿Ese equipo puede mandar video?    GDS: manda y no recibe; GRP: audio o JPEG; GXV: obturador, atendió solo audio
```
2. Dejá H.264 en Codec Preference de la 1003 y la 1004 (en la extensión, pestaña Media), iniciá Ethernet Capture en la UCM y hacé una videollamada de 20 segundos. En Wireshark, RTP Streams muestra cuatro flujos: audio y video, cada uno en los dos sentidos. El video es el payload H.264 (99 de fábrica en los GXV) y la línea `a=fmtp:99` trae `profile-level-id` y `packetization-mode`.
3. Provocá una falla de negociación para ver la diferencia: sacá H.264 de la 1004 y repetí. Nadie ve video y en la respuesta aparece `m=video 0`: eso no es "de un lado", es video rechazado para los dos. Volvé a poner H.264.
4. Provocá el caso. En el MikroTik, limitá la subida de la 1004 como un 4G con poca señal:
```routeros
/queue/simple/add name=simula-4g target=10.10.10.31/32 max-limit=768k/10M comment="ies-lab-video"
```
Videollamada de la 1003 a la 1004: la 1004 ve a la 1003; la 1003 ve negro, congelado o a saltos. El GXV3350 manda de fábrica 720P a 2048 kbps, casi tres veces lo que entra.
5. Diagnosticá en los tres lugares con la captura de la UCM:
```text
¿se manda?           hay flujo de video de 10.10.10.31 hacia la UCM y el SDP dice sendrecv
¿llega entero?       RTP Streams, columna Lost; RTP Stream Analysis: saltos de secuencia
¿se decodifica?      solo si llega entero: profile-level-id y packetization-mode de cada lado
```
El flujo de video de la 1004 llega con pérdida alta (Lost se calcula con los números de secuencia); el de la UCM hacia la 1004, sin pérdida. Se manda y llega roto, en el sentido de subida del depósito: es el enlace.
6. Arreglá en el GXV del depósito lo que recomienda Grandstream para redes que no dan:
```text
Account > Codec Settings
H.264 Image Size: VGA      Video Bit Rate: 384 kbps
```
7. Verificá con la misma captura: el flujo de la 1004 sin pérdida y la imagen fluida en la 1003. Sacá la cola (`/queue/simple/remove [find comment="ies-lab-video"]`). En la ficha de la sede: subida medida, resolución y bit rate que quedaron.
8. El tercer lugar, para reconocerlo: con la cola sacada, cerrá el obturador de privacidad del GXV3480 y llamá. El flujo de video llega entero y con paquetes, y del otro lado se ve negro: la fuente es la cámara. Si un flujo entero no se ve y la cámara está bien, compará el `profile-level-id` y el `packetization-mode` de los dos SDP; en el GDS3710, SIP Packetization Compatibility Mode existe para videoteléfonos que solo decodifican `packetization-mode=0` (probalo según el modelo y el firmware).

Firmas para la ficha:

| Lugar | Causa | Qué se ve |
| - | - | - |
| No se manda | cámara tapada o sin permiso (Wave), atendió solo audio | sin flujo de video de ese lado, o flujo con imagen negra |
| No se manda | `sendonly` o `recvonly` en el SDP | el `a=` de la línea `m=video` |
| No se manda | H.264 fuera de Codec Preference | `m=video 0`: no ve ninguno de los dos |
| Llega roto | subida chica, 720P a 2048 kbps | Lost alto en un solo flujo de video |
| Llega roto | puerto de video bloqueado o reescrito | audio con flujo, video sin flujo de vuelta |
| No se decodifica | perfil o `packetization-mode` que el otro no arma | flujo entero, pantalla negra |
| Congelado | cuadro completo perdido sin pedido de refresco | imagen quieta hasta el próximo I-frame |

⚠️ La cola del MikroTik es solo para el banco: en un router de cliente, un `max-limit` mal puesto le baja la velocidad a toda la sede.

**Regla para quedarse**
Video de un lado: primero si ese equipo puede mandar, después si el flujo llega entero y recién al final el decodificador.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Codecs de video del GXV3350, H.264 Image Size, bit rate y RFC5168: https://documentation.grandstream.com/knowledge-base/gxv3350-administration-guide/
- El GDS371x manda video pero no lo recibe: https://documentation.grandstream.com/knowledge-base/gds371x-gds370x-faq/
- Perfil, I-frame y packetization-mode en el GDS3710: https://documentation.grandstream.com/knowledge-base/gds3710-gds3712-user-manual/
- sendonly, recvonly y puerto 0 en la oferta y respuesta: https://datatracker.ietf.org/doc/html/rfc3264
- profile-level-id y packetization-mode de H.264 sobre RTP: https://datatracker.ietf.org/doc/html/rfc6184
- El teléfono sin cámara que pedía recvonly: https://issues-archive.asterisk.org/ASTERISK-19830
