# Lección 2. Host dedicado

**Escuchá:** host-dedicado.mp3 (2 min)

**La idea, en tres líneas**
- Si el controlador es software propio, que viva en un equipo dedicado que no se duerma ni se reinicie por su cuenta.
- En Docker (imagen comunitaria mbentley/omada-controller, no oficial) usá red host: el descubrimiento es broadcast y no cruza la red bridge.
- Controlador 6.x pide CPU con AVX (no Raspberry Pi 4 ni NAS viejos), unos 2 GB de RAM y tiempo para que MongoDB cierre limpio.

**Impacto:** los equipos aparecen solos para adoptar y el controlador no deja la red sin gestión un domingo.

**Quién lo dice:** 4 de 5 fuentes de instalación coinciden en el host dedicado; el fabricante no publica imagen Docker y recomienda hardware o nube si no querés mantener un host.

**Laboratorio** · Foco · 20 min
En una VM Linux (Debian/Ubuntu) con Docker y el plugin Compose, en la misma subred que un EAP de laboratorio:
1. Verificá AVX:
```bash
grep -o -m1 avx /proc/cpuinfo || echo "SIN AVX: usar mbentley/omada-controller:5"
```
2. Creá el compose:
```bash
sudo mkdir -p /opt/omada && cd /opt/omada
cat > docker-compose.yml <<'EOF'
services:
  omada-controller:
    image: mbentley/omada-controller:6.2
    container_name: omada-controller
    network_mode: host
    restart: unless-stopped
    stop_grace_period: 60s
    environment:
      - TZ=America/Montevideo
    volumes:
      - omada-data:/opt/tplink/EAPController/data
      - omada-logs:/opt/tplink/EAPController/logs
volumes:
  omada-data:
  omada-logs:
EOF
docker compose up -d && docker logs -f omada-controller
```
3. Esperá la línea de arranque con la versión (1 a 2 minutos) y entrá a `https://<IP-de-la-VM>:8043`.
4. En el asistente elegí **Create a Local Account**, región **Uruguay** y zona horaria correcta.
5. Verificá que el EAP aparezca en Devices como Pending.
⚠️ Para actualizar: `docker compose pull && docker compose up -d`. Nunca `docker compose down -v`: borra los volúmenes con toda la configuración.

**Regla para quedarse**
Controlador propio en host dedicado, red host, CPU con AVX y sesenta segundos para apagar.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía probada con Omada 6.2.10.17 en Docker, con HTTPS: https://computingforgeeks.com/omada-controller-docker/
- Docker, backups, puertos y el problema de AVX en Raspberry Pi: https://lazyadmin.nl/home-network/omada-controller-docker/
- La historia de la PC que se dormía y la migración a un equipo dedicado: https://whitkirkchurch.org.uk/tech-blog/2021/08/installing-an-omada-sdn-controller-on-a-raspberry-pi-using-docker/
