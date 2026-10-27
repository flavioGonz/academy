# Lección 18. Abrir desde sistemas

**Escuchá:** abrir-desde-sistemas.mp3 (2 min)

**La idea, en tres líneas**
- Cualquier cliente HTTP abre: se prueba con curl y se muda a Home Assistant (`rest_command`), MikroTik (`/tool/fetch`) o Asterisk (`CURL()` en el dialplan).
- El cliente habla el mismo método que el equipo: Home Assistant y MikroTik usan basic por defecto y pasan a digest con `authentication: digest` o `http-auth-scheme=digest`.
- Cámaras de patentes abren por la HTTP API en Allowlist (Hikvision solo con X912 912.30.12.114 o R29 29.30.10.745 en adelante). En UCM y HikCentral no hay acción HTTP documentada en las páginas leídas: DTMF o un intermediario.

**Impacto:** el portón se abre desde el sistema que el cliente ya usa, y cada apertura queda atada a un usuario que se puede cambiar.

**Quién lo dice:** 7 de 7 fuentes coinciden en que cualquier cliente HTTP sirve (Home Assistant, MikroTik, Asterisk, pylocal-akuvox, ComfortClick, guía LPR, guía EC33); 3 de 7 marcan igualar basic o digest. Ninguna documenta UCM ni HikCentral.

**Laboratorio** · Foco · 20 min
Reemplazá `<IP_PORTERO>`, `<USUARIO>` y `<CLAVE>` por los de tu laboratorio; un usuario distinto por sistema.
1. curl (si responde 401 con basic, agregá `--digest`):
```bash
curl -s -u 'curl-lab:Ejemplo-Curl-2026' "192.168.88.21/fcgi/OpenDoor?action=OpenDoor&DoorNum=2"
```
2. MikroTik RouterOS 7 (el `\?` evita que la consola abra la ayuda):
```routeros
/tool/fetch url="http://<IP_PORTERO>/fcgi/OpenDoor\?action=OpenDoor&DoorNum=2" user=mk-porton password="Ejemplo-MK-2026" output=none
```
3. Home Assistant, `configuration.yaml`, reiniciar y llamar `rest_command.abrir_porton`:
```yaml
rest_command:
  abrir_porton:
    url: "http://<IP_PORTERO>/fcgi/OpenDoor?action=OpenDoor&DoorNum=2"
    method: get
    username: "ha-porton"
    password: "Ejemplo-HA-2026"
    authentication: basic
```
4. Asterisk o FreePBX (extensión de prueba):
```text
exten => 7001,1,Set(RESP=${CURL(http://<USUARIO>:<CLAVE>@<IP_PORTERO>/fcgi/OpenDoor?action=OpenDoor&DoorNum=2)})
 same => n,Hangup()
```
5. Actualizá la tabla de credenciales de la lección 14.
⚠️ La extensión 7001 abre el portón: restringila en la central a los internos que corresponda.

**Regla para quedarse**
Pruebo con curl, lo muevo al sistema y anoto quién tiene cada credencial.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Home Assistant rest_command (basic o digest): https://www.home-assistant.io/integrations/rest_command
- MikroTik /tool/fetch y http-auth-scheme: https://manual.mikrotik.com/docs/system-information-and-utilities/fetch/
- Asterisk CURL(): https://docs.asterisk.org/Latest_API/API_Documentation/Dialplan_Functions/CURL/
- Cámaras de patentes por la HTTP API: https://knowledge.akuvox.com/docs/integration-with-milesight-lpr-camera-for-door-opening
