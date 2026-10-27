# Lección 22. X916 y X915

**Escuchá:** x916-y-x915.mp3 (2 min)

**La idea, en tres líneas**
- Android con frente de acero y apps de terceros: X916 de 13" con cámara Starlight (versiones estándar y LTE) y el relé más fuerte de la línea, 30 V 5 A; X915 de 8" (estándar, HID iClass, HID Prox y X915P con palma), relé 30 V 3 A.
- Protección: la guía de selección dice IP65 para X916 y X915; la ficha del X915 V2.0 dice IP66 e IK10. Vale la ficha de la versión que se compra.
- Alimentación: PoE+ en ambos; X916 también 12 V 4 A o 24 V 2 A, X915 24 V 2 A. La salida de 12 V (X916 500 mA, X915 1 A) pide fuente de 24 V 2,5 A, salvo X915 V2 con hardware 2915.1.0.8 a 2915.1.0.13 y firmware 2915.30.10.228 o más.

**Impacto:** el grado IP e IK que va en el pliego y la fuente que se lleva a obra salen de la página correcta.

**Quién lo dice:** 3 de 10 fuentes del catálogo coinciden en confirmar IP e IK en la ficha de la versión (guía de selección, fichas de X915 y R29); la guía de selección discrepa con la ficha del X915 (IP65 contra IP66 e IK10).

**Laboratorio** · Foco · 15 min
1. IP del X915: `9999` + Dial, `3888` + OK, `System Info`, `Network`.
2. Web, `Status > Basic > Product Information`: anotá versión de hardware (el X915 tiene dos) y firmware (`915.` en la primera generación; los de la V2 aparecen como `2915.` en las tablas de Akuvox).
3. Buscá en la ficha de esa versión el grado IP e IK y copialo a la planilla con la fuente: "ficha X915 V2.0".
4. Decidí la alimentación:
```text
¿Cerradura desde el portero?  no -> PoE+ 802.3at
                               sí -> fuente 24 V 2,5 A o más
                                     (excepción X915 V2: hw 2915.1.0.8 a .13 y fw >= 2915.30.10.228 -> también con PoE)
```
⚠️ Con dos datos distintos de protección, en una propuesta se cita la ficha de la versión, no la guía general.

**Regla para quedarse**
El grado IP e IK sale de la ficha de la versión exacta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ficha del X915 (IP66 e IK10, versiones HID y palma): https://www.akuvox.com/productsDisp?pid=37
- Guía de selección de porteros (IP65): https://www.akuvox.com/productSelectionGuide?cid=3
- Carga del relé por modelo: https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors
