cat > /tmp/gzip.conf <<'EOF'
gzip on;
gzip_vary on;
gzip_comp_level 6;
gzip_min_length 1024;
gzip_proxied any;
gzip_types text/css application/javascript application/json image/svg+xml text/plain;
EOF
pct push 115 /tmp/gzip.conf /etc/nginx/conf.d/entrenamientos-gzip.conf
pct exec 115 -- bash -c 'sed -i "s/^\s*gzip on;/# gzip on; (ver conf.d)/" /etc/nginx/nginx.conf; nginx -t 2>&1 | tail -1 && systemctl reload nginx && echo recargado'
