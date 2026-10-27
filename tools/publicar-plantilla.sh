set -e
# Plantilla: __SLUG__, __MD5__ (md5 del JSON del servidor del que se partió), __PROBE__ (una ilustración a probar).
# Antes: pvex put de <slug>.json a /tmp/__SLUG__.json, importar-curso.php a /tmp y glosario a /tmp/glosario.json.
S=__SLUG__
H=$(pct exec 115 -- md5sum /var/www/entrenamientos/data/$S.json | cut -c1-32)
[ "$H" = "__MD5__" ] || { echo "OJO: $S.json cambió en el servidor ($H); no importo"; exit 1; }
if [ -f /tmp/glosario.json ]; then
  pct push 115 /tmp/glosario.json /var/www/entrenamientos/data/glosario.json --perms 0644
  pct exec 115 -- chown www-data:www-data /var/www/entrenamientos/data/glosario.json
  rm -f /tmp/glosario.json
fi
pct push 115 /tmp/$S.json /tmp/$S.json --perms 0644
pct push 115 /tmp/importar-curso.php /tmp/importar-curso.php --perms 0644
pct exec 115 -- su -s /bin/sh www-data -c "php /tmp/importar-curso.php $S /tmp/$S.json --forzar"
pct exec 115 -- rm -f /tmp/$S.json
rm -f /tmp/$S.json
wget -qO- http://172.26.20.218/data/catalog.json | python3 -c "import json,sys;c=json.load(sys.stdin);print([(x['slug'],len(x['lessons'])) for x in c['courses'] if x['slug']=='$S'])"
for u in /data/glosario.json __PROBE__ "/api/course.php?slug=$S"; do printf "%-40s " "$u"; wget -q -S -O /dev/null "http://172.26.20.218$u" 2>&1 | awk '/HTTP\//{print $2}' | tail -1; done
