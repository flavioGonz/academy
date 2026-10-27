# Lección 9. RTSP al NVR

**Escuchá:** rtsp-al-nvr.mp3 (2 min)

**La idea, en tres líneas**
- El portero entrega dos streams RTSP: `/live/ch00_0` (principal, 2048 kbps por defecto) y `/live/ch00_1` (secundario, 512 kbps), H.264 a 25 fps.
- También se agrega por ONVIF (`/onvif/device_service`), cuyo usuario de fábrica es admin / admin.
- RTSP, ONVIF y MJPEG (puerto 8080) llevan credencial propia; si cambia la del RTSP, el monitor que lo mira necesita la misma.

**Impacto:** el portero queda grabado en el NVR del cliente como una cámara más, sin abrir una puerta trasera al video.

**Quién lo dice:** 1 de 1 fuente (capítulo Monitor and Image de la guía del E16); evidencia escasa, sin discrepancias. Falta un caso de practicante con un NVR concreto.

**Laboratorio** · Rápido · 10 min
1. Desde la PC, probá los dos streams (VLC o ffprobe):
```bash
ffprobe -hide_banner "rtsp://192.168.88.21/live/ch00_0"
ffprobe -hide_banner "rtsp://192.168.88.21/live/ch00_1"
```
2. En la web del portero: `Surveillance > RTSP > RTSP Basic`, RTSP Authorization activado, modo Digest, usuario `nvr-lab`, clave `Ejemplo-Rtsp-2026`.
3. Volvé a probar con credenciales:
```bash
ffprobe -hide_banner "rtsp://nvr-lab:Ejemplo-Rtsp-2026@192.168.88.21/live/ch00_1"
```
4. `Surveillance > ONVIF`: Discoverable activado y usuario/clave propios (no admin / admin).
5. En el NVR, agregá el portero por ONVIF o como RTSP manual con la ruta `ch00_1` para la grilla.
6. Activá `MJPEG Authorization` si no se usa el acceso MJPEG por 8080.
7. Si un monitor mira este portero por RTSP, actualizá su usuario y clave en `Device > Monitor`.

**Regla para quedarse**
El NVR graba el stream secundario salvo que haga falta detalle, y ninguno de los tres accesos al video queda con admin / admin.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- RTSP, ONVIF, MJPEG y parámetros de video del portero: https://knowledge.akuvox.com/docs/monitor-and-image-13
