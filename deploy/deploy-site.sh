set -e
# Uso: copiar el paquete a pve01:/tmp/ies-entrenamientos-site.tgz y ajustar SHA y DATOS abajo.
# DATOS=0 no toca data/ (los cursos editados desde el panel quedan como están).
ID=115
SHA="__SHA__"
DATOS="__DATOS__"
echo "$SHA  /tmp/ies-entrenamientos-site.tgz" | sha256sum -c -
pct exec $ID -- bash -c 'export DEBIAN_FRONTEND=noninteractive; dpkg -s php8.4-sqlite3 >/dev/null 2>&1 || apt-get install -y -qq php-sqlite3 >/dev/null 2>&1; systemctl restart php8.4-fpm'
pct push $ID /tmp/ies-entrenamientos-site.tgz /root/site.tgz
pct exec $ID -- bash -c "
set -e
W=/var/www/entrenamientos
D=/var/www/entrenamientos-data
TS=\$(date +%Y%m%d-%H%M%S)
mkdir -p /root/respaldos \$D
tar czf /root/respaldos/web-\$TS.tgz -C \$W --exclude=capturas . 2>/dev/null || true
tar czf /root/respaldos/datos-\$TS.tgz -C \$D . 2>/dev/null || true
if [ '$DATOS' = '1' ]; then tar xzf /root/site.tgz -C \$W; else tar xzf /root/site.tgz -C \$W --exclude=./data; fi
mkdir -p \$W/capturas
chown -R www-data:www-data \$W \$D
find \$W -type d -exec chmod 755 {} +; find \$W -type f -exec chmod 644 {} +
chmod 750 \$D; chmod 640 \$W/api/config.php
grep -q 'api/lib.php' /etc/nginx/sites-available/entrenamientos || sed -i 's#location = /api/config.php { deny all; }#location = /api/config.php { deny all; }\n    location = /api/lib.php { deny all; }#' /etc/nginx/sites-available/entrenamientos
nginx -t 2>&1 | tail -1 && systemctl reload nginx
echo desplegado
"
IP=172.26.20.218
for u in / /data/catalog.json /api/auth.php?a=me /api/lib.php /api/config.php; do printf "%-28s " "$u"; wget -q -S -O /dev/null "http://$IP$u" 2>&1 | awk '/HTTP\//{print $2}' | tail -1; done
