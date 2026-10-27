# Lección 3. Alta del contador

**Escuchá:** alta-del-contador.mp3 (2 min)

**La idea, en tres líneas**
- La cámara se da de alta en Dispositivos Conteo como "Contador de Filas", fabricante Bosch, con IP, usuario y clave.
- OmniAccess le pide a la cámara un pull point ONVIF y pregunta cada 5 s; graba un evento solo cuando el valor cambia. El push (la cámara avisa sola) es opcional y, si entrega, el pull se calla.
- Se verifica con Filas → Analíticas ONVIF y con el estado del sondeo en el servidor, y se da por instalada recién cuando el aforo cambia en la tabla.

**Impacto:** cuando una fila "no cuenta", en dos minutos sabés si el problema es la cámara, la suscripción o la red.

**Quién lo dice:** 3 de 5 fuentes describen el pull point igual (especificación ONVIF Core, Milestone, EdgeX) y 3 de 5 filtran por cambio de valor. El foro de Milestone muestra que el filtrado falla fácil. Los intervalos y pantallas de OmniAccess salen del código.

**Laboratorio** · Foco · 20 min
Instalación de prueba con Modo Cola y la cámara de la lección 2 (192.0.2.10).
1. Abrí Dispositivos Conteo → Agregar. Tipo: Contador de Filas. Fabricante: Bosch. Nombre de ejemplo: "Fila Caja 1". Cargá IP, usuario y clave. Guardá.
2. Abrí Filas. En la tabla "Detección por fila (en vivo)" esperá las filas Aforo (tipo Aforo), Entrada y Salida (tipo Flujo) con su "Última lectura".
3. Tocá "Analíticas ONVIF" sobre el video. Revisá:
```text
Reglas VCA detectadas      Aforo · OccupancyCounting, entrada y salida de campo
Tópicos ONVIF              lista de lo que la cámara puede emitir
Reglas Activas             eventos que llegaron recién
Últimos Conteos en Base    último valor por canal
```
4. En el servidor, consultá el estado del sondeo:
```bash
curl -s "127.0.0.1:10001/api/queue/poll?info=1"
# autoPolling: true, y en subscriptions: pullPointUrl, expiresAt, lastPull
```
5. Mirá el registro mientras alguien camina por la zona:
```bash
pm2 logs omniaccess-web --lines 50 | grep ONVIF
# [ONVIF] Created subscription for 192.0.2.10 ...
# [ONVIF-Poll] ✅ Fila Caja 1: Aforo = 1 personas (Changed)
```
6. Si aparece "Failed to create subscription", revisá desde el servidor que la cámara responda por HTTPS en el puerto 443 y que el usuario sea el correcto.

⚠️ Si alguien configura el push (variable ONVIF_PUSH_URL), en esta versión los eventos que entran por push solo avisan por Telegram y no por los otros canales. Antes de dejarlo activo, probá todos los avisos.

**Regla para quedarse**
No doy por instalada una fila hasta ver un cambio de aforo llegar a la tabla.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Pull point y Basic Notification en la especificación (ONVIF Core 26.06): https://www.onvif.org/specs/2606/ONVIF-Core-Spec-v2606.pdf
- Cómo un VMS consulta eventos cada 5 s y filtra los Changed (Milestone): https://doc.milestonesys.com/latest/en-US/onvifdriver/events.htm
- Pull contra push, con suscripción y renovación (EdgeX): https://docs.edgexfoundry.org/3.2/microservices/device/services/device-onvif-camera/supplementary-info/api-event-handling/
- Tópicos tns1:IVA y tns1:RuleEngine en Bosch (Keenfinity): https://knowledge.keenfinity-group.com/video-systems/article/tns1-iva-does-not-include-all-iva-rules-in-camera
