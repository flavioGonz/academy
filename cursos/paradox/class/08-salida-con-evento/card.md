# Lección 8. Salida con evento

**Escuchá:** salida-con-evento.mp3 (2 min)

**La idea, en tres líneas**
- Cada PGM tiene evento de activación ([220], [222]...) y de desactivación ([221], [223]...), cada uno con grupo, subgrupo y partición (01, 02 o 99 para ambas); o un tiempo en [281] a [296] (5 s de fábrica).
- Las PGM de la placa son de baja corriente (100 a 150 mA según la guía): para portones, luces o sirenas extra, siempre relé externo.
- De fábrica, PGM1 se activa con el botón B de cualquier control (08/99/99) y PGM2 con el C. El evento de falla de AC espera el retardo de [839] (15 min de fábrica).

**Impacto:** el portón abre con un pulso limpio, la luz de falla dice la verdad y no se quema ninguna salida.

**Quién lo dice:** 2 de 2 fuentes coinciden (guías de instalación y programación SP+). Evidencia fina del fabricante; no se encontró quien discrepe.

**Laboratorio** · Campo · 20 min
Material: central SP+ de banco, dos relés de 12 V con bobina por debajo de 100 mA, un LED con su resistencia o una lámpara de 12 V en el contacto del relé.
1. Portón (PGM1): conectá la bobina del relé a la PGM1 y el contacto seco a la entrada de pulsador de la placa del portón. Dejá el evento de fábrica y poné un pulso de 2 s:
```text
[ENTER] + código de instalador + [281]
002              PGM1: 2 s, base en segundos ([261] opción 1 apagada)
```
Sin control remoto en el banco, usá la tecla de utilidad 1 (teclas 1 y 2 juntas, partición 1):
```text
[CLEAR] [220]  06 08 01      activación: grupo 06, subgrupo 08, partición 1
```
2. Luz de falla de AC (PGM2), que se apaga sola al volver la red:
```text
[CLEAR] [222]  44 01 99      activación: nueva falla, falla de AC, ambas particiones
[CLEAR] [223]  45 01 99      desactivación: falla restaurada, AC restaurada
[CLEAR] [282]  000           sin tiempo: sigue al evento de desactivación
```
3. Para probar en el banco, bajá temporalmente el retardo de reporte de AC:
```text
[CLEAR] [839]  001           1 minuto (de fábrica: 015)
```
4. Cortá la red, esperá un minuto, mirá la luz; reconectá y mirá que se apague.
5. Devolvé [839] al valor acordado con la empresa de monitoreo.

⚠️ Un portón que abre por la alarma es un riesgo físico: probalo con el motor desconectado y avisale al cliente cómo se activa.

**Regla para quedarse**
La PGM manda, el relé carga.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Conexión de PGM, eventos, temporizador y opciones (guía de instalación SP+): https://www.paradox.com/Downloader/?ID=11662
- Tabla de eventos y valores de fábrica de PGM1 y PGM2 (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
