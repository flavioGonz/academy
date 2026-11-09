# Lección 21. Audio en un sentido

**Escuchá:** caso-audio-un-sentido.mp3 (2 min)

**La idea, en tres líneas**
- El caso: recepción atiende por la Troncal SIP de Antel y el que llama la escucha, ella a él no. Las internas y los remotos andan bien. Lo único que cambió fue que se sumaron internos remotos con External Host.
- El método va antes que la herramienta: síntoma exacto (quién no oye a quién, en qué llamadas, desde cuándo y qué cambió), captura en la interfaz por donde sale ese audio, hipótesis en orden y una prueba que separe cada una.
- El sentido que falta dice dónde mirar. Si la oficina no oye al de afuera, el audio de afuera va a una dirección equivocada: la línea `c=` que anunció la UCM. Si el de afuera no oye a la oficina, el audio de la UCM sale mal: por otra interfaz o hacia otra IP.

**Impacto:** el reclamo "se escucha de un solo lado" se cierra con una captura y un cambio, sin tocar routers a ciegas ni culpar a Antel.

**Quién lo dice:** 4 de 5 fuentes (el manual del UCM630x, la guía de internos remotos, PathSolutions y un hilo de FreePBX) ponen primero lo que cada lado anuncia en el SDP y el camino de vuelta del audio; otro hilo de FreePBX lo resolvió con el codec y uno con el firmware del teléfono. Ninguna fuente pública trae el caso de la troncal de Antel con External Host: sale de juntar el manual con lo que ya armaste en Troncal SIP de Antel.

**Laboratorio** · Campo · 25 min
El banco de la lección Troncal SIP de Antel: tu UCM en modo Dual con LAN1 en 198.51.100.2/30 y, conectada a ese puerto, otra UCM (o un Asterisk) que hace de Antel en 198.51.100.1, con su Peer SIP Trunk hacia la tuya y NAT en No (si está en Sí, devuelve el audio adonde le llega y tapa la falla). Una interna en cada una (1001 en la tuya, 2001 en la "de Antel") y una notebook con Wireshark. Todo es de ejemplo.
1. Antes de tocar nada, anotá el síntoma exacto en la ficha. Estas cuatro preguntas ordenan todo lo que sigue:
```text
¿Quién no oye a quién?            la oficina al de afuera / el de afuera a la oficina
¿En qué llamadas?                 troncal, internas entre sí, internos remotos
¿Desde cuándo y qué cambió?       firmware, router, External Host, una VLAN nueva
¿Desde el primer segundo?         si además corta a los 30 y pico: lección Audio de un lado
```
2. Mirá la llamada sana, así sabés cómo se ve cuando anda. Iniciá la captura en el puerto de la troncal y llamá de la 1001 a la 2001 por la troncal durante 20 segundos:
```text
Maintenance > Network Troubleshooting > Ethernet Capture
Interface Type: LAN1, el puerto de la troncal   Start
```
En Wireshark, Telephony > RTP > RTP Streams: dos flujos, uno por sentido, con cantidades parecidas.
3. Provocá la falla del caso, como queda cuando se suman remotos y nadie revisa la troncal:
```text
PBX Settings > SIP Settings > NAT
External Host: 192.0.2.10        Use IP address in SDP: Sí
Local Network Address: 192.168.88.0/24     (sin 198.51.100.0/30 ni 203.0.113.0/24)
```
4. Llamá otra vez de la 1001 a la 2001 y anotá el síntoma: la 2001 escucha a la 1001; la 1001 no escucha a la 2001. Es el caso: el de afuera oye a la oficina y la oficina no lo oye.
5. Diagnosticá en orden, con la captura en LAN1. Cada hipótesis tiene su prueba, de la más probable a la menos:
```text
H1  la UCM anuncia otra IP en c=           c= del INVITE o del 200 OK que sale por LAN1
H2  el audio de la UCM sale por otra boca  captura en LAN2: RTP hacia la red de Antel
H3  algo en el medio filtra o reescribe    c= sale bien y llega distinto, o no vuelve
H4  codec                                  Active Calls y la línea m= de cada lado
```
Filtrá `sip || sdp` y abrí el INVITE de tu UCM: `c=IN IP4 192.0.2.10`. Le está diciendo a "Antel" que mande el audio a la IP pública, que desde la red de Antel no existe. En RTP Streams queda un solo flujo, de 198.51.100.2 a 198.51.100.1; Ctrl+R lo marca como flujo sin vuelta. H1 confirmada: no hace falta seguir con H2.
6. Arreglá: sumá a Local Network Address la red de la troncal y las de Antel de la planilla, y aplicá los cambios:
```text
Local Network Address: 192.168.88.0/24
                       198.51.100.0/30
                       203.0.113.0/24
```
7. Verificá con la misma prueba que encontró la falla: nueva captura, `c=IN IP4 198.51.100.2` en el INVITE, dos flujos en RTP Streams y la 1001 escucha. En la ficha, qué se cambió, por qué y la captura de antes y de después (lo justo, después se borra).
8. La otra firma de la troncal, para reconocerla en obra: si en el SDP de Antel la línea `c=` trae una red que no está en Static Routes, la UCM manda su audio por la ruta por defecto (LAN2, el router del cliente) y el que no oye es el de afuera. Se ve capturando en LAN2 con `udp portrange 10000-20000`: el RTP hacia Antel sale por ahí. Arreglo: esa red a Static Routes (por LAN1) y a Local Network Address.

Firmas para la ficha, cuando no es la troncal:

| Causa | Qué se ve | Dónde |
| - | - | - |
| VLAN de voz y datos con firewall o ruta de vuelta distinta | un flujo sale y no vuelve, solo entre ciertas redes | RTP Streams en la UCM y en el router |
| Direct Media entre redes distintas | anda dentro de la misma red, falla entre sedes o VLAN | extensión, pestaña Media; Active Calls |
| SIP ALG del router | `c=` sale bien de la UCM y llega cambiado | dos capturas, una de cada lado (lección Audio de un lado) |
| Rango RTP distinto del reenviado | puertos del `m=` fuera de lo abierto en el router | PBX Settings > SIP Settings > RTP Settings |
| Teléfono que anuncia mal | `c=` o puerto raro en el SDP del teléfono | captura; firmware y STUN del teléfono |
| Codec | se arma la llamada y un lado queda mudo | `m=` de cada lado; probá solo PCMA y PCMU |

⚠️ En la central de un cliente, cambiar Local Network Address o External Host afecta a todos los internos remotos: hacelo fuera de hora y probá un remoto y la troncal antes de irte.

**Regla para quedarse**
Primero quién no oye a quién; el sentido que falta te dice si mirar la `c=` que anunció la central o el camino por donde sale su audio.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- External Host, Use IP address in SDP y Local Network Address en el UCM630x: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Por qué sin Local Network Address la IP externa queda mal: https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/
- RTP Streams de Wireshark y los flujos sin vuelta: https://www.wireshark.org/docs/wsug_html_chunked/ChTelRTP.html
- Causas de one-way audio en orden, con el ruteo asimétrico: https://www.pathsolutions.com/resources/what-causes-voip-one-way-audio
- Dos GXP2160 que no oían el audio interno: https://community.freepbx.org/t/one-way-audio-but-its-interoffice/91454
