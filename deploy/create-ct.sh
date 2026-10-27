set -e
ID=115
if pct status $ID >/dev/null 2>&1; then echo "CT $ID ya existe"; pct status $ID; exit 0; fi
pct create $ID local:vztmpl/debian-13-standard_13.1-2_amd64.tar.zst \
  --hostname entrenamientos --cores 1 --memory 1024 --swap 512 \
  --rootfs local-lvm:16 --net0 name=eth0,bridge=vmbr0,ip=dhcp,firewall=0 \
  --unprivileged 1 --features nesting=1 --onboot 1 --start 1 \
  --description "IES Training - portal de cursos (entrenamientos.ies.com.uy). nginx + php-fpm. Creado por Claude 2026-10-27."
sleep 8
for i in $(seq 1 20); do IP=$(pct exec $ID -- sh -c "ip -4 -o addr show eth0 | awk '{print \$4}' | cut -d/ -f1"); [ -n "$IP" ] && break; sleep 2; done
echo "IP=$IP"
pct exec $ID -- ping -c1 -W2 172.26.20.1 >/dev/null && echo "gateway ok"
