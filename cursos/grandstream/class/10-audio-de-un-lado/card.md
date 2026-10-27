# Lección 10. Audio de un lado

**Escuchá:** audio-de-un-lado.mp3 (2 min)

**La idea, en tres líneas**
- Orden de diagnóstico: NAT y puertos (External Host, Local Network Address, 5060 y 10000 a 20000), después SIP ALG, después captura.
- Corte fijo entre 30 y 35 segundos: casi siempre un ACK perdido por reescritura en el camino (Timer H, 64 × 500 ms).
- La captura en la UCM (Ethernet Capture) muestra en la línea `c=` del SDP a dónde se manda el audio.

**Impacto:** los tickets de audio unidireccional se cierran con evidencia y sin tocar routers a ciegas.

**Quién lo dice:** 6 de 7 fuentes ponen NAT y puertos primero; 5 de 5 dicen apagar SIP ALG; Plexatalk y SureVoIP admiten casos raros donde ayuda, y el caso de 3CX muestra que a veces el problema está del lado del servidor.

**Laboratorio** · Campo · 20 min
1. Iniciá la captura en la UCM:
```text
Maintenance > Network Troubleshooting > Ethernet Capture
Interfaz: la de los teléfonos   Start
```
2. Hacé una llamada de 20 segundos entre una interna y el troncal o una interna remota. Detené la captura y descargá el archivo.
3. En Wireshark filtrá la señalización y mirá el SDP:
```text
sip || sdp
```
En el INVITE y en el 200 OK buscá:
```text
c=IN IP4 203.0.113.10      <- correcto hacia afuera
c=IN IP4 192.168.88.20     <- IP privada hacia afuera: falta External Host o lo reescribió un ALG
m=audio 10044 RTP/AVP 8 0  <- puerto RTP dentro de 10000 a 20000
```
4. Verificá el audio real: Telephony > RTP > RTP Streams. Si hay un solo sentido, comprobá a qué IP y puerto va el que falta.
5. Si sospechás ALG: apagalo, reiniciá el router y repetí la captura.
⚠️ Una captura contiene números y audio de llamadas reales: guardala solo el tiempo necesario y no la compartas fuera del soporte.

**Regla para quedarse**
No se toca un router sin una captura antes.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- SIP ALG explicado, síntomas y cómo probarlo: https://didlogic.com/learn/sip-alg-explained/
- Por qué conviene apagarlo y cuándo no: https://www.plexatalk.co.uk/?p=17613
- Caso real de audio de un lado con GXP: https://www.3cx.com/community/threads/grandstream-phone-receiver-cant-hear-me.116955/
