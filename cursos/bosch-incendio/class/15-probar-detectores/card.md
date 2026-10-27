# Lección 15. Probar detectores

**Escuchá:** probar-detectores.mp3 (2 min)

**La idea, en tres líneas**
- La zona se pasa a modo revisión (walk test) antes de probar: el detector evalúa la evolución de la señal y en revisión se prepara para la prueba. El cabezal queda arriba hasta que dispare: hasta 10 s con aerosol, hasta 20 s en multisensores.
- Multisensores: walk test secuencial (aerosol, calor, gas de CO de 0,5 a 1 s) o simultáneo con herramienta multiestímulo tipo Testifire; en simultáneo, si no aparece alarma, un sensor falla.
- Con dependencia de dos detectores se prueba fuera de revisión: el óptico puede tardar hasta 1 min, con aerosol en ráfagas. El lazo se lee con la herramienta FME-420-LSN-TTL, actualizada en 2026.

**Impacto:** pruebas que encuentran sensores fallados en vez de declararlos buenos por apuro.

**Quién lo dice:** 2 de 2 fuentes coinciden (guía de operación AVENAR detector 4000 y TI 2706 de la herramienta de lazo); sin discrepancias. El autotest remoto de Bosch complementa, no reemplaza, lo que pida el proyecto.

**Laboratorio** · Campo · 20 min
Material: panel de banco, un FAP-425-O-R y un FAP-425-OT-R (o DOT-R), aerosol de prueba, herramienta de calor.
1. Avisá y aislá como en la lección 14 (aunque sea banco, practicá el hábito).
2. Pasá la zona a modo revisión.
3. Óptico: aerosol con el cabezal, contá segundos hasta la alarma.
4. Multisensor, walk test secuencial: aerosol y después calor, anotá cada tiempo.
5. Completá:
```text
Dirección | Modelo        | Modo prueba  | Sensor  | Segundos | Resultado | Hora
3.1       | FAP-425-O-R   | revisión     | óptico  |          |           |
3.2       | FAP-425-OT-R  | secuencial   | óptico  |          |           |
3.2       | FAP-425-OT-R  | secuencial   | térmico |          |           |
```
6. Sacá la zona de revisión y verificá el panel en reposo.
⚠️ En un edificio real, el modo revisión y las salidas deshabilitadas se cierran antes de irte: un detector que queda en revisión no da alarma de fuego normal.

**Regla para quedarse**
Cada detector probado queda con método, segundos, resultado y hora.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Instrucciones de prueba y walk test de los FAP-425 (guía de operación): https://armosystems.ru/upload/iblock/a58/a58a375f59a20cf60064da272d2b6fd9.pdf
- Actualización de la herramienta de prueba de lazo LSN (TI 2706): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2706_2026_TI_EN_FW-Update_LSN-Test_Tool.pdf?collection=bosch-bt-lifesafetysystems
- Autotest remoto de detectores con NEXOSPACE: https://www.boschbuildingtechnologies.com/lifesafetysystems/en/products/remote-monitoring-fire-alarm-systems/
