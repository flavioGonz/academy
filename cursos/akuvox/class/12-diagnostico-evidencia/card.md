# Lección 12. Diagnóstico con evidencia

**Escuchá:** diagnostico-evidencia.mp3 (2 min)

**La idea, en tres líneas**
- Ante "no registra, no abre, no se ve": log de la central, captura PCAP del portero y versión de firmware, antes de tocar nada.
- La PCAP del portero guarda solo 1 MB: se arranca justo antes de reproducir la falla.
- Soporte de Akuvox pide firmware, configuración exportada, log en nivel 7, PCAP y topología; con eso el ticket avanza.

**Impacto:** fallas que antes llevaban visitas enteras se resuelven leyendo un log, y los tickets al fabricante no vuelven pidiendo datos.

**Quién lo dice:** 2 de 3 fuentes coinciden (portal de soporte de Akuvox y comunidad FreePBX); el caso de la vista previa muestra el método en la práctica.

**Laboratorio** · Foco · 20 min
1. Rompé el registro a propósito: cambiá una letra de la contraseña SIP del portero.
2. En la central (Asterisk/FreePBX), mirá el error:
```bash
asterisk -rvvv
pjsip set logger on
# esperar el REGISTER del portero y buscar "Failed to authenticate"
```
3. En la web del portero, sección de diagnóstico o upgrade avanzado: log level 7, PCAP Start.
4. Reproducí la falla (reiniciá la cuenta SIP), PCAP Stop y Export.
5. Abrí la captura en Wireshark con el filtro:
```text
sip.Method == "REGISTER" || sip.Status-Code == 401 || sip.Status-Code == 403
```
6. Armá la carpeta del ticket:
```text
ticket-portero/
  firmware.txt        (Status > Product Information)
  config-export.tgz
  syslog-nivel7.log
  captura.pcap
  topologia.png
```
7. Corregí la contraseña y verificá el registro.

**Regla para quedarse**
Sin firmware, configuración, log y captura no hay ticket, y sin captura no hay diagnóstico de llamadas.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Qué pide soporte de Akuvox y cómo sacar log y PCAP: https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-
- La vista previa que se rompía por una opción del Dial: https://community.freepbx.org/t/early-media-doorphone-video-preview/99698
- Recuperar la clave web en porteros de un botón: https://ticket.akuvox.com/support/solutions/articles/48001156051-how-to-reset-the-web-password-for-single-button-series-door-phone-
