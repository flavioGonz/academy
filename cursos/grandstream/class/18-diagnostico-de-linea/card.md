# Lección 18. Diagnóstico de línea

**Escuchá:** diagnostico-de-linea.mp3 (2 min)

**La idea, en tres líneas**
- Caso real (sin nombres): FXO2 que no recibe y, al otro día, se ocupa y se libera cada unos 10 segundos; en Active Calls, una llamada por la línea 2 con destino `s` y otra por la línea 1 con número "Undetected".
- Método de la ficha a la configuración: medir el par, teléfono de prueba, desconectar lo que está en paralelo, cambiar el par de puerto, revisar ruta y detección, grabar.
- Cambiar el par de puerto separa línea de central: si la falla sigue a la línea, se reclama a Antel con datos; si se queda en el puerto, es la UCM.

**Impacto:** una visita con evidencia en lugar de tres a prueba y error, y un reclamo a Antel que no vuelve con "la línea está bien".

**Quién lo dice:** 6 de 8 fuentes respaldan alguna pieza del método (Grandstream con Analog Record Trace y syslog, Asterisk con el FXO en uso por tensión, FreePBX con las llamadas fantasma, AudioCodes con el teléfono de prueba, Sandman con la alarma en paralelo); ninguna describe este caso, así que la causa queda como hipótesis hasta medir.

**Laboratorio** · Campo · 25 min
En el banco con una línea real o la línea simulada con el FXS de un ATA. Las capturas de esta lección están editadas: los números reales se reemplazaron por Antel_Linea1 y Antel_Linea2.
1. Sacá la foto del estado antes de tocar nada:
```text
System Status > Dashboard      (color de cada FXO y estado de cada troncal)
System Status > Active Calls   (canal, troncal, destino, número)
CDR > CDR                      (hora, número y duración de las últimas entrantes)
```
2. Desconectá el FXO2 y medí el par en reposo y descolgado con el teléfono de prueba; compará con la ficha de la línea.
3. Con el teléfono de prueba: tono, llamada desde un celular, timbre. Descolgá y escuchá si el tono es el normal: con la transferencia de Antel activa se escucha uno distinto.
4. Desconectá todo lo que cuelga del par (alarma, posnet, fax, teléfonos) y repetí la prueba.
5. Cambiá los pares: la línea 2 al FXO1 y la línea 1 al FXO2. Anotá si la falla sigue a la línea o se queda en el puerto. Después volvé cada par a su puerto.
6. Revisá la configuración de la troncal de esa línea:
```text
Extension/Trunk > Inbound Routes      (ruta de Antel_Linea2, patrón _. y destino)
Extension/Trunk > Analog Trunks > Antel_Linea2
Ring Timeout: 8000   Tone Settings   Enable Polarity Reversal
```
7. Grabá dos o tres ciclos de la falla y levantá el log analógico:
```text
Maintenance > Signaling Troubleshooting > Analog Record Trace   Puerto: FXO2
Maintenance > Syslog   módulo chan_dahdi: NOTICE y VERBOSE (después volvé a error)
```
8. Si la falla sigue a la línea, reclamá a Antel con los datos:
```text
Reclamos telefonía fija: 121 (o *121 desde un móvil Antel), todos los días 24 horas
Empresas, atención técnica: 0800 2599
Datos: número de la línea, síntoma, desde cuándo, horarios, tensión medida,
resultado con teléfono de prueba y que la falla siguió a la línea al cambiar de puerto.
```
⚠️ Una grabación de la línea contiene conversaciones reales del cliente: guardala solo mientras dure el diagnóstico.

**Regla para quedarse**
Antes de culpar a la central o a Antel, cambiá el par de puerto: la falla dice sola de qué lado está.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- FXO en uso porque no ve la tensión de la línea: https://community.asterisk.org/t/functioning-pstn-line-with-red-alarm/65892
- Llamadas fantasma por inversión de polaridad: https://community.freepbx.org/t/polarity-switch-causing-false-call-backs/35199
- Números de atención y reclamos de Antel: https://antel.com.uy/atencion-telefonica
