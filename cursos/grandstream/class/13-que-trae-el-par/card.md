# Lección 13. Qué trae el par

**Escuchá:** que-trae-el-par.mp3 (2 min)

**La idea, en tres líneas**
- La línea de Antel es un FXS: da tensión, timbre y tono. El puerto de la UCM es un FXO: descuelga y cuelga como un teléfono.
- Antel no publica tensiones ni frecuencias de su línea: se miden antes de enchufar (reposo, descolgado, tono, timbre).
- Todo lo que cuelga del mismo par (alarma, posnet, fax, otro teléfono) también descuelga; se anota y, para probar, se desconecta.

**Impacto:** cada obra arranca con una ficha de la línea sana, que después es la vara para cualquier reclamo o diagnóstico.

**Quién lo dice:** 4 de 4 fuentes coinciden en qué hace el FXS y qué hace el FXO; en los valores difieren (Patton unos 50 V, innovaphone de 24 a 70 V, Sandman 48 V en reposo y 4 a 18 V descolgado) y ninguna da los de Antel.

**Laboratorio** · Campo · 20 min
Con una línea real de Antel. Si en el banco no tenés línea, el FXS de un ATA HT80x registrado en la UCM hace de línea (tensión, timbre y tonos serán los del ATA, no los de Antel).
1. Desconectá el cable que va al UCM y medí en continua sobre los contactos del medio de la ficha RJ11 (3 y 4). Anotá la tensión en reposo.
2. Enchufá un teléfono analógico de prueba en la misma ficha y descolgá: tiene que haber tono continuo. Si el tono sale entrecortado o distinto, anotalo: puede ser un servicio activo en la línea.
3. Con el teléfono descolgado, medí otra vez. La tensión tiene que caer a pocos voltios; anotá el valor.
4. Llamá a la línea desde un celular: el teléfono tiene que sonar. Si tiene pantalla y la línea tiene identificador contratado, mirá si aparece el número.
5. Recorré el par y anotá todo lo que está en paralelo: panel de alarma, posnet, fax, teléfonos en otros ambientes.
6. Armá la ficha de la línea:
```text
Línea 1 (FXO1)  número: ________   reposo: ___ V   descolgado: ___ V
Tono: sí/no     Timbre: sí/no      Identificador en display: sí/no
En paralelo: alarma / posnet / fax / teléfonos: ____________
```
7. Conectá la línea al FXO1 del UCM6304A con un cable RJ11 y mirá System Status > Dashboard > Interface Status: el FXO1 pasa a gris, conectado pero sin configurar.
⚠️ El timbre es alterna de unos 70 V: no toques los contactos mientras la línea suena.

**Regla para quedarse**
Ninguna línea se enchufa al FXO sin su ficha: tensión en reposo, tensión descolgada, tono, timbre y qué más cuelga del par.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- FXS y FXO, quién da qué: https://www.patton.com/technotes/what-are-fxs-and-fxo/
- La línea de dos hilos explicada para técnicos: https://wiki.innovaphone.com/?i=11277
- La alarma que falla en la línea compartida: https://www.sandman.com/firealarm-bul.html
