# Lección 1. Qué cuenta Filas

**Escuchá:** que-cuenta-filas.mp3 (2 min)

**La idea, en tres líneas**
- La cámara Bosch con IVA Pro cuenta: ocupación de la zona de la fila y cruces de entrada y salida.
- OmniAccess Filas lee esos eventos por ONVIF, los guarda, los muestra (monitor, kiosko, app) y avisa cuando se pasa el umbral.
- Filas es un modo exclusivo (Modo Cola): al activarlo cambia el menú entero y se apagan LPR y Face.

**Impacto:** cuando el número está mal sabés que empieza en la cámara, y cuando no llega sabés que es el camino.

**Quién lo dice:** 3 de 4 fuentes coinciden en que la analítica vive en la cámara y sale como evento (Bosch, Keenfinity, Axis). FootfallCam recuerda que ningún contador es exacto. El funcionamiento de OmniAccess sale del código (octubre de 2026).

**Laboratorio** · Admin · 15 min
Hacelo en una instalación de prueba o demo, nunca en una con LPR en uso.
1. Entrá como administrador y abrí Configuración → Modos (LPR / Face / Cola).
2. Elegí la pestaña "Modo Cola", tocá "Activar" y confirmá con "Sí, cambiar". La aplicación se recarga.
3. Recorré el menú lateral y anotá qué hace cada ítem:
```text
Monitor en Vivo        cámaras de fila con su aforo
Flujo de Filas         eventos del día, entradas y salidas
Filas                  zonas VCA, tabla en vivo, umbrales
Despachos              cola de avisos enviados
Reportes               afluencia por hora, día, semana, mes
Dispositivos Conteo    alta de cámaras de fila
Horarios de Filas      reseteo de contadores a la apertura
Pantalla / Kiosko      cartel de sala (PASE / AGUARDE)
Calibración            zona, rebote y señal del aforo
```
4. Dibujá en una hoja los cuatro pasos: cámara → evento → monitor → alerta. Al lado de cada paso escribí la pantalla donde lo ves.
5. Si tenés acceso al servidor de la demo, mirá los procesos:
```bash
pm2 status   # omniaccess-web, omniaccess-webhooks, dispatch-worker
```

⚠️ Cambiar de modo en un sistema en uso apaga el modo anterior para todos los usuarios. Se coordina con el cliente.

**Regla para quedarse**
El número nace en la cámara; OmniAccess lo transporta, lo guarda y lo muestra.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo cuenta IVA Pro y cómo se leen los datos (Keenfinity): https://knowledge.keenfinity-group.com/video-systems/article/how-to-set-up-count-with-iva-pro-fw-9-40-and-get-the-data-from-the-camera
- Profile M y la gestión de filas como caso de uso (ONVIF, 2020): https://www.onvif.org/?p=4937
- Ningún contador es perfecto (FootfallCam): https://www.footfallcam.com/blog/2024/03/redefining-queue-analytics-a-big-data-modelling-approach/
