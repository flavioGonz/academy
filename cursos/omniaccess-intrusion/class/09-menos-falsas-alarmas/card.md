# Lección 9. Menos falsas alarmas

**Escuchá:** menos-falsas-alarmas.mp3 (2 min)

**La idea, en tres líneas**
- Se atacan en orden: primero la instalación (posición, horizonte fuera del cuadro, vidrio limpio, telarañas, luces que prenden y apagan), después la regla (línea lejos de árboles, un solo sentido, zona más chica, sensibilidad 40 a 60), después el objetivo persona o vehículo, y al final medir.
- Para medir, OmniAccess ya trae los números en el **Análisis** de cada detección: porcentaje de falsas de las últimas 50 revisadas de esa cámara (con 5 o más), ritmo de hoy contra la misma hora de los 7 días previos, y ráfagas. En la ficha de la cámara de la pared: **Detecciones hoy**, **Reales hoy** y **Falsas hoy**.
- El riesgo del otro lado: bajar tanto la sensibilidad que el intruso real no dispara. Un cambio por vez, y probar caminando de noche.

**Impacto:** el operador vuelve a confiar en la alarma, y la alarma verdadera no se pierde entre cien falsas.

**Quién lo dice:** 4 de 5 fuentes coinciden en empezar por instalación y configuración antes que tecnología; Davantis (que vende analítica) suma medir cada mes por zona y advierte contra perder detecciones reales; un foro muestra que sin clasificación ni porcentaje ni sensibilidad alcanzan.

**Laboratorio** · Admin · 20 min
1. **Monitor Intrusión → Evidencia**, **Estado**: Revisadas, últimos 7 días. Elegí la cámara con más tarjetas **Falsa**.
2. En la vista de pared, abrí una detección falsa de esa cámara y anotá del **Análisis**: % de falsas, "hoy en esta cámara" y si hay ráfagas.
3. Mirá 3 fotos falsas y anotá la causa: animal, faros, árbol, telaraña, lluvia, sombra.
4. Elegí **un** cambio según la causa:
```text
Telaraña o vidrio sucio  -> limpieza (sin tocar la regla)
Faros o calle en cuadro  -> línea más adentro o sentido A→B
Animales                 -> Objetivo: Persona (si la cámara clasifica)
Árbol o vegetación       -> zona más chica o línea lejos del árbol; sensibilidad 40
```
5. Aplicalo con el **calibrador** y cruzá caminando de noche para confirmar que la persona sigue disparando.
6. Anotá la fecha del cambio. En una semana repetí el paso 2 y compará el porcentaje.

⚠️ No bajes la sensibilidad de todo el perímetro de una vez: es la forma más rápida de quedarte sin detecciones reales.

**Regla para quedarse**
Un cambio por vez, probado de noche y medido una semana.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Causas, cuatro niveles de intervención y el riesgo del falso negativo (Davantis): https://www.davantis.com/wp-content/uploads/perimeter-security-false-alarms-guide.pdf
- Arañas, reflejos y región de interés (Uniview): https://www.uniview.com/News/Blog/202605/1100575_169683_0.htm
- Cuando ni porcentaje ni sensibilidad frenan gatos y pájaros (ipcamtalk): https://ipcamtalk.com/threads/intrusion-detection-settings-does-not-work.24107
