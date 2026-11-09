# Lección 23. Cuelga y no corta

**Escuchá:** caso-no-corta.mp3 (2 min)

**La idea, en tres líneas**
- El caso: un comercio con un UCM6304A, dos líneas de Antel por FXO y dos vendedores con teléfono en la casa. La encargada: "a veces el cliente ya cortó y el teléfono sigue en llamada, en silencio o con un tu tu tu; y cuando le corto a un vendedor, a él le sigue la llamada un rato". En el CDR hay llamadas de 40 minutos que nadie hizo.
- Primero se separan los dos mundos con el CDR y Active Calls. Si la llamada colgada entró por una troncal analógica, la UCM nunca se enteró del corte: es detección (lección Tonos y corte). Si es SIP, el corte se mandó y no llegó: un BYE perdido, casi siempre por NAT o por un Contact con una IP que no sirve.
- Cada mundo tiene su red de seguridad, que se prueba: en SIP, RTP Timeout y Session Timer en la UCM y el RTP timeout del teléfono; en analógico, Maximum Call Duration y el largo máximo del buzón; en el portero, el corte después de abrir.

**Impacto:** se terminan las troncales ocupadas por llamadas muertas, los buzones llenos de tono de ocupado y los teléfonos que siguen "en llamada" con nadie del otro lado.

**Quién lo dice:** 6 de 7 fuentes (RFC 3261, RFC 4028, el manual del UCM630x, Wazo y dos hilos de la lista de Kamailio, de 2005 y de 2016) coinciden en que una llamada SIP queda viva cuando el BYE se pierde y en que la defensa son los timers de sesión y de RTP; Wazo y Kamailio discrepan en cuánto confiar en los session timers, y un caso de Asterisk muestra un RTP timeout configurado que no cortaba. En analógico, el foro de Asterisk y el manual del UCM630xA coinciden en que el corte depende de detectar tono, polaridad o corriente.

