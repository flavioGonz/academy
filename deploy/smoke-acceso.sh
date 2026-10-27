set -e
# Prueba de acceso: sin sesión solo temario; con sesión curso completo, capturas e ilustraciones.
pct exec 115 -- su -s /bin/bash www-data -c '
cd /tmp
SID=$(php -r "require \"/var/www/entrenamientos/api/lib.php\"; \$id=db()->query(\"SELECT id FROM users WHERE active=1 ORDER BY id LIMIT 1\")->fetchColumn(); session_name(\"ies_training\"); session_save_path(data_dir().\"/sesiones\"); session_start(); \$_SESSION[\"uid\"]=(int)\$id; echo session_id(); session_write_close();")
CAP=$(ls /var/www/entrenamientos/capturas/akuvox/01/*.png 2>/dev/null | head -1 | sed "s#/var/www/entrenamientos##")
for who in visitante sesion; do
  H=""; [ $who = sesion ] && H="--header=Cookie: ies_training=$SID"
  printf "%-10s course.php locked=" $who; wget -qO- "$H" "http://127.0.0.1/api/course.php?slug=akuvox" | php -r "\$j=json_decode(stream_get_contents(STDIN),true); echo var_export(\$j[\"course\"][\"locked\"],true), \" lecciones=\", count(\$j[\"course\"][\"lessons\"]), \" lab=\", isset(\$j[\"course\"][\"lessons\"][0][\"lab\"][\"md\"])?\"si\":\"no\", PHP_EOL;"
  printf "%-10s captura %s -> " $who "$CAP"; wget -q -S -O /dev/null "$H" "http://127.0.0.1$CAP" 2>&1 | awk "/HTTP\\//{print \$2}" | tail -1
done
rm -f /var/www/entrenamientos-data/sesiones/sess_$SID
'
