# Lección 14. Quién puede abrir

**Escuchá:** quien-puede-abrir.mp3 (2 min)

**La idea, en tres líneas**
- `Setting > HTTP API` (todos los porteros) ofrece None (solo pruebas), Allowlist (IP permitidas, red local), Basic (en claro) y Digest (credencial protegida); Normal es interno de Akuvox.
- Un usuario propio por integración, nunca admin: la clave en la URL puede quedar en logs de proxies o del equipo.
- Todo dentro de la VLAN de porteros (lección 11), nada publicado a internet, y HTTPS donde el equipo lo soporte.

**Impacto:** cuando un integrador o un empleado deja la obra, se cambia una sola credencial y nadie más pierde acceso.

**Quién lo dice:** 3 de 5 fuentes coinciden en credenciales propias con Digest o Allowlist (Akuvox HTTP API, guía LPR, pylocal-akuvox); discrepan la guía de apertura de Akuvox, que permite dejarlo en blanco, y el foro LogicMachine, que usa admin.

**Laboratorio** · Admin · 15 min
1. En el portero de laboratorio: `Setting > HTTP API`, habilitado, modo `Digest`, usuario `api-lab`, clave `Ejemplo-Api-2026`, `Submit`.
2. En una PC de la misma VLAN: `pip install pylocal-akuvox` y este script (de la guía de la librería, con tus datos):
```python
import asyncio
from pylocal_akuvox import AkuvoxDevice, AuthConfig, AuthMethod

async def main():
    auth = AuthConfig(method=AuthMethod.DIGEST, username="api-lab", password="Ejemplo-Api-2026")
    async with AkuvoxDevice("192.168.88.21", auth=auth) as device:
        info = await device.get_info()
        print(info.model, info.firmware_version)

asyncio.run(main())
```
3. Cambiá la clave del script por una mala y mirá el error de autenticación.
4. Armá la tabla de credenciales del sitio:
```text
Integración        Usuario        Mecanismo                 Origen permitido
Home Assistant     ha-porton      Open Relay via HTTP       10.10.40.5
Central            pbx-porton     Open Relay via HTTP       10.10.20.10
Cámara LPR         lpr-porton     HTTP API (Allowlist)      10.10.30.21
```
⚠️ None y "usuario en blanco" quedan solo para la mesa de laboratorio; en producción, nunca.

**Regla para quedarse**
Un usuario por integración, ninguno es admin, y solo se habla desde la VLAN de porteros.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Los cinco modos de la HTTP API: https://knowledge.akuvox.com/docs/configure-http-api
- Autenticación, logs y TLS vistos desde una librería cliente: https://pylocal-akuvox.readthedocs.io/en/latest/quickstart.html
- Lo que no conviene copiar: admin en la URL y alta seguridad apagada: https://forum.logicmachine.net/showthread.php?tid=6156