**Laboratorio** · Campo · 25 min
UCM de banco con la 1001 en la LAN (192.168.88.0/24, UCM en 192.168.88.20) y la 1002 detrás del MikroTik del banco, ruteada por ether3 en 10.10.10.32, como el "vendedor de la casa". Si tenés una línea por FXO, mejor. Datos de ejemplo.
1. Anotá el síntoma exacto y separá los mundos antes de tocar nada:
```text
¿Quién colgó primero y qué quedó vivo?   la interna, la troncal, el remoto
¿Por dónde entró esa llamada?            CDR: troncal analógica o SIP, extensión
¿Cuánto dura lo colgado?                  siempre lo mismo (un timer) o cualquier cosa
¿Qué escucha el que quedó?                ocupado de 425 Hz: FXO; silencio: SIP
```
Con una llamada colgada en curso, System Status > Active Calls la muestra con su troncal o extensión y el color: naranja pasada la media hora, roja pasada la hora. Desde ahí se puede colgar.
2. SIP, el BYE que no llega. Llamá de la 1002 a la 1001, atendé, y con la llamada en curso cortá en el MikroTik la señalización de la UCM hacia la 1002 (5060, o el puerto SIP de tu teléfono), como hace un router que se olvidó del puerto:
```routeros
/ip/firewall/filter/add chain=forward src-address=192.168.88.20 dst-address=10.10.10.32 protocol=udp dst-port=5060 action=drop comment="ies-lab-bye" place-before=0
```
Colgá la 1001. La 1002 sigue en llamada, en silencio. En Ethernet Capture de la UCM: el BYE hacia 10.10.10.32 repetido, sin 200 OK. Medí cuánto tarda la 1002 en cortar sola: es su propio RTP timeout (en un GXV3350, RTP Timeout Timer de 30 s de fábrica; anotá el de tu modelo). Sacá la regla:
```routeros
/ip/firewall/filter/remove [find comment="ies-lab-bye"]
```
3. El arreglo del caso para el remoto: en la extensión de la 1002, pestaña Advanced Settings, Enable Keep-alive con Keep-alive Frequency de 20 s, y en Media, NAT prendido como en Extensión sólida. Cada OPTIONS de la central pasa por el router del remoto y mantiene abierto el camino por donde vuelve el BYE (probalo en obra con una llamada de más de cinco minutos).
4. SIP, el teléfono que desaparece. Llamá de la 1001 a la 1002 y desenchufá el cable de la 1002 en plena llamada. La 1001 queda en silencio y la llamada sigue en Active Calls hasta que alguien cuelga. Poné la red de seguridad y repetí:
```text
PBX Settings > SIP Settings > ToS
RTP Timeout: 60        RTP Hold Timeout: 300
PBX Settings > SIP Settings > Session Timer
Timer: Sí (de fábrica)   Session Expiration: 1800   Min SE: 90
```
A los 60 segundos sin audio, la UCM corta. Session Timer solo actúa si el otro lado lo negocia: es la red de los 30 minutos.
⚠️ RTP Timeout corta también los equipos que dejan de mandar audio en mute: probalo con los teléfonos y la troncal del cliente antes de dejarlo.
5. Analógico, si tenés línea: llamá desde un celular a la línea, atendé en la 1001 y colgá el celular. Si la 1001 se queda con el ocupado y Active Calls sigue mostrando la troncal analógica, la UCM no detectó el corte: tonos de Uruguay, Busy Detection y PSTN Detection, como en Tonos y corte. Red de seguridad para las entrantes de esa línea:
```text
Extensions > (la que atiende) > Features
Call Duration Limit: Sí     Maximum Call Duration (s): 3600
Basic Call Features > Voicemail > Voicemail
Max Message Length (m): 5        (15 de fábrica)
```
Si con todo eso la línea no libera, el reclamo a Antel va con datos: qué manda la línea al cortar (tono, polaridad o corriente) según PSTN Detection y una grabación de Analog Record Trace.
6. Portero, si tenés un GDS3710: en Door System Settings > Basic Settings, Enable On Hook After Remote Door Opened, con Onhook Timer After Remote Open Door(s) en 5 (3 de fábrica). Abrí con el PIN y verificá que corta. Auto On-Hook Timer, en SIP Advanced Settings de la cuenta (300 s de fábrica), queda como última red.
7. Verificá cada red con la falla que la dispara, como en los pasos 2 y 4, y anotá en la ficha qué timer quedó, en qué equipo y con qué valor.

Firmas para la ficha:

| Mundo | Qué se ve | Causa | Arreglo |
| - | - | - | - |
| FXO | interna con ocupado, troncal analógica en Active Calls | la UCM no detecta el corte | Tonos y corte, PSTN Detection |
| FXO | buzón o cola con mensajes llenos de tono | nadie del lado de la UCM cuelga | máximos de llamada y de mensaje |
| SIP | BYE repetido sin 200 OK en la captura | el BYE no llega: NAT o firewall | Keep-alive, NAT en la extensión |
| SIP | BYE hacia una IP privada o vieja | Contact o Record-Route mal armados | NAT, External Host y Local Network Address |
| SIP | lo colgado corta solo, siempre al mismo tiempo | un timer: RTP timeout o Session Expiration | buscar por qué no llegó el BYE |
| Portero | el GDS queda en llamada después de abrir | sin corte al abrir | On Hook After Remote Door Opened |

**Regla para quedarse**
Llamada que no corta: el CDR dice si es FXO o SIP; en FXO la central no se enteró, en SIP el BYE no llegó, y la red de seguridad se prueba provocando la falla.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Session Timer, RTP Timeout, Call Duration Limit y Active Calls en el UCM630x: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Session timers, el estándar para cuando el BYE se pierde: https://datatracker.ietf.org/doc/html/rfc4028
- Llamadas fantasma y sus redes de seguridad: https://wazo-platform.org/uc-doc/administration/phantom_calls
- El celular que se iba sin BYE: https://lists.kamailio.org/pipermail/sr-users/2016-January/091262.html
- Un RTP timeout configurado que no cortaba: https://issues-archive.asterisk.org/ASTERISK-27251
- Corte después de abrir y Auto On-Hook Timer en el GDS3710: https://documentation.grandstream.com/knowledge-base/gds3710-gds3712-user-manual/
