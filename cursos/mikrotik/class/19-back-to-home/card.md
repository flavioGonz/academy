# Lección 19. Back To Home

**Escuchá:** back-to-home.mp3 (2 min)

**La idea, en tres líneas**
- Back To Home convierte al router en servidor WireGuard: con IP pública el cliente entra directo; sin IP pública (CGNAT) entra por un relay de MikroTik, cifrado de punta a punta y a veces más lento.
- Solo en CPU ARM, ARM64 o TILE con RouterOS 7.12 o posterior: los RouterBOARD MIPS quedan afuera. Mirá `architecture-name` antes de prometerlo.
- Un usuario por dispositivo; `allow-lan=no` (por defecto) da solo internet a través del router; la LAN se da a quien la necesita, con `client-allowed-address` acotado y `expires` si es temporal.

**Impacto:** acceso remoto a un sitio con CGNAT sin VPS ni puertos abiertos, y bajas individuales cuando alguien pierde el celular.

**Quién lo dice:** 2 de 3 fuentes coinciden (documentación de Back To Home y de Cloud, y un distribuidor canadiense); ninguna discrepa. La propia documentación recomienda WireGuard a mano (lección 8) cuando hace falta control fino.

**Laboratorio** · Foco · 20 min
En un RouterBOARD ARM o ARM64 con RouterOS 7 y configuración por defecto (LAN 192.168.88.0/24):
1. Arquitectura y activación:
```routeros
/system/resource/print
/ip/cloud/set back-to-home-vpn=enabled
/ip/cloud/print
```
Esperá `vpn-status: running`. Mirá `vpn-dns-name` y `vpn-relay-ipv4-status` (directo o por relay).
2. Usuario para el celular de un técnico, con acceso a la LAN y vencimiento:
```routeros
/ip/cloud/back-to-home-user/add name=tecnico-lucia allow-lan=yes client-allowed-address=192.168.88.0/24 expires=30d comment="Celular Lucia"
/ip/cloud/back-to-home-user/show-client-config [find name=tecnico-lucia]
```
3. En el celular, con datos móviles, importá el QR en la app WireGuard (o en la app Back To Home) y conectá. Probá entrar a 192.168.88.1 por WinBox o al NVR de ejemplo en 192.168.88.50.
4. Usuario de solo internet, para comparar:
```routeros
/ip/cloud/back-to-home-user/add name=invitado allow-lan=no expires=1d
```
Con este, la LAN no tiene que responder.
5. Revisá que tus redes locales estén en la lista LAN (de eso depende la restricción):
```routeros
/interface/list/member/print where list=LAN
```
6. Para dar de baja a una persona: `/ip/cloud/back-to-home-user/remove [find name=invitado]`.

⚠️ `back-to-home-vpn=revoked-and-disabled` borra todos los usuarios y claves; al reactivarlo hay claves y puerto nuevos y cada teléfono se configura otra vez. Para una baja, borrá el usuario, no revoques todo.

**Regla para quedarse**
Un usuario por equipo, la LAN solo a quien la necesita, y nunca revoco para dar una baja.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Back To Home en RouterOS 7.25: app, usuarios, relays y lo que agrega al router: https://manual.mikrotik.com/docs/7.25/network-management/cloud/back-to-home/
- Back To Home frente al doble NAT y equipos soportados: https://www.wirelessnetware.ca/blog/back-to-home-with-mikrotik/
- Cómo el router llega a la nube y a los relays: https://manual.mikrotik.com/docs/7.25/network-management/cloud/
