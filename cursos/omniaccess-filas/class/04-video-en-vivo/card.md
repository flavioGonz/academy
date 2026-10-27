# Lección 4. Video en vivo

**Escuchá:** video-en-vivo.mp3 (2 min)

**La idea, en tres líneas**
- go2rtc toma el RTSP de la cámara una vez y lo entrega al navegador como MP4 por HTTP (`/go2rtc/api/stream.mp4`), sin WebSocket.
- OmniAccess pide el stream por nombre: `bosch_` más la IP con guiones bajos. Ese stream se carga a mano en go2rtc.yaml.
- El mismo stream alimenta el anillo de grabación del que salen los clips de las alertas: sin stream no hay vivo ni clip.

**Impacto:** el vivo de la fila anda en el monitor, en el kiosko de alerta y en la app, y las alertas salen con clip.

**Quién lo dice:** 2 de 3 fuentes coinciden en pedir el segundo stream y en cómo se arma la URL (documento RTSP de Bosch, go2rtc). Puertos 1984 y 8554 según la documentación de go2rtc. El nombre del stream, el reintento y el clip salen del código y de la guía de instalación de OmniAccess.

**Laboratorio** · Foco · 20 min
Servidor de prueba con go2rtc y la cámara de banco 192.0.2.10.
1. En la cámara, dejá el stream 2 en H.264 (así el navegador lo reproduce sin transcodificar).
2. En el archivo go2rtc.yaml de la instalación agregá el stream con el nombre exacto:
```yaml
streams:
  bosch_192_0_2_10: rtsp://omniaccess:Cambiar.2026@192.0.2.10/rtsp_tunnel?p=1&line=1&inst=2&vcd=2
```
3. Reiniciá y comprobá que go2rtc lo ve:
```bash
systemctl restart go2rtc
curl -s 127.0.0.1:1984/api/streams
```
4. Abrí la interfaz web de go2rtc (puerto 1984) desde la red del servidor y reproducí `bosch_192_0_2_10`.
5. En OmniAccess abrí Filas y Monitor en Vivo: el video tiene que aparecer con las zonas VCA dibujadas encima.
6. Probá la falla: renombrá el stream, reiniciá go2rtc y recargá Filas. Después de unos reintentos aparece "Cámara offline · Sin señal · reintentando…" con una foto cada 5 s. Volvé el nombre a su lugar.
7. Si usás el proxy inverso, revisá que la ruta `/go2rtc/` apunte al puerto 1984 del servidor (127.0.0.1:1984).

⚠️ go2rtc.yaml guarda la clave de la cámara en texto: permisos de lectura solo para el servicio, y nunca en una captura de pantalla para el cliente.

**Regla para quedarse**
El stream de una cámara de fila se llama bosch_ y la IP con guiones bajos, y si no está, no hay vivo ni clip.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Parámetros RTSP de Bosch: inst, line, rtsp_tunnel, vcd: https://knowledge.keenfinity-group.com/video-systems/article/how-is-rtsp-usage-supported-with-bosch-vip-devices
- go2rtc: configuración, puertos y stream.mp4: https://pkg.go.dev/github.com/AlexxIT/go2rtc
- RTSP 2.0 (RFC 7826): https://datatracker.ietf.org/doc/html/rfc7826
