set -e
# Plantilla: reemplazar __SLUG__ y __FORZAR__ ("" o "--forzar"). Antes: pvex put de <slug>.json e importar-curso.php a /tmp de pve01.
S=__SLUG__
pct push 115 /tmp/$S.json /tmp/$S.json --perms 0644
pct push 115 /tmp/importar-curso.php /tmp/importar-curso.php --perms 0644
pct exec 115 -- su -s /bin/sh www-data -c "php /tmp/importar-curso.php $S /tmp/$S.json __FORZAR__"
pct exec 115 -- rm -f /tmp/$S.json
wget -qO- http://172.26.20.218/data/catalog.json | python3 -c "import json,sys;c=json.load(sys.stdin);print([(x['slug'],len(x['lessons']),x.get('logo')) for x in c['courses'] if x['slug']=='$S'])"
