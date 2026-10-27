pct push 115 /tmp/crear-admin.php /tmp/crear-admin.php --perms 0644
pct exec 115 -- su -s /bin/sh www-data -c 'php /tmp/crear-admin.php "Nicolás Mármol" nicolas@ies.com.uy'
pct exec 115 -- rm -f /tmp/crear-admin.php
pct exec 115 -- ls -la /var/www/entrenamientos-data
