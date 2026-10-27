set -e
# Contenido solo para registrados: los cursos completos salen por /api/course.php (con sesión) y
# /capturas/ e /ilustraciones/ pasan por /api/gate.php (auth_request). catalog.json sigue público.
pct exec 115 -- bash -c '
set -e
nginx -V 2>&1 | grep -q http_auth_request_module && echo "auth_request: ok" || { echo "FALTA http_auth_request_module"; exit 1; }
S=/etc/nginx/sites-available/entrenamientos
cp $S /root/entrenamientos.nginx.$(date +%Y%m%d-%H%M%S).bak
cat > $S <<'"'"'NGX'"'"'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name entrenamientos.ies.com.uy _;
    root /var/www/entrenamientos;
    index index.html;
    client_max_body_size 70m;
    server_tokens off;

    # IP real del visitante detras del Nginx Proxy Manager
    set_real_ip_from 172.26.20.17;
    real_ip_header X-Forwarded-For;

    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;

    location ~ /\. { deny all; }
    location = /api/config.php { deny all; }
    location = /api/lib.php { deny all; }

    # control de acceso interno (nginx pregunta si hay sesion)
    location = /api/gate.php {
        internal;
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.4-fpm.sock;
        fastcgi_pass_request_body off;
        fastcgi_param CONTENT_LENGTH "";
    }

    location ^~ /api/ {
        location ~ ^/api/[a-z0-9_-]+\.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/run/php/php8.4-fpm.sock;
        }
        return 404;
    }

    # los cursos completos solo por la API (con sesion); el catalogo es publico
    location ~ ^/data/(?!catalog\.json$)[^/]+\.json$ { return 403; }

    # capturas: imagenes, GIF y videos; solo con sesion; nunca se ejecuta nada
    location ^~ /capturas/ {
        auth_request /api/gate.php;
        location ~* \.(png|jpe?g|webp|gif|mp4|webm)$ { expires 30d; add_header Cache-Control "private"; try_files $uri =404; }
        return 404;
    }

    # ilustraciones de las lecciones: solo con sesion
    location ^~ /ilustraciones/ {
        auth_request /api/gate.php;
        location ~* \.(webp|png|jpe?g|svg|gif)$ { expires 7d; add_header Cache-Control "private"; try_files $uri =404; }
        return 404;
    }

    location ~* \.(css|js|svg|png|jpe?g|webp)$ { expires 7d; add_header Cache-Control "public"; }
    location ~* \.json$ { add_header Cache-Control "no-cache"; }
    location / { try_files $uri $uri/ =404; }
}
NGX
if nginx -t 2>/dev/null; then systemctl reload nginx; echo nginx-ok; else nginx -t; cp $(ls -t /root/entrenamientos.nginx.*.bak | head -1) $S; echo "nginx -t fallo, restaurado"; exit 1; fi
'
IP=172.26.20.218
for u in /data/catalog.json /data/mikrotik.json "/api/course.php?slug=mikrotik" /api/gate.php /capturas/akuvox/01/index.json /ilustraciones/mikrotik/4.webp /logos/; do printf "%-36s " "$u"; wget -q -S -O /dev/null "http://$IP$u" 2>&1 | awk '/HTTP\//{print $2}' | tail -1; echo; done
