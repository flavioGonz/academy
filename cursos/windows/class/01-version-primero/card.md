# Lección 1. Versión primero

**Escuchá:** version-primero.mp3 (2 min)

**La idea, en tres líneas**
- Lo primero que se anota de un Windows es edición, versión y build, antes que la IP.
- Desde Windows 11 24H2 y en Windows Server 2025 la firma SMB es obligatoria, y Windows 11 Pro ya no entra como invitado a carpetas sin usuario.
- Un NAS, grabador o pendrive en router que "dejó de abrir" después de actualizar suele ser esto, no la red.

**Impacto:** en soporte dejás de buscar cables cuando el problema es una política de seguridad del sistema.

**Quién lo dice:** 2 de 2 fuentes coinciden (evidencia fina): la documentación de Microsoft sobre Server 2025 y The Register citando a Ned Pyle; nadie discrepa, y Microsoft prefiere actualizar o reemplazar el equipo viejo antes que bajar la seguridad.

**Laboratorio** · Rápido · 10 min
En tu notebook o en una VM con Windows 11 o Windows Server 2025:
1. Abrí Ejecutar (Win+R), escribí `winver` y anotá versión y build.
2. En PowerShell, sacá los mismos datos por registro (sirve también por escritorio remoto):
```powershell
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' |
  Select-Object EditionID, DisplayVersion, CurrentBuild, UBR
```
3. Mirá cómo está el cliente SMB:
```powershell
Get-SmbClientConfiguration |
  Select-Object RequireSecuritySignature, EnableInsecureGuestLogons
```
4. Anotá en tu planilla de obra: edición, DisplayVersion (por ejemplo 24H2 o 25H2), build y los dos valores de SMB.
5. Si tenés un NAS o grabador viejo a mano, probá abrir su carpeta con `\\IP\carpeta` y con usuario y contraseña propios del equipo.

⚠️ Volver a permitir invitados o quitar la firma SMB deja el equipo más expuesto; primero firmware del NAS o del grabador, o una cuenta con contraseña.

**Regla para quedarse**
Lo primero que anoto de un Windows es edición, versión y build.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Firma SMB obligatoria y fin del invitado en 24H2: https://www.theregister.com/2024/05/30/windows_11_24h2_security_tweaks/
- Novedades de Windows Server 2025 (SMB, LAPS, OpenSSH): https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025
