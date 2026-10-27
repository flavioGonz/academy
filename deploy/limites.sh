set -e
# Sube los límites de carga (GIF de hasta 30 MB, videos de hasta 60 MB) y permite servir mp4/webm en /capturas/.
ID=115
pct exec $ID -- bash -c '
set -e
S=/etc/nginx/sites-available/entrenamientos
cp $S /root/entrenamientos.nginx.bak
sed -i "s/client_max_body_size [0-9]*m;/client_max_body_size 70m;/" $S
grep -q "webp|gif|mp4|webm)" $S || sed -i "s/webp|gif)/webp|gif|mp4|webm)/" $S
sed -i "s/# capturas: solo imagenes, nunca se ejecuta nada/# capturas: imagenes, GIF y videos; nunca se ejecuta nada/" $S
I=/etc/php/8.4/fpm/php.ini
sed -i "s/^upload_max_filesize = .*/upload_max_filesize = 64M/; s/^post_max_size = .*/post_max_size = 70M/" $I
grep -nE "client_max_body_size|mp4" $S
grep -E "^(upload_max_filesize|post_max_size)" $I
if nginx -t 2>/dev/null; then systemctl reload nginx; else cp /root/entrenamientos.nginx.bak $S; echo "nginx -t fallo, restaurado"; exit 1; fi
systemctl restart php8.4-fpm
echo limites-ok
'
