# Lección 9. Atender la alerta

**Escuchá:** atender-la-alerta.mp3 (2 min)

**La idea, en tres líneas**
- Al pasar el umbral aparece en cualquier pantalla el recuadro "Alerta de aforo" con el video de la fila, "Excede umbral", el aforo contra el límite y "Acción requerida"; al mismo tiempo sale el aviso al supervisor y la notificación a la app de filas.
- Primero se mira la imagen, después se actúa (otra caja, despejar la zona). Si la fila sigue sobre el umbral 5 minutos, llega el aviso de escalamiento por Telegram.
- Hay alertas de salud que invalidan el número ("Cámara movida o tapada", "Imagen demasiado clara", "Imagen demasiado oscura") y cortes de cámara que quedan registrados con su duración.

**Impacto:** el operador reacciona a colas reales y deja registro, en lugar de correr detrás de un número.

**Quién lo dice:** el flujo de la alerta sale del código de OmniAccess. De las fuentes web, FootfallCam (1 de 1 sobre este punto) explica por qué un contador falla con conductas reales de la fila; evidencia fina.

**Laboratorio** · Foco · 15 min
Práctica guiada en la fila de prueba, con la alerta "Aforo Caja 1" (umbral 2) y un canal configurado.
1. Dejá abierta cualquier pantalla del panel (por ejemplo Reportes). Meté tres personas en la zona.
2. Cuando aparezca abajo a la derecha "Alerta de aforo", seguí este orden:
```text
1. Mirar el video del recuadro: ¿es cola real?
2. Real: abrir otra caja o despejar la zona (lo que diga el procedimiento del cliente)
3. Falsa (carro abandonado, reflejo): anotarlo para calibrar (lección 5)
4. Silenciar o descartar el recuadro con la cruz
```
3. Revisá en el celular del supervisor el mensaje con foto o clip, y en la app de filas la pestaña Alertas.
4. Dejá la fila arriba del umbral 5 minutos y verificá el aviso de escalamiento en Telegram.
5. Abrí Despachos y ubicá la alerta en la lista de la derecha (filtros Todas, Críticas, Superado, En umbral).
6. Simulá un corte: desconectá la cámara unos 30 segundos y volvé a conectarla. En Monitor en Vivo tocá la cámara y buscá la marca "Corte de cámara" en la curva de hoy.
7. Si la cámara tiene activada la detección de sabotaje y la publica por ONVIF, tapá el lente un momento y mirá si llega "Cámara movida o tapada".

⚠️ Mientras haya una alerta de salud o un corte abierto, el aforo de esa fila no es confiable: avisalo al supervisor antes de tomar decisiones con ese número.

**Regla para quedarse**
Miro la imagen antes de llamar al supervisor, y anoto cada alerta falsa para calibrar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Por qué ningún contador es perfecto en una fila real (FootfallCam): https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/
- Web Push, el aviso que llega a la app aunque esté cerrada (MDN): https://developer.mozilla.org/en-US/docs/Web/API/Push_API
