# Lección 23. Safe Mode

**Escuchá:** safe-mode.mp3 (2 min)

**La idea, en tres líneas**
- Safe Mode marca un punto de vuelta: si la sesión que lo tomó se corta, RouterOS deshace todo lo hecho desde ahí. Esos cambios llevan la marca `F` en `/system/history`, el mismo historial que usa `/undo`.
- Se entra con el botón **Safe Mode** de WinBox o WebFig, o con `Ctrl+X` (o `F4`) en la terminal, donde el prompt muestra `<SAFE>`. Para confirmar: `Ctrl+X` otra vez o soltar el botón. Para descartar: `Ctrl+D`.
- Entran 100 acciones: si te pasás, sale solo del modo seguro y no deshace nada. Pasos chicos: un cambio, verificás, confirmás y volvés a entrar.

**Impacto:** tocás firewall, bridge y VLAN, IP de gestión o ruta por defecto de un cliente remoto sin arriesgar un viaje al sitio.

**Quién lo dice:** 5 de 6 fuentes coinciden en cómo se entra, se confirma y se deshace (documentación 7.25, página de la CLI, foro oficial, una guía universitaria; una guía de practicantes difiere en detalles); discrepan en cuánto tarda la reversión (la documentación toma el timeout TCP de 9 minutos, el foro la ve en segundos o al minuto), en si un corte de energía confirma los cambios (el foro lo vio en 6.40.4, la página de la CLI sugiere lo contrario, sin confirmar en RouterOS 7) y en si conviene quedarse en Safe Mode todo el trabajo (la guía universitaria sí, la documentación pide pasos chicos).

**Laboratorio** · Foco · 15 min
En un hAP o cualquier RouterBOARD de laboratorio con RouterOS 7 y la configuración por defecto, nunca en un equipo de cliente:
1. Conectá la notebook a ether2 y entrá por WinBox a 192.168.88.1. Abrí New Terminal y sacá la foto de antes:
```routeros
/export file=antes-safe
```
2. Activá Safe Mode: en WinBox, el botón **Safe Mode** de la barra de arriba, al lado de Undo y Redo; en New Terminal, `Ctrl+X`. En la terminal aparece `[Safe Mode taken]` y el prompt termina en `<SAFE>`.
3. Cortate a propósito deshabilitando el puerto por donde entrás:
```routeros
/interface/disable ether2
```
WinBox se congela y se desconecta. Eso es lo que buscabas.
4. Esperá sin tocar nada. Cuando el router da tu sesión por muerta, deshace el cambio, ether2 vuelve y reconectás. Puede tardar de segundos a varios minutos; la documentación toma como referencia el timeout TCP de 9 minutos. Verificá:
```routeros
/interface/print where name=ether2
/system/history/print
```
5. Ahora un cambio bueno, confirmado. `Ctrl+X` de nuevo, cambiá el nombre y mirá la marca `F` en el historial:
```routeros
/system/identity/set name=LAB-SAFE
/system/history/print
```
Confirmá con `Ctrl+X` (o soltando el botón): el prompt pierde el `<SAFE>`. Desconectate, volvé a entrar y verificá que el nombre quedó.
6. Probá la salida que descarta: `Ctrl+X`, `/system/identity/set name=LAB-DESCARTE` y `Ctrl+D`. Abrí otra terminal: el nombre sigue siendo `LAB-SAFE`.

Si otro técnico tiene el Safe Mode tomado, al pedirlo RouterOS pregunta `u` (deshace lo suyo y te lo da), `r` (conserva sus cambios y te lo da) o `d` (no toca nada).

⚠️ Safe Mode mira la sesión, no si el cambio era bueno: si el cambio corta tu sesión a propósito (por ejemplo, mover la VPN por la que entrás), se deshace igual. Para eso, un veterano del foro usa un backup y un scheduler que lo restaura a los 5 minutos si no lo borrás. Y un corte de energía no es una forma de deshacer.

**Regla para quedarse**
Antes de un cambio que me puede cortar: export, Safe Mode, un cambio, verifico y confirmo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Safe Mode, historial, undo y toma del modo por otro usuario (RouterOS 7.25): https://manual.mikrotik.com/docs/7.25/getting-started/configuration-management/
- Barra de WinBox 4 con Undo, Redo y Safe Mode: https://manual.mikrotik.com/docs/7.25/management-tools/winbox
- Foro: Safe Mode en WebFig y por qué cada sesión es independiente: https://forum.mikrotik.com/t/safe-mode-in-webfig/92508
- Foro: qué pasó al cortar la energía en Safe Mode, y el límite con las VPN: https://forum.mikrotik.com/t/safe-mode-powercycle-useless/105625
- Foro: backup con restauración programada para cambios que Safe Mode no cubre: https://forum.mikrotik.com/t/how-to-execute-risky-mikrotik-commands-safely/165189
