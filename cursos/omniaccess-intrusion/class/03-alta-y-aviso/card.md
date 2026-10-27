# Lección 3. Alta y aviso

**Escuchá:** alta-y-aviso.mp3 (2 min)

**La idea, en tres líneas**
- Alta: **Dispositivos → Agregar → Cámara de intrusión**, o desde el NVR con **Importar cámaras (clasificar)**, eligiendo por canal LPR, intrusión u omitir. La puesta a punto pone la hora, el aviso a OmniAccess, el video en vivo y la grabación (NVR y canal).
- Aviso: en el canal, el ícono de campana abre **Servidor de alarma**. Con Hikvision, **Configurar OmniAccess como alarma** agrega el servidor (HTTP, XML, puerto 10000) sin borrar los otros, y **Probar reporte** manda el test. Con NVR Dahua, **Verificar suscripción**.
- En la cámara Hikvision, el evento tiene que tener tildado **Notificar al centro de vigilancia** en la vinculación. El test no lo prueba: lo prueba cruzar la línea.

**Impacto:** la cámara queda dada de alta de verdad: detecta, avisa, y el evento llega con foto y grabación.

**Quién lo dice:** 2 de 2 fuentes marcan el tilde de notificar al centro como condición para que el evento salga; 2 de 2 describen el test que espera un 200 del servidor. Lo demás, del código de OmniAccess.

**Laboratorio** · Campo · 25 min
Demo con NVR 192.0.2.50 y servidor OmniAccess 192.0.2.10:
1. **Dispositivos → NVR**, en el NVR elegí **Importar cámaras (clasificar)**. Marcá dos canales del perímetro como **intrusión** y el resto **omitir**. Las que ya existen solo se vinculan a su canal.
2. Las cámaras importadas toman el usuario y la clave del NVR. Si la cámara tiene otra clave, corregila en **Editar**: sin la clave de la cámara no hay foto propia del evento.
3. En **Monitor Intrusión**, pasá el mouse por "Perímetro Norte 12" y tocá la campana. Si dice **OmniAccess no configurado**, tocá **Configurar OmniAccess como alarma**.
4. Tocá **Probar reporte**. Puede contestar "El equipo reporta OK a OmniAccess ✓" o que no confirmó: varias cámaras no implementan el test. Seguí al paso 5 igual.
5. En la web de la cámara verificá la vinculación de la regla:
```text
Configuración > Evento > Evento inteligente > Detección de cruce de línea
> Método de vinculación: [x] Notificar al centro de vigilancia
```
6. Cruzá la línea. En segundos el canal se pone rojo con "Cruce de línea detectada" y la tarjeta de la franja trae la foto.
7. En **Dispositivos → Intrusión**, la fila tiene que decir **Configurada** y **Avisa**.

⚠️ Si sale "Falta configurar el host de eventos de OmniAccess", el servidor no tiene cargada su IP de eventos: es de la instalación del servidor, no de la cámara.

**Regla para quedarse**
Una cámara de intrusión está dada de alta cuando cruzaste su línea y la viste llegar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Notificación HTTP, botón Test y heartbeat: https://videos.cctvcamerapros.com/developer/docs/getting-started/http-post-setup
- Pasos en un NVR Hikvision V5 con Notify Surveillance Center: https://www.securitywholesalers.com.au/faqs/how-to-configure-acusense-using-hikvision-nvr-v5-0-firmware/
- Permisos del usuario y eventos que se notifican (Home Assistant): https://www.home-assistant.io/integrations/hikvision
