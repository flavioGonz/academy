# Lección 15. Tonos y corte

**Escuchá:** tonos-y-corte.mp3 (2 min)

**La idea, en tres líneas**
- En analógico el corte se adivina: tono de ocupado, inversión de polaridad o corte de corriente. Antel no publica cuál usa; se mide con PSTN Detection.
- Según la lista de tonos de la UIT, en Uruguay todo es 425 Hz: ocupado 0,5 s y 0,5 s, llamada 1 s y 4 s, invitación a marcar continuo. Lo que distingue un tono de otro es la cadencia.
- La UCM viene con tonos de Estados Unidos (480 y 620 Hz): con eso no detecta el ocupado de acá.

**Impacto:** llamadas que se cortan cuando cuelga el otro, líneas que no quedan tomadas y buzones sin dos minutos de tono grabado.

**Quién lo dice:** 5 de 7 fuentes coinciden en los tres métodos de corte y en medirlo (Grandstream, Yeastar, Wikipedia, innovaphone); un caso de Asterisk muestra la detección de ocupado cortando salientes buenas y otro detectó mejor sin patrón fijo.

**Laboratorio** · Foco · 20 min
1. Abrí la troncal y cargá los tonos. Si Uruguay no está en la lista, usá Custom con los valores de la UIT (el nivel @-50 es el mismo que usa el valor de fábrica):
```text
Extension/Trunk > Analog Trunks > Antel_Linea1 > Tone Settings
Tone Country: Custom
Busy Tone:       f1=425@-50,c=500/500
Congestion Tone: f1=425@-50,c=250/250
Busy Detection: Yes      Busy Tone Count: 4
```
2. Corré la detección con la línea libre. Con una sola línea:
```text
Tone Settings > Detect
Detect Model: Semi-auto Detect
Source Channel: FXO1
Destination Number: (tu celular)
```
Atendé y cortá cuando la web te lo pida. Con dos líneas podés usar Auto Detect, con Destination Channel FXO2 y el número real de la línea 2.
3. Revisá lo que encontró (Busy Tone, Polarity Reversal, Current Disconnect) y guardá. Activá Enable Polarity Reversal solo si la detección la encontró.
4. Probá el corte: llamá desde el celular a una interna, atendé, cortá desde el celular y contá cuántos segundos tarda el FXO1 en volver a libre en el Dashboard. Repetí con una llamada saliente.
5. Si no corta, grabá la línea y medí el tono:
```text
Maintenance > Signaling Troubleshooting > Analog Record Trace
Puerto: FXO1   Start  (llamada, cortá desde el celular, esperá 10 s)   Stop  Download
Audacity > File > Import > Raw Data: Signed 16-bit PCM, 1 canal (Mono), 8000 Hz
```
Medí cuánto dura cada tono y cada silencio, y su frecuencia en Analyze > Plot Spectrum (menús de Audacity en inglés).
⚠️ PSTN Detection ocupa la línea alrededor de un minuto: hacela fuera del horario de atención.

**Regla para quedarse**
Los tonos de la línea se cargan o se miden, nunca se dejan en Estados Unidos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Tonos nacionales de la UIT, Uruguay incluido: https://www.itu.int/dms_pub/itu-t/opb/sp/T-SP-E.180-2010-PDF-S.pdf
- PSTN Detection y medición con Audacity: https://documentation.grandstream.com/knowledge-base/manage-analog-lines/
- Busy detection que corta de más: https://community.asterisk.org/t/asterisk-hangsup-when-busydetect-yes/44836
