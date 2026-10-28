# Lección 16. Identificador y audio

**Escuchá:** identificador-y-audio.mp3 (2 min)

**La idea, en tres líneas**
- Sin la facilidad de Antel "Identificación de número llamante" no llega número; si está contratada, lo que falta es acertar el Caller ID Scheme.
- Ninguna fuente dice qué esquema usa Antel: se prueba Auto-Detect y, si no, uno por uno (Bellcore, ETSI-FSK, ETSI-DTMF y sus variantes antes del timbre), comparando con un teléfono con pantalla.
- Eco, ruido o volumen bajo: primero impedancia (ACIM en Analog Hardware), después ganancias RX y TX (-13,5 a +12 dB).

**Impacto:** el cliente ve quién llama en todos los teléfonos y la línea analógica suena como una SIP, sin eco ni volumen bajo.

**Quién lo dice:** 5 de 6 fuentes coinciden en confirmar el servicio y probar esquemas (Antel, manual del UCM630x, Wikipedia, AudioCodes, Yeastar); ninguna confirma el esquema de Antel y Wikipedia no lista a Uruguay.

**Laboratorio** · Foco · 20 min
1. Confirmá el servicio: con un teléfono con pantalla en el par, llamá desde un celular. Si no muestra el número, la línea no tiene la facilidad: se pide a Antel.
2. En la troncal probá la detección automática:
```text
Extension/Trunk > Analog Trunks > Antel_Linea1
Use CallerID: Yes
Caller ID Scheme: Auto-Detect
```
3. Llamá desde el celular, dejá sonar al menos dos timbres y mirá el número en CDR > CDR y en el teléfono que atiende.
4. Si no aparece, probá de a uno y anotá cuál funciona:
```text
Bellcore/Telcordia
ETSI-FSK During Ringing
ETSI-DTMF During Ringing
ETSI-FSK Prior to Ringing with LR    (y las variantes DTAS y RP)
ETSI-DTMF Prior to Ringing with LR
```
5. Con la línea libre, detectá la impedancia:
```text
PBX Settings > Interface Settings > Analog Hardware > FXO (opciones)
Detect (ERL o Pr) > Update
```
6. Hacé una llamada real y ajustá de a poco: RX Gain si vos escuchás bajo, TX Gain si al otro lado te escuchan bajo.
7. Si queda eco o zumbido, probá en la troncal Echo Cancellation Mode y el filtro de baja frecuencia (Noise Cancellation RX Frequency: 60 Hz deja pasar solo lo que está por encima).
8. Si la línea lleva un fax: Fax Detection en No en la troncal y la ruta entrante directo a la extensión del fax.

**Regla para quedarse**
El esquema de identificador que funciona se anota en la ficha de la línea, junto con la tensión y los tonos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Identificación de número llamante de Antel: https://antel.com.uy/personas/servicios/telefonia-fija/identificacion-de-numero-llamante
- Estándares de identificador y tabla de países: https://en.wikipedia.org/wiki/Caller_ID
- Cómo depurar el identificador en un FXO: https://techdocs.audiocodes.com/multi-service-business-routers/mediant-500-msbr/user-manual/version-720/Content/UM/Debugging%20a%20Caller%20ID%20Detection%20on%20FXO.htm
