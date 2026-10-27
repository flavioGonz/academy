# Lección 8. Monitor y espera

**Escuchá:** monitor-y-espera.mp3 (2 min)

**La idea, en tres líneas**
- Monitor en Vivo muestra cada fila con video, zona, aforo y estado (OK, ALTO desde el 70 % del umbral, LLENO al 100 %); tocando una cámara aparece su curva con cortes y capturas.
- Pantalla / Kiosko es el cartel de sala: PASE, AGUARDE o AFORO COMPLETO, personas en fila y espera estimada.
- La espera estimada aplica la ley de Little: aforo actual dividido por el ritmo de salidas de los últimos 15 minutos. Sin salidas en ese lapso muestra un guion.

**Impacto:** el operador lee la fila de un vistazo y puede explicar de dónde sale el número de espera.

**Quién lo dice:** 3 de 4 fuentes explican la ley de Little igual (third-bit, Wikipedia, el propio Little a los 50 años) y 2 de 4 avisan que solo vale con la fila estable. Discrepa FootfallCam, que estima con el tiempo medio de atención. El cálculo exacto sale del código de OmniAccess.

**Laboratorio** · Rápido · 15 min
Fila de prueba con movimiento (o datos de una demo).
1. Abrí Monitor en Vivo. Probá las grillas (auto, 1x1, 2x2, 3x3) y leé el estado de cada celda.
2. Tocá una cámara. En su línea de tiempo elegí "Hoy" y después "1h". Tocá un punto de la curva para fijar su captura. Buscá si hay marcas de "Corte de cámara".
3. Abrí Pantalla / Kiosko. Si hay varias filas, elegí la tuya con el botón de lista (la dirección queda con `?device=` y el id de la fila). Anotá "Personas en fila" y "Espera estimada".
4. Abrí Flujo de Filas y contá las salidas de los últimos 15 minutos.
5. Calculá a mano y compará con el kiosko:
```text
ritmo  = salidas en 15 min / 15         ej. 20 / 15 = 1,33 personas por minuto
espera = aforo / ritmo                  ej. 8 / 1,33 ≈ 6 minutos  (el kiosko muestra ~6)
sin salidas en 15 min                   el kiosko muestra un guion
```
6. Anotá un caso donde el número engañe: llega mucha gente de golpe y todavía no salió nadie.

⚠️ En esta versión el pitido del Monitor en Vivo suena desde 8 personas, sin mirar el umbral, y Flujo de Filas pinta niveles fijos (Medio desde 4, Alto desde 7, Crítico desde 10). El estado que vale para el cliente es el del umbral configurado.

**Regla para quedarse**
La espera estimada es un promedio de los últimos 15 minutos, no una promesa al cliente.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- La ley de Little, con la prueba por áreas y la condición de estabilidad: https://third-bit.com/2026/05/30/littles-law/
- Historia: de 1954 a la prueba de 1961: https://en.wikipedia.org/wiki/Little%27s_law
- Otra forma de estimar la espera (FootfallCam): https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/
