# Lección 7. Usuarios y horarios

**Escuchá:** usuarios-horarios.mp3 (2 min)

**La idea, en tres líneas**
- PIN público compartido (de fábrica 33333333) o privado por usuario; cada usuario lleva PIN, hasta 5 tarjetas, rostro, relé y horario.
- La carga masiva se hace exportando el `.tgz`, editando el `.csv` de adentro y reimportando.
- En reconocimiento facial, el antisuplantación en "Close" deja pasar una foto; en tarjetas, Mifare cifrada es más segura que leer solo el UID.

**Impacto:** el edificio pasa de un código para todos a credenciales por persona que se dan de baja una por una y respetan horarios.

**Quién lo dice:** 1 de 1 fuente (guía de administrador del E16); evidencia escasa, sin discrepancias. Los límites varían por modelo: E12 y E16 solo leen tarjetas IC de 13,56 MHz.

**Laboratorio** · Admin · 15 min
1. `Access Control > PIN Setting > Public PIN`: cambiá 33333333 por un código propio o deshabilitalo.
2. Creá un horario "Lun a Vie 08 a 18" en la sección de horarios de acceso.
3. `Directory > User > +Add`: dos usuarios con PIN privado, una tarjeta (Obtain y acercar la tarjeta), Relay A y el horario nuevo.
4. `Directory > User > Export`: descomprimí el `.tgz` y abrí el `.csv`:
```text
UserID,Name,PIN Code,Card Code
1003,Prueba Tres,482913,
1004,Prueba Cuatro,559107,
1005,Prueba Cinco,603418,
```
5. Volvé a comprimir en `.tgz` (7-Zip en Windows) e importá con `Select File > Import`.
6. Probá un PIN dentro y otro fuera del horario (cambiá la hora del equipo si hace falta).
7. Si el modelo tiene rostro: `Access Control > Face Setting`, revisá que el antisuplantación no esté en Close.

**Regla para quedarse**
Nadie entra con "Always" si tiene un horario real, y el PIN público de fábrica no llega al día de la entrega.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- PIN, tarjetas, rostro, horarios y carga masiva en el E16: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
