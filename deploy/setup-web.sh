set -e
ID=115
pct exec $ID -- bash -c 'export DEBIAN_FRONTEND=noninteractive; apt-get update -qq && apt-get install -y -qq nginx php-fpm php-mbstring unattended-upgrades >/dev/null && echo instalado'
PHPV=$(pct exec $ID -- sh -c "ls /etc/php | sort -V | tail -1")
echo "PHP $PHPV"
pct exec $ID -- mkdir -p /var/www/entrenamientos
cat > /tmp/entrenamientos.nginx <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name entrenamientos.ies.com.uy _;
    root /var/www/entrenamientos;
    index index.html;
    client_max_body_size 10m;
    server_tokens off;

    # IP real del visitante detras del Nginx Proxy Manager
    set_real_ip_from 172.26.20.17;
    real_ip_header X-Forwarded-For;

    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;

    location ~ /\. { deny all; }
    location = /api/config.php { deny all; }

    location ^~ /api/ {
        location ~ ^/api/[a-z0-9_-]+\.php\$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/run/php/php${PHPV}-fpm.sock;
        }
        return 404;
    }

    # capturas: solo imagenes, nunca se ejecuta nada
    location ^~ /capturas/ {
        location ~* \.(png|jpe?g|webp|gif)\$ { expires 30d; add_header Cache-Control "public"; try_files \$uri =404; }
        return 404;
    }

    location ~* \.(css|js|svg|png|jpe?g|webp)\$ { expires 7d; add_header Cache-Control "public"; }
    location ~* \.json\$ { add_header Cache-Control "no-cache"; }
    location / { try_files \$uri \$uri/ =404; }
}
EOF
pct push $ID /tmp/entrenamientos.nginx /etc/nginx/sites-available/entrenamientos
pct exec $ID -- bash -c "rm -f /etc/nginx/sites-enabled/default; ln -sf /etc/nginx/sites-available/entrenamientos /etc/nginx/sites-enabled/entrenamientos; sed -i 's/^upload_max_filesize.*/upload_max_filesize = 10M/; s/^post_max_size.*/post_max_size = 12M/' /etc/php/$PHPV/fpm/php.ini; nginx -t && systemctl enable --now php$PHPV-fpm nginx >/dev/null 2>&1; systemctl restart php$PHPV-fpm nginx; echo '<!doctype html><title>IES Training</title><p>Instalando…</p>' > /var/www/entrenamientos/index.html; chown -R www-data:www-data /var/www/entrenamientos"
pct exec $ID -- sh -c "curl -s -o /dev/null -w 'http %{http_code}\n' http://127.0.0.1/ || wget -qO- http://127.0.0.1/ | head -c 80"
