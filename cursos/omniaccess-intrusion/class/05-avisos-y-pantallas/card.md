# Lección 5. Avisos y pantallas

**Escuchá:** avisos-y-pantallas.mp3 (2 min)

**La idea, en tres líneas**
- En esta versión la intrusión avisa en pantallas: el canal se pone rojo en el **Monitor Intrusión**; el **Mapa** pita y habla ("Persona en Perímetro Norte 12") y la línea dibujada titila; y las pantallas de pared de **Monitores** suenan como las configures.
- Pantalla de pared Intrusión: enlace sin usuario (solo lectura), sonido **Sin sonido**, **Un tono por alarma** o **Repetir hasta que se acepte**; la **Rotación** se queda en Intrusión mientras haya una confirmada sin resolver.
- Telegram avisa la salud de los equipos ("ALERTA" y "NORMALIZADO"). Las reglas de Notificaciones y los Despachos son de Filas: no hay regla de intrusión por Telegram, WhatsApp ni push. Lo que sí sale por WhatsApp es el clip que manda el operador.

**Impacto:** el cliente sabe exactamente dónde va a sonar la alarma y nadie promete un aviso que no existe.

**Quién lo dice:** 2 de 4 fuentes piden que la alarma llegue calificada y con el video a un clic; 2 de 2 describen Telegram y Web Push como canales fuera del puesto. Lo de OmniAccess, del código: los avisos de intrusión al celular figuran en textos de la interfaz pero no están en esta versión.

**Laboratorio** · Admin · 20 min
1. **Monitores**, tarjeta **Intrusión**: en **Sonido** elegí **Repetir hasta que se acepte**.
2. En **Enlaces de pantalla** tocá **Nuevo enlace**, nombre "Pared puesto", **Crear enlace** y copiá la URL. Es de solo lectura: nadie decide desde ahí sin usuario del panel.
3. En la PC de la pared, abrí Chrome en modo kiosco con ese enlace (el ejemplo está en la misma pantalla de Monitores):
```text
chrome.exe --kiosk --autoplay-policy=no-user-gesture-required "https://<servidor>/monitor/intrusion?pantalla=<token>"
```
Sin kiosco también anda, pero pide un toque: "Tocá la pantalla para habilitar el sonido y la pantalla completa".
4. **Mapa → Editar mapa** → ícono de video → **Cruces de línea**. En "Perímetro Norte 12" tocá **Dibujar**, marcá los dos puntos sobre el cerco en el mapa y **Finalizar**. Si la cámara ya está ubicada, probá **Sugerir**.
5. Salí de edición, dejá el sonido del mapa activado y cruzá la línea: el mapa pita, dice la cámara y la línea titila en rojo con "tocá para aceptar".
6. Anotá para la entrega al cliente: dónde suena (pared, mapa, monitor) y que el celular no recibe la intrusión.

**Regla para quedarse**
Decile al cliente por escrito dónde suena la alarma y dónde no.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- La alarma calificada y con video a un clic, y la fatiga del operador (Davantis): https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf
- Cómo funcionan los bots de Telegram: https://core.telegram.org/bots/features
- Web Push, el protocolo de los avisos del navegador (RFC 8030): https://datatracker.ietf.org/doc/html/rfc8030
