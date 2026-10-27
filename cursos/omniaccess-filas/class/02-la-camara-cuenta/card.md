# Lección 2. La cámara cuenta

**Escuchá:** la-camara-cuenta.mp3 (2 min)

**La idea, en tres líneas**
- Vista lo más cenital posible, a más de 3 m, sin superficies que reflejen y con lugar antes y después de la zona: de frente, la gente se tapa y no se cuenta.
- Sobre la zona de la fila van tres tareas IVA: ocupación (cuántos hay) y entrada y salida de campo (cuántos pasaron).
- La tarea de ocupación se llama "Aforo": OmniAccess usa el nombre de la regla como canal, y la espera estimada, el reporte diario y el reseteo buscan ese nombre.

**Impacto:** el aforo arranca bien desde la instalación y la espera estimada y el reporte diario funcionan sin tocar nada más.

**Quién lo dice:** 2 de 4 fuentes separan ocupación de cruces (Keenfinity, Axis); la lista de ubicación es de Bosch (1 de 2, evidencia fina). Discrepa en la práctica la venta, que promete usar "las mismas cámaras del lugar" (manual de OmniAccess). Lo del nombre "Aforo" sale del código.

**Laboratorio** · Campo · 25 min
Cámara Bosch con IVA Pro de banco (ejemplo 192.0.2.10), PC con Configuration Manager 7.74 o superior.
1. Abrí la cámara en Configuration Manager y andá a VCA → Main Operation. Confirmá que el tipo de análisis sea IVA Pro Buildings.
2. En VCA → Tasks seleccioná la tarea por defecto (Detect moving objects) y borrala con el tacho.
3. Con el botón + agregá una tarea Occupancy. Dibujá la zona de la fila (un clic por vértice, doble clic para cerrar, hasta 16 nodos) y nombrala exactamente así:
```text
Aforo
```
4. Agregá sobre la misma zona una tarea de entrada al campo y otra de salida del campo (Entering field / Leaving field). El nombre es libre: OmniAccess las registra como "Entrada" y "Salida".
5. Si el cliente quiere que la cámara marque la zona llena, en la tarea de ocupación activá "Alarm on overcrowding" y cargá el valor crítico.
6. Guardá, pasá caminando por la zona dos o tres veces y mirá que el contador de ocupación suba y vuelva a cero.
7. En la configuración de red de la cámara dejá ONVIF habilitado y creá el usuario que va a usar OmniAccess. Anotá IP, usuario y clave para la lección 3.
```text
Cámara:   192.0.2.10   (HTTPS, puerto 443)
Usuario:  omniaccess   (clave de ejemplo: Cambiar.2026)
Tareas:   Aforo (Occupancy) · entrada · salida
```

⚠️ Escribir una configuración IVA nueva reinicia los contadores de la cámara. En un local abierto, hacelo fuera de horario.

**Regla para quedarse**
La tarea de ocupación se llama Aforo, y la cámara mira la fila desde arriba.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Planificar y configurar el conteo con IVA Pro (Keenfinity): https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Qué reglas IVA salen por ONVIF y con qué datos (Bosch): https://media.boschsecurity.com/fs/media/pb/media/partners_1/integration_tools_1/developer/Bosch-Metadata-and-IVA-Events.pdf
- Ocupación contra cruces en otra marca (Axis): https://developer.axis.com/analytics/axis-object-analytics-counting-data
