# Lección 11. Portero blindado

**Escuchá:** portero-blindado.mp3 (2 min)

**La idea, en tres líneas**
- Un portero es cámara, micrófono y relé en la calle: no se expone a internet y vive en su propia VLAN.
- Desde esa VLAN habla solo con la central, el NVR y la gestión; claves propias en web, RTSP, ONVIF y HTTP, y `Prevent SIP Hacking` activado.
- La central también se asegura: clave fuerte, lista blanca de IP para la web, SRTP y TLS cuando los equipos lo soportan.

**Impacto:** el portero deja de ser la puerta de entrada a la red del cliente y una vulnerabilidad futura queda encerrada en una VLAN.

**Quién lo dice:** 3 de 11 fuentes de seguridad coinciden en no exponer (Claroty, CISA); Yeastar documenta registro remoto con reenvío de puertos y SmartPlus requiere salida a internet.

**Laboratorio** · Campo · 20 min
1. Armá la VLAN de porteros (ejemplo 10.10.10.0/24) con este esquema de reglas:
```text
VLAN porteros 10.10.10.0/24
  -> central   10.10.20.10   UDP 5060, UDP RTP (rango configurado)
  -> NVR       10.10.30.10   TCP 554 (RTSP)
  -> gestión   10.10.40.0/28 TCP 80/443
  todo lo demás: denegado. Ningún reenvío de puertos desde WAN.
```
2. Desde una PC de la red de usuarios, escaneá el portero:
```bash
nmap -sS -sU -p T:22,23,80,443,554,5060,8080,U:5060,8500 10.10.10.21
```
3. Todo lo que responda desde la red de usuarios es un hueco: filtralo en el firewall y volvé a escanear.
4. En el portero: clave web propia, RTSP con Digest, ONVIF con usuario propio, MJPEG con autorización.
5. `Account > Advanced > Call`: activá `Prevent SIP Hacking` y verificá que la central esté en contactos.
6. Revisá que el firmware sea el último de su modelo y hardware.
⚠️ Escaneá solo equipos propios o con autorización escrita del cliente.

**Regla para quedarse**
El portero vive en su VLAN, sin puertos abiertos desde internet, y solo habla con la central, el NVR y la gestión.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Las 13 vulnerabilidades del E11 y las recomendaciones: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar
- Aviso de CISA ICSA-23-068-01: https://www.cisa.gov/news-events/ics-advisories/icsa-23-068-01
- Seguridad de la central Grandstream UCM: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/
