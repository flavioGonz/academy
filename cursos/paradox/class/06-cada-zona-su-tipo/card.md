# Lección 6. Cada zona su tipo

**Escuchá:** cada-zona-su-tipo.mp3 (2 min)

**La idea, en tres líneas**
- En SP/MG cada zona es una sección de [001] a [032]: dos dígitos de definición, un dígito de partición (1, 2 o 3 para ambas) y opciones 1 a 8.
- 01 retardo de entrada para la puerta, 05 seguimiento para el sensor que cuida el teclado, 08 instantánea para el perímetro, 11 fuego, 16 robo 24 h. Fuego no se puede anular.
- Contra falsas alarmas: Intellizone (opción 6, espera 48 s de fábrica en [713]) y retardo de transmisión (opción 7, tiempo en [833]).

**Impacto:** el cliente entra, desarma y no suena; y cuando suena, es porque hay algo.

**Quién lo dice:** 1 de 1 fuente: la guía de instalación SP+. Evidencia fina, es la regla del fabricante; no se encontraron practicantes que la discutan.

**Laboratorio** · Foco · 20 min
Casa tipo en una central SP o MG de banco: 4 zonas, una partición.
1. Programá cada zona (definición, partición y opciones de fábrica 1, 2, 3 y 8 encendidas):
```text
[ENTER] + código de instalador + [001]
01 1 [ENTER]     zona 1: puerta principal, retardo de entrada 1, partición 1
05 1 [ENTER]     zona 2: PIR del living que ve el teclado, seguimiento
08 1 [ENTER]     zona 3: ventanas, instantánea
16 1 [ENTER]     zona 4: robo 24 h (tapa de caja de medidores)
[CLEAR]
```
(Cada ENTER guarda y avanza a la sección siguiente.)
2. Revisá los tiempos sin cambiarlos: desde la espera de sección, tecleá la sección y ENTER (modo visualización), y CLEAR para volver:
```text
[710]   retardo de entrada 1   (045 s de fábrica)
[745]   salida partición 1     (060 s de fábrica)
[747]   corte de sirena        (004 min de fábrica)
```
3. Armá y probá como el cliente: abrí la puerta y caminá frente al PIR. Tiene que haber retardo, no alarma.
4. Armá otra vez y activá primero el PIR, sin abrir la puerta: tiene que disparar al instante.
5. Si la obra tiene falsas alarmas en la entrada, activá en la zona 1 la opción 7 (retardo de transmisión) y cargá el tiempo en [833].

⚠️ Con la central conectada a monitoreo, avisá antes de cada prueba de disparo.

**Regla para quedarse**
El tipo de zona sale del recorrido de entrada, no de la costumbre.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Definiciones de zona, tiempos, Intellizone y retardo de transmisión (guía de instalación SP+): https://www.paradox.com/Downloader/?ID=11662
- Hojas de programación de zonas (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
