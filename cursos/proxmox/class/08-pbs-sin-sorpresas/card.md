# Lección 8. PBS sin sorpresas

**Escuchá:** pbs-sin-sorpresas.mp3 (2 min)

**La idea, en tres líneas**
- **Prune** decide qué backups se quedan; **garbage collection** libera el espacio (con un día de gracia); **verify** detecta corrupción, y también ransomware.
- Proxmox VE se conecta a PBS con un usuario que tiene el rol **DatastoreBackup**: puede crear backups pero no borrarlos.
- Retención generosa al principio y una copia fuera del sitio con **sync job** (regla 3-2-1).

**Impacto:** el datastore no se llena por sorpresa y un host comprometido no puede borrar tus copias.

**Quién lo dice:** 5 de 7 fuentes sobre PBS coinciden en prune, GC y verify; Thomas Krenn conecta PVE con `root@pam`, mientras Hake Hardware y la doc de PBS prefieren un usuario dedicado y restringido.

**Laboratorio** · Admin · 20 min
En el PBS (web en el puerto 8007, datastore de ejemplo `main`):
1. Prune job con retención (ajustala al cliente; podés probarla en el Prune Simulator de la doc):
```bash
proxmox-backup-manager prune-job create diario --store main --schedule '21:30' --keep-last 3 --keep-daily 13 --keep-weekly 8 --keep-monthly 11
```
2. Garbage collection semanal y verify diario que reverifica cada 30 días:
```bash
proxmox-backup-manager datastore update main --gc-schedule 'sun 02:00'
proxmox-backup-manager verify-job create verif-main --store main --schedule '01:00' --ignore-verified true --outdated-after 30
```
3. Usuario de backup con token y permiso solo de escritura (la contraseña es de ejemplo):
```bash
proxmox-backup-manager user create backup@pbs --password 'Ejemplo.Cambiar.2026'
proxmox-backup-manager user generate-token backup@pbs pve
proxmox-backup-manager acl update /datastore/main DatastoreBackup --auth-id 'backup@pbs!pve'
```
4. En Proxmox VE: **Datacenter → Storage → Add → Proxmox Backup Server**, con el token `backup@pbs!pve`, el secreto y el fingerprint del dashboard de PBS.
5. Lanzá un backup de prueba y mirá en PBS que aparezca en **Content**.

⚠️ Guardá el secreto del token en el gestor de contraseñas: PBS lo muestra una sola vez.

**Regla para quedarse**
En PBS programo prune, GC y verify el mismo día que creo el datastore.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Prune, garbage collection y verify, doc oficial: https://pbs.proxmox.com/docs/maintenance.html
- Ransomware y regla 3-2-1 en PBS: https://pbs.proxmox.com/docs/storage.html
- Guía completa con usuario DatastoreBackup y horarios: https://hakedev.substack.com/p/complete-proxmox-backup-server-setup
