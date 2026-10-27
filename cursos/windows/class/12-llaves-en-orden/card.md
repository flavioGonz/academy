# Lección 12. Llaves en orden

**Escuchá:** llaves-en-orden.mp3 (2 min)

**La idea, en tres líneas**
- Cada equipo con su administrador local único y recuperable (Windows LAPS si hay dominio), y el resto de las cuentas con lo mínimo: es la puerta de emergencia cuando el dominio no responde.
- La clave de recuperación de BitLocker se guarda fuera del equipo, y se suspende BitLocker antes de tocar BIOS, firmware o hardware: sin clave no hay recuperación.
- La contraseña DSRM de un controlador de dominio nunca va en texto plano en un script.

**Impacto:** una visita de emergencia que se resuelve en minutos y no un disco cifrado sin vuelta.

**Quién lo dice:** 4 de 4 fuentes coinciden en administrador local único y mínimo privilegio (TheITBros en dos páginas, Microsoft, TechTarget); BitLocker y DSRM salen de una fuente cada uno (LazyAdmin y la guía de instalación de AD DS de Microsoft); nadie discrepa.

**Laboratorio** · Admin · 15 min
En tu notebook o una VM con BitLocker activo en C: (si no lo tenés, hacé solo los pasos 1 y 5), PowerShell como administrador:
1. Estado de BitLocker y protectores:
```text
manage-bde -status C:
manage-bde -protectors -get C:
```
2. Anotá el ID del protector "Contraseña numérica" y copiá la clave de recuperación al gestor de contraseñas de la empresa, con el nombre del equipo.
3. Si el equipo está en dominio y la directiva lo permite, respaldá la clave en Active Directory:
```powershell
$kp = (Get-BitLockerVolume C:).KeyProtector | Where-Object KeyProtectorType -eq 'RecoveryPassword' | Select-Object -First 1
Backup-BitLockerKeyProtector -MountPoint C: -KeyProtectorId $kp.KeyProtectorId
```
4. Antes de una actualización de BIOS, suspendé BitLocker por un reinicio (se reanuda solo):
```powershell
Suspend-BitLocker -MountPoint C: -RebootCount 1
```
5. Quién es administrador local en este equipo:
```powershell
Get-LocalGroupMember -SID S-1-5-32-544
```
Si aparecen cuentas que nadie reconoce, anotalas y consultá antes de borrarlas.

⚠️ Nunca guardes la clave de recuperación solo en el mismo disco cifrado ni pegues contraseñas en texto plano en scripts o tickets.

**Regla para quedarse**
Ninguna llave vive solo dentro del equipo que protege.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Windows LAPS en Active Directory: https://theitbros.com/enable-windows-laps-in-active-directory/
- Dónde encontrar y respaldar la clave de BitLocker: https://lazyadmin.nl/it/bitlocker-recovery-key/
- Novedades de LAPS en Windows Server 2025: https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025
