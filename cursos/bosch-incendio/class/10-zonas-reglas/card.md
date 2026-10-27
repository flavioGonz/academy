# Lección 10. Zonas y reglas

**Escuchá:** zonas-reglas.mp3 (2 min)

**La idea, en tres líneas**
- Cada elemento tiene dirección física (lugar en el lazo) y lógica (grupo y subdirección); el panel muestra la lógica en cada mensaje y las integraciones la heredan.
- Desde la cuenta 4.5: puntos de alarma (definen si hace falta redundancia) y puntos lógicos (4096 en panel solo, 2048 por panel en red).
- La matriz de causa y efecto se programa con reglas por evento, reglas dependientes de estado, contadores y estados compuestos; RPS puede no avisar si una tecla de función y un grupo de entradas comparten dirección.

**Impacto:** el guardia, el BMS y el técnico de mantenimiento leen el mismo nombre para el mismo lugar.

**Quién lo dice:** 3 de 3 fuentes coinciden (System manual, TI 2715 y documentación de integración HSYCO para FPA-5000); sin discrepancias.

**Laboratorio** · Foco · 20 min
1. Escribí en papel la matriz de un piso de oficinas:
```text
CAUSA \ EFECTO          | Sirenas piso | Retención puertas | Ventilación | Transmisión monitoreo
Detector grupo 3 (1 eq.) |              |                   |             |
Detector grupo 3 (2 eq.) |              |                   |             |
Pulsador piso 3          |              |                   |             |
Flujo rociadores piso 3  |              |                   |             |
```
2. Marcá cada cruce con: activa / no activa / solo en modo noche.
3. Asigná direcciones lógicas sin repetir:
```text
Grupo 3, sub 1 a 20: detectores piso 3
Grupo 30, sub 1 a 4: pulsadores piso 3
Grupo 300: entradas técnicas (flujo, presión)
Teclas de función: grupo propio, distinto de cualquier grupo de entradas
```
4. Traducí cada cruce a una regla (por evento o por estado) y anotá su nombre.
⚠️ La matriz de causa y efecto es parte del proyecto: la define y firma el técnico responsable, no se inventa en obra.

**Regla para quedarse**
Primero la matriz en papel y firmada; después las reglas en RPS, con direcciones lógicas únicas.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Reglas, puntos de alarma y puntos lógicos (TI 2715): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2715_2026_TI_AVENAR_FW-4.8.1__FSO-5000-RPS_5.15.27.pdf?collection=bosch-bt-lifesafetysystems
- Cómo ve los eventos una integración externa: https://docs.hsyco.com/docs/io-servers/boschfpa
- Zonas lógicas y límites (System manual): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
