# Lección 15. Llaves de la central

**Escuchá:** llaves-de-la-central.mp3 (2 min)

**La idea, en tres líneas**
- Una SP+ tiene varias llaves con valor de fábrica publicado: instalador 0000, mantenimiento vacío, maestro 1234, ID de panel y contraseña de PC, contraseña de instalador del software BabyWare ("admin"), contraseña de receptor IP (123456 en legado) y la del módulo IP.
- Bloqueo de instalador: [395] = 147 traba la programación y el reseteo por botón deja de borrarla; 000 lo quita. Se usa solo si está en el contrato.
- Bloqueo de teclado: tras [717] códigos inválidos, los teclados se bloquean [716] minutos y se reporta.

**Impacto:** ninguna central de tu cartera se abre con un cable y una lista de códigos de manual.

**Quién lo dice:** 4 de 10 fuentes del tema seguridad sostienen cambiar los valores de fábrica (guías SP+, IPVM, Fórum da Casa); ninguna discrepa. Bloqueo de instalador y reseteo: 2 de 10 (guía SP+ y TremTech).

**Laboratorio** · Admin · 15 min
1. Copiá esta ficha y completala con la central de banco, mirando cada sección con ENTER (modo visualización) antes de cambiar:
```text
Llave                                Dónde         Fábrica             Nuevo / fecha
Código de instalador                 [397]         0000
Código de mantenimiento              [398]         vacío
Maestro del sistema (no se borra)    [399]         1234
ID de panel                          [910]         0000 (*)
Contraseña de PC                     [911]         0000 (*)
Instalador del software BabyWare     [927]         admin
Contraseña de receptor IP (legado)   [933]         123456
Contraseña del módulo IP150          app / web     paradox (firmware viejo)
Bloqueo de instalador                [395]         000 = apagado
Bloqueo de teclado (intentos/min)    [717]/[716]   000 = apagado
```
(*) La guía SP+ dice que BabyWare obliga a cambiarlas; otros manuales siguen citando 0000.
2. Cambiá cada llave que siga de fábrica por una propia de la obra.
3. Configurá el bloqueo de teclado (valores de ejemplo):
```text
[ENTER] + código de instalador + [717] 005     5 intentos
[CLEAR] [716] 010                              10 minutos de bloqueo
```
4. Decidí con el responsable comercial si se usa el bloqueo de instalador; si se usa, que conste en el contrato.
5. Guardá la ficha en el sistema de gestión, nunca dentro del gabinete.

⚠️ Si recibís una central bloqueada sin códigos, el camino es el cliente y el instalador anterior. Si no hay forma y el bloqueo está apagado, el reseteo y la reprogramación completa se hacen con autorización escrita del cliente.

**Regla para quedarse**
Ninguna central sale de obra con un código de fábrica.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Códigos de acceso, bloqueo de instalador, bloqueo de teclado y reseteo (guía de instalación SP+): https://www.paradox.com/Downloader/?ID=11662
- Contraseñas de software y receptor IP (guía de programación SP+): https://www.paradox.com/Downloader/?ID=11650
- MG5050 sin código de instalador (IPVM): https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue
- Reseteo de SP4000/SP65 con bloqueo apagado (TremTech): https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/
