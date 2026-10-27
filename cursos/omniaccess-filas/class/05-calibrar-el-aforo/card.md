# Lección 5. Calibrar el aforo

**Escuchá:** calibrar-el-aforo.mp3 (2 min)

**La idea, en tres líneas**
- "Señal del aforo" compara la curva cruda de la cámara con una estabilizada, cuenta los cambios por minuto y sugiere un tiempo de rebote (más de 8 cambios por minuto es parpadeo de más).
- "Zona y rebote en la cámara" (solo Bosch) edita sobre el video la zona de la fila, el rebote, la ventana anti doble conteo y el aforo crítico, y los escribe en la cámara.
- Cada escritura guarda antes un backup, relee la cámara y restaura sola si algo no coincide. Solo un administrador puede guardar.

**Impacto:** menos alertas falsas y un aforo que el cliente cree cuando lo mira.

**Quién lo dice:** 1 de 2 fuentes (Keenfinity) pide lugar antes y después del borde y evitar gente que merodea sobre la línea: es la razón del rebote y de la ventana. Evidencia fina en la web; las pantallas y valores salen del código de OmniAccess.

**Laboratorio** · Foco · 20 min
Fila de prueba con gente pasando (o vos caminando), usuario con rol ADMIN.
1. Abrí Calibración → pestaña "Señal del aforo". Elegí la ventana de 30 min.
2. Anotá los cuatro números: Cambios crudos, Cambios estabilizado, Cambios por minuto y Amplitud (máx − mín). Anotá el "Tiempo de rebote sugerido".
```text
Cambios por minuto   rebote sugerido
hasta 4              1 s
más de 4             1,5 s
más de 8             2 s
más de 15            2,5 s
más de 30            3 s
```
3. Pasá a la pestaña "Zona y rebote en la cámara". Mirá "Medición del rebote" en 1 h: parpadeo del aforo, rebote en el borde y entradas de menos de 10 s.
4. Si la zona corta la fila, arrastrá sus puntos (doble clic agrega uno, clic derecho lo quita; entre 3 y 16 puntos).
5. Llevá "Rebote de la zona" al valor sugerido. Si hay gente que sale y vuelve enseguida, subí la "Ventana anti doble conteo" (por ejemplo 20 s).
6. Tocá "Guardar en la cámara" y confirmá. Revisá que en "Backups de la cámara" aparezca el respaldo nuevo.
7. Esperá 30 min de actividad y volvé a "Señal del aforo": los cambios por minuto tendrían que bajar.

⚠️ Guardar en la cámara aplica la configuración al instante y reinicia sus contadores. En un local abierto, hacelo en un momento tranquilo y avisá al supervisor.

**Regla para quedarse**
Primero mido el parpadeo, después toco la cámara, y siempre con backup.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Dónde dibujar zonas y líneas para contar bien (Keenfinity): https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Por qué ningún contador es exacto y cómo se compensa (FootfallCam): https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/
