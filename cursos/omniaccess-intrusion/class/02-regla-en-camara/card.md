# Lección 2. Regla en cámara

**Escuchá:** regla-en-camara.mp3 (2 min)

**La idea, en tres líneas**
- La línea de cruce y la zona de intrusión viven en la cámara (o en el NVR Dahua). El calibrador de OmniAccess las dibuja sobre un cuadro real y las escribe en el equipo por ISAPI: una regla de línea y una de zona por cámara.
- Línea: dos puntos y un sentido (A→B, Ambos, B→A). Zona: tres puntos o más. Sensibilidad 40, 60 u 80; objetivo Persona, Vehículo o Ambos en las cámaras que clasifican (AcuSense).
- **Auto-perfil · Perímetro recomendado** deja sensibilidad 60, objetivo personas y vehículos y el aviso a OmniAccess. Es un punto de partida: después se camina la escena.

**Impacto:** la cámara avisa por lo que importa y no por cada sombra.

**Quién lo dice:** 4 de 5 fuentes coinciden en cómo dibujar la línea (larga, lejos del borde, con sentido) y 4 de 4 en filtrar por persona o vehículo; Davantis advierte que la clasificación sola falla con objetos chicos y lejanos de noche.

**Laboratorio** · Foco · 20 min
Cámara de demo "Perímetro Norte 12" (192.0.2.21), Hikvision con cruce de línea:
1. En **Monitor Intrusión**, pasá el mouse por el canal y tocá el ícono de regla y lápiz (**Calibrar líneas y zonas**). También se abre desde **Dispositivos → Intrusión → Calibrar**.
2. Tocá **Línea**. Marcá los dos extremos a lo largo del cerco, que la línea corte todo el paso posible y no quede pegada al borde del cuadro ni sobre un árbol o un poste.
3. Elegí el sentido: **A→B** si solo importa entrar. Mirá las flechas que dibuja sobre la línea y tocá **Guardar**. Aparece "Línea guardada en la cámara".
4. Tocá **Sensibilidad** hasta 60 y **Objetivo** hasta Persona. Si dice "esta cámara no filtra por objetivo", anotalo: esa cámara va a necesitar más ajuste.
5. Pedile a alguien que cruce caminando en el sentido elegido y después al revés. Con A→B, solo la primera pasada tiene que aparecer en la franja **Detecciones**.
6. Para ver lo mismo en la cámara, entrá a su web:
```text
Navegador: 192.0.2.21
Configuración > Evento > Evento inteligente > Detección de cruce de línea
(en inglés: Configuration > Event > Smart Event > Line Crossing Detection)
```
⚠️ El calibrador escribe en la cámara del cliente: en producción, avisá antes y anotá los valores que había.

**Regla para quedarse**
La línea corta todo el camino, lejos del borde, y se prueba caminando.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Recomendaciones para dibujar la línea y probarla (Ajax): https://ajax.systems/support/posts/line-crossing-detection-in-ajax-video-surveillance/
- Sentido A→B, B→A y A↔B, y objetivo persona o vehículo (Milesight): https://www.milesight.com/support/download/document-center/ipc-series/ai/en/user-manual/line-crossing.html
- Umbral de tiempo, sensibilidad y porcentaje en la zona (Uniview): https://global.uniview.com/res/201905/30/20190530_1728629_How-to-set-Intrusion-Detection_850805_168459_0.pdf
