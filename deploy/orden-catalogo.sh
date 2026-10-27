set -e
# Ubica paradox y bosch-incendio después de hikcentral en el orden del catálogo (el resto queda igual).
pct exec 115 -- su -s /bin/bash www-data -c 'php -r "
require \"/var/www/entrenamientos/api/lib.php\";
\$f=\"/var/www/entrenamientos/data/catalog.json\"; \$c=json_decode(file_get_contents(\$f),true);
\$o=array_values(array_diff(\$c[\"order\"],[\"paradox\",\"bosch-incendio\"]));
\$i=array_search(\"hikcentral\",\$o); array_splice(\$o,\$i===false?count(\$o):\$i+1,0,array_values(array_intersect([\"paradox\",\"bosch-incendio\"],array_column(\$c[\"courses\"],\"slug\"))));
\$c[\"order\"]=\$o; atomic_write(\$f,json_encode(\$c,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)); echo implode(\" \",\$o),PHP_EOL;"'
