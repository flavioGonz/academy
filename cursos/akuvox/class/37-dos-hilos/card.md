# Lección 37. Dos hilos

**Escuchá:** dos-hilos.mp3 (2 min)

**La idea, en tres líneas**
- Línea para reformar edificios sobre el cableado existente: porteros R20K-2, R20A-2 y E12S-2; monitores S562W-2 y C313W-2; equipos NS-2, NC-2 y NX-2; y un kit de video portero IP de 2 hilos.
- Sin PoE en los porteros: R20A-2 y R20K-2 a 48 V DC 1,25 A. El C313-2 se alimenta desde el NS-2 (o 48 V sin NS-2). Relé 30 V 2 A en R20-2 y C313-2; el C313W-2 tiene RS485, relé, timbre y un RJ45, sin PoE.
- Credenciales: R20A-2 tarjetas 13,56 y 125 kHz sin PIN; R20K-2 PIN y tarjetas. El rol exacto de NC-2 y NX-2 no está en lo leído.

**Impacto:** un edificio sin UTP pasa a video portero IP sin recablear, con las fuentes de 48 V previstas desde la cotización.

**Quién lo dice:** 2 de 11 fuentes de esta parte tocan los 2 hilos (menú de productos y tabla de alimentación); evidencia escasa y sin fichas propias leídas.

**Laboratorio** · Admin · 10 min
1. En un edificio con portero viejo de 2 hilos, relevá:
```text
Apartamentos          : ____
Par disponible hasta  : portero ___  / cada apartamento ___
Accesos (portones)    : ____
```
2. Armá la lista preliminar:
```text
Porteros  : R20A-2 (tarjeta) o R20K-2 (PIN y tarjeta), 48 V DC 1,25 A cada uno
Monitores : C313W-2 o S562W-2, alimentados desde NS-2 o con 48 V
Red       : NS-2 / NC-2 / NX-2 (rol y cantidades a confirmar con el distribuidor)
```
3. Marcá en rojo todo lo que no sale de una página leída y pedilo por escrito antes de cotizar.
⚠️ Antes de reutilizar el par existente, medí aislación y continuidad: un par en mal estado no lo arregla ningún equipo.

**Regla para quedarse**
En 2 hilos, la fuente de 48 V y el rol de cada equipo de red se confirman antes de cotizar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Menú de productos con la línea de 2 hilos: https://www.akuvox.com/products
- Alimentación de los equipos de 2 hilos: https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Interfaces del C313W-2: https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors
