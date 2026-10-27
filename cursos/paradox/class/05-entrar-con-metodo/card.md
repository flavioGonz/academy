# Lección 5. Entrar con método

**Escuchá:** entrar-con-metodo.mp3 (2 min)

**La idea, en tres líneas**
- SP/MG: ENTER, código de instalador, sección de tres dígitos y dato; el dato puede ser decimal (000 a 255), hexadecimal (la tecla 0 vale A) o por opciones 1 a 8 que se guardan con ENTER. CLEAR sale sin guardar.
- ENTER apenas entrás a una sección, antes de cargar nada, muestra el valor actual sin cambiarlo (modo visualización).
- De fábrica: instalador 0000, maestro del sistema 1234, mantenimiento vacío. Se cambian el primer día en [397] y [399].

**Impacto:** no pisás valores sin querer y la central no queda abierta con códigos que figuran en el manual público.

**Quién lo dice:** 3 de 3 fuentes coinciden en el procedimiento (guías de instalación y programación SP+, guía EVOHD+); en cambiar los códigos de fábrica, 4 de 10 páginas del tema seguridad lo sostienen y ninguna discrepa.

**Laboratorio** · Rápido · 10 min
Central SP o MG de banco, desarmada y con StayD apagado.
1. Leé un valor sin tocarlo (retardo de entrada 1, 45 s de fábrica):
```text
[ENTER] + código de instalador + [710]
[ENTER]          modo visualización: muestra el primer dígito
[ENTER]          siguiente dígito (sigue a las secciones siguientes)
[CLEAR]          sale sin cambiar nada
```
2. Cambiá el código de instalador por uno propio de la obra (4 o 6 dígitos, que no sea 0000, 1234 ni una fecha):
```text
[ENTER] + código de instalador actual + [397] + código nuevo
```
3. Cambiá el maestro del sistema (no se puede borrar, solo cambiar):
```text
[ENTER] + código de instalador + [399] + código maestro nuevo
```
4. Si vas a usar código de mantenimiento para otro técnico, cargalo en [398]: puede programar casi todo, menos comunicación ([815] a [817], [910], [911], [918] a [949]) y códigos de usuario.
5. Anotá los códigos en la ficha de la obra (sistema de gestión, no en el gabinete).

⚠️ En EVO la entrada es distinta: mantener [0], código de seis dígitos (000000 de fábrica) y secciones de cuatro dígitos.

**Regla para quedarse**
Miro la sección antes de escribirla.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Códigos de fábrica, modo de programación y visualización (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
- Métodos de carga decimal, hexadecimal y por opciones (guía de instalación SP+): https://www.paradox.com/Downloader/?ID=11662
- Hilo donde se sugiere entrar con códigos de fábrica (Fórum da Casa, en portugués): https://forumdacasa.com/discussion/60287/4/alarme-paradox/
