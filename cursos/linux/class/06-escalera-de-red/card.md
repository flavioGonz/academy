# Lección 6. Escalera de red

**Escuchá:** escalera-de-red.mp3 (2 min)

**La idea, en tres líneas**
- Diagnóstico en escalera: interfaz con IP, gateway, IP pública, nombre (DNS), puerto. El primer escalón que falla es el problema.
- iproute2 reemplaza a net-tools: `ip addr`, `ip route`, `ip neigh`, `ss` (en vez de ifconfig, route, arp, netstat).
- IP fija: netplan en Ubuntu Server (`netplan try` revierte solo a los 120 s) y `/etc/network/interfaces` en Debian servidor.

**Impacto:** dejás de reportar "no anda internet" y pasás a decir en qué capa se corta, con evidencia.

**Quién lo dice:** 4 de 5 fuentes de red coinciden en iproute2 y en el diagnóstico por capas (Debian Reference, Debian Handbook, linuxconfig, ssdnodes). La Debian Reference lista netplan también como opción para Debian, aunque minoritaria.

**Laboratorio** · Campo · 15 min
En una VM de laboratorio (red de ejemplo 192.168.88.0/24, gateway 192.168.88.1):
1. Subí la escalera y anotá el resultado de cada escalón:
```bash
ip -br addr                     # 1. ¿la interfaz tiene IP?
ip route                        # ¿hay ruta default?
ping -c3 192.168.88.1           # 2. gateway
ping -c3 1.1.1.1                # 3. IP pública
ping -c3 debian.org             # 4. nombre
dig debian.org +short           # ¿qué resuelve?
ss -tlnp                        # 5. qué escucha y en qué dirección
curl -sI deb.debian.org | head -3   # 5. un servicio real
```
2. IP fija en Ubuntu con netplan (archivo propio, permisos 600):
```yaml
# /etc/netplan/90-ies.yaml   (interfaz: la que muestra ip -br addr)
network:
  version: 2
  ethernets:
    ens18:
      dhcp4: false
      addresses: [192.168.88.50/24]
      routes:
        - to: default
          via: 192.168.88.1
      nameservers:
        addresses: [192.168.88.1, 1.1.1.1]
```
```bash
sudo chmod 600 /etc/netplan/90-ies.yaml
sudo netplan generate          # valida la sintaxis
sudo netplan try               # sin Enter en 120 s, vuelve atrás
```
3. Equivalente en Debian 13 con ifupdown:
```text
# /etc/network/interfaces
auto ens18
iface ens18 inet static
    address 192.168.88.50/24
    gateway 192.168.88.1
```
⚠️ En Debian no hay try: cambiá la IP remota solo con acceso de consola (la de Proxmox o la VM) a mano.

**Regla para quedarse**
Subo la escalera de abajo hacia arriba, sin saltear escalones, y en remoto cambio la red con netplan try.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Netplan en Ubuntu 26.04: archivos, YAML, try y diagnóstico: https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04
- Comandos de red seguros y tabla de iproute2 en la Debian Reference: https://www.debian.org/doc/manuals/debian-reference/ch05.en.html
- Configuración de red con ifupdown en el Debian Handbook: https://www.debian.org/doc/manuals/debian-handbook/sect.network-config.en.html
