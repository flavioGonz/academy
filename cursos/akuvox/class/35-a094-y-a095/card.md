# Lección 35. A094 y A095

**Escuchá:** a094-y-a095.mp3 (2 min)

**La idea, en tres líneas**
- Controladoras de 4 puertas para el tablero. A094: sin PoE, 100 a 240 VAC 1,5 A, 4 salidas de 12 V de 800 mA (compartidas con esa entrada); versión estándar y sin adaptador AC-DC. IP con IP Scanner.
- A095: PoE 802.3at o 12 V 5 A; 8 salidas de 12 V: 500 mA con fuente; con PoE+, 0,2 A por salida con 8 lectores o 0,2 a 0,4 A con 4 o menos. PIN y tarjetas 13,56 y 125 kHz; IP anunciada con Reset.
- Relé 30 V 2 A en las dos. El A094 no se integra con el ascensor EC33; el A095 sí.

**Impacto:** la controladora se elige por el presupuesto de energía de lectores y cerraduras, no por el precio.

**Quién lo dice:** 8 de 11 fuentes de control de acceso coinciden en el reparto terminal, controladora, relé de borde y ascensor; la tabla de 12 V es la única con el detalle por salida. Sin ficha propia leída de A094 ni A095.

**Laboratorio** · Admin · 15 min
1. Para una obra de 4 puertas, listá cargas por salida:
```text
Puerta  Lector (mA)  Cerradura (mA)  Total
1       ____         ____            ____
2       ____         ____            ____
3       ____         ____            ____
4       ____         ____            ____
```
2. Compará con los límites:
```text
A094            4 salidas x 800 mA, entrada 100-240 VAC 1,5 A
A095 con fuente 8 salidas x 500 mA (fuente 12 V 5 A)
A095 con PoE+   8 lectores: 0,2 A por salida; 4 o menos: 0,2 a 0,4 A
```
3. Si alguna puerta supera el límite, la cerradura va con fuente propia.
4. Si hay ascensor con EC33 en la obra, descartá el A094 para esa integración.
⚠️ El A094 trabaja con 220 V en el gabinete: lo instala alguien habilitado para baja tensión de red.

**Regla para quedarse**
La controladora se elige por energía disponible por salida, y lo que no entra va con fuente propia.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Salidas de 12 V de A094 y A095: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Alimentación por modelo: https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Equipos que no se integran con el EC33: https://knowledge.akuvox.com/docs/configure-lift-control-1
