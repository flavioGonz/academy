# Lección 4. Troncal registrado

**Escuchá:** troncal-registrado.mp3 (2 min)

**La idea, en tres líneas**
- Proveedor con usuario y contraseña: Register SIP Trunk. Peer es para unir centrales por IP; Account, para equipos que se registran en tu UCM.
- El estado se ve en System Status > Dashboard; "Rejected" es alcance al servidor o credenciales.
- Heartbeat activo, codecs recortados a los del proveedor y, para el troncal registrado, sin reenvío de puertos.

**Impacto:** troncales que registran a la primera y caídas que se detectan antes de que llame el cliente.

**Quién lo dice:** 3 de 3 fuentes coinciden en Register y verificación en el Dashboard (guía oficial, Simtex, Telnyx); lo de recortar codecs y no abrir puertos lo afirma un solo proveedor, Simtex.

**Laboratorio** · Foco · 15 min
1. Creá el troncal con los datos de tu cuenta de prueba (los de abajo son de ejemplo).
```text
Extension/Trunk > VoIP Trunks > Add
Type: Register SIP Trunk
Provider Name: Proveedor_Lab
Host Name: sip.proveedor.example
Username / Auth ID: 21000000
Password: (la del proveedor, copiada y pegada)
```
2. Guardá, aplicá y entrá a Advanced Settings:
```text
Codec Preference: PCMA, PCMU (sacá el resto)
DTMF Mode: RFC4733
Enable Heartbeat Detection: Sí   Heartbeat Frequency: 60
```
3. Revisá el estado en System Status > Dashboard (Trunks). Si dice Rejected, volvé a pegar usuario y contraseña y probá que el host del proveedor resuelve y responde desde una PC en la misma red de la central.
4. Hacé las cuatro pruebas: saliente, entrante desde un celular, caller ID mostrado y DTMF dejando un mensaje en un buzón.

**Regla para quedarse**
Un troncal se da por terminado con cuatro pruebas: sale, entra, muestra bien el número y pasa los tonos.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de troncales SIP: https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/
- Ejemplo completo de un proveedor (Simtex): https://www.simtex.com.au/support/kb/pbx-setup-guides/grandstream-ucm-sip-trunk-configuration
- Guía de Telnyx para UCM6xxx: https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series
