# Lección 1. Entrar sin romper

**Escuchá:** entrar-sin-romper.mp3 (2 min)

**La idea, en tres líneas**
- Entrá por WinBox desde un puerto LAN (ether1 es WAN por defecto) y, si la IP no responde, por la MAC desde Neighbors.
- Todo cambio que pueda cortarte, en Safe Mode y en pasos chicos: si la sesión se cae, el router deshace los cambios.
- Conservá la configuración por defecto salvo que vayas a reconstruir todo con criterio; los CCR vienen sin ella.

**Impacto:** dejás de perder el acceso a equipos remotos por un cambio mal hecho.

**Quién lo dice:** 3 de 3 fuentes coinciden en acceso por MAC y Safe Mode; sobre la configuración por defecto, la documentación recomienda conservarla y la guía de VLAN del foro arranca de cero.

**Laboratorio** · Rápido · 10 min
Con un hAP o cualquier RouterBOARD de laboratorio con RouterOS 7:
1. Conectá la notebook a ether2. En WinBox, pestaña Neighbors, conectate por la **MAC** con usuario `admin` (contraseña vacía o la de la etiqueta).
2. Abrí New Terminal y mirá qué trae de fábrica:
```routeros
/interface/list/member/print
/ip/firewall/filter/print
/ip/address/print
```
3. Guardá el estado inicial:
```routeros
/export file=inicial
```
4. Probá Safe Mode: apretá `Ctrl+X` (el prompt muestra `<SAFE>`), agregá una regla inocua y salí con `Ctrl+D`:
```routeros
/ip/firewall/filter/add chain=forward action=passthrough comment="prueba-safe"
```
5. Volvé a entrar y verificá que la regla no está: `/ip/firewall/filter/print where comment="prueba-safe"`.
6. Mirá el historial: `/system/history/print`.

⚠️ Safe Mode guarda hasta 100 acciones; si pegás un script largo, sale solo del modo seguro y no deshace nada.

**Regla para quedarse**
Todo cambio que me puede cortar el acceso lo hago en Safe Mode y de a uno.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Primera configuración en RouterOS 7.25 (WinBox, Neighbors, defconf): https://manual.mikrotik.com/docs/7.25/getting-started/first-time-configuration
- Safe Mode, undo y export: https://help.mikrotik.com/docs/spaces/ROS/pages/328155/Configuration+Management
