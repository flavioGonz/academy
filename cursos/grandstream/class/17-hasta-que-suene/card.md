# Lección 17. Hasta que suene

**Escuchá:** hasta-que-suene.mp3 (2 min)

**La idea, en tres líneas**
- Por una línea analógica no llega número llamado: la llamada entra a la extensión `s` y la ruta entrante se elige por troncal, con un patrón que acepte todo (`_.`) y un destino.
- El destino es lo que ya está armado: el grupo 6000, el IVR 7000 con horario o la extensión del fax. Si en Active Calls la llamada queda en `s`, lo más probable es que no haya encontrado destino.
- La salida por varias líneas va con los patrones de Uruguay y failover; el que recibe ve el número de la línea por la que salió, porque Outbound Route CID no aplica a analógicas.

**Impacto:** cada línea de Antel termina sonando donde el cliente espera, con salida por la línea libre y sin sorpresas con el número que se muestra.

**Quién lo dice:** 4 de 4 fuentes coinciden en que en analógico no hay DID y la ruta va por troncal (documentación de Asterisk, comunidad de Asterisk, guía de líneas analógicas y manual del UCM630x); en la salida, 3 de 3 coinciden en orden de puertos, failover y número de la línea.

**Laboratorio** · Foco · 25 min
Usa el grupo 6000 de la lección Grupo o cola y el IVR 7000 de IVR con horario.
1. Ruta entrante de la línea 1:
```text
Extension/Trunk > Inbound Routes > Add
Trunks: Antel_Linea1
Pattern: _.
Default Destination: IVR 7000
Time Condition: Office Time -> IVR 7000 | fuera de horario -> Ring Group 6000
```
2. Ruta entrante de la línea 2 (en el ejemplo, la del fax):
```text
Trunks: Antel_Linea2   Pattern: _.   Default Destination: Extension (la del fax)
```
3. Llamá a cada línea desde un celular. Durante la llamada, mirá System Status > Active Calls: el destino tiene que ser el IVR, el grupo o la extensión, nunca `s`.
4. Ruta saliente por las líneas, con los números de Uruguay:
```text
Extension/Trunk > Outbound Routes > Add
Calling Rule Name: Uruguay_Antel
Pattern:
_2XXXXXXX
_4XXXXXXX
_09XXXXXXX
_911
Privilege Level: National
Use Trunk: Antel_Linea1    Failover Trunk: Antel_Linea2
```
Si preferís que marquen un prefijo para tomar línea, usá `_9X.` con Strip 1, como el ejemplo de Grandstream.
5. Llamá a tu celular desde una interna y mirá qué número aparece: es el de la línea 1.
6. Desconectá el cable del FXO1 y repetí. Si sale por la línea 2, con su número, el failover anda; si no sale, la alternativa es una troncal con las dos FXO (Antel_Grupo, Ascend), que toma la libre. Volvé a conectar.
⚠️ El 911 no se usa para pruebas: el patrón queda cargado y la ruta se prueba con un celular.

**Regla para quedarse**
Toda troncal analógica tiene su ruta entrante con destino, y ninguna llamada de prueba se da por buena si en Active Calls quedó en `s`.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- La extensión s de Asterisk: https://docs.asterisk.org/Configuration/Dialplan/Special-Dialplan-Extensions/
- Rutas para líneas analógicas en la UCM: https://documentation.grandstream.com/knowledge-base/manage-analog-lines/
- Numeración de Uruguay: https://en.wikipedia.org/wiki/Telephone_numbers_in_Uruguay
