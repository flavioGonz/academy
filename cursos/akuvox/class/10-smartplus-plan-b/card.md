# Lección 10. SmartPlus con plan B

**Escuchá:** smartplus-plan-b.mp3 (2 min)

**La idea, en tres líneas**
- SmartPlus da app del residente, llaves temporales y apertura por Bluetooth, y ocupa la cuenta SIP 1 del equipo.
- Las reseñas públicas de la app reportan llamadas que fallan y notificaciones tardías: es un extra, no el único camino.
- Monitor, PIN y tarjeta trabajan localmente; si se cae internet, la entrada sigue andando.

**Impacto:** el cliente tiene app y además una entrada que no depende de la nube, y el reclamo por la app no se convierte en "el portero no anda".

**Quién lo dice:** 2 de 3 fuentes coinciden (guía del E16 y la ficha de la app en Google Play); Claroty recomienda no exponer el equipo a internet aunque se pierda la app.

**Laboratorio** · Admin · 15 min
1. En una hoja, armá la tabla de qué depende de internet:
```text
Función                      Local   Necesita internet
Llamada portero -> monitor    ?           ?
Apertura desde el monitor     ?           ?
PIN / tarjeta en el portero   ?           ?
Llamada a la app SmartPlus    ?           ?
Llave temporal nueva          ?           ?
```
2. Revisá en `Account > Basic` qué cuenta quedó para SmartPlus y cuál para la central (si hay).
3. Desconectá el WAN del router de laboratorio.
4. Probá cada fila y completá la tabla con lo que realmente pasó.
5. Volvé a conectar el WAN y verificá que la app recupere la llamada.
6. Pasá la tabla a la ficha de entrega del cliente.

**Regla para quedarse**
Si se corta internet, el monitor atiende y la puerta abre igual; la app es un extra que se explica así en la entrega.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- La app SmartPlus y sus reseñas: https://play.google.com/store/apps/details?id=com.akuvox.mobile.smartplus&hl=en&gl=US&pli=1
- Cuenta SIP 1 y SmartPlus: https://knowledge.akuvox.com/docs/intercom-call-configuration-8
- Por qué Claroty recomienda no exponer el equipo: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar
