# Lección 17. El portero avisa

**Escuchá:** el-portero-avisa.mp3 (2 min)

**La idea, en tres líneas**
- Action URL (R20A 320.30.11.47: `Device Management > Setting > Action URL`) manda un pedido HTTP a un servidor cuando pasa un evento: llamada, corte, relé, entrada, código, tarjeta, rostro, QR, intrusión o arranque.
- El equipo reemplaza variables antes de mandar: `$relay1status` (1 abierto, 0 cerrado), `$input1status`, `$code`, `$card_sn`, `$unlocktype`, `$remote`, `$mac`, `$ip`, `$model`, `$firmware`.
- `Setup Completed` no lo controla el interruptor general: si no se usa, el campo queda vacío. Los eventos disponibles cambian por modelo.

**Impacto:** el NVR, la domótica o un registro propio se enteran de cada apertura y cada tarjeta rechazada sin consultar al portero.

**Quién lo dice:** 2 de 2 fuentes coinciden (la guía de Akuvox y el ejemplo de ComfortClick con un E11R); evidencia escasa, así que se prueba en el modelo real.

**Laboratorio** · Foco · 15 min
1. En la PC de laboratorio (ejemplo 192.168.88.10) levantá un servidor que solo registre pedidos:
```bash
python3 -m http.server 8000 --bind 192.168.88.10
```
2. En el portero, `Action URL`: habilitado; cargá (reemplazando `<IP_SERVIDOR>` por la IP de la PC):
```text
Relay A Triggered   : http://<IP_SERVIDOR>:8000/relaytrigger=$relay1status
Relay A Closed      : http://<IP_SERVIDOR>:8000/relayclose=$relay1status
Valid Card Entered  : http://<IP_SERVIDOR>:8000/validcard=$card_sn
Setup Completed     : (vacío)
```
3. `Submit`, abrí la puerta con una tarjeta válida y mirá la terminal: llegan líneas `GET /validcard=...`, `GET /relaytrigger=1` y `GET /relayclose=0` (el servidor responde 404, no importa: lo que vale es la línea).
4. Sumá `mac=$mac:ip=$ip:model=$model` a una URL y fijate qué llega.
⚠️ `$card_sn` y `$code` viajan dentro de la URL: el servidor que los recibe va en la VLAN de porteros y no guarda esos logs a la vista.

**Regla para quedarse**
Lo que abre por HTTP también avisa por HTTP, a un servidor de la misma red.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Action URL, variables y la lista de eventos del X915V2: https://knowledge.akuvox.com/docs/set-up-action-url
- Un E11R integrado ida y vuelta por HTTP: https://www.comfortclick.com/Support/ExampleDetails/Akuvox
