# Lección 10. Portal cautivo

**Escuchá:** portal-cautivo.mp3 (2 min)

**La idea, en tres líneas**
- Portal en Site Settings > Authentication > Portal: sin autenticación, clave simple, Hotspot (voucher, usuario local, SMS, RADIUS, formulario), RADIUS (servidor incorporado desde 5.12), LDAP externo o portal externo.
- El portal autentica mientras el controlador esté corriendo; en la nube, además, con licencia vigente.
- Pre-Authentication Access deja pasar URLs o subredes antes de autenticar; Authentication-Free Client exceptúa IPs o MACs.

**Impacto:** hoteles y salas de espera con acceso controlado y sin dictar la clave del WiFi en recepción.

**Quién lo dice:** 2 de 3 fuentes sobre portal coinciden en que depende del controlador corriendo; la guía de upgrade al controlador SDN 4.1.5 muestra que el portal hubo que reconfigurarlo a mano tras un salto grande. No se encontró discrepancia.

**Laboratorio** · Foco · 15 min
Con un controlador v6 y un EAP:
1. **Network Config > WLAN**: SSID `Huespedes-Lab`, abierto o WPA2 con clave de ejemplo, en la VLAN de invitados (Lección 7).
2. **Site Settings > Authentication > Portal > Create New Portal**:
```text
Portal Name: Huespedes
SSID & Network: Huespedes-Lab
Authentication Type: Hotspot
Hotspot Option: Voucher
HTTPS Redirection: activado
Landing Page: la URL original que pidió el cliente
```
3. En **Portal Customization** cargá un logo y un texto de bienvenida; mirá la vista previa de celular.
4. **Access Control**: activá **Pre-Authentication Access** y agregá la URL del sitio del cliente. Activá **Authentication-Free Client** y agregá la MAC de un equipo de prueba.
5. En la sección **Voucher** del portal, generá 2 códigos de 1 día y probá uno desde un celular.
⚠️ Si el controlador se apaga, los clientes nuevos no pueden autenticarse: en hotelería, controlador dedicado y backup al día.

**Regla para quedarse**
Portal sin controlador no autentica: después de cada upgrade grande, probalo con un celular.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Configuración de portal en controlador v5.9 a v6: https://support.omadanetworks.com/en/document/13285/
- Certificado propio para el portal (pfx único): https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/
- Cambios de portal al pasar al controlador SDN: https://www.omadanetworks.com/us/omada-sdn/controller-upgrade/
