# Lección 35. Vigilar con Netwatch

**Escuchá:** netwatch.mp3 (2 min)

**La idea, en tres líneas**
- Netwatch prueba un equipo cada tanto y, cuando cambia de estado, corre `down-script` o `up-script` una vez. En RouterOS 7 hay sondas `simple`, `icmp` (10 paquetes por prueba, pérdida y latencia), `tcp-conn`, `http-get`, `https-get` y `dns`.
- Para un NVR, mejor `tcp-conn` al puerto del servicio que un ping solo; para no recibir falsas alarmas, `icmp` con varios paquetes en vez de un ping suelto.
- Los scripts corren con permisos acotados (read, write, test, reboot): desde 7.13, un `fetch` a Telegram desde Netwatch necesita `output=none`. Después de cada actualización, probá el aviso desenchufando.

**Impacto:** te enterás vos de que cayó el NVR, una cámara o un enlace antes que el cliente, y algunas fallas se arreglan solas, como una cámara PoE colgada.

**Quién lo dice:** 4 de 5 fuentes coinciden en el uso (sondas, scripts al caer y al volver, avisos por mail o mensajería); discrepan en el failover (Netwatch, más rápido y con scripts, contra rutas recursivas sin scripts) y en el reinicio de PoE (script de Netwatch o el vigilante `power-cycle-ping` del propio puerto).

**Laboratorio** · Foco · 20 min
Escenario como en la lección de port forwarding: NVR en 192.168.88.50 con RTSP en el 554; cámara PoE en `ether5` con 192.168.88.60 (router con PoE out, por ejemplo un hEX PoE; sin PoE, salteá el paso 5). RouterOS 7 con la hora puesta por NTP. Sin NVR sirve una PC con un servicio en el 554.
1. Sonda al servicio del NVR, con aviso en el log:
```routeros
/tool/netwatch/add name=nvr host=192.168.88.50 type=tcp-conn port=554 interval=30s down-script=":log warning \"NVR 192.168.88.50 caido\"" up-script=":log info \"NVR 192.168.88.50 volvio\""
/tool/netwatch/print
```
La columna de estado pasa de `unknown` a `up`. Después de reiniciar el router, Netwatch espera 5 minutos (`startup-delay`) antes de probar.
2. Desenchufá el NVR (o deshabilitá su puerto) y mirá el log:
```routeros
/log/print where message~"NVR|192.168.88.50"
```
En menos de un minuto aparece el evento `down` con el host y tu mensaje; al volver a enchufar, el `up`.
3. Aviso por mail (datos de tu proveedor; con Gmail, contraseña de aplicación). Primero probá el envío solo:
```routeros
/tool/e-mail/set server=smtp.gmail.com port=587 tls=starttls from=alertas@example.com user=alertas@example.com password="clave-de-aplicacion"
/tool/e-mail/send to=soporte@example.com subject="Prueba alerta" body="Hola desde el router"
/tool/e-mail/print
```
Si `last-status` dice `succeeded`, salió. Después, al script de caída:
```routeros
/tool/netwatch/set [find name=nvr] down-script=":log warning \"NVR caido\"; /tool/e-mail/send to=soporte@example.com subject=\"NVR caido\" body=\"El NVR 192.168.88.50 no responde en el puerto 554\""
```
Texto sin tildes: la documentación sugiere ASCII para que se lea bien en cualquier cliente de correo.
4. Aviso a Telegram (token del bot y chat de ejemplo, se sacan desde Telegram). El `\?` es para que la terminal no abra la ayuda, y `output=none` es lo que lo hace andar desde Netwatch desde 7.13:
```routeros
/tool/netwatch/set [find name=nvr] up-script=":log info \"NVR volvio\"; /tool/fetch mode=https address=api.telegram.org src-path=\"bot123456:TOKEN-EJEMPLO/sendMessage\?chat_id=-1001234567890&text=NVR%20volvio\" check-certificate=yes output=none"
```
Desenchufá y volvé a enchufar el NVR: llega el mail al caer y el Telegram al volver.
5. Cámara PoE que se cuelga: Netwatch le corta el PoE 10 segundos al caer.
```routeros
/tool/netwatch/add name=cam-entrada host=192.168.88.60 type=icmp interval=1m down-script="/interface/ethernet/poe/power-cycle ether5 duration=10s"
```
O sin Netwatch, con el vigilante del propio puerto (elegí una de las dos):
```routeros
/interface/ethernet/poe/set ether5 power-cycle-ping-enabled=yes power-cycle-ping-address=192.168.88.60 power-cycle-ping-timeout=1m
```
El `down-script` corre una vez por caída: si la cámara no vuelve, no la reinicia en bucle.

⚠️ Netwatch no puede avisar si se cae el router entero o su única salida a internet: para eso, un monitor de afuera (otro router o un servidor en la oficina que vigile al cliente).

**Regla para quedarse**
Cada equipo crítico tiene su sonda y su aviso, y lo pruebo desenchufando después de cada actualización.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Netwatch en RouterOS 7.25, sonda por sonda con ejemplos de log: https://manual.mikrotik.com/docs/7.25/diagnostics-monitoring-and-troubleshooting/netwatch
- El aviso a Telegram que dejó de andar con 7.13: https://forum.mikrotik.com/t/netwatch-with-fetch-stopped-working-after-7-13/172865
- Reinicio y vigilante de PoE out: https://manual.mikrotik.com/docs/7.25/hardware/poe-out
