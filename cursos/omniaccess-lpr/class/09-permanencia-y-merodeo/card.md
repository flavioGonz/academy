# Lección 9. Permanencia y merodeo

**Escuchá:** permanencia-y-merodeo.mp3 (2 min)

**La idea, en tres líneas**
- Permanencia: cuando una matrícula sale por una cámara declarada Salida, la ficha muestra cuánto estuvo adentro desde su última entrada. Depende de que cada cámara tenga bien puesto el sentido.
- Merodeo: la misma matrícula pasa 3 veces o más en 30 minutos (valores por defecto) y no es un residente autorizado. Salta una alerta Merodeo abajo a la izquierda del monitor y queda una entrada en la bitácora con cuántas pasadas y por cuántos accesos.
- Plazas de Parking → Anomalías de presencia junta lo que se arrastra en días: autos no identificados adentro, vehículos del barrio adentro hace mucho (4 días) y lotes sin movimiento, posible casa vacía (21 días).

**Impacto:** el guardia ve patrones (alguien relevando, un auto que nunca salió, una casa vacía) en vez de lecturas sueltas que no dicen nada.

**Quién lo dice:** sale del código y del Manual del Operador; la web aporta que el merodeo es un metadato de analítica estandarizado (ONVIF Profile M) y que las lecturas guardadas se vuelven un mapa de por dónde anda la gente. Diferencia a tener en cuenta: el manual habla de pasadas "por el mismo acceso"; el código cuenta pasadas por cualquier acceso, y los umbrales se ajustan en la configuración del sistema (no hay pantalla propia en esta versión).

**Laboratorio** · Foco · 15 min
Pasos 3 y 4 solo en una instalación de prueba: crean eventos reales.
1. En Monitor LPR abrí la salida de un residente. En la ficha, leé la Permanencia y compará con su entrada en la pestaña Historial.
2. Plazas de Parking → Anomalías de presencia: anotá cuántos autos no identificados hay adentro y qué vehículo lleva más días.
3. Simulá un merodeo con una matrícula que no está en el padrón, tres pasadas separadas por 30 segundos (más que el antirrebote de 20):
```bash
for i in 1 2 3; do
  curl -s -X POST 192.0.2.10:10000/api/webhooks/hikvision -H "Content-Type: application/xml" \
    --data '<EventNotificationAlert><ipAddress>192.0.2.21</ipAddress><eventType>ANPR</eventType><ANPR><licensePlate>SCD5678</licensePlate></ANPR></EventNotificationAlert>'
  echo; sleep 30
done
```
4. Con la tercera pasada aparece la alerta Merodeo en el monitor. Buscala también en el Historial de Acceso.
5. Abrí la ficha de `SCD5678` → Perfil: confirmá las pasadas de hoy y por qué cámara.
6. Escribí en la bitácora qué harías en un barrio real: ¿repartidor buscando una dirección o alguien relevando? Lo que decide es el historial y la grabación, no la alerta sola.
⚠️ Merodeo y permanencia hablan de vehículos, no de personas: antes de escalar, se mira la grabación.

**Regla para quedarse**
Un patrón se confirma con el historial y la grabación antes de escalarlo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- El merodeo como metadato de analítica estandarizado: https://www.videoexpertsgroup.com/glossary/onvif-profile-m
- Las lecturas guardadas como mapa de movimientos, y su cuidado: https://www.forasoft.com/learn/video-surveillance/articles-vms/license-plate-recognition-lpr-anpr
- Retención y privacidad de los datos de matrículas: https://en.wikipedia.org/wiki/Automatic_number-plate_recognition
