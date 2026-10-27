# Lección 12. Backup primero

**Escuchá:** backup-primero.mp3 (2 min)

**La idea, en tres líneas**
- Antes de actualizar, backup. Siempre. En saltos de versión mayor, de a una (5.x a 6.x, sin saltear) y un backup guardado por cada versión: el downgrade del controlador es reinstalar y un backup nuevo no entra en una versión vieja.
- Backup automático en Settings > Maintenance > Backup Schedule, guardado fuera del controlador (servidor de archivos/SFTP).
- Migración (v6.2.10 y posteriores): exportar, importar en el destino, migrar equipos con la IP o Inform URL nueva, y Forget en el viejo solo cuando todos estén Connected. Misma versión Major.Minor.Patch.

**Impacto:** un controlador quemado o un upgrade fallido se resuelve restaurando, no rehaciendo la obra.

**Quién lo dice:** 4 de 7 fuentes sobre firmware coinciden en backup previo y saltos de a una versión; el ritmo de firmware se discute: un usuario del foro de Lawrence Systems vio una sola actualización de switch en un año, mientras TP-Link ofrece canales Beta y RC.

**Laboratorio** · Admin · 20 min
Con el controlador de laboratorio (Lección 2) y un segundo contenedor o VM limpia de la misma versión:
1. **Settings > Maintenance > Backup Schedule**: activalo, semanal, domingo 3:00, contenido **Configuration**; si tenés un SFTP de laboratorio, elegí **Save to File Server**.
2. Exportá un backup a mano y guardalo con la versión en el nombre:
```text
omada-lab_v6.2.10.17_2026-10-27.cfg
```
3. En Docker (compose en /opt/omada), copiá también el volumen de datos con el contenedor detenido:
```bash
cd /opt/omada && docker compose stop
sudo tar czf ~/omada-data-$(date +%F).tar.gz -C /var/lib/docker/volumes/omada_omada-data/_data .
docker compose start
```
4. En el controlador nuevo: en el asistente creá una cuenta local, y en el paso siguiente elegí **Restore from Backup File** con el `.cfg`. La cuenta creada se reemplaza por la del backup.
5. Verificá sitios, redes y SSID. Si querés probar la migración con equipos, usá **Global View > Settings > Migration** y seguí el orden: exportar, importar, migrar equipos, Forget al final.
⚠️ Antes de cualquier upgrade de controlador o de firmware en producción: backup descargado fuera del equipo, notas de la versión leídas y ventana de mantenimiento. Beta y RC solo en laboratorio.

**Regla para quedarse**
Antes de actualizar, backup. Siempre. Y uno guardado por cada versión.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Migración de sitio y controlador (v6.2.10 y posteriores): https://www.tp-link.com/us/support/faq/3589
- Upgrade y downgrade del controlador hardware y software: https://tp-link.com/support/faq/3684
- Backup programado y restore en Docker: https://lazyadmin.nl/home-network/omada-controller-docker/
