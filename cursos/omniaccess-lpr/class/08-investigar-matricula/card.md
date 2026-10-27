# Lección 8. Investigar matrícula

**Escuchá:** investigar-matricula.mp3 (2 min)

**La idea, en tres líneas**
- Un clic en cualquier captura abre la ficha del evento: estado, hora, foto completa, dirección, credencial, cámara y, en una salida, la Permanencia. Seis acciones: Grabación, Similares, Clip, Exportar, Registrar y Lista negra.
- Tres pestañas responden "¿es habitual o es la primera vez?": Perfil (pasadas por día con el gráfico de 30 días, cámaras habituales con entradas y salidas, horarios habituales), Historial (todos sus accesos) y Datos (lo que mandó la cámara).
- Búsqueda inteligente, modo Accesos, busca escrito como se habla sobre la base propia y responde en menos de un segundo: `camioneta blanca ayer a la tarde`, `entradas denegadas hoy`, o la matrícula. Exportar arma el ZIP de evidencia.

**Impacto:** un reclamo de "no me abrió" o un incidente de anoche se responde en minutos y con evidencia lista para entregar, en vez de revisar video durante una hora.

**Quién lo dice:** los Manuales del Operador y del Administrador describen la ficha, la búsqueda y el ZIP; el código confirma las acciones y que el ítem Búsqueda inteligente aparece solo con un NVR VPro dado de alta (si no está, se investiga desde Historial de Acceso). La web coincide en que la evidencia vale si la hora es confiable y si una persona verifica la lectura.

**Laboratorio** · Foco · 20 min
Práctica guiada sobre un barrio de demo o de prueba.
1. Búsqueda inteligente → modo Accesos (ícono verde). Escribí:
```text
entradas denegadas hoy
```
Mirá las etiquetas verdes con lo que el sistema entendió.
2. Abrí uno de los eventos. Leé estado, hora, dirección, cámara y credencial.
3. Pestaña Perfil: ¿cuántas pasadas por día tiene esa matrícula? ¿Por qué cámaras entra y sale? ¿A qué hora suele pasar? Escribí en una línea si es habitual o nueva.
4. Pestaña Historial: anotá sus últimos tres accesos.
5. Grabación: mirá el video del NVR en ese instante y comprobá que es el mismo auto.
6. Exportar: bajá el ZIP y abrilo. Tiene que traer cuatro archivos:
```text
captura.jpg · recorte_matricula.jpg · clip_30s.mp4 · evento.json
```
7. Reclamo simulado: "ayer a la noche no me abrió" con la matrícula de prueba `SBA1234`. Buscá la matrícula. Si hay evento Denegado, revisá padrón y grupo; si no hay evento, la cámara no la leyó: mirá la grabación de esa hora.
⚠️ El ZIP tiene datos personales (patente, hora, foto): se entrega solo a quien el cliente autoriza.

**Regla para quedarse**
Antes de afirmar algo sobre una matrícula miro el recorte, el perfil y la grabación, y recién ahí exporto.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Qué hace que una grabación sirva como prueba: https://mobatime.com/support/faq/why-is-time-important-for-cctv
- Una lectura identifica un vehículo, no a quien maneja: https://www.forasoft.com/learn/video-surveillance/articles-vms/license-plate-recognition-lpr-anpr
- Alertas equivocadas que se frenaron porque alguien verificó: https://www.techspot.com/community/topics/one-california-town-found-flocks-license-plate-cameras-were-wrong-71-of-the-time.298313/
