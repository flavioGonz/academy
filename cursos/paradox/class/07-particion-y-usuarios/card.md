# Lección 7. Partición y usuarios

**Escuchá:** particion-y-usuarios.mp3 (2 min)

**La idea, en tres líneas**
- Particionado en [700] opción 1 (SP+: dos particiones; EVOHD+: ocho). El tercer dígito de cada zona la asigna: 1, 2 o 3 (ambas). Si se apaga el particionado, las zonas de la partición 2 dejan de funcionar.
- Usuarios: maestro del sistema, un maestro por partición y 29 usuarios. Opciones en [404] a [432]: 1 y 2 particiones, 3 anular, 4 Stay/Sleep, 5 forzado, 6 solo armar, 7 solo PGM, 8 coacción.
- Largo de código 4 o 6 dígitos en [701] opción 1. Al pasar a 6, la central completa con los dos primeros dígitos (1234 pasa a 123412).

**Impacto:** cada persona arma y desarma solo lo suyo, y nadie queda con un código que dejó de andar.

**Quién lo dice:** 1 de 1 fuente: la guía de instalación SP+. Evidencia fina del fabricante; no se encontró quien discrepe.

**Laboratorio** · Foco · 15 min
Casa con taller en una central SP+ de banco.
1. Activá el particionado:
```text
[ENTER] + código de instalador + [700]
[1]  [ENTER]        opción 1: particionado encendido
```
2. Pasá las zonas del taller a la partición 2 (CLEAR vuelve a la espera de sección, con ARM y STAY titilando):
```text
[CLEAR] [005]
       01 2 [ENTER]  zona 5: puerta del taller, retardo, partición 2
       08 2 [ENTER]  zona 6: ventana del taller, instantánea, partición 2
```
3. Usuario 005, empleado del taller: solo partición 2, sin anular, sin Stay, sin forzado. De fábrica vienen encendidas la 1, 3, 4 y 5; SLEEP las apaga todas:
```text
[CLEAR] [405]  [SLEEP]  [2]  [ENTER]    queda encendida solo la opción 2
```
4. Revisá con ENTER (visualización) los tiempos por partición: salida [745] y [746], corte de sirena [747] y [748].
5. Pedí al "maestro" que cargue el código del usuario 005 desde su menú o desde BabyWare, y probá: ese código arma y desarma el taller, y no la casa.
6. Decidí el largo de código ([701] opción 1) antes de cargar usuarios, y no lo cambies después.

⚠️ Con la central en servicio, cambiar el particionado o el largo de código afecta a todos los usuarios: coordinalo con el cliente y con monitoreo.

**Regla para quedarse**
Cada usuario con la partición y las opciones mínimas que necesita.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Particionado, códigos de acceso, opciones de usuario y largo de código (guía de instalación SP+): https://www.paradox.com/Downloader/?ID=11662
- Hojas de programación de usuarios y particiones (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
