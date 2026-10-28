# Lección 43. Theme del monitor

**Escuchá:** theme-monitores.mp3 (2 min)

**La idea, en tres líneas**
- La pantalla de inicio se elige por modelo: C319, S567, IT88, X933 y S562 en `Device > Display Setting > Theme`, con Default (íconos) o Call List (lista de contactos para llamar); el C313 Linux en `Device > Key/Display > Home Page Mode`, con Classic o Call List Simple.
- Los botones no son el theme: cada área de `Home Page Display` y `More Page Display` lleva un tipo (Arming, SOS, Unlock, Contacts, Monitor, Browser y otros), una etiqueta y un ícono propio de hasta 100x100. `Settings Page Display` oculta entradas del menú del residente.
- Protector (Local Pictures, Local Videos o Clock, con horario), fondo, logo de arranque, idioma de pantalla y, en el S567, el estilo visual se cargan en la web; para muchos monitores, el fondo va por AutoP desde SmartPlus y toma efecto al reiniciar.

**Impacto:** el monitor se entrega con los botones que el residente usa, en español y con la imagen del edificio, y el mismo cambio se repite igual en todos los apartamentos.

**Quién lo dice:** 10 de 10 páginas leídas sobre pantallas de monitor son de la Knowledge Base de Akuvox y coinciden en el mecanismo; cambian los nombres según modelo (Default contra Classic, `Display Setting` contra `Key/Display`). No encontramos practicantes que lo documenten.

**Laboratorio** · Foco · 20 min
Con un C319 (o cualquier monitor Android de las series C, S, IT o X) en la mesa y su web abierta:
1. Pasá la pantalla de inicio de Default a Call List, mirá el monitor y volvé:
```text
C319 / S567 / IT88 / X933 / S562 : Device > Display Setting > Theme           -> Default | Call List
C313 (Linux)                     : Device > Key/Display > Home Page Mode      -> Classic | Call List Simple
```
2. En `Device > Display Setting`, sección Home Page Display, buscá el área que tiene `Arming`, cambiá su Type a `Unlock` y poné Label `Portón`. En S567 y X933, Value toma uno de los `Remote Relay HTTP` armados en Botón del monitor. Tocá `Example` para ver la grilla.
3. En `Device > Display Setting > Settings Page Display`, destildá lo que el residente no necesita tocar.
4. En `Device > Display Setting > Screen Saver Setting`, tipo `Local Pictures`, subí un JPG de 1280x800 con el nombre del edificio y fijá el horario; en `Display Settings`, `Sleep Time` de 1 minuto.
5. Pasá la pantalla a español en `Device > Time/Lang > LCD Language`.
6. Si el monitor está en SmartPlus, probá el fondo por AutoP (proyecto, AutoP, el equipo) y reiniciá:
```text
Comando                              Valor
Config.Wallpaper.Url01               URL del JPG en tu servidor HTTPS, FTP o TFTP (ej. 192.0.2.10/fondo-edificio.jpg)
Config.Settings.PICTURE.Wallpaper    1
```
7. Anotá en la ficha de la obra theme, áreas, etiquetas y protector: es lo que se repite en cada apartamento.
⚠️ En el C313, cambiar el color de la barra o del área de funciones reinicia el monitor; y una línea AutoP de otro modelo puede valer distinto (en las planillas oficiales, la pantalla de inicio es 4 o 5 en el S567 y 0 o 1 en el S562).

**Regla para quedarse**
El botón que sobra no se esconde con el theme: se cambia el tipo del área, y lo que se cambia en un monitor queda anotado para todos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Pantalla del C319 (theme, íconos, protector, logos): https://knowledge.akuvox.com/docs/screen-display-configuration-7
- Pantalla del C313, con Home Page Mode: https://knowledge.akuvox.com/docs/screen-display-configuration-6
- Formatos de protector por modelo: https://knowledge.akuvox.com/docs/screensaver-specifications
- Fondo por AutoP desde la nube: https://knowledge.akuvox.com/docs/configure-screensaver-on-indoor-monitors-using-autop-commands
