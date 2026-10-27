# Lección 1. Quién manda

**Escuchá:** quien-manda.mp3 (2 min)

**La idea, en tres líneas**
- La configuración vive en el controlador de cada sitio (Cloud Gateway, CloudKey o UniFi OS Server). Site Manager en unifi.ui.com es la puerta, no el cerebro.
- Cada dispositivo tiene un solo host. Un UDM o UCG corre su propio Network y no se gestiona desde un servidor central.
- Desde UniFi Network 11.0 el Network Server clásico queda afuera: el self-hosted es UniFi OS Server, y Network 11 pide UniFi OS 6.0 o superior.

**Impacto:** elegís el controlador correcto antes de cotizar y no migrás a los seis meses.

**Quién lo dice:** 3 de 4 fuentes coinciden en que cada sitio tiene su controlador y Site Manager solo conecta; nadie lo discute, aunque las fuentes de hosting (UniHosted) empujan el controlador central.

**Laboratorio** · Admin · 15 min
1. Creá una VM Ubuntu 24.04 con 2 vCPU, 2 GB de RAM y 10 GB libres (mínimos publicados por Ubiquiti, según UniHosted). Hyper-V no está soportado.
2. Bajá el instalador de UniFi OS Server (build x86-64 o ARM64) desde la página de descargas de Ubiquiti y corrélo:
```bash
sudo apt update
sudo apt install -y podman slirp4netns
chmod +x ./<instalador-uos-server>
sudo ./<instalador-uos-server>
```
3. Al terminar, el instalador indica la dirección de acceso (https, IP de la VM, por ejemplo 10.10.10.5, y el puerto). Abrila, creá el admin local y entrá a UniFi Network.
4. Anotá en tu planilla: versión de UniFi OS, versión de Network y, para el sitio de prueba, quién es el host de cada equipo:
```text
Equipo        Host
Gateway       UXG / terceros / UCG (en ese caso el UCG es el controlador)
Switches      UniFi OS Server 10.10.10.5
APs           UniFi OS Server 10.10.10.5
```
⚠️ No clones esta VM para armar otro cliente: los clones comparten los tokens de acceso remoto de Site Manager.

**Regla para quedarse**
Antes de cotizar, escribo quién es el host de cada equipo del sitio.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Notas oficiales de UniFi Network 11.0.97, fin del Network Server: https://community.ui.com/releases/UniFi-Network-Application-11-0-97/15662d06-8122-44e2-a1ba-af5d71b8a045
- UniFi OS Server, requisitos y límites: https://www.unihosted.com/blog/unifi-os-server
- Site Manager frente al controlador de cada sitio: https://www.unihosted.com/blog/unifi-site-management
