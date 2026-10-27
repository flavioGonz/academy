# Lección 39. Accesorios y módulos

**Escuchá:** accesorios-y-modulos.mp3 (2 min)

**La idea, en tres líneas**
- Accesorios por modelo, según su ficha: X915 con caja de embutir, caja de superficie (normal y gruesa), cubiertas de lluvia y kit de ángulo; R29 con cubiertas de lluvia (negro y plata) y soportes de pared y embutir, uno propio para el R29C-L.
- Módulos: SR01 relé de seguridad (30 V 2 A); MK485 y RSAC-C1-R8 para el monitor; lectores ACR-CRP12 (UHF), ACR-CID12 y ACR-CID01 (escritorio), tarjeta UHF-TAG11, Bkey (tarjeta Bluetooth); KF01 a KF03 sin descripción en lo leído.
- Cerradura desde el portero: NC entre masa y NC con salida `Always`; NO entre masa y NO con `Triggered by Open Relay`. Fuente recomendada por modelo en la tabla de alimentación.

**Impacto:** el portero se instala el día previsto, con su caja, su cubierta y su fuente, sin segunda visita.

**Quién lo dice:** 2 de 7 fuentes coinciden en pedir el accesorio del modelo exacto (fichas de R29 y X915, guía de relés externos); la tabla de 12 V es la que fija el cableado de cerraduras.

**Laboratorio** · Admin · 15 min
1. Elegí un portero con ficha (X915 o R29) y armá el pedido:
```text
Frente        : versión exacta (ej. R29C)
Montaje       : caja/soporte de embutir o de superficie del modelo
Cubierta      : de lluvia, embutir o superficie, color
Alimentación  : PoE (tipo) o fuente recomendada en la tabla
Cerradura     : desde el portero (si su salida alcanza) o fuente propia
Módulos       : SR01 / lector / Bkey si corresponde
```
2. Cableado de la cerradura si sale del portero:
```text
Cerradura NC (abre al cortar)  -> GND + NC, salida 12 V en "Always"
Cerradura NO (abre al dar 12 V) -> GND + NO, salida 12 V en "Triggered by Open Relay"
```
3. Verificá cada línea contra la ficha o la tabla; lo que no esté, "a confirmar".
⚠️ La salida de 12 V tiene límite por modelo (lecciones 20 a 29): si la cerradura pide más, fuente propia.

**Regla para quedarse**
El pedido sale de la ficha del modelo exacto, con caja, cubierta, fuente y módulos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Accesorios del X915: https://www.akuvox.com/productsDisp?pid=37
- Accesorios del R29: https://www.akuvox.com/productsDisp?pid=17
- Cableado de cerraduras con la salida de 12 V: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
