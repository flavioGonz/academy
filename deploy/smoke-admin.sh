set -e
# Prueba de humo del panel: crea una sesi??n temporal del primer admin, consulta la API y la borra.
pct exec 115 -- su -s /bin/bash www-data -c '
cd /tmp
SID=$(php -r "require \"/var/www/entrenamientos/api/lib.php\"; \$id=db()->query(\"SELECT id FROM users WHERE role=\x27admin\x27 AND active=1 ORDER BY id LIMIT 1\")->fetchColumn(); session_name(\"ies_training\"); session_save_path(data_dir().\"/sesiones\"); session_start(); \$_SESSION[\"uid\"]=(int)\$id; echo session_id(); session_write_close();")
for a in dashboard courses users audit; do
  printf "%-10s " $a
  wget -qO- --header "Cookie: ies_training=$SID" "http://127.0.0.1/api/admin.php?a=$a" | php -r "\$j=json_decode(stream_get_contents(STDIN),true); echo \$j===null?\"JSON INVALIDO\":(isset(\$j[\"error\"])?\"error: \".\$j[\"error\"]:implode(\",\",array_keys(\$j))), PHP_EOL;"
done
wget -qO- --header "Cookie: ies_training=$SID" "http://127.0.0.1/api/admin.php?a=dashboard" | php -r "\$j=json_decode(stream_get_contents(STDIN),true); echo json_encode(\$j[\"kpi\"]), PHP_EOL, count(\$j[\"courses\"]), \" cursos, \", count(\$j[\"days\"]), \" dias\", PHP_EOL;"
rm -f /var/www/entrenamientos-data/sesiones/sess_$SID
'
