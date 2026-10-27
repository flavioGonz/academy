# Lección 12. Docker sin sorpresas

**Escuchá:** docker-sin-sorpresas.mp3 (2 min)

**La idea, en tres líneas**
- Panorama: imagen (el software empaquetado), contenedor (la imagen corriendo), volumen (los datos que sobreviven), red de Docker (cómo se hablan los contenedores).
- Los puertos publicados con `-p` se saltean ufw: Docker los redirige en la tabla nat antes de que lleguen a las reglas de ufw.
- Publicá en `127.0.0.1` salvo que haya un motivo; lo público va detrás de un proxy inverso o filtrado en la cadena DOCKER-USER, y se verifica desde otra máquina.

**Impacto:** los paneles y servicios en contenedores (monitoreo, automatización, gestores) no quedan abiertos a internet por un firewall que solo parecía cerrado.

**Quién lo dice:** 4 de 6 fuentes sobre Docker coinciden, incluida la documentación oficial de Docker; ninguna discrepa. La cifra de Ollama expuestos es de Intruder (mayo de 2026), citada por findstack.

**Laboratorio** · Foco · 20 min
En una VM de prueba con ufw activo en deny (lección 8) y otra VM en la misma red para escanear:
1. Instalá Docker desde el repositorio de Ubuntu:
```bash
sudo apt install docker.io
sudo docker version | grep -m1 Version
```
2. Publicado en todas las interfaces (la forma riesgosa):
```bash
sudo docker run -d -p 8080:80 nginx          # anotá el ID que devuelve
sudo ss -tlnp | grep 8080          # 0.0.0.0:8080
sudo ufw status                    # no dice nada del 8080
```
3. Desde la OTRA VM:
```bash
nmap -Pn -p 8080,8081 192.168.88.50   # 8080 abierto pese a ufw
```
4. Publicado solo para el host:
```bash
sudo docker run -d -p 127.0.0.1:8081:80 nginx
sudo ss -tlnp | grep 8081          # 127.0.0.1:8081
curl -sI 127.0.0.1:8081 | head -1  # responde en el servidor
```
Repetí el nmap desde la otra VM: 8081 ya no aparece abierto.
5. Volumen para datos que sobreviven al contenedor:
```bash
sudo docker volume create datos-prueba
sudo docker volume inspect datos-prueba     # Mountpoint en /var/lib/docker/volumes
```
6. Limpieza:
```bash
sudo docker ps                    # lista los contenedores
sudo docker rm -f ID1 ID2         # los dos IDs de prueba
```
⚠️ No pongas "iptables": false en la configuración de Docker: según su documentación rompe la red de los contenedores y deja sus puertos accesibles desde la red local.

**Regla para quedarse**
Todo puerto de contenedor va a 127.0.0.1 salvo que haya un motivo, y lo verifico desde otra red.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Docker y ufw, en la documentación oficial de Docker: https://docs.docker.com/engine/network/packet-filtering-firewalls/
- El caso n8n y las tres formas de arreglarlo: https://findstack.com/resources/ufw-not-blocking-docker-ports
- DOCKER-USER, 127.0.0.1 y persistencia en after.rules: https://www.ssdnodes.com/learn/docker-ports-bypass-ufw
- Docker para administradores en Ubuntu Server (volúmenes, redes, logs): https://documentation.ubuntu.com/server/how-to/containers/docker-for-system-admins/
