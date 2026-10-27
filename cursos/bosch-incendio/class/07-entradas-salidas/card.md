# Lección 7. Entradas y salidas

**Escuchá:** entradas-salidas.mp3 (2 min)

**La idea, en tres líneas**
- Pulsadores FMC-420, sirenas y balizas FNM-420 y FNX-425U (hasta 84 por lazo con detectores, 127 sin ellos), y módulos FLM: 420/4-CON (dos zonas convencionales), 430-I2M1, 430-I4R2, 420-NAC, 420-RLE-S (extinción).
- Cada entrada que puede dar alarma consume un punto: un FLM de ocho entradas puede sumar ocho para los límites del panel.
- En EN 54-2, silenciar o reponer avisadores es una acción manual; un temporizador de duración solo vale para señales que no son EN 54.

**Impacto:** el panel no se queda corto de puntos a mitad de obra y ninguna salida crítica queda sin identificar.

**Quién lo dice:** 2 de 2 fuentes coinciden (System manual y TI 2715); la IT-11 uruguaya de 2010 suma el criterio de pulsador a 30 m y uno por piso, siempre sujeto al proyecto.

**Laboratorio** · Foco · 15 min
Con el plano de una obra chica, completá el inventario:
```text
Dispositivo        | Modelo          | Cant. | Puntos | Mueve / avisa      | Cómo se aísla
Pulsador           | FMC-420RW       |       |        | alarma             | deshabilitar en panel
Sirena/baliza      | FNX-425U        |       |   0    | aviso              | deshabilitar salida
Módulo 2E/1S       | FLM-430-I2M1    |       |        | ej. retención puerta | deshabilitar salida
Módulo extinción   | FLM-420-RLE-S   |       |        | disparo de gas     | bloqueo en central de extinción
Zona convencional  | FLM-420/4-CON   |       |        | detectores viejos  | deshabilitar zona
Total de puntos:   ____
```
1. Contá un punto por cada entrada programada como alarma.
2. Marcá en rojo cada salida que mueve algo físico (gas, puertas, ascensores, ventilación).
3. Verificá que la versión de RPS de la oficina sea 5.15.28 o posterior si hay RLE-S en la obra.
⚠️ Con extinción por gas, cualquier prueba se coordina con la empresa de extinción y con la central bloqueada; el diseño lo fija el proyecto.

**Regla para quedarse**
Toda salida que mueve algo físico queda identificada, con su punto contado y con una forma documentada de aislarla.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Límites por módulo y puntos de detección (System manual): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
- RLE-S, FLM-430 y silenciado manual en EN 54-2 (TI 2715): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2715_2026_TI_AVENAR_FW-4.8.1__FSO-5000-RPS_5.15.27.pdf?collection=bosch-bt-lifesafetysystems
