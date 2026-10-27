# Lección 2. Extensión sólida

**Escuchá:** extension-solida.mp3 (2 min)

**La idea, en tres líneas**
- La contraseña SIP la genera la central (Enable Random Password): 10 caracteres o más, con mayúscula, minúscula, número y especial.
- Registros concurrentes: 3 por defecto, hasta 10. Solo los que se usen.
- En Media: NAT activado y Direct Media apagado, como viene; DTMF en RFC4733.

**Impacto:** menos extensiones adivinables y menos audio cortado por teléfonos que intentan hablarse directo a través de NAT.

**Quién lo dice:** 2 de 2 fuentes oficiales coinciden (manual del UCM630x y manual de seguridad); no se encontró quién discrepe. Evidencia delgada en cantidad.

**Laboratorio** · Rápido · 10 min
1. Activá la contraseña aleatoria para extensiones nuevas.
```text
PBX Settings > General Settings > Enable Random Password: Sí
```
2. Creá tres extensiones de prueba (1001, 1002, 1003) en Extension/Trunk > Extensions > Add. Verificá que la contraseña SIP se completó sola.
3. En cada una, revisá:
```text
Basic Settings > Concurrent Registrations: 1 o 2 si no hay app Wave (por defecto 3)
Media > NAT: activado
Media > Enable Direct Media: desactivado
Media > DTMF Mode: RFC4733
```
4. Exportá la lista de extensiones y guardala con el resto de la documentación del cliente.
⚠️ Cambiar la contraseña de una extensión en producción desregistra el teléfono hasta que se reprovisiona.

**Regla para quedarse**
La contraseña de la extensión la genera la central y la carga el teléfono; ninguna persona la inventa.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Parámetros de extensión SIP en el manual del UCM630x: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Seguridad de extensiones (contraseñas, SRTP, ZRTP): https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/
