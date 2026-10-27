# Lección 8. Deny por defecto

**Escuchá:** deny-por-defecto.mp3 (2 min)

**La idea, en tres líneas**
- Entrante denegado por defecto, saliente permitido, y se abre solo lo que el equipo sirve; SSH se permite antes de activar, idealmente solo desde la red de gestión.
- Ubuntu: ufw (instalado, deshabilitado de fábrica). Debian 13: nftables con `/etc/nftables.conf` y `systemctl enable nftables`.
- Antes de filtrar, que el servicio no escuche donde no hace falta; el firewall es la segunda capa.

**Impacto:** el servidor, gateway o appliance solo responde a lo que tiene que responder, y desde donde corresponde.

**Quién lo dice:** 4 de 7 fuentes sobre firewall coinciden (Ubuntu Server, Debian Handbook, ssdnodes, findstack). Discrepan en la herramienta: Ubuntu enseña ufw y Debian enseña nftables directo.

**Laboratorio** · Campo · 15 min
En una VM de prueba, con la consola abierta (red de gestión de ejemplo 10.10.10.0/24):
1. ¿Qué escucha y dónde?
```bash
sudo ss -tlnp      # 0.0.0.0 o [::] = todas las interfaces; 127.0.0.1 = solo local
```
2. Opción Ubuntu con ufw:
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 10.10.10.0/24 to any port 22 proto tcp
sudo ufw enable
sudo ufw status numbered
```
3. Opción Debian 13 con nftables (equivalente mínimo):
```text
#!/usr/sbin/nft -f
# /etc/nftables.conf
flush ruleset
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif lo accept
    ip saddr 10.10.10.0/24 tcp dport 22 accept
    icmp type echo-request accept
    meta l4proto ipv6-icmp accept     # IPv6 no funciona sin ICMPv6
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output  { type filter hook output priority 0; policy accept; }
}
```
```bash
sudo nft -c -f /etc/nftables.conf      # valida sin aplicar
sudo systemctl enable nftables && sudo systemctl restart nftables
sudo nft list ruleset
```
4. Verificá desde OTRA máquina, no desde el servidor:
```bash
nc -zv 192.168.88.50 22
nmap -Pn -p 22,80,443 192.168.88.50
```
⚠️ En un equipo remoto, cargá el firewall con la consola a mano: una regla de SSH mal escrita te deja afuera.

**Regla para quedarse**
Primero permito SSH desde la red de gestión, después activo el firewall, y lo verifico desde otra máquina.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- ufw en Ubuntu Server, reglas por origen y NAT: https://documentation.ubuntu.com/server/how-to/security/firewalls/
- nftables en Debian, tablas, cadenas y arranque: https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html
